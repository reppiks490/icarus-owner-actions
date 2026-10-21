# Icarus Prime return — 2026-10-21

Owner direction: Icarus1 is now **Icarus Prime**; stable session remains `icarus1-20261020-system-recovery`. Icarus2 provides focused support. The 40-minute timing refers to the worker returning, not a software-start deadline. No restart is scheduled by this handoff.

## Ready for your review

| PR | Verified result | Scope |
|---|---|---|
| [Engine #226](https://github.com/reppiks490/Icarus-engine/pull/226) `a02c781c` | 10 regressions reproduced; 57 local tests passed; independent review CLEAR; 12 CI checks reported successful | Four files: approved Databento account-budget binding and provider-evidence freshness. Replaces closed #213/#214. |
| [Icarus #463](https://github.com/reppiks490/Icarus/pull/463) `aa6aaf10` | Main reproduced 1 failure/166 passes; repaired selection 167 passed; independent review CLEAR. Hosted engine CI pending at packet creation. | One test fixture; production code/defaults unchanged. Current defaults include CL; the non-expansion test now uses a controlled NQ-only baseline. |
| [Owner-actions #51](https://github.com/reppiks490/icarus-owner-actions/pull/51) `1837a3ae` | Fresh 58 tests plus 8 subtests passed; current source compilation showed 2 current /17 stale /19 nonterminal sessions | Optional headline correction; preserves schema and leases. Recent records do not prove continuous execution. |

## Continue your existing work

Preserve your unpublished renderer/client changes. Latest observed source is `024-core-helper-implementation.json` at 13:53Z; Icarus2 has not inspected your private working tree. Published recovery [#462](https://github.com/reppiks490/Icarus/pull/462) remains `68acaec0`, draft/unmerged with successful existing checks.

A read-only Node probe on that published client rejects `6E`, `6J`, `6B`, `6A` with `INVALID_REQUEST` before transport. This is already your numeric-futures task, not a competing implementation. Finish that, operation receipts/action acknowledgment, and common-renderer parity; publish the exact next head for focused review. Green baseline CI does not certify those unpublished changes.

## PR cleanup already completed

- Closed Icarus #451: bridge source/tests/docs already on main; Windows selection retained.
- Closed Icarus #452: consumer feature already on main; 8/10 files exact, remaining intake code/tests add the optional futures expansion. Original tests preserved. The stale added fixture is handled by #463.
- Parked owner-actions #60 after the owner canceled broad integration loops; branch/code/old receipt remain preserved.
- Closed Engine #213/#214 after consolidating their code/tests onto current main in #226.
- Icarus #456: 20/32 changed files already match your published baseline. Of 12 remaining differences, 10 overlap #462; the other two are legacy dedicated renderer HTML/JS. Preserve unique behavior through parity checks; avoid a wholesale old-branch merge.

## Work state and next action

Icarus2 review worktrees are clean: `/workspace/Engine-restart-guards` on `icarus2/restart-data-guards-20261021`; `/workspace/Icarus-pr452-current-main` on `icarus2/corpus-default-fixture-20261021`. Python/pytest and Node were available for offline checks; your environment must be verified independently. No provider requests, spending, model training, live activation, code-main merge or owner-PC restart was performed.

First review #226 and #463, preserve your current renderer work, then publish its exact head for the next targeted review. Broader research drafts stay parked. The hourly Icarus2 automation is paused and was read back disabled; historical worker configuration is not proof that the old loop is active. Owner-PC runtime and final software restart readiness remain unverified.
