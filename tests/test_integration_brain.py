"""Behavioral oracles for source-bound integration snapshots, not system readiness."""
from __future__ import annotations

import copy
import hashlib
import json

import pytest

from integration_brain import build_cycle

ENGINE = 'reppiks490/Icarus-engine'
BUS = 'reppiks490/icarus-owner-actions'
A = 'a' * 40
B = 'b' * 40
C = 'c' * 40
START = '2026-10-20T18:20:00Z'
OBSERVED = '2026-10-20T18:20:10Z'
END = '2026-10-20T18:20:20Z'


def seal_manifest(snapshot, document):
    raw = json.dumps(document, indent=2) + '\n'
    data = raw.encode()
    snapshot['manifest'].update(raw_json=raw, document=copy.deepcopy(document),
        blob_sha=hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest(),
        sha256=hashlib.sha256(data).hexdigest())


def example():
    specs = [dict(repository=ENGINE, role='canonical_data_plane', data_authority='CANONICAL_LEDGER_AND_COLLECTION', evidence_paths=['config/data_ingestion_manifest.json']),
             dict(repository=BUS, role='governance_plane', data_authority='GOVERNANCE_EVIDENCE_ONLY', evidence_paths=['coordination/owner_status.json'])]
    doc = dict(schema_version='icarus-federated-repo-evidence-v1', required_for_every_ai_unit=True,
        authority='RESEARCH_EVIDENCE_ONLY', repositories=specs)
    snapshot = dict(schema_version='icarus2-snapshot-v1', cycle_id='icarus2-20261020T182000Z-fixture',
        started_at_utc=START, completed_at_utc=END,
        manifest=dict(repository=ENGINE, commit=A, path='config/federated_repo_evidence.json'),
        coordination=dict(repository=BUS, commit=B, owner_status=dict(schema_version='icarus-coordination-owner-status-v1', live_broker_arming=False), claims=[]),
        repositories=[])
    seal_manifest(snapshot, doc)
    for spec, commit in zip(specs, [A, B]):
        snapshot['repositories'].append(dict(repository=spec['repository'], commit=commit,
            verified_commit=commit, observed_at_utc=OBSERVED, pr_pages_complete=True, runs_pages_complete=True,
            pull_requests=[dict(number=7, head_sha=C, base_sha=commit, draft=True)],
            workflow_runs=[dict(id=99, name='tests', status='completed', conclusion='success', head_sha=commit,
                created_at=START, updated_at=OBSERVED, jobs_started=1, jobs_pages_complete=True,
                jobs=[dict(id=44, status='completed', conclusion='success', steps=[dict(
                    status='completed', conclusion='success', started_at=START, completed_at=OBSERVED)])])],
            anchors=[dict(path=spec['evidence_paths'][0], status='PRESENT', blob_sha=C, sha256='d'*64, size=21)]))
    return snapshot


def codes(report):
    return {gap['code'] for gap in report['gaps']}


def test_complete_metadata_never_claims_runtime_or_trading_readiness():
    report = build_cycle(example())
    assert report['status'] == 'SNAPSHOT_VALIDATED'
    assert report['metadata_only'] is True
    assert report['system_ready'] is False
    assert report['execution_authorized'] is False
    assert report['automatic_merge_authorized'] is False
    assert report['summary']['repositories_expected'] == 2
    assert report['repositories'][0]['runtime_health'] == 'UNVERIFIED'
    assert report['repositories'][0]['ci']['current_head_status'] == 'OBSERVED_SUCCESS'
    assert len(report['swarms']) == 5
    assert all(row['agent_execution_observed'] is False for row in report['swarms'])


def test_core_does_not_mutate_its_snapshot_or_share_returned_state():
    snapshot = example()
    before = copy.deepcopy(snapshot)
    first = build_cycle(snapshot)
    first['repositories'].clear()
    assert snapshot == before
    assert len(build_cycle(snapshot)['repositories']) == 2


def test_repository_universe_is_derived_from_sealed_manifest_not_a_named_ceiling():
    snapshot = example()
    extra = copy.deepcopy(snapshot['repositories'][0])
    extra['repository'] = 'reppiks490/additional-evidence'
    snapshot['repositories'].append(extra)
    doc = copy.deepcopy(snapshot['manifest']['document'])
    doc['repositories'].append(dict(repository=extra['repository'], role='additional_research', data_authority='EVIDENCE_PRODUCER', evidence_paths=[extra['anchors'][0]['path']]))
    seal_manifest(snapshot, doc)
    assert build_cycle(snapshot)['summary']['repositories_expected'] == 3


def test_drift_requires_restart_even_when_the_original_revision_has_green_ci():
    snapshot = example()
    snapshot['repositories'][0]['verified_commit'] = C
    report = build_cycle(snapshot)
    assert report['status'] == 'RESTART_CYCLE_REQUIRED'
    assert 'REPOSITORY_DRIFT' in codes(report)


def test_cross_revision_manifest_and_coordination_cannot_validate():
    snapshot = example()
    snapshot['manifest']['commit'] = C
    snapshot['coordination']['commit'] = C
    report = build_cycle(snapshot)
    assert report['status'] == 'RESTART_CYCLE_REQUIRED'
    assert {'MANIFEST_REVISION_MISMATCH', 'COORDINATION_REVISION_MISMATCH'} <= codes(report)


def test_missing_declared_repository_is_explicitly_incomplete():
    snapshot = example()
    snapshot['repositories'].pop()
    report = build_cycle(snapshot)
    assert report['status'] == 'INCOMPLETE'
    assert 'REPOSITORY_MISSING' in codes(report)
    assert report['summary']['repositories_observed'] == 1


def test_inaccessible_repository_is_not_fabricated_as_an_empty_healthy_repo():
    snapshot = example()
    snapshot['repositories'][0] = dict(repository=ENGINE, error_code='ACCESS_DENIED')
    report = build_cycle(snapshot)
    assert report['status'] == 'INCOMPLETE'
    assert 'REPOSITORY_UNAVAILABLE' in codes(report)
    assert report['repositories'][0]['ci']['current_head_status'] == 'UNVERIFIED'


@pytest.mark.parametrize('field', ['pr_pages_complete', 'runs_pages_complete'])
def test_partial_pagination_is_not_a_complete_snapshot(field):
    snapshot = example()
    snapshot['repositories'][0][field] = False
    report = build_cycle(snapshot)
    assert report['status'] == 'INCOMPLETE'
    assert 'PAGINATION_INCOMPLETE' in codes(report)


@pytest.mark.parametrize('status,conclusion,started,expected', [
    ('queued', None, 0, 'PENDING'), ('in_progress', None, 1, 'PENDING'),
    ('completed', 'success', 0, 'NOT_STARTED'), ('completed', 'success', None, 'UNVERIFIED'),
    ('completed', 'failure', 0, 'NOT_STARTED'), ('completed', 'failure', 1, 'OBSERVED_FAILURE'),
    ('completed', 'skipped', 0, 'NOT_STARTED'), ('completed', 'cancelled', 1, 'NOT_SUCCESSFUL'),
])
def test_pending_and_unstarted_runs_never_count_as_green(status, conclusion, started, expected):
    snapshot = example()
    run = snapshot['repositories'][0]['workflow_runs'][0]
    run.update(status=status, conclusion=conclusion, jobs_started=started)
    if started is None:
        run.pop('jobs')
        run['jobs_pages_complete'] = False
    elif started == 0:
        run['jobs'][0]['steps'] = []
    ci = build_cycle(snapshot)['repositories'][0]['ci']
    assert ci['current_head_status'] == expected
    assert ci['successful_current_runs'] == 0


def test_old_revision_ci_is_historical_even_when_passed():
    snapshot = example()
    snapshot['repositories'][0]['workflow_runs'][0]['head_sha'] = C
    ci = build_cycle(snapshot)['repositories'][0]['ci']
    assert ci['current_head_status'] == 'UNVERIFIED'
    assert ci['historical_runs'] == 1
    assert ci['successful_current_runs'] == 0


def test_a_later_failure_or_pending_run_cannot_be_hidden_by_one_green_run():
    snapshot = example()
    runs = snapshot['repositories'][0]['workflow_runs']
    bad = copy.deepcopy(runs[0])
    bad.update(id=100, name='other-tests', conclusion='failure')
    runs.append(bad)
    assert build_cycle(snapshot)['repositories'][0]['ci']['current_head_status'] == 'OBSERVED_FAILURE'


@pytest.mark.parametrize('case', ['manifest_bytes', 'manifest_sha', 'manifest_blob', 'manifest_document', 'duplicate_json', 'nonfinite_json'])
def test_manifest_bytes_and_exact_identity_are_bound(case):
    snapshot = example()
    manifest = snapshot['manifest']
    if case == 'manifest_bytes': manifest['raw_json'] += ' '
    elif case == 'manifest_sha': manifest['sha256'] = '0' * 64
    elif case == 'manifest_blob': manifest['blob_sha'] = '0' * 40
    elif case == 'manifest_document': manifest['document']['repositories'].clear()
    else:
        raw = '{"authority":"RESEARCH_EVIDENCE_ONLY","authority":"OTHER"}' if case == 'duplicate_json' else '{"x":NaN}'
        manifest.update(raw_json=raw, sha256=hashlib.sha256(raw.encode()).hexdigest(),
            blob_sha=hashlib.sha1(b'blob '+str(len(raw.encode())).encode()+b'\0'+raw.encode()).hexdigest())
        manifest.pop('document')
    with pytest.raises(ValueError): build_cycle(snapshot)


@pytest.mark.parametrize('where', ['observed', 'run_created', 'run_updated', 'start', 'naive', 'overprecision'])
def test_future_inconsistent_or_ambiguous_clocks_fail_closed(where):
    snapshot = example()
    row = snapshot['repositories'][0]
    future = '2026-10-20T18:21:00Z'
    if where == 'observed': row['observed_at_utc'] = future
    elif where == 'run_created': row['workflow_runs'][0]['created_at'] = future
    elif where == 'run_updated': row['workflow_runs'][0]['updated_at'] = future
    elif where == 'start': snapshot['started_at_utc'] = future
    elif where == 'naive': row['observed_at_utc'] = '2026-10-20T18:20:10'
    else: row['observed_at_utc'] = '2026-10-20T18:20:10.0000001Z'
    with pytest.raises(ValueError): build_cycle(snapshot)


@pytest.mark.parametrize('case', ['empty_universe', 'duplicate_repo', 'duplicate_observation', 'duplicate_anchor', 'duplicate_run', 'duplicate_pr', 'unsafe_repo', 'unsafe_path', 'bool_pages', 'bool_jobs', 'true_authority', 'owner_authority'])
def test_ambiguous_schema_and_authority_are_rejected(case):
    snapshot = example()
    row = snapshot['repositories'][0]
    if case == 'empty_universe':
        doc = snapshot['manifest']['document']; doc['repositories'] = []; seal_manifest(snapshot, doc)
    elif case == 'duplicate_repo':
        doc = snapshot['manifest']['document']; doc['repositories'].append(copy.deepcopy(doc['repositories'][0])); seal_manifest(snapshot, doc)
    elif case == 'duplicate_observation': snapshot['repositories'].append(copy.deepcopy(row))
    elif case == 'duplicate_anchor': row['anchors'].append(copy.deepcopy(row['anchors'][0]))
    elif case == 'duplicate_run': row['workflow_runs'].append(copy.deepcopy(row['workflow_runs'][0]))
    elif case == 'duplicate_pr': row['pull_requests'].append(copy.deepcopy(row['pull_requests'][0]))
    elif case == 'unsafe_repo': row['repository'] = '../bad'
    elif case == 'unsafe_path': row['anchors'][0]['path'] = '../secrets'
    elif case == 'bool_pages': row['pr_pages_complete'] = 'true'
    elif case == 'bool_jobs': row['workflow_runs'][0]['jobs_started'] = True
    elif case == 'true_authority': snapshot['execution_authorized'] = True
    else: snapshot['coordination']['owner_status']['live_broker_arming'] = 'false'
    with pytest.raises(ValueError): build_cycle(snapshot)


def test_missing_and_unavailable_anchors_are_reported_without_invented_consumption():
    snapshot = example()
    snapshot['repositories'][0]['anchors'][0] = dict(path='config/data_ingestion_manifest.json', status='MISSING', blob_sha=None, sha256=None, size=None)
    report = build_cycle(snapshot)
    assert report['status'] == 'INCOMPLETE'
    assert 'EVIDENCE_ANCHOR_UNAVAILABLE' in codes(report)
    assert report['repositories'][0]['runtime_health'] == 'UNVERIFIED'


def test_undeclared_repository_and_undeclared_evidence_are_explicit_gaps():
    snapshot = example()
    other = copy.deepcopy(snapshot['repositories'][0]); other['repository'] = 'reppiks490/unreconciled'
    snapshot['repositories'].append(other)
    extra = copy.deepcopy(snapshot['repositories'][0]['anchors'][0]); extra['path'] = 'new/evidence.json'
    snapshot['repositories'][0]['anchors'].append(extra)
    report = build_cycle(snapshot)
    assert report['status'] == 'INCOMPLETE'
    assert {'UNDECLARED_REPOSITORY', 'UNDECLARED_EVIDENCE_ANCHOR'} <= codes(report)


def test_icarus1_reserved_paths_are_handoff_only_and_collisions_are_visible():
    snapshot = example()
    snapshot['coordination']['claims'] = [
        dict(session_id='icarus1-restart', type='UPDATE', at_utc=OBSERVED,
             targets=[dict(repo=ENGINE, path='runtime/server.py')]),
        dict(session_id='other-worker', type='CLAIM', at_utc=OBSERVED,
             targets=[dict(repo=ENGINE, path='runtime')]),
    ]
    report = build_cycle(snapshot)
    assert report['status'] == 'INCOMPLETE'
    assert 'CLAIM_COLLISION' in codes(report)
    reserved = report['coordination']['reserved_targets']
    assert next(row for row in reserved if row['session_id']=='icarus1-restart')['handoff_only'] is True
    assert report['handoffs']
    assert all(row['automatic_repair_authorized'] is False for row in report['handoffs'])


def test_released_claims_do_not_keep_paths_reserved():
    snapshot = example()
    snapshot['coordination']['claims'] = [dict(session_id='done', type='RELEASE', at_utc=OBSERVED,
        targets=[dict(repo=ENGINE, path='runtime/server.py')])]
    assert build_cycle(snapshot)['coordination']['reserved_targets'] == []


def test_cycle_bound_is_enforced_before_large_input_is_traversed():
    snapshot = example()
    snapshot['oversized'] = 'x' * (8 * 1024 * 1024)
    with pytest.raises(ValueError): build_cycle(snapshot)


def test_incomplete_coordination_with_missing_owner_status_stays_unknown():
    snapshot = example()
    snapshot['coordination'].update(complete=False, owner_status=None, error_code='SOURCE_INACCESSIBLE')
    report = build_cycle(snapshot)
    assert report['status'] == 'INCOMPLETE'
    assert {'COORDINATION_SNAPSHOT_INCOMPLETE', 'OWNER_STATUS_UNAVAILABLE'} <= codes(report)
    assert report['coordination']['owner_status_verified'] is False
    assert report['coordination']['live_broker_arming'] is None
    assert report['execution_authorized'] is False


def test_cooperation_is_only_effective_when_both_sources_name_one_another():
    snapshot = example()
    snapshot['coordination']['claims'] = [dict(session_id=sid, type='CLAIM', at_utc=OBSERVED,
        targets=[dict(repo=ENGINE, path='runtime')], coordination_mode='cooperate', cooperates_with=peers)
        for sid, peers in [('alpha',['beta']), ('beta',[])]]
    assert 'CLAIM_COLLISION' in codes(build_cycle(snapshot))
    snapshot['coordination']['claims'][1]['cooperates_with'] = ['alpha']
    report = build_cycle(snapshot)
    assert 'CLAIM_COLLISION' not in codes(report)
    assert len(report['coordination']['reserved_targets']) == 2


def test_overflowing_source_float_is_rejected_even_in_an_unused_manifest_field():
    snapshot = example()
    raw = snapshot['manifest']['raw_json'].replace('"authority":', '"overflow": 1e9999, "authority":')
    data = raw.encode()
    snapshot['manifest'].update(raw_json=raw, sha256=hashlib.sha256(data).hexdigest(),
        blob_sha=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest())
    snapshot['manifest'].pop('document')
    with pytest.raises(ValueError): build_cycle(snapshot)


def test_collision_reporting_is_bounded_and_its_partial_state_explicit():
    snapshot = example()
    snapshot['coordination']['claims'] = [dict(session_id='worker-'+str(index), type='CLAIM',
        at_utc=OBSERVED, targets=[dict(repo=ENGINE,path='same/path')]) for index in range(20)]
    report = build_cycle(snapshot)
    assert len(report['coordination']['collisions']) == 128
    assert report['coordination']['collisions_complete'] is False
    assert 'COLLISION_REPORT_TRUNCATED' in codes(report)
    assert report['status'] == 'INCOMPLETE'


def test_missing_manifest_does_not_invent_an_empty_complete_repository_universe():
    snapshot = example()
    snapshot['manifest'] = dict(repository=ENGINE, path='config/federated_repo_evidence.json', error_code='ACCESS_DENIED')
    snapshot['repositories'] = []
    report = build_cycle(snapshot)
    assert report['status'] == 'INCOMPLETE'
    assert report['summary']['repositories_expected'] is None
    assert report['source']['verified'] is False
    assert report['source']['commit'] is None
    assert 'MANIFEST_UNAVAILABLE' in codes(report)
    assert report['system_ready'] is False


def test_missing_bus_head_has_unknown_policy_and_source_revision():
    snapshot = example()
    snapshot['coordination'].update(commit=None, owner_status=None, complete=False, error_code='ACCESS_DENIED')
    snapshot['repositories'][1] = dict(repository=BUS, error_code='ACCESS_DENIED')
    report = build_cycle(snapshot)
    assert report['status'] == 'INCOMPLETE'
    assert report['coordination']['commit'] is None
    assert report['coordination']['live_broker_arming'] is None
    assert 'COORDINATION_SNAPSHOT_INCOMPLETE' in codes(report)
    assert 'COORDINATION_REVISION_MISMATCH' not in codes(report)


def test_available_manifest_cannot_silently_lose_its_source_bytes():
    snapshot = example()
    snapshot['manifest'].pop('raw_json')
    with pytest.raises(ValueError): build_cycle(snapshot)


@pytest.mark.parametrize('authority', [ENGINE, BUS])
def test_canonical_authorities_cannot_disappear_from_the_reconciled_universe(authority):
    snapshot = example()
    document = copy.deepcopy(snapshot['manifest']['document'])
    document['repositories'] = [spec for spec in document['repositories'] if spec['repository'] != authority]
    seal_manifest(snapshot, document)
    snapshot['repositories'] = [row for row in snapshot['repositories'] if row['repository'] != authority]
    if authority == ENGINE: snapshot['manifest']['commit'] = C
    else: snapshot['coordination']['commit'] = C
    report = build_cycle(snapshot)
    assert report['status'] == 'INCOMPLETE'
    assert 'REQUIRED_AUTHORITY_NOT_IN_UNIVERSE' in codes(report)


def test_observed_at_is_acquisition_start_while_later_run_updates_remain_in_cycle():
    snapshot = example()
    snapshot['repositories'][0]['workflow_runs'][0]['updated_at'] = '2026-10-20T18:20:15Z'
    assert build_cycle(snapshot)['status'] == 'SNAPSHOT_VALIDATED'


def test_owner_policy_cannot_be_verified_without_its_coordination_revision():
    snapshot = example()
    snapshot['coordination'].update(complete=False, commit=None)
    report = build_cycle(snapshot)
    assert report['status'] == 'INCOMPLETE'
    assert report['coordination']['owner_status_verified'] is False
    assert report['coordination']['live_broker_arming'] is None
    assert 'OWNER_STATUS_UNAVAILABLE' in codes(report)


def run_with_jobs():
    snapshot = example()
    run = snapshot['repositories'][0]['workflow_runs'][0]
    run.update(jobs_pages_complete=True, jobs=[dict(id=44, status='completed', conclusion='success',
        steps=[dict(status='completed', conclusion='success', started_at=START, completed_at=OBSERVED)])])
    return snapshot, run


def test_complete_job_evidence_matches_derived_started_count():
    snapshot, _ = run_with_jobs()
    assert build_cycle(snapshot)['repositories'][0]['ci']['current_head_status'] == 'OBSERVED_SUCCESS'


def test_partial_job_evidence_cannot_prove_green_even_with_a_positive_lower_bound():
    snapshot, run = run_with_jobs()
    run['jobs_pages_complete'] = False
    assert build_cycle(snapshot)['repositories'][0]['ci']['current_head_status'] == 'UNVERIFIED'


@pytest.mark.parametrize('field', ['started_at', 'completed_at'])
def test_future_job_step_clocks_cannot_support_observed_ci(field):
    snapshot, run = run_with_jobs()
    run['jobs'][0]['steps'][0][field] = '2026-10-20T18:21:00Z'
    with pytest.raises(ValueError): build_cycle(snapshot)


def test_started_job_count_cannot_contradict_its_full_evidence():
    snapshot, run = run_with_jobs()
    run['jobs_started'] = 0
    with pytest.raises(ValueError): build_cycle(snapshot)


def test_skipped_step_timestamp_does_not_establish_execution():
    snapshot, run = run_with_jobs()
    run['jobs'][0]['steps'][0]['conclusion'] = 'skipped'
    run['jobs_started'] = 0
    assert build_cycle(snapshot)['repositories'][0]['ci']['current_head_status'] == 'NOT_STARTED'


def test_unfinished_or_failed_job_is_not_masked_by_successful_run_metadata():
    snapshot, run = run_with_jobs()
    run['jobs'][0]['conclusion'] = 'failure'
    assert build_cycle(snapshot)['repositories'][0]['ci']['current_head_status'] == 'OBSERVED_FAILURE'
    run['jobs'][0].update(status='in_progress', conclusion=None)
    assert build_cycle(snapshot)['repositories'][0]['ci']['current_head_status'] == 'UNVERIFIED'


def test_failed_final_head_read_preserves_pinned_partial_evidence():
    snapshot = example()
    snapshot['repositories'][0].update(verified_commit=None, verification_error_code='HTTP_403')
    report = build_cycle(snapshot)
    assert report['status'] == 'INCOMPLETE'
    assert 'HEAD_VERIFICATION_UNAVAILABLE' in codes(report)
    assert 'REPOSITORY_DRIFT' not in codes(report)
    row = report['repositories'][0]
    assert row['commit'] == A and row['verified_commit'] is None
    assert row['verification_error_code'] == 'HTTP_403'
    assert row['anchors'] and row['pull_requests']


def test_aggregate_started_count_without_job_evidence_cannot_prove_success():
    snapshot = example()
    run = snapshot['repositories'][0]['workflow_runs'][0]
    run.pop('jobs', None)
    run['jobs_pages_complete'] = True
    report = build_cycle(snapshot)
    assert report['status'] == 'INCOMPLETE'
    assert report['repositories'][0]['ci']['execution_verified'] is False
    assert report['repositories'][0]['ci']['current_head_status'] == 'UNVERIFIED'


def test_consistent_future_cycle_is_rejected_against_runtime_clock():
    snapshot = example()
    snapshot = json.loads(json.dumps(snapshot).replace('2026-10-20T18:', '2099-10-20T18:'))
    with pytest.raises(ValueError, match='FUTURE_CYCLE_CLOCK'):
        build_cycle(snapshot)


def test_validation_clock_can_be_injected_but_is_not_snapshot_authority():
    from datetime import datetime, timezone
    snapshot = example()
    snapshot['now'] = '2099-01-01T00:00:00Z'
    assert build_cycle(snapshot, now=datetime(2026, 10, 20, 18, 20, 20, tzinfo=timezone.utc))['status'] == 'SNAPSHOT_VALIDATED'
    with pytest.raises(ValueError, match='FUTURE_CYCLE_CLOCK'):
        build_cycle(snapshot, now=datetime(2026, 10, 20, 18, 20, 19, tzinfo=timezone.utc))
    with pytest.raises(ValueError, match='INVALID_VALIDATION_CLOCK'):
        build_cycle(snapshot, now=datetime(2026, 10, 20, 18, 20, 20))


def test_actual_jobs_without_explicit_complete_pagination_cannot_prove_success():
    snapshot = example()
    snapshot['repositories'][0]['workflow_runs'][0].pop('jobs_pages_complete')
    assert build_cycle(snapshot)['repositories'][0]['ci']['current_head_status'] == 'UNVERIFIED'


@pytest.mark.parametrize('error', ['HTTP 403', True, 'x' * 81])
def test_invalid_head_verification_error_cannot_be_persisted(error):
    snapshot = example()
    snapshot['repositories'][0].update(verified_commit=None, verification_error_code=error)
    with pytest.raises(ValueError, match='INVALID_VERIFICATION_ERROR'):
        build_cycle(snapshot)
