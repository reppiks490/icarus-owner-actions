# ICARUS Perpetual Saturation and Convergence Architecture

Date: 2026-10-18
Status: APPROVED DESIGN — implementation plan not yet authorized
Repository authority: `reppiks490/icarus-owner-actions`

## 1. Purpose

This specification defines the approved architecture for taking ICARUS from its current post-integration baseline into a continuously evolving, evidence-bound system that maximizes every useful integration except broker arming.

The design has four locked pillars:

1. Family Qualification → Full Saturation
2. Perpetual Five-Agent Convergence Protocol
3. Full Source-Family Saturation + Inference Routing + Cross-Family Intelligence Fabric + Anti-Ceiling Mandate
4. Completion Proof + Failure Engineering + Recovery + Authority Boundaries + Release Governance

The design is intentionally non-terminal. ICARUS may reach a provable convergence baseline, but the agent federation continues discovery, verification, maintenance, and capability expansion afterward.

## 2. Global invariants

The following rules govern every subsystem, provider, model, data source, agent, and release:

- `execution_authorized = false` remains a hard invariant until an explicit owner action changes it.
- Broker adapters, account discovery, paper/shadow execution, reconciliation, order-state logic, risk controls, prop-firm rules, rejects, reconnect handling, and kill switches may be completed; autonomous live-order arming may not be crossed by agents.
- No provider, connector, API, model, corpus, endpoint, field, workflow, repository, instrument, subsystem, or example listed in this specification is a ceiling unless explicitly marked `CLOSED_SET_BY_EXTERNAL_AUTHORITY`.
- Every enumerated example means “including, but not limited to.”
- Discovery completeness requires an explicit search for what was not listed.
- Existing canonical manifests/contracts must be extended or reconciled rather than replaced by parallel competing registries.
- Provider existence, credential possession, entitlement, transport, ingestion, consumption, freshness, licensing, and measured value are separate states.
- Raw licensed/private data must remain within its permitted storage boundary; permitted derivatives, metadata, and provenance may federate according to existing rules.
- No synthetic evidence may be represented as real evidence.
- No research result may be promoted when point-in-time availability, leakage controls, provenance, or holdout integrity are unresolved.
- Maximum utilization means maximum beneficial utilization, not pointless request volume or duplicated inference.
- Zero new spend remains the default unless explicitly approved by the owner.

## 3. Anti-Ceiling Mandate

Any enumeration in ICARUS specifications, Deep Research instructions, agent assignments, schemas, manifests, tests, or documentation is non-exhaustive unless an external authority truly defines a closed set.

Agents must actively search beyond every listed set for additional:

- providers and connectors
- capability families
- endpoints, streams, websocket channels, and bulk feeds
- fields and metadata
- instruments and entities
- models and datasets
- transformations and features
- cross-family interactions
- regimes and temporal resolutions
- consumers and subsystems
- repositories, branches, workflows, artifacts, and PRs
- failure modes and recovery paths
- scientific methods and optimization opportunities

Passing all currently named requirements proves only that the named requirements passed. It never proves that unknown requirements do not exist.

## 4. Family Qualification → Full Saturation

### 4.1 Unit of qualification

The unit of qualification is a complete provider data family, not a handpicked endpoint.

The canonical hierarchy is:

`Provider → Family → Capability → Endpoint/Stream → Field`

Every source must be decomposed across this hierarchy before it can be called understood.

### 4.2 Discovery

For every provider, connector, API, corpus, model source, or research service, ICARUS must enumerate the complete accessible capability-family surface.

This applies recursively to all families and all useful sub-capabilities. Providers must not be stereotyped into a single role. For example, a provider known for options data may also expose fundamentals, macro, institutional, crypto, event, or research data; all such families must be discovered and separately qualified.

### 4.3 Qualification gate

Each family enters rapid empirical qualification across every relevant ICARUS instrument, regime, horizon, subsystem, and consumer.

A family may qualify by demonstrating material value in one or more dimensions, including but not limited to:

- unique information content
- earlier detection
- improved regime discrimination
- better model calibration
- reduced false positives
- improved anomaly recognition
- stronger risk avoidance
- better source confirmation
- superior historical reconstruction
- improved research efficiency
- improved operational reliability
- useful redundancy
- cross-family interaction value

A family does not need to increase raw P&L by itself in order to qualify.

### 4.4 Saturation transition

Once a family qualifies, gradual introduction ends. It enters `SATURATION_REQUIRED` and is driven toward the maximum useful accessible surface permitted by entitlement and infrastructure.

Saturation includes, as applicable:

- maximum useful historical depth
- maximum relevant symbol/entity coverage
- all meaningful fields and metadata
- all useful resolutions and timeframes
- complete pagination traversal
- incremental updates
- websocket/streaming channels
- revision history
- reference data
- status and health events
- automatic gap repair

Maximum speed means maximum useful source-native throughput, not useless polling.

### 4.5 Four acquisition modes

Every saturated family runs four concurrent acquisition modes:

1. `BACKFILL` — acquire useful permitted history as deeply as practical.
2. `LIVE_INGESTION` — continuously acquire new information at the highest sustainable useful rate.
3. `GAP_REPAIR` — compare expected versus observed coverage and repair missing windows, pagination gaps, failed requests, and stale partitions.
4. `CAPABILITY_REDISCOVERY` — re-check documentation, schemas, models, datasets, fields, endpoints, websocket channels, entitlement, and source behavior for newly available capability.

### 4.6 Family states

Families must be machine-classified using states such as:

`DISCOVERED`, `ENUMERATING`, `QUALIFYING`, `QUALIFIED`, `BACKFILLING`, `SATURATING`, `LIVE_SATURATED`, `CONTINUOUSLY_VALIDATED`, `BLOCKED_ENTITLEMENT`, `BLOCKED_TRANSPORT`, `BLOCKED_SECRET_INSTALL`, `LOW_VALUE_CURRENTLY`, `AVAILABLE_LOW_CURRENT_VALUE`, `DEGRADED`, `SCHEMA_DRIFT`, `REQUALIFICATION_REQUIRED`, `RETIRED`.

No useful family may silently disappear from scope.

## 5. Source-to-Decision Fabric

Qualified data must not be dumped directly into Brain or a monolithic payload.

The required flow is:

`Source → Raw/Private Intake → Validation → Canonical Identity Resolution → Normalized Family Store → Feature Factory → Cross-Family Fabric → Evidence/Confidence Layer → Appropriate Consumers`

Every record or derivative should preserve, where applicable:

- provider
- family
- capability
- endpoint/stream
- source event time
- retrieval time
- entity/instrument identity
- entitlement state
- schema version
- revision/version
- freshness
- normalization version
- derivation lineage
- downstream consumer lineage

A provider is not maximally integrated merely because it has a key, connector, workflow, or collector.

`MAXIMALLY_UTILIZED_CURRENT_ENTITLEMENT` requires that all accessible families are discovered and dispositioned, all passing families are saturated, lineage is intact, useful derivatives reach appropriate consumers, cross-family interactions are explored, contribution is measured, health/fallback exists, and every unused capability has an explicit reason.

## 6. Cross-Family Intelligence Fabric

ICARUS must treat cross-family interaction as first-class evidence.

Every qualified family should be evaluated individually, conditionally, and in combination with other plausibly related families across relevant regimes and horizons.

The system should support tests of the form:

- `F_i` alone
- `F_j` alone
- `F_i + F_j`
- `F_i | regime R`
- `F_i + F_j | regime R`

Candidate interactions should be prioritized by shared entity/instrument coverage, temporal proximity, causal plausibility, historical information gain, regime relevance, and complementary information.

Cross-provider disagreement is itself a feature family. ICARUS should derive and track, where meaningful:

- source agreement ratios
- first-detection timestamps
- confirmation latency
- numeric divergence
- revision divergence
- stale-source state
- missing-source state
- historical provider reliability
- confidence-weighted consensus

## 7. Source Universes

Deep Research and the perpetual provider agent must treat all currently connected, screenshot-authorized, repository-listed, publicly available, and subsequently discovered sources as an open universe.

This includes, without limiting scope, sources such as:

- Unusual Whales
- Hugging Face
- Massive
- FMP
- Bigdata
- The Fly
- Zacks
- Bybit
- Blockscout
- Firecrawl
- DataBlue
- Parallel Search
- Scite
- Exa
- Jina AI
- Groq
- Mistral
- OpenRouter
- Cerebras
- Cloudflare Workers AI
- U.S. Gold Bureau Metal Spots
- StackerScan
- SEC/EDGAR
- FRED/ALFRED
- CFTC
- Treasury and central-bank/public economic sources
- Coinbase/Kraken/Binance public sources
- retained private corpora
- historical CSV repositories
- AION, DAEDALUS, Divine Providence, causal-router, and other federated repositories

Screenshot-authorized credentials may be treated as owner-authorized integration candidates even when they are not yet installed in GitHub Actions. Literal secret values are not part of this specification.

## 8. Hugging Face and Open Model Discovery

Hugging Face is a permanent model, dataset, paper, Space, embedding, reranking, time-series, anomaly-detection, and financial-NLP discovery ecosystem.

Every candidate should progress through:

`LICENSE → PROVENANCE → LEAKAGE_AUDIT → RESOURCE_REQUIREMENT → INPUT_COMPATIBILITY → TASK_BENCHMARK → EXISTING_ICARUS_COMPARISON → SHADOW_USE → DISPOSITION`

The goal is not to download more models indiscriminately. The goal is to discover whether any legally usable free/open capability materially improves an ICARUS task.

## 9. Inference Competition and Routing

Inference providers and local/open models must compete on real ICARUS workloads rather than receive permanent roles by assumption.

Applicable tasks include, but are not limited to:

- structured extraction
- contradiction detection
- code analysis
- agent planning
- market-event classification
- long-context synthesis
- scientific critique
- research summarization
- schema mapping
- anomaly explanation
- retrieval reranking
- feature interpretation
- hypothesis generation and criticism
- JSON/schema compliance
- low-latency classification

Each provider/model should be benchmarked on quality, latency, structured-output reliability, context capacity, failure rate, throughput, cost under current entitlement, and disagreement with peers.

A high-value routing pattern is:

`Primary Model → Independent Model-Family Critic → Deterministic Validator → Disagreement Score`

Additional models or external evidence should be invoked only when disagreement or uncertainty warrants escalation.

Probabilistic model output is advisory evidence unless it passes the explicit authority path for a deterministic control decision.

## 10. Retrieval Competition

Retrieval providers must be benchmarked rather than treated as interchangeable.

A retrieval benchmark corpus should include provider documentation, exchange rules, scientific literature, corporate information, broker/prop-firm rules, technical documentation, recent news, and regulatory/public sources.

Measure at minimum:

- unique valid source discovery
- precision
- freshness
- source authority
- latency
- extraction quality
- duplication
- failure rate

The query router should select the best retrieval source or combination for the task.

## 11. Perpetual Five-Agent Convergence Protocol

The five permanent identities are:

### 11.1 VERITAS — Authority & Architecture

Owns repository discovery, subsystem lifecycle, PR/main/branch truth, schema/config authority, documentation drift, duplicated implementations, mission-register reconciliation, governance, and architectural contradictions.

Perpetual question: **What exists that ICARUS does not currently understand accurately?**

### 11.2 HERMES — Data / Provider / Entitlement / Saturation

HERMES replaces the earlier external-agent name ARGOS to avoid confusion with the existing ICARUS subsystem ARGUS.

Owns every provider, API, connector, credential state, entitlement, family, endpoint, stream, field, dataset, rate limit, storage path, freshness SLA, licensing boundary, saturation state, fallback, and capability rediscovery process.

Perpetual question: **What information can ICARUS legitimately access that it is not yet extracting and exploiting at maximum justified capacity?**

### 11.3 KEPLER — Market & Instrument Authority

Owns canonical instrument identity, futures/equity/index/FX/crypto mappings, micro/full relationships, contract economics, sessions, holidays, roll/expiry/first-notice logic, calendars, paper qualification, and broker/prop compatibility.

Perpetual question: **Could any market identity, timing, economics, or execution assumption still be wrong?**

### 11.4 MNEMOSYNE — Evidence / Brain / Science Authority

Owns Brain, ML, statistical evidence, feature lineage, family qualification, model routing, scientific literature, leakage prevention, calibration, regime conditioning, ablation, provenance, synthetic-vs-real integrity, champion/challenger research, and cross-family utility.

Perpetual question: **Is ICARUS extracting all defensible intelligence from everything it knows?**

### 11.5 SYNAPSE — Integration / Resilience / Convergence Authority

Owns system convergence, release integration, CI, Sentinel, runtime health, provider fallbacks, recovery, resets, performance, load/soak/fault tests, cross-agent contradictions, and the final Claude/Codex handoff state.

Perpetual question: **Does everything that should work together actually work together under normal and abnormal conditions?**

## 12. Agent State Machine

No role has a terminal `COMPLETE` state unless the owner explicitly stops it.

Each agent follows:

`CLAIM_IDENTITY → RECONSTRUCT_TRUTH → DISCOVER → TRIAGE → REVIEW → FIX → VERIFY → ADVERSARIAL_REVIEW → CROSS_REVIEW → INTEGRATION_REVIEW → BASELINE_GREEN → GENERATE_SUCCESSOR_CRITERIA → NEXT_EPOCH`

Every satisfied exit criterion must generate successor criteria.

After `BASELINE_GREEN`, the role transitions into continuous evolution rather than stopping.

### 12.1 Successor-criterion hierarchy

Each new epoch must search progressively through:

1. regression
2. known gaps
3. coverage gaps
4. contradictions
5. orphans
6. negative space
7. adversarial failure
8. efficiency opportunities
9. newly available capabilities
10. frontier combinations and new useful capability

Then the cycle restarts against the changed system.

### 12.2 Review rule

A material task follows:

`Initial Audit → Fix/Implementation → Self-Review From Scratch → Fix → Independent-Agent Challenge → Fix → Machine/Runtime Verification → Deliberate Missed-Case Hunt → Fix → Fresh Review`

A task reaches `BASELINE_GREEN` only when two consecutive independent review passes find no new material internally controlled defect and all applicable automated/runtime verification is green.

A later finding automatically reopens the task.

### 12.3 No-idle rule

Agents must not invent changes to appear busy.

If an epoch finds no justified modification, it records `NO_CHANGE_JUSTIFIED` with the exact evidence/SHAs examined, categories inspected, tests performed, rejected candidate improvements, reasons, and the next reevaluation trigger, then moves to another discovery category.

### 12.4 Cross-agent forcing function

No consequential domain may be unilaterally certified by the same agent that changed it.

For material closure:

- one specialist owns the work
- a different specialist challenges it
- SYNAPSE verifies integration consequences
- automated/runtime evidence verifies behavior

Any agent may reopen another agent’s green work when new evidence invalidates it.

## 13. Completion Proof and Dependency Closure

A capability is not complete because it exists. It is complete only when ICARUS can prove what it is, where it came from, whether it works, how it fails, how it recovers, what depends on it, what authority it has, and how to reproduce the exact working state.

Lifecycle states should distinguish at least:

`UNDISCOVERED`, `DISCOVERED`, `UNDER_REVIEW`, `IMPLEMENTING`, `VERIFYING`, `BASELINE_GREEN`, `CONTINUOUS_EVOLUTION`, plus degraded/blocked/superseded/quarantined/requalification states.

Completion is closed over the dependency graph. A downstream component cannot be fully green while a required upstream dependency is unknown, stale, contradictory, or unverifiable.

If the expected universe itself is unknown, the state is `COVERAGE_BOUND_UNKNOWN`, not complete.

## 14. Fault Injection

Controlled fault injection is part of normal verification.

Agents must test failures including, but not limited to:

- provider outage
- authentication expiration
- HTTP errors and rate limits
- websocket disconnects
- schema drift
- stale, duplicated, delayed, reordered, malformed, or incomplete data
- impossible timestamps and clock skew
- missing pagination pages
- partial/corrupt files and checksums
- disk pressure
- database locking
- interrupted writes
- process crashes
- port collisions
- browser/mobile disconnects
- restart mid-position
- dependency-version changes
- downstream lag

The expected behavior is fail-closed operation, preserved evidence, explicit error surfacing, no invented data, safe recovery, and a reconstructable incident record.

## 15. Recovery Authority Manifest

Every durable component must have a canonical recovery record containing:

- repository/ref
- bootstrap/install method
- dependencies
- state location
- restart method
- non-destructive refresh
- destructive reset if legitimate
- backup method
- restore method
- rollback method
- verification command
- expected preserved state
- expected cleared state
- recovery duration

Recovery must be demonstrated at three tiers:

1. process recovery
2. state recovery
3. clean-environment reconstruction

Critical subsystems should define RPO and RTO targets and improve them where practical.

## 16. Persistent-State Integrity

Deep Research and SYNAPSE must map every durable store across Git, JSON, SQLite/journals, encrypted provider evidence, model artifacts, CSV corpora, and any subsequently discovered store.

The audit must cover:

- schema versioning
- migrations
- transactional boundaries
- atomicity
- locking/concurrency
- idempotency
- duplicate detection
- referential integrity
- checksums
- corruption detection
- retention
- archival
- restoration

Cross-store and documentation references must be continuously scanned for dangling paths, SHAs, PRs, issue IDs, workflow IDs, artifact IDs, schemas, models, datasets, provider IDs, subsystem names, and reset commands.

## 17. Runtime Identity and Reproducibility

Every running command center or critical service should expose enough identity to prove exactly what is running, including where applicable:

- software SHA/release
- configuration digest
- schema versions
- instrument/economics version
- evidence snapshot IDs
- model versions
- feature versions
- migration state
- startup timestamp
- environment mode

Software release identity, evidence snapshot identity, runtime deployment identity, and research experiment identity must remain distinct.

Research conclusions must be reproducible from code revision, evidence snapshot, parameters, feature versions, model versions, random seeds where relevant, environment, and experiment metadata.

## 18. Release Governance

A consequential release may advance only after applicable specialist review, cross-agent challenge, automated tests, exact-head CI, integration verification, and runtime evidence.

Each release proof packet should identify:

- what changed
- why it changed
- exact source SHA
- dependencies
- tests and validation
- failures encountered
- recovery behavior
- performance impact
- schema/data migrations
- rollback instructions
- unresolved external blockers

Open PRs and branches must be continuously reconciled into one of:

`MERGE`, `REBASE`, `SPLIT`, `SUPERSEDE`, `CLOSE`, `KEEP_ISOLATED_RESEARCH`, `EXTERNALLY_BLOCKED`.

Forgotten ambiguous stacks are not acceptable.

## 19. Security and Authority Boundaries

Security is represented as explicit authority, not a generic warning.

At minimum distinguish:

- research/read-only
- data acquisition
- artifact writing
- configuration modification
- paper execution
- broker connectivity
- live-order preparation
- live execution

Components receive only the authority required for their function.

External AI/model output may not silently mutate deterministic risk limits, canonical market identities, execution authorization, or credential policy.

Retrieved external text is always treated as data, never as trusted control instructions. Prompt-injection and hostile-document handling are mandatory parts of the retrieval/data plane.

## 20. Performance, Backpressure, and Soak Verification

Aggressive saturation requires explicit backpressure and priority handling.

When resources contend, ICARUS must prioritize latency-sensitive realtime evidence above recoverable incremental data, historical backfill, and low-priority rediscovery work.

The expected response to overload is controlled queueing, spillover, prioritization, retry, and gap repair—not silent data loss.

Load and soak testing must reflect the actual system, including combinations of:

- four simultaneous command centers
- large asset selections
- A200 research activity
- saturated provider families
- continuous feature derivation
- agent evidence traffic
- growing journals
- browser/mobile reconnects
- multiple retrieval/model providers
- historical gap repair

Measure memory growth, CPU, storage growth, queue depth, event latency, UI responsiveness, consumer lag, duplicate processing, dropped messages, deadlocks, reconnect time, and long-duration stability.

Performance regression can reopen otherwise functionally green work.

## 21. Scientific and Temporal Integrity

The following distinctions remain hard research gates:

- real fills vs synthetic fills
- tuning vs holdout
- historical vs point-in-time evidence
- observation vs inference
- correlation vs causality
- present-day availability vs historical availability

Every model and dataset should carry temporal availability semantics such as `available_as_of`, revision state, and publication timing where relevant.

A source family cannot introduce lookahead contamination merely because it improves historical results.

## 22. Cost and Budget Behavior

Perpetual agents must never equate “keep working” with “keep spending.”

When a metered source or experiment budget is exhausted, the role switches to free/public providers, cached evidence, code/reliability work, historical analysis, scientific research, feature work, cross-family analysis, or other zero-new-spend activity until permitted capacity returns.

No agent may manufacture paid calls without explicit authorization.

## 23. Definition of ICARUS Convergence

The highest pre-broker state is:

`ICARUS_CONVERGENCE_GREEN_BROKER_LOCKED`

This state may be declared only when, to the best evidence currently available:

- all discovered internally controllable requirements are satisfied
- the owner mission register is reconciled
- the relevant repository universe is closed or explicitly unresolved
- all subsystems have current lifecycle/authority states
- all useful available integrations are operational or explicitly blocked
- all provider families are dispositioned and passing families are saturated
- downstream consumption is proven
- cross-family intelligence has been explored sufficiently to establish a current baseline
- instrument/economics/session/calendar identities are qualified
- historical contamination is resolved or explicitly labeled
- research-integrity gates hold
- model/data provenance is intact
- Sentinel/CI/internal health contains no unexplained internally controlled failures
- reset, recovery, and disaster-recovery paths are proven
- open development work is dispositioned
- runtime identity is reproducible
- load, soak, fault, and adversarial verification is green
- all remaining blockers are demonstrably external, owner-deferred, or the explicitly withheld broker-arming boundary

This state is not terminal.

It transitions immediately to:

`CONTINUOUS_EVOLUTION`

where the five agents continue successor epochs indefinitely until explicitly stopped by the owner.

## 24. Deep Research Deliverables Required by This Design

The next Deep Research phase must produce implementation-grade evidence, not merely observations.

Its outputs must include at minimum:

- post-current-main repo/PR/branch authority snapshot
- complete subsystem lifecycle registry
- mission-register reconciliation
- full provider/family/capability/endpoint/field exhaustiveness ledger
- entitlement/credential/transport/ingestion/consumption/freshness/licensing/value matrix
- provider-to-consumer lineage graph
- source-confidence and disagreement design
- family qualification results and saturation dispositions
- current saturation/backfill/gap-repair state
- complete inference/model capability benchmark plan and results where executable
- retrieval-provider benchmark plan and results where executable
- instrument/execution-qualification matrix
- historical-contamination audit
- Brain/ML/evidence-utilization graph
- open-PR disposition and convergence plan
- Sentinel/CI/runtime health baseline
- recovery authority manifest
- persistent-store/schema/migration map
- fault/load/soak verification plan and findings
- authority/security map
- exact reset/recovery commands for current stable components
- final repository-ready implementation queue
- final Claude/Codex handoff artifact

The final Deep Research synthesis must perform a delta rescan immediately before completion so that changes made during research are reconciled rather than silently omitted.

## 25. Non-Goals of This Design Phase

This document is a design specification only.

It does not itself authorize:

- live broker arming
- paid-provider purchases
- implementation changes to production code
- mutation of the five GitHub agent issues
- secret installation
- merging experimental research branches

Those actions require the implementation plan and the normal verification/review path.
