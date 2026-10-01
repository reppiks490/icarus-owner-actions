# Icarus export intake — 2026-09-30

This intake records metadata and validation results for the TradingView exports supplied to ChatGPT on 2026-09-30.

## Repository policy

Raw market-data CSV/XLSX payloads are **not committed** here. `OWNER_TASKS.md` / `EXPORT_MATRIX.md` require keeping licensed raw files private. This folder stores only hashes, filenames, structural metadata, and validation findings.

## Intake summary

- 21 distinct uploaded filenames were available to the intake process.
- SHA-256 deduplication reduced them to **11 unique payloads**.
- 10 observed files were byte-for-byte duplicate copies of another uploaded payload.
- NQ: 15 observed filenames / 7 unique payloads.
- ES: 6 observed filenames / 4 unique payloads.

## NQ 20-minute parity packet

The central NQ pair is structurally valid and aligned:

- **Heikin Ashi chart export:** `CME_MINI_DL_NQ1!, 2(1).csv`
  - SHA-256: `4fe26a9b2ee9a5e81c24577f2abd51073e7e944f4f6aa43a77b61095af44e48c`
  - 41,239 bars.
  - UTC range: 2024-06-02 22:00 through 2026-09-30 13:20.
  - Modal spacing: 1,200 seconds (20 minutes).
- **Standard OHLC chart export:** `CME_MINI_DL_NQ1!, 20(1).csv`
  - SHA-256: `a8141ffa372b4ffaba4d6bf8b8998a489f2daf00bfad5e248bf27132d99f0932`
  - 41,239 bars over the identical timestamp set and date range.
  - Re-validation on 2026-10-01 confirmed complete timestamp alignment. HA open matches all rows when seeded from the supplied HA export; HA high/low/close geometry matches 41,238 of 41,239 rows. The only mismatch is the final timestamp (2026-09-30 13:20 UTC) between the separately downloaded files. No cause is inferred; the standard-OHLC export remains the canonical runtime history input.

The matching current-window NQ Heikin Ashi strategy report is represented by one unique XLSX payload (three identical filename copies were uploaded):

- SHA-256: `a8d83d6ee2a1270cf90e5155ee63e317e7fddcbaf475eaf95c0feb920a292594`
- Symbol: `CME_MINI:NQ1!`
- Timeframe: 20 minutes
- Chart type: Heikin Ashi
- Backtesting range: Jun 2, 2024 17:00 — Sep 30, 2026 08:20
- 883 trade numbers / 1,766 trade rows
- Net profit shown in the TradingView report: $700,427
- Intrabar max drawdown shown in the report: $165,324
- Commission: 2; slippage: 0 ticks; execution: on bar close; order execution delay: one tick.

The NQ trade-list CSV is also present. Seven uploaded filenames are byte-identical copies of the same 1,766-row trade list:

- SHA-256: `0e05de5ba655c90fa9a0f77153ab45816a73557fe5185373d5467671774088a6`
- Last trade number: 883
- First listed event: 2024-06-03 10:20
- Last dated event: 2026-09-29 06:20

A current-window 20-minute standard-candlestick NQ TradingView report is also present:

- `THE_PULSE_OF_ICARUS_CME_MINI_NQ1!_2026-09-30 2.xlsx`
- SHA-256: `99e74653ebb9444d27ed3a11f826d3304d46e72bff7e53a2acfb03dd69b17577`
- Chart type: Candles
- Same backtesting window as the current HA report
- Last trade number: 748
- Net profit: -$148,547
- Intrabar max drawdown: $218,906

Two additional long-history NQ 20-minute reports are retained in the manifest:
- standard Candles, Feb 2019–Sep 2026: SHA-256 `05cebeb4a44fcad254b6c7ee05d66ef8a81593e5d984cf91b5ee1b1a8dd9aae3`
- Heikin Ashi, Feb 2019–Sep 2026: SHA-256 `dc3c1c3b32bc7da97bcbaa5bd207eb1d462d8104cc77b9f4e5cb75eef9425585`

## ES material received

ES contains both Heikin Ashi and standard-candlestick 20-minute reports, plus a matching long-history HA trade-list CSV:

- Long-history HA XLSX: SHA-256 `9b471fb02fd6dde9b967b1ef7fe8da07fe5be5c638c09038c2160b0bd755c7a3`
- Long-history HA trade-list CSV: SHA-256 `0c702ce1b34e5d2bab03b9820ed483609c85b2c2113dafda5b5696f879e48cf7`
- Current-window HA XLSX: SHA-256 `9b039da30ce28c9d7ca57d213ea1d178e2375c877c69eb0c4d5a54cc4930fac5`
- Current-window Candles XLSX: SHA-256 `30e885410e8fff5dc6977a7ea6902e3e8432e9363d66d3e33c5068468bed013a` (`...7.xlsx` and `...8.xlsx` are identical)

## User-confirmed session provenance

The owner confirmed that the export families are distinguished by their history start date:

- **RTH:** reports/export families whose backtest/trade history begins in **2019**.
- **ETH:** reports/export families whose backtest/trade history begins in **2024**.

This resolves the main session ambiguity in the intake. The strategy property `RTH Session Gate = Off` is an internal Pine/strategy input and is **not** used here as the TradingView chart-session label.

Accordingly:
- NQ 2019 standard report (`... 3.xlsx`) = **RTH**.
- NQ 2019 Heikin Ashi report (`... 4.xlsx`) = **RTH**.
- NQ 2024 Heikin Ashi report family (`...(1).xlsx`, `...(2).xlsx`, base `.xlsx`) = **ETH**.
- NQ 2024 standard report (`... 2.xlsx`) = **ETH**.
- NQ 2024 trade-list CSV family = **ETH**.
- NQ 2024 20m HA and standard chart-data CSV pair = **ETH**.
- ES 2019 Heikin Ashi report (`... 4.xlsx`) and its 2019 trade-list CSV family = **RTH**.
- ES 2024 Heikin Ashi report (`... 6.xlsx`) = **ETH**.
- ES 2024 standard report family (`... 7.xlsx` / `... 8.xlsx`) = **ETH**.

Byte-identical copies remain duplicate payloads within the same session family; the RTH/ETH distinction is between the 2019-start and 2024-start families.

## Checklist status

This intake provides strong evidence for the **20-minute NQ portion of O03**:
- 20m HA chart CSV: present and validated.
- 20m standard OHLC CSV: present and timestamp-aligned.
- Strategy Report List of trades CSV: present.
- TradingView performance summary/report: present in XLSX.

`O03` should remain unchecked because the same task also asks for standard 1m, 5m, 60m, 240m and daily exports as available.

`O04` is **not marked complete**. A standard-candlestick report exists, but the owner checklist specifically requires proof of a Heikin-Ashi signal chart using TradingView's **Standard bars** execution-price mode, with separate trade list/summary and settings evidence. The uploaded report does not by itself prove that emulator mode.

`O05` is **complete**. The owner supplied NQ 20m screenshots showing both
RTH and ETH session selection. The retained NQ chart-data history contains
ordinary sessions and the 2025-11-28 shortened session, satisfying the requested
session-behavior evidence without another redundant bulk export.

`O06` is **complete by owner acceptance**. The private intake originals were
SHA-256 hashed and recorded in the intake manifest. The owner explicitly chose
to rely on that existing integrity record rather than perform a second local
checksum pass. Raw licensed payloads remain outside GitHub as required.

See `EXPORT_INTAKE_MANIFEST.csv` for every observed filename, SHA-256, duplicate group, row count, report range, and key report metadata.


## O14 historical corpus recovery

The wider multi-asset corpus was located in historical Git revisions and should
be inventoried before any large re-export campaign.

Authoritative recovered checkpoints:

- `reppiks490/multi-level-csv` at
  `ce82124352762c14eb33836a5c894bc3a2a71dfe`: nine source ZIPs.
- `reppiks490/csv-data-multi-chart-type` at
  `a482e7d1801fa7fa5aec093960097c0051c0403c`: `Csv indexes.zip`.
- PARALLAX ten-archive audit: **659 usable CSV members / 13,788,256 logical
  rows / 542 distinct byte-exact contents**.
- DAEDALUS extracted-corpus reconciliation: **803 physical CSV files / 542
  distinct byte contents**, with zero ZIP-only or extracted-only content hashes.

The physical count is larger because the extracted roots preserve additional
lineage/copies. It is not evidence of 803 independent market signals.

The owner clarified that the corpus intentionally spans multiple chart and
sampling constructions across assets: regular candles, Heikin Ashi, Renko,
TPO/profile views, volume-footprint/profile views, session-volume-profile views,
plus seconds/minutes/hours, tick and range sampling. O14 must therefore inventory
`asset -> venue/contract -> session -> chart/view family -> price geometry ->
sampling construction/native setting -> schema -> date span -> hash`.

NEXUS and PARALLAX have been hardened so chart/view family and sampling
construction are separate axes. Tick/range claims are event-driven sampling
constructions, not automatic chart-family labels. Duplicate payloads do not gain
evidence weight. Representation-sensitive modeling is fail-closed and uses the
hierarchy: sampling construction -> price geometry -> reviewed chart/view
family -> symbol -> cross-asset weighting.

**O14 remains open only for reconciliation of the existing corpus against the
required execution/micro/contract matrix and for genuinely missing cells. Bulk
re-export of the historical ~800-file corpus is not requested.**


### O14 identity refinement

Transform comparisons are treated as **price-geometry evidence**, not automatic
chart/view-family evidence. Standard-OHLC equality cannot by itself distinguish
an ordinary candlestick export from a TPO, footprint or profile view that
preserves the same OHLC fields. Family-specific O14 cells stay unresolved until
the view identity is independently evidenced.
