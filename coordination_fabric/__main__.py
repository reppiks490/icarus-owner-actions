from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import compile_state, prune_terminal_events, render_active, validate_tree


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    tmp.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser(description="ICARUS multi-chat coordination compiler")
    parser.add_argument("--root", type=Path, default=Path("."))
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    sub.add_parser("compile")
    prune = sub.add_parser("prune")
    prune.add_argument("--days", type=int, default=14)
    args = parser.parse_args()

    if args.command == "validate":
        tree = validate_tree(args.root)
        print(json.dumps({
            "sessions": len(tree["sessions"]),
            "events": len(tree["events"]),
            "summaries": len(tree["summaries"]),
            "valid": True,
        }, sort_keys=True))
        return 0

    if args.command == "compile":
        state = compile_state(args.root)
        base = args.root / "coordination"
        _write(base / "index.json", json.dumps(state, indent=2, sort_keys=True) + "\n")
        _write(base / "collisions.json", json.dumps({
            "schema_version": "icarus-coordination-collisions-v2",
            "generated_at_utc": state["generated_at_utc"],
            "collisions": state["collisions"],
        }, indent=2, sort_keys=True) + "\n")
        _write(base / "ACTIVE.md", render_active(state))
        print(json.dumps(state["counts"], sort_keys=True))
        return 0

    removed = prune_terminal_events(args.root, days=args.days)
    print(json.dumps({"removed": removed, "count": len(removed)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
