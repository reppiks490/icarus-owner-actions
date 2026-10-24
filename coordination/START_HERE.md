# ICARUS multi-chat START HERE

## Current full restart and HIGHLY IMPORTANT Inputs

Use the [current full restart guide](https://github.com/reppiks490/Icarus/blob/main/docs/recovery/PRIME_AS_IS_RESTART.md) and [HIGHLY IMPORTANT NQ/ETHUSD/SOLUSD settings](https://github.com/reppiks490/Icarus/blob/main/docs/recovery/HIGHLY_IMPORTANT_RESTART_INFO.md). Exact runtime: `3122d349524fbce803970dc34ab6fc74dad87467`; tree `9ad37de97e160aead6602351b54c43608086a006`; branch `prime/as-is-restart-20261022`; [PR #471](https://github.com/reppiks490/Icarus/pull/471). Main documentation commit `3b82b2c3d95e5854e8d57ddd22f9bab55891b2c6` updates five documentation files only; runtime remains on the draft branch. [Old notes are archived with exact original bytes](https://github.com/reppiks490/Icarus/blob/main/docs/recovery/archive/2026-10-24/INDEX.md).

Owner explicitly requests every Main/CC asset use actual Main NQ strategy/chart defaults, with BOTH ETHUSD and SOLUSD exceptions: 30-minute timeframe, RTH/session filtering disabled, quantity input 25. This supersedes preserving old custom Inputs; journals, asset selections, power settings and native contract economics remain preserved. The preparation helper captures authenticated live NQ or verifies actual saved NQ when stopped, never silently substitutes stock values. It works whether the owner has already pressed Ctrl+C or is still running. Stop normally after preparation, then use the full guarded backup/apply/verify/launch commands. Phone reconnection follows actual PC restart confirmation.

The source retains native NEXUS/AION connections, Main rendering/scrolling fixes, bounded chart batches, independent CC1–CC4 switches, Windows setup repair and all 35 Main symbols. It repairs reproduced request blocking: authentication activity writes no longer block reads; status consumes published runner/journal views rather than doing work on HTTP. Dirty or unavailable accounting remains unknown while assets remain observable. Metadata is published after committed Main/CC/activation changes. No request deadlines or freshness limits were widened.

State: **WAITING_EXACT_HEAD_HOSTED_CHECKS_AND_OWNER_PC**. Frozen source passed 4,152 runtime checks, 128 skipped, 111 subtests (468.28s), and all 107 real Chromium checks (437.29s). Eighteen defaults/preparation checks include actual Python 3.10; auth integration passed 96 checks; final writer audit 69. Exact-head Linux/Windows/visual CI is running with no failure observed; no final Windows pass is claimed yet. [Receipt 022](events/2026/10/24/icarus2-20261020-federation-integration/022-full-restart-published-hosted-waiting.json) records exact identities and pending state. Earlier-source passes are historical evidence, not this head's Windows pass.

Permanent worker `icarus2`, session `icarus2-20261020-federation-integration`, carries the functional Prime role under the [owner takeover directive](directives/2026-10-22-owner-prime-takeover.json). Original Prime remains stopped. The recurring federation mega-loop remains cancelled and paused specialists remain paused. Worker/scheduler records are provenance, not new execution permission.

Full-system readiness remains **NO_GO** and **execution_authorized=false**. Cloud checks do not certify owner-PC restart, sustained uptime, provider freshness/entitlement, open-position reconstruction or trading accuracy. Do not resume unrelated collection, training, live broker arming, spending, scheduler changes or a main runtime merge.

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
