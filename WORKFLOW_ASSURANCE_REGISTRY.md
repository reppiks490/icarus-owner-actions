# ICARUS research assurance registry

This register gives the owner-facing ICARUS layer one place to understand the
assurance state of the three Python research siblings.

It is an observability register, **not** an execution-control surface. It does
not authorize orders, certify an edge, spend protected holdouts, or promote a
model.

## Current components

| Component | Workflow | Current state | Authority |
|---|---|---|---|
| `aion-parallax-research` | `AION / PARALLAX assurance` | Operational; latest verified main workflow run passed | Read-only research |
| `daedalus-research-os` | `DAEDALUS research assurance` | Public runner restored; scheduled assurance run 37639188767 attempt 3 **passed** | Research only |
| `icarus-causal-router` | `ICARUS causal-router assurance` | Public runner restored; run 37644317860 attempt 3 **failed in unit tests**, missing `causal_router.journal` | Research only |

The machine-readable source of truth is
[`intake/research_assurance_registry.json`](intake/research_assurance_registry.json).

## What each workflow now provides

The three repositories have a common assurance shape:

- push / pull-request / manual validation;
- merge-queue coverage;
- a reduced-cost scheduled drift path;
- supported Python-version testing appropriate to each repository;
- compilation and dependency consistency checks;
- package build/install verification;
- repository-specific scientific or replay firewalls;
- a final aggregate assurance gate;
- machine-readable `assurance-summary.json` artifacts with 30-day retention;
- weekly Dependabot maintenance for GitHub Actions and Python packaging metadata.

AION additionally validates its JSON contracts, cockpit JavaScript, synthetic
replay, and installed CLI package. DAEDALUS additionally enforces its static
research audit, ResourceWarning failures, and a coverage floor. Causal Router
additionally verifies deterministic seeded replay and hard-codes that synthetic
results cannot become market validation or a profitability claim.

## Artifact contract

Successful aggregate jobs upload one JSON evidence document whose fields include:

- repository and workflow identity;
- run ID and run attempt;
- event, commit SHA, and ref;
- generated timestamp;
- component authority / execution permissions;
- individual gate results;
- aggregate result.

This shape is intentionally suitable for a future ICARUS UI assurance panel or
owner automation without giving the research repositories order authority.

## Runner restoration and new code-level blocker (2026-10-07)

Owner-authorized visibility changes made DAEDALUS, Causal Router, and Owner Actions public. The previously blocked hosted runners have now actually executed steps. DAEDALUS scheduled assurance run [37639188767](https://github.com/reppiks490/daedalus-research-os/actions/runs/37639188767) passed on attempt 3. Causal Router [37644317860](https://github.com/reppiks490/icarus-causal-router/actions/runs/37644317860) reached its Python suite and failed: `ModuleNotFoundError: No module named 'causal_router.journal'`.

Do not treat this as either an unresolved private-runner failure or a passing research assurance check. The code must be repaired and retested. Full historical recovery and substantive worker-result processing remain incomplete; see [the recovery plan](RECOVERY_MASTER_PLAN_20261007.md).

## Refresh discipline

When these states change, update both this document and
`intake/research_assurance_registry.json` with the current main SHA and the
latest verified/observed workflow run. Do not call a red private run a Python
failure unless GitHub actually starts the job and produces step-level evidence.


## Runner portability fallback

DAEDALUS and Causal Router now default to `ubuntu-latest` through the
`ASSURANCE_RUNNER` repository-variable expression. If a maintained Linux
self-hosted runner is later registered, the owner can point that variable at its
label without another workflow edit. This is a fallback for private hosted-runner
quota/billing constraints, not a reason to run untrusted pull-request code on an
unisolated personal machine.

The current default is GitHub-hosted. Runners now execute in these public repositories; any remaining red result must be diagnosed at the actual failed step.


## Shared assurance schema

The canonical downstream contract is
[`templates/assurance-summary.schema.json`](templates/assurance-summary.schema.json).
It defines the common v1 fields used by the three workflow evidence artifacts,
including commit/run identity, research authority, an explicit
`execution_allowed=false` invariant, gate outcomes, and aggregate result.

Consumers should reject a document with an unknown `schema_version` rather than
silently guessing its semantics.


## Actions runtime refresh

The first Dependabot major-version wave has been reconciled against current
workflow heads. AION/PARALLAX now runs `actions/checkout@v7`,
`actions/setup-python@v7`, `actions/setup-node@v7`, and
`actions/upload-artifact@v7`; its full assurance matrix passed on the final
main SHA.

DAEDALUS and Causal Router now carry the corresponding checkout/setup-python/
upload-artifact v7 updates. Those exact action majors were proven on the public
AION runner before the private repositories were updated. The public hosted runners now execute steps; DAEDALUS passed scheduled assurance while Causal Router has a Python import failure.
