# Icarus 2 integration brain implementation plan

**Goal:** Establish a recurring, evidence-bound integration worker with distinct parallel swarms and durable GitHub handoffs to Icarus 1.

**Architecture:** Reuse the canonical federation manifest and coordination compiler. A bounded read-only collector feeds a pure snapshot validator; an independently scheduled agent performs reasoning and reviewed branch repairs. Worker identity and immutable cycle records are separate from runtime health and trading authority.

**Tech stack:** Python standard library, existing GitHub CLI/connector, pytest, current coordination fabric, scheduled-agent runtime.

**Spec:** `coordination/icarus2/DESIGN.md`; approved perpetual-saturation architecture under `docs/superpowers/specs/`.

## Constraints and review focus

Preserve Icarus 1's restart/accounting targets, live-arm lock, zero new spend, private-data boundaries and separate release decisions. Do not treat task names, scheduler configuration, static `LIVE`, fresh heartbeats, publication success or open/closed PR state as completed integration. The five swarms are functional scopes, not acquisition of legacy issue identities.

The principal adverse inputs are mixed repository revisions; incomplete pagination or source-claim reads; future/stale evidence; jobs that never started; and false authority or unverified persistence. Each belongs to a negative regression below.

## 1. Pure cycle contract — SYNAPSE

Files: `integration_brain/core.py`, `integration_brain/__init__.py`, `tests/test_integration_brain.py`.

Interface: `build_cycle(snapshot: dict) -> dict`. Verify exact manifest bytes and Git blob, declared repository coverage, clocks, head stability, source claims, anchor identities and CI observations. Emit `SNAPSHOT_VALIDATED`, `INCOMPLETE` or `RESTART_CYCLE_REQUIRED`; always preserve metadata-only, system readiness unverified and disabled execution/automatic merge authority.

- [ ] Capture failing cases for missing/duplicate repositories, wrong manifest digests, future clocks, incomplete pagination, source conflicts, drift and unstarted CI.
- [ ] Implement pure validation and bounded handoff generation.
- [ ] Run focused tests and obtain a separate science/authority review.

## 2. Pinned collection — HERMES

Files: `integration_brain/transport.py`, `tests/test_integration_brain_transport.py`.

Interface: `collect_snapshot(client=None, cycle_id=None) -> dict`. Read only GitHub metadata and canonical public anchors; use fixed API routes and bounded authorized transport. Derive reservations from the pinned source sessions/events/summaries through the existing compiler. Never use a stale generated board as sole write authority.

- [ ] Capture failing controls for unsafe routes, incorrect Git blobs, pagination, transport errors and resource limits.
- [ ] Collect all declared repositories concurrently, preserve exact revisions and missing/inaccessible evidence, then re-read heads.
- [ ] Run mocked transport tests and one actual bounded metadata cycle; distinguish capture from product/runtime qualification.

## 3. Worker runtime and handoff — Icarus 2

Files: `coordination/icarus2/worker.json`, this design/plan, `integration_brain/__main__.py`, `tests/test_icarus2_cli.py`, `docs/icarus2-integration-brain.md`.

- [ ] Publish the worker identity and immutable source-pinned first cycle with exact readback.
- [ ] After successful GitHub connector preflight and duplicate-task check, create one enabled recurring scheduled-agent task in America/Chicago. Record returned ID/state; never manufacture a successful future run.
- [ ] Scheduled work checks owner stop state and current claims, spawns available bounded swarms, fixes confirmed unreserved defects on reviewed branches, and persists exact evidence. It cannot mutate its own schedule or activate trading/release authority.
- Deferred: the earlier manual/PR workflow draft is excluded from this cycle because the current owner instruction prohibits editing worker automation or schedulers.
- [ ] Test CLI/output behavior and workflow boundaries, then run the complete owning repository suite.

## 4. Independent cross-review and transition

Artifacts: `coordination/icarus2/swarm-inputs/*.json`, immutable cycles and central session events.

- [ ] VERITAS reviews source authority and role boundaries; KEPLER reviews operational/CI interpretation; MNEMOSYNE reviews temporal/evidence semantics.
- [ ] Fix newly demonstrated internal defects and re-review; retain exact external blockers.
- [ ] Push a concrete review PR and state separately what is scheduled, locally verified, on a branch, on main and observed running.
- [ ] Handoff integration findings to Icarus 1 without modifying his reserved files. Preserve previous stopped work as-is.

Success establishes a recoverable recurring worker. It does not certify all Icarus requirements, an owner-PC restart, production deployment, licensed data access or profitability.

## Verified continuation checkpoint

The bounded cycle `icarus2-20261020T225043Z` resumed this work after runtime interruptions. It preserves the established worker identity and does not alter worker controls, its schedule, or any workflow. The review branch is `icarus2/federation-verification-20261021`; the original setup checkout remains preserved.

Meaningful failing regressions reproduced the GitHub CLI hostname error, numeric Actions pagination mismatch, absent final-head receipt crash, aggregate-only CI false success, and future-cycle acceptance. Repairs passed 113 focused tests and independent review. The clean owning-repository suite passed 170 tests and 8 subtests. Local coordination validation covered 212 events, 42 sessions and 24 summaries at the tested source revision; later source records require their own fresh validation.

Two actual bounded read-only captures observed all six declared repositories and 22 evidence anchors. The repaired capture used 357 GitHub reads, no provider requests, and retained eight explicit gaps, including the five-page history limits and actual Divine Providence CI failure. Open PR pagination completed. Subsequent source drift and interrupted specialist audits remain explicit in the immutable cycle receipt; this is not complete federation health or restart certification. Publication and its exact readback are recorded separately in that receipt and central handoff.
