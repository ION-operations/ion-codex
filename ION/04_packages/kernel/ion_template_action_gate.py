"""ION V101 template/action proof gate."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from typing import Any

CONTEXT_PROOF_HEADING = "### CONTEXT PROOF"
TEMPLATE_ACTION_PROOF_HEADING = "### TEMPLATE ACTION PROOF"
DEFAULT_ALLOWED_TEMPLATE_IDS = {
    "ion.template.autonomous_loop.local_worker.v1",
    "ion.template.context_system.maintenance.v1",
    "ion.template.patch_proposal.v1",
    "ion.template.audit_observation.v1",
    "ion.template.single_carrier_sequential_runtime.v1",
    "ion.template.single_carrier_sequence_receipt.v1",
}

def _section(text: str, heading: str) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    body = text[start + len(heading):]
    next_heading = body.find("\n### ")
    return body if next_heading < 0 else body[:next_heading]

def _scalar(section: str, key: str) -> str | None:
    prefix = f"{key}:"
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith(prefix):
            value = stripped[len(prefix):].strip().strip("`\"'")
            return value or None
    return None

def _list_value(section: str, key: str) -> list[str]:
    lines = section.splitlines()
    values: list[str] = []
    in_block = False
    prefix = f"{key}:"
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(prefix):
            remainder = stripped[len(prefix):].strip()
            if remainder and remainder not in {"[]", "none", "None"}:
                if remainder.startswith("[") and remainder.endswith("]"):
                    for item in remainder[1:-1].split(","):
                        cleaned = item.strip().strip("`\"'")
                        if cleaned:
                            values.append(cleaned)
                else:
                    values.append(remainder.strip("`\"'"))
            in_block = True
            continue
        if in_block:
            if stripped.startswith("-"):
                cleaned = stripped[1:].strip().strip("`\"'")
                if cleaned:
                    values.append(cleaned)
                continue
            if stripped and not line.startswith(" ") and not line.startswith("\t"):
                break
    ordered: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            ordered.append(value)
            seen.add(value)
    return ordered

def _path_finding(path: str) -> str | None:
    normalized = path.replace("\\", "/").strip()
    if not normalized:
        return "empty_path"
    if normalized.startswith("/") or normalized.startswith("../") or "/../" in normalized or normalized.endswith("/.."):
        return "path_escape"
    if normalized.startswith(".git/"):
        return "git_internal_path"
    return None

def evaluate_template_action_proof(*, worker_output: str, allowed_template_ids: set[str] | None = None) -> dict[str, Any]:
    allowed = allowed_template_ids or DEFAULT_ALLOWED_TEMPLATE_IDS
    findings: list[str] = []
    if not worker_output.lstrip().startswith(CONTEXT_PROOF_HEADING):
        findings.append("missing_initial_context_proof_heading")
    if TEMPLATE_ACTION_PROOF_HEADING not in worker_output:
        findings.append("missing_template_action_proof_heading")
    proof = _section(worker_output, TEMPLATE_ACTION_PROOF_HEADING)
    if not proof.strip():
        findings.append("empty_template_action_proof_section")
    template_id = _scalar(proof, "template_id")
    action_id = _scalar(proof, "action_id")
    result = _scalar(proof, "result")
    touched_paths = _list_value(proof, "touched_paths")
    if not template_id:
        findings.append("missing_template_id")
    elif template_id not in allowed:
        findings.append(f"unapproved_template_id:{template_id}")
    if not action_id:
        findings.append("missing_action_id")
    if not result:
        findings.append("missing_result")
    if not touched_paths:
        findings.append("missing_touched_paths")
    for path in touched_paths:
        problem = _path_finding(path)
        if problem:
            findings.append(f"invalid_touched_path:{path}:{problem}")
    accepted = not findings
    return {
        "schema_id": "ion.template_action_gate_result.v1",
        "accepted": accepted,
        "findings": findings,
        "template_id": template_id,
        "action_id": action_id,
        "touched_paths": touched_paths,
        "integration_decision": "ALLOW_STEWARD_INTEGRATION" if accepted else "REJECT_RETURN_AND_RERUN_OR_REPAIR",
        "production_authority": False,
        "live_external_execution_authority": False,
    }

def evaluate_template_action_proof_file(path: str | Path) -> dict[str, Any]:
    return evaluate_template_action_proof(worker_output=Path(path).read_text(encoding="utf-8", errors="replace"))

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate ION TEMPLATE ACTION PROOF returns.")
    parser.add_argument("--worker-output", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = evaluate_template_action_proof_file(args.worker_output)
    print(json.dumps(result, indent=2, sort_keys=True) if args.json else ("ION_TEMPLATE_ACTION_GATE_ACCEPTED" if result["accepted"] else "ION_TEMPLATE_ACTION_GATE_REJECTED"))
    return 0 if result["accepted"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
