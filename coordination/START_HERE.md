# ICARUS multi-chat START HERE

## Current operator startup

**Complete PC/Git Bash command guide: [Icarus START_HERE.md](https://github.com/reppiks490/Icarus/blob/main/START_HERE.md).** It is also linked at the top of Icarus's default README. The owner authorized a limited current as-is paper launch; full-system readiness remains NO_GO and live broker execution stays disabled. Runtime code is on `icarus1/restart-readiness-20261020` (PR462), not automatically on main.

Published operator source `debf6e180eb41db120a139f92a694f60f6994916`: preceding startup aggregate3852passed,4skipped,111subtests; actual contained launcher start/stop and persistent-state regression verified. Final narrow drawer correction passed4targeted browser+122UI/world/JS checks and unchanged cinema; final hosted results remain a separate pending disposition. These are cloud/synthetic checks, not an owner-PC restart. The runbook provides a separate source worktree, private backup, explicit feed/assets, one-command local shortcut, all dashboard URLs, diagnostics/exports and rollback. [Icarus2 remaining-access continuation](https://github.com/reppiks490/Icarus/blob/icarus1/restart-readiness-20261020/docs/recovery/ICARUS2_NEXT_12_DAYS.md) preserves next priorities and current limits. Consult the durable session summary for later exact-head CI.


This is the common entrypoint for every ChatGPT/Codex/Claude/other AI chat working anywhere in the ICARUS federation. The coordination bus is intentionally model-neutral: tasks are not owned by a model family. Coordination and evidence are mandatory; artificial agent gating is not.

## Current recovery direction

Read [the 2026-10-20 Icarus two-worker recovery direction](directives/2026-10-20-icarus-two-worker-recovery.md) first. Icarus 1 leads runtime recovery; Icarus 2 has registered the separate `icarus2-20261020-federation-integration` session. A full restart waits for verified readiness. The runtime recovery record is `reppiks490/Icarus:docs/recovery/ICARUS_RECOVERY_STATUS.md` on `icarus1/restart-readiness-20261020` (draft PR #462) until reviewed and released.

The earlier five-agent board in issue #59 and `coordination/directives/2026-10-19-five-agent-final-convergence.md` remains historical scope/evidence. Its mandatory identity selection is superseded for this recovery workstream by the owner's newer direction. Keep its unresolved audit questions visible without assigning those names to Icarus 1 or Icarus 2.

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
