# A200 to Pulse stopping handoff — 2026-10-17

## Stopping point

Icarus PR [#446](https://github.com/reppiks490/Icarus/pull/446) is merged. It adds a fail-closed historical-data qualification boundary and a signal-only research runtime for the A200 catalog. The merged implementation is at `02e99b1c0f6d50e511ff63eff2247a539d65b3d9` (feature head `881d285f9bee9491128aaf220cf162354ccf179c`).

This is a safe stopping point for the code delivered in #446, **not** completion of the user's goal to connect 200 assets to Pulse. The catalog has 200 listings, but currently has zero source-connected, entitled, historical-qualified, Pulse-enabled, or strategy-qualified rows. Do not describe the assets as operationally connected or Pulse-fed.

## What landed

- `icarus_engine/a200_runtime_feed.py`: rejects history that cannot prove qualification and exposes a signal-only Pulse research path. It does not create positions, fills, or orders.
- `icarus_engine/runtime.py`: adds portfolio research entrypoints while keeping the A200 runner outside the normal portfolio asset list.
- `icarus_engine/bar_receipts.py`: binds the corporate-action policy and source witness into receipt identity.
- `tests_engine/test_a200_runtime_feed.py`: covers the new gate and runtime behavior.
- The path fails closed before provider access when the current adapter cannot attest entitlement, closed-bar status, and source-bound corporate-action adjustment. Corporate-action verifier registry is empty.

The final independent review found no blocking findings after fixes for provider-call avoidance, atomic catalog-snapshot admission, and fail-closed corporate-action proof.

## Verification recorded

- Focused A200 and market-universe tests: **55 passed**.
- Hosted exact-head `tests` run `38960360006`: Linux engine suite passed; Windows engine contract passed.
- Configuration checks run `38960360007` passed on Linux and Windows (push rerun `38960355650`).
- Source-data contract run `38960355579` and intelligence-feed contract run `38960355631` passed on Linux and Windows.
- `py_compile` and `git diff --check` passed.
- A local whole-suite attempt lacked optional xgboost and Databento dependencies and showed dependency-related failures. Hosted CI with its configured extras is the complete passing suite evidence.

## Next bounded work

1. Identify an entitled provider path for the listed assets that can produce auditable source identity, entitlement evidence, closed-bar status, and corporate-action-adjustment evidence.
2. Implement or adapt the provider verifier without weakening freshness, provenance, catalog snapshot, or authority checks; do not spend or add credentials without the required owner authorization and ledger entry.
3. Qualify rows only from source receipts, then demonstrate source-to-Pulse research readback and cover missing, stale, duplicate, mismatched, and incomplete evidence.
4. Update counts from fresh receipts. The milestone is not 200 configured symbols; it is 200 individually evidenced assets reaching the required research qualification states.

No provider call, spend, new credential, broker action, or live-execution authorization occurred in this work. Live execution remains disabled. Until the provider evidence path exists and passes the gate, the correct state is blocked before collection, with zero qualified assets.

## Source of truth

- Implementation and exact-head checks: [Icarus PR #446](https://github.com/reppiks490/Icarus/pull/446).
- Current merged source: Icarus `main` at `02e99b1c0f6d50e511ff63eff2247a539d65b3d9`.
- Session coordination record: `coordination/sessions/codex-20261017-a200-stopping-handoff.json` and its event under `coordination/events/2026/10/17/codex-20261017-a200-stopping-handoff/`.
