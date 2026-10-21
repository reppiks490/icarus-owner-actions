"""Bounded read-only GitHub acquisition for an evidence-only integration cycle.

No provider is queried and no remote code is imported or executed. Only the
canonical manifest's raw JSON is returned; other file bodies become identities.
"""
from __future__ import annotations

import base64
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import tempfile
import threading
import time
from urllib.parse import parse_qs, quote, urlencode, urlsplit

ENGINE = 'reppiks490/Icarus-engine'
BUS = 'reppiks490/icarus-owner-actions'
MANIFEST_PATH = 'config/federated_repo_evidence.json'
MAX_REQUESTS = 500
MAX_SECONDS = 180
MAX_RESPONSE_BYTES = 8 * 1024 * 1024
MAX_AGGREGATE_BYTES = 64 * 1024 * 1024
MAX_PAGES = 5
MAX_REPOSITORIES = 64
MAX_COORD_RECORDS = 400
MAX_TREE_ITEMS = 20000
_REPO = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,99}/[A-Za-z0-9][A-Za-z0-9_.-]{0,99}\Z')
_SHA = re.compile(r'[0-9a-f]{40}\Z')
_ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,159}\Z')
_STATUS = {'queued','requested','waiting','pending','in_progress','completed'}
_CONCLUSION = {None,'success','failure','neutral','cancelled','skipped','timed_out','action_required','stale','startup_failure'}


class TransportError(ValueError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


@dataclass
class GitHubResponse:
    status_code: int
    data: object
    headers: dict
    raw_body: bytes | None = None


def _fail(code):
    raise TransportError(code)


def _repo(value):
    if not isinstance(value, str) or not _REPO.fullmatch(value):
        _fail('INVALID_REPOSITORY')
    return value


def _sha(value):
    if not isinstance(value, str) or not _SHA.fullmatch(value):
        _fail('INVALID_SOURCE_SHA')
    return value


def _path(value, *, private_check=True):
    if (not isinstance(value, str) or not 1 <= len(value) <= 300 or value.startswith('/')
            or any(c in value for c in ('\\',':','%','\0','?','#')) or any(ord(c)<32 for c in value)):
        _fail('INVALID_PATH')
    parts = value.rstrip('/').split('/')
    if any(part in ('','.','..') for part in parts):
        _fail('INVALID_PATH')
    lower = [part.lower() for part in parts]
    if private_check and (any(part in {'.git','.ssh','.aws','.private','private','.secrets','secrets','depth_vault','vault','.provider_collection_archives','.native_provider_archives'} or part.startswith('.env') for part in lower)
            or lower[-1].endswith(('.enc','.pem','.key','.p12','.sqlite','.sqlite3','.db','.zip','.gz','.parquet','.csv','.bin'))):
        _fail('PRIVATE_PATH_DENIED')
    return value.rstrip('/')


def _integer(value, *, minimum=0, maximum=10**12):
    if type(value) is not int or not minimum <= value <= maximum:
        _fail('INVALID_METADATA')
    return value


def _clock(value):
    if not isinstance(value,str) or not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]{1,6})?(?:Z|[+-][0-9]{2}:[0-9]{2})',value):
        _fail('INVALID_METADATA_CLOCK')
    try:
        parsed=datetime.fromisoformat(value.replace('Z','+00:00'))
        if parsed.tzinfo is None or parsed.utcoffset() is None or parsed>datetime.now(timezone.utc):
            _fail('INVALID_METADATA_CLOCK')
        return parsed
    except (ValueError,OverflowError):
        _fail('INVALID_METADATA_CLOCK')


def _utc():
    return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')


def _json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                _fail('INVALID_JSON')
            result[key] = value
        return result
    def constant(_value):
        _fail('INVALID_JSON')
    try:
        def floating(text):
            number=float(text)
            if not math.isfinite(number):_fail('INVALID_JSON')
            return number
        value = json.loads(raw, object_pairs_hook=pairs, parse_constant=constant, parse_float=floating)
        stack = [(value,0)]
        count = 0
        while stack:
            item, depth = stack.pop()
            count += 1
            if count > 200000 or depth > 48:
                _fail('JSON_STRUCTURE_BOUND')
            if isinstance(item,dict):
                stack.extend((child,depth+1) for child in item.values())
            elif isinstance(item,list):
                stack.extend((child,depth+1) for child in item)
        return value
    except (ValueError,UnicodeError,RecursionError,OverflowError) as ex:
        if isinstance(ex,TransportError):raise
        _fail('INVALID_JSON')


def _api_path(path):
    """Only the exact REST read surfaces used below can reach the gh process."""
    if not isinstance(path,str) or len(path)>700 or not path.startswith('repos/'):
        _fail('UNSAFE_API_PATH')
    parsed = urlsplit(path)
    if parsed.scheme or parsed.netloc or parsed.fragment or any(c in path for c in ('\\',';','\0')):
        _fail('UNSAFE_API_PATH')
    pieces = parsed.path.split('/')
    if len(pieces)<4:
        _fail('UNSAFE_API_PATH')
    _repo('/'.join(pieces[1:3]))
    tail = '/'.join(pieces[3:])
    try:queries = parse_qs(parsed.query,keep_blank_values=True,strict_parsing=True)
    except ValueError:_fail('UNSAFE_API_PATH')
    if any(len(values)!=1 for values in queries.values()):
        _fail('UNSAFE_API_PATH')
    if tail == 'git/ref/heads/main' and not queries:return path
    if re.fullmatch(r'git/(commits|trees)/[0-9a-f]{40}',tail):
        if not queries or queries == {'recursive':['1']}:return path
    if tail.startswith('contents/'):
        rawpath = tail.removeprefix('contents/')
        # Our encoded file paths contain only canonical percent escapes.
        from urllib.parse import unquote
        decoded = unquote(rawpath)
        _path(decoded)
        if quote(decoded,safe='/') != rawpath or set(queries)!={'ref'}:
            _fail('UNSAFE_API_PATH')
        _sha(queries['ref'][0]);return path
    expected = {'per_page','page'} | ({'state'} if tail=='pulls' else set())
    if tail in ('pulls','actions/runs') or re.fullmatch(r'actions/runs/[1-9][0-9]*/jobs',tail):
        if set(queries)!=expected or queries.get('per_page')!=['100']:
            _fail('UNSAFE_API_PATH')
        if tail=='pulls' and queries.get('state')!=['open']:
            _fail('UNSAFE_API_PATH')
        if not re.fullmatch('[1-5]',queries['page'][0]):
            _fail('UNSAFE_API_PATH')
        return path
    _fail('UNSAFE_API_PATH')


class GhClient:
    """Use inherited GitHub authentication without reading or logging credentials."""
    def __init__(self, *, deadline=None):
        self.deadline = deadline if deadline is not None else time.monotonic()+MAX_SECONDS

    def get(self,path):
        _api_path(path)
        remaining = min(25,self.deadline-time.monotonic())
        if remaining<=0:_fail('DEADLINE_EXCEEDED')
        try:
            process = subprocess.Popen(['gh','api','--include','--hostname','github.com',path],
                stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        except OSError:
            _fail('GITHUB_CLIENT_UNAVAILABLE')
        chunks, errors = [], []
        exceeded = threading.Event()
        def read(stream, maximum, destination):
            total = 0
            try:
                while True:
                    chunk=stream.read(16384)
                    if not chunk:break
                    total+=len(chunk)
                    if total>maximum:
                        exceeded.set();process.kill();break
                    destination.append(chunk)
            except (OSError,ValueError):
                exceeded.set()
            finally:
                stream.close()
        readers=[threading.Thread(target=read,args=(process.stdout,MAX_RESPONSE_BYTES+65536,chunks),daemon=True),
                 threading.Thread(target=read,args=(process.stderr,65536,errors),daemon=True)]
        for thread in readers:thread.start()
        try:
            process.wait(timeout=remaining)
        except subprocess.TimeoutExpired:
            process.kill();process.wait()
            for thread in readers:thread.join(timeout=1)
            _fail('REQUEST_TIMEOUT')
        for thread in readers:thread.join(timeout=1)
        if exceeded.is_set() or any(thread.is_alive() for thread in readers):
            _fail('RESPONSE_BOUND')
        raw=b''.join(chunks)
        split=re.search(br'\r?\n\r?\n',raw)
        if split is None:_fail('GITHUB_RESPONSE_UNAVAILABLE')
        header,body=raw[:split.start()],raw[split.end():]
        if len(body)>MAX_RESPONSE_BYTES:_fail('RESPONSE_BOUND')
        try:lines=header.decode('ascii',errors='strict').splitlines()
        except UnicodeError:_fail('INVALID_HTTP_RESPONSE')
        match=re.fullmatch(r'HTTP/[0-9](?:\.[0-9])? ([0-9]{3})(?: .*)?',lines[0])
        if not match:_fail('INVALID_HTTP_RESPONSE')
        headers={}
        for line in lines[1:]:
            if ':' not in line:_fail('INVALID_HTTP_RESPONSE')
            key,value=line.split(':',1);key=key.lower().strip();value=value.strip()
            if key in headers and key in ('link','content-length'):_fail('INVALID_HTTP_RESPONSE')
            headers[key]=value
        status=int(match[1])
        if process.returncode and status<400:_fail('GITHUB_RESPONSE_UNAVAILABLE')
        data=_json(body) if body else {}
        return GitHubResponse(status,data,headers,body)


class _Budget:
    def __init__(self,client):
        self.deadline=time.monotonic()+MAX_SECONDS
        self.client=client if client is not None else GhClient(deadline=self.deadline)
        self.lock=threading.Lock()
        self.requests=0;self.bytes=0;self.exhausted=False

    def get(self,path):
        _api_path(path)
        with self.lock:
            if self.requests>=MAX_REQUESTS or time.monotonic()>=self.deadline:
                self.exhausted=True;_fail('ACQUISITION_BUDGET')
            self.requests+=1
        try:
            response=self.client.get(path)
        except TransportError:raise
        except Exception:_fail('TRANSPORT_UNAVAILABLE')
        if not isinstance(response,GitHubResponse):_fail('INVALID_HTTP_RESPONSE')
        if type(response.status_code) is not int or not 100<=response.status_code<=599:_fail('INVALID_HTTP_RESPONSE')
        if not isinstance(response.headers,dict) or any(not isinstance(k,str) or not isinstance(v,str) for k,v in response.headers.items()):_fail('INVALID_HTTP_RESPONSE')
        raw=response.raw_body
        if raw is None:
            try:raw=json.dumps(response.data,allow_nan=False,separators=(',',':')).encode()
            except (ValueError,TypeError,RecursionError):_fail('INVALID_JSON')
        if len(raw)>MAX_RESPONSE_BYTES:_fail('RESPONSE_BOUND')
        with self.lock:
            self.bytes+=len(raw)
            if self.bytes>MAX_AGGREGATE_BYTES:
                self.exhausted=True;_fail('ACQUISITION_BUDGET')
        if response.status_code!=200:_fail(f'HTTP_{response.status_code}')
        return response


def _head(budget,repo):
    value=budget.get(f'repos/{_repo(repo)}/git/ref/heads/main').data
    if not isinstance(value,dict) or value.get('ref')!='refs/heads/main' or not isinstance(value.get('object'),dict) or value['object'].get('type')!='commit':_fail('INVALID_HEAD_METADATA')
    return _sha(value['object'].get('sha'))


def _file(budget,repo,commit,path,expected_sha=None):
    _repo(repo);_sha(commit);path=_path(path)
    value=budget.get(f'repos/{repo}/contents/{quote(path,safe="/")}?ref={commit}').data
    if not isinstance(value,dict) or value.get('type')!='file' or value.get('path')!=path or value.get('encoding')!='base64':_fail('INVALID_FILE_METADATA')
    reported=_sha(value.get('sha'))
    if expected_sha is not None and reported!=_sha(expected_sha):_fail('BLOB_MISMATCH')
    size=_integer(value.get('size'),maximum=MAX_RESPONSE_BYTES)
    encoded=value.get('content')
    if not isinstance(encoded,str) or len(encoded)>MAX_RESPONSE_BYTES:_fail('RESPONSE_BOUND')
    try:raw=base64.b64decode(''.join(encoded.split()),validate=True)
    except (ValueError,UnicodeError):_fail('INVALID_FILE_ENCODING')
    if len(raw)!=size:_fail('FILE_SIZE_MISMATCH')
    if hashlib.sha1(b'blob '+str(size).encode()+b'\0'+raw).hexdigest()!=reported:_fail('BLOB_MISMATCH')
    return raw,reported


def _next_page(headers,repo,tail,page):
    header={k.lower():v for k,v in headers.items()}.get('link','')
    matches=re.findall(r'<([^>]+)>\s*;\s*rel="next"',header)
    if len(matches)>1:_fail('INVALID_PAGINATION')
    if not matches:
        if 'rel="next"' in header:_fail('INVALID_PAGINATION')
        return None
    url=urlsplit(matches[0])
    # GitHub emits numeric repository URLs for Actions pagination. This is
    # only a next-page hint: _pages reconstructs the route from our pinned
    # repository name and never requests the supplied link URL.
    same_surface = (url.path == f'/repos/{repo}/{tail}' or
        re.fullmatch(r'/repositories/[1-9][0-9]*/' + re.escape(tail), url.path) is not None)
    if url.scheme!='https' or url.hostname!='api.github.com' or url.port not in (None,443) or url.username or url.password or url.fragment or not same_surface:_fail('UNSAFE_PAGINATION')
    query=parse_qs(url.query,strict_parsing=True)
    expected={'per_page':['100'],'page':[str(page+1)]}
    if tail=='pulls':expected['state']=['open']
    if query!=expected:_fail('INVALID_PAGINATION')
    return page+1


def _pages(budget,repo,tail,field=None):
    rows=[];page=1;total=None
    while page<=MAX_PAGES:
        query=({'state':'open','per_page':100,'page':page} if tail=='pulls' else {'per_page':100,'page':page})
        try:
            response=budget.get(f'repos/{repo}/{tail}?{urlencode(query)}')
            value=response.data
            if field:
                if not isinstance(value,dict):_fail('INVALID_COLLECTION')
                total=_integer(value.get('total_count'),maximum=10000000)
                value=value.get(field)
            if not isinstance(value,list) or len(value)>100:_fail('INVALID_COLLECTION')
            rows.extend(value)
            next_page=_next_page(response.headers,repo,tail,page)
            if next_page is None:
                return rows,total is None or total==len(rows),None if total is None or total==len(rows) else 'PAGINATION_INCOMPLETE'
            if page==MAX_PAGES:return rows,False,'PAGINATION_BOUND'
            page=next_page
        except (TransportError,ValueError) as error:
            return rows,False,error.code if isinstance(error,TransportError) else 'INVALID_PAGINATION'
    return rows,False,'PAGINATION_BOUND'


def _prs(values):
    rows=[];seen=set()
    for value in values:
        if not isinstance(value,dict):_fail('INVALID_PR_METADATA')
        number=_integer(value.get('number'),minimum=1)
        if number in seen:_fail('DUPLICATE_PR_METADATA')
        seen.add(number)
        if type(value.get('draft')) is not bool:_fail('INVALID_PR_METADATA')
        rows.append(dict(number=number,head_sha=_sha(value.get('head',{}).get('sha')),base_sha=_sha(value.get('base',{}).get('sha')),draft=value['draft']))
    return rows


def _runs(values):
    rows=[];seen=set()
    for value in values:
        if not isinstance(value,dict):_fail('INVALID_RUN_METADATA')
        identity=_integer(value.get('id'),minimum=1)
        if identity in seen:_fail('DUPLICATE_RUN_METADATA')
        seen.add(identity)
        name=value.get('name')
        if not isinstance(name,str) or not 1<=len(name)<=240 or any(ord(c)<32 for c in name):_fail('INVALID_RUN_METADATA')
        if value.get('status') not in _STATUS or value.get('conclusion') not in _CONCLUSION:_fail('INVALID_RUN_METADATA')
        for name2 in ('created_at','updated_at'):
            if not isinstance(value.get(name2),str) or len(value[name2])>40:_fail('INVALID_RUN_METADATA')
        if _clock(value['created_at'])>_clock(value['updated_at']):_fail('INVALID_METADATA_CLOCK')
        row=dict(id=identity,name=name,status=value['status'],conclusion=value.get('conclusion'),head_sha=_sha(value.get('head_sha')),created_at=value['created_at'],updated_at=value['updated_at'],jobs_started=None)
        if value.get('workflow_id') is not None:row['workflow_id']=_integer(value['workflow_id'],minimum=1)
        rows.append(row)
    return rows


def _job_projection(values):
    rows=[];seen=set()
    started=0
    for value in values:
        if not isinstance(value,dict):_fail('INVALID_JOB_METADATA')
        identity=_integer(value.get('id'),minimum=1)
        if identity in seen:_fail('INVALID_JOB_METADATA')
        seen.add(identity)
        if value.get('status') not in _STATUS or value.get('conclusion') not in _CONCLUSION:_fail('INVALID_JOB_METADATA')
        steps=value.get('steps')
        if not isinstance(steps,list) or len(steps)>500:_fail('INVALID_JOB_METADATA')
        projected=[];executed=False
        for step in steps:
            if not isinstance(step,dict) or step.get('status') not in _STATUS or step.get('conclusion') not in _CONCLUSION:_fail('INVALID_JOB_METADATA')
            out={key:step.get(key) for key in ('status','conclusion','started_at','completed_at')}
            for name in ('started_at','completed_at'):
                if out[name] is not None and (not isinstance(out[name],str) or len(out[name])>40):_fail('INVALID_JOB_METADATA')
            started_at=_clock(out['started_at']) if out['started_at'] is not None else None
            completed_at=_clock(out['completed_at']) if out['completed_at'] is not None else None
            if completed_at is not None and (started_at is None or completed_at<started_at):_fail('INVALID_METADATA_CLOCK')
            projected.append(out)
            executed |= bool(started_at is not None and step.get('status') in ('in_progress','completed') and step.get('conclusion')!='skipped')
        started+=int(executed)
        rows.append(dict(id=identity,status=value['status'],conclusion=value.get('conclusion'),steps=projected))
    return rows,started


def _repository(budget,spec,known_commit=None):
    repo=spec['repository'];row=dict(repository=repo)
    try:commit=known_commit or _head(budget,repo)
    except TransportError as error:return dict(repository=repo,error_code=error.code)
    row.update(commit=commit,verified_commit=None,observed_at_utc=_utc(),pull_requests=[],workflow_runs=[],anchors=[],pr_pages_complete=False,runs_pages_complete=False)
    errors={}
    values,complete,error=_pages(budget,repo,'pulls')
    try:row['pull_requests']=_prs(values);row['pr_pages_complete']=complete
    except (TransportError,AttributeError) as ex:error=ex.code if isinstance(ex,TransportError) else 'INVALID_PR_METADATA'
    if error:errors['pull_requests']=error
    values,complete,error=_pages(budget,repo,'actions/runs','workflow_runs')
    try:row['workflow_runs']=_runs(values);row['runs_pages_complete']=complete
    except (TransportError,AttributeError) as ex:error=ex.code if isinstance(ex,TransportError) else 'INVALID_RUN_METADATA'
    if error:errors['workflow_runs']=error
    current=sorted((r for r in row['workflow_runs'] if r['head_sha']==commit),key=lambda r:(r['created_at'],r['id']),reverse=True)[:3]
    for run in current:
        jobs,complete,error=_pages(budget,repo,f'actions/runs/{run["id"]}/jobs','jobs')
        try:
            projection,started=_job_projection(jobs)
            run.update(jobs=projection,jobs_pages_complete=complete,jobs_started=started if complete else None)
        except TransportError as ex:error=ex.code
        if error:run['jobs_error_code']=error
    for path in spec.get('evidence_paths',[]):
        anchor=dict(path=path,status='MISSING',blob_sha=None,sha256=None,size=None)
        try:
            _path(path)
            raw,identity=_file(budget,repo,commit,path)
            anchor.update(status='PRESENT',blob_sha=identity,sha256=hashlib.sha256(raw).hexdigest(),size=len(raw))
        except TransportError as error:
            anchor['status']='BLOCKED' if error.code in ('PRIVATE_PATH_DENIED','HTTP_403','HTTP_429') else 'MISSING'
            anchor['error_code']=error.code
        row['anchors'].append(anchor)
    row['observed_at_utc']=_utc()
    if errors:row['acquisition_errors']=errors
    return row


def _coordination(budget,commit):
    state=dict(repository=BUS,commit=commit,owner_status=None,claims=[],complete=False)
    if commit is None:
        state['error_code']='COORDINATION_REPOSITORY_UNAVAILABLE';return state
    try:
        metadata=budget.get(f'repos/{BUS}/git/commits/{commit}').data
        if not isinstance(metadata,dict) or metadata.get('sha')!=commit:_fail('INVALID_TREE_METADATA')
        tree_sha=_sha(metadata.get('tree',{}).get('sha'))
        value=budget.get(f'repos/{BUS}/git/trees/{tree_sha}?recursive=1').data
        if not isinstance(value,dict) or value.get('sha')!=tree_sha or value.get('truncated') is not False:_fail('COORDINATION_TREE_INCOMPLETE')
        entries=value.get('tree')
        if not isinstance(entries,list) or len(entries)>MAX_TREE_ITEMS:_fail('COORDINATION_TREE_BOUND')
        records=[];seen=set()
        for item in entries:
            if not isinstance(item,dict):_fail('INVALID_TREE_METADATA')
            path=item.get('path')
            if not isinstance(path,str):_fail('INVALID_TREE_METADATA')
            relevant=path=='coordination/owner_status.json' or bool(re.fullmatch(r'coordination/(sessions|summaries)/[^/]+\.json',path)) or path.startswith('coordination/events/') and path.endswith('.json')
            if not relevant:continue
            _path(path)
            if path in seen or item.get('type')!='blob' or item.get('mode') not in ('100644','100755'):_fail('INVALID_COORDINATION_RECORD')
            seen.add(path);records.append((path,_sha(item.get('sha'))))
        if 'coordination/owner_status.json' not in seen or len(records)>MAX_COORD_RECORDS:_fail('COORDINATION_RECORD_BOUND')
        records.sort()
        # Only verified public JSON metadata is materialized; no remote Python.
        with tempfile.TemporaryDirectory(prefix='icarus2-coordination-') as temporary:
            root=Path(temporary)
            def acquire(item):
                path,sha=item;raw,identity=_file(budget,BUS,commit,path,expected_sha=sha)
                document=_json(raw)
                if not isinstance(document,dict):_fail('INVALID_COORDINATION_RECORD')
                target=root/path;target.parent.mkdir(parents=True,exist_ok=True)
                target.write_bytes(raw)
                return dict(path=path,blob_sha=identity,size=len(raw))
            with ThreadPoolExecutor(max_workers=8) as pool:
                fetched=list(pool.map(acquire,records))
            from coordination_fabric import compile_state
            compiled=compile_state(root,now=datetime.now(timezone.utc))
            state['owner_status']=compiled['owner_status']
            claims=[]
            for row in compiled['active_sessions']:
                claims.append(dict(session_id=row['session_id'],type=row['latest_type'],at_utc=row['last_event_at_utc'],targets=row['reserved_targets'],stale=row['stale'],coordination_mode=row['coordination_mode'],cooperates_with=row['cooperates_with']))
            state.update(claims=claims,complete=True,tree_sha=tree_sha,source_records=fetched,source_record_count=len(fetched))
    except (TransportError,ValueError,KeyError,TypeError,OSError,RecursionError) as error:
        state['error_code']=error.code if isinstance(error,TransportError) else 'COORDINATION_VALIDATION_FAILED'
    return state


def collect_snapshot(client=None,cycle_id=None):
    """Return one bounded source-pinned observation; failures remain explicit.

    Injected clients implement ``get(relative_rest_path) -> GitHubResponse``.
    They must obey the same deadline; the built-in gh client enforces it.
    """
    if cycle_id is None:cycle_id='icarus2-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    if not isinstance(cycle_id,str) or not _ID.fullmatch(cycle_id):_fail('INVALID_CYCLE_ID')
    budget=_Budget(client)
    snapshot=dict(schema_version='icarus2-snapshot-v1',cycle_id=cycle_id,started_at_utc=_utc(),completed_at_utc=None,
        manifest=dict(repository=ENGINE,commit=None,path=MANIFEST_PATH),coordination=dict(repository=BUS,commit=None,owner_status=None,claims=[],complete=False,error_code='COORDINATION_UNAVAILABLE'),repositories=[])
    try:
        commit=_head(budget,ENGINE);snapshot['manifest']['commit']=commit
        raw,identity=_file(budget,ENGINE,commit,MANIFEST_PATH)
        document=_json(raw)
        if not isinstance(document,dict) or document.get('schema_version')!='icarus-federated-repo-evidence-v1' or document.get('authority')!='RESEARCH_EVIDENCE_ONLY' or document.get('required_for_every_ai_unit') is not True:_fail('INVALID_MANIFEST')
        specs=document.get('repositories')
        if not isinstance(specs,list) or not 1<=len(specs)<=MAX_REPOSITORIES:_fail('INVALID_MANIFEST')
        repositories=[]
        for spec in specs:
            if not isinstance(spec,dict):_fail('INVALID_MANIFEST')
            repo=_repo(spec.get('repository'));repositories.append(repo)
            paths=spec.get('evidence_paths',[])
            if not isinstance(paths,list) or len(paths)>100 or any(not isinstance(path,str) for path in paths):_fail('INVALID_MANIFEST')
            for path in paths:_path(path,private_check=False)
            if len(paths)!=len(set(paths)):_fail('INVALID_MANIFEST')
        if len(repositories)!=len(set(repositories)):_fail('INVALID_MANIFEST')
        snapshot['manifest'].update(raw_json=raw.decode('utf-8'),document=document,blob_sha=identity,sha256=hashlib.sha256(raw).hexdigest())
        with ThreadPoolExecutor(max_workers=6) as pool:
            snapshot['repositories']=list(pool.map(lambda spec:_repository(budget,spec,commit if spec['repository']==ENGINE else None),specs))
        owner=next((r for r in snapshot['repositories'] if r['repository']==BUS),{})
        snapshot['coordination']=_coordination(budget,owner.get('commit'))
        for row in snapshot['repositories']:
            if 'commit' not in row:continue
            try:row['verified_commit']=_head(budget,row['repository'])
            except TransportError as error:row['verification_error_code']=error.code
    except (TransportError,UnicodeError) as error:
        snapshot['manifest']['error_code']=error.code if isinstance(error,TransportError) else 'INVALID_JSON'
    snapshot['completed_at_utc']=_utc()
    snapshot['transport']=dict(requests=budget.requests,response_bytes=budget.bytes,budget_exhausted=budget.exhausted,
        request_limit=MAX_REQUESTS,wall_seconds_limit=MAX_SECONDS,response_byte_limit=MAX_RESPONSE_BYTES,aggregate_byte_limit=MAX_AGGREGATE_BYTES,
        read_only=True,provider_requests=0)
    return snapshot
