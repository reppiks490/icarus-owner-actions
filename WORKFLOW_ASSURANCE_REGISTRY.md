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
| `daedalus-research-os` | `DAEDALUS research assurance` | Workflow installed; private hosted-runner infrastructure currently blocks execution before usable logs | Research only |
| `icarus-causal-router` | `ICARUS causal-router assurance` | Workflow installed; private hosted-runner infrastructure currently blocks execution before usable logs | Research only |

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

## Private-repository runner blocker

DAEDALUS and Causal Router both currently fail before useful job logs are
created. A temporary workflow containing only a bare GitHub-hosted runner probe
reproduced the same failure, while AION's public workflow executed normally.
That isolates the observed failure away from the Python test logic.

GitHub's current product model meters standard hosted-runner minutes for private
repositories. If included private-repository minutes are exhausted and billing
cannot cover additional use, hosted usage is blocked. The owner should treat
private Actions quota/billing/runner availability as the infrastructure gate,
not weaken the research workflows to hide the failure.

Do **not** make either private repository public merely to clear CI without an
explicit repository-visibility decision.

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

The current default remains GitHub-hosted and therefore remains blocked until
private hosted-runner eligibility/quota/settings permit execution.
