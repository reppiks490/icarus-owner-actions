# Icarus task review and first repair tranche — 2026-10-17

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
