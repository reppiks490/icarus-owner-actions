"""Offline requirement compilation and fail-closed evidence-record validation.

No network, subprocess, provider, broker or scheduler operations. Validation
checks record consistency; it cannot establish the truth of submitted evidence.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

BASELINE = frozenset(range(1, 203))
STATES = frozenset(('DISCOVERED', 'NOT_STARTED', 'DEPENDENCY_BLOCKED', 'READY',
    'IN_PROGRESS', 'IMPLEMENTED_UNVERIFIED', 'VERIFIED', 'INTEGRATED', 'BLOCKED',
    'AWAITING_APPROVAL', 'RESEARCH_HYPOTHESIS', 'UNKNOWN', 'NOT_APPLICABLE'))
INVARIANTS = ('chatgpt_automation_changes_authorized', 'live_trading_authorized',
    'broker_activation_authorized', 'new_spend_authorized', 'force_push_authorized',
    'unreviewed_merge_authorized', 'protected_holdout_tuning_authorized')


def require(condition, message):
    if not condition: raise ValueError(message)


def sha(value, size):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{' + str(size) + '}', value) is not None


def timestamp(value):
    require(isinstance(value, str), 'timestamp string required')
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    require(parsed.tzinfo is not None, 'timestamp must have timezone')


def compile_directive(text):
    require(isinstance(text, str), 'directive text required')
    matches = list(re.finditer(r'^## (\d+)\. (.+)$', text, re.M))
    ids = [int(m[1]) for m in matches]
    require(len(ids) == len(set(ids)), 'duplicate requirement headings')
    require(BASELINE <= set(ids), 'baseline requirements missing')
    requirements = [dict(id=int(m[1]), title=m[2], owner='UNASSIGNED_DOMAIN_OWNER',
        work_package_id=f'WP-{int(m[1]):03d}', completion_state='DISCOVERED',
        priority='UNTRIAGED', dependencies=[], acceptance_criteria=[m[2]],
        evidence=[], consumers=[], blockers=['Implementation and owner not verified'],
        exact_next_action='Inspect implementation/ownership and define component-specific acceptance tests.',
        execution_authorized=False) for m in matches]
    record = dict(schema_version='1.0', mission_state='PARTIAL',
        source_sha256=hashlib.sha256(text.encode()).hexdigest(),
        observed_at=datetime.now(timezone.utc).isoformat(),
        invariants={key: False for key in INVARIANTS}, requirements=requirements)
    validate(record)
    return record


def validate_coverage(coverage):
    require(isinstance(coverage, dict), 'coverage object required')
    if coverage.get('status') != 'COMPLETE_WITHIN_VERIFIED_ENTITLEMENT': return
    require(coverage.get('eligible_scope_known') is True, 'unknown coverage denominator')
    require(coverage.get('license_verified') is True, 'unverified license')
    require(coverage.get('acquisition_kind') == 'PRODUCTION', 'diagnostic data cannot prove full acquisition')
    require(bool(coverage.get('entitlement_identity')), 'entitlement identity required')
    require(sha(coverage.get('manifest_sha256'), 64), 'coverage manifest hash required')
    eligible, validated = coverage.get('eligible_partitions'), coverage.get('validated_partitions')
    for values in (eligible, validated):
        require(isinstance(values, list) and values and all(isinstance(v, str) and v for v in values),
            'explicit nonempty partition identities required')
        require(len(values) == len(set(values)), 'duplicate partitions')
    require(set(eligible) == set(validated), 'eligible and validated partitions differ')
    durable = coverage.get('durable_partitions')
    require(isinstance(durable, list) and durable, 'durable partition witnesses required')
    stored = set()
    for partition in durable:
        require(isinstance(partition, dict), 'durable partition object required')
        ident = partition.get('partition_id')
        require(isinstance(ident, str) and ident and ident not in stored,
            'invalid or duplicate durable partition identity')
        stored.add(ident)
        require(isinstance(partition.get('storage_identity'), str) and partition['storage_identity'],
            'durable storage identity required')
        require(sha(partition.get('sha256'), 64), 'durable byte hash required')
        require(partition.get('integrity_verified') is True, 'durable integrity proof required')
        for quantity in ('rows', 'bytes'):
            require(type(partition.get(quantity)) is int and partition[quantity] >= 0,
                'nonnegative integer ' + quantity + ' required')
        timestamp(partition.get('verified_at'))
    require(stored == set(eligible), 'durable and eligible partitions differ')


def validate(record):
    require(isinstance(record, dict), 'record object required')
    require(record.get('schema_version') == '1.0', 'unsupported schema')
    require(isinstance(record.get('invariants'), dict), 'invariants object required')
    for key in INVARIANTS:
        require(record.get('invariants', {}).get(key) is False, 'mandatory authority invariant: ' + key)
    rows = record.get('requirements')
    require(isinstance(rows, list), 'requirements list required')
    ids, packages = set(), set()
    for row in rows:
        require(isinstance(row, dict), 'requirement object required')
        ident = row.get('id')
        require(type(ident) is int and ident > 0 and ident not in ids, 'invalid or duplicate requirement id')
        ids.add(ident)
        require(bool(row.get('title')) and bool(row.get('acceptance_criteria')), 'title and acceptance required')
        require(row.get('execution_authorized') is False, 'research-only authority required')
        state = row.get('completion_state')
        require(state in STATES, 'unknown completion state')
        if state == 'NOT_APPLICABLE':
            require(bool(row.get('disposition_reason')), 'NOT_APPLICABLE reason required')
        package = row.get('work_package_id')
        require(isinstance(package, str) and package, 'work package identity required')
        packages.add(package)
        deps = row.get('dependencies')
        require(isinstance(deps, list) and all(isinstance(d, str) for d in deps), 'dependencies list required')
        if 'data_coverage' in row: validate_coverage(row['data_coverage'])
        if state not in ('VERIFIED', 'INTEGRATED'): continue
        require(isinstance(row.get('owner'), str) and row['owner'] and not row['owner'].startswith('UNASSIGNED'), 'verified requirement needs assigned owner')
        require(not row.get('blockers'), 'blocked requirement cannot be verified')
        v = row.get('verification', {})
        require(isinstance(v, dict), 'verification object required')
        require(bool(v.get('repository')) and sha(v.get('commit_sha'), 40), 'pinned source required')
        timestamp(v.get('verified_at'))
        require(bool(v.get('method')), 'verification method required')
        require(v.get('vetoes') == [], 'critical veto prevents completion')
        tests = v.get('tests')
        require(isinstance(tests, list) and tests, 'test evidence required')
        for test in tests:
            require(isinstance(test, dict), 'test evidence object required')
            require(bool(test.get('command')) and type(test.get('exit_code')) is int
                and test['exit_code'] == 0 and test.get('commit_sha') == v['commit_sha'],
                'passing exact-source test required')
        artifacts = v.get('artifacts')
        require(isinstance(artifacts, list) and artifacts, 'persisted evidence required')
        for artifact in artifacts:
            require(isinstance(artifact, dict), 'artifact evidence object required')
            require(bool(artifact.get('identity')) and sha(artifact.get('sha256'), 64), 'artifact identity/hash required')
        if state == 'INTEGRATED':
            consumers = row.get('consumers')
            require(isinstance(consumers, list) and consumers, 'actual consumer required')
            for consumer in consumers:
                require(isinstance(consumer, dict), 'consumer evidence object required')
                require(bool(consumer.get('identity')) and consumer.get('verified') is True
                    and consumer.get('artifact_identity') in {a['identity'] for a in artifacts}
                    and bool(consumer.get('contract_test')), 'verified bound consumer contract required')
    require(BASELINE <= ids, 'baseline requirements missing')
    graph = {p: set() for p in packages}
    for row in rows:
        for dep in row['dependencies']:
            require(dep in packages, 'dependency package missing: ' + dep)
            graph[row['work_package_id']].add(dep)
    visited, active = set(), set()
    def visit(node):
        require(node not in active, 'dependency cycle')
        if node in visited: return
        active.add(node)
        for dep in graph[node]: visit(dep)
        active.remove(node)
        visited.add(node)
    for node in graph: visit(node)
    return True


def certificate(record):
    validate(record)
    counts = Counter(row['completion_state'] for row in record['requirements'])
    return dict(schema_version='icarus-scoped-mission-certificate-v1',
        verification_scope='OFFLINE_RECORD_CONSISTENCY_ONLY',
        required_baseline_count=202, registered_count=len(record['requirements']),
        additional_discoveries=len(record['requirements'])-202,
        declared_verified_count=counts['VERIFIED']+counts['INTEGRATED'],
        declared_integrated_count=counts['INTEGRATED'], state_counts=dict(counts),
        entire_system_certified=False, completion_probability=None,
        limitation='Evidence truth, complete accessible universe, source-to-UI behavior and durability require independent verification.',
        execution_authorized=False)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    for name in ('compile', 'validate', 'certificate'):
        sub = commands.add_parser(name)
        sub.add_argument('input', type=Path)
        if name == 'compile': sub.add_argument('output', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'compile':
            result = compile_directive(args.input.read_text(encoding='utf-8'))
            with args.output.open('x', encoding='utf-8') as handle:
                json.dump(result, handle, indent=2, allow_nan=False)
                handle.write('\n')
        else:
            record = json.loads(args.input.read_text(encoding='utf-8'))
            result = certificate(record) if args.command == 'certificate' else dict(
                valid=validate(record), verification_scope='OFFLINE_RECORD_CONSISTENCY_ONLY')
        print(json.dumps(result, sort_keys=True, allow_nan=False))
        return 0
    except (ValueError, TypeError, KeyError, OSError) as exc:
        print(json.dumps(dict(status='BLOCKED_INVALID_RECORD', reason=str(exc))))
        return 2


if __name__ == '__main__': raise SystemExit(main())
