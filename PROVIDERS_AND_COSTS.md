# Data, broker and prop decisions

Checked 2026-09-23 against the linked official pages. Prices and eligibility
change; the owner must verify the checkout page and license **before paying**.
No subscription is required to read this repository. No purchase has been
made on the owner's behalf.

## The actual ten-minute problem

The engine's Yahoo futures source was measured about ten minutes behind the
exchange in the earlier audit. That is not a Python performance problem.
Loading delayed bars faster still produces delayed decisions. These are the
plausible paths, in order of least commitment:

| Path | Owner action | Cost / caveat |
|---|---|---|
| TradingView exchange entitlement + secure bar alerts | Click the futures chart's **Data is delayed** / market-status label and buy the relevant CME/CBOT/COMEX/NYMEX real-time packages, **or** verify an eligible broker data subscription through Trading Panel. Enable 2FA and, only after a reviewed paper endpoint exists, create 1m bar-close alerts. | Exchange fees and TradingView plan limits vary. A bar-close design has up to one bar of waiting plus delivery lag; it is not literally zero latency. Webhooks can fail and require gap monitoring. |
| Massive Futures Advanced direct API | Check current coverage, nonprofessional eligibility and commercial terms; evaluate sample timestamps before subscribing. | [Official page](https://massive.com/pricing?product=futures) displayed **$199/month billed monthly** for Advanced on 2026-09-23, with real-time CME/CBOT/NYMEX/COMEX aggregates, trades and top-of-book. Starter $29 and Developer $79 explicitly say **10-minute delayed**; do not buy them to solve this lag. Advanced is not an MBO/depth replacement. |
| Databento Standard direct API | Request a sample of CME Globex trade/depth schemas, symbol mapping, retention, and licensed use; estimate historical charges. | [Official page](https://databento.com/pricing) displayed **$199/month** for Standard on 2026-09-23, with live data and limited included depth history; additional history is usage-priced. Check actual entitlement, exchange agreements and data redistribution restrictions. |
| Broker-provided real-time data | Verify the intended broker offers the exact futures exchanges, API feed, paper environment and contract-level history. | Broker/exchange data fees, account requirements and professional status vary. A TradingView-only chart data purchase may not populate the broker's order panel; see [TradingView's source warning](https://www.tradingview.com/support/solutions/43000739323-how-does-the-source-of-real-time-data-affect-the-trading-experience/). |

The **highest-priority question** is whether the existing TradingView chart is
already real-time. If the chart itself is ten minutes delayed, its webhooks
will not fix that underlying entitlement. If it is real-time, the secure
TradingView bar-feed route may avoid a second market-data purchase. TradingView
notes that some supported broker subscriptions can be verified in the Trading
Panel and renewed on login: [official list and conditions](https://www.tradingview.com/support/solutions/43000479666-how-can-i-get-real-time-data-from-exchanges-that-i-have-already-purchased-with-my-broker/).

## Webhook setup: owner clicks, after code review

1. Enable two-factor authentication on TradingView.
2. Confirm each source chart is the correct symbol, session, interval and
   real-time exchange data; choose standard 1-minute closed bars for feed
   replay, while keeping the 20-minute HA signal chart as the reference.
3. Use an HTTPS endpoint on port 443 with a private high-entropy path and
   source validation. Never put broker credentials in the webhook JSON.
4. In TradingView's **Create alert** dialog choose the reviewed condition,
   message, **Webhook URL**, expiration, and notification policy. For strategy
   order alerts, select the intended fill/`alert()` condition. A separate
   closed-bar feed alert must send OHLCV rather than merely a trade signal.
5. Send a test to the shadow-only endpoint. Check TradingView **Alert log ->
   Webhook status**, dashboard receipt time, bar UTC time, duplicates,
   missing bars and reordering. Keep the paper engine flat until the
   receiver has passed recovery and authorization tests.

TradingView currently restricts webhook destinations to ports **80/443**, a
request taking over **three seconds** may be cancelled, and delivery can fail.
Its strategy alert is a **snapshot** of code/settings when created; recreate
after changes. Sources: [webhook requirements](https://www.tradingview.com/support/solutions/43000529348-how-to-configure-webhook-alerts/), [strategy-alert behavior](https://www.tradingview.com/support/solutions/43000481368-strategy-alerts/).

## Paper broker or prop-firm choice

**Alpaca is not the CME futures paper broker.** Its current overview lists US
stocks/ETFs, options and crypto, with futures on the roadmap. The original
Alpaca bridge could mirror NQ exposure to QQQ, but that changes the instrument,
session, basis, multipliers and fill mechanics. It is a proxy experiment, not
NQ parity: [Alpaca supported assets](https://docs.alpaca.markets/us/docs/about-alpaca).

If actual futures paper trading is desired, compare brokers by the following
checklist **before** opening/funding an account:

- Exact support for NQ/ES/YM/GC/SI/PL/PA/BTC futures and allowed micros.
- Paper or simulator API availability, authentication and rate limits.
- Live exchange-data entitlement in **paper**, not only on a chart.
- Historical contract bars, contract rolls, holidays and RTH/ETH metadata.
- Broker-realistic fees, margin, order types, stop behavior, disconnect
  recovery and daily risk controls.
- Ability to keep a distinct paper ledger with no live credential present.

IBKR is an example of a documented futures-capable paper environment, **not a
recommendation or required purchase**. Its [paper-account lesson](https://www.interactivebrokers.com/campus/trading-lessons/how-to-open-an-ibkr-paper-trading-account/)
says an approved live account is needed, the paper account uses separate
credentials, and its permissions and market-data subscriptions mirror the
live account. Check eligibility and current account requirements directly.
Do not send credentials in chat or commit them.

Prop firms are independent rule systems. Obtain current written terms on API
automation, strategy mirroring, news trading, position holds, scaling,
contract counts, daily/trailing drawdown, and payout restrictions. A paper
simulation is not evidence a prop firm permits the method. No prop or live
orders are authorized by this register.

## Order flow and company/macro data

If book mapping is a real research need, ask a vendor for timestamped CME
**trades + MBP-10/MBO** by named contract. The [Databento schema list](https://databento.com/pricing)
distinguishes top-of-book, market-by-price and market-by-order; [CME DataMine](https://www.cmegroup.com/education/files/cme-datamine-overview.pdf)
describes historical market depth and MBO. OHLCV chart exports cannot recover
order identities or queue changes. Obtain a sample and license before paying
for a full history. Market depth is not proof of named institutional ownership.

For macro and company events, start with primary, mostly free sources:
[Federal Reserve FOMC calendar](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm),
[BLS release schedule](https://www.bls.gov/schedule/),
[BEA release schedule](https://www.bea.gov/news/schedule), and
[SEC EDGAR data APIs](https://www.sec.gov/search-filings/edgar-application-programming-interfaces).
Retain **published-at** timestamps and revisions; do not join a revised
historical value to a model decision made before publication. EDGAR filings
are disclosed with lag and cannot identify every real-time market participant.

## Purchase hold points

- **No payment yet** for context-symbol chart exports if your existing plan
  already allows them.
- **Do not pay** for a delayed futures tier when the objective is to eliminate
  the ten-minute delay.
- **Do not pay** for MBO until an as-of feature and falsifiable test are
  specified; depth is expensive and can overfit.
- **Do not connect** a broker/prop account to live execution while candidate
  qualification, real-fill parity and risk recovery remain incomplete.
