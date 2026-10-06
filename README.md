# ICARUS owner action register

This private repository is the human-side checklist for the ICARUS research and
paper-trading system. It is separate from the engine code. It does not authorize
live orders, certify an ML candidate, or promise a win rate.

**Start here:** [OWNER_TASKS.md](OWNER_TASKS.md). The exact chart/export request
is in [EXPORT_MATRIX.md](EXPORT_MATRIX.md); optional subscriptions and account
choices are in [PROVIDERS_AND_COSTS.md](PROVIDERS_AND_COSTS.md).
For cross-repository workflow health, machine-readable assurance artifacts, and
the current private-runner blocker, see
[WORKFLOW_ASSURANCE_REGISTRY.md](WORKFLOW_ASSURANCE_REGISTRY.md).

For click-to-complete checkboxes, use [Owner action checklist #1](https://github.com/reppiks490/icarus-owner-actions/issues/1).

## The next three things

1. Record the **exact TradingView chart and strategy configuration** used for
   the 20-minute NQ result, including Heikin Ashi and its **fill mode**.
2. Export matching **20-minute Heikin Ashi and standard OHLC chart CSVs**, plus
   the Strategy Report trade list and property/input settings. Keep both price
   streams: HA is the signal chart; standard OHLC is the real-fill reference.
3. Check whether the NQ chart says **Data is delayed**. If it does, choose a
   real-time exchange-data entitlement or a qualifying broker-data verification
   before expecting a low-latency live feed. A TradingView alert is near-real-
   time only relative to the data that TradingView itself receives.

Do not buy a data feed or open a broker account just to satisfy a checklist.
The research and parity tasks come first. Paid choices are explicitly optional
until their prerequisite is met.

## What belongs where

| Item | Destination |
|---|---|
| Checkmarks, decisions, nonsecret screenshots, links | This repository |
| Raw TradingView/market-data CSVs, xlsx, recordings | Local private folder; share only through an authorized channel |
| API keys, passwords, webhook tokens, broker credentials | Local secret manager or local `.env`, never GitHub or a chat |
| Engine code, models, candidate audits | `reppiks490/Icarus`, separate from this register |

This repository intentionally excludes raw data and account secrets. Even a
private GitHub repository is not a substitute for checking market-data license
terms. Do not assume a chart export may be redistributed.

## Status language

- **Required for parity**: without it, we cannot compare the engine with your
  validated TradingView run on equal terms.
- **Required for paper futures**: needed before testing actual futures orders.
- **Optional research**: may improve evidence, but is not a proven edge.
- **Deferred**: do not enable until the preceding gates pass.

Checked against official provider documentation on 2026-09-23. Prices,
entitlements, contract symbols, API policies, and prop-firm rules can change;
verify again before purchasing or connecting anything.

Prepared by CA / Codex, 2026-09-23.

## Key source documents

- [TradingView chart export](https://www.tradingview.com/support/solutions/43000537255-how-to-export-chart-data/)
- [TradingView Strategy Report export](https://www.tradingview.com/support/solutions/43000613680-how-to-export-strategy-data/)
- [TradingView Heikin Ashi fill modes](https://www.tradingview.com/support/solutions/43000786181-broker-emulator/)
- [TradingView exchange-data purchases](https://www.tradingview.com/support/solutions/43000471705-how-to-purchase-additional-market-data/)
- [TradingView webhooks](https://www.tradingview.com/support/solutions/43000529348-how-to-configure-webhook-alerts/)
