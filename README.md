# Maintainer workspace

> [!CAUTION]
> **PROPRIETARY — ALL RIGHTS RESERVED**
>
> **No public license or personal-use license is granted.** Except where [LICENSE.md](LICENSE.md) preserves applicable law, GitHub platform rights, third-party terms, or prior valid permissions, written authorization is required to use, run, copy, modify, redistribute, or sell covered material. Do not remove ownership notices or claim this work as your own.
>
> Unauthorized infringement may lead to takedown requests and legal proceedings for available remedies. Public visibility is not permission to reuse.

This workspace is maintained for its owner and authorized collaborators. Permission requests and the full terms are in [LICENSE.md](LICENSE.md).

<details>
<summary>Maintainer documentation</summary>

# ICARUS owner action register

This repository is the human-side checklist and shared coordination surface for the ICARUS research and paper-trading system. It is separate from the engine code. It does not authorize live orders, certify an ML candidate, or promise a win rate.

**Every AI/chat starts here first:** [`coordination/START_HERE.md`](coordination/START_HERE.md). For shared provider/API access, also read [`coordination/directives/GITHUB_NATIVE_DATA_ACCESS.md`](coordination/directives/GITHUB_NATIVE_DATA_ACCESS.md). Those two files are the current federation authority for coordination and for how agents use the GitHub-native data plane.

For owner checklist work, use [OWNER_TASKS.md](OWNER_TASKS.md). The exact chart/export request is in [EXPORT_MATRIX.md](EXPORT_MATRIX.md); optional subscriptions and account choices are in [PROVIDERS_AND_COSTS.md](PROVIDERS_AND_COSTS.md). For cross-repository workflow health, machine-readable assurance artifacts, and the current private-runner blocker, see [WORKFLOW_ASSURANCE_REGISTRY.md](WORKFLOW_ASSURANCE_REGISTRY.md).

For click-to-complete checkboxes, use [Owner action checklist #1](https://github.com/reppiks490/icarus-owner-actions/issues/1).

## Shared credential/data model

Do not collapse all secrets into one `.env` rule. ICARUS has two different credential classes:

1. **Provider API credentials** used by shared collection workflows belong in **GitHub Actions Secrets** and are resolved through the canonical Icarus-engine credential contract. Agents normally do **not** read or possess those plaintext values. They consume the resulting GitHub Actions-backed capability, redacted health state, and persisted evidence described by `reppiks490/Icarus-engine:config/data_ingestion_manifest.json`.
2. **Local privileged runtime controls** such as the Plant/bridge `ADMIN_TOKEN`, webhook secrets, and machine-local broker/runtime credentials remain local to the operator/runtime and must not be copied into chats or coordination records. A cloud agent's inability to read a Plant admin token is not evidence that shared provider data is unavailable.

Before any AI says “I cannot access the key/data,” it must follow `coordination/directives/GITHUB_NATIVE_DATA_ACCESS.md`. In particular, do not search `$ICARUS_HOME/.env`, local `.env` files, DAV task comments, another AI account, or Plant/operator notes for a shared provider key. Use the canonical GitHub-native health, workflows, and evidence paths instead.

**Live broker arming remains disabled by owner direction.** Privileged runtime credentials do not grant permission to enable live execution.

## The next three owner-side things

1. Record the **exact TradingView chart and strategy configuration** used for the 20-minute NQ result, including Heikin Ashi and its **fill mode**.
2. Export matching **20-minute Heikin Ashi and standard OHLC chart CSVs**, plus the Strategy Report trade list and property/input settings. Keep both price streams: HA is the signal chart; standard OHLC is the real-fill reference.
3. Check whether the NQ chart says **Data is delayed**. If it does, choose a real-time exchange-data entitlement or a qualifying broker-data verification before expecting a low-latency live feed. A TradingView alert is near-real-time only relative to the data that TradingView itself receives.

Do not buy a data feed or open a broker account just to satisfy a checklist. The research and parity tasks come first. Paid choices are explicitly optional until their prerequisite is met.

## What belongs where

| Item | Destination |
|---|---|
| AI coordination, claims, waiting/handoffs, completion evidence | `coordination/**` in this repository |
| Checkmarks, decisions, nonsecret screenshots, links | This repository |
| Raw TradingView/market-data CSVs, xlsx, recordings | Local/private licensed storage or an explicitly authorized repository path |
| Provider API credentials used by GitHub collection | GitHub Actions Secrets; never plaintext in Git/chat/artifacts |
| Local Plant/bridge admin token, webhook secret, machine-local broker credentials | Local privileged secret store / local `.env`; never Git/chat/artifacts |
| Engine code, models, candidate audits | `reppiks490/Icarus-engine` / federation repositories |

This repository intentionally excludes raw private account secrets. Even a private GitHub repository is not a substitute for checking market-data license terms. Do not assume a chart export may be redistributed.

## Status language

- **Required for parity**: without it, we cannot compare the engine with your validated TradingView run on equal terms.
- **Required for paper futures**: needed before testing actual futures orders.
- **Optional research**: may improve evidence, but is not a proven edge.
- **Deferred**: do not enable until the preceding gates pass.

Checked against official provider documentation on 2026-09-23. Prices, entitlements, contract symbols, API policies, and prop-firm rules can change; verify again before purchasing or connecting anything.

Prepared by CA / Codex, 2026-09-23; federation credential/coordination routing updated 2026-10-16.

## Key source documents

- [TradingView chart export](https://www.tradingview.com/support/solutions/43000537255-how-to-export-chart-data/)
- [TradingView Strategy Report export](https://www.tradingview.com/support/solutions/43000613680-how-to-export-strategy-data/)
- [TradingView Heikin Ashi fill modes](https://www.tradingview.com/support/solutions/43000786181-broker-emulator/)
- [TradingView exchange-data purchases](https://www.tradingview.com/support/solutions/43000471705-how-to-purchase-additional-market-data/)
- [TradingView webhooks](https://www.tradingview.com/support/solutions/43000529348-how-to-configure-webhook-alerts/)

## License and ownership

Copyright (c) 2026 reppiks490. **Proprietary — all rights reserved.**
Public visibility does not grant permission to reuse, redistribute, sell, or claim this work as your own. Written permission is required except where applicable law, existing grants, third-party terms, or GitHub's terms provide otherwise. See [LICENSE.md](LICENSE.md) for the full notice and permission requests.

</details>
