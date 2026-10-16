from pathlib import Path
import unittest


class CoordinationAutomationContractTests(unittest.TestCase):
    def test_main_push_compiles_generated_state_and_can_prune(self):
        workflow = Path('.github/workflows/coordination-maintenance.yml')
        self.assertTrue(workflow.exists(), 'coordination maintenance workflow is missing')
        text = workflow.read_text(encoding='utf-8')
        self.assertIn('contents: write', text)
        self.assertIn('coordination/events/**', text)
        self.assertIn('coordination/sessions/**', text)
        self.assertIn('coordination/summaries/**', text)
        self.assertIn('python -m coordination_fabric validate', text)
        self.assertIn('python -m coordination_fabric compile', text)
        self.assertIn('python -m coordination_fabric prune', text)
        self.assertIn('coordination/ACTIVE.md', text)
        self.assertIn('coordination/index.json', text)
        self.assertIn('coordination/collisions.json', text)
        self.assertIn('git push', text)

    def test_generated_files_do_not_retrigger_the_push_filter(self):
        workflow = Path('.github/workflows/coordination-maintenance.yml')
        self.assertTrue(workflow.exists(), 'coordination maintenance workflow is missing')
        text = workflow.read_text(encoding='utf-8')
        push_section = text.split('workflow_dispatch:', 1)[0]
        self.assertNotIn("- 'coordination/ACTIVE.md'", push_section)
        self.assertNotIn("- 'coordination/index.json'", push_section)
        self.assertNotIn("- 'coordination/collisions.json'", push_section)


if __name__ == '__main__':
    unittest.main()
