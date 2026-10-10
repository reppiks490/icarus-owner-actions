# ICARUS supporting architecture blueprint

Prepared 2026-10-09 from read-only public documentation. This is a design proposal, not a deployed service or verified integration. No paid jobs, credentials, database queries, deployments, or external mutations were performed.

GitHub repository `reppiks490/icarus-owner-actions`, branch `main`, file `mission/register.json`, is the sole canonical source of mission status. Supporting storage and agent traces must never override, duplicate as authoritative, or independently advance that status. This document makes no claim about the branch's current contents or completion state.

## Supabase: private metadata only

Use a dedicated schema such as `icarus_support_private`, excluded from the Data API's exposed schemas. Store only an allowlisted evidence category, a public canonical commit reference, opaque local correlation identifiers, timestamps, and a digest of an already sanitized artifact. Do not store vendor response bodies, prompts, conversation histories, tool arguments, provider account references, credentials, contact details, or provider resource URLs.

Schema exposure, object grants, and row policies are independent controls: excluding the schema reduces the API surface; revoking role access denies object access; RLS governs permitted rows. Supabase documents explicit grants and recommends a dedicated API schema for deliberate exposure. [Securing your API](https://supabase.com/docs/guides/api/securing-your-api)

Enable and force RLS on private tables as an additional safeguard. Start without grants or permissive policies for `anon`, `authenticated`, or `service_role`. Any future worker must use an explicitly reviewed role, minimal object privileges, and policies matching its actual access model. Superusers and roles with `BYPASSRLS` remain privileged; a service-role key cannot be treated as proof of row isolation. Review default privileges for the actual object-creating role, since defaults are role-specific. [Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security)

The companion `supabase-metadata-blueprint.sql` is **UNAPPLIED and unvalidated on PostgreSQL**. It ends with `ROLLBACK`, is not a migration, and deliberately provides no runtime access. Schema exposure settings cannot be established by this file. No connected project configuration or privilege inheritance was inspected.

Before adoption, a separate authorized implementation should verify exposed schemas, grants, inherited privileges, RLS enforcement, tenant separation if needed, absence of privileged API functions, and denial from anonymous/authenticated contexts. None of those live checks occurred here.

## Agent workflow: bounded, auditable support

Proposed flow: intake validator → coordinator → documentation or evidence specialist → artifact validator → reviewable local output. GitHub status is read as evidence only. Spend caps, tool permissions, and mutation authorization are application controls at the tool boundary; model instructions alone cannot enforce them. This blueprint assumes a caller-owned workflow requiring SDK handoffs and guardrails. It does not select or instantiate a hosted Agents API session.

Define one fixed specialist destination per SDK handoff. Supply a narrow structured reason, validate it in `on_handoff` before side effects, and filter every history-bearing field before forwarding. `input_type` validates handoff arguments but does not replace conversation history; `is_enabled` does not authorize argument values. Handoffs are outside the function-tool guardrail pipeline. [Handoffs](https://openai.github.io/openai-agents-python/handoffs/)

Use deterministic blocking intake checks before any potentially charged or mutating action. Agent input guardrails apply at entry and output guardrails at final output; checks needed for every function call belong on the function-tool boundary. Hosted and built-in tools require their own authorization wrappers because they do not share that pipeline. Output checks occur after execution and cannot undo prior effects. Reject unauthorized spend and mutations before execution. [Guardrails](https://openai.github.io/openai-agents-python/guardrails/)

SDK tracing is enabled by default and may include sensitive inputs and outputs. A future implementation should disable sensitive-data capture and replace default processors before creating traces. A single application-owned exporter must serialize, allowlist/redact, and deliver sanitized copies; if redaction fails, discard the batch without payload logging. Merely adding a redaction observer leaves the default exporter active. Store only safe event categories and locally generated correlation values in supporting storage. [Tracing](https://openai.github.io/openai-agents-python/tracing/)

## Lookup evidence and limits

- Callable Supabase documentation metadata: `mcp__codex_apps__supabase_search_docs`, accepting GraphQL `graphql_query`.
- No dedicated OpenAI Developers documentation search/fetch tool was present in the available tool metadata. The visible `openai_platform` tools concern key setup/dashboard access and were not used.
- Free public-page lookup used `mcp__codex_apps__search_service_web_run` to read the official OpenAI-maintained SDK documentation linked above. All three pages returned HTML successfully.
- Supabase query `private schema exposed schemas grants row level security service role` with limit 3 returned `Advanced pgTAP Testing`, `Postgres Changes`, and `Securing your API`. Query `Securing your API` with limit 2 returned that guide and `Build a Product Management Android App with Jetpack Compose`. Query `Row Level Security` with limit 1 returned that guide alone. The narrower official security guides supply the design evidence.
- The skill-requested `https://supabase.com/changelog.md` lookup failed because the browser reported unsupported `text/markdown`; direct shell retrieval failed because the configured proxy was unreachable. The HTML [changelog](https://supabase.com/changelog) opened successfully, but a complete relevant breaking-change review was not performed. This limits implementation readiness.
- Only synthesized notes and public documentation links are retained here. No raw vendor payloads or connected-account data were written to these artifacts.
