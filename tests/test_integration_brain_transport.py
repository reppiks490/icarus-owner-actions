"""Read-only collector behavior under source drift, missing pages and hostile metadata."""
from __future__ import annotations

import base64
import copy
from datetime import datetime, timezone
import hashlib
import json
import threading

import pytest

from integration_brain.transport import GitHubResponse, TransportError, collect_snapshot, GhClient

ENGINE = 'reppiks490/Icarus-engine'
BUS = 'reppiks490/icarus-owner-actions'
A, B, C = 'a'*40, 'b'*40, 'c'*40
UTC = '2026-10-20T18:20:00Z'


def blob(raw):
    return hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()


def file_response(path, document=None, raw=None):
    raw = raw if raw is not None else (json.dumps(document,sort_keys=True)+'\n').encode()
    return dict(type='file',path=path,encoding='base64',size=len(raw),sha=blob(raw),content=base64.b64encode(raw).decode())


class Client:
    def __init__(self):
        self.lock = threading.Lock()
        self.calls = []
        self.counts = {}
        self.routes = {}
        self.documents = dict(schema_version='icarus-federated-repo-evidence-v1',
            required_for_every_ai_unit=True,authority='RESEARCH_EVIDENCE_ONLY',repositories=[
                dict(repository=ENGINE,role='data',data_authority='CANONICAL_LEDGER_AND_COLLECTION',evidence_paths=['AGENTS.md']),
                dict(repository=BUS,role='bus',data_authority='GOVERNANCE_EVIDENCE_ONLY',evidence_paths=['coordination/owner_status.json'])])
        self.routes[f'repos/{ENGINE}/contents/config/federated_repo_evidence.json?ref={A}']=file_response('config/federated_repo_evidence.json',self.documents)
        status=dict(schema_version='icarus-coordination-owner-status-v1',updated_at_utc=UTC,live_broker_arming=False)
        session=dict(schema_version='icarus-coordination-session-v2',session_id='icarus1-fixture',actor='Icarus 1',model_family='openai',goal='Restart readiness',home_repo=BUS,branch='icarus1/restart',started_at_utc=UTC,stale_after_minutes=1440,capabilities=['github'],initial_dependencies=[])
        event=dict(schema_version='icarus-coordination-event-v2',event_id='claim',session_id='icarus1-fixture',at_utc=UTC,type='CLAIM',phase='repair',summary='Reserved restart scope',repos=[BUS],targets=[dict(repo=BUS,path='runtime.py')],dependencies=[],evidence=[],next_action='Verify',coordination_mode='independent',cooperates_with=[])
        paths={'coordination/owner_status.json':status,'coordination/sessions/icarus1-fixture.json':session,'coordination/events/2026/10/20/icarus1-fixture/claim.json':event}
        tree=[]
        for path,doc in paths.items():
            response=file_response(path,doc)
            self.routes[f'repos/{BUS}/contents/{path}?ref={B}']=response
            tree.append(dict(path=path,mode='100644',type='blob',sha=response['sha'],size=response['size']))
        self.routes[f'repos/{BUS}/git/commits/{B}']=dict(sha=B,tree=dict(sha=C))
        self.routes[f'repos/{BUS}/git/trees/{C}?recursive=1']=dict(sha=C,truncated=False,tree=tree)
        self.routes[f'repos/{ENGINE}/contents/AGENTS.md?ref={A}']=file_response('AGENTS.md',raw=b'PRIVATE_PAYLOAD_MARKER\n')
        for repo,commit in ((ENGINE,A),(BUS,B)):
            self.routes[f'repos/{repo}/git/ref/heads/main']=dict(ref='refs/heads/main',object=dict(type='commit',sha=commit))
            self.routes[f'repos/{repo}/pulls?state=open&per_page=100&page=1']=[]
            self.routes[f'repos/{repo}/actions/runs?per_page=100&page=1']=dict(total_count=0,workflow_runs=[])

    def get(self,path):
        with self.lock:
            self.calls.append(path)
            self.counts[path]=self.counts.get(path,0)+1
        value=self.routes.get(path)
        if isinstance(value,Exception):raise value
        if callable(value):value=value(self.counts[path])
        if value is None:return GitHubResponse(404,{}, {})
        if isinstance(value,GitHubResponse):return copy.deepcopy(value)
        return GitHubResponse(200,copy.deepcopy(value),{})


def collect(client):
    return collect_snapshot(client=client,cycle_id='icarus2-transport-fixture')


def test_real_source_bytes_and_live_claims_are_collected_without_payload_projection():
    client=Client();snapshot=collect(client)
    assert snapshot['manifest']['document']==client.documents
    assert snapshot['manifest']['blob_sha']==blob(snapshot['manifest']['raw_json'].encode())
    assert len(snapshot['repositories'])==2
    assert all(row['pr_pages_complete'] and row['runs_pages_complete'] for row in snapshot['repositories'])
    assert snapshot['coordination']['complete'] is True
    assert snapshot['coordination']['claims'][0]['session_id']=='icarus1-fixture'
    assert snapshot['coordination']['claims'][0]['targets']==[dict(repo=BUS,path='runtime.py')]
    assert 'PRIVATE_PAYLOAD_MARKER' not in json.dumps(snapshot)
    assert not any('ACTIVE.md' in path or 'index.json' in path for path in client.calls)
    assert all(path.startswith('repos/') for path in client.calls)


def test_repository_head_drift_remains_visible():
    client=Client();key=f'repos/{ENGINE}/git/ref/heads/main'
    client.routes[key]=lambda count:dict(ref='refs/heads/main',object=dict(type='commit',sha=A if count==1 else C))
    row=next(r for r in collect(client)['repositories'] if r['repository']==ENGINE)
    assert row['commit']==A and row['verified_commit']==C


@pytest.mark.parametrize('status', [403,404,429,500])
def test_repository_access_failure_is_an_explicit_error_not_empty_success(status):
    client=Client();client.routes[f'repos/{BUS}/git/ref/heads/main']=GitHubResponse(status,{}, {})
    snapshot=collect(client)
    row=next(r for r in snapshot['repositories'] if r['repository']==BUS)
    assert row['error_code']
    assert snapshot['coordination']['complete'] is False


def test_missing_manifest_cannot_invent_a_repository_universe():
    client=Client();client.routes[f'repos/{ENGINE}/contents/config/federated_repo_evidence.json?ref={A}']=GitHubResponse(404,{}, {})
    snapshot=collect(client)
    assert snapshot['repositories']==[]
    assert snapshot['manifest']['error_code']


def test_declared_new_repository_is_automatically_in_scope():
    client=Client();repo='reppiks490/additional-evidence'
    client.documents['repositories'].append(dict(repository=repo,role='other',data_authority='EVIDENCE_PRODUCER',evidence_paths=[]))
    client.routes[f'repos/{ENGINE}/contents/config/federated_repo_evidence.json?ref={A}']=file_response('config/federated_repo_evidence.json',client.documents)
    client.routes[f'repos/{repo}/git/ref/heads/main']=dict(ref='refs/heads/main',object=dict(type='commit',sha=C))
    client.routes[f'repos/{repo}/pulls?state=open&per_page=100&page=1']=[]
    client.routes[f'repos/{repo}/actions/runs?per_page=100&page=1']=dict(total_count=0,workflow_runs=[])
    assert {r['repository'] for r in collect(client)['repositories']}=={ENGINE,BUS,repo}


def test_blob_hash_mismatch_is_rejected_before_manifest_parse():
    client=Client();key=f'repos/{ENGINE}/contents/config/federated_repo_evidence.json?ref={A}'
    client.routes[key]['sha']=C
    snapshot=collect(client)
    assert snapshot['manifest']['error_code']=='BLOB_MISMATCH'
    assert snapshot['repositories']==[]


def test_mutable_remote_contents_url_is_never_followed():
    client=Client();client.routes[f'repos/{ENGINE}/contents/AGENTS.md?ref={A}']['download_url']='https://hostile.example/secrets'
    collect(client)
    assert all('hostile' not in path for path in client.calls)


def test_cross_host_pagination_is_not_followed_and_remains_incomplete():
    client=Client();key=f'repos/{ENGINE}/pulls?state=open&per_page=100&page=1'
    client.routes[key]=GitHubResponse(200,[],{'link':'<https://hostile.example/steal>; rel="next"'})
    row=next(r for r in collect(client)['repositories'] if r['repository']==ENGINE)
    assert row['pr_pages_complete'] is False
    assert all('hostile' not in path for path in client.calls)


def test_paginated_open_prs_are_collected_and_bound_to_head_identity():
    client=Client();base=f'repos/{ENGINE}/pulls?state=open&per_page=100&page='
    pr=dict(number=7,head=dict(sha=C),base=dict(sha=A),draft=False)
    client.routes[base+'1']=GitHubResponse(200,[pr],{'link':f'<https://api.github.com/{base}2>; rel="next"'})
    client.routes[base+'2']=[]
    row=next(r for r in collect(client)['repositories'] if r['repository']==ENGINE)
    assert row['pr_pages_complete'] is True
    assert row['pull_requests'][0]['head_sha']==C


def test_truncated_coordination_tree_cannot_clear_claims():
    client=Client();client.routes[f'repos/{BUS}/git/trees/{C}?recursive=1']['truncated']=True
    state=collect(client)['coordination']
    assert state['complete'] is False and state['error_code']


def test_missing_source_event_is_incomplete_not_silently_unreserved():
    client=Client();key=f'repos/{BUS}/contents/coordination/events/2026/10/20/icarus1-fixture/claim.json?ref={B}'
    client.routes[key]=GitHubResponse(403,{}, {})
    state=collect(client)['coordination']
    assert state['complete'] is False


def test_source_tree_blob_and_contents_blob_must_match():
    client=Client();tree=client.routes[f'repos/{BUS}/git/trees/{C}?recursive=1']
    tree['tree'][1]['sha']='d'*40
    state=collect(client)['coordination']
    assert state['complete'] is False


def test_billing_job_timestamps_without_executed_steps_do_not_prove_started():
    client=Client();runs=f'repos/{ENGINE}/actions/runs?per_page=100&page=1'
    run=dict(id=4,name='tests',head_sha=A,status='completed',conclusion='failure',created_at=UTC,updated_at=UTC)
    client.routes[runs]=dict(total_count=1,workflow_runs=[run])
    client.routes[f'repos/{ENGINE}/actions/runs/4/jobs?per_page=100&page=1']=dict(total_count=1,jobs=[dict(id=8,name='engine',status='completed',conclusion='failure',started_at=UTC,completed_at=UTC,steps=[])])
    row=next(r for r in collect(client)['repositories'] if r['repository']==ENGINE)
    assert row['workflow_runs'][0]['jobs_started']==0


def test_executed_steps_prove_started_but_job_lookup_failure_stays_unknown():
    client=Client();runs=f'repos/{ENGINE}/actions/runs?per_page=100&page=1'
    client.routes[runs]=dict(total_count=1,workflow_runs=[dict(id=4,name='tests',head_sha=A,status='completed',conclusion='success',created_at=UTC,updated_at=UTC)])
    job=f'repos/{ENGINE}/actions/runs/4/jobs?per_page=100&page=1'
    client.routes[job]=dict(total_count=1,jobs=[dict(id=8,status='completed',conclusion='success',steps=[dict(status='completed',conclusion='success',started_at=UTC,completed_at=UTC)])])
    row=next(r for r in collect(client)['repositories'] if r['repository']==ENGINE)
    assert row['workflow_runs'][0]['jobs_started']==1
    client.routes[job]=GitHubResponse(403,{}, {})
    row=next(r for r in collect(client)['repositories'] if r['repository']==ENGINE)
    assert row['workflow_runs'][0]['jobs_started'] is None


def test_sensitive_anchors_are_blocked_without_fetching_contents():
    client=Client();path='private/secrets.env'
    client.documents['repositories'][0]['evidence_paths']=[path]
    client.routes[f'repos/{ENGINE}/contents/config/federated_repo_evidence.json?ref={A}']=file_response('config/federated_repo_evidence.json',client.documents)
    row=next(r for r in collect(client)['repositories'] if r['repository']==ENGINE)
    assert row['anchors'][0]['status']=='BLOCKED'
    assert not any('/contents/private/' in path for path in client.calls)


def test_request_budget_exhaustion_is_explicit(monkeypatch):
    import integration_brain.transport as transport
    monkeypatch.setattr(transport,'MAX_REQUESTS',2)
    snapshot=collect(Client())
    assert snapshot['coordination']['complete'] is False
    assert snapshot['transport']['budget_exhausted'] is True


def test_nonfinite_and_duplicate_json_never_enter_source_documents():
    client=Client();path='config/federated_repo_evidence.json'
    client.routes[f'repos/{ENGINE}/contents/{path}?ref={A}']=file_response(path,raw=b'{"repositories":[],"repositories":[NaN]}')
    assert collect(client)['manifest']['error_code']=='INVALID_JSON'


def test_gh_client_rejects_non_rest_paths_before_starting_any_process():
    for path in ('https://hostile.example/api','/repos/x/y','--method=POST','repos/a/b/contents/../.env','repos/a/b/pulls?state=open;rm=x'):
        with pytest.raises(TransportError):GhClient().get(path)


def test_same_named_workflows_preserve_their_distinct_workflow_ids():
    client=Client();runs=f'repos/{ENGINE}/actions/runs?per_page=100&page=1'
    client.routes[runs]=dict(total_count=2,workflow_runs=[dict(id=i,name='tests',workflow_id=i+10,head_sha=A,status='completed',conclusion='success',created_at=UTC,updated_at=UTC) for i in (4,5)])
    rows=next(r for r in collect(client)['repositories'] if r['repository']==ENGINE)['workflow_runs']
    assert [row['workflow_id'] for row in rows]==[14,15]


@pytest.mark.parametrize('stamp',['not-a-time','2026-10-20T18:20:00','2026-10-20T18:20:00.0000001Z','2099-01-01T00:00:00Z'])
def test_invalid_step_clock_cannot_prove_a_job_started(stamp):
    client=Client();runs=f'repos/{ENGINE}/actions/runs?per_page=100&page=1'
    client.routes[runs]=dict(total_count=1,workflow_runs=[dict(id=4,name='tests',head_sha=A,status='completed',conclusion='success',created_at=UTC,updated_at=UTC)])
    client.routes[f'repos/{ENGINE}/actions/runs/4/jobs?per_page=100&page=1']=dict(total_count=1,jobs=[dict(id=8,status='completed',conclusion='success',steps=[dict(status='completed',conclusion='success',started_at=stamp,completed_at=stamp)])])
    row=next(r for r in collect(client)['repositories'] if r['repository']==ENGINE)
    assert row['workflow_runs'][0]['jobs_started'] is None


def test_aggregate_response_budget_is_enforced_before_source_use(monkeypatch):
    import integration_brain.transport as transport
    monkeypatch.setattr(transport,'MAX_AGGREGATE_BYTES',20)
    snapshot=collect(Client())
    assert snapshot['transport']['budget_exhausted'] is True
    assert snapshot['manifest']['error_code']=='ACQUISITION_BUDGET'


def test_an_exponent_overflow_is_invalid_json_not_a_finite_source():
    client=Client();path='config/federated_repo_evidence.json'
    client.routes[f'repos/{ENGINE}/contents/{path}?ref={A}']=file_response(path,raw=b'{"x":1e999}')
    assert collect(client)['manifest']['error_code']=='INVALID_JSON'


def test_more_pages_than_the_bound_is_not_silently_complete():
    client=Client();base=f'repos/{ENGINE}/pulls?state=open&per_page=100&page='
    for page in range(1,6):
        client.routes[base+str(page)]=GitHubResponse(200,[],{'link':f'<https://api.github.com/{base}{page+1}>; rel="next"'})
    row=next(r for r in collect(client)['repositories'] if r['repository']==ENGINE)
    assert row['pr_pages_complete'] is False
    assert row['acquisition_errors']['pull_requests']=='PAGINATION_BOUND'
    assert all(not path.endswith('page=6') for path in client.calls)


def test_collection_total_without_a_next_link_is_not_silently_complete():
    client=Client();client.routes[f'repos/{ENGINE}/actions/runs?per_page=100&page=1']=dict(total_count=4,workflow_runs=[])
    row=next(r for r in collect(client)['repositories'] if r['repository']==ENGINE)
    assert row['runs_pages_complete'] is False


def test_source_tree_symlinks_cannot_be_materialized():
    client=Client();client.routes[f'repos/{BUS}/git/trees/{C}?recursive=1']['tree'][1]['mode']='120000'
    state=collect(client)['coordination']
    assert state['complete'] is False and state['error_code']=='INVALID_COORDINATION_RECORD'


def test_verified_source_json_failure_does_not_expose_input_text():
    client=Client();path='coordination/owner_status.json'
    raw=b'{"private_marker":"DO_NOT_PRINT"'
    response=file_response(path,raw=raw)
    client.routes[f'repos/{BUS}/contents/{path}?ref={B}']=response
    client.routes[f'repos/{BUS}/git/trees/{C}?recursive=1']['tree'][0]['sha']=response['sha']
    state=collect(client)['coordination']
    assert state['complete'] is False
    assert 'DO_NOT_PRINT' not in json.dumps(state)


def test_gh_process_argv_is_fixed_get_and_header_response_is_parsed(monkeypatch):
    import subprocess
    import sys
    import integration_brain.transport as transport
    original=subprocess.Popen;seen=[]
    raw='HTTP/2.0 200 OK\r\nContent-Type: application/json\r\n\r\n{"total_count":0,"workflow_runs":[]}'
    def spawn(argv,**kwargs):
        seen.append(argv)
        assert 'shell' not in kwargs
        return original([sys.executable,'-c','import sys;sys.stdout.write('+repr(raw)+')'],**kwargs)
    monkeypatch.setattr(transport.subprocess,'Popen',spawn)
    response=GhClient().get(f'repos/{ENGINE}/actions/runs?per_page=100&page=1')
    assert response.status_code==200 and response.data['workflow_runs']==[]
    assert seen==[['gh','api','--include','--hostname','github.com',f'repos/{ENGINE}/actions/runs?per_page=100&page=1']]


def test_gh_response_body_and_stderr_are_bounded_without_echoing_them(monkeypatch):
    import subprocess
    import sys
    import integration_brain.transport as transport
    original=subprocess.Popen
    def spawn(_argv,**kwargs):
        return original([sys.executable,'-c',"import sys;sys.stdout.write('HTTP/2.0 200 OK\\n\\n'+('x'*100000));sys.stderr.write('SECRET_MARKER')"],**kwargs)
    monkeypatch.setattr(transport,'MAX_RESPONSE_BYTES',32)
    monkeypatch.setattr(transport.subprocess,'Popen',spawn)
    with pytest.raises(TransportError,match='RESPONSE_BOUND') as failure:
        GhClient().get(f'repos/{ENGINE}/git/ref/heads/main')
    assert 'SECRET_MARKER' not in str(failure.value)


def test_gh_hanging_request_is_terminated_at_its_deadline(monkeypatch):
    import subprocess
    import sys
    import time
    import integration_brain.transport as transport
    original=subprocess.Popen;children=[]
    def spawn(_argv,**kwargs):
        child=original([sys.executable,'-c','import time;time.sleep(30)'],**kwargs);children.append(child);return child
    monkeypatch.setattr(transport.subprocess,'Popen',spawn)
    with pytest.raises(TransportError,match='REQUEST_TIMEOUT'):
        GhClient(deadline=time.monotonic()+.1).get(f'repos/{ENGINE}/git/ref/heads/main')
    assert children[0].poll() is not None


def test_numeric_github_pagination_is_only_a_hint_for_fixed_repository_route():
    from integration_brain.transport import _Budget, _pages
    client=Client()
    first=f'repos/{ENGINE}/actions/runs?per_page=100&page=1'
    second=f'repos/{ENGINE}/actions/runs?per_page=100&page=2'
    client.routes[first]=GitHubResponse(200,dict(total_count=2,workflow_runs=[dict(id=1)]),
        {'link':'<https://api.github.com/repositories/1377828482/actions/runs?per_page=100&page=2>; rel="next"'})
    client.routes[second]=dict(total_count=2,workflow_runs=[dict(id=2)])
    rows,complete,error=_pages(_Budget(client),ENGINE,'actions/runs','workflow_runs')
    assert complete is True and error is None
    assert rows == [dict(id=1),dict(id=2)]
    assert client.calls == [first,second]
