"""Keep malformed historical receipts immutable and corrections explicitly scoped."""
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import unittest

from coordination_fabric import compile_state, validate_tree

ROOT = Path(__file__).resolve().parents[1]
REPAIR_SESSION = 'codex-20261025-federation-record-repair'
RECORDS = [{'original_path': 'coordination/events/2026/10/25/codex-20261025-icarus-licensing/20261025T164210Z-complete-licensing.json', 'archive_path': 'coordination/archive/invalid-events/codex-20261025-icarus-licensing/20261025T164210Z-complete-licensing.json', 'sha256': '0c6c39160d209dd2e29da7e90b72906dbee4b3906140486b366450a3d0d1042c', 'correction_path': 'coordination/events/2026/10/25/codex-20261025-federation-record-repair/20261025T231616Z-correction-1.json'}, {'original_path': 'coordination/events/2026/10/25/codex-20261025-icarus-licensing/20261025T165640Z-complete-neutral-landings.json', 'archive_path': 'coordination/archive/invalid-events/codex-20261025-icarus-licensing/20261025T165640Z-complete-neutral-landings.json', 'sha256': '633d85714ad177e3cf70afbb9ce8da20d44d5d0e14e70370ae72d0fd2767e6fa', 'correction_path': 'coordination/events/2026/10/25/codex-20261025-federation-record-repair/20261025T231616Z-correction-2.json'}]
SUMMARY = {
    'original_path': 'coordination/summaries/codex-20261025-icarus-licensing.json',
    'archive_path': 'coordination/archive/invalid-summaries/codex-20261025-icarus-licensing.json',
    'sha256': 'a66073d4848258c4b2baa227fe4beb8b69d5d0739142932fd6f1e6e66d8fb734',
}


class ArchivedCorrectionTests(unittest.TestCase):
    def test_actual_record_tree_validates_without_relaxing_multi_repo_paths(self):
        tree = validate_tree(ROOT)
        self.assertIn(REPAIR_SESSION, tree["sessions"])

    def test_original_receipts_keep_exact_bytes_outside_active_event_scan(self):
        for record in RECORDS:
            with self.subTest(original=record["original_path"]):
                self.assertFalse((ROOT / record["original_path"]).exists())
                archived = ROOT / record["archive_path"]
                self.assertTrue(archived.is_file(), "immutable original must be archived")
                self.assertEqual(hashlib.sha256(archived.read_bytes()).hexdigest(), record["sha256"])

    def test_malformed_summary_is_archived_and_schema_fields_are_corrected_from_history(self):
        archived = ROOT / SUMMARY["archive_path"]
        self.assertTrue(archived.is_file())
        self.assertEqual(hashlib.sha256(archived.read_bytes()).hexdigest(), SUMMARY["sha256"])
        original = json.loads(archived.read_text(encoding="utf-8"))
        active = json.loads((ROOT / SUMMARY["original_path"]).read_text(encoding="utf-8"))
        self.assertEqual(original["status"], "COMPLETE")
        self.assertEqual(active["result"], "complete")
        self.assertEqual(active["completed_at_utc"], original["at_utc"])
        self.assertNotIn("status", active)
        self.assertNotIn("at_utc", active)
        self.assertTrue(any(SUMMARY["sha256"] in item for item in active["evidence"]))

    def test_corrections_bind_original_hash_identity_and_only_documented_targets(self):
        state = compile_state(ROOT, now=datetime.now(timezone.utc))
        repair = next(row for row in state["terminal_sessions"] if row["session_id"] == REPAIR_SESSION)
        self.assertEqual(repair["reserved_targets"], [])
        for index, record in enumerate(RECORDS):
            with self.subTest(original=record["original_path"]):
                original = json.loads((ROOT / record["archive_path"]).read_text(encoding="utf-8"))
                correction = json.loads((ROOT / record["correction_path"]).read_text(encoding="utf-8"))
                self.assertEqual(correction["session_id"], REPAIR_SESSION)
                self.assertNotEqual(correction["session_id"], original["session_id"])
                self.assertNotEqual(correction["event_id"], original["event_id"])
                self.assertGreater(correction["at_utc"], original["at_utc"])
                self.assertEqual(correction["paths"], [])
                expected = {(repo, path) for repo in original["repos"] for path in ("README.md", "LICENSE.md")}
                if index == 1:
                    expected.add(("reppiks490/aion-parallax-research", "docs/CURRENT.md"))
                targets = [(row["repo"], row["path"]) for row in correction["targets"]]
                self.assertEqual(set(targets), expected)
                self.assertEqual(len(targets), len(expected))
                provenance = correction["correction"]
                for key in ("original_path", "archive_path", "sha256"):
                    self.assertEqual(provenance[key], record[key])
                self.assertEqual(provenance["original_session_id"], original["session_id"])
                self.assertEqual(provenance["original_event_id"], original["event_id"])
                self.assertEqual(provenance["original_summary"], original["summary"])
                self.assertIs(provenance["historical_verification_only"], True)
                self.assertEqual(correction["evidence"][:len(original["evidence"])], original["evidence"])
                self.assertIn(record["sha256"], " ".join(correction["evidence"]))


if __name__ == "__main__":
    unittest.main()
