# ICARUS multi-chat START HERE

## Current operator startup and stopping point

**Use the [current pinned PC restart guide](https://github.com/reppiks490/Icarus/blob/main/docs/recovery/PRIME_AS_IS_RESTART.md).** Exact newest source: `402722b4b708fc0ea6e2b2ede62252e75ccdd4a0`, tree `7df29ad8829d123eb6ad52e4599fe464c8295db3`, branch `prime/as-is-restart-20261022`, [PR #471](https://github.com/reppiks490/Icarus/pull/471). All eight newest-head hosted workflows succeeded, including Windows/Linux and actual browser/visual checks. The preceding identical runtime passed the local 4,009-test full suite and separate 177 API/Chromium checks.

The owner's previous Prime is stopped. By [owner takeover directive](directives/2026-10-22-owner-prime-takeover.json), the current Prime role is carried by permanent worker `icarus2`, session `icarus2-20261020-federation-integration`. The owner now requests a stopping point, updated observable as-is paper restart and replacement/archive of old restart notes. **Current Prime is on standby until the owner calls again; the broad recurring integration loop remains cancelled.** Existing worker/scheduler records are provenance, not renewed execution permission.

The [final handoff](handoffs/prime-as-is-restart-20261023.json) separates cloud tests from the owner-PC launch still to be performed. Runtime code has not been merged into main. Documentation-only main commit `3ed592bb190db563efb42daf9856a5ab040de304` replaces old operator entrypoints and [archives their original bytes and blob identities](https://github.com/reppiks490/Icarus/blob/main/docs/recovery/archive/2026-10-23/INDEX.md). The [former coordination startup entrypoint](archive/restart-notes/2026-10-23/START_HERE.md) is historical.

Full-system readiness remains NO_GO and execution_authorized=false. The tested launcher preserves the existing private root and independently saved workspaces. No proof of owner-PC uptime, paid-feed entitlement, measured trading value or full subsystem readiness is inferred. Existing main background network/subprocess attempts were denied during contained rehearsal; its strict result remains NOT_FULLY_READY despite passing core start/status/preserved-config/shutdown.

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
