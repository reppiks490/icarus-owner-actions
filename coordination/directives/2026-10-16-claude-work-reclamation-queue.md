# Claude inactive-work reclamation queue — 2026-10-16

Owner direction: Claude is inactive for approximately one to two months with no fixed return date. Model-specific ownership is superseded by the central coordination bus. The items below were read from `reppiks490/Icarus-engine/coordination/board/claude.md` on 2026-10-16. They are **not automatically complete** and they are **not reserved to Claude**.

Before claiming any item, read the current repo/main, open PRs, `coordination/ACTIVE.md`, and `coordination/collisions.json`; publish a repo-qualified `CLAIM` event before mutation. If later work has already satisfied a requirement, verify it and publish evidence instead of rebuilding it.

## Reclaim now after collision/relevance check

| Legacy ID | Work | Reclamation guidance |
|---|---|---|
| L1 | Move public `data/panel/*.csv` raw vendor ETF bars into the encrypted vault | Security/licensing priority. Do not delete first. Prove encrypted/private destination integrity and recoverability, then remove public copies through a reviewable PR. |
| C2 | Win-rate frontier: win rate vs expectancy over TP/SL/time-stop per setup against random-entry null | Research/evaluation lane. Require leakage-safe splits, cost model, null distribution and reproducible receipts. |
| P1 | Shadow trader: forward paper trades of noise-boundary rule on MNQ | Paper/shadow only. Live arming remains prohibited. Fix MNQ contract identity/multiplier before relying on P&L. |
| C4 | Regime cartographer: ex-ante regime labels and rules active today | Keep regime labels causal/ex-ante; publish feature timestamps and no-lookahead tests. |
| C3 | Meta-labeler: take/skip model on Icarus entries | Require out-of-sample evaluation, probability calibration, leakage checks and explicit abstain behavior. |
| I1 | Red team every claimed result for look-ahead, Heikin-Ashi fills, roll jumps and cost stress | High-value independent validation lane; do not modify the candidate merely to make the audit pass. |
| I2 | Fragility scanner: 1,000 small perturbations per setup | Make perturbation distribution explicit, deterministic under seed, and summarize failure surfaces rather than only pass/fail. |
| R1 | Claims referee: ledger of every AI claim checked against repo/CI evidence | Strong fit for the central coordination/evidence plane. Prefer machine-verifiable links/SHAs/run IDs. |
| T6 | Optional-dependency test skips and cleanup | Audit current CI first; make skips explicit and justified rather than masking missing required dependencies. |

## Reconcile before doing new implementation

| Legacy ID | State | Required first action |
|---|---|---|
| X1 | Claude ↔ ChatGPT two-agent coordination was `in progress` | **Superseded in architecture** by the model-neutral many-chat bus in `icarus-owner-actions`. Preserve old mailbox/boards as historical evidence; do not rebuild a two-agent gate. Reconcile any useful old tooling (`tools/coordination.py`) into the new bus only if it adds verified capability. |
| CL-84 | Port PR #84 Databento guards was `in progress` on `claude/cl84-port` | Inspect Icarus-engine PR #84, PR #140 and current `main` first. The 2026-10-16 ingestion closure merged to main as `20616cce0ac5c30d05750fdb53169800f75cb3b6`; several credential/data-policy changes may supersede or alter the old port. Do not duplicate/delete newer protections. |

## Externally/data blocked

| Legacy ID | Blocker | Parallel work allowed |
|---|---|---|
| D1 | Order-flow test D1 waiting for 20 vaulted NQ MBP-10 days | Verify whether the required vaulted corpus now exists. If not, keep the experimental preregistration intact, improve validation/tooling that does not require the missing rows, and publish the exact data blocker. Do not fabricate depth/order-flow evidence. |

## Already marked done on the legacy board

S1 data-health sentinel, C8 daily phone briefing routine, R2 `ICARUS_STATE.md`, F1 ALFRED vintages and F2 SEC EDGAR fair-access contact were marked done. Future chats may audit them, but must not reclaim them merely because Claude is absent unless fresh evidence shows a regression or unmet requirement.

## Divide-and-conquer rule

Multiple chats may work on different legacy items simultaneously. A large item may be decomposed into research, tests, implementation, UI/evidence and independent review sessions, but each session must reserve narrow repo-qualified targets. Dependencies and useful results should be linked through `HANDOFF`/`UPDATE` events. No chat should stop simply because another chat holds one conflicting file; choose a non-conflicting subproblem or validation lane.
