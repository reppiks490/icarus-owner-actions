# Icarus task review and first repair tranche — 2026-10-17

## Continued three-worker pass

Owner direction: continue across the federation; only this worker and two other agents are currently working. Historical stale sessions are stopping points, not permanent reservations. This worker retains inventory and futures verification; the active hub/GRU peer's reserved files remain separate. No extra worker was spawned.

The initial compiler blocker below is now **resolved on main** by owner-actions PR #47. Current-main validation at `7196802bac0bb064f0e3b2752faf4e4791c0f957` passed with 143 events, 35 sessions and 22 summaries; all 52 governance tests passed. The original malformed records remain preserved. PR #49 also carries the offset cron regression. Do not rebuild these repairs from the historical list.

Icarus PR #447's exact-head hosted run `39078186866` completed successfully at `a9217cc16086130a30883162903bccb3f67e9357`. It remains unmerged; successful tests do not override the control-plane requirement for a separate merge decision.

The [refreshed PR audit](../current-pr-audit-20261017.json) covers all 35 open federation PRs returned by the user-scoped query at the observation time, including head SHAs, branch relationships, draft state, and exact-head PR-triggered workflow results. The tool exposes only the first workflow page; no missing workflow is silently treated as green. Historical failing runs remain failures even where main now contains a repair.

The stopped futures stack is being consolidated on `codex/futures-convergence-review-20261017`: #438's paper-readiness correction, #432's Databento tests, #435's calendar coverage, current main, and #447's deterministic fixtures. A confirmed Brain evidence defect accepted truthy strings as decision authorization and false-like non-booleans as disabled execution. Fifteen failing regression cases reproduced before strict checks were added; all 30 Brain evidence tests and 167 focused stack tests now pass. The consolidated draft is [Icarus #450](https://github.com/reppiks490/Icarus/pull/450), head `4f6ef403ab187bccb57a64800638a8675a1af128`. Full local code verification at `a017008717d4ed130e9bfe58edb55e7d127a828f` passes **2,975 tests and 111 subtests**, with 3 skips, in 147.46 seconds; later changes add documentation and seven omitted modules to the Windows test command (110 cases collected), without changing runtime Python. Hosted exact-head run `39079800021` **passes on Linux and Windows**, including the expanded Windows module list. Independent semantic review and the separate merge decision remain pending. This evidence contract currently has no production caller; contract tests are not source-to-runtime integration proof.

An exact-head cross-repository finding was handed to the hub peer: Divine Providence PR #59's Observatory run `39078762673`, Windows job `117531250781`, failed `test_successful_suite_does_not_leave_windows_descendant` (1 failed, 174 passed, 1 skipped), despite its separate lifecycle run passing. Preserve that failure until the peer resolves it; do not claim whole-Windows containment from the narrower green workflow.

[Owner-actions #51](https://github.com/reppiks490/icarus-owner-actions/pull/51), head `1837a3ae7827c901377b6c413a857f5d600a8199`, fixes the misleading active-worker headline: 3 current sessions, 11 stale/reclaimable, 14 non-terminal total. It preserves machine fields and unfinished history. Its failing-first regression and all 53 local governance tests pass; hosted run `39079763194` succeeds. It is not yet merged.

The initial observations below remain a dated record. Their old compiler-blocked and hosted-pending states are superseded by this continuation.

## Initial inventory

The source-pinned [inventory](../task-audit-20261017.json) includes every one of the 202 mission requirements, all 19 owner-checklist tasks, all 46 task-table entries on the three legacy Engine boards, and 30 open federation PRs observed before this tranche. These sources overlap; their counts must not be added as unique tasks. Every baseline requirement keeps its original reported state. None is newly certified by this inventory.

## Work delivered

- Published the central session and PLAN/CLAIM records before editing.
- Reproduced two positive listing-crosswalk failures and five positive research-runtime failures against Icarus main `335148c8d911f3320b5bde1ed77b38df1ba9704e`. Dated listing evidence had expired against the wall clock.
- Published [Icarus PR #447](https://github.com/reppiks490/Icarus/pull/447), head `a9217cc16086130a30883162903bccb3f67e9357`: freeze the listing test clock and provide explicit synthetic listing identity in the qualified research fixture. Added missing/stale/mismatched identity rejection checks. Runtime authority and freshness policy are unchanged.
- All 26 focused tests pass. Syntax compilation and diff whitespace checks pass. Remote branch files match the tested local files byte for byte.
- Full local Linux application regression: **2,890 passed, 3 skipped, 111 subtests passed**, in 138.57 seconds with CI ML/bridge/Databento extras installed. This is not independent Windows/browser visual verification. Isolated Plant setup, control CLI help and doctor smoke checks pass; doctor has zero failures and two clean-worker warnings.
- All 47 governance tests pass. Mission register validation passes; its offline certificate still reports zero declared VERIFIED or INTEGRATED requirements and does not certify the system.

## Remaining work and exact continuation

1. Restore the central coordination validator/compiler. Five immutable event records from the pointer-contract session have schema drift; its summary also lacks required fields. The first actual tree-validation failure is `unknown event type None` at `20261016T131600Z-claim.json`. The inventory lists all six record errors. Preserve the original event bytes. Publish a narrow claim before a compatibility/migration implementation, and test that malformed or ambiguous repository targets cannot silently acquire reservations. PR #19 at `2bb9e8ed901f0ca5f07ec46f1efcfbf409a37019` only changes a scheduling test; it does not repair these records.
2. Read final hosted verification before considering merge. The complete local application suite now passes with the workflow's ML and Databento extras installed. The initial local run omitted those extras; its environment-related failures were resolved by installation, not product changes. Hosted tests for PR #447 are run `39078186866`; require their final outcome before considering merge. No merge was performed in this tranche.
3. Review the remaining open PRs against their actual current heads, dependencies and draft boundaries; do not merge stale alternatives merely to empty a queue. The 46 historical board rows retain reported status, not fresh independent completion credit. Central model-neutral coordination supersedes old model ownership restrictions.
4. Reconcile the 202-requirement evidence index with newer merged implementations one bounded component at a time. DISCOVERED in this older register means evidence closure remains unverified; it does not prove the implementation is absent. Acceptance belongs to the original package and actual consumer contract.
5. Reclaim research tasks only after checking current main/PRs, authorized data, preregistration, protected splits and the global trial ledger. Preserve D1's authentic-data prerequisite. Broker connection work remains excluded.

The owner checklist reports O01–O06 checked; their original proofs were not independently re-audited here. O07–O19 remain unchecked. Account, entitlement, risk, rights and execution decisions must not be marked complete by an engineering test.

The checked-in provider ledgers and Sentinel were consulted as dated evidence, not proof of current API access. No provider collection, purchase, licensed-data export, scheduler change, broker connection or execution activation was performed. The historical Drive governance capsule defers to newer repository truth; archived sibling-build claims are not imported as Icarus verification.

This completes the initial inventory and begins repairs. It does not complete all Icarus tasks.

## Current continuation boundary

The canonical repository registry was read at Engine `2680123fa0245b8d8f740febc01f2d92afb89cfb`; it identifies the six repositories covered by the PR audit. The connected twelve-system hub remains the active peer lane. No claim is made that all 202 requirements, all external provider access, or every connected subsystem is complete.

Implementation and fresh automated checks are delivered for the current root-worker repairs. Continue with independent review of Icarus #450, review of owner-actions #45/#51, and the hub peer's Windows containment repair. `Icarus:coordination/CONTROL_PLANE_CONTRACT.md` requires a separate authorization for merge/release; this pass does not infer that decision from green CI. The research snapshot still has no qualified champion. Preregistration #137 and draft #142's explicit approval/merge and leakage-review gates remain prerequisites before any real frontier experiment. No gate was relaxed to manufacture completion.
