"""Audit the active Cursor carrier workflow surfaces.

This audit is intentionally narrow. It checks the failure mode that made the
Cursor carrier brittle: stale spawn plans, path-only onboarding, MINI/CAPSULE
before Agent Context System authority, and missing carrier-turn state.
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
from .ion_human_gate_queue import ACTIVE_HUMAN_GATE_QUEUE_RELATIVE_PATH
from .ion_operator_message_queue import ACTIVE_OPERATOR_MESSAGE_QUEUE_RELATIVE_PATH
from .ion_carrier_onboard import ACTIVE_PACKET_RELATIVE_PATH, resolve_shell_root_from_ion_root
from .ion_cycle_runner import ACTIVE_SPAWN_PLAN_RELATIVE_PATH


REQUIRED_CONTEXT_PREFIXES = (
    "ION/02_architecture/ION_AGENT_CONTEXT_SYSTEMS_PROTOCOL.md",
    "ION/03_registry/agent_context_system_registry.yaml",
    "ION/05_context/current/agent_context_systems/",
    "ION/07_templates/context/AGENT_CONTEXT_BUILD_STEP.md",
)


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _path_index(paths: list[str], predicate) -> int | None:
    for idx, path in enumerate(paths):
        if predicate(path):
            return idx
    return None


def _zero_spawn_turn_is_lawful(turn: Mapping[str, Any], plan: Mapping[str, Any] | None) -> bool:
    if turn.get("spawn_row_limit") != 0:
        return False
    if plan is None:
        return False
    return (
        plan.get("spawn_row_limit") == 0
        and plan.get("active_spawn_count") == 0
        and plan.get("execution_bundle_materialized") is False
    )


def audit_carrier_workflow(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = resolve_shell_root_from_ion_root(root)
    findings: list[str] = []

    active_packet_path = shell_root / ACTIVE_PACKET_RELATIVE_PATH
    active_plan_path = shell_root / ACTIVE_SPAWN_PLAN_RELATIVE_PATH
    active_turn_path = shell_root / ACTIVE_TURN_PACKET_RELATIVE_PATH
    active_ledger_path = shell_root / ACTIVE_TASK_RETURN_LEDGER_RELATIVE_PATH
    active_queue_path = shell_root / ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH
    operator_queue_path = shell_root / ACTIVE_OPERATOR_MESSAGE_QUEUE_RELATIVE_PATH
    human_gate_queue_path = shell_root / ACTIVE_HUMAN_GATE_QUEUE_RELATIVE_PATH

    packet = _read_json(active_packet_path)
    plan = _read_json(active_plan_path)
    turn = _read_json(active_turn_path)
    ledger = _read_json(active_ledger_path)
    queue = _read_json(active_queue_path)
    operator_queue = _read_json(operator_queue_path)
    human_gate_queue = _read_json(human_gate_queue_path)

    if packet is None:
        findings.append(f"missing_active_work_packet:{ACTIVE_PACKET_RELATIVE_PATH}")
    if plan is None:
        findings.append(f"missing_active_spawn_plan:{ACTIVE_SPAWN_PLAN_RELATIVE_PATH}")
    if turn is None:
        findings.append(f"missing_active_carrier_turn_packet:{ACTIVE_TURN_PACKET_RELATIVE_PATH}")
    if ledger is None:
        findings.append(f"missing_active_task_return_ledger:{ACTIVE_TASK_RETURN_LEDGER_RELATIVE_PATH}")
    if queue is None:
        findings.append(f"missing_active_steward_integration_queue:{ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH}")
    if operator_queue is None:
        findings.append(f"missing_active_operator_message_queue:{ACTIVE_OPERATOR_MESSAGE_QUEUE_RELATIVE_PATH}")
    if human_gate_queue is None:
        findings.append(f"missing_active_human_gate_queue:{ACTIVE_HUMAN_GATE_QUEUE_RELATIVE_PATH}")

    if (shell_root / "_archive").exists():
        findings.append("productization_live_root_contains_archive_directory")

    if plan is not None:
        if plan.get("schema_id") != "ion.carrier_cycle_plan.v1":
            findings.append("active_spawn_plan_missing_or_invalid_schema_id")
        execution_root = str(plan.get("execution_bundle_root", ""))
        if "v77" in execution_root.lower():
            findings.append(f"active_spawn_plan_stale_execution_root:{execution_root}")

        rows = plan.get("role_spawn_plan")
        if not isinstance(rows, list) or not rows:
            findings.append("active_spawn_plan_missing_role_spawn_plan")
        else:
            for row in rows:
                if row.get("spawn") is not True:
                    continue
                role = row.get("role", "unknown")
                context_package = row.get("context_package_path")
                receipt = row.get("context_load_receipt_path")
                if not context_package:
                    findings.append(f"{role}:missing_context_package_path")
                elif not (shell_root / str(context_package)).exists():
                    findings.append(f"{role}:context_package_path_missing_on_disk:{context_package}")
                else:
                    text = (shell_root / str(context_package)).read_text(encoding="utf-8", errors="replace")
                    if "## Agent Context System authority" not in text:
                        findings.append(f"{role}:context_package_missing_agent_context_system_authority_section")
                    if "### CONTEXT PROOF" not in text:
                        findings.append(f"{role}:context_package_missing_context_proof_contract")

                compiled_bundle = row.get("compiled_context_bundle_path")
                if not compiled_bundle:
                    findings.append(f"{role}:missing_compiled_context_bundle_path")
                elif not (shell_root / str(compiled_bundle)).exists():
                    findings.append(f"{role}:compiled_context_bundle_missing_on_disk:{compiled_bundle}")
                else:
                    bundle_text = (shell_root / str(compiled_bundle)).read_text(encoding="utf-8", errors="replace")
                    if f"COMPILED {str(role).upper()} CONTEXT BUNDLE" not in bundle_text:
                        findings.append(f"{role}:compiled_context_bundle_missing_role_header")
                    if "## Agent Context System authority" not in bundle_text:
                        findings.append(f"{role}:compiled_context_bundle_missing_agent_context_system_authority_section")
                    if "### CONTEXT PROOF" not in bundle_text:
                        findings.append(f"{role}:compiled_context_bundle_missing_context_proof_contract")

                if not receipt:
                    findings.append(f"{role}:missing_context_load_receipt_path")
                elif not (shell_root / str(receipt)).exists():
                    findings.append(f"{role}:context_load_receipt_missing_on_disk:{receipt}")
                else:
                    receipt_json = _read_json(shell_root / str(receipt)) or {}
                    if "agent_context_system" not in receipt_json:
                        findings.append(f"{role}:receipt_missing_agent_context_system")

                agent_context_system = row.get("agent_context_system")
                if not isinstance(agent_context_system, Mapping):
                    findings.append(f"{role}:missing_agent_context_system_summary")
                elif agent_context_system.get("status") != "active":
                    findings.append(f"{role}:agent_context_system_not_active:{agent_context_system.get('status')}")

                context_system_reads = row.get("context_system_read_paths")
                if not isinstance(context_system_reads, list) or not context_system_reads:
                    findings.append(f"{role}:missing_context_system_read_paths")

                read_paths = [str(item) for item in row.get("read_paths_ordered", [])]
                first_mini = _path_index(read_paths, lambda p: p.endswith("/MINI.md") or p.endswith("/CAPSULE.md"))
                first_context = _path_index(read_paths, lambda p: p.startswith("ION/02_architecture/ION_AGENT_CONTEXT_SYSTEMS_PROTOCOL.md"))
                if first_context is None:
                    findings.append(f"{role}:read_order_missing_agent_context_system_protocol")
                if first_mini is not None and (first_context is None or first_mini < first_context):
                    findings.append(f"{role}:legacy_mini_capsule_precedes_agent_context_system")
                for prefix in REQUIRED_CONTEXT_PREFIXES:
                    if not any(path.startswith(prefix) for path in read_paths):
                        findings.append(f"{role}:read_order_missing_required_context_surface:{prefix}")

    if turn is not None:
        if turn.get("schema_id") != "ion.carrier_turn_packet.v1":
            findings.append("active_turn_packet_missing_or_invalid_schema_id")
        if turn.get("active_spawn_plan_path") != str(ACTIVE_SPAWN_PLAN_RELATIVE_PATH):
            findings.append("active_turn_packet_not_bound_to_active_spawn_plan")
        blocked_by_gate = turn.get("blocked_by_human_gate") is True
        zero_spawn_lawful = _zero_spawn_turn_is_lawful(turn, plan)
        if not isinstance(turn.get("spawn_queue"), list) or (not turn.get("spawn_queue") and not blocked_by_gate and not zero_spawn_lawful):
            findings.append("active_turn_packet_missing_spawn_queue")
        if turn.get("production_authority") is not False:
            findings.append("active_turn_packet_production_authority_not_false")
        if turn.get("live_execution_authority") is not False:
            findings.append("active_turn_packet_live_execution_authority_not_false")
        if turn.get("task_return_ledger_path") != str(ACTIVE_TASK_RETURN_LEDGER_RELATIVE_PATH):
            findings.append("active_turn_packet_not_bound_to_active_task_return_ledger")
        if turn.get("steward_integration_queue_path") != str(ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH):
            findings.append("active_turn_packet_not_bound_to_steward_integration_queue")
        if turn.get("operator_message_queue_path") != str(ACTIVE_OPERATOR_MESSAGE_QUEUE_RELATIVE_PATH):
            findings.append("active_turn_packet_not_bound_to_operator_message_queue")
        if turn.get("human_gate_queue_path") != str(ACTIVE_HUMAN_GATE_QUEUE_RELATIVE_PATH):
            findings.append("active_turn_packet_not_bound_to_human_gate_queue")
        if not isinstance(turn.get("operator_message_classification"), Mapping):
            findings.append("active_turn_packet_missing_operator_message_classification")
        intake = turn.get("return_intake_state")
        if not isinstance(intake, Mapping):
            findings.append("active_turn_packet_missing_return_intake_state")
        elif intake.get("status") not in {"WAITING_FOR_TASK_RETURNS", "WAITING_OR_REJECTED_TASK_RETURNS", "ALL_ACCEPTED_READY_FOR_STEWARD", "BLOCKED_BY_HUMAN_GATE", "NO_TASK_RETURNS_REQUIRED"}:
            findings.append(f"active_turn_packet_invalid_return_intake_status:{intake.get('status')}")

    if ledger is not None:
        if ledger.get("schema_id") != "ion.carrier_task_return_ledger.v1":
            findings.append("active_task_return_ledger_invalid_schema_id")
        if ledger.get("active_spawn_plan_path") != str(ACTIVE_SPAWN_PLAN_RELATIVE_PATH):
            findings.append("active_task_return_ledger_not_bound_to_active_spawn_plan")
        if ledger.get("production_authority") is not False:
            findings.append("active_task_return_ledger_production_authority_not_false")
        if ledger.get("live_execution_authority") is not False:
            findings.append("active_task_return_ledger_live_execution_authority_not_false")
    if queue is not None:
        if queue.get("schema_id") != "ion.steward_integration_queue.v1":
            findings.append("active_steward_integration_queue_invalid_schema_id")
        if queue.get("active_spawn_plan_path") != str(ACTIVE_SPAWN_PLAN_RELATIVE_PATH):
            findings.append("active_steward_integration_queue_not_bound_to_active_spawn_plan")
        if queue.get("production_authority") is not False:
            findings.append("active_steward_integration_queue_production_authority_not_false")
        if queue.get("live_execution_authority") is not False:
            findings.append("active_steward_integration_queue_live_execution_authority_not_false")


    if operator_queue is not None:
        if operator_queue.get("schema_id") != "ion.operator_message_queue.v1":
            findings.append("active_operator_message_queue_invalid_schema_id")
        if operator_queue.get("production_authority") is not False:
            findings.append("active_operator_message_queue_production_authority_not_false")
        if operator_queue.get("live_execution_authority") is not False:
            findings.append("active_operator_message_queue_live_execution_authority_not_false")
    if human_gate_queue is not None:
        if human_gate_queue.get("schema_id") != "ion.human_gate_queue.v1":
            findings.append("active_human_gate_queue_invalid_schema_id")
        if human_gate_queue.get("production_authority") is not False:
            findings.append("active_human_gate_queue_production_authority_not_false")
        if human_gate_queue.get("live_execution_authority") is not False:
            findings.append("active_human_gate_queue_live_execution_authority_not_false")

    return {
        "schema_id": "ion.carrier_workflow_audit.v1",
        "verdict": "ION_CARRIER_WORKFLOW_READY" if not findings else "ION_CARRIER_WORKFLOW_BLOCKED",
        "accepted": not findings,
        "findings": findings,
        "active_work_packet_path": str(ACTIVE_PACKET_RELATIVE_PATH),
        "active_spawn_plan_path": str(ACTIVE_SPAWN_PLAN_RELATIVE_PATH),
        "active_turn_packet_path": str(ACTIVE_TURN_PACKET_RELATIVE_PATH),
        "active_task_return_ledger_path": str(ACTIVE_TASK_RETURN_LEDGER_RELATIVE_PATH),
        "active_steward_integration_queue_path": str(ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH),
        "active_operator_message_queue_path": str(ACTIVE_OPERATOR_MESSAGE_QUEUE_RELATIVE_PATH),
        "active_human_gate_queue_path": str(ACTIVE_HUMAN_GATE_QUEUE_RELATIVE_PATH),
        "production_authority": False,
        "live_execution_authority": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit ION active carrier workflow state.")
    parser.add_argument("--ion-root", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = audit_carrier_workflow(args.ion_root)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["verdict"])
        for finding in result["findings"]:
            print(f"- {finding}")
    return 0 if result["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
