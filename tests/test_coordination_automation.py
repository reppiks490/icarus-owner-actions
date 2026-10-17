from pathlib import Path
import re
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

    def test_contract_workflow_accepts_and_publishes_visible_collision_diagnostics(self):
        workflow = Path('.github/workflows/coordination-fabric.yml')
        text = workflow.read_text(encoding='utf-8')
        self.assertIn('Validate collision diagnostics are present', text)
        self.assertIn("assert isinstance(d.get('collisions'), list)", text)
        self.assertNotIn("assert not d['collisions']", text)

    def test_generated_files_do_not_retrigger_the_push_filter(self):
        workflow = Path('.github/workflows/coordination-maintenance.yml')
        self.assertTrue(workflow.exists(), 'coordination maintenance workflow is missing')
        text = workflow.read_text(encoding='utf-8')
        push_section = text.split('workflow_dispatch:', 1)[0]
        self.assertNotIn("- 'coordination/ACTIVE.md'", push_section)
        self.assertNotIn("- 'coordination/index.json'", push_section)
        self.assertNotIn("- 'coordination/collisions.json'", push_section)

    def test_schedule_fallback_recompiles_within_five_minutes_off_hour_boundary(self):
        workflow = Path('.github/workflows/coordination-maintenance.yml')
        self.assertTrue(workflow.exists(), 'coordination maintenance workflow is missing')
        text = workflow.read_text(encoding='utf-8')
        cron_values = re.findall(r"cron:\s*['\"]([^'\"]+)['\"]", text)
        self.assertTrue(cron_values, 'coordination maintenance needs a schedule fallback')
        five_minute = [value for value in cron_values if '/5' in value.split()[0]]
        self.assertTrue(five_minute, f'expected five-minute fallback schedule, got {cron_values!r}')
        minute_field = five_minute[0].split()[0]
        self.assertNotEqual(minute_field, '*/5', 'avoid top-of-hour/high-load minute zero')
        self.assertRegex(minute_field, r'^[1-9][0-9]?-[0-9]+/5$')


if __name__ == '__main__':
    unittest.main()
