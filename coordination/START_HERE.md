# ICARUS multi-chat START HERE

## Current operator startup and stopping point

**Use the [current pinned PC restart guide](https://github.com/reppiks490/Icarus/blob/main/docs/recovery/PRIME_AS_IS_RESTART.md).** Exact source: `7aa3900282213c4e690436098702300a0447cb8d`, tree `d6020c33e6a7c7d72946a2faaae52ca8189bae40`, branch `prime/as-is-restart-20261022`, [PR #471](https://github.com/reppiks490/Icarus/pull/471). The frozen equivalent local build passed **4,083 tests and 111 subtests**, with 89 explicit skips. Final-source real Chromium power controls passed 16 checks and four additional browser API/settings/lifecycle checks passed. Exact-head hosted Linux and visual jobs passed; Windows restart-persistence checks passed, while the broader Windows suites were still executing at the delivery observation. Consult the receipt and PR for subsequent conclusions.

Permanent worker `icarus2`, session `icarus2-20261020-federation-integration`, carries the Prime role under the [owner takeover directive](directives/2026-10-22-owner-prime-takeover.json); the original Prime remains stopped. **State: WAITING_OWNER_PC_READBACK_AND_WINDOWS_CI**, rather than standby before actual PC restart verification. The recurring federation mega-loop remains cancelled; paused specialists remain paused. Existing worker/scheduler records are provenance, not renewed execution permission.

The create-only, byte-verified [delivery handoff](handoffs/prime-installer-expanded-restart-20261023.json) records exact source/blob identities, actual tests and reviews, earlier failures/cancellations, provider boundaries and remaining work. Runtime includes independent paper worker ON/OFF, responsive Main monitoring, Windows Python 3.10 setup repair, asset-error diagnostics and expected client-disconnect handling. The guide includes backup, exact-version verification, the canonical 35-symbol Main command, saved CC preservation, diagnostics and rollback. Main documentation commit `5fa97822af3b1af31610772a58bd8f7f5635e41d` replaces current instructions; [old notes retain their original bytes in the archive](https://github.com/reppiks490/Icarus/blob/main/docs/recovery/archive/2026-10-23/INDEX.md). Runtime code has not been merged into main.

Full-system readiness remains **NO_GO** and **execution_authorized=false**. Cloud checks do not certify owner-PC uptime, current feed/history/journal freshness, entitlement, open-position reconstruction or measured trading value. Earlier contained synthetic launcher rehearsals passed core lifecycle checks but retained strict **NOT_FULLY_READY** because external attempts were denied. Owner-PC command output is the next required evidence; no restart on that PC is claimed.

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
