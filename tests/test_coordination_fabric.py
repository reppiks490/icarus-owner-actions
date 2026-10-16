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
