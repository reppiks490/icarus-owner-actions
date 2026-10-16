from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import tempfile
import unittest


def _write(root: Path, rel: str, value: dict) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")


def _session(root: Path, sid: str, repo: str) -> None:
    _write(root, f"coordination/sessions/{sid}.json", {
        "schema_version": "icarus-coordination-session-v2",
        "session_id": sid,
        "actor": "ChatGPT",
        "model_family": "openai",
        "goal": "cross-repo work",
        "home_repo": repo,
        "branch": f"chatgpt/{sid}",
        "pr": None,
        "started_at_utc": "2026-10-16T02:00:00Z",
        "stale_after_minutes": 180,
        "capabilities": ["github"],
        "initial_dependencies": [],
    })


def _event(root: Path, sid: str, *, targets: list[dict[str, str]], stamp: str) -> None:
    event_id = stamp.replace(":", "").replace("-", "") + "-claim-" + sid
    _write(root, f"coordination/events/2026/10/16/{sid}/{event_id}.json", {
        "schema_version": "icarus-coordination-event-v2",
        "event_id": event_id,
        "session_id": sid,
        "at_utc": stamp,
        "type": "CLAIM",
        "phase": "coding",
        "summary": "reserve repo-qualified targets",
        "repos": sorted({target["repo"] for target in targets}),
        "paths": [],
        "targets": targets,
        "dependencies": [],
        "evidence": [],
        "next_action": "continue",
        "coordination_mode": "independent",
        "cooperates_with": [],
    })


class RepoQualifiedTargetTests(unittest.TestCase):
    def test_same_path_in_different_repos_does_not_collide(self):
        from coordination_fabric import compile_state
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _session(root, "a", "reppiks490/Icarus")
            _session(root, "b", "reppiks490/Icarus-engine")
            _event(root, "a", targets=[{"repo": "reppiks490/Icarus", "path": "AGENTS.md"}], stamp="2026-10-16T02:10:00Z")
            _event(root, "b", targets=[{"repo": "reppiks490/Icarus-engine", "path": "AGENTS.md"}], stamp="2026-10-16T02:11:00Z")
            state = compile_state(root, now=datetime(2026, 10, 16, 2, 20, tzinfo=timezone.utc))
            self.assertEqual(state["collisions"], [])
            self.assertEqual(state["counts"]["active"], 2)

    def test_same_repo_ancestor_target_collides_and_reports_repo(self):
        from coordination_fabric import compile_state
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _session(root, "a", "reppiks490/Icarus-engine")
            _session(root, "b", "reppiks490/Icarus-engine")
            _event(root, "a", targets=[{"repo": "reppiks490/Icarus-engine", "path": "icarus_engine/assets.py"}], stamp="2026-10-16T02:10:00Z")
            _event(root, "b", targets=[{"repo": "reppiks490/Icarus-engine", "path": "icarus_engine"}], stamp="2026-10-16T02:11:00Z")
            state = compile_state(root, now=datetime(2026, 10, 16, 2, 20, tzinfo=timezone.utc))
            self.assertEqual(len(state["collisions"]), 1)
            collision = state["collisions"][0]
            self.assertEqual(collision["repo"], "reppiks490/Icarus-engine")
            # Preserve the v2 path_pairs key while repo qualifies the lock domain.
            self.assertEqual(collision["path_pairs"], [["icarus_engine/assets.py", "icarus_engine"]])

    def test_cross_repo_event_reserves_every_declared_target(self):
        from coordination_fabric import compile_state, render_active
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _session(root, "a", "reppiks490/icarus-owner-actions")
            _event(root, "a", targets=[
                {"repo": "reppiks490/Icarus", "path": "AGENTS.md"},
                {"repo": "reppiks490/Icarus-engine", "path": "coordination/README.md"},
            ], stamp="2026-10-16T02:10:00Z")
            state = compile_state(root, now=datetime(2026, 10, 16, 2, 20, tzinfo=timezone.utc))
            row = state["active_sessions"][0]
            self.assertEqual(row["reserved_targets"], [
                {"repo": "reppiks490/Icarus", "path": "AGENTS.md"},
                {"repo": "reppiks490/Icarus-engine", "path": "coordination/README.md"},
            ])
            rendered = render_active(state)
            self.assertIn("reppiks490/Icarus:AGENTS.md", rendered)
            self.assertIn("reppiks490/Icarus-engine:coordination/README.md", rendered)


if __name__ == "__main__":
    unittest.main()
