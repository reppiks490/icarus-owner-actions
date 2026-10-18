# Integration co-lead audit handoff — 2026-10-18

Root session: `codex-20261017-hub-integration-lead`.
Recipients: `codex-20261017-task-inventory-start` and `codex-20261018-dashboard-integration-audit`.
This is an evidence handoff, not a claim on the recipients' dashboard/account paths.

## Ownership and immediate work

Root retains Divine Providence runner/tour lifecycle PR59 and complete GRU PR353+387+399 integration. Peer task-inventory reserves workspace/backend/account-connection files. Dashboard-integration-audit has proposed a revised A200/P&L split in Icarus452 comment6248248774. Obtain explicit mutual cooperation or refine targets before overlapping source edits.

The four recordings' recovered intent includes IBKR, ProjectX/TopstepX, Tradovate and TradeLocker demo transports; Apex, Lucid, Goat Funded Futures and MyFundedFutures rule profiles; Rithmic/CQG and Tastytrade were follow-up proposals. These are recovered intended scope, not proof of implemented or authorized accounts.

## Reproduced P&L defects

Audit pinned to Icarus main `c993130534126a352c766fb7abc0de3145fc110f`; no existing checkout was edited.

- Four configured profiles with no runtime return realized/open totals of zero, conflating unavailable results with an empty valid ledger.
- Running the actual header function in Node accepts four duplicate profile IDs, stale marks and mixed EUR/USD values as a dollar total.
- HTTP failure invalidates the global header while the existing deck can retain old figures. Hung requests have no timeout/last-success expiry.
- Current combined-P&L test passes (1 passed, 68 deselected), demonstrating missing coverage.
- Combined numbers are paper closure profit plus emulator marks, not broker account P&L. Preserve this distinction.
- Saved workspace asset selections are overwritten by defaults. A200 is not in normal workspace runners/asset pickers; its historical research consumer discards strategy commands.

Recommended boundary: a pure `paper_pnl.py` four-ledger contract plus shared UI presentation. Require exact unique cc1–cc4 IDs, finite values, runtime availability, accounting currency, observation times and explicit partial/stale reasons. Retain known realized P&L while withholding a complete combined total if any required component is unavailable or incompatible. A flat position may validly have zero unrealized without a mark. Do not add currencies without verified conversion.

Existing inputs: journal `realized_pnl/closed_pieces/last_close_ts`; status `now/view_stale`; per-asset `price/price_age/last_bar_ts/poll_age/feed_delay/market.open`; position/open trade `upl/open_profit`. Currency is absent from existing workspace/AssetSpec P&L contracts and must be established, not assumed. Test missing runtimes, valid empty ledgers, duplicate/missing IDs, stale open vs flat positions, currency conflicts, nonfinite input, replay exclusion, delayed/out-of-order responses, failure and expiry.

## Futures expansion research

Engine already has32 catalog families while the audited Icarus main had16 runtime roots; open convergence work must be integrated before counting new additions. Preliminary ten genuinely new families beyond that32-root set: ZM soybean meal, ZL soybean oil, LE live cattle, HE lean hogs, 6C Canadian dollar, 6S Swiss franc, Ether futures (distinct identity from spot ETH), RB gasoline, HO ULSD, KE Kansas City wheat.

Micro candidates include MZM/MZL/MET and micro-CAD/micro-CHF, but every alias, multiplier, currency, price scale, expiry and roll requires official product verification before runtime qualification. CME micro agriculture has distinct settlement/expiry; do not copy parent roll rules. Official FX expiry differs:6C one business day before third Wednesday versus6S two days.

Public Yahoo chart probes returning FUTURE prove reachability only. They do not prove automated-use or redistribution rights; Yahoo terms expressly restrict automated collection absent permission: https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html. CME delayed quotes likewise are not a general license grant. Investigate legitimate existing-account delayed API access, licensed retained history and explicit provider terms. Do not purchase entitlements, claim every family has a micro, or infer profitable strategy performance from liquidity/catalog presence.

## Prop-firm safety findings requiring source-specific rules

These are preliminary official-source findings; bind each to the exact program, account stage, platform, effective date and reviewed source before enforcing.

- Apex official prohibited-activities page says “No Automation or Algorithm Usage allowed”: https://apextraderfunding.com/help-center/getting-started/prohibited-activities/ . Default manual/read-only until applicable program permissions are verified. Legacy vs new EOD/Intraday programs have different drawdown and platform treatment; a single generic Apex policy is invalid.
- TopstepX/ProjectX documentation describes API subscription/key requirements, application-body success/errorCode checks even after HTTP200, expiring JWTs and agreement/firm-disabled states. Current Topstep help describes simulated API access and remote-order/VPS/VPN restrictions. A successful generic ProjectX login does not establish per-firm or live-funded API permission.
- Goat's official trading-rules FAQ has program-specific bot permissions (some plans manual-only), news restrictions and conflicting older/newer sections. Conflicting source evidence must require review rather than silently selecting a permissive rule.
- Discover actual supported account/programs; never equate a transport adapter with prop-firm authorization. Keep read-only/manual configuration independent from order arming.
- FAQ-derived rules need versioned provenance and tests; non-machine-verifiable terms require an explicit review/acknowledgment state, not a false automated PASS.

## Current verified hub evidence

PR59 `ee8d91ba` passed Linux/Windows3.11 lifecycle and full twelve-system validation. Diagnostic head `47e419dd` passed lifecycle matrix3.11/3.13 and subsystem validation, but full Windows bootstrap failed its timed-marker fixture. Diagnostics prove marker time432270158500 occurred BEFORE runner return432279813700 (run0.91s). This does not prove an after-return orphan. Root is replacing that fixture with an explicitly detached-output child, startup handshake and actual process-exit check; merge remains gated on complete CI.

No broker arming, provider purchase, canonical holdout experiment or production model promotion is authorized by this note.
