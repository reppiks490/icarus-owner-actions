# ICARUS historical recovery / continuity master plan — 2026-10-07

**Status: IN PROGRESS, not fully recovered.** This recovery record is source-verified, non-trading, and non-destructive. It grants no new broker, paid-provider, deployment, publication or trade authority. No passwords or raw licensed market data may be committed here.

## Recovery truth

1. Every currently accessible repo in the connected owner account (18/18) is public as of the audit; DAEDALUS, Causal Router and Owner Actions recently changed visibility. This does **not** validate every workflow.
2. DAEDALUS scheduled assurance run [37639188767](https://github.com/reppiks490/daedalus-research-os/actions/runs/37639188767) attempt 3 succeeded on `main`. Causal Router run [37644317860](https://github.com/reppiks490/icarus-causal-router/actions/runs/37644317860) attempt 3 failed **after** the runner started: missing `causal_router.journal`. Treat this as a code defect, not private-runner quota.
3. Canonical hybrid contracts: [engine hybrid fabric](https://github.com/reppiks490/Icarus-engine/tree/main/automation_intelligence/hybrid_loop_fabric_v1). On current default branch: 306 immutable requests versus five exact result files (77/0 robustness, 77/0 advanced CSV, 76/1 alpha, 76/4 microstructure). The remaining 301 have no matching result file on `main`. Other branches, artifacts and prior commits may supply additional evidence and must be audited before calling a record unrecoverable.
4. The engine contains ~801 restored-five receipt JSON files, other historical ledgers, GitHub run histories, and encrypted provider checkpoints. Liveness receipts, nominal requests and status dashboards do **not** by themselves prove substantive research happened.
5. Eleven provider artifact ZIPs from [ICARUS run 37694893733](https://github.com/reppiks490/Icarus/actions/runs/37694893733) were downloaded and hashed separately as evidence; each is a **receipt-only** archive and records no newly collected market rows. The provider artifacts from that run expire **2026-10-14**. Never treat a green collection workflow as proof of row-level ingestion.
6. A separate `Icarus-engine` provider collection receipt shows **partial** ingestion: FRED 2,794 rows; Tiingo 27,453; FMP 6,853; EODHD 70 (all with encrypted checkpoints). These are provider-reported counts, not independently checked raw payloads. Other configured providers report missing credentials or other blocks. Cross-repository credentials do not automatically propagate.
7. `icarus-owner-actions/intake/research_assurance_registry.json` is stale about visibility and runner states. Correct only on fresh evidence.

## Action order and ownership

### P0 — evidence rescue and expiration
- Query every relevant GitHub repository's workflow runs, artifact pages, expiration timestamps and logs. Archive **unexpired** evidence with SHA-256 and complete provenance before each deadline.
- Store licensed/raw/private datasets only in an approved private encrypted destination; public GitHub holds metadata, redacted diagnostic receipts, and references.
- Catalogue existing repo branches, commits, immutable ledgers, encrypted checkpoints and ChatGPT/Library exports. Recover existing bytes first; recollect only licensed historical data genuinely available from source.
- Missing raw data, lost secrets, or never-executed jobs **cannot** be reconstructed merely by replaying a scheduler.

### P1 — oldest unresolved requests
- Read `registry.json` and `CONTRACT.md`; verify exact lane ID, original request, contract fingerprint and current authorization.
- Audit all unresolved requests, including older than the 24-request hot window, oldest unresolved first; avoid erasing or renaming originals.
- Only produce an exact immutable `icarus-hybrid-work-result-v1` after **actual** substantive work. For time-sensitive missed slots, never pretend to have observed at the old time: truthfully mark `BLOCKED`, preserve due-slot provenance, record actual recovery time and blockers.
- Commit the result into the exact expected path and fetch its byte-identical contents back. Do not equate Github liveness with cognition.

### P2 — repairs and assurance
- Restore Causal Router's missing journal/session module with idempotent SQLite replay, deterministic hash integrity and crash/duplicate validation; tests must pass before merge.
- Keep DAEDALUS and AION research-only; retain their assurance evidence and compare freshest `main` SHAs.
- Update stale owner assurance registry with visibility, actual run attempt and conclusion.
- Set appropriate reviewed branch protection/rulesets on public `main` branches; do not interrupt other active branch ownership.

### P3 — provider and UI propagation
- Verify per-repository secret **presence** and auth/entitlement without exposing values. In particular, ICARUS vs ICARUS Engine have different collection results.
- Verify checksum/decryption rights, row counts, event timestamps, retrieval timestamps, source, license, asset, timeframe and chart construction, data gaps, duplicates and transformations.
- Feed verified research outputs and lineage into existing canonical engine federation, and expose in the ICARUS UI: last *substantive* result, request backlog, provider collected_rows vs blocked, artifact expiry, source age and no-trade status.
- Any read path claiming success needs an end-to-end consumer/UI test, not just successful producer Actions.

### P4 — value gate
- Every loop must declare a question, qualified inputs, unique verifiable output, actual consumer, cost/budget, error/latency, data retention, and acceptance test.
- Avoid duplicate green heartbeat loops without meaningful evidence. Do not infer profitable edges or future prices from synthetic/unvalidated historical replay.

## Master continuation prompt

> Continue ICARUS recovery from **current** GitHub HEAD and this documented evidence, without resetting/restarting ongoing branches or rewriting unique work. First preserve unexpired Actions artifacts and enumerate all immutable hybrid requests/results/receipts. Audit all 18 visible repositories with source-linked evidence, clearly separate durable liveness from completed substantive cognition, and reconcile each old request oldest first. Never fabricate missing historical observations. Diagnose and repair verified CI issues through isolated tests and PRs. Verify separately per-repository provider credentials and entitlements without exposing values; preserve public vs private/licensed data boundaries. Trace each meaningful output into the existing engine federation and ICARUS UI, including last substantive processing, backlog, coverage and expiry. Keep execution_authorized=false, protected holdouts and broker restrictions intact. No force pushes, destructive moves, broad merges or unverified success claims. Update the shared audit registry with live status, and make every loop demonstrably useful. Continue iterating with current-head tests and evidence-backed completion gates.

## Acceptance criteria

The project is **not finished** until: expired-vs-recovered artifacts are inventoried; every historical request has a verifiable exact result or clearly documented irrecoverable blocker; tested provider ingestion persists valid licensed rows; Causal Router passes; assurance registry is fresh; UI consumers display evidence; relevant branch/security protections are reviewed; and missing data is never quietly relabeled as recovered.
