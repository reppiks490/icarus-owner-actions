# ICARUS shared GitHub-native credential and data access

This directive is mandatory for every ChatGPT, Codex, Claude, or other AI unit working anywhere in the ICARUS federation.

## The critical distinction

**Secret possession is not data access.** Agents are not expected to read, recover, copy, or possess plaintext API keys. GitHub Actions Secrets intentionally do not reveal stored values back to chats, repository readers, or normal workflow logs.

The shared capability is the **GitHub-native execution and evidence plane**: approved repository workflows receive credentials at runtime, collect provider data, and persist permitted normalized/derived evidence that every cooperating AI unit can inspect from repository state.

Therefore:

- **Do not search local `.env` files, DAV task comments, another ChatGPT account, another agent's workspace, or Plant/operator notes for a private provider API key.** Those are not federation provider-credential authority.
- **Do not ask another AI to paste or reveal a key.**
- If your current runtime cannot see a secret string, that is expected and is not proof that ICARUS lacks access.
- Check credential availability through the redacted GitHub-native health workflow and check actual data availability through the ingestion manifest and persisted evidence receipts.

## Two different secret planes — do not confuse them

### Shared provider credentials

Provider API credentials used by ICARUS collection belong in **GitHub Actions Secrets** and are resolved through the canonical Engine credential contract. They power shared collection/evidence; agents normally never see the plaintext values.

### Local Plant / bridge runtime controls

`ADMIN_TOKEN` / `ICARUS_ADMIN_TOKEN`, webhook secrets, and machine-local broker/runtime credentials are **privileged local runtime controls**, not the shared provider credential plane. Legacy Plant/bridge code may correctly load those from the operator's local `.env` because the bridge is a localhost process.

A cloud worker that cannot read the Plant `ADMIN_TOKEN` must **not** conclude that API/provider data is inaccessible. It should use the shared GitHub-native evidence plane for data/research. If a task truly requires a privileged Plant operation, report `LOCAL_RUNTIME_CAPABILITY_REQUIRED` and use an explicitly approved/brokered runtime-control path; never copy the admin token into a chat, issue, coordination note, or repository file.

The current owner boundary keeps **live broker arming disabled**. Read-only research/observability and paper/shadow work may continue within their verified scope, but the existence of a Plant credential never grants live-order authority.

## Canonical credential authority

Repository: `reppiks490/Icarus-engine`

Read these before making any provider-access claim:

- `AGENT_CREDENTIALS.md`
- `docs/agent-handoffs/GITHUB_NATIVE_CREDENTIALS.md`
- `config/credential_contract.json`
- `config/data_ingestion_manifest.json`
- `.github/workflows/github-native-credential-health.yml`
- `tools/credential_health.py`
- `tools/provider_credentials.py`

The canonical contract/resolver chooses approved aliases; workflows inject Secrets at runtime. The health workflow reports only canonical name, presence, and matched alias. It never exposes values.

## How every AI unit actually uses the data

### 1. Prefer persisted shared evidence

Before attempting a fresh provider call, read `config/data_ingestion_manifest.json`. Its `evidence_paths` are the machine-readable routing table for the federation.

Core shared paths include:

- `automation_intelligence/provider_collection_v1/latest/`
- `automation_intelligence/provider_collection_v1/research_context.json`
- `automation_intelligence/cl_lab/`
- `automation_intelligence/native_research_v1/`
- `automation_intelligence/sentinel/data_health.json`

A chat that only needs research/context should consume these shared outputs instead of trying to obtain a secret.

### 2. Use the established GitHub Actions collection lanes when fresh collection is required

Primary credentialed/public provider lane:

- `.github/workflows/provider-exhaustive-collection.yml`

Supplemental provider lane:

- `.github/workflows/provider-supplemental-collection.yml`

Credential verification:

- `.github/workflows/github-native-credential-health.yml`

Additional dedicated lanes and their exact evidence paths are enumerated in `config/data_ingestion_manifest.json`.

### 3. Interpret states correctly

The federation truth model is three separate facts:

1. `credential_state` — is an approved credential/public access path available?
2. `ingestion_state` — is collection actually running and returning data?
3. `consumption_state` — is that data being consumed by ICARUS research/runtime paths?

Never infer all three from one green workflow wrapper.

## Current important provider examples

- **Unusual Whales:** GitHub-native credential present; supplemental collection is live/partial/resumable. Shared receipts live under `automation_intelligence/provider_collection_v1/latest/unusual_whales.json` and the shared research context.
- **Alpha Vantage:** credential present; accessible endpoints return data, while some endpoint families are entitlement-limited.
- **Finnhub:** a stored credential exists, but the verified provider response is HTTP **401** using documented authentication. Treat this as `BLOCKED_AUTHENTICATION`, not as accessible data, until the stored secret is repaired/replaced.
- **Intrinio / Quiver / Alpaca / Tickstream:** remain explicit missing-credential blockers unless the current health/manifest state has changed.

Always prefer the live health/manifest state over this explanatory example if they differ later.

## What to do when a chat says “I cannot see the key”

That statement by itself is not a blocker. Follow this sequence:

1. Determine whether the task means a **provider API credential** or a **local Plant/bridge runtime-control token**. Do not conflate them.
2. For provider/data work, read `AGENT_CREDENTIALS.md` and `docs/agent-handoffs/GITHUB_NATIVE_CREDENTIALS.md` in `reppiks490/Icarus-engine`.
3. Read `config/data_ingestion_manifest.json` and the relevant provider receipt/evidence path.
4. Check the redacted `github-native-credential-health` result if credential presence matters.
5. Consume the existing shared evidence if it satisfies the task.
6. If fresh collection is required, use/extend the established GitHub Actions collector for that provider without exposing the secret.
7. Only report a provider credential blocker when the canonical health/manifest says missing/invalid/denied—not because the current chat cannot read plaintext.
8. If the task genuinely requires Plant admin control, report the local-runtime capability boundary precisely; do not request or distribute `ADMIN_TOKEN`.

## Security boundary

No AI unit should ever need plaintext provider API-key possession for normal ICARUS work. Never print, copy, commit, artifact, or place private credential values into coordination notes, PR comments, issues, dashboards, or shared files. The federation shares **capability, collection, status, and evidence**—not secret strings.
