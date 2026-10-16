# ICARUS federation instructions for AI units

Every AI unit working in this repository must treat owner-actions as part of the shared ICARUS evidence and governance plane.

Before making claims about provider data, source access, freshness, research status, mission completion, or system blockers, read the canonical federation state in `reppiks490/Icarus-engine`:

- `config/data_ingestion_manifest.json`
- `docs/agent-handoffs/FEDERATED_DATA_COLLECTION.md`
- `docs/agent-handoffs/DATA_GAP_LEDGER.md`
- `automation_intelligence/sentinel/data_health.json`
- `automation_intelligence/manifest.json`

This repository's `mission/**` records and certificates are governance/evidence artifacts, not a separate market-data source. `.github/workflows/mission-register.yml` is an offline consistency gate and does not grant API access.

Do not store or copy plaintext provider credentials here. GitHub-native credential authority and provider runtime evidence live in the shared ICARUS data plane. If a mission depends on a source unavailable to this AI unit, record that blocker explicitly rather than assuming another account's connector or secret is transferable.

Preserve immutable mission history, evidence provenance, research-only authority, and execution gates. All AI units have a standing obligation to close ICARUS-owned gaps they discover or publish the exact external blocker and evidence path.
