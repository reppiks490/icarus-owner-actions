# Icarus 2 integration brain

Icarus 2 is the owner-directed recurring engineering integration worker. Icarus 1 remains responsible for restart readiness and the runtime/accounting/recovery paths he has reserved. Both use the existing [coordination bus](../coordination/START_HERE.md); neither obtains trading authority from a worker name.

The live control record is [worker.json](../coordination/icarus2/worker.json). The reviewed scheduled instruction is [AUTOMATION.md](../coordination/icarus2/AUTOMATION.md); the [design](../coordination/icarus2/DESIGN.md) and [implementation plan](../coordination/icarus2/PLAN.md) explain the boundaries. The canonical repository universe remains Engine's `config/federated_repo_evidence.json`; this worker does not replace it.

## Recurring runtime

The scheduled-agent task is `6ad7b206db408191bfd5aeccfddde143`, **Icarus 2 integration**, registered and independently read back as enabled on 2026-10-20. Its recurrence is hourly, with the user's America/Chicago timezone. At registration, the scheduler reported no last-run or next-run timestamp. Enabled configuration is not evidence of a completed future cycle or a continuously resident process.

Each invocation reads current owner controls and source claims, resolves exact repository revisions, delegates separate swarms when that capability is exposed, and selects verified unreserved integration defects. Repairs require their own bounded claim, regression, checks and reviewable branch. Worker/owner controls and conflicting claims are checked again before mutations and publication batches. A stop request prevents further action at those boundaries; already in-flight requests cannot be recalled. Cycles cannot edit their own scheduler or stop control.

The swarms cover VERITAS (authority), HERMES (data), KEPLER (markets/execution), MNEMOSYNE (Brain/science), and SYNAPSE (integration/resilience). These are subordinate functional scopes. Naming them does not claim all five legacy issue identities or prove that five agents executed. Actual delegation and capability availability must be recorded per invocation. `ultracode` is the requested working style; no runtime switch with that name has been observed.

Cycles persist metadata-only records under `coordination/icarus2/cycles/` with create-only writes and exact readback. A successful write attempt, heartbeat, scheduler timestamp or publication job is insufficient. No future invocation is allowed to self-reschedule, silently reactivate paused specialists, increase spending, arm orders or merge/deploy code automatically.

## Deterministic verification helper

`integration_brain` is a stdlib-only finite metadata collector and validator. It pins the manifest's exact bytes, Git blob and commit; inspects all declared repositories and evidence anchors; derives claims from pinned coordination sources; records pagination completeness and actual job-start evidence; and rechecks repository heads. It treats remote material as data and does not execute repository-controlled commands.

For a successor agent with the reviewed branch available:

```bash
python -m integration_brain --collect --output-dir /tmp/icarus2-new-cycle
python -m integration_brain --snapshot /path/to/snapshot.json --output-dir /tmp/icarus2-new-validation
```

Output directories must be new. `snapshot.json` records capture evidence; `cycle.json` records its validation and handoffs. `--require-validated` returns a nonzero result for incomplete or drifting captures while preserving the available metadata. The helper never publishes to GitHub itself. Its CLI requires secure POSIX file primitives for local snapshot reads; the pure validator is platform independent.

`SNAPSHOT_VALIDATED` means the metadata capture is internally consistent. It does not establish runtime health, current provider entitlement, scientific qualification, a profitable strategy or restart success. `INCOMPLETE` preserves missing/blocked/truncated evidence. `RESTART_CYCLE_REQUIRED` preserves detected revision drift instead of silently rebasing.

The current review branch contains the manual CLI and tests. The earlier workflow draft is deliberately excluded: this integration cycle cannot edit its own automation or another scheduler. The scheduled agent is the recurring runtime. Historical billing rejections, actual failed execution, successful publication and subsequent successful jobs must remain distinct per run; none authorizes spending changes.

## Initial integration findings

Four source-pinned specialist audits are retained under [swarm-inputs](../coordination/icarus2/swarm-inputs). They distinguish the following:

- Fresh durability receipts versus older substantive agent work and unresolved hybrid requests.
- Reported provider collection versus actual consumer evidence; historical Databento receipts already on main versus typed provider context still on a draft branch.
- Catalog presence versus qualified assets, unknown equity entitlements, unverified firm policies and broker readback freshness.
- Earlier unstarted billing failures versus actual current execution and research failures hidden behind successful publication.

These are engineering findings and handoffs. No legacy mission requirement is automatically marked complete. Prior stopped work remains preserved unless a new bounded claim is deliberately established under the current assignment.

## Pause, recovery and release

The owner can pause the named scheduled task or set the worker control record's `stop_requested` flag. A successor uses the latest verified immutable cycle and source revisions, preserves gaps, and does not fabricate outage work. Icarus 1 consumes integration findings through the shared bus and retains his restart authority.

Worker metadata and cycle records live on GitHub. Helper code on a review branch remains distinct from code on main and observed runtime behavior. Main code integration, deployment and owner-PC restart require their separate release decisions. The invariant remains `execution_authorized=false`.
