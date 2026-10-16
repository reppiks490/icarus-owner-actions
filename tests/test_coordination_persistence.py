from __future__ import annotations

from pathlib import Path
import unittest


PUBLISH = Path('.github/workflows/coordination-fabric.yml')
MAINTENANCE = Path('.github/workflows/coordination-maintenance.yml')
README = Path('coordination/README.md')


class CoordinationPersistenceTests(unittest.TestCase):
    def test_main_push_publishes_compiled_views_from_fresh_main(self):
        text = PUBLISH.read_text(encoding='utf-8')
        self.assertIn('publish:', text)
        self.assertIn("github.event_name == 'push'", text)
        self.assertIn("github.ref == 'refs/heads/main'", text)
        self.assertIn('contents: write', text)
        self.assertIn('git reset --hard origin/main', text)
        self.assertIn('python -m coordination_fabric validate', text)
        self.assertIn('python -m coordination_fabric compile', text)
        self.assertIn('coordination/ACTIVE.md', text)
        self.assertIn('coordination/index.json', text)
        self.assertIn('coordination/collisions.json', text)
        self.assertIn("assert not d['collisions']", text)
        self.assertIn('[skip ci]', text)
        self.assertIn('git push origin HEAD:main', text)

    def test_maintenance_supports_scheduled_and_manual_safe_pruning(self):
        self.assertTrue(MAINTENANCE.exists(), 'coordination maintenance workflow is missing')
        text = MAINTENANCE.read_text(encoding='utf-8')
        self.assertIn('schedule:', text)
        self.assertIn('workflow_dispatch:', text)
        self.assertIn('retention_days:', text)
        self.assertIn('contents: write', text)
        self.assertIn('git reset --hard origin/main', text)
        self.assertIn('python -m coordination_fabric prune --days', text)
        self.assertIn('python -m coordination_fabric compile', text)
        self.assertIn("assert not d['collisions']", text)
        self.assertIn('[skip ci]', text)
        self.assertIn('git push origin HEAD:main', text)

    def test_operator_docs_explain_refresh_and_easy_cleanup(self):
        text = README.read_text(encoding='utf-8').lower()
        self.assertIn('automatically', text)
        self.assertIn('active.md', text)
        self.assertIn('workflow_dispatch', text)
        self.assertIn('retention', text)
        self.assertIn('prune', text)
        self.assertIn('git history', text)


if __name__ == '__main__':
    unittest.main()
