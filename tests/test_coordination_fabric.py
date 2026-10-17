from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import tempfile
import unittest


MODULE = Path("coordination_fabric/__init__.py")


def _write(root: Path, rel: str, value: dict) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")


def _session(root: Path, sid: str, *, goal: str = "work", stale: int = 45) -> None:
    _write(root, f"coordination/sessions/{sid}.json", {
        "schema_version": "icarus-coordination-session-v2",
        "session_id": sid,
        "actor": "ChatGPT",
        "model_family": "openai",
        "goal": goal,
        "home_repo": "reppiks490/Icarus-engine",
        "branch": f"chatgpt/{sid}",
        "pr": None,
        "started_at_utc": "2026-10-16T02:00:00Z",
        "stale_after_minutes": stale,
        "capabilities": ["github"],
        "initial_dependencies": [],
    })


def _event(root: Path, sid: str, stamp: str, kind: str, *, paths=None, phase="coding",
           mode="independent", cooperates=None, summary=None, deps=None, evidence=None) -> None:
    event_id = stamp.replace(":", "").replace("-", "") + "-" + kind.lower()
    _write(root, f"coordination/events/2026/10/16/{sid}/{event_id}.json", {
        "schema_version": "icarus-coordination-event-v2",
        "event_id": event_id,
        "session_id": sid,
        "at_utc": stamp,
        "type": kind,
        "phase": phase,
        "summary": summary or kind,
        "repos": ["reppiks490/Icarus-engine"],
        "paths": paths or [],
        "dependencies": deps or [],
        "evidence": evidence or [],
        "next_action": "continue",
        "coordination_mode": mode,
        "cooperates_with": cooperates or [],
    })


class CoordinationFabricContractTests(unittest.TestCase):
    def _api(self):
        self.assertTrue(MODULE.exists(), "coordination_fabric implementation is missing")
        from coordination_fabric import compile_state, prune_terminal_events, render_active, validate_tree
        return compile_state, prune_terminal_events, render_active, validate_tree

    def test_compiles_latest_state_and_waiting_note_deterministically(self):
        compile_state, _, render_active, _ = self._api()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _session(root, "chat-a")
            _event(root, "chat-a", "2026-10-16T02:10:00Z", "PLAN", paths=["icarus_engine/assets.py"], phase="planning")
            _event(root, "chat-a", "2026-10-16T02:20:00Z", "WAITING", paths=["icarus_engine/assets.py"], phase="waiting", summary="waiting on CI", deps=["github-run:123"])
            now = datetime(2026, 10, 16, 2, 30, tzinfo=timezone.utc)
            first = compile_state(root, now=now)
            second = compile_state(root, now=now)
            self.assertEqual(first, second)
            self.assertEqual(first["active_sessions"][0]["phase"], "waiting")
            self.assertEqual(first["active_sessions"][0]["latest_summary"], "waiting on CI")
            self.assertIn("github-run:123", first["active_sessions"][0]["dependencies"])
            self.assertIn("waiting on CI", render_active(first))

    def test_detects_exact_and_ancestor_path_collisions(self):
        compile_state, _, _, _ = self._api()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _session(root, "chat-a")
            _session(root, "chat-b")
            _event(root, "chat-a", "2026-10-16T02:10:00Z", "CLAIM", paths=["icarus_engine/assets.py"])
            _event(root, "chat-b", "2026-10-16T02:11:00Z", "CLAIM", paths=["icarus_engine"])
            state = compile_state(root, now=datetime(2026, 10, 16, 2, 20, tzinfo=timezone.utc))
            self.assertEqual(len(state["collisions"]), 1)
            self.assertEqual(set(state["collisions"][0]["sessions"]), {"chat-a", "chat-b"})

    def test_explicit_mutual_cooperation_allows_overlap(self):
        compile_state, _, _, _ = self._api()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _session(root, "chat-a")
            _session(root, "chat-b")
            _event(root, "chat-a", "2026-10-16T02:10:00Z", "CLAIM", paths=["icarus_engine/assets.py"], mode="cooperate", cooperates=["chat-b"])
            _event(root, "chat-b", "2026-10-16T02:11:00Z", "CLAIM", paths=["icarus_engine/assets.py"], mode="cooperate", cooperates=["chat-a"])
            state = compile_state(root, now=datetime(2026, 10, 16, 2, 20, tzinfo=timezone.utc))
            self.assertEqual(state["collisions"], [])

    def test_cooperative_alias_in_immutable_bus_record_compiles_canonically(self):
        compile_state, _, _, validate_tree = self._api()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _session(root, "chat-a")
            _event(root, "chat-a", "2026-10-16T02:10:00Z", "NOTE",
                   mode="cooperative", cooperates=["chat-b"])
            tree = validate_tree(root)
            self.assertEqual(tree["events"][0][1]["coordination_mode"], "cooperate")
            state = compile_state(root, now=datetime(2026, 10, 16, 2, 20, tzinfo=timezone.utc))
            self.assertEqual(state["active_sessions"][0]["coordination_mode"], "cooperate")

    def test_legacy_cross_repo_paths_with_qualified_targets_use_target_authority(self):
        _, _, _, validate_tree = self._api()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _session(root, "chat-a")
            event = {
                "schema_version": "icarus-coordination-event-v2", "event_id": "legacy-cross-repo",
                "session_id": "chat-a", "at_utc": "2026-10-16T02:10:00Z", "type": "NOTE",
                "phase": "repair", "summary": "legacy cross-repo shape", "repos": [
                    "reppiks490/Icarus-engine", "reppiks490/icarus-owner-actions"],
                "paths": ["legacy/path"], "targets": [
                    {"repo": "reppiks490/Icarus-engine", "path": "engine/path"}],
            }
            _write(root, "coordination/events/2026/10/16/chat-a/legacy.json", event)
            tree = validate_tree(root)
            self.assertEqual(tree["events"][0][1]["targets"], [
                {"repo": "reppiks490/Icarus-engine", "path": "engine/path"}])

    def test_immutable_event_type_and_timestamp_aliases_compile_with_targets(self):
        compile_state, _, _, validate_tree = self._api()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _session(root, "chat-a")
            event = {
                "schema_version": "icarus-coordination-event-v2",
                "event_id": "immutable-legacy-claim", "session_id": "chat-a",
                "event_type": "CLAIM", "created_at_utc": "2026-10-16T02:10:00Z",
                "summary": "legacy event aliases", "targets": [
                    {"repo": "reppiks490/Icarus-engine", "path": "coordination_fabric/__init__.py"},
                    {"repo": "reppiks490/icarus-owner-actions", "path": "tests/test_coordination_fabric.py"},
                ], "collaborators": ["chat-b"],
            }
            _write(root, "coordination/events/2026/10/16/chat-a/legacy-claim.json", event)
            validated = validate_tree(root)["events"][0][1]
            self.assertEqual(validated["type"], "CLAIM")
            self.assertEqual(validated["at_utc"], "2026-10-16T02:10:00Z")
            self.assertEqual(validated["phase"], "legacy")
            self.assertEqual(validated["repos"], ["reppiks490/Icarus-engine", "reppiks490/icarus-owner-actions"])
            self.assertEqual(validated["cooperates_with"], ["chat-b"])
            state = compile_state(root, now=datetime(2026, 10, 16, 2, 20, tzinfo=timezone.utc))
            self.assertEqual(len(state["active_sessions"]), 1)
            self.assertEqual(len(state["active_sessions"][0]["reserved_targets"]), 2)

    def test_legacy_event_rejects_conflicting_canonical_alias(self):
        _, _, _, validate_tree = self._api()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _session(root, "chat-a")
            event = {
                "schema_version": "icarus-coordination-event-v2",
                "event_id": "conflicting-legacy-alias", "session_id": "chat-a",
                "type": "NOTE", "event_type": "CLAIM",
                "at_utc": "2026-10-16T02:10:00Z", "created_at_utc": "2026-10-16T02:11:00Z",
                "phase": "legacy", "summary": "must reject ambiguity",
            }
            _write(root, "coordination/events/2026/10/16/chat-a/conflict.json", event)
            with self.assertRaisesRegex(ValueError, "conflicting event fields"):
                validate_tree(root)

    def test_immutable_legacy_string_targets_and_status_get_canonicalized(self):
        _, _, _, validate_tree = self._api()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _session(root, "chat-a")
            event = {
                "schema_version": "icarus-coordination-event-v2", "event_id": "old-string-targets",
                "session_id": "chat-a", "type": "UPDATE", "at_utc": "2026-10-16T02:10:00Z",
                "status": "superseded", "summary": "old immutable string targets",
                "repos": ["reppiks490/Icarus", "reppiks490/icarus-owner-actions"],
                "targets": ["tests_engine/browser_depth.cjs", "coordination/summaries/chat-a.json"],
            }
            _write(root, "coordination/events/2026/10/16/chat-a/old.json", event)
            _write(root, "coordination/summaries/chat-a.json", {
                "schema_version": "icarus-coordination-summary-v2", "session_id": "chat-a",
                "status": "superseded", "finished_at_utc": "2026-10-16T02:11:00Z",
                "summary": "legacy superseded summary",
            })
            normalized = validate_tree(root)["events"][0][1]
            self.assertEqual(normalized["phase"], "legacy")
            self.assertEqual(normalized["targets"], [
                {"repo": "reppiks490/Icarus", "path": "tests_engine/browser_depth.cjs"},
                {"repo": "reppiks490/icarus-owner-actions", "path": "coordination/summaries/chat-a.json"}])
            validated_summary = validate_tree(root)["summaries"]["chat-a"]
            self.assertEqual(validated_summary["completed_at_utc"], "2026-10-16T02:11:00Z")
            self.assertEqual(validated_summary["result"], "cancelled")

    def test_legacy_summary_rejects_conflicting_canonical_fields(self):
        _, _, _, validate_tree = self._api()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _session(root, "chat-a")
            _write(root, "coordination/summaries/chat-a.json", {
                "schema_version": "icarus-coordination-summary-v2", "session_id": "chat-a",
                "status": "superseded", "result": "complete",
                "finished_at_utc": "2026-10-16T02:11:00Z", "completed_at_utc": "2026-10-16T02:12:00Z",
            })
            with self.assertRaisesRegex(ValueError, "conflicting summary fields"):
                validate_tree(root)

    def test_orphaned_events_require_a_terminal_complete_receipt(self):
        compile_state, _, _, validate_tree = self._api()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _event(root, "missing-session", "2026-10-16T02:10:00Z", "CLAIM")
            with self.assertRaisesRegex(ValueError, "unknown session"):
                validate_tree(root)
            _event(root, "missing-session", "2026-10-16T02:20:00Z", "COMPLETE")
            tree = validate_tree(root)
            self.assertEqual(len(tree["events"]), 2)
            state = compile_state(root, now=datetime(2026, 10, 16, 2, 30, tzinfo=timezone.utc))
            self.assertEqual(state["terminal_sessions"][0]["session_id"], "missing-session")

    def test_stale_session_is_reclaimable_not_complete(self):
        compile_state, _, _, _ = self._api()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _session(root, "chat-a", stale=30)
            _event(root, "chat-a", "2026-10-16T01:00:00Z", "UPDATE", paths=["foo/bar.py"])
            state = compile_state(root, now=datetime(2026, 10, 16, 2, 0, tzinfo=timezone.utc))
            self.assertTrue(state["active_sessions"][0]["stale"])
            self.assertTrue(state["active_sessions"][0]["reclaimable"])
            self.assertNotEqual(state["active_sessions"][0]["status"], "complete")

    def test_owner_status_can_mark_claude_inactive_without_return_date(self):
        compile_state, _, _, _ = self._api()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _write(root, "coordination/owner_status.json", {
                "schema_version": "icarus-coordination-owner-status-v1",
                "updated_at_utc": "2026-10-16T02:00:00Z",
                "claude": {"active": False, "return_date": None, "note": "inactive per owner; unfinished work is reclaimable"},
                "live_broker_arming": False,
            })
            state = compile_state(root, now=datetime(2026, 10, 16, 2, 0, tzinfo=timezone.utc))
            self.assertFalse(state["owner_status"]["claude"]["active"])
            self.assertIsNone(state["owner_status"]["claude"]["return_date"])
            self.assertFalse(state["owner_status"]["live_broker_arming"])

    def test_validation_rejects_unsafe_paths_and_unknown_event_types(self):
        _, _, _, validate_tree = self._api()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _session(root, "chat-a")
            _event(root, "chat-a", "2026-10-16T02:10:00Z", "CLAIM", paths=["../secret"])
            with self.assertRaises(ValueError):
                validate_tree(root)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _session(root, "chat-a")
            _event(root, "chat-a", "2026-10-16T02:10:00Z", "MYSTERY")
            with self.assertRaises(ValueError):
                validate_tree(root)

    def test_prune_requires_terminal_summary_and_never_prunes_active(self):
        _, prune_terminal_events, _, _ = self._api()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _session(root, "done")
            _session(root, "active")
            _event(root, "done", "2026-09-01T02:00:00Z", "COMPLETE", phase="complete", evidence=["run:1"])
            _event(root, "active", "2026-09-01T02:00:00Z", "UPDATE")
            cutoff = datetime(2026, 10, 16, tzinfo=timezone.utc)
            self.assertEqual(prune_terminal_events(root, now=cutoff, days=14), [])
            _write(root, "coordination/summaries/done.json", {
                "schema_version": "icarus-coordination-summary-v2", "session_id": "done",
                "completed_at_utc": "2026-09-01T02:00:00Z", "result": "complete", "evidence": ["run:1"]
            })
            removed = prune_terminal_events(root, now=cutoff, days=14)
            self.assertTrue(removed)
            self.assertFalse(any((root / p).exists() for p in removed))
            self.assertTrue(any((root / "coordination/events").glob("**/active/*.json")))

    def test_scales_to_64_parallel_chats_with_precise_collision_accounting(self):
        compile_state, _, _, _ = self._api()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for i in range(64):
                sid = f"chat-{i:02d}"
                _session(root, sid, stale=180)
                # 62 chats reserve unique narrow files. Chat-62 reserves their
                # common parent; chat-63 reserves a sibling of chat-00's file.
                if i == 62:
                    path = "workstreams/00"
                elif i == 63:
                    path = "workstreams/00/shared.py"
                else:
                    path = f"workstreams/{i:02d}/task.py"
                _event(
                    root,
                    sid,
                    f"2026-10-16T02:{i % 60:02d}:00Z",
                    "CLAIM",
                    paths=[path],
                    summary=f"chat {i} active",
                )
            now = datetime(2026, 10, 16, 3, 0, tzinfo=timezone.utc)
            state = compile_state(root, now=now)
            self.assertEqual(state["counts"]["active"], 64)
            self.assertEqual(state["counts"]["stale"], 0)
            pairs = {tuple(sorted(item["sessions"])) for item in state["collisions"]}
            self.assertEqual(
                pairs,
                {
                    ("chat-00", "chat-62"),
                    ("chat-62", "chat-63"),
                },
            )
            # Compilation must remain deterministic at this scale.
            self.assertEqual(state, compile_state(root, now=now))


if __name__ == "__main__":
    unittest.main()
