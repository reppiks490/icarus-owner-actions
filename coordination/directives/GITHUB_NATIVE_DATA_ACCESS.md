# ICARUS shared GitHub-native credential and data access

This directive is mandatory for every ChatGPT, Codex, Claude, or other AI unit working anywhere in the ICARUS federation.

## The critical distinction

**Secret possession is not data access.** Agents are not expected to read, recover, copy, or possess plaintext API keys. GitHub Actions Secrets intentionally do not reveal stored values back to chats, repository readers, or normal workflow logs.

The shared capability is the **GitHub-native execution and evidence plane**: approved repository workflows receive credentials at runtime, collect provider data, and persist permitted normalized/derived evidence that every cooperating AI unit can inspect from repository state.

Therefore:

- **Do not search local `.env` files, DAV task comments, another ChatGPT account, another agent's workspace, or Plant/operator notes for a private API key.** Those are not federation credential authority.
- **Do not ask another AI to paste or reveal a key.**
- If your current runtime cannot see a secret string, that is expected and is not proof that ICARUS lacks access.
- Check credential availability through the redacted GitHub-native health workflow and check actual data availability through the ingestion manifest and persisted evidence receipts.

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

1. Read `AGENT_CREDENTIALS.md` and `docs/agent-handoffs/GITHUB_NATIVE_CREDENTIALS.md` in `reppiks490/Icarus-engine`.
2. Read `config/data_ingestion_manifest.json` and the relevant provider receipt/evidence path.
3. Check the redacted `github-native-credential-health` result if credential presence matters.
4. Consume the existing shared evidence if it satisfies the task.
5. If fresh collection is required, use/extend the established GitHub Actions collector for that provider without exposing the secret.
6. Only report a credential blocker when the canonical health/manifest says missing/invalid/denied—not because the current chat cannot read plaintext.

## Security boundary

No AI unit should ever need plaintext API-key possession for normal ICARUS work. Never print, copy, commit, artifact, or place private credential values into coordination notes, PR comments, issues, dashboards, or shared files. The federation shares **capability, collection, status, and evidence**—not secret strings.
