"""Pure, bounded snapshot validation; this module grants no operational authority."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import PurePosixPath
import re

SCHEMA = 'icarus2-cycle-v1'
MAX_SNAPSHOT_BYTES = 8 * 1024 * 1024
MAX_REPOSITORIES = 64
MAX_ITEMS = 2_000
ENGINE = 'reppiks490/Icarus-engine'
BUS = 'reppiks490/icarus-owner-actions'
MANIFEST_PATH = 'config/federated_repo_evidence.json'
SWARMS = (
    ('VERITAS', 'authority_architecture'),
    ('HERMES', 'data_providers_corpora'),
    ('KEPLER', 'markets_execution'),
    ('MNEMOSYNE', 'brain_science_evidence'),
    ('SYNAPSE', 'integration_resilience'),
)
_STAMP = re.compile(r'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d{1,6})?(?:Z|[+-]\d\d:\d\d)\Z')
_REPO = re.compile(r'[A-Za-z0-9][A-Za-z0-9-]{0,99}/[A-Za-z0-9][A-Za-z0-9_.-]{0,99}\Z')
_ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,159}\Z')


def _fail(code='INVALID_SNAPSHOT'):
    # Do not echo repository-controlled strings, paths, or provider values.
    raise ValueError('Invalid Icarus 2 snapshot: ' + code)


def _object(value):
    if not isinstance(value, dict):
        _fail()
    return value


def _list(value, maximum=MAX_ITEMS):
    if not isinstance(value, list) or len(value) > maximum:
        _fail('COLLECTION_BOUND_OR_TYPE')
    return value


def _text(value, maximum=240):
    if not isinstance(value, str) or not value or len(value) > maximum or any(ord(c) < 32 for c in value):
        _fail()
    return value


def _repo(value):
    if not isinstance(value, str) or not _REPO.fullmatch(value):
        _fail('INVALID_REPOSITORY')
    return value


def _path(value):
    value = _text(value, 1024)
    raw = value[:-1] if value.endswith('/') else value
    path = PurePosixPath(raw)
    if (not raw or '\\' in raw or raw.startswith(('~', '/')) or ':' in raw
            or any(part in ('', '.', '..') for part in raw.split('/')) or path.is_absolute()):
        _fail('INVALID_PATH')
    return value


def _sha(value, length=40):
    if not isinstance(value, str) or not re.fullmatch('[0-9a-f]{' + str(length) + '}', value):
        _fail('INVALID_SOURCE_IDENTITY')
    return value


def _integer(value, maximum=10**15, minimum=0):
    if type(value) is not int or not minimum <= value <= maximum:
        _fail('INVALID_INTEGER')
    return value


def _boolean(value):
    if type(value) is not bool:
        _fail('INVALID_BOOLEAN')
    return value


def _stamp(value):
    if not isinstance(value, str) or not _STAMP.fullmatch(value):
        _fail('INVALID_CLOCK')
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if parsed.tzinfo is None or parsed.utcoffset() is None:
            _fail('INVALID_CLOCK')
        return parsed.astimezone(timezone.utc)
    except (ValueError, OverflowError):
        _fail('INVALID_CLOCK')


def _unique(values):
    if len(values) != len(set(values)):
        _fail('DUPLICATE_IDENTITY')


def _strict_json(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                _fail('DUPLICATE_JSON_KEY')
            result[key] = value
        return result
    def constant(_):
        _fail('NONFINITE_JSON')
    def floating(value):
        result = float(value)
        if not math.isfinite(result):
            _fail('NONFINITE_JSON')
        return result
    def integer(value):
        if len(value) > 128:
            _fail('SOURCE_INTEGER_BOUND')
        return int(value)
    try:
        return json.loads(raw, object_pairs_hook=pairs, parse_constant=constant,
                          parse_float=floating, parse_int=integer)
    except (ValueError, UnicodeError, RecursionError):
        _fail('INVALID_SOURCE_JSON')


def _bounded(snapshot):
    try:
        raw = json.dumps(snapshot, allow_nan=False).encode()
    except (ValueError, TypeError, OverflowError, RecursionError):
        _fail('INVALID_OR_NONFINITE_INPUT')
    if len(raw) > MAX_SNAPSHOT_BYTES:
        _fail('SNAPSHOT_BYTE_BOUND')
    stack = [(snapshot, 0)]
    nodes = 0
    while stack:
        value, depth = stack.pop()
        nodes += 1
        if nodes > 200_000 or depth > 32:
            _fail('SNAPSHOT_STRUCTURE_BOUND')
        if isinstance(value, dict):
            if any(not isinstance(key, str) for key in value):
                _fail('INVALID_OBJECT_KEY')
            stack.extend((item, depth + 1) for item in value.values())
        elif isinstance(value, list):
            stack.extend((item, depth + 1) for item in value)


def _manifest(value):
    source = _object(value)
    if source.get('repository') != ENGINE or source.get('path') != MANIFEST_PATH:
        _fail('WRONG_MANIFEST_AUTHORITY')
    if source.get('error_code') is not None:
        error = source['error_code']
        if not isinstance(error, str) or not re.fullmatch('[A-Z0-9_]{1,80}', error):
            _fail('INVALID_ACQUISITION_ERROR')
        return None, dict(repository=ENGINE, path=MANIFEST_PATH, verified=False,
            commit=_sha(source['commit']) if source.get('commit') is not None else None,
            blob_sha=None, sha256=None)
    commit = _sha(source.get('commit'))
    raw_json = source.get('raw_json')
    if not isinstance(raw_json, str) or len(raw_json.encode()) > 1024 * 1024:
        _fail('MANIFEST_BYTE_BOUND_OR_TYPE')
    raw = raw_json.encode()
    sha256 = hashlib.sha256(raw).hexdigest()
    blob = hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
    if _sha(source.get('sha256'), 64) != sha256 or _sha(source.get('blob_sha')) != blob:
        _fail('MANIFEST_IDENTITY_MISMATCH')
    document = _object(_strict_json(raw_json))
    if 'document' in source and source['document'] != document:
        _fail('MANIFEST_PROJECTION_MISMATCH')
    if (document.get('schema_version') != 'icarus-federated-repo-evidence-v1'
            or document.get('required_for_every_ai_unit') is not True
            or document.get('authority') != 'RESEARCH_EVIDENCE_ONLY'
            or document.get('execution_authorized', False) is not False):
        _fail('INVALID_MANIFEST_AUTHORITY')
    specs = _list(document.get('repositories'), MAX_REPOSITORIES)
    if not specs:
        _fail('EMPTY_REPOSITORY_UNIVERSE')
    normalized = []
    for spec in specs:
        spec = _object(spec)
        evidence = [_path(path) for path in _list(spec.get('evidence_paths'))]
        _unique(evidence)
        if not evidence:
            _fail('EMPTY_EVIDENCE_CONTRACT')
        normalized.append(dict(repository=_repo(spec.get('repository')), role=_text(spec.get('role')),
            data_authority=_text(spec.get('data_authority')), evidence_paths=evidence))
    _unique([spec['repository'] for spec in normalized])
    return normalized, dict(repository=ENGINE, commit=commit, path=MANIFEST_PATH,
        blob_sha=blob, sha256=sha256, verified=True)


def _job_evidence(run, completed):
    complete = _boolean(run.get('jobs_pages_complete', False))
    if 'jobs' not in run:
        return False, False, False
    jobs = _list(run['jobs'])
    identifiers, observed_started = [], 0
    failed, unfinished = False, False
    for job in jobs:
        job = _object(job)
        identifiers.append(_integer(job.get('id'), minimum=1))
        job_status = _text(job.get('status'), 40)
        conclusion = job.get('conclusion')
        if conclusion is not None:
            _text(conclusion, 64)
        failed |= conclusion in ('failure', 'timed_out', 'action_required', 'startup_failure')
        unfinished |= job_status != 'completed'
        started = False
        for step in _list(job.get('steps')):
            step = _object(step)
            step_status = _text(step.get('status'), 40)
            step_conclusion = step.get('conclusion')
            if step_conclusion is not None:
                _text(step_conclusion, 64)
            begin = _stamp(step['started_at']) if step.get('started_at') is not None else None
            end = _stamp(step['completed_at']) if step.get('completed_at') is not None else None
            if ((begin is not None and begin > completed) or (end is not None and end > completed)
                    or (begin is not None and end is not None and begin > end)):
                _fail('FUTURE_OR_INCONSISTENT_JOB_CLOCK')
            started |= (begin is not None and step_status in ('in_progress', 'completed')
                        and step_conclusion != 'skipped')
        observed_started += int(started)
    _unique(identifiers)
    if complete and run.get('jobs_started') != observed_started:
        _fail('JOB_EXECUTION_COUNT_MISMATCH')
    return complete, failed, unfinished


def _ci(runs, commit, completed):
    normalized = []
    for run in _list(runs):
        run = _object(run)
        created, updated = _stamp(run.get('created_at')), _stamp(run.get('updated_at'))
        if created > updated or updated > completed:
            _fail('FUTURE_OR_INCONSISTENT_RUN_CLOCK')
        status = run.get('status')
        if status not in ('queued', 'requested', 'waiting', 'pending', 'in_progress', 'completed'):
            _fail('INVALID_WORKFLOW_STATUS')
        conclusion = run.get('conclusion')
        if conclusion is not None:
            _text(conclusion, 64)
        started = run.get('jobs_started')
        if started is not None:
            _integer(started, maximum=10_000)
        jobs_complete, jobs_failed, jobs_unfinished = _job_evidence(run, completed)
        name = _text(run.get('name'))
        workflow = run.get('workflow_id')
        if workflow is not None:
            _integer(workflow, minimum=1)
        normalized.append(dict(id=_integer(run.get('id'), minimum=1), name=name,
            status=status, conclusion=conclusion, head_sha=_sha(run.get('head_sha')),
            created_at=run['created_at'], updated_at=run['updated_at'], jobs_started=started,
            workflow_id=workflow, jobs_pages_complete=jobs_complete,
            job_failure_observed=jobs_failed, job_unfinished_observed=jobs_unfinished))
    _unique([run['id'] for run in normalized])
    current = [run for run in normalized if run['head_sha'] == commit]
    # Keep earlier same-head outcomes as evidence; the newest run of each
    # workflow controls its current status. Different workflows cannot mask one
    # another, and unknown job execution never upgrades to observed success.
    latest = {}
    for run in current:
        key = ('id', run['workflow_id']) if run['workflow_id'] is not None else ('name', run['name'])
        old = latest.get(key)
        if old is None or (_stamp(run['created_at']), run['id']) > (_stamp(old['created_at']), old['id']):
            latest[key] = run
    selected = sorted(latest.values(), key=lambda row: (row['name'], row['id']))
    statuses = []
    for run in selected:
        if run['status'] != 'completed':
            state = 'PENDING'
        elif not run['jobs_pages_complete']:
            state = 'UNVERIFIED'
        elif run['jobs_started'] == 0:
            state = 'NOT_STARTED'
        elif run['jobs_started'] is None:
            state = 'UNVERIFIED'
        elif run['job_failure_observed']:
            state = 'OBSERVED_FAILURE'
        elif run['job_unfinished_observed']:
            state = 'UNVERIFIED'
        elif run['conclusion'] == 'success':
            state = 'OBSERVED_SUCCESS'
        elif run['conclusion'] in ('failure', 'timed_out', 'action_required', 'startup_failure'):
            state = 'OBSERVED_FAILURE'
        else:
            state = 'NOT_SUCCESSFUL'
        statuses.append(state)
    priority = ('OBSERVED_FAILURE', 'NOT_STARTED', 'PENDING', 'UNVERIFIED', 'NOT_SUCCESSFUL')
    overall = next((value for value in priority if value in statuses), 'OBSERVED_SUCCESS' if statuses else 'UNVERIFIED')
    return dict(current_head_status=overall, successful_current_runs=statuses.count('OBSERVED_SUCCESS'),
        current_runs=len(current), workflows_observed=len(selected), historical_runs=len(normalized) - len(current),
        selected_runs=selected, execution_verified=overall == 'OBSERVED_SUCCESS')


def _pull_requests(values):
    rows = []
    for value in _list(values):
        value = _object(value)
        row = dict(number=_integer(value.get('number'), minimum=1), head_sha=_sha(value.get('head_sha')),
            base_sha=_sha(value.get('base_sha')), draft=_boolean(value.get('draft')))
        rows.append(row)
    _unique([row['number'] for row in rows])
    return rows


def _anchors(values):
    rows = []
    for value in _list(values):
        value = _object(value)
        status = value.get('status')
        if status not in ('PRESENT', 'MISSING', 'BLOCKED'):
            _fail('INVALID_ANCHOR_STATUS')
        kind = value.get('kind', 'file')
        if kind not in ('file', 'tree'):
            _fail('INVALID_ANCHOR_KIND')
        row = dict(path=_path(value.get('path')), status=status, kind=kind,
            blob_sha=value.get('blob_sha'), sha256=value.get('sha256'), size=value.get('size'))
        if status == 'PRESENT':
            _sha(row['blob_sha'])
            _sha(row['sha256'], 64)
            _integer(row['size'], maximum=64 * 1024 * 1024)
        elif any(row[field] is not None for field in ('blob_sha', 'sha256', 'size')):
            _fail('UNAVAILABLE_ANCHOR_HAS_CONTENT_IDENTITY')
        rows.append(row)
    _unique([row['path'] for row in rows])
    return rows


def _coordination(value, completed):
    coordination = _object(value)
    if coordination.get('repository') != BUS:
        _fail('WRONG_COORDINATION_AUTHORITY')
    complete = _boolean(coordination.get('complete', True))
    commit = (_sha(coordination.get('commit')) if complete or coordination.get('commit') is not None
              else None)
    owner = coordination.get('owner_status')
    if owner is None and not complete:
        owner_verified = False
    else:
        owner = _object(owner)
        if (owner.get('schema_version') != 'icarus-coordination-owner-status-v1'
                or owner.get('live_broker_arming') is not False):
            _fail('OWNER_AUTHORITY_NOT_DISABLED')
        owner_verified = commit is not None
    error = coordination.get('error_code')
    if error is not None and not re.fullmatch('[A-Z0-9_]{1,80}', _text(error, 80)):
        _fail('INVALID_ACQUISITION_ERROR')
    reserved, sessions, modes = [], [], {}
    for claim in _list(coordination.get('claims'), 512):
        claim = _object(claim)
        sid = claim.get('session_id')
        if not isinstance(sid, str) or not _ID.fullmatch(sid):
            _fail('INVALID_CLAIM_IDENTITY')
        sessions.append(sid)
        if _stamp(claim.get('at_utc')) > completed:
            _fail('FUTURE_CLAIM_CLOCK')
        kind = claim.get('type')
        if kind not in ('REGISTERED','START','PLAN','CLAIM','HEARTBEAT','WAITING','UPDATE','BLOCKED','HANDOFF','RELEASE','COMPLETE','CANCELLED','NOTE'):
            _fail('INVALID_CLAIM_TYPE')
        mode = claim.get('coordination_mode', 'independent')
        if mode not in ('independent', 'cooperate'):
            _fail('INVALID_COOPERATION_MODE')
        cooperates = _list(claim.get('cooperates_with', []), 512)
        if any(not isinstance(other, str) or not _ID.fullmatch(other) for other in cooperates):
            _fail('INVALID_COOPERATION_IDENTITY')
        _unique(cooperates)
        modes[sid] = (mode, cooperates)
        stale = claim.get('stale', False)
        _boolean(stale)
        targets = []
        for target in _list(claim.get('targets')):
            target = _object(target)
            targets.append((_repo(target.get('repo')), _path(target.get('path'))))
        _unique(targets)
        if kind in ('RELEASE','COMPLETE','CANCELLED') or stale:
            continue
        reserved.extend(dict(session_id=sid, repository=repo, path=path,
            handoff_only=sid.lower().startswith('icarus1')) for repo, path in targets)
        if len(reserved) > 512:
            _fail('RESERVATION_BOUND')
    _unique(sessions)
    collisions = []
    collisions_complete = True
    for index, left in enumerate(reserved):
        for right in reserved[index+1:]:
            left_mode, left_peers = modes[left['session_id']]
            right_mode, right_peers = modes[right['session_id']]
            if (left_mode == right_mode == 'cooperate'
                    and right['session_id'] in left_peers and left['session_id'] in right_peers):
                continue
            lpath, rpath = left['path'].rstrip('/'), right['path'].rstrip('/')
            if (left['session_id'] != right['session_id'] and left['repository'] == right['repository']
                    and (lpath == rpath or lpath.startswith(rpath + '/') or rpath.startswith(lpath + '/'))):
                collisions.append(dict(repository=left['repository'], sessions=sorted((left['session_id'], right['session_id'])),
                    paths=sorted((left['path'], right['path']))))
                if len(collisions) == 128:
                    collisions_complete = False
                    break
        if not collisions_complete:
            break
    return dict(repository=BUS, commit=commit, complete=complete, owner_status_verified=owner_verified,
        live_broker_arming=False if owner_verified else None,
        reserved_targets=reserved, collisions=collisions, collisions_complete=collisions_complete)


def _finish(snapshot, source, coordination, reports, gaps, expected_count):
    for collision in coordination['collisions']:
        gaps.append(dict(code='CLAIM_COLLISION', repository=collision['repository'],
            sessions=collision['sessions'], paths=collision['paths']))
    if not coordination['collisions_complete']:
        gaps.append(dict(code='COLLISION_REPORT_TRUNCATED', repository=BUS))
    drift_codes = {'REPOSITORY_DRIFT', 'MANIFEST_REVISION_MISMATCH', 'COORDINATION_REVISION_MISMATCH'}
    status = ('RESTART_CYCLE_REQUIRED' if any(item['code'] in drift_codes for item in gaps)
        else 'INCOMPLETE' if gaps else 'SNAPSHOT_VALIDATED')
    handoffs = [dict(gap_record, automatic_repair_authorized=False,
        required_next_step='CLAIM_AND_VERIFY_BEFORE_REPAIR') for gap_record in gaps]
    output = dict(schema_version=SCHEMA, cycle_id=snapshot['cycle_id'], worker='Icarus 2',
        started_at_utc=snapshot['started_at_utc'], completed_at_utc=snapshot['completed_at_utc'], status=status,
        metadata_only=True, system_ready=False, execution_authorized=False, automatic_merge_authorized=False,
        source=source, coordination=coordination, repositories=reports, gaps=gaps, handoffs=handoffs,
        swarms=[dict(role=role, scope=scope, status='SCOPE_ONLY', agent_execution_observed=False) for role, scope in SWARMS],
        summary=dict(repositories_expected=expected_count,
            repositories_observed=sum(row['commit'] is not None for row in reports),
            evidence_anchors_present=sum(anchor['status']=='PRESENT' for row in reports for anchor in row['anchors']),
            open_pull_requests=sum(len(row['pull_requests']) for row in reports), gaps=len(gaps)),
        limits=dict(snapshot_bytes=MAX_SNAPSHOT_BYTES, repository_count=MAX_REPOSITORIES,
            collection_items=MAX_ITEMS, unknown_universe_closed=False))
    if len(json.dumps(output, allow_nan=False).encode()) > MAX_SNAPSHOT_BYTES:
        _fail('REPORT_BYTE_BOUND')
    return output


def build_cycle(snapshot: dict, *, now: datetime | None = None) -> dict:
    """Validate one immutable metadata snapshot and emit a bounded handoff.

    Raises ``ValueError`` on malformed/untrusted structure. Coherent partial
    acquisition is a reportable INCOMPLETE result, not fabricated healthy data.
    This function has no network, filesystem mutation, scheduler or execution
    capability. Successful metadata validation never proves system readiness.
    """
    snapshot = _object(snapshot)
    _bounded(snapshot)
    if snapshot.get('schema_version') != 'icarus2-snapshot-v1':
        _fail('INVALID_SNAPSHOT_SCHEMA')
    cycle_id = snapshot.get('cycle_id')
    if not isinstance(cycle_id, str) or not _ID.fullmatch(cycle_id):
        _fail('INVALID_CYCLE_ID')
    for field in ('execution_authorized', 'automatic_merge_authorized', 'system_ready'):
        if snapshot.get(field, False) is not False:
            _fail('FORBIDDEN_AUTHORITY')
    started, completed = _stamp(snapshot.get('started_at_utc')), _stamp(snapshot.get('completed_at_utc'))
    if started > completed:
        _fail('INVALID_CYCLE_CLOCK')
    # The validation clock is supplied by the caller/runtime, never by the
    # untrusted snapshot. Injection keeps historical checks deterministic.
    now = datetime.now(timezone.utc) if now is None else now
    if not isinstance(now, datetime) or now.tzinfo is None or now.utcoffset() is None:
        _fail('INVALID_VALIDATION_CLOCK')
    if completed > now:
        _fail('FUTURE_CYCLE_CLOCK')
    specs, source = _manifest(snapshot.get('manifest'))
    coordination = _coordination(snapshot.get('coordination'), completed)
    raw_rows = _list(snapshot.get('repositories'), MAX_REPOSITORIES)
    _unique([_repo(_object(row).get('repository')) for row in raw_rows])
    observed = {row['repository']: row for row in raw_rows}
    gaps = []
    def gap(code, repository=None, path=None, **extra):
        row = dict(code=code, **extra)
        if repository is not None:
            row['repository'] = repository
        if path is not None:
            row['path'] = path
        gaps.append(row)
    if not coordination['complete']:
        gap('COORDINATION_SNAPSHOT_INCOMPLETE', BUS)
    if not coordination['owner_status_verified']:
        gap('OWNER_STATUS_UNAVAILABLE', BUS)
    if specs is None:
        gap('MANIFEST_UNAVAILABLE', ENGINE)
        # Repository observations cannot establish their own authority or
        # denominator when the canonical universe is unavailable.
        for repo in sorted(observed):
            gap('UNVERIFIED_REPOSITORY_WITHOUT_MANIFEST', repo)
        return _finish(snapshot, source, coordination, [], gaps, None)
    expected = {spec['repository']: spec for spec in specs}
    # The universe is extensible, but the two authorities defining its source
    # and coordination contract must themselves be revision-reconciled.
    for authority in (ENGINE, BUS):
        if authority not in expected:
            gap('REQUIRED_AUTHORITY_NOT_IN_UNIVERSE', authority)
    for repo in sorted(set(observed) - set(expected)):
        gap('UNDECLARED_REPOSITORY', repo)
    reports = []
    for spec in specs:
        repo = spec['repository']
        row = observed.get(repo)
        base = dict(repository=repo, role=spec['role'], data_authority=spec['data_authority'], runtime_health='UNVERIFIED')
        if row is None or row.get('error_code') is not None:
            if row is not None:
                error = _text(row['error_code'], 80)
                if not re.fullmatch('[A-Z0-9_]+', error):
                    _fail('INVALID_ACQUISITION_ERROR')
            gap('REPOSITORY_MISSING' if row is None else 'REPOSITORY_UNAVAILABLE', repo)
            reports.append(dict(base, commit=None, verified_commit=None, snapshot_status='INCOMPLETE',
                ci=dict(current_head_status='UNVERIFIED', successful_current_runs=0, current_runs=0,
                    workflows_observed=0, historical_runs=0, selected_runs=[], execution_verified=False),
                anchors=[], pull_requests=[]))
            continue
        commit = _sha(row.get('commit'))
        verified = _sha(row['verified_commit']) if row.get('verified_commit') is not None else None
        verification_error = row.get('verification_error_code')
        if verification_error is not None:
            if (not isinstance(verification_error, str)
                    or not re.fullmatch('[A-Z0-9_]{1,80}', verification_error)
                    or verified is not None):
                _fail('INVALID_VERIFICATION_ERROR')
        # Acquisition-start time, not a claim that every mutable API response
        # already existed then. Run updates are bounded by cycle completion.
        observed_time = _stamp(row.get('observed_at_utc'))
        if not started <= observed_time <= completed:
            _fail('FUTURE_OR_OUTSIDE_CYCLE_OBSERVATION')
        before = len(gaps)
        if verified is None:
            gap('HEAD_VERIFICATION_UNAVAILABLE', repo, error_code=verification_error)
        elif commit != verified:
            gap('REPOSITORY_DRIFT', repo)
        if repo == ENGINE and source['commit'] != commit:
            gap('MANIFEST_REVISION_MISMATCH', repo)
        if repo == BUS and coordination['commit'] is not None and coordination['commit'] != commit:
            gap('COORDINATION_REVISION_MISMATCH', repo)
        for field in ('pr_pages_complete', 'runs_pages_complete'):
            if not _boolean(row.get(field)):
                gap('PAGINATION_INCOMPLETE', repo, collection=field)
        prs = _pull_requests(row.get('pull_requests'))
        ci = _ci(row.get('workflow_runs'), commit, completed)
        if ci['current_head_status'] != 'OBSERVED_SUCCESS':
            gap('CURRENT_HEAD_CI_' + ci['current_head_status'], repo)
        anchors = _anchors(row.get('anchors'))
        by_path = {anchor['path']: anchor for anchor in anchors}
        for path in spec['evidence_paths']:
            if path not in by_path or by_path[path]['status'] != 'PRESENT':
                gap('EVIDENCE_ANCHOR_UNAVAILABLE', repo, path)
        for path in sorted(set(by_path) - set(spec['evidence_paths'])):
            gap('UNDECLARED_EVIDENCE_ANCHOR', repo, path)
        reports.append(dict(base, commit=commit, verified_commit=verified,
            verification_error_code=verification_error, observed_at_utc=row['observed_at_utc'], snapshot_status='INCOMPLETE' if len(gaps) > before else 'METADATA_OBSERVED',
            ci=ci, anchors=anchors, pull_requests=prs))
    return _finish(snapshot, source, coordination, reports, gaps, len(expected))
