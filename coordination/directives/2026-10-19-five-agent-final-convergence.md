# Five-agent final convergence directive — 2026-10-19

Owner-authorized final convergence now uses five named agent lanes. The selection board is GitHub issue #59 in `reppiks490/icarus-owner-actions`.

## Selection board

- VERITAS — issue #54 — system authority, contradictions, lifecycle, PR truth.
- ARGOS — issue #55 — data, APIs, credentials, entitlement, corpus utilization.
- KEPLER — issue #56 — futures, market structure, historical contamination, execution qualification.
- MNEMOSYNE — issue #57 — Brain, ML, research integrity, evidence-to-decision lineage.
- SYNAPSE — issue #58 — final integration, release convergence, reset/recovery manifest, Claude handoff.

Each incoming agent must choose exactly one unclaimed role in #59, check that role there, check the `CLAIM <NAME>` box in the corresponding role issue, then comment its `session_id`, model/account, UTC claim time, and exact base SHAs. The agent must also create/resume its coordination session and publish a `CLAIM` or `PLAN` event before mutating code or shared state.

## Inheritance rule

Claiming a name inherits the entire role issue, including later-discovered work inside that scope. The role remains inherited until `COMPLETE`, explicit `HANDOFF`, owner reassignment, or a documented external blocker. A role may not be silently partially claimed.

## Mandatory iterative closure rule

Every delegated task follows the same cycle:

1. primary review against current exact-head source/runtime evidence;
2. fix every internal error or gap found that is safe and non-conflicting;
3. re-review from scratch without trusting the first pass;
4. actively hunt for second-order misses, stale assumptions, hidden branches, edge cases, authority leaks, and regression paths;
5. fix all newly found internal defects;
6. adversarially review the repaired result and attempt to falsify the success claim;
7. cross-review dependencies with the neighboring agent lane;
8. verify with focused tests plus all applicable full CI/runtime receipts and exact SHAs;
9. close only after two consecutive review passes reveal no new material internal defect.

A newly discovered material defect automatically reopens the affected task and repeats the cycle. Existing code, one passing test, or one reviewer opinion never satisfies completion by itself.

## Cross-agent mesh

- VERITAS challenges authority/supersession/lifecycle claims from all lanes.
- ARGOS and KEPLER cross-check provider symbols, data readiness, entitlement, and transport.
- ARGOS and MNEMOSYNE cross-check whether collected data is actually consumed.
- KEPLER and MNEMOSYNE cross-check instrument economics, historical-result contamination, and evidence lineage.
- SYNAPSE consumes all specialist handoffs, arbitrates evidence conflicts, and reopens the responsible specialist issue if integration exposes a new material defect.

## Global completion gate

The phase is not complete until all five role issues satisfy their exit criteria, every discovered internal object/gap has a final classification/action, every open PR/workstream has a disposition, internal CI/Sentinel/runtime defects are fixed or reduced to exact external blockers, the canonical reset/recovery manifest is complete, and the final Claude Code handoff is reproducible from exact SHAs without this chat.

Constraints remain unchanged: no live broker arming, no new spend without explicit owner authorization, no plaintext secret exposure, and no restricted raw-vendor-data publication.
