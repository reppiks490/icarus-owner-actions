# ICARUS Multi-Chat Coordination Bus

This directory is the canonical cooperation bus for all ICARUS coding/research chats and agents. It replaces model-specific task ownership as a coordination mechanism. Tasks are not gated to Claude, ChatGPT, Codex, Grok, or any other model family. Cooperation, evidence, and collision avoidance are mandatory.

## Before substantial work

1. Read `coordination/ACTIVE.md`, `coordination/collisions.json`, and applicable directives under `coordination/directives/`.
2. Create or resume exactly one `coordination/sessions/<session_id>.json` identity for this chat/workstream.
3. Before modifying code, workflows, UI, data contracts, or shared documentation, publish a `PLAN` or `CLAIM` event naming the repository and intended paths.
4. If another active session reserves an overlapping path, do not silently overwrite it. Either choose different paths or both sessions publish mutual `coordination_mode: cooperate` notes referencing each other.
5. Reservations prevent accidental collisions; they do **not** grant model ownership of a task.

## While working

Publish a new immutable event whenever any of these is true:

- scope or target paths change (`UPDATE`);
- a meaningful checkpoint is reached (`HEARTBEAT` or `UPDATE`);
- you are waiting on CI, provider responses, review, another branch, or another agent (`WAITING`);
- an external or internal blocker is established (`BLOCKED`);
- another session can use your result or should take over a subproblem (`HANDOFF`).

A chat waiting on CI should say so explicitly, for example: `waiting on Icarus-engine PR #123 run 456; focused tests passed; continuing non-conflicting source audit`. Waiting is not permission to disappear when other useful non-conflicting work exists.

## Before stopping or declaring completion

- Publish `COMPLETE` only with concrete evidence: PR/head, test run, runtime receipt, artifact, or exact external blocker.
- Publish `RELEASE` when abandoning reserved paths without completing the whole session.
- Publish `CANCELLED` only when the workstream itself is intentionally abandoned.
- Write `coordination/summaries/<session_id>.json` before old terminal events are eligible for pruning.

## Record model

- `sessions/*.json` — stable chat/workstream identity.
- `events/YYYY/MM/DD/<session_id>/*.json` — immutable individual notes. Separate files avoid a single high-contention append ledger.
- `summaries/*.json` — durable terminal summaries.
- `index.json` — compiled active/terminal state.
- `ACTIVE.md` — human-readable active worker view.
- `collisions.json` — active overlapping path reservations requiring resolution.
- `owner_status.json` — owner-declared global constraints/availability.

Use `python -m coordination_fabric validate` to validate records and `python -m coordination_fabric compile` to rebuild the generated views. `python -m coordination_fabric prune --days 14` may remove old terminal event files from the working tree only after a durable session summary exists. Git history remains the provenance record.

## Automatic refresh and retention cleanup

The `coordination-maintenance` GitHub Actions workflow automatically refreshes the compiled coordination surfaces when session, event, summary, or owner-status records change on `main`. Each publication attempt fetches the latest `main`, performs `git reset --hard origin/main`, validates the record tree, recompiles `coordination/ACTIVE.md`, `coordination/index.json`, and `coordination/collisions.json`, and refuses to publish while an undeclared active collision exists. If another worker moves `main` before the push succeeds, the workflow discards that stale derived snapshot and recomputes from the newer main before retrying.

The workflow also runs every five minutes, offset from minute zero, to recover when connector-authored commits skip push triggers. This scheduled freshness fallback compiles but does not prune. Retention is summary-gated and runs only when an operator explicitly invokes `workflow_dispatch` with a configurable `retention_days` value. Pruning calls `python -m coordination_fabric prune --days N`; only old terminal sessions that already have a durable summary are eligible. Active, waiting, blocked, stale-but-reclaimable, or unsummarized work is not deleted. After pruning, the workflow validates and recompiles the shared views again before pushing.

For an easy manual cleanup, run the `coordination-maintenance` workflow with `workflow_dispatch` and choose the desired retention window. Local operators may run `python -m coordination_fabric prune --days N`, followed by validate/compile, but the Actions workflow is preferred because it applies the fresh-main concurrency retry rules automatically. Working-tree event cleanup never rewrites Git history; Git history remains the durable provenance trail for notes that have been pruned from the current tree.

## Scale rules for 50+ chats

- Session IDs must be unique and stable for the life of the chat/workstream.
- Do not reuse another chat's session ID.
- Prefer narrow path reservations. Reserving an entire repository when only two files will change creates unnecessary collisions.
- Split independent work into separate sessions when it materially improves parallelism.
- Link dependencies using concrete identifiers (`github-run:...`, `pr:repo#...`, `session:...`, `external:...`).
- Read current compiled state before every new implementation phase, not only at chat startup.
- Cross-repo work must list every affected repository/path before mutation.
- No agent may infer another chat's credentials, connector access, or unstaged local work.

## Claude availability and legacy boards

The owner has declared Claude inactive for approximately one to two months, without a fixed return date. Claude's unfinished work is therefore reclaimable by active chats after a takeover/cooperation note is published. Do not mark legacy Claude work complete merely because Claude is absent.

`reppiks490/Icarus-engine/coordination/board/*` and its old two-agent inbox remain historical evidence and may help discover unfinished work, but their model-specific ownership rules are superseded by this bus. They are inputs to reconciliation, not task locks.

## Safety boundary

Live broker arming remains disabled by owner direction. Coordination notes never contain plaintext credentials, broker secrets, private tokens, or licensed raw vendor payloads. A coordination record can point to secured evidence; it must not duplicate that evidence if duplication would violate security or licensing rules.
