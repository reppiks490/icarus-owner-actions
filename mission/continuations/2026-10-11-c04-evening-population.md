# C04 evening full hybrid population — read-only receipt

Observed: 2026-10-11T21:11:09.494961Z

Repository: `reppiks490/Icarus-engine`
Source commit: `dc5ef0d5ab5165eaa6f560268dca25066c3a9237`
Source Git tree: `ff8a97119f5779fc0e538eca3c9ea94bdc2f6e8f`

Scope: every committed JSON request/result path under `automation_intelligence/hybrid_loop_fabric_v1/`. Four byte-identical `latest.json` mirrors are excluded from the immutable request denominator. No newest-24 or other hot-window limit was applied to the population audit.

There are **685 immutable requests**, **six exact-identity result files**, **five strictly valid BLOCKED dispositions**, and **680 strictly unresolved requests**: 679 have no matching result and one has an invalid matching result. There are no MATERIAL_DELTA results. No duplicate identities, orphan results, identity mismatches, or invalid/naive clocks were found.

The sole schema issue remains `SUBSTANTIVE_WORK_PERFORMED_NOT_BOOLEAN` in `automation_intelligence/hybrid_loop_fabric_v1/results/alpha_synthesis/alpha_synthesis-20261004T192000Z.json`. Its structured object was preserved unchanged; its existing NO_MATERIAL_DELTA file receives no completion credit.

| Lane | Immutable requests | Typed-valid matching results | Strict unresolved | Oldest unresolved | Reason |
|---|---:|---:|---:|---|---|
| advanced_csv | 171 | 1 | 170 | `advanced_csv-20261004T201000Z` | NO_MATCHING_RESULT |
| alpha_synthesis | 171 | 0 | 171 | `alpha_synthesis-20261004T192000Z` | MATCHING_RESULT_SCHEMA_INVALID |
| microstructure_sensor_grid | 171 | 4 | 167 | `microstructure_sensor_grid-20261004T223000Z` | NO_MATCHING_RESULT |
| robustness_guardian | 172 | 0 | 172 | `robustness_guardian-20261004T200000Z` | NO_MATCHING_RESULT |

The globally oldest strict-unresolved identity remains `alpha_synthesis-20261004T192000Z`, due 2026-10-04T19:20:00Z.

## Verification

- Main was discovered with `git ls-remote ... refs/heads/main`, then fetched by its explicit SHA using `--no-write-fetch-head`. The pinned commit's tree was enumerated using `git ls-tree -r -l`; source bytes were materialized using `git cat-file --batch`.
- All **695 request/result path entries / 691 unique request/result blobs** passed Git blob rehash, tree-size and JSON-object checks. The four committed health documents were separately rehashed and parsed.
- The unchanged pinned `tools/hybrid_loop_bridge.py` validator (`b66d46978d5fef6642cc332486b0ae01907b5afd`; SHA-256 `12937ab18fee9dbf8a707f5474398f0002f86f42004c32b0c11ca493ecf8c7d9`) executed `result_valid` against every one of the **685** immutable request identities and agreed with the independent audit: five strictly valid dispositions and 680 unresolved.
- Full `unresolved_requests(..., limit=0)` views exactly matched the independent oldest-first reconciliation for each lane. The committed lane-health totals and oldest identities also matched. Each newest-24 view omits its lane's oldest unresolved request; it cannot serve as the recovery population.

## Change from the 14:23:22 UTC snapshot

Previous source commit: `f4c803ad06ec2f512fdc69b9c3b10c817270b039`.

- Immutable requests increased from **658 to 685** (**27 added**); strict unresolved increased from **653 to 680**.
- Per-lane new identities: advanced_csv +6; alpha_synthesis +7; microstructure_sensor_grid +7; robustness_guardian +7.
- No prior immutable request disappeared or changed bytes. No prior result disappeared or changed bytes. No new result was added. The strict-valid disposition count remains five.
- The invalid Alpha object and every oldest unresolved lane identity remain unchanged.

## Next bounded action

Preserve this source-pinned continuation without replacing the earlier 14:23 or Oct 9 evidence. Recovery must use full oldest-first identities and preserve original request mandates and timestamps. Before acting on the oldest Alpha identity, agree an append-only correction or supersession policy for its occupied invalid immutable result path; neither overwriting it nor coercing the structured object to a boolean establishes historical completion.

Limits: this is a read-only syntax, aware-clock, execution-false, identity/path and byte-integrity audit. The five BLOCKED files are validated dispositions, not substantive domain completion. No prior cognition, source-domain correctness, historical worker readback, or original archive restoration is established. No requests were executed, records modified, provider calls made, spend incurred, credentials introduced, schedules or automations changed, or execution authority granted. Atlas discovery/research-allocation files and Claude Code UI files were not touched.

No pytest suite was run: verification was the complete-population independent reconciliation, pinned-validator execution for 685 identities, and exact full-worker view comparison.
