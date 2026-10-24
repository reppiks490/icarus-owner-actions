# ICARUS multi-chat START HERE

## Current working stopping point: begin phone pairing

Owner's latest direction is to find a working stopping point and begin mobile connection now. Retain the currently working PC engine and settings; new subsystem/defaults work is paused. This supersedes the earlier order to wait for a full PC restart before reconnecting the phone.

Use the [current phone commands](https://github.com/reppiks490/Icarus/blob/main/docs/PHONE_ACCESS.md), [restart checkpoint](https://github.com/reppiks490/Icarus/blob/main/docs/recovery/PRIME_AS_IS_RESTART.md), and [HIGHLY IMPORTANT asset settings](https://github.com/reppiks490/Icarus/blob/main/docs/recovery/HIGHLY_IMPORTANT_RESTART_INFO.md). Main documentation commit `715e6229f6ba1fdc0af58972bdf67c36673d3d5d` archives interim old restart notes exactly and contains no runtime merge. The phone command fetches immutable Git objects and executes only the hash-verified, standard-library relay; it does not switch/restart the working desktop engine.

Phone correction: `8ec6199d0133db345b4ea81ef89f7519b3bf238f`, tree `d713310928c8f779f8e085e4e898f17180b4452a`, on draft [PR #471](https://github.com/reppiks490/Icarus/pull/471). Only `icarus_engine/phone_access_proxy.py` and its test changed from candidate3122. It permits workspace/revision CORS request headers and exposes response identity headers while preserving exact Origin and bearer validation. Source SHA256 `568e11f718a202609c81309f90b7ff76d4a54d6156d89dd81ac032e243636464`. Fresh evidence: 37 proxy checks passed; independent three regressions passed; actual Python3.10 launch rehearsal seven cases passed. Physical PC/phone connectivity remains unverified until owner readback. Optional command gateway8792 is not needed for observation; relay8790 routes engine APIs to8791.

Full restart is **HELD**. Candidate `3122d349524fbce803970dc34ab6fc74dad87467` locally passed4152runtime checks,128skipped,111subtests and107Chromium; both exact-head hosted Linux full suites passed. Both Windows full suites failed8.3shortpath handling and stopped-port timeoutfixture; visualCI failed power/startup browser coverage. These are pending gates. Do not present the candidate as all-green or deploy it just for mobile. The dirty forced-delay browser experiment is saved as unshipped WIP, not included in the mobile commit. New head automatic checks are in progress and are not claimed passing.

Owner asset requirements remain: every Main/CC asset inherits actual current Main NQ strategy/chart defaults, except BOTH ETHUSD and SOLUSD:30-minute timeframe, RTH/session filtering disabled, quantity input25. Journals, asset selections, CC power and native economics must be preserved. Full default migration waits for the remaining verification repairs.

State: **WAITING_OWNER_PC_MOBILE_PAIRING; FULL_RESTART_HELD**. Permanent worker `icarus2`, session `icarus2-20261020-federation-integration`, retains functional Prime role; original Prime remains stopped. The mega-loop remains cancelled, paused specialists stay paused. No live broker arming, main runtime merge, spending, provider collection, training or scheduler change is implied. Full-system readiness remains NO_GO; execution_authorized=false; all_icarus_requirements_complete=false.

## Current recovery direction

The newer owner takeover and stopping-point instructions supersede the primary-worker assignment in the [20 October two-worker direction](directives/2026-10-20-icarus-two-worker-recovery.md). Original source identities and immutable evidence remain intact; do not impersonate the stopped sessions or resume their jobs. Historical directives and unresolved research/provider gates remain evidence, not authority to expand the delivered restart scope.

## Every time the owner tells a chat to continue

1. Read `coordination/ACTIVE.md`, `coordination/collisions.json`, `coordination/owner_status.json`, and the relevant files under `coordination/directives/` in `reppiks490/icarus-owner-actions`.
2. Create or resume one stable `coordination/sessions/<session_id>.json` for this chat/workstream. Never reuse another chat's session ID.
3. Before changing code, UI, workflows, contracts, research state, or shared docs, publish a `PLAN` or `CLAIM` event with repo-qualified `targets` (`repo` + narrow `path`). Read the compiled state again immediately before mutation.
4. Work continuously on useful non-conflicting scope. Publish `WAITING` when CI/review/provider/external work is pending, but keep progressing on independent work. Publish `UPDATE`, `BLOCKED`, `HANDOFF`, or `RELEASE` whenever the state actually changes.
5. Publish `COMPLETE` only with evidence (PR/head, test/run ID, runtime receipt, artifact, or exact external blocker), then create a durable session summary before old event files are eligible for pruning.

Owner communication preference: read `coordination/directives/2026-10-16-owner-contact-boundary.md`. The owner requests no routine progress pings, questions, or manual-work requests while authorized ICARUS work remains; continue independently and use the shared bus for coordination and blockers.

## Mandatory GitHub-native credential and data access

Every AI unit must read `coordination/directives/GITHUB_NATIVE_DATA_ACCESS.md` before declaring that a credential, API, or shared provider-data path is unavailable.

The federation shares **data-access capability and evidence, not plaintext secret strings**. GitHub Actions Secrets are intentionally injected only at workflow runtime; agents are not expected to read those values back.

For provider/data work, the canonical authority is `reppiks490/Icarus-engine`:

- `AGENT_CREDENTIALS.md`
- `docs/agent-handoffs/GITHUB_NATIVE_CREDENTIALS.md`
- `config/credential_contract.json`
- `config/data_ingestion_manifest.json`
- `.github/workflows/github-native-credential-health.yml`

**Do not search `.env` files, DAV task comments, another AI account, or Plant/operator notes for a shared private key.** Those locations are not federation credential authority. If a chat cannot see plaintext, that is expected; use GitHub Actions and the shared evidence paths in `config/data_ingestion_manifest.json` instead. Only report a credential blocker when the canonical health/manifest or provider response proves one.

## Collision rule

A reservation is a coordination lease, not ownership. Two chats may touch the same target only after both publish explicit mutual `coordination_mode: cooperate` records naming each other. Sibling files are independent; an ancestor-directory reservation conflicts with its descendants inside the same repository. Identically named paths in different repositories do not conflict.

## Cooperation rule

When your work can help another active session, reference that session and publish a `HANDOFF`/`UPDATE` instead of silently duplicating it. When you discover a gap outside your original task, either close it if it is non-conflicting or publish a precise claimable handoff. There is almost always useful work available even while one dependency is waiting.

## Owner constraints currently in force

- Claude is inactive by owner direction with no fixed return date. Its unfinished work is reclaimable; see `coordination/directives/2026-10-16-claude-work-reclamation-queue.md`.
- Live broker arming is disabled. Research, replay, simulation, paper/shadow infrastructure and read-only broker validation may continue, but no live-order authority is to be enabled.
- Do not place plaintext API keys, tokens, passwords, sessions, or licensed raw vendor payloads in coordination records.

## Useful commands

```bash
python -m coordination_fabric validate
python -m coordination_fabric compile
python -m coordination_fabric prune --days 14
```

The generated `ACTIVE.md`, `index.json`, and `collisions.json` are views. Immutable per-chat events and durable summaries are the evidence trail; Git history preserves pruned records.
