"""Unified ION carrier status command.

V88 gives Cursor a single non-mutating status command so the parent chat can
answer "where are we?" from active packets instead of conversational memory.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Mapping

from .ion_carrier_continue import (
    ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH,
    ACTIVE_TASK_RETURN_LEDGER_RELATIVE_PATH,
    ACTIVE_TURN_PACKET_RELATIVE_PATH,
)
from .ion_active_state_integrity_audit import audit_active_state_integrity
from .ion_carrier_onboard import ACTIVE_PACKET_RELATIVE_PATH, resolve_shell_root_from_ion_root
from .ion_cycle_runner import ACTIVE_SPAWN_PLAN_RELATIVE_PATH
from .ion_human_gate_queue import ACTIVE_HUMAN_GATE_QUEUE_RELATIVE_PATH, load_human_gate_queue, unresolved_human_gates
from .ion_operator_message_queue import ACTIVE_OPERATOR_MESSAGE_QUEUE_RELATIVE_PATH, load_operator_message_queue, queue_counts


ACTIVE_CURSOR_HOOK_STATE_RELATIVE_PATH = Path("ION/05_context/current/ACTIVE_CURSOR_HOOK_STATE.json")
TRUNK_PRESERVATION_REPORT_GLOB = "ION/05_context/current/TRUNK_PRESERVATION_REPORT_V*.json"
SAFE_FULL_PROJECT_PACKAGE_RESULT_GLOB = "ION/05_context/current/SAFE_FULL_PROJECT_PACKAGE_RESULT_V*.json"
V72_MCP_DONOR_RECONCILIATION_AUDIT_RELATIVE_PATH = Path("ION/05_context/current/V108_V72_MCP_DONOR_RECONCILIATION_AUDIT.json")


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _latest_safe_package_result_path(shell_root: Path) -> Path | None:
    current = shell_root / "ION/05_context/current"
    candidates = sorted(current.glob("SAFE_FULL_PROJECT_PACKAGE_RESULT_V*.json"))
    if not candidates:
        return None
    return candidates[-1].relative_to(shell_root)


def _latest_trunk_preservation_report_path(shell_root: Path) -> Path | None:
    current = shell_root / "ION/05_context/current"
    candidates = sorted(current.glob("TRUNK_PRESERVATION_REPORT_V*.json"))
    if not candidates:
        return None
    return candidates[-1].relative_to(shell_root)


def _count_return_records(ledger: Mapping[str, Any] | None) -> dict[str, int]:
    counts = {"accepted": 0, "rejected": 0, "total": 0}
    if not ledger:
        return counts
    for record in ledger.get("records", []):
        if not isinstance(record, dict):
            continue
        counts["total"] += 1
        if record.get("accepted") is True:
            counts["accepted"] += 1
        else:
            counts["rejected"] += 1
    return counts


def _plan_spawn_counts(plan: Mapping[str, Any] | None) -> dict[str, int]:
    rows = plan.get("role_spawn_plan", []) if plan else []
    if not isinstance(rows, list):
        return {"plan_spawn_count": 0, "deferred_spawn_count": 0, "completed_role_count": 0}
    plan_spawn_count = 0
    deferred_spawn_count = 0
    completed_role_count = 0
    for row in rows:
        if not isinstance(row, Mapping):
            continue
        if row.get("completion_status") == "ALREADY_INTEGRATED":
            completed_role_count += 1
            continue
        if row.get("spawn") is True:
            plan_spawn_count += 1
        elif row.get("spawn_intent") is True or row.get("spawn_deferral_reason"):
            deferred_spawn_count += 1
    return {
        "plan_spawn_count": plan_spawn_count,
        "deferred_spawn_count": deferred_spawn_count,
        "completed_role_count": completed_role_count,
    }


def _latest_steward_items_by_role_index(items: list[Any]) -> list[dict[str, Any]]:
    latest: dict[tuple[str, int], dict[str, Any]] = {}
    anonymous: list[dict[str, Any]] = []
    for ordinal, item in enumerate(items):
        if not isinstance(item, dict):
            continue
        role = str(item.get("role") or "")
        try:
            index = int(item.get("index", ordinal))
        except (TypeError, ValueError):
            index = ordinal
        if role:
            latest[(role, index)] = item
        else:
            anonymous.append(item)
    return [*latest.values(), *anonymous]


def build_ion_status(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = resolve_shell_root_from_ion_root(root)
    trunk_preservation_report_rel = _latest_trunk_preservation_report_path(shell_root)
    safe_package_result_rel = _latest_safe_package_result_path(shell_root)
    paths = {
        "cursor_hook_state": ACTIVE_CURSOR_HOOK_STATE_RELATIVE_PATH,
        "v72_mcp_donor_reconciliation_audit": V72_MCP_DONOR_RECONCILIATION_AUDIT_RELATIVE_PATH,
        "active_work_packet": ACTIVE_PACKET_RELATIVE_PATH,
        "active_spawn_plan": ACTIVE_SPAWN_PLAN_RELATIVE_PATH,
        "active_turn_packet": ACTIVE_TURN_PACKET_RELATIVE_PATH,
        "task_return_ledger": ACTIVE_TASK_RETURN_LEDGER_RELATIVE_PATH,
        "steward_integration_queue": ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH,
        "operator_message_queue": ACTIVE_OPERATOR_MESSAGE_QUEUE_RELATIVE_PATH,
        "human_gate_queue": ACTIVE_HUMAN_GATE_QUEUE_RELATIVE_PATH,
    }
    optional_paths: dict[str, Path | None] = {
        "trunk_preservation_report": trunk_preservation_report_rel,
        "safe_full_project_package_result": safe_package_result_rel,
    }
    loaded = {name: _read_json(shell_root / rel) for name, rel in paths.items()}
    loaded.update({name: _read_json(shell_root / rel) if rel is not None else None for name, rel in optional_paths.items()})
    # Ensure V88 queues exist even for status-only usage.
    operator_queue = load_operator_message_queue(shell_root)
    human_gate_queue = load_human_gate_queue(shell_root)
    loaded["operator_message_queue"] = operator_queue
    loaded["human_gate_queue"] = human_gate_queue

    missing = [name for name, rel in paths.items() if not (shell_root / rel).exists()]
    turn = loaded.get("active_turn_packet") or {}
    work = loaded.get("active_work_packet") or {}
    plan = loaded.get("active_spawn_plan") or {}
    ledger = loaded.get("task_return_ledger") or {}
    steward_queue = loaded.get("steward_integration_queue") or {}
    cursor_hook_state = loaded.get("cursor_hook_state") or {}
    trunk_preservation_report = loaded.get("trunk_preservation_report") or {}
    safe_full_project_package_result = loaded.get("safe_full_project_package_result") or {}
    v72_mcp_donor_reconciliation_audit = loaded.get("v72_mcp_donor_reconciliation_audit") or {}

    spawn_queue = turn.get("spawn_queue") if isinstance(turn.get("spawn_queue"), list) else []
    plan_spawn_counts = _plan_spawn_counts(plan)
    open_gates = unresolved_human_gates(shell_root)
    return_counts = _count_return_records(ledger)
    steward_items = steward_queue.get("items", []) if isinstance(steward_queue.get("items"), list) else []
    latest_steward_items = _latest_steward_items_by_role_index(steward_items)
    pending_steward = [item for item in latest_steward_items if item.get("status") == "PENDING_STEWARD_INTEGRATION"]
    rejected_steward = [item for item in latest_steward_items if item.get("status") == "STEWARD_INTEGRATION_REJECTED"]
    active_state_integrity = audit_active_state_integrity(shell_root)
    trunk_preservation_failed = bool(
        trunk_preservation_report
        and (
            trunk_preservation_report.get("packaging_verdict") == "FAIL"
            or trunk_preservation_report.get("accepted") is False
        )
    )
    safe_package_failed = bool(
        safe_full_project_package_result
        and (
            safe_full_project_package_result.get("accepted") is False
            or (safe_full_project_package_result.get("zip_root_audit") or {}).get("verdict") not in {None, "ZIP_ROOT_CONFIRMED"}
        )
    )
    v72_mcp_donor_failed = bool(
        v72_mcp_donor_reconciliation_audit
        and v72_mcp_donor_reconciliation_audit.get("reconciliation_verdict") != "V72_MCP_DONOR_RECONCILIATION_PASS"
    )

    if not active_state_integrity.get("accepted"):
        next_action = "repair_active_state_integrity"
    elif trunk_preservation_failed:
        next_action = "repair_trunk_preservation_failure"
    elif safe_package_failed:
        next_action = "repair_safe_full_project_package_failure"
    elif v72_mcp_donor_failed:
        next_action = "repair_v72_mcp_donor_reconciliation"
    elif open_gates:
        next_action = "resolve_human_gate"
    elif spawn_queue and return_counts["total"] < len(spawn_queue):
        next_action = "execute_spawn_rows_and_run_task_return_intake"
    elif pending_steward:
        next_action = "spawn_steward_integration_from_accepted_queue"
    elif rejected_steward:
        next_action = "repair_rejected_steward_integration"
    elif queue_counts(operator_queue).get("pending", 0):
        next_action = "run_ion_carrier_continue_with_consume_operator_queue"
    else:
        next_action = "continue_or_queue_new_work"

    return {
        "schema_id": "ion.status.v1",
        "verdict": (
            "ION_STATUS_PARTIAL"
                if missing
                else (
                    "ION_STATUS_DEGRADED"
                    if not active_state_integrity.get("accepted") or trunk_preservation_failed or safe_package_failed or v72_mcp_donor_failed
                    else "ION_STATUS_READY"
                )
        ),
        "shell_root": str(shell_root),
        "missing_state_surfaces": missing,
        "objective": turn.get("objective") or plan.get("objective") or work.get("objective"),
        "workstream": turn.get("workstream") or plan.get("workstream"),
        "operator_message_interpretation": turn.get("operator_message_interpretation"),
        "operator_message_classification": turn.get("operator_message_classification"),
        "spawn_queue_count": len(spawn_queue),
        "plan_spawn_count": plan_spawn_counts["plan_spawn_count"],
        "deferred_spawn_count": plan_spawn_counts["deferred_spawn_count"],
        "completed_role_count": plan_spawn_counts["completed_role_count"],
        "execution_bundle_materialized": plan.get("execution_bundle_materialized"),
        "spawn_queue": spawn_queue,
        "task_return_counts": return_counts,
        "steward_queue_pending_count": len(pending_steward),
        "steward_queue_rejected_count": len(rejected_steward),
        "operator_queue_counts": queue_counts(operator_queue),
        "open_human_gate_count": len(open_gates),
        "open_human_gates": open_gates,
        "cursor_hook_state": {
            "status": cursor_hook_state.get("status"),
            "cursor_hook_bridge_verdict": cursor_hook_state.get("cursor_hook_bridge_verdict"),
            "host_connection_state": cursor_hook_state.get("host_connection_state"),
            "live_hook_event_seen": cursor_hook_state.get("live_hook_event_seen"),
            "path": str(ACTIVE_CURSOR_HOOK_STATE_RELATIVE_PATH),
        },
        "active_state_integrity": {
            "verdict": active_state_integrity.get("verdict"),
            "finding_count": active_state_integrity.get("finding_count", 0),
            "findings": active_state_integrity.get("findings", []),
        },
        "trunk_preservation": {
            "path": str(trunk_preservation_report_rel) if trunk_preservation_report_rel is not None else None,
            "path_pattern": TRUNK_PRESERVATION_REPORT_GLOB,
            "present": bool(trunk_preservation_report),
            "version_line": trunk_preservation_report.get("version_line"),
            "policy_version": trunk_preservation_report.get("policy_version"),
            "packaging_verdict": trunk_preservation_report.get("packaging_verdict"),
            "accepted": trunk_preservation_report.get("accepted"),
            "contained_removed_files": trunk_preservation_report.get("contained_removed_files"),
            "containment_move_count": len(trunk_preservation_report.get("containment_moves") or []),
            "unexpected_removed_files": trunk_preservation_report.get("unexpected_removed_files"),
            "protected_removed_files": trunk_preservation_report.get("protected_removed_files"),
            "new_full_zip": trunk_preservation_report.get("new_full_zip"),
        },
        "safe_full_project_package": {
            "path": str(safe_package_result_rel) if safe_package_result_rel is not None else None,
            "path_pattern": SAFE_FULL_PROJECT_PACKAGE_RESULT_GLOB,
            "present": bool(safe_full_project_package_result),
            "accepted": safe_full_project_package_result.get("accepted"),
            "zip_path": safe_full_project_package_result.get("zip_path"),
            "zip_sha256": safe_full_project_package_result.get("zip_sha256"),
            "zip_root_verdict": (safe_full_project_package_result.get("zip_root_audit") or {}).get("verdict"),
            "archive_root_mode": (safe_full_project_package_result.get("zip_root_audit") or {}).get("archive_root_mode"),
        },
        "v72_mcp_donor_reconciliation": {
            "path": str(V72_MCP_DONOR_RECONCILIATION_AUDIT_RELATIVE_PATH),
            "present": bool(v72_mcp_donor_reconciliation_audit),
            "verdict": v72_mcp_donor_reconciliation_audit.get("reconciliation_verdict"),
            "restored_donor_surface_count": v72_mcp_donor_reconciliation_audit.get("restored_donor_surface_count"),
            "missing_donor_surface_count": v72_mcp_donor_reconciliation_audit.get("missing_donor_surface_count"),
            "forbidden_runtime_file_count": v72_mcp_donor_reconciliation_audit.get("forbidden_runtime_file_count"),
            "cursor_bridge_preserved": v72_mcp_donor_reconciliation_audit.get("cursor_bridge_preserved"),
            "donor_runtime_receipts_restored": v72_mcp_donor_reconciliation_audit.get("donor_runtime_receipts_restored"),
            "live_execution_authority": v72_mcp_donor_reconciliation_audit.get("live_execution_authority", False),
            "production_authority": v72_mcp_donor_reconciliation_audit.get("production_authority", False),
        },
        "next_lawful_action": next_action,
        "authoritative_paths": {name: str(rel) for name, rel in paths.items()},
        "optional_evidence_paths": {
            name: str(rel)
            if rel is not None
            else (
                TRUNK_PRESERVATION_REPORT_GLOB
                if name == "trunk_preservation_report"
                else SAFE_FULL_PROJECT_PACKAGE_RESULT_GLOB
            )
            for name, rel in optional_paths.items()
        },
        "production_authority": False,
        "live_execution_authority": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Report active ION carrier status without mutating runtime work.")
    parser.add_argument("--ion-root", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = build_ion_status(args.ion_root)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["verdict"])
        print(f"objective: {result.get('objective')}")
        print(f"spawn_queue_count: {result['spawn_queue_count']}")
        print(f"task_return_counts: {result['task_return_counts']}")
        print(f"operator_queue_counts: {result['operator_queue_counts']}")
        print(f"open_human_gate_count: {result['open_human_gate_count']}")
        print(f"next_lawful_action: {result['next_lawful_action']}")
    return 0 if result["verdict"] in {"ION_STATUS_READY", "ION_STATUS_PARTIAL"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
