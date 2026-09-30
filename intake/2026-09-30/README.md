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
  - The HA transform was independently checked against this standard OHLC source: timestamp alignment is complete, and HA close/high/low identities hold for all post-seed rows.

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

## Checklist status

This intake provides strong evidence for the **20-minute NQ portion of O03**:
- 20m HA chart CSV: present and validated.
- 20m standard OHLC CSV: present and timestamp-aligned.
- Strategy Report List of trades CSV: present.
- TradingView performance summary/report: present in XLSX.

`O03` should remain unchecked because the same task also asks for standard 1m, 5m, 60m, 240m and daily exports as available.

`O04` is **not marked complete**. A standard-candlestick report exists, but the owner checklist specifically requires proof of a Heikin-Ashi signal chart using TradingView's **Standard bars** execution-price mode, with separate trade list/summary and settings evidence. The uploaded report does not by itself prove that emulator mode.

`O05` is **not marked complete**. The report properties show `RTH Session Gate = Off` and a configured ET session, while the bar history includes overnight timestamps, but the checklist requires explicit session-toggle evidence and representative session exports.

`O06` now has a reproducible checksum/provenance manifest, but raw files remain outside GitHub as required.

See `EXPORT_INTAKE_MANIFEST.csv` for every observed filename, SHA-256, duplicate group, row count, report range, and key report metadata.
