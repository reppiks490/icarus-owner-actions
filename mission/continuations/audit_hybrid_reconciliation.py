"""Offline, pinned hybrid identity reconciliation. Does not modify source records."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path, PurePosixPath
import tempfile


FABRIC = "icarus-account-hybrid-loop-fabric-v1"
ROOT = "automation_intelligence/hybrid_loop_fabric_v1"
REQUEST_REQUIRED = {
    "schema_version", "fabric_id", "request_id", "lane", "title",
    "automation_id", "project_scope", "requested_at_utc", "request_origin",
    "workflow_run_id", "workflow_run_attempt", "contract_fingerprint",
    "contract_registry_path", "required_result_path", "prior_unresolved_request_ids",
    "backfill_policy", "substantive_ai_inference_required",
    "github_liveness_receipt_is_not_completion", "execution_authorized",
}
RESULT_REQUIRED = {
    "schema_version", "fabric_id", "request_id", "lane", "automation_id",
    "started_at_utc", "completed_at_utc", "outcome", "substantive_work_performed",
    "summary", "evidence", "research_receipt_paths", "event_paths", "blockers",
    "backfilled_request_ids", "execution_authorized",
}
OUTCOMES = {"MATERIAL_DELTA", "NO_MATERIAL_DELTA", "BLOCKED"}


def clock(value):
    if not isinstance(value, str) or not value:
        raise ValueError("missing/non-string timestamp")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("timezone-naive timestamp")
    return parsed.astimezone(timezone.utc)


def z(value):
    return value.isoformat().replace("+00:00", "Z")


def reconcile(tree_path: Path, blob_dir: Path):
    tree_bytes = tree_path.read_bytes()
    tree = json.loads(tree_bytes)
    records = {}
    integrity_errors = []
    all_entries = tree["req"] + tree["res"]
    for entry in all_entries:
        path = entry["path"]
        try:
            raw = (blob_dir / (entry["sha"] + ".json")).read_bytes()
            actual_blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
            if actual_blob != entry["sha"]:
                raise ValueError("GIT_BLOB_SHA_MISMATCH")
            if len(raw) != entry["size"]:
                raise ValueError("TREE_SIZE_MISMATCH")
            payload = json.loads(raw)
            if not isinstance(payload, dict):
                raise ValueError("JSON_OBJECT_REQUIRED")
            records[path] = (entry, payload, hashlib.sha256(raw).hexdigest())
        except (OSError, ValueError, KeyError) as exc:
            integrity_errors.append({"path": path, "error": str(exc)})
    if integrity_errors:
        raise ValueError(json.dumps({"integrity_errors": integrity_errors}))

    request_entries = [x for x in tree["req"] if PurePosixPath(x["path"]).name != "latest.json"]
    mirror_entries = [x for x in tree["req"] if PurePosixPath(x["path"]).name == "latest.json"]
    request_ids = defaultdict(list)
    result_ids = defaultdict(list)
    issues = []
    requests = []
    results = []

    def issue(path, code, fields=None):
        row = {"path": path, "code": code}
        if fields:
            row["fields"] = fields
        issues.append(row)

    def validate_common(path, payload, required, schema):
        missing = sorted(required - payload.keys())
        if missing:
            issue(path, "MISSING_REQUIRED_FIELDS", missing)
        if payload.get("schema_version") != schema:
            issue(path, "SCHEMA_VERSION_MISMATCH")
        if payload.get("fabric_id") != FABRIC:
            issue(path, "FABRIC_ID_MISMATCH")
        if payload.get("execution_authorized") is not False:
            issue(path, "EXECUTION_AUTHORITY_INVARIANT_FAILED")
        for field in ("request_id", "lane", "automation_id"):
            if not isinstance(payload.get(field), str) or not payload[field]:
                issue(path, "INVALID_IDENTITY_FIELD", [field])

    for entry in request_entries:
        path = entry["path"]
        _, payload, digest = records[path]
        validate_common(path, payload, REQUEST_REQUIRED, "icarus-hybrid-work-request-v1")
        if REQUEST_REQUIRED - payload.keys():
            raise ValueError(f"request required key missing: {path}")
        request_id = payload.get("request_id")
        lane = payload.get("lane")
        request_ids[request_id].append(path)
        expected_request_path = f"{ROOT}/requests/{lane}/{request_id}.json"
        expected_result_path = f"{ROOT}/results/{lane}/{request_id}.json"
        if path != expected_request_path:
            issue(path, "REQUEST_ID_OR_LANE_PATH_MISMATCH")
        if payload.get("required_result_path") != expected_result_path:
            issue(path, "REQUIRED_RESULT_PATH_MISMATCH")
        for field in ("substantive_ai_inference_required", "github_liveness_receipt_is_not_completion"):
            if payload.get(field) is not True:
                issue(path, "REQUEST_COMPLETION_INVARIANT_FAILED", [field])
        for field in ("workflow_run_id", "workflow_run_attempt", "contract_fingerprint"):
            if not isinstance(payload.get(field), str) or not payload[field]:
                issue(path, "INVALID_REQUEST_METADATA", [field])
        parsed = {}
        for field in ("requested_at_utc", "due_slot_utc", "request_created_at_utc"):
            if field != "requested_at_utc" and field not in payload:
                continue
            try:
                parsed[field] = clock(payload.get(field))
            except ValueError:
                issue(path, "INVALID_OR_NAIVE_CLOCK", [field])
                raise ValueError(f"invalid or naive request clock {field}: {path}")
        if "requested_at_utc" not in parsed or ("due_slot_utc" in payload and "due_slot_utc" not in parsed):
            raise ValueError(f"clock validation failed: {path}")
        ordering_field = "due_slot_utc" if "due_slot_utc" in payload else "requested_at_utc"
        requests.append({
            "request_id": request_id, "lane": lane,
            "automation_id": payload.get("automation_id"), "request_path": path,
            "required_result_path": payload.get("required_result_path"),
            "request_blob_sha": entry["sha"], "request_sha256": digest,
            "size_bytes": entry["size"], "requested_at_utc": payload.get("requested_at_utc"),
            "due_slot_utc": payload.get("due_slot_utc"),
            "ordering_clock_field": ordering_field, "ordering_at_utc": z(parsed[ordering_field]),
            "workflow_run_id": payload.get("workflow_run_id"),
            "workflow_run_attempt": payload.get("workflow_run_attempt"),
            "contract_fingerprint": payload.get("contract_fingerprint"),
        })

    for entry in tree["res"]:
        path = entry["path"]
        _, payload, digest = records[path]
        previous_issue_count = len(issues)
        validate_common(path, payload, RESULT_REQUIRED, "icarus-hybrid-work-result-v1")
        result_ids[payload.get("request_id")].append(path)
        if path != f"{ROOT}/results/{payload.get('lane')}/{payload.get('request_id')}.json":
            issue(path, "RESULT_ID_OR_LANE_PATH_MISMATCH")
        if payload.get("outcome") not in OUTCOMES:
            issue(path, "UNKNOWN_RESULT_OUTCOME")
        if not isinstance(payload.get("substantive_work_performed"), bool):
            issue(path, "SUBSTANTIVE_WORK_PERFORMED_NOT_BOOLEAN")
        for field in ("evidence", "research_receipt_paths", "event_paths", "blockers", "backfilled_request_ids"):
            if not isinstance(payload.get(field), list):
                issue(path, "RESULT_LIST_REQUIRED", [field])
        parsed = {}
        for field in ("started_at_utc", "completed_at_utc", "original_due_slot_utc", "original_requested_at_utc"):
            if field.startswith("original_") and field not in payload:
                continue
            try:
                parsed[field] = clock(payload.get(field))
            except ValueError:
                issue(path, "INVALID_OR_NAIVE_CLOCK", [field])
        if "started_at_utc" not in parsed or "completed_at_utc" not in parsed:
            raise ValueError(f"result clock validation failed: {path}")
        if parsed["completed_at_utc"] < parsed["started_at_utc"]:
            issue(path, "RESULT_COMPLETES_BEFORE_START")
        results.append({
            "request_id": payload.get("request_id"), "lane": payload.get("lane"),
            "automation_id": payload.get("automation_id"), "result_path": path,
            "result_blob_sha": entry["sha"], "result_sha256": digest, "size_bytes": entry["size"],
            "outcome": payload.get("outcome"), "started_at_utc": payload.get("started_at_utc"),
            "completed_at_utc": payload.get("completed_at_utc"),
            "substantive_work_performed_type": type(payload.get("substantive_work_performed")).__name__,
            "substantive_work_performed_boolean": payload.get("substantive_work_performed") if isinstance(payload.get("substantive_work_performed"), bool) else None,
            "schema_and_clocks_valid": len(issues) == previous_issue_count,
            "schema_issue_codes": [x["code"] for x in issues[previous_issue_count:]],
        })

    duplicate_request_ids = {k: v for k, v in request_ids.items() if len(v) > 1}
    duplicate_result_ids = {k: v for k, v in result_ids.items() if len(v) > 1}
    mirror_report = []
    for entry in mirror_entries:
        path = entry["path"]
        _, payload, digest = records[path]
        targets = request_ids.get(payload.get("request_id"), [])
        mirror_lane = PurePosixPath(path).parent.name
        verified = len(targets) == 1 and records[targets[0]][0]["sha"] == entry["sha"] and payload.get("lane") == mirror_lane
        if not verified:
            issue(path, "LATEST_MIRROR_TARGET_MISMATCH")
        mirror_report.append({
            "mirror_path": path, "request_id": payload.get("request_id"),
            "lane": payload.get("lane"), "blob_sha": entry["sha"], "sha256": digest,
            "target_request_path": targets[0] if len(targets) == 1 else None,
            "identical_to_single_immutable_request": verified,
        })

    request_map = {r["request_id"]: r for r in requests}
    result_map = {r["result_path"]: r for r in results}
    orphan_results = []
    for result in results:
        req = request_map.get(result["request_id"])
        if req is None:
            orphan_results.append(result)
            result["request_identity_matches"] = False
            continue
        mismatched = [field for field in ("request_id", "lane", "automation_id") if result[field] != req[field]]
        if result["result_path"] != req["required_result_path"]:
            mismatched.append("required_result_path")
        if mismatched:
            issue(result["result_path"], "REQUEST_RESULT_IDENTITY_MISMATCH", mismatched)
        result["request_identity_matches"] = not mismatched
        original_comparisons = {}
        payload = records[result["result_path"]][1]
        for result_field, req_field in (
            ("original_due_slot_utc", "due_slot_utc"),
            ("original_requested_at_utc", "requested_at_utc"),
            ("original_workflow_run_id", "workflow_run_id"),
            ("original_workflow_run_attempt", "workflow_run_attempt"),
        ):
            if result_field not in payload:
                original_comparisons[result_field] = "NOT_RECORDED_IN_RESULT"
            elif payload[result_field] == req.get(req_field):
                original_comparisons[result_field] = "MATCH"
            else:
                original_comparisons[result_field] = "MISMATCH"
                issue(result["result_path"], "ORIGINAL_REQUEST_METADATA_MISMATCH", [result_field])
        result["original_request_metadata_comparisons"] = original_comparisons
        result["strict_valid_matching_result"] = result["schema_and_clocks_valid"] and result["request_identity_matches"] and "MISMATCH" not in original_comparisons.values() and result["request_id"] not in duplicate_result_ids

    requests.sort(key=lambda r: (clock(r["ordering_at_utc"]), r["request_id"], r["request_path"]))
    presence_unmatched = []
    strict_unresolved = []
    for req in requests:
        result = result_map.get(req["required_result_path"])
        req["matching_result_present"] = result is not None and result.get("request_identity_matches") is True
        req["strict_valid_matching_result"] = req["matching_result_present"] and result.get("strict_valid_matching_result") is True and req["request_id"] not in duplicate_request_ids
        if req["matching_result_present"]:
            req["result_blob_sha"] = result["result_blob_sha"]
            req["result_outcome"] = result["outcome"]
        if not req["matching_result_present"]:
            presence_unmatched.append(req["request_id"])
        if not req["strict_valid_matching_result"]:
            strict_unresolved.append({
                "request_id": req["request_id"], "lane": req["lane"],
                "ordering_at_utc": req["ordering_at_utc"], "ordering_clock_field": req["ordering_clock_field"],
                "request_blob_sha": req["request_blob_sha"],
                "reason": "MATCHING_RESULT_SCHEMA_INVALID" if req["matching_result_present"] else "NO_MATCHING_RESULT",
            })

    lanes = {}
    for lane in sorted({r["lane"] for r in requests}):
        reqs = [r for r in requests if r["lane"] == lane]
        res = [r for r in results if r["lane"] == lane]
        unresolved = [r for r in strict_unresolved if r["lane"] == lane]
        unmatched = [r for r in reqs if r["request_id"] in presence_unmatched]
        automation_ids = sorted({r["automation_id"] for r in reqs})
        if len(automation_ids) != 1:
            issue(f"{ROOT}/requests/{lane}", "LANE_AUTOMATION_ID_NOT_UNIQUE")
        lanes[lane] = {
            "automation_ids": automation_ids, "immutable_requests": len(reqs),
            "matching_result_files": sum(r["matching_result_present"] for r in reqs),
            "strict_valid_matching_results": sum(r["strict_valid_matching_result"] for r in reqs),
            "outcomes_in_present_results": dict(sorted(Counter(r["outcome"] for r in res).items())),
            "presence_only_unmatched": len(unmatched), "strict_unresolved": len(unresolved),
            "oldest_presence_only_unmatched_request_id": unmatched[0]["request_id"] if unmatched else None,
            "oldest_strict_unresolved": unresolved[0] if unresolved else None,
            "newest_request_id": reqs[-1]["request_id"],
        }

    report = {
        "schema_version": "icarus-pinned-hybrid-reconciliation-v1",
        "observed_at_utc": z(datetime.now(timezone.utc)),
        "source_repository": "reppiks490/Icarus-engine", "source_commit_sha": tree["sha"],
        "input_tree_manifest_sha256": hashlib.sha256(tree_bytes).hexdigest(),
        "scope": "All request/result JSON entries in supplied pinned tree manifest; immutable request identities exclude latest.json mirrors.",
        "ordering_policy": {"primary": "due_slot_utc", "fallback": "requested_at_utc only when due_slot_utc key is absent", "timezone_required": True, "tie_breakers": ["request_id", "request_path"], "hot_window_limit_applied": False},
        "integrity": {"tree_entries_rehashed": len(all_entries), "unique_blobs_rehashed": len({e["sha"] for e in all_entries}), "git_blob_sha_and_tree_size_verified": True, "invalid_or_missing_or_naive_clock_count": sum(x["code"] == "INVALID_OR_NAIVE_CLOCK" for x in issues)},
        "counts": {
            "request_json_paths_including_mirrors": len(tree["req"]), "latest_mirror_paths": len(mirror_entries),
            "immutable_request_paths": len(request_entries), "unique_immutable_request_ids": len(request_ids),
            "result_json_paths": len(tree["res"]), "unique_result_request_ids": len(result_ids),
            "identity_matched_result_files": sum(r.get("request_identity_matches") is True for r in results),
            "strict_valid_matching_results": sum(r.get("strict_valid_matching_result") is True for r in results),
            "presence_only_unmatched_immutable_requests": len(presence_unmatched), "strict_unresolved_immutable_requests": len(strict_unresolved),
            "orphan_result_files": len(orphan_results), "duplicate_immutable_request_ids": len(duplicate_request_ids),
            "duplicate_result_request_ids": len(duplicate_result_ids),
            "request_result_identity_inconsistencies": sum(x["code"] == "REQUEST_RESULT_IDENTITY_MISMATCH" for x in issues),
            "schema_or_invariant_issue_count": len(issues),
        },
        "outcomes_in_present_results": dict(sorted(Counter(r["outcome"] for r in results).items())),
        "due_slot_fallback_request_ids": [r["request_id"] for r in requests if r["ordering_clock_field"] == "requested_at_utc"],
        "latest_mirrors": mirror_report,
        "duplicate_immutable_request_ids": duplicate_request_ids, "duplicate_result_request_ids": duplicate_result_ids,
        "orphan_results": orphan_results, "issues": issues, "lanes": lanes,
        "results": sorted(results, key=lambda r: (r["request_id"], r["result_path"])),
        "immutable_requests_oldest_first": requests,
        "presence_only_unmatched_request_ids_oldest_first": presence_unmatched,
        "strict_unresolved_oldest_first": strict_unresolved,
        "limitations": [
            "Valid matching result means syntax, aware clocks and exact identity/path agreement; this audit does not prove prior worker cognition, source-domain correctness or historical read-back.",
            "Five BLOCKED dispositions and one schema-invalid NO_MATERIAL_DELTA file are present; no MATERIAL_DELTA result is present.",
            "Four mutable latest.json aliases are verified byte-identical to their immutable targets and never increase the request denominator.",
            "Five historical requests lack due_slot_utc; each explicitly uses its valid requested_at_utc for ordering.",
            "No historical record, canonical index, automation schedule, workflow, result or source payload is changed by this reconciliation.",
        ],
    }
    # Store shared identity/path metadata once while retaining every immutable ID.
    report["identity_path_templates"] = {
        "request": f"{ROOT}/requests/{{lane}}/{{request_id}}.json",
        "required_result": f"{ROOT}/results/{{lane}}/{{request_id}}.json",
        "request_and_required_result_paths_all_checked_against_templates": not any(
            x["code"] in {"REQUEST_ID_OR_LANE_PATH_MISMATCH", "REQUIRED_RESULT_PATH_MISMATCH"}
            for x in issues
        ),
        "automation_id": "lanes[lane].automation_ids (exactly one ID required)",
        "contract_fingerprint": "lanes[lane].contract_fingerprints",
    }
    for lane, info in lanes.items():
        info["contract_fingerprints"] = sorted({r["contract_fingerprint"] for r in requests if r["lane"] == lane})
    retained = {
        "request_id", "lane", "request_blob_sha", "size_bytes", "requested_at_utc",
        "due_slot_utc", "ordering_clock_field", "workflow_run_id", "workflow_run_attempt",
        "matching_result_present", "strict_valid_matching_result", "result_blob_sha", "result_outcome",
    }
    report["immutable_requests_oldest_first"] = [{k: v for k, v in r.items() if k in retained} for r in requests]
    report["strict_unresolved_request_ids_oldest_first"] = [r["request_id"] for r in strict_unresolved]
    del report["strict_unresolved_oldest_first"]
    return report


def check_pinned_validator(report, tree_path, blob_dir, validator_path, expected_sha):
    raw = validator_path.read_bytes()
    source = raw
    transport_newline_excluded = False
    def git_hash(value):
        return hashlib.sha1(b"blob " + str(len(value)).encode() + b"\0" + value).hexdigest()
    if git_hash(source) != expected_sha:
        if raw.endswith(b"\n") and git_hash(raw[:-1]) == expected_sha:
            source = raw[:-1]
            transport_newline_excluded = True
        else:
            raise ValueError("pinned validator Gitblob SHA mismatch")
    spec = importlib.util.spec_from_file_location("pinned_hybrid_audit_validator", validator_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    tree = json.loads(tree_path.read_text())
    valid = set()
    with tempfile.TemporaryDirectory(prefix="icarus-pinned-hybrid-audit-") as directory:
        shadow = Path(directory)
        for row in tree["req"] + tree["res"]:
            path = shadow / row["path"]
            path.parent.mkdir(parents=True, exist_ok=True)
            path.symlink_to(blob_dir.resolve() / (row["sha"] + ".json"))
        for row in tree["req"]:
            if PurePosixPath(row["path"]).name == "latest.json":
                continue
            payload = json.loads((blob_dir / (row["sha"] + ".json")).read_text())
            if module.result_valid(shadow, payload["lane"], payload["automation_id"], payload["request_id"]):
                valid.add(payload["request_id"])
    audit_valid = {r["request_id"] for r in report["immutable_requests_oldest_first"] if r["strict_valid_matching_result"]}
    if valid != audit_valid:
        raise ValueError("audit and pinned validator disagree")
    count = report["counts"]["unique_immutable_request_ids"]
    report["pinned_validator_check"] = {
        "repository_path": "tools/hybrid_loop_bridge.py",
        "source_commit_sha": report["source_commit_sha"],
        "git_blob_sha": expected_sha, "sha256": hashlib.sha256(source).hexdigest(),
        "source_size_bytes": len(source),
        "local_transport_extra_eof_newline_excluded_for_hash": transport_newline_excluded,
        "result_valid_executed_for_all_immutable_requests": count,
        "validator_valid_matching_results": len(valid), "validator_unresolved": count - len(valid),
        "audit_and_pinned_validator_agree": True,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tree", type=Path, required=True)
    parser.add_argument("--blobs", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--validator", type=Path)
    parser.add_argument("--validator-blob-sha")
    args = parser.parse_args()
    report = reconcile(args.tree, args.blobs)
    if args.validator:
        if not args.validator_blob_sha:
            parser.error("--validator-blob-sha required with --validator")
        check_pinned_validator(report, args.tree, args.blobs, args.validator, args.validator_blob_sha)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"counts": report["counts"], "lanes": report["lanes"], "issues": report["issues"]}, indent=2))
