# C04 current full hybrid population — read-only receipt

Observed: 2026-10-11T14:23:22.350121Z

Repository: `reppiks490/Icarus-engine`
Source commit: `f4c803ad06ec2f512fdc69b9c3b10c817270b039`
Scope: all committed JSON request/result paths under `automation_intelligence/hybrid_loop_fabric_v1/`, with four byte-identical `latest.json` mirrors excluded from the immutable denominator. No hot-window limit was applied to reconciliation.

There are **658 immutable requests**, **six exact-identity result files**, **five strictly valid BLOCKED dispositions**, and **653 strictly unresolved requests**: 652 with no matching result and one with an invalid matching result. There are no MATERIAL_DELTA results. No duplicate IDs, orphan results, identity mismatches or invalid/naive clocks were observed.

The one schema issue is `SUBSTANTIVE_WORK_PERFORMED_NOT_BOOLEAN` in `automation_intelligence/hybrid_loop_fabric_v1/results/alpha_synthesis/alpha_synthesis-20261004T192000Z.json`. Its existing NO_MATERIAL_DELTA file must not receive completion credit or be overwritten to manufacture a valid historical receipt.

| Lane | Requests | Typed-valid results | Strict unresolved | Oldest unresolved identity | Reason |
|---|---:|---:|---:|---|---|
| advanced_csv | 165 | 1 | 164 | `advanced_csv-20261004T201000Z` | NO_MATCHING_RESULT |
| alpha_synthesis | 164 | 0 | 164 | `alpha_synthesis-20261004T192000Z` | MATCHING_RESULT_SCHEMA_INVALID |
| microstructure_sensor_grid | 164 | 4 | 160 | `microstructure_sensor_grid-20261004T223000Z` | NO_MATCHING_RESULT |
| robustness_guardian | 165 | 0 | 165 | `robustness_guardian-20261004T200000Z` | NO_MATCHING_RESULT |

The globally oldest strict-unresolved request is `alpha_synthesis-20261004T192000Z` (2026-10-04T19:20:00Z).

## Verification

- Git `ls-tree -r -l` enumerated all immutable files and mirrors at the pinned revision; `git cat-file --batch` materialized exact blob bytes into a private local evidence directory.
- All **668 path entries / 664 unique blobs** were rehashed as Git blobs, checked against tree sizes and parsed as JSON objects.
- The existing offline auditor performed exact identity/path, typed schema, execution-false and timezone-aware clock checks across every request and result.
- The pinned `tools/hybrid_loop_bridge.py` validator (`b66d46978d5fef6642cc332486b0ae01907b5afd`; SHA-256 `12937ab18fee9dbf8a707f5474398f0002f86f42004c32b0c11ca493ecf8c7d9`) was executed for all **658** immutable request identities and agreed with the independent audit: five valid dispositions, 653 unresolved.
- Relative to the Oct 9 full report at `0f1089f9fd6e412e11fd8c69afef508099638869`, **180** immutable request identities were added. No old request/result blob changed and no old request identity disappeared.
- The four committed lane-health records correctly report full counts and globally oldest lane identities. Their newest-24 hot lists omit all four oldest unresolved identities; those lists must not become the recovery population.

## Next bounded implementation

1. Preserve this source-pinned full reconciliation as an M01/C04 continuation receipt. Do not change the old Oct 9 evidence package or imply recovery occurred.
2. Explicitly handle the oldest Alpha request's existing invalid immutable result: design an append-only correction/supersession or other agreed invalid-result disposition before attempting to create another result at the occupied path. Do not coerce its structured `substantive_work_performed` object to a boolean or credit the original file.
3. For executable recovery, select identities using the full list (`unresolved_requests(..., limit=0)` or the independently reconciled population), not the newest-24 list. Review each original request mandate; perform real bounded work or emit a correctly typed BLOCKED disposition with original request identity, original timestamps, actual recovery time and matching source evidence. Run restart/conflict/dedup checks and confirm target-branch read-back before crediting it.
4. No cadence, enabled state, automation prompt, provider acquisition, credentials or execution authority changes are needed for this read-only refresh.

Limits: the five BLOCKED files are validated dispositions, not substantive domain completion. This audit proves source population, syntax, clocks and identity matching; it does not prove historical cognition, source-domain correctness, authenticated original data restoration, or historical worker read-back. Nothing was executed or newly disposed by this refresh.
