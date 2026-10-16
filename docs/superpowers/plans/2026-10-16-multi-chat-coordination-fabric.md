# Multi-Chat Coordination Fabric Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a scalable, collision-aware coordination bus for dozens of ICARUS chats, federate it into every repo, expose it read-only in the Engine UI, and reclaim Claude-stalled work without model ownership gates.

**Architecture:** `icarus-owner-actions` stores per-session registration and immutable per-event files; a deterministic Python compiler generates `index.json`, `ACTIVE.md`, and `collisions.json`. All repos point agents to the bus. Icarus Engine consumes only the compiled read-only view for its dashboard.

**Tech Stack:** Python stdlib, JSON, Markdown, GitHub Actions, existing Icarus Engine stdlib HTTP server/dashboard.

**Spec:** `docs/superpowers/specs/2026-10-16-multi-chat-coordination-fabric-design.md`

## Global Constraints

- No live broker arming.
- No plaintext secrets or licensed raw payloads in coordination records.
- No model-family ownership gates.
- Intent note before substantial mutation; waiting note while CI/review/external dependency blocks progress.
- Completion requires fresh evidence.
- Central writes must avoid a single append-only hot file.

## Review Focus

- Concurrent sessions claiming ancestor/descendant paths must surface a collision unless explicit cooperation exists.
- Stale or Claude-owned legacy work must become reclaimable without being silently marked complete.
- Cleanup must never remove nonterminal sessions or terminal sessions lacking a durable summary.
- Invalid/malicious paths, timestamps, or event types must fail closed.
- UI consumption must remain read-only and tolerate an unavailable coordination bus.

---

### Task 1: Core record compiler

**Files:**
- Create: `coordination_fabric/__init__.py`
- Create: `coordination_fabric/__main__.py`
- Create: `tests/test_coordination_fabric.py`
- Create: `.github/workflows/coordination-fabric.yml`

**Interfaces:**
- Consumes: files under `coordination/sessions`, `coordination/events`, `coordination/summaries`.
- Produces: `compile_state(root: Path, now: datetime) -> dict`, `render_active(state: dict) -> str`, CLI validate/compile/prune.

- [ ] Write tests for valid compilation, malformed records, collision detection, cooperation exemption, waiting state, stale state, Claude-inactive metadata, and safe pruning.
- [ ] Run PR CI and confirm the tests fail because `coordination_fabric` does not exist.
- [ ] Implement the minimal compiler/CLI.
- [ ] Run focused and full owner-actions tests.

### Task 2: Protocol, templates, and generated coordination state

**Files:**
- Create: `coordination/README.md`
- Create: `coordination/schema/session.example.json`
- Create: `coordination/schema/event.example.json`
- Create: `coordination/owner_status.json`
- Create: initial session/event records for this work.
- Modify: `AGENTS.md`

**Interfaces:**
- Consumes: compiler from Task 1.
- Produces: human instructions and machine examples all chats can copy.

- [ ] Add contract tests requiring pre-work notes, waiting notes, no agent gating, and central bus references.
- [ ] Generate `coordination/index.json`, `coordination/ACTIVE.md`, and `coordination/collisions.json` from fixtures/live records.
- [ ] Verify zero malformed records and zero undeclared collisions for this session.

### Task 3: Claude work reclamation and mass-worker directives

**Files:**
- Create: `coordination/directives/2026-10-16-claude-reclamation.md`
- Create: `coordination/directives/2026-10-16-mass-chat-operating-contract.md`
- Create: a `PLAN`/`UPDATE` event advertising the futures expansion paths once selected.

**Interfaces:**
- Produces: explicit instruction that Claude inactivity removes exclusive ownership and that all chats divide-and-conquer using reservations/cooperation notes.

- [ ] Test that directives prohibit model ownership gates and require handoff/dependency notes.
- [ ] Enumerate known Claude lanes from Engine coordination records as reclaimable categories without marking unfinished work done.

### Task 4: Cross-repository adoption

**Files:**
- Modify/create `AGENTS.md` in `Icarus-engine`, `Icarus`, `divine-providence`, `icarus-causal-router`, `icarus-csv-evidence-lab`, and `icarus-owner-actions`.
- Preserve existing repo-specific safety/evidence rules.

**Interfaces:**
- Produces: universal entrypoint to owner-actions coordination bus.

- [ ] Add or update repo-local contract tests where practical.
- [ ] Ensure legacy two-agent rules are explicitly historical/superseded where they conflict.

### Task 5: Engine read-only coordination API and dashboard panel

**Files:**
- Modify/create focused Engine modules after inspecting current server/dashboard patterns.
- Test: Engine API/dashboard tests.

**Interfaces:**
- Produces: `/api/coordination` read-only snapshot plus dashboard panel/table.

- [ ] Write failing fixture-based API/UI tests first.
- [ ] Implement bounded cached read of the public compiled coordination state with safe offline fallback.
- [ ] Add dashboard visualization of session, phase, repo, branch/PR, latest note, wait reason, reservations, dependencies, and collisions.
- [ ] Run Linux/Windows Engine tests.

### Task 6: Futures universe research and collision-free integration

**Files:**
- Research artifact: Engine docs/coordination records.
- Modify asset registry/feed/calendar/UI/test files only after collision audit and public exchange/source verification.

**Interfaces:**
- Produces: at least 10 newly selected high-value futures roots plus eligible micro counterparts, all discoverable by Engine/UI and paper-runtime paths; live broker arming stays disabled.

- [ ] Audit open PRs/branches and current registry for overlapping asset work.
- [ ] Research liquidity, diversification, macro sensitivity, contract specs, tick values, sessions, data-source mapping, and micro equivalents from current official exchange/source material.
- [ ] Publish selected symbols and intended paths to the coordination bus before edits.
- [ ] Write failing registry/feed/UI tests for the selected universe.
- [ ] Implement registry/feed/calendar/runtime/UI support with source-accurate contract metadata.
- [ ] Verify bars/source identity where accessible; mark unsupported live-source mappings explicitly rather than pretending tradability.
- [ ] Run focused plus full Engine suites and read-only runtime/UI smoke checks.

### Task 7: Merge and post-merge verification

- [ ] Finish existing Engine #178 and Icarus #397 verification; merge only exact green heads.
- [ ] Merge coordination fabric and futures changes only after exact-head CI is green.
- [ ] Re-run main-branch health/coordination checks and record a final `COMPLETE` event with run/PR evidence.
