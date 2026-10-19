# ICARUS Perpetual Saturation Master Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the approved perpetual-saturation architecture into a coordinated, testable five-agent operating system and implementation program without enabling live broker execution.

**Architecture:** This master plan decomposes the approved design into five independently testable subplans: perpetual coordination, provider-family saturation, evidence/inference intelligence, recovery/governance, and final Deep Research convergence. The subplans share exact artifacts through GitHub rather than chat memory; each can ship independently and exposes machine-readable outputs consumed by the next stage.

**Tech Stack:** Python 3 stdlib coordination/mission tooling, JSON manifests, GitHub Actions, pytest, Markdown control-plane docs, existing ICARUS/Icarus-engine runtime and Sentinel evidence.

**Spec:** `docs/superpowers/specs/2026-10-18-icarus-perpetual-saturation-convergence-design.md`

## Global Constraints

- `execution_authorized = false` remains a hard invariant until explicit owner action changes it.
- Zero new spend unless explicitly owner-approved.
- No plaintext secrets or restricted raw vendor payloads in repository records.
- Existing canonical manifests/contracts are extended or reconciled; no parallel competing registries.
- Every enumeration is non-exhaustive unless explicitly `CLOSED_SET_BY_EXTERNAL_AUTHORITY`.
- Provider existence, credential possession, entitlement, transport, ingestion, consumption, freshness, licensing, cost, and measured value remain separate states.
- Synthetic evidence may never masquerade as real evidence.
- Passing named requirements never proves the unknown universe is closed; every convergence pass includes explicit negative-space discovery.

## Review Focus

- Stale role/issue names after ARGOS→HERMES: every claim, handoff, directive, and generated view must resolve to one canonical identity.
- Agent loop termination: satisfying exit criteria must generate successor criteria instead of emitting terminal completion.
- Provider saturation overreach: throughput must remain bounded by entitlement, licensing, source-native update rate, backpressure, and zero-new-spend policy.
- Evidence contamination: new provider/model data must preserve point-in-time availability and cannot bypass research promotion gates.
- Recovery/release mismatch: a green repository SHA is insufficient if the running process, evidence snapshot, or persisted state cannot be reproduced.

---

### Task 1: Implement the perpetual five-agent coordination contract

**Files:**
- Plan: `docs/superpowers/plans/2026-10-18-perpetual-agent-coordination.md`
- Modify: `coordination/START_HERE.md`
- Modify: `coordination/directives/2026-10-19-five-agent-final-convergence.md`
- Modify: GitHub issues #54–#59
- Modify: `coordination_fabric/__init__.py`
- Modify: `tests/test_coordination_fabric.py`
- Modify: `tests/test_coordination_maintenance_hardening.py`

**Interfaces:**
- Consumes: approved design spec; existing `icarus-coordination-event-v2` and session/event compiler.
- Produces: canonical five-role identities, `BASELINE_GREEN`/successor-epoch semantics, machine-checkable non-terminal role lifecycle, role-claim compatibility rules.

- [ ] Implement and verify the full subplan `docs/superpowers/plans/2026-10-18-perpetual-agent-coordination.md`.
- [ ] Verify `python -m coordination_fabric validate` succeeds against the repository tree.
- [ ] Verify focused tests for role claims, successor criteria, stale ARGOS rejection/compatibility migration, and no terminal completion for perpetual roles.
- [ ] Commit the coordination lane as one reviewable change.

### Task 2: Implement provider-family qualification and saturation control

**Files:**
- Plan: `docs/superpowers/plans/2026-10-18-provider-family-saturation.md`
- Modify: `reppiks490/Icarus-engine/config/credential_contract.json`
- Modify: `reppiks490/Icarus-engine/config/data_ingestion_manifest.json`
- Modify: `reppiks490/Icarus-engine/config/provider_endpoint_catalog.json`
- Modify: `reppiks490/Icarus-engine/config/federated_repo_evidence.json`
- Create: `reppiks490/Icarus-engine/config/provider_family_registry.json`
- Create: provider-family registry validator/tests under existing Icarus-engine test layout.

**Interfaces:**
- Consumes: canonical provider/credential/endpoint manifests, current provider receipts and Sentinel health.
- Produces: family-level states, acquisition modes, saturation dispositions, coverage denominator, entitlement/licensing/freshness/value fields, exact consumer/fallback ownership.

- [ ] Implement and verify the full subplan `docs/superpowers/plans/2026-10-18-provider-family-saturation.md`.
- [ ] Validate every canonical provider has at least one explicit family disposition or a machine-readable unresolved classification.
- [ ] Verify no provider is called fully integrated without consumption evidence.
- [ ] Commit family-registry/manifest changes separately from runtime collectors.

### Task 3: Implement evidence-to-decision, model routing, retrieval competition, and cross-family intelligence

**Files:**
- Plan: `docs/superpowers/plans/2026-10-18-evidence-inference-cross-family.md`
- Reconcile: PR #457 or its successor against current `reppiks490/Icarus` main.
- Create/modify: Brain/provider-context consumer modules in `reppiks490/Icarus` using the existing provider-statistics path.
- Create: inference/retrieval benchmark manifests and result schemas in `reppiks490/Icarus-engine`.
- Modify: Sentinel/health inputs for consumer-read and family-value evidence.

**Interfaces:**
- Consumes: provider-family registry from Task 2, exact point-in-time evidence snapshots.
- Produces: provider→feature→consumer lineage, family qualification evidence, model/retrieval routing scores, disagreement/confidence features, explicit unused-capability reasons.

- [ ] Implement and verify the full subplan `docs/superpowers/plans/2026-10-18-evidence-inference-cross-family.md`.
- [ ] Ensure no probabilistic model output can directly change deterministic execution/risk authority.
- [ ] Verify point-in-time and synthetic/real boundaries with focused tests.
- [ ] Commit research/consumer changes only after exact-head tests are green.

### Task 4: Implement recovery, fault injection, runtime identity, and release governance

**Files:**
- Plan: `docs/superpowers/plans/2026-10-18-recovery-governance-convergence-proof.md`
- Create: canonical reset/recovery manifest in `reppiks490/icarus-owner-actions`.
- Modify: Icarus command-center runtime identity/status surfaces.
- Modify: Sentinel/CI health evidence where needed.
- Add: recovery/fault/load tests in the owning repositories.

**Interfaces:**
- Consumes: runtime SHA/config/evidence/model identities; current restart commands; persistent-state locations.
- Produces: machine-readable recovery authority, runtime fingerprint, fault/soak evidence, release proof packet, `ICARUS_CONVERGENCE_GREEN_BROKER_LOCKED` gate.

- [ ] Implement and verify the full subplan `docs/superpowers/plans/2026-10-18-recovery-governance-convergence-proof.md`.
- [ ] Demonstrate process, state, and clean-environment recovery for critical components.
- [ ] Verify broker arming remains disabled through all recovery and release paths.
- [ ] Commit recovery/governance changes independently of research promotion changes.

### Task 5: Run the final Deep Research convergence commission and feed the five lanes

**Files:**
- Plan: `docs/superpowers/plans/2026-10-18-final-deep-research-convergence.md`
- Create: final Deep Research commission under `coordination/directives/`.
- Create/update: agent handoff artifacts under `coordination/handoffs/`.
- Update: issue #59 and role issues with the approved perpetual contract after implementation review.

**Interfaces:**
- Consumes: Tasks 1–4 artifacts plus current repo/PR/Sentinel/provider state at launch time.
- Produces: delta-reconciled authority graph, full capability ledger, saturation dispositions, instrument matrix, evidence-to-decision graph, recovery manifest findings, implementation queue, Claude/Codex handoff.

- [ ] Implement and verify the full subplan `docs/superpowers/plans/2026-10-18-final-deep-research-convergence.md`.
- [ ] Perform a fresh repo/PR/Sentinel snapshot immediately before launch.
- [ ] Require final delta reconciliation before synthesis.
- [ ] Feed new defects back to the owning perpetual role instead of closing the program.

### Task 6: Whole-program verification and transition to continuous evolution

**Files:**
- Modify: final convergence directive and handoff artifacts only after Tasks 1–5 pass.
- Update: `mission/register.json` through the mission compiler/evidence process rather than manual blanket status changes.

**Interfaces:**
- Consumes: verified outputs of Tasks 1–5.
- Produces: reproducible pre-broker convergence decision and successor-epoch queue.

- [ ] Run owner-actions tests: `pytest -q` and `python -m coordination_fabric validate`.
- [ ] Run applicable Icarus-engine and Icarus exact-head test suites/CI identified in the subplans.
- [ ] Verify every open PR/workstream has a disposition and every internally controlled failing health check is fixed or reopened to an owner lane.
- [ ] Verify `execution_authorized=false` in every canonical authority surface.
- [ ] If all pre-broker criteria pass, record `ICARUS_CONVERGENCE_GREEN_BROKER_LOCKED` and immediately generate `CONTINUOUS_EVOLUTION` successor criteria rather than terminating the five roles.
- [ ] Commit the final convergence evidence/handoff packet.
