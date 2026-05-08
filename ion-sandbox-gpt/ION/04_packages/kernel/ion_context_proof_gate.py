"""Validate Cursor Task context-proof returns for ION carrier slots.

The carrier-cycle planner can generate a ContextPackage and a parent receipt, but
that only solves the *prompt* side of the Cursor problem. This gate validates the
*return* side: a Task worker is not treated as onboarded unless its output starts
with `### CONTEXT PROOF` and acknowledges every required file read from the
context-load receipt.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Mapping

CONTEXT_PROOF_HEADING = "### CONTEXT PROOF"


def _load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def required_file_paths_from_receipt(receipt: Mapping[str, Any]) -> list[str]:
    """Return required file-read paths from an ION context-load receipt."""

    reads = receipt.get("required_context_reads", [])
    paths: list[str] = []
    if isinstance(reads, list):
        for item in reads:
            if not isinstance(item, Mapping):
                continue
            if item.get("required") is True and item.get("kind") == "file":
                path = item.get("path")
                if isinstance(path, str) and path.strip():
                    paths.append(path.strip())
    return paths


def _proof_section(output: str) -> str:
    text = output.lstrip()
    if not text.startswith(CONTEXT_PROOF_HEADING):
        return ""
    rest = text[len(CONTEXT_PROOF_HEADING):]
    match = re.search(r"\n###\s+", rest)
    if match:
        return rest[: match.start()]
    return rest


def evaluate_context_proof_return(
    *,
    receipt: Mapping[str, Any],
    task_output: str,
) -> dict[str, Any]:
    """Evaluate whether a Cursor Task output satisfies the context-proof gate.

    This intentionally does not try to prove that Cursor's UI performed a real
    file-tool read; that proof remains visual/tool-log evidence in the host. The
    gate enforces the machine-checkable minimum needed before Steward may
    integrate the return: correct heading, all required paths named in the proof
    section, no fake/empty proof, and at least one excerpt/EOF/line signal per
    required read.
    """

    required_paths = required_file_paths_from_receipt(receipt)
    stripped = task_output.lstrip()
    findings: list[str] = []

    if not stripped.startswith(CONTEXT_PROOF_HEADING):
        findings.append("missing_initial_context_proof_heading")

    proof = _proof_section(task_output)
    if not proof.strip():
        findings.append("empty_context_proof_section")

    missing_paths = [path for path in required_paths if path not in proof]
    for path in missing_paths:
        findings.append(f"missing_required_read_path:{path}")

    proof_lower = proof.lower()
    for path in required_paths:
        if path in proof:
            path_pos = proof.find(path)
            window = proof[path_pos : path_pos + 900].lower()
            if not any(token in window for token in ("excerpt", "verbatim", "line", "eof", "sha256", "heading")):
                findings.append(f"missing_read_evidence_near_path:{path}")

    if any(phrase in proof_lower for phrase in ("i have context", "i read the context file", "context acknowledged")) and not required_paths:
        findings.append("generic_context_acknowledgment_without_required_paths")

    accepted = not findings
    return {
        "schema_id": "ion.context_proof_return_evaluation.v1",
        "accepted": accepted,
        "findings": findings,
        "required_paths": required_paths,
        "missing_paths": missing_paths,
        "context_proof_heading": CONTEXT_PROOF_HEADING,
        "integration_decision": "ALLOW_STEWARD_REVIEW" if accepted else "REJECT_RETURN_AND_RERUN_TASK",
        "production_authority": False,
        "live_execution_authority": False,
    }


def evaluate_context_proof_return_files(
    *,
    receipt_path: str | Path,
    task_output_path: str | Path,
) -> dict[str, Any]:
    receipt = _load_json(receipt_path)
    output = Path(task_output_path).read_text(encoding="utf-8", errors="replace")
    result = evaluate_context_proof_return(receipt=receipt, task_output=output)
    result["receipt_path"] = str(receipt_path)
    result["task_output_path"] = str(task_output_path)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate ION Cursor Task CONTEXT PROOF returns.")
    parser.add_argument("--receipt", required=True, help="Path to *_context_load_receipt.json")
    parser.add_argument("--task-output", required=True, help="Path to captured Task output markdown/text")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = evaluate_context_proof_return_files(receipt_path=args.receipt, task_output_path=args.task_output)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("ION_CONTEXT_PROOF_RETURN_ACCEPTED" if result["accepted"] else "ION_CONTEXT_PROOF_RETURN_REJECTED")
        for finding in result["findings"]:
            print(f"- {finding}")
    return 0 if result["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
