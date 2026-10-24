# ICARUS multi-chat START HERE

## Current operator update and stopping point

Use the [current pinned PC update/restart guide](https://github.com/reppiks490/Icarus/blob/main/docs/recovery/PRIME_AS_IS_RESTART.md). Exact source: `c8bd8d49d9fc759067c75ee76157b812ce287775`, tree `98533b4e053d6cc13447c4decd62f5b327385f3c`, branch `prime/as-is-restart-20261022`, [PR #471](https://github.com/reppiks490/Icarus/pull/471). Main documentation commit `19c6c770b52cdafb80f2a9c812bddb8ef1791c9d` replaces current instructions; [the previous guide is archived as its exact original Git blob](https://github.com/reppiks490/Icarus/blob/main/docs/recovery/archive/2026-10-24/INDEX.md). Main received four documentation files only; runtime code remains on the draft branch.

The owner reports that the engine is working but Main scrolling/clicking lag heavily and runtime observations sometimes expire. This update removes the confirmed idle decoration loop, preserves asset/chart nodes, prevents overlapping chart batches and bounds Main chart concurrency while keeping scoped CC readers serial. Request deadlines and freshness limits remain unchanged. The base build's setup, independent CC1–CC4 power, disconnect handling, saved state and 35-symbol Main list are retained.

State: **WAITING_CURRENT_HEAD_CI_AND_OWNER_PC_UPDATE**. Ten focused Chromium checks and 114 presentation/client checks passed; the wider browser run passed 93 checks at the identical production UI. The final commit changes only a recovery-test fixture and passed three focused checks. The first hosted visual failure, its hold-all route race, actual-deadline observation repair and exact source are preserved in [event005](events/2026/10/24/icarus2-20261020-federation-integration/005-status-recovery-fixture.json). New exact-head hosted Chromium route/recovery checks now pass; world contracts and the Linux/Windows test jobs are still running. Earlier-source hosted passes are not current-head passes.

A UI update can keep the existing Python process running only when its owning launcher is already confirmed to use the clean exact previous `7aa390028221` checkout at `C:/Users/tripl/Icarus-as-is`. The guarded guide verifies base/new commit/tree, clean source, four allowed paths and the served script. Hot-update identity is **Python launched at7aa3900, served UI source c8bd8d4**, not a newly restarted c8bd8d4 process. Otherwise use the full controlled restart and preserve the stopped private state. Five synthetic local Git guard scenarios passed; no owner-PC commands were executed.

Permanent worker `icarus2`, session `icarus2-20261020-federation-integration`, carries the Prime role under the [owner takeover directive](directives/2026-10-22-owner-prime-takeover.json). Original Prime remains stopped. The recurring federation mega-loop remains cancelled and paused specialists remain paused. Worker/scheduler records are provenance, not renewed execution permission.

Full-system readiness remains **NO_GO** and **execution_authorized=false**. No PC performance, sustained uptime, feed entitlement/freshness, journal/open-position reconstruction or trading-accuracy success is certified by cloud checks. Real unavailable observations stay unavailable. Continue the bounded update/readback work; do not resume unrelated collection/training, live broker arming, spending, scheduler changes or a main runtime merge.

This is the common entrypoint for every ChatGPT/Codex/Claude/other AI chat working anywhere in the ICARUS federation. The coordination bus is intentionally model-neutral: tasks are not owned by a model family. Coordination and evidence are mandatory; artificial agent gating is not.

## Current recovery direction

The newer owner takeover and stopping-point instructions supersede the primary-worker assignment in the [20 October two-worker direction](directives/2026-10-20-icarus-two-worker-recovery.md). Original source identities and immutable evidence remain intact; do not impersonate the stopped sessions or resume their jobs. Historical directives and unresolved research/provider gates remain evidence, not authority to expand the delivered restart scope.

## Every time the owner tells a chat to continue

1. Read `coordination/ACTIVE.md`, `coordination/collisions.json`, `coordination/owner_status.json`, and the relevant files under `coordination/directives/` in `reppiks490/icarus-owner-actions`.
2. Create or resume one stable `coordination/sessions/<session_id>.json` for this chat/workstream. Never reuse another chat's session ID.
3. Before changing code, UI, workflows, contracts, research state, or shared docs, publish a `PLAN` or `CLAIM` event with repo-qualified `targets` (`repo` + narrow `path`). Read the compiled state again immediately before mutation.
4. Work continuously on useful non-conflicting scope. Publish `WAITING` when CI/review/provider/external work is pending, but keep progressing on independent work. Publish `UPDATE`, `BLOCKED`, `HANDOFF`, or `RELEASE` whenever the state actually changes.
5. Publish `COMPLETE` only with evidence (PR/head, test/run ID, runtime receipt, artifact, or exact external blocker), then create a durable session summary before old event files are eligible for pruning.

Owner communication preference: read `coordination/directives/2026-10-16-owner-contact-boundary.md`. The owner requests no routine progress pings, questions, or manual-work requests while authorized ICARUS work remains; continue independently and use the shared bus for coordination and blockers.

## Mandatory GitHub-native credential and data access

Every AI unit must read `coordination/directives/GITHUB_NATIVE_DATA_ACCESS.md` before declaring that a credential, API, or shared provider-data path is unavailable.

The federation shares **data-access capability and evidence, not plaintext secret strings**. GitHub Actions Secrets are intentionally injected only at workflow runtime; agents are not expected to read those values back.

For provider/data work, the canonical authority is `reppiks490/Icarus-engine`:

- `AGENT_CREDENTIALS.md`
- `docs/agent-handoffs/GITHUB_NATIVE_CREDENTIALS.md`
- `config/credential_contract.json`
- `config/data_ingestion_manifest.json`
- `.github/workflows/github-native-credential-health.yml`

**Do not search `.env` files, DAV task comments, another AI account, or Plant/operator notes for a shared private key.** Those locations are not federation credential authority. If a chat cannot see plaintext, that is expected; use GitHub Actions and the shared evidence paths in `config/data_ingestion_manifest.json` instead. Only report a credential blocker when the canonical health/manifest or provider response proves one.

## Collision rule

A reservation is a coordination lease, not ownership. Two chats may touch the same target only after both publish explicit mutual `coordination_mode: cooperate` records naming each other. Sibling files are independent; an ancestor-directory reservation conflicts with its descendants inside the same repository. Identically named paths in different repositories do not conflict.

## Cooperation rule

When your work can help another active session, reference that session and publish a `HANDOFF`/`UPDATE` instead of silently duplicating it. When you discover a gap outside your original task, either close it if it is non-conflicting or publish a precise claimable handoff. There is almost always useful work available even while one dependency is waiting.

## Owner constraints currently in force

- Claude is inactive by owner direction with no fixed return date. Its unfinished work is reclaimable; see `coordination/directives/2026-10-16-claude-work-reclamation-queue.md`.
- Live broker arming is disabled. Research, replay, simulation, paper/shadow infrastructure and read-only broker validation may continue, but no live-order authority is to be enabled.
- Do not place plaintext API keys, tokens, passwords, sessions, or licensed raw vendor payloads in coordination records.

## Useful commands

```bash
python -m coordination_fabric validate
python -m coordination_fabric compile
python -m coordination_fabric prune --days 14
```

The generated `ACTIVE.md`, `index.json`, and `collisions.json` are views. Immutable per-chat events and durable summaries are the evidence trail; Git history preserves pruned records.
