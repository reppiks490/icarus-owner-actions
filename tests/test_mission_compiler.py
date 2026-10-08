import copy
import unittest

from mission.compiler import compile_directive, validate, certificate


def document():
    return '\n'.join(f'## {i}. Requirement {i}\nVerify requirement {i}.' for i in range(1, 203))


class CompilerTests(unittest.TestCase):
    def setUp(self):
        self.record = compile_directive(document())

    def test_all_202_registered_without_success_credit(self):
        validate(self.record)
        result = certificate(self.record)
        self.assertEqual(result['required_baseline_count'], 202)
        self.assertEqual(result['registered_count'], 202)
        self.assertEqual(result['declared_verified_count'], 0)
        self.assertFalse(result['entire_system_certified'])

    def test_missing_requirement_rejected(self):
        self.record['requirements'].pop()
        with self.assertRaisesRegex(ValueError, 'baseline requirements missing'):
            validate(self.record)

    def test_duplicate_and_boolean_ids_rejected(self):
        for value in (2, True):
            record = copy.deepcopy(self.record)
            record['requirements'][0]['id'] = value
            with self.assertRaises(ValueError): validate(record)

    def test_compiler_rejects_duplicate_headings(self):
        with self.assertRaises(ValueError): compile_directive(document() + '\n## 1. Duplicate')

    def test_unknown_state_rejected(self):
        self.record['requirements'][0]['completion_state'] = 'PERFECT'
        with self.assertRaises(ValueError): validate(self.record)

    def test_verified_without_bound_tests_rejected(self):
        self.record['requirements'][0]['completion_state'] = 'VERIFIED'
        with self.assertRaisesRegex(ValueError, 'owner'):
            validate(self.record)

    def verified(self):
        row = self.record['requirements'][0]
        row.update(completion_state='VERIFIED', owner='offline-fixture-reviewer', blockers=[])
        row['verification'] = dict(repository='fixture/repo', commit_sha='a'*40,
            verified_at='2026-10-08T00:00:00+00:00', method='independent test readback',
            tests=[dict(command='synthetic fixture test', exit_code=0, commit_sha='a'*40)],
            artifacts=[dict(identity='fixture-artifact', sha256='b'*64)], vetoes=[])
        return row

    def test_negative_exit_and_boolean_exit_rejected(self):
        row = self.verified()
        for value in (1, False):
            row['verification']['tests'][0]['exit_code'] = value
            with self.assertRaises(ValueError): validate(self.record)

    def test_commit_mismatch_rejected(self):
        row = self.verified()
        row['verification']['tests'][0]['commit_sha'] = 'c'*40
        with self.assertRaises(ValueError): validate(self.record)

    def test_critical_veto_cannot_be_averaged_away(self):
        row = self.verified()
        row['verification']['vetoes'] = ['leakage']
        with self.assertRaises(ValueError): validate(self.record)

    def test_integrated_requires_real_consumer_record(self):
        row = self.verified()
        row['completion_state'] = 'INTEGRATED'
        with self.assertRaises(ValueError): validate(self.record)
        row['consumers'] = [dict(identity='fixture-consumer', verified=True,
            artifact_identity='fixture-artifact', contract_test='fixture contract')]
        validate(self.record)

    def test_unknown_coverage_and_diagnostic_samples_cannot_be_complete(self):
        row = self.verified()
        row['data_coverage'] = dict(status='COMPLETE_WITHIN_VERIFIED_ENTITLEMENT',
            eligible_partitions=None, validated_partitions=[], eligible_scope_known=False,
            license_verified=True, acquisition_kind='DIAGNOSTIC_ONLY')
        with self.assertRaises(ValueError): validate(self.record)

    def test_partition_identity_not_just_count(self):
        row = self.verified()
        row['data_coverage'] = dict(status='COMPLETE_WITHIN_VERIFIED_ENTITLEMENT',
            eligible_partitions=['a','b'], validated_partitions=['a','c'],
            eligible_scope_known=True, license_verified=True, acquisition_kind='PRODUCTION',
            entitlement_identity='fixture-entitlement', manifest_sha256='d'*64)
        with self.assertRaises(ValueError): validate(self.record)
        row['data_coverage']['validated_partitions'] = ['a','b']
        row['data_coverage']['durable_partitions'] = [self.partition('a'), self.partition('b')]
        validate(self.record)

    def partition(self, identity):
        return dict(partition_id=identity, storage_identity='fixture/'+identity,
            sha256='e'*64, rows=12, bytes=120, integrity_verified=True,
            verified_at='2026-10-08T00:00:00Z')

    def complete_coverage(self):
        row = self.verified()
        row['data_coverage'] = dict(status='COMPLETE_WITHIN_VERIFIED_ENTITLEMENT',
            eligible_partitions=['a','b'], validated_partitions=['a','b'],
            eligible_scope_known=True, license_verified=True, acquisition_kind='PRODUCTION',
            entitlement_identity='fixture-entitlement', manifest_sha256='d'*64,
            durable_partitions=[self.partition('a'), self.partition('b')])
        return row['data_coverage']

    def test_validated_names_without_all_durable_bytes_cannot_be_complete(self):
        coverage = self.complete_coverage()
        coverage['durable_partitions'].pop()
        with self.assertRaises(ValueError): validate(self.record)

    def test_duplicate_or_unverified_storage_witness_cannot_prove_coverage(self):
        for bad in ('duplicate', 'unverified', 'missing_hash', 'missing_storage'):
            coverage = self.complete_coverage()
            if bad == 'duplicate': coverage['durable_partitions'][1] = self.partition('a')
            elif bad == 'unverified': coverage['durable_partitions'][1]['integrity_verified'] = False
            elif bad == 'missing_hash': coverage['durable_partitions'][1]['sha256'] = None
            else: coverage['durable_partitions'][1]['storage_identity'] = ''
            with self.assertRaises(ValueError): validate(self.record)

    def test_invalid_row_byte_count_or_naive_verification_clock_rejected(self):
        for field, value in [('rows', True), ('rows', -1), ('bytes', -1), ('bytes', '120'),
                             ('verified_at', '2026-10-08T00:00:00')]:
            coverage = self.complete_coverage()
            coverage['durable_partitions'][0][field] = value
            with self.assertRaises(ValueError): validate(self.record)

    def test_loop_trading_and_spend_expansion_rejected(self):
        for key in self.record['invariants']:
            record = copy.deepcopy(self.record)
            record['invariants'][key] = True
            with self.assertRaises(ValueError): validate(record)

    def test_dependency_cycle_and_missing_package_rejected(self):
        row = self.record['requirements'][0]
        row['dependencies'] = ['absent']
        with self.assertRaises(ValueError): validate(self.record)
        row['dependencies'] = ['WP-002']
        self.record['requirements'][1]['dependencies'] = ['WP-001']
        with self.assertRaises(ValueError): validate(self.record)

    def test_additional_discoveries_expand_disclosed_denominator(self):
        row = copy.deepcopy(self.record['requirements'][0])
        row.update(id=203, work_package_id='WP-203', title='Additional discovery')
        self.record['requirements'].append(row)
        self.assertEqual(certificate(self.record)['registered_count'], 203)

    def test_explicit_not_applicable_requires_reason(self):
        row = self.record['requirements'][0]
        row['completion_state'] = 'NOT_APPLICABLE'
        with self.assertRaises(ValueError): validate(self.record)
        row['disposition_reason'] = 'Fixture scope excludes this surface'
        validate(self.record)

    def test_malformed_nested_evidence_is_rejected_cleanly(self):
        for field in ('tests', 'artifacts'):
            self.verified()
            record = copy.deepcopy(self.record)
            record['requirements'][0]['verification'][field] = ['malformed']
            with self.assertRaises(ValueError): validate(record)
        self.record['invariants'] = []
        with self.assertRaises(ValueError): validate(self.record)


if __name__ == '__main__': unittest.main()
