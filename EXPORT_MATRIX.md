# Chart-data export matrix

Prepared by CA / Codex, 2026-09-23.

The goal is **comparable, timestamped evidence**, not a pile of similar files.
Start with the P0 packet. The P1/P2 lists are a research universe, not
qualified trade recommendations. Confirm each chart's exact exchange ticker
in TradingView Symbol Search; ticker aliases, continuous-roll conventions and
historical availability differ by provider. Never infer a futures fill from a
stock/ETF proxy.

## How to export one chart

1. In TradingView Supercharts, choose the exact symbol and set **RTH or ETH**.
   Save a screenshot of the symbol and session selector.
2. Choose the chart type and interval. For the reference strategy use
   **Heikin Ashi, 20 minutes**; export a separate **standard candlestick,
   20-minute** file over the same dates. Do not rename a standard file `HA`.
3. Scroll left until the oldest data you need is loaded. In the upper toolbar
   menu choose **Download chart data...**, select the chart, then **Download**.
   TradingView exports the bars currently loaded on the chart. If a long
   interval needs multiple exports, retain the date ranges and overlap.
4. Keep the raw file unchanged. Record the symbol, exchange, named contract or
   continuous contract, session, chart type, interval, timezone, date range,
   row count, export date, indicator settings and SHA-256 in a manifest.
5. On the same strategy chart, open **Strategy Report** and download **List
   of trades** and the summary separately. A chart CSV is not a trade list.

Official directions: [chart CSV export](https://www.tradingview.com/support/solutions/43000537255-how-to-export-chart-data/), [Strategy Report export](https://www.tradingview.com/support/solutions/43000613680-how-to-export-strategy-data/).

### Suggested private folder and checksum command

In Windows PowerShell:

```powershell
New-Item -ItemType Directory -Path "$HOME\Downloads\ICARUS_EXPORTS" -Force
Get-ChildItem -LiteralPath "$HOME\Downloads\ICARUS_EXPORTS" -File -Filter *.csv |
  Where-Object Name -ne 'manifest_sha256.csv' |
  Get-FileHash -Algorithm SHA256 |
  Select-Object Path, Hash |
  Export-Csv -NoTypeInformation -Path "$HOME\Downloads\ICARUS_EXPORTS\manifest_sha256.csv"
```

Put the downloaded CSVs in that folder before running the checksum command.
The command does not upload or alter the raw files. The checksum CSV itself is
metadata; do not commit the raw chart CSVs here.

Suggested filename (never change the original's contents):
`NQ1__CME__continuous__RTH__HA__20m__2024-01_to_2026-09.csv`.
Use another filename for `STANDARD`, `ETH`, a named contract, or a different
exchange. Do not use `:` in a Windows filename.

## P0: exact strategy and execution parity

For **NQ first**: 20m HA; 20m standard OHLC; 1m and 5m standard OHLC; 60m,
240m and daily standard OHLC; Strategy Report trade list and settings. Export
the same interval and session on all variants where possible. Also retain
the original 10m run **labeled as a separate comparator**, not the current
20m reference. Capture both HA-fill and standard-fill Strategy Reports.

| Owner traded asset | Search/verify underlying contract | Exchange group | Initial export priority |
|---|---|---|---|
| NQ (Nasdaq 100 futures) | NQ continuous **and** named expiry | CME | P0: full parity packet above |
| ES (S&P 500 futures) | ES continuous + named expiry | CME | P1: 20m HA/standard, 1m, 60m, daily |
| YM (Dow futures) | YM continuous + named expiry | CBOT | P1: same |
| GC (gold futures) | GC continuous + named expiry | COMEX | P1: same |
| SI (silver futures) | SI continuous + named expiry | COMEX | P1: same |
| PL (platinum futures) | PL continuous + named expiry | NYMEX | P1: same |
| PA (palladium futures) | PA continuous + named expiry | NYMEX | P1: same |
| BTCF (CME Bitcoin futures) | BTC continuous + named expiry | CME | P1: same; distinct from spot BTC |
| BTCUSD spot | One named spot venue and exact quote currency | Chosen venue | P1: 20m HA/standard, 1m, 60m, daily |

For each futures product, retain the **named front and next contract around
each roll** and the provider's continuous-series adjustment rule. A continuous
contract splice can create a fictitious gap; the actual traded contract is
needed to verify real fills. If a bar is missing or the chart is delayed,
record that fact. TradingView's RTH/ETH selector changes intraday bars, but
not its daily bars: [official session guide](https://www.tradingview.com/support/solutions/43000670909-regular-and-electronic-trading-hours-for-cme-futures/).

## P1: distinct micro-contract tapes

These are separate instruments, **not** parent fills divided by ten. The
current owner archives have no source CSVs for them. Obtain 20m standard/HA,
1m standard, daily, named contracts around rolls, and current exchange
specification for each available product. Verify actual listing in your
TradingView/data account before exporting.

| Parent | Separate micro to request | Venue | Why |
|---|---|---|---|
| NQ | MNQ | CME | Lower multiplier; independent fees/liquidity/fills |
| ES | MES | CME | Same |
| YM | MYM | CBOT | Same |
| GC | MGC | COMEX | Same |
| SI | SIL | COMEX | Same; do not assume an SI tick |
| PL | PLM | NYMEX | Same |
| PA | PAM | NYMEX | Same |

**Excluded:** MBT is an existing CME product but is owner-banned. No ETH or
SOL spot/futures export is requested for the traded/model universe. CME
[micro equity FAQ](https://www.cmegroup.com/articles/faqs/frequently-asked-questions-micro-e-mini-equity-index-futures.html)
and [micro metals guide](https://www.cmegroup.com/markets/microsuite/metals.html)
are the starting specs; verify current listings and tick values before use.

## P2: contextual chart candidates (not automatically beneficial)

For these sensors, start with **20m standard, 60m, daily** over a window
overlapping the execution asset; add 1m only if an explicitly tested
event/lead-lag hypothesis needs it. Export the source's real timestamp and
venue. An attractive correlation is not a trading edge; each sensor must
survive as-of availability, lag and final-holdout tests.

| Purpose | Asset/code list to inspect | Main question |
|---|---|---|
| Equity-index breadth/lead-lag | RTY/M2K futures; QQQ, SPY, DIA, IWM; NDX, SPX, DJI, RUT indices | Does breadth/lead-lag add out-of-sample information beyond the index future itself? ETFs/indices are context, not fill proxies. |
| Volatility/risk | VX futures; VIX, VXN, VVIX indices; MOVE index if licensed | Does a known-at-time volatility state improve position/risk decisions? Check index calculation delay. |
| Rates/curve | ZT, ZF, ZN, ZB futures; 2Y and 10Y Treasury yields, 10Y-2Y spread; SOFR futures | Rate shocks and duration sensitivity, especially NQ/gold. Respect the source's publication/update clock. |
| Dollar/FX | DXY/US Dollar Index; EURUSD, USDJPY, USDCNH; 6E and 6J futures if available | Dollar/risk and metals transmission, not a substitute for futures tape. |
| Energy/inflation | CL, MCL, NG futures; WTI/Brent spot/reference series; gasoline/heating oil if licensed | Macro/inflation and commodity regime context. |
| Metals complex | HG/MHG copper futures; gold and silver spot references; GDX, GDXJ, SIL, PPLT, PALL ETFs | Cross-metal regime and liquidity context. Do not confuse the `SIL` ETF with `SIL` micro silver contract; venue matters. |
| Credit/liquidity | HYG, LQD, TLT, SHY, UUP ETFs; credit-spread index if licensed | Stress/flight-to-quality proxy; daily often sufficient. |
| Nasdaq concentration | NVDA, MSFT, AAPL, AMZN, META, GOOGL, AVGO, TSLA, AMD, INTC, ORCL, TSM | Test large-cap earnings/opening shocks. Weights change; use dated index membership/weights rather than assuming this is a fixed top-ten. |
| Semis/sectors | SMH, SOXX, XLK, XLF, XLE, XLI, XLY | Sector/breadth context; avoid training the same information repeatedly through near-duplicate ETFs. |
| Other company/event context | BRK.B, JPM, CAT, XOM, JNJ, PFE and the owner's existing candidate-stock list | Only if a causal hypothesis connects them to an execution asset. Existing owner batches already include many of these; deduplicate hashes first. |
| Bitcoin context | BTCUSD at a named spot venue; BTCUSDT only as a distinct quote market if explicitly approved; IBIT ETF; CME BTC front/next contracts | Spot/futures basis, regulated-market hours, ETF flows. Never label spot prints as CME futures fills. |

This is a **broad shortlist**, not a claim that every item improves returns.
Prioritize missing direct execution data before spending time on context.
The six recent candidate-data archives already contain 177 CSV files but only
89 distinct content hashes and 15 distinct instrument names; duplicate files
do not create independent evidence.

### Data that a chart CSV cannot supply

- True order flow: time-and-sales, top-of-book, level-2 depth and level-3
  market-by-order data need a licensed exchange/vendor feed with nanosecond
  or microsecond timestamps, sequence numbers and contract identifiers.
- Macro surprises: record the **actual release timestamp**, first-published
  value, consensus available before release, and later revisions separately.
- Named institutional moves: a price/volume bar cannot identify who traded.
  SEC filings describe disclosed holdings/events with publication lags; they
  are not a live participant-by-participant tape.

## Intake fields

| Field | Example |
|---|---|
| asset_role | execution / micro / context / event |
| market_id | `CME:NQ1!` as shown on your chart |
| contract_id | continuous or named expiry |
| session | RTH / ETH / 24x7 |
| chart_view_family | standard candles / HA / Renko / TPO / volume footprint / session volume profile / unknown |
| price_geometry | standard OHLC / Heikin Ashi / Renko-like / unknown |
| sampling_domain | time / event / provider-native profile |
| sampling_construction | time_bar / tick / range / provider-native |
| native_setting | 1s / 1m / 20m / 60m / 240m / 1D / 1000T / 10R / exact provider setting |
| time_zone | exchange and displayed time zone |
| first_ts, last_ts | UTC timestamps after validation |
| rows, sha256 | Count and checksum from unchanged raw file |
| adjusted_roll | on/off and vendor method |
| data_entitlement | delayed / real-time / historical only |
| source_url_or_account | provider; do not enter credentials |

Renko/profile chart families and tick/range sampling constructions need their
exact provider-native settings and identity. Tick/range describe how bars are
sampled; they are not automatically chart-family labels. None may be silently
treated as 20-minute time bars. Re-export after changing TradingView chart settings or contract
roll mode.


### Existing multi-representation corpus rule

Before requesting new O14 exports, reconcile the owner's existing historical
multi-asset corpus. The recovered PARALLAX checkpoint contains 10 source ZIPs,
659 usable archive members, 13,788,256 logical rows and 542 distinct byte
contents; the DAEDALUS extracted catalog reconciled to 803 physical CSV files.

Those files intentionally span **orthogonal chart/view, price-geometry and sampling axes**.
Chart/view families include regular candles, Heikin Ashi, Renko, TPO, volume
footprint/profile and session volume profile where explicitly identified.
Price geometry is tracked separately because a TPO/footprint/profile view can
still export standard OHLC or Heikin-Ashi-derived OHLC. Sampling/construction
separately includes seconds/minutes/hours and other time bars, tick sampling,
and range sampling. A `1000T` or `10R` suffix establishes
a sampling construction only; it does not by itself identify the chart family.

These are correlated views of the same underlying markets, not independent
votes. Preserve native construction and clock semantics. The required fusion
order is: streams within sampling construction -> sampling constructions within price
geometry -> price geometries within reviewed chart/view family -> chart/view
families to a symbol-level state -> cross-asset
weighting. Do not coerce tick/range/Renko/profile streams to fixed minute/hour
cadence. Exact-byte duplicates retain lineage but receive no additional
evidence weight.

Only export a new file after the inventory proves that an O14-required cell
(asset/contract/session/representation/native setting/date span) is genuinely
missing.


### Price geometry is not chart/view identity

A mathematical OHLC transform check proves **price geometry only**. Equality to
a known standard-OHLC stream does not prove that the source was an ordinary
candlestick view: TPO, footprint and profile views can retain the same OHLC
geometry. Likewise, Heikin-Ashi geometry does not rule out an additional
profile/footprint view layer. O14 therefore requires view-family provenance
separately from price-geometry proof before a family-specific matrix cell is
marked satisfied.
