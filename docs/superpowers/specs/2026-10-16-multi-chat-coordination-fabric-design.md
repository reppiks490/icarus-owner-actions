# Multi-Chat Coordination Fabric Design

## Intent

Scale ICARUS collaboration from a small Claude/ChatGPT board model to an adaptive many-chat work fabric that can support dozens of concurrent ChatGPT chats without task ownership gates. Every worker must publish what it is about to do, what paths it expects to touch, what it is waiting on, what changed, and what evidence proves completion. The fabric prevents accidental overlap through visibility and collision detection, not model-specific ownership.

## Non-negotiable constraints

- Live broker arming remains out of scope.
- No plaintext credentials, account secrets, or licensed raw vendor payloads may enter coordination records.
- A task is never reserved to a model family. Claude being inactive cannot block work.
- Every worker records intent before implementation or destructive mutation.
- Waiting on CI, provider responses, review, or another dependency is itself a reportable work state.
- Coordination must remain useful at 50-60+ concurrent chats.
- Work must be discoverable from any participating ICARUS repository.
- Claims are evidence-backed; completion requires test/runtime evidence.

## Architecture

`reppiks490/icarus-owner-actions` is the central coordination bus. It is governance-oriented, small, public, and independent of trading/runtime execution.

Each chat receives a unique `session_id`, for example `chatgpt-20261016-futures-expansion-a1b2c3`. A session has one registration record and writes immutable event files rather than appending to a shared ledger. This avoids a high-contention single-file write path.

### Records

- `coordination/sessions/<session_id>.json` — stable session identity, goal, home repo, branch/PR, capabilities, initial dependencies.
- `coordination/events/YYYY/MM/DD/<session_id>/<timestamp>-<event_id>.json` — one event per note.
- `coordination/summaries/<session_id>.json` — compact terminal summary required before cleanup.
- `coordination/index.json` — generated global view of active sessions, reservations, dependencies, stale workers, and latest evidence.
- `coordination/ACTIVE.md` — generated human-readable view for chats and the owner.
- `coordination/collisions.json` — generated list of active path conflicts or mutually incompatible declared changes.

### Event types

`START`, `PLAN`, `CLAIM`, `HEARTBEAT`, `WAITING`, `UPDATE`, `BLOCKED`, `HANDOFF`, `RELEASE`, `COMPLETE`, `CANCELLED`.

Every event contains `session_id`, `at_utc`, `type`, `summary`, `repos`, `paths`, `dependencies`, `evidence`, and `next_action`. `CLAIM` and `PLAN` events declare intended paths. `WAITING` must name the dependency, such as a CI run URL/run id. `COMPLETE` must cite verification evidence.

### Cooperative reservation semantics

A reservation is an advisory collision-prevention lease, not ownership. Two sessions may deliberately overlap only when both records declare `coordination_mode: cooperate` and reference each other. Otherwise overlapping exact paths or ancestor/descendant path reservations are reported in `collisions.json` and the later worker must either choose different files or publish a cooperation note before proceeding.

Reservations expire when released/completed/cancelled or when a session becomes stale. Staleness never transfers authority; it merely marks work as reclaimable.

### Compiler

`python -m coordination_fabric` validates registrations/events and compiles the latest per-session state. It must be deterministic, tolerate hundreds of event files, reject malformed paths/timestamps/event types, and never execute repo code from events.

The compiler also emits:

- active session count and latest heartbeat;
- declared repo/branch/PR/goal;
- current phase (`planning`, `coding`, `testing`, `waiting`, `reviewing`, `fixing`, `researching`, `complete`, etc.);
- path reservations;
- dependency graph;
- collision set;
- stale sessions;
- Claude-inactive notice and reclaimable legacy work notice.

### Cleanup

`python -m coordination_fabric prune --days N` may remove working-tree event files only for terminal sessions that already have a summary and whose last event is older than `N` days. It never rewrites Git history. Active, blocked, or waiting sessions are never pruned. Default automated retention is 14 days.

### Claude inactivity

The owner has declared Claude inactive for roughly one to two months. The fabric records this as an owner status fact without inventing a return date. Existing Claude tasks become available to other chats after they publish a takeover/cooperation event. No code path may require a Claude reply before work can continue.

## Cross-repository adoption

Every ICARUS `AGENTS.md` must point to this bus and require:

1. Read `coordination/ACTIVE.md` and `coordination/collisions.json` before substantial work.
2. Register or resume a session.
3. Publish `PLAN/CLAIM` before mutation.
4. Publish `WAITING` when blocked on CI/review/external dependencies instead of going silent.
5. Publish `UPDATE` when scope/paths change.
6. Publish `COMPLETE` with verification evidence or `BLOCKED` with the exact blocker.
7. Continue useful non-conflicting work when a dependency is waiting.

Legacy Engine `coordination/board/*` and inbox records remain historical evidence but no longer impose model-specific task gates.

## UI

Icarus Engine will expose a read-only coordination endpoint backed by the compiled public bus and a dashboard panel showing active workers, phase, repo/branch, latest note, waiting reason, reserved paths, dependencies, and collisions. UI access is observational only; it does not arm execution or mutate reservations.

## Verification

Tests must cover schema rejection, deterministic compilation, collision detection, cooperation exceptions, stale/reclaimable state, waiting notes, Claude inactivity semantics, summary requirements, safe pruning, and generated Markdown. Cross-repo tests must verify each participating `AGENTS.md` points to the central fabric. UI tests must verify the coordination endpoint and dashboard rendering without network access by using fixture data.