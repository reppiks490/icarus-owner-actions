"""Deterministic, file-backed coordination fabric for ICARUS agent sessions.

The fabric is intentionally stdlib-only and treats coordination records as data.
It never imports or executes code referenced by records.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any


SESSION_SCHEMA = "icarus-coordination-session-v2"
EVENT_SCHEMA = "icarus-coordination-event-v2"
SUMMARY_SCHEMA = "icarus-coordination-summary-v2"
OWNER_SCHEMA = "icarus-coordination-owner-status-v1"
EVENT_TYPES = {
    "START", "PLAN", "CLAIM", "HEARTBEAT", "WAITING", "UPDATE", "BLOCKED",
    "HANDOFF", "RELEASE", "COMPLETE", "CANCELLED",
}
TERMINAL_TYPES = {"COMPLETE", "CANCELLED"}
SESSION_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]{0,127}\Z")


def _load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid JSON record: {path}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"record must be an object: {path}")
    return value


def _stamp(value: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise ValueError("timestamp must be a non-empty ISO-8601 string")
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"invalid timestamp: {value}") from exc
    if dt.tzinfo is None:
        raise ValueError(f"timestamp must include timezone: {value}")
    return dt.astimezone(timezone.utc)


def _safe_session_id(value: Any) -> str:
    if not isinstance(value, str) or not SESSION_ID_RE.fullmatch(value):
        raise ValueError(f"unsafe session_id: {value!r}")
    return value


def _safe_path(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("coordination path must be a non-empty string")
    raw = value.strip().replace("\\", "/")
    p = PurePosixPath(raw)
    if p.is_absolute() or ".." in p.parts or raw.startswith("~") or ":" in p.parts[0]:
        raise ValueError(f"unsafe coordination path: {value!r}")
    if any(part in {"", "."} for part in p.parts):
        raise ValueError(f"unsafe coordination path: {value!r}")
    return str(p)


def _string_list(value: Any, field: str) -> list[str]:
    if value is None:
        return []
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ValueError(f"{field} must be a list of strings")
    return list(value)


def _validate_session(doc: dict[str, Any], path: Path) -> dict[str, Any]:
    if doc.get("schema_version") != SESSION_SCHEMA:
        raise ValueError(f"unsupported session schema: {path}")
    sid = _safe_session_id(doc.get("session_id"))
    if path.stem != sid:
        raise ValueError(f"session filename/id mismatch: {path}")
    _stamp(doc.get("started_at_utc"))
    stale = doc.get("stale_after_minutes")
    if not isinstance(stale, int) or stale < 1 or stale > 10080:
        raise ValueError(f"invalid stale_after_minutes: {path}")
    for key in ("actor", "model_family", "goal", "home_repo", "branch"):
        if not isinstance(doc.get(key), str) or not doc[key].strip():
            raise ValueError(f"session {key} must be non-empty: {path}")
    _string_list(doc.get("capabilities", []), "capabilities")
    _string_list(doc.get("initial_dependencies", []), "initial_dependencies")
    return doc


def _validate_event(doc: dict[str, Any], path: Path, sessions: set[str]) -> dict[str, Any]:
    if doc.get("schema_version") != EVENT_SCHEMA:
        raise ValueError(f"unsupported event schema: {path}")
    sid = _safe_session_id(doc.get("session_id"))
    if sid not in sessions:
        raise ValueError(f"event references unknown session {sid}: {path}")
    kind = doc.get("type")
    if kind not in EVENT_TYPES:
        raise ValueError(f"unknown event type {kind!r}: {path}")
    _stamp(doc.get("at_utc"))
    if not isinstance(doc.get("event_id"), str) or not doc["event_id"].strip():
        raise ValueError(f"missing event_id: {path}")
    if not isinstance(doc.get("phase"), str) or not doc["phase"].strip():
        raise ValueError(f"missing phase: {path}")
    if not isinstance(doc.get("summary"), str) or not doc["summary"].strip():
        raise ValueError(f"missing summary: {path}")
    for key in ("repos", "dependencies", "evidence", "cooperates_with"):
        _string_list(doc.get(key, []), key)
    paths = doc.get("paths", [])
    if not isinstance(paths, list):
        raise ValueError(f"paths must be a list: {path}")
    doc["paths"] = [_safe_path(item) for item in paths]
    mode = doc.get("coordination_mode", "independent")
    if mode not in {"independent", "cooperate"}:
        raise ValueError(f"invalid coordination_mode: {path}")
    return doc


def _validate_summary(doc: dict[str, Any], path: Path, sessions: set[str]) -> dict[str, Any]:
    if doc.get("schema_version") != SUMMARY_SCHEMA:
        raise ValueError(f"unsupported summary schema: {path}")
    sid = _safe_session_id(doc.get("session_id"))
    if sid not in sessions or path.stem != sid:
        raise ValueError(f"invalid summary session: {path}")
    _stamp(doc.get("completed_at_utc"))
    if doc.get("result") not in {"complete", "cancelled", "blocked"}:
        raise ValueError(f"invalid summary result: {path}")
    _string_list(doc.get("evidence", []), "evidence")
    return doc


def validate_tree(root: Path | str) -> dict[str, Any]:
    root = Path(root)
    sessions_dir = root / "coordination" / "sessions"
    events_dir = root / "coordination" / "events"
    summaries_dir = root / "coordination" / "summaries"

    sessions: dict[str, dict[str, Any]] = {}
    for path in sorted(sessions_dir.glob("*.json")) if sessions_dir.exists() else []:
        doc = _validate_session(_load(path), path)
        sid = doc["session_id"]
        if sid in sessions:
            raise ValueError(f"duplicate session: {sid}")
        sessions[sid] = doc

    events: list[tuple[Path, dict[str, Any]]] = []
    seen_events: set[str] = set()
    if events_dir.exists():
        for path in sorted(events_dir.glob("**/*.json")):
            doc = _validate_event(_load(path), path, set(sessions))
            event_id = doc["event_id"]
            if event_id in seen_events:
                raise ValueError(f"duplicate event_id: {event_id}")
            seen_events.add(event_id)
            events.append((path, doc))

    summaries: dict[str, dict[str, Any]] = {}
    for path in sorted(summaries_dir.glob("*.json")) if summaries_dir.exists() else []:
        doc = _validate_summary(_load(path), path, set(sessions))
        summaries[doc["session_id"]] = doc

    owner_status: dict[str, Any] = {}
    owner_path = root / "coordination" / "owner_status.json"
    if owner_path.exists():
        owner_status = _load(owner_path)
        if owner_status.get("schema_version") != OWNER_SCHEMA:
            raise ValueError("unsupported owner-status schema")
        _stamp(owner_status.get("updated_at_utc"))
        if "live_broker_arming" in owner_status and not isinstance(owner_status["live_broker_arming"], bool):
            raise ValueError("live_broker_arming must be boolean")
        claude = owner_status.get("claude")
        if claude is not None:
            if not isinstance(claude, dict) or not isinstance(claude.get("active"), bool):
                raise ValueError("claude owner status must contain boolean active")
            if claude.get("return_date") is not None and not isinstance(claude.get("return_date"), str):
                raise ValueError("claude return_date must be string or null")

    return {
        "sessions": sessions,
        "events": events,
        "summaries": summaries,
        "owner_status": owner_status,
    }


def _overlap(left: str, right: str) -> bool:
    return left == right or left.startswith(right + "/") or right.startswith(left + "/")


def _mutual_cooperation(a: dict[str, Any], b: dict[str, Any]) -> bool:
    return (
        a.get("coordination_mode") == "cooperate"
        and b.get("coordination_mode") == "cooperate"
        and b["session_id"] in a.get("cooperates_with", [])
        and a["session_id"] in b.get("cooperates_with", [])
    )


def compile_state(root: Path | str, *, now: datetime | None = None) -> dict[str, Any]:
    tree = validate_tree(root)
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    by_session: dict[str, list[dict[str, Any]]] = {sid: [] for sid in tree["sessions"]}
    for _, event in tree["events"]:
        by_session[event["session_id"]].append(event)
    for events in by_session.values():
        events.sort(key=lambda e: (_stamp(e["at_utc"]), e["event_id"]))

    rows: list[dict[str, Any]] = []
    terminal_rows: list[dict[str, Any]] = []
    for sid, session in sorted(tree["sessions"].items()):
        events = by_session[sid]
        latest = events[-1] if events else None
        last_at = _stamp(latest["at_utc"]) if latest else _stamp(session["started_at_utc"])
        terminal = bool(latest and latest["type"] in TERMINAL_TYPES)
        stale = (not terminal) and now - last_at > timedelta(minutes=session["stale_after_minutes"])

        reservations: list[str] = []
        dependencies = list(session.get("initial_dependencies", []))
        mode = "independent"
        cooperates: list[str] = []
        for event in events:
            if event["type"] in TERMINAL_TYPES or event["type"] == "RELEASE":
                reservations = []
            elif event.get("paths"):
                reservations = list(dict.fromkeys(event["paths"]))
            if event.get("dependencies"):
                dependencies = list(dict.fromkeys(event["dependencies"]))
            mode = event.get("coordination_mode", mode)
            cooperates = list(dict.fromkeys(event.get("cooperates_with", cooperates)))

        row = {
            "session_id": sid,
            "actor": session["actor"],
            "model_family": session["model_family"],
            "goal": session["goal"],
            "home_repo": session["home_repo"],
            "branch": session["branch"],
            "pr": session.get("pr"),
            "status": "complete" if latest and latest["type"] == "COMPLETE" else "cancelled" if latest and latest["type"] == "CANCELLED" else "active",
            "phase": latest["phase"] if latest else "registered",
            "latest_type": latest["type"] if latest else "REGISTERED",
            "latest_summary": latest["summary"] if latest else session["goal"],
            "last_event_at_utc": latest["at_utc"] if latest else session["started_at_utc"],
            "dependencies": dependencies,
            "reserved_paths": [] if stale or terminal else reservations,
            "declared_paths": reservations,
            "coordination_mode": mode,
            "cooperates_with": cooperates,
            "stale": stale,
            "reclaimable": stale and not terminal,
        }
        (terminal_rows if terminal else rows).append(row)

    collisions: list[dict[str, Any]] = []
    live_rows = [row for row in rows if not row["stale"] and row["reserved_paths"]]
    for idx, left in enumerate(live_rows):
        for right in live_rows[idx + 1:]:
            if _mutual_cooperation(left, right):
                continue
            pairs = sorted({(lp, rp) for lp in left["reserved_paths"] for rp in right["reserved_paths"] if _overlap(lp, rp)})
            if pairs:
                collisions.append({
                    "sessions": [left["session_id"], right["session_id"]],
                    "path_pairs": [[a, b] for a, b in pairs],
                    "severity": "collision",
                })

    return {
        "schema_version": "icarus-coordination-index-v2",
        "generated_at_utc": now.isoformat().replace("+00:00", "Z"),
        "owner_status": tree["owner_status"],
        "active_sessions": rows,
        "terminal_sessions": terminal_rows,
        "collisions": collisions,
        "counts": {
            "active": len(rows),
            "terminal": len(terminal_rows),
            "stale": sum(bool(row["stale"]) for row in rows),
            "collisions": len(collisions),
        },
    }


def render_active(state: dict[str, Any]) -> str:
    lines = [
        "# ICARUS Active Coordination",
        "",
        f"Generated: `{state.get('generated_at_utc', '')}`",
        "",
        f"Active sessions: **{state.get('counts', {}).get('active', 0)}** · "
        f"Stale/reclaimable: **{state.get('counts', {}).get('stale', 0)}** · "
        f"Collisions: **{state.get('counts', {}).get('collisions', 0)}**",
        "",
        "| Session | Phase | Repo / branch | Latest note | Dependencies | Reserved paths |",
        "|---|---|---|---|---|---|",
    ]
    for row in state.get("active_sessions", []):
        stale = " ⚠️ STALE/RECLAIMABLE" if row.get("stale") else ""
        deps = "<br>".join(row.get("dependencies") or []) or "—"
        paths = "<br>".join(row.get("reserved_paths") or []) or "—"
        lines.append(
            f"| `{row['session_id']}`{stale} | {row['phase']} | "
            f"`{row['home_repo']}` / `{row['branch']}` | {row['latest_summary']} | {deps} | {paths} |"
        )
    if state.get("collisions"):
        lines += ["", "## Active collisions", ""]
        for item in state["collisions"]:
            pairs = ", ".join(f"`{a}` ↔ `{b}`" for a, b in item["path_pairs"])
            lines.append(f"- **{' ↔ '.join(item['sessions'])}**: {pairs}")
    return "\n".join(lines) + "\n"


def prune_terminal_events(root: Path | str, *, now: datetime | None = None, days: int = 14) -> list[str]:
    if not isinstance(days, int) or days < 1:
        raise ValueError("days must be a positive integer")
    root = Path(root)
    tree = validate_tree(root)
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc)
    cutoff = now - timedelta(days=days)
    by_session: dict[str, list[tuple[Path, dict[str, Any]]]] = {sid: [] for sid in tree["sessions"]}
    for path, event in tree["events"]:
        by_session[event["session_id"]].append((path, event))

    removed: list[str] = []
    for sid, records in by_session.items():
        if not records or sid not in tree["summaries"]:
            continue
        records.sort(key=lambda pair: (_stamp(pair[1]["at_utc"]), pair[1]["event_id"]))
        latest = records[-1][1]
        if latest["type"] not in TERMINAL_TYPES or _stamp(latest["at_utc"]) >= cutoff:
            continue
        for path, _ in records:
            rel = path.relative_to(root).as_posix()
            path.unlink()
            removed.append(rel)
    return sorted(removed)
