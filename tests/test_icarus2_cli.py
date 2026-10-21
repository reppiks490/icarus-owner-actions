"""Runtime boundaries: inspection never gains release or trading authority."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class Icarus2CommandTests(unittest.TestCase):
    def test_help_is_available_without_network_or_credentials(self):
        result = subprocess.run([sys.executable, '-m', 'integration_brain', '--help'],
            cwd=ROOT, capture_output=True, text=True, timeout=10)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('--snapshot', result.stdout)
        self.assertIn('--collect', result.stdout)

    def test_malformed_snapshot_never_publishes_a_cycle(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp)/'bad.json', Path(tmp)/'cycle'
            source.write_text('{"schema_version":"unsafe", "execution_authorized":true}')
            result = subprocess.run([sys.executable, '-m', 'integration_brain', '--snapshot', str(source),
                '--output-dir', str(output)], cwd=ROOT, capture_output=True, text=True, timeout=10)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((output/'cycle.json').exists())
            self.assertNotIn('unsafe', result.stdout)

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            source, output = Path(tmp)/'snapshot.json', Path(tmp)/'cycle'
            source.write_text('{}')
            output.mkdir()
            previous = output/'cycle.json'
            previous.write_text('existing immutable evidence')
            subprocess.run([sys.executable, '-m', 'integration_brain', '--snapshot', str(source),
                '--output-dir', str(output)], cwd=ROOT, capture_output=True, text=True, timeout=10)
            self.assertEqual(previous.read_text(), 'existing immutable evidence')



if __name__ == '__main__':
    unittest.main()
