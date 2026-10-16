# ICARUS federation instructions for every AI/chat

Every AI unit working in this repository is part of the shared ICARUS evidence, governance, and coordination plane. Model identity does not grant or restrict task ownership.

## Mandatory coordination before substantial work

Read these first:

- `coordination/START_HERE.md`
- `coordination/README.md`
- `coordination/ACTIVE.md`
- `coordination/collisions.json`
- applicable files under `coordination/directives/`

Create or resume a unique coordination session and publish a `PLAN` or `CLAIM` event before modifying shared code/workflows/UI/contracts. Publish `WAITING` while CI/review/external dependencies are pending, `UPDATE` when scope changes, `HANDOFF` when another worker can use/take over work, and `COMPLETE` only with fresh evidence. Path reservations prevent accidental collisions; they are not permanent ownership. Explicit mutual cooperation is allowed and encouraged.

Claude is currently inactive by owner direction. Legacy Claude-owned tasks are reclaimable under `coordination/directives/2026-10-16-claude-reclamation.md`; do not wait for Claude authorization and do not mark unfinished work complete merely because Claude is absent.

## Shared GitHub-native credential/data access

Before any claim that an API key, provider, dataset, or shared market-data path is unavailable, read:

- `coordination/directives/GITHUB_NATIVE_DATA_ACCESS.md`
- `reppiks490/Icarus-engine:AGENT_CREDENTIALS.md`
- `reppiks490/Icarus-engine:docs/agent-handoffs/GITHUB_NATIVE_CREDENTIALS.md`
- `reppiks490/Icarus-engine:config/credential_contract.json`
- `reppiks490/Icarus-engine:config/data_ingestion_manifest.json`

The shared authority is GitHub Actions-backed capability plus persisted evidence—not plaintext key possession. **Do not search local `.env` files, `$ICARUS_HOME/.env`, DAV task comments, Plant/operator notes, another AI account, or another worker workspace for a shared private key.** Do not ask another AI to reveal one. GitHub Actions Secrets are intentionally injected into approved workflows at runtime; a normal chat not being able to read the value is expected.

Use the ingestion manifest's `evidence_paths` first. If fresh collection is required, use or extend the established GitHub Actions provider lane without exposing the secret. Only report a credential blocker when canonical redacted health, the ingestion manifest, or a verified provider response proves missing/invalid/denied access.

## Shared ICARUS data/evidence truth

Before claims about provider data, source access, freshness, research status, mission completion, or blockers, read the canonical federation state in `reppiks490/Icarus-engine`:

- `config/data_ingestion_manifest.json`
- `docs/agent-handoffs/FEDERATED_DATA_COLLECTION.md`
- `docs/agent-handoffs/DATA_GAP_LEDGER.md`
- `automation_intelligence/sentinel/data_health.json`
- `automation_intelligence/manifest.json`

This repository's `mission/**` records and certificates are governance/evidence artifacts, not a separate market-data source. `.github/workflows/mission-register.yml` is an offline consistency gate and does not grant API access.

Do not store or copy plaintext provider credentials here. GitHub-native credential authority and provider runtime evidence live in the shared ICARUS data plane. If a task depends on a source unavailable to this AI unit, record the blocker explicitly rather than assuming another account's connector or secret is transferable.

Preserve immutable mission history, evidence provenance, research-only authority, and execution gates. **Live broker arming is currently disabled by owner direction.** Every AI unit has a standing obligation to close ICARUS-owned gaps it discovers or publish the exact external blocker and evidence path, and to continue useful non-conflicting work rather than going silent while one dependency is waiting.
