from pathlib import Path
import unittest


WORKFLOW = Path('.github/workflows/coordination-maintenance.yml')
README = Path('coordination/README.md')


class CoordinationMaintenanceHardeningTests(unittest.TestCase):
    def test_one_workflow_handles_push_refresh_schedule_and_manual_cleanup(self):
        text = WORKFLOW.read_text(encoding='utf-8')
        self.assertIn('push:', text)
        self.assertIn('schedule:', text)
        self.assertIn("cron: '2-57/5 * * * *'", text)
        self.assertIn("github.event_name == 'workflow_dispatch' && inputs.retention_days || '0'", text)
        self.assertIn('workflow_dispatch:', text)
        self.assertIn('retention_days:', text)
        self.assertIn("default: '14'", text)
        self.assertIn('contents: write', text)

    def test_generated_state_is_recomputed_from_fresh_main_and_retried_on_concurrency(self):
        text = WORKFLOW.read_text(encoding='utf-8')
        self.assertIn('for attempt in 1 2 3 4 5 6 7 8', text)
        self.assertIn('git fetch origin main', text)
        self.assertIn('git reset --hard origin/main', text)
        self.assertIn('python -m coordination_fabric validate', text)
        self.assertIn('python -m coordination_fabric compile', text)
        self.assertIn('coordination/ACTIVE.md', text)
        self.assertIn('coordination/index.json', text)
        self.assertIn('coordination/collisions.json', text)
        self.assertIn('[skip ci]', text)
        self.assertIn('git push origin HEAD:main', text)
        self.assertIn("assert isinstance(d.get('collisions'), list)", text)
        self.assertNotIn("assert not d['collisions']", text)

    def test_pruning_is_positive_bounded_summary_gated_and_recomputed_afterward(self):
        text = WORKFLOW.read_text(encoding='utf-8')
        self.assertIn('RETENTION_DAYS', text)
        self.assertIn('python -m coordination_fabric prune --days "$RETENTION_DAYS"', text)
        self.assertIn('3650', text)
        prune_pos = text.index('python -m coordination_fabric prune --days')
        compile_pos = text.rindex('python -m coordination_fabric compile')
        self.assertLess(prune_pos, compile_pos)

    def test_operator_docs_explain_automatic_refresh_and_easy_cleanup(self):
        text = README.read_text(encoding='utf-8').lower()
        for phrase in ('automatically', 'active.md', 'workflow_dispatch', 'retention', 'prune', 'git history'):
            self.assertIn(phrase, text)
        self.assertIn('active', text)
        self.assertIn('waiting', text)
        self.assertIn('summary', text)


if __name__ == '__main__':
    unittest.main()
