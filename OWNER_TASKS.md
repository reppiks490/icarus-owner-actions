# Owner tasks

Check a box only after its **proof to provide** is available. `P0` tasks are
needed for like-for-like parity; `P1` tasks come before live paper futures;
`P2` tasks are optional research or later execution preparation. Monetary
amounts are not approvals to spend.

## P0: identify the validated strategy and its data

- [ ] **O01 - Freeze the reference run (free).** On the exact NQ chart that
  produced the result you trust, record the Pine script name/version, current
  code text or a file hash, `NQ1!`/contract ticker, `20m`, exchange timezone,
  chart timezone, Heikin Ashi chart type, RTH vs ETH, continuous-contract
  adjustment/roll setting, and the visible date range. Do not silently switch
  from the 20-minute customized run to the older 10-minute test. **Proof:**
  screenshots of the chart header, symbol/session settings, and script name.
- [ ] **O02 - Freeze all strategy inputs and properties (free).** Open the
  strategy settings and record every changed input, order size, initial
  capital, commission, slippage, pyramiding, margin, limit-fill rule, bar
  magnifier/detalization setting, execution delay, and Heikin Ashi mode.
  On HA, explicitly capture whether fills use **Heikin Ashi bars** or
  **Standard bars**. Both reports are useful, but they answer different
  questions. **Proof:** a complete screen recording or screenshots that show
  every settings group, with no cropped values.
- [ ] **O03 - Export the NQ parity packet (free or current TV plan).** From
  the **same symbol, session and time span**, download the 20m HA chart CSV,
  20m standard OHLC CSV, Strategy Report **List of trades** CSV, and the
  performance summary. Also export standard 1m, 5m, 60m, 240m and daily
  chart data as available; scroll the chart left to load older history before
  export. Follow [EXPORT_MATRIX.md](EXPORT_MATRIX.md). **Proof:** filenames,
  first/last timestamp, row count, SHA-256 hashes. Do not edit the raw files.
- [ ] **O04 - Export a second, real-fill comparison run (free).** Keep the
  same HA signal chart and inputs but select **Standard bars** as the HA
  execution-price mode. Export its List of trades and summary separately.
  Keep the original synthetic-fill result too; label both. Do not interpret
  the synthetic-fill report as broker-achievable P&L. **Proof:** both reports
  with the settings screenshot for each.
- [ ] **O05 - Confirm session behavior (free).** On NQ 20m, note whether
  the first bar is 08:30 CT (RTH) or an overnight bar (ETH). Export one
  complete regular trading day and one holiday/early-close day if available.
  TradingView documents RTH and ETH as different intraday data streams.
  **Proof:** chart CSV and session-toggle screenshot.
- [ ] **O06 - Preserve raw data provenance (free).** Keep the CSVs in a local
  private folder. Use the command in [EXPORT_MATRIX.md](EXPORT_MATRIX.md) to
  generate a checksum manifest, and provide the manifest without altering
  CSVs. **Proof:** manifest plus the original files through a permitted,
  private channel. Do not commit licensed CSVs to this repository.

## P1: remove the 10-minute feed lag and prepare paper futures

- [ ] **O07 - Check the chart's exchange-data entitlement (may cost money).**
  On each futures chart, click its market-status/`Data is delayed` label and
  inspect the needed exchange package (CME, CBOT, COMEX, NYMEX as applicable).
  In TradingView, avatar -> **Settings and billing** -> **Subscriptions** ->
  **Real-time market data** is the other route. If a supported broker already
  carries the entitlement, verify it in TradingView's **Trading Panel** before
  buying duplicate access. Record whether each chart is real-time. This
  removes the exchange's ten-minute delay; it cannot remove bar-close time,
  network latency, or webhook delivery failures. **Proof:** the chart status
  for NQ, ES, YM, GC, SI, PL, PA, BTC futures.
- [ ] **O08 - Choose the live-bar source (decision, possible cost).** Preferred
  low-friction research path: TradingView **closed 1-minute standard bars**
  over a secure HTTPS webhook, preserving the exact chart/exchange/session
  identity. Alternative: a licensed direct futures feed with timestamped
  trades and bars. Decide only after comparing price, license, coverage,
  latency, and connection reliability in
  [PROVIDERS_AND_COSTS.md](PROVIDERS_AND_COSTS.md). **Proof:** chosen source,
  entitlement, exchange list, and measured event-to-receipt lag. No source
  guarantees literally zero latency.
- [ ] **O09 - Enable the TradingView webhook only after the endpoint is ready
  (current plan may be required).** Turn on TradingView two-factor
  authentication. With the engine in **shadow/paper-only** mode, create a
  one-minute **bar-close** alert for each required chart using the reviewed
  JSON payload and HTTPS endpoint. TradingView accepts destination ports 80
  and 443 and can occasionally miss delivery. Do not put broker keys or
  passwords in the alert body. In the alert log, inspect the **Webhook
  status** column and compare received bar timestamps to the chart.
  **Proof:** a redacted alert screenshot and a 1-hour latency/gap report.
- [ ] **O10 - Recreate stale strategy alerts after any change (free).** A
  TradingView strategy alert keeps a server-side snapshot of the code and
  settings at alert creation. Editing the chart later does not update it.
  Delete and recreate each alert after changing the script, inputs, symbol,
  timeframe, or session. **Proof:** alert creation time/version recorded.
- [ ] **O11 - Pick an actual futures paper venue (broker account may be
  required).** Alpaca's published asset list covers US securities/options
  and crypto, not CME futures; its QQQ proxy is **not** an NQ fill. If you
  want NQ, metals, ES, YM and BTC futures paper fills, choose a broker or
  platform offering these actual contracts, an accessible paper API, and
  exchange entitlements. IBKR is one documented option, but its paper
  account depends on an approved live account and mirrors its permissions
  and market-data subscriptions. Do not create live API credentials yet.
  **Proof:** broker name, paper-account status, supported contracts, API
  terms, exchange data status, fee/margin schedule.
- [ ] **O12 - Record prop-firm automation rules before connecting one
  (possibly paid).** If a prop firm is intended, ask it in writing about
  API/third-party automation, copy trading, news trading, overnight holds,
  daily loss, trailing drawdown, order-rate limits, permitted contract sizes,
  and data rights. Do not route orders until the rules and paper parity are
  reviewed. **Proof:** current rules and written permission/terms.
- [ ] **O13 - Set paper risk approvals (decision).** Choose a **single
  portfolio** starting equity, per-asset risk cap, aggregate open risk,
  allowed sessions, flat-on-disconnect behavior, daily loss guard, and
  contract-count ceiling. Confirm micro contracts are separate instruments.
  The engine's historical per-asset capital figures are not a shared
  brokerage balance. **Proof:** signed risk sheet, then paper-only order
  reconciliation across several sessions.

## P2: broader evidence, optional purchases, later authorization

- [ ] **O14 - Export the wider asset matrix (time; maybe exchange fees).**
  Work through [EXPORT_MATRIX.md](EXPORT_MATRIX.md) in priority order.
  Execution assets and micro contracts need their **own** OHLCV and contract
  metadata. Context symbols (stocks/ETFs/rates) are sensors only, never
  futures execution prices. Avoid re-downloading byte-identical files.
  **Proof:** source/ticker/venue/session/timeframe/date-span manifest.
- [ ] **O15 - Decide whether true order-flow research merits a paid feed.**
  TradingView chart CSV OHLCV cannot reconstruct market-by-order queues,
  cancellations, iceberg attribution or precise depth. If this is a priority,
  obtain licensed CME trades + level-2/level-3 MBO history and live access,
  specify product/contract/time range, and check export/retention rights.
  Databento and CME DataMine are examples, **not** purchases requested now.
  **Proof:** provider quote, schema sample, license, timestamp quality.
- [ ] **O16 - Supply macro and company-event records (mostly free).** Use
  primary released-time sources for FOMC, CPI, payrolls, PPI, PCE/GDP and
  SEC company filings, not a retrospectively revised value without its
  original publication timestamp. A mere list of future event dates is
  insufficient to train event reactions. **Proof:** event ID, announced-at
  timestamp/timezone, original value, revision, source URL/version.
- [ ] **O17 - Supply loss and execution journals (free).** For each paper
  trade, retain decision time, candidate/config ID, known features at that
  time, chosen action, order/ack/fill timestamps, prices, fees, slippage,
  session, roll, and eventual outcome. This lets a separate failure-analysis
  model study **causes** without training on future information or merely
  banning losses. **Proof:** sample redacted ledger and reconciliation.
- [ ] **O18 - Review data rights and privacy before sharing (decision).**
  Check each provider's personal-use, API, derived-data, retention and
  redistribution rules. Keep this repository private and free of keys and
  market-data dumps. **Proof:** license/plan name and permitted use noted.
- [ ] **O19 - Explicitly approve any transition beyond shadow mode.** Only
  after source freshness, parity, broker-paper fills, risk stops, kill switch,
  restart/recovery, and independent review pass should an operator consider
  any live mode. This checklist is **not** that approval. **Proof:** a
  separate dated decision and go/no-go report.

## Known exclusions

The currently approved traded set is NQ, ES, YM, GC, SI, PL, PA, CME BTC
futures (`BTCF`) and spot BTCUSD at a **named exchange**. MBT, SOL and ETH
are excluded by owner instruction. Do not treat an asset's context data as
an authorized traded symbol.

## Official references

- [Chart export](https://www.tradingview.com/support/solutions/43000537255-how-to-export-chart-data/), [Strategy Report export](https://www.tradingview.com/support/solutions/43000613680-how-to-export-strategy-data/)
- [Heikin Ashi price modes](https://www.tradingview.com/support/solutions/43000786181-broker-emulator/), [RTH/ETH futures sessions](https://www.tradingview.com/support/solutions/43000670909-regular-and-electronic-trading-hours-for-cme-futures/)
- [Market-data purchase/verification](https://www.tradingview.com/support/solutions/43000471705-how-to-purchase-additional-market-data/), [broker entitlements](https://www.tradingview.com/support/solutions/43000479666-how-can-i-get-real-time-data-from-exchanges-that-i-have-already-purchased-with-my-broker/)
- [Webhooks](https://www.tradingview.com/support/solutions/43000529348-how-to-configure-webhook-alerts/), [strategy-alert snapshots](https://www.tradingview.com/support/solutions/43000481368-strategy-alerts/)
- [Alpaca supported classes](https://docs.alpaca.markets/us/docs/about-alpaca), [IBKR paper account](https://www.interactivebrokers.com/campus/trading-lessons/how-to-open-an-ibkr-paper-trading-account/)
