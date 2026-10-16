from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile
import unittest

from coordination_fabric import compile_state, validate_tree


def write(root: Path, rel: str, value: dict) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value) + "\n", encoding="utf-8")


def session(root: Path, sid: str) -> None:
    write(root, f"coordination/sessions/{sid}.json", {
        "schema_version": "icarus-coordination-session-v2",
        "session_id": sid,
        "actor": "ChatGPT",
        "model_family": "openai",
        "goal": "cross repo work",
        "home_repo": "reppiks490/Icarus-engine",
        "branch": f"chatgpt/{sid}",
        "pr": None,
        "started_at_utc": "2026-10-16T02:00:00Z",
        "stale_after_minutes": 120,
        "capabilities": ["github"],
        "initial_dependencies": [],
    })


def event(root: Path, sid: str, sec: int, targets: list[dict[str, str]]) -> None:
    eid = f"20261016T0210{sec:02d}Z-claim-{sid}"
    write(root, f"coordination/events/2026/10/16/{sid}/{eid}.json", {
        "schema_version": "icarus-coordination-event-v2",
        "event_id": eid,
        "session_id": sid,
        "at_utc": f"2026-10-16T02:10:{sec:02d}Z",
        "type": "CLAIM",
        "phase": "coding",
        "summary": "qualified reservation",
        "repos": sorted({target["repo"] for target in targets}),
        "paths": [],
        "targets": targets,
        "dependencies": [],
        "evidence": [],
        "next_action": "code",
        "coordination_mode": "independent",
        "cooperates_with": [],
    })


class MultiRepoReservationTests(unittest.TestCase):
    def test_same_path_in_different_repositories_does_not_collide(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            session(root, "a")
            session(root, "b")
            event(root, "a", 1, [{"repo": "reppiks490/Icarus-engine", "path": "AGENTS.md"}])
            event(root, "b", 2, [{"repo": "reppiks490/Icarus", "path": "AGENTS.md"}])
            state = compile_state(root, now=datetime(2026, 10, 16, 2, 20, tzinfo=timezone.utc))
            self.assertEqual(state["collisions"], [])
            self.assertEqual(state["active_sessions"][0]["reserved_targets"][0]["repo"], "reppiks490/Icarus-engine")

    def test_same_repository_ancestor_paths_still_collide(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            session(root, "a")
            session(root, "b")
            event(root, "a", 1, [{"repo": "reppiks490/Icarus-engine", "path": "icarus_engine"}])
            event(root, "b", 2, [{"repo": "reppiks490/Icarus-engine", "path": "icarus_engine/assets.py"}])
            state = compile_state(root, now=datetime(2026, 10, 16, 2, 20, tzinfo=timezone.utc))
            self.assertEqual(len(state["collisions"]), 1)
            self.assertEqual(state["collisions"][0]["repo"], "reppiks490/Icarus-engine")

    def test_multi_repo_event_with_unqualified_paths_is_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            session(root, "a")
            eid = "20261016T021001Z-claim-a"
            write(root, f"coordination/events/2026/10/16/a/{eid}.json", {
                "schema_version": "icarus-coordination-event-v2", "event_id": eid, "session_id": "a",
                "at_utc": "2026-10-16T02:10:01Z", "type": "CLAIM", "phase": "coding", "summary": "ambiguous",
                "repos": ["reppiks490/Icarus-engine", "reppiks490/Icarus"], "paths": ["AGENTS.md"],
                "dependencies": [], "evidence": [], "next_action": "code", "coordination_mode": "independent",
                "cooperates_with": []
            })
            with self.assertRaises(ValueError):
                validate_tree(root)


if __name__ == "__main__":
    unittest.main()
