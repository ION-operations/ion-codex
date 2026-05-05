"""Collapse active ION carrier state into one next lawful action.

The carrier onboarding packet explains how a carrier mounts ION. This module
answers the next operational question: what exactly should the mounted carrier
do now, without inferring work from chat memory?
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .ion_carrier_continue import ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH, ACTIVE_TURN_PACKET_RELATIVE_PATH
from .ion_carrier_onboard import ACTIVE_PACKET_RELATIVE_PATH, resolve_shell_root_from_ion_root
from .ion_carrier_onboarding_packet import (
    CARRIER_PROFILE_BY_ALIAS,
    OUTPUT_RELATIVE_PATH as ACTIVE_CARRIER_ONBOARDING_PACKET_RELATIVE_PATH,
    build_carrier_onboarding_packet,
    carrier_onboarding_packet_output_path,
)
from .ion_carrier_task_return import ACTIVE_TASK_RETURN_LEDGER_RELATIVE_PATH
from .ion_cycle_runner import ACTIVE_SPAWN_PLAN_RELATIVE_PATH
from .ion_human_gate_queue import ACTIVE_HUMAN_GATE_QUEUE_RELATIVE_PATH
from .ion_status import build_ion_status

SCHEMA_ID = "ion.carrier_tick.v1"
VERSION_LINE = "V125_CARRIER_TICK_NEXT_ACTION_CONTROL_LOOP"
OUTPUT_RELATIVE_PATH = Path("ION/05_context/current/ACTIVE_CARRIER_TICK.json")

ACTION_EXECUTE_CONTEXT_PACKAGE = "EXECUTE_CONTEXT_PACKAGE"
ACTION_RUN_COMMAND = "RUN_COMMAND"
ACTION_WAIT_FOR_HUMAN_GATE = "WAIT_FOR_HUMAN_GATE"
ACTION_SUBMIT_TASK_RETURN = "SUBMIT_TASK_RETURN"
ACTION_READ_PACKET = "READ_PACKET"
ACTION_NO_WORK = "NO_WORK"
ACTION_BLOCKED = "BLOCKED"
ACTION_CAPABILITY_CONFLICT = "CAPABILITY_CONFLICT"

CAPABILITY_KEYS = (
    "can_read_files",
    "can_edit_files",
    "can_run_tests",
    "can_use_mcp",
    "can_spawn_carrier_slots",
)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else None


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _parse_yaml_scalar(value: str) -> Any:
    cleaned = value.strip().strip("\"'")
    lowered = cleaned.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "none", "~"}:
        return None
    return cleaned


def _read_simple_yaml(path: Path) -> dict[str, Any]:
    """Read the top-level scalar subset used by carrier profile YAML files."""

    if not path.exists():
        return {}
    result: dict[str, Any] = {}
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line[:1].isspace() or ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        key = key.strip()
        if key and value.strip():
            result[key] = _parse_yaml_scalar(value)
    return result


def _profile_path_for_carrier(carrier: str) -> Path:
    normalized = carrier.lower().strip()
    return Path(CARRIER_PROFILE_BY_ALIAS.get(normalized, "ION/03_registry/chatgpt_browser_carrier_profile.yaml"))


def _normalize_carrier(value: Any) -> str:
    text = str(value or "").strip().lower()
    return text.removesuffix("_carrier")


def _active_onboarding_packet_for_carrier(shell_root: Path, carrier: str) -> tuple[dict[str, Any], Path, str]:
    carrier_specific_rel = carrier_onboarding_packet_output_path(carrier)
    carrier_specific = _read_json(shell_root / carrier_specific_rel)
    if carrier_specific and _normalize_carrier(carrier_specific.get("carrier_id")) == _normalize_carrier(carrier):
        return carrier_specific, carrier_specific_rel, "carrier_specific_file"

    generic = _read_json(shell_root / ACTIVE_CARRIER_ONBOARDING_PACKET_RELATIVE_PATH)
    if generic and _normalize_carrier(generic.get("carrier_id")) == _normalize_carrier(carrier):
        return generic, ACTIVE_CARRIER_ONBOARDING_PACKET_RELATIVE_PATH, "active_file"

    projected = build_carrier_onboarding_packet(shell_root, carrier_id=carrier)
    return projected, carrier_specific_rel, "projected_for_carrier"


def _action(action: str, **kwargs: Any) -> dict[str, Any]:
    value = {"action": action}
    value.update(kwargs)
    return value


def _command_text(parts: list[str]) -> str:
    return " ".join(parts)


def _carrier_continue_command(*, carrier: str, consume_operator_queue: bool = False) -> dict[str, Any]:
    parts = [
        "PYTHONDONTWRITEBYTECODE=1",
        "PYTHONPATH=ION/04_packages",
        "python3",
        "-S",
        "-m",
        "kernel.ion_carrier_continue",
        "--ion-root",
        ".",
        "--carrier",
        carrier,
        "--operator-message",
        "continue",
        "--max-spawn-rows",
        "1",
        "--mode",
        "manual-cursor",
        "--json",
    ]
    if consume_operator_queue:
        parts.insert(-1, "--consume-operator-queue")
    return {
        "command": parts,
        "command_text": _command_text(parts),
        "purpose": "materialize_or_advance_next_spawn_context_package",
    }


def _steward_integrate_queue_command() -> dict[str, Any]:
    parts = [
        "PYTHONDONTWRITEBYTECODE=1",
        "PYTHONPATH=ION/04_packages",
        "python3",
        "-S",
        "-m",
        "kernel.ion_steward_integrate",
        "--ion-root",
        ".",
        "--integrate-queue",
        "--write",
        "--json",
    ]
    return {
        "command": parts,
        "command_text": _command_text(parts),
        "purpose": "integrate_accepted_task_returns_through_steward_queue",
    }


def _capability_conflicts(work_packet: Mapping[str, Any], carrier_profile: Mapping[str, Any]) -> list[dict[str, Any]]:
    active = work_packet.get("carrier_capabilities")
    if not isinstance(active, Mapping):
        return []
    conflicts: list[dict[str, Any]] = []
    for key in CAPABILITY_KEYS:
        if key not in active or key not in carrier_profile:
            continue
        if active.get(key) != carrier_profile.get(key):
            conflicts.append(
                {
                    "capability": key,
                    "active_work_packet": active.get(key),
                    "carrier_profile": carrier_profile.get(key),
                }
            )
    return conflicts


def _active_spawn_rows(plan: Mapping[str, Any]) -> list[dict[str, Any]]:
    rows = plan.get("role_spawn_plan")
    if not isinstance(rows, list):
        return []
    return [dict(row) for row in rows if isinstance(row, Mapping) and row.get("spawn") is True]


def _role_index_key(value: Mapping[str, Any]) -> tuple[str, int]:
    role = str(value.get("role") or "").lower()
    try:
        index = int(value.get("index") or 0)
    except (TypeError, ValueError):
        index = 0
    return role, index


def _latest_return_records_by_role_index(ledger: Mapping[str, Any]) -> dict[tuple[str, int], dict[str, Any]]:
    records = ledger.get("records")
    if not isinstance(records, list):
        return {}
    latest: dict[tuple[str, int], dict[str, Any]] = {}
    for record in records:
        if not isinstance(record, Mapping):
            continue
        latest[_role_index_key(record)] = dict(record)
    return latest


def _active_spawn_rows_needing_return(plan: Mapping[str, Any], ledger: Mapping[str, Any]) -> list[dict[str, Any]]:
    latest_returns = _latest_return_records_by_role_index(ledger)
    rows: list[dict[str, Any]] = []
    for row in _active_spawn_rows(plan):
        latest = latest_returns.get(_role_index_key(row))
        if latest is None or latest.get("accepted") is not True:
            rows.append(row)
    return rows


def _first_context_package_action(shell_root: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    row = sorted(rows, key=lambda item: int(item.get("index") or 0))[0]
    context_package = str(row.get("context_package_path") or "").strip()
    if not context_package:
        return _action(
            ACTION_BLOCKED,
            reason="spawn_row_missing_context_package_path",
            row_index=row.get("index"),
            role=row.get("role"),
        )
    exists = (shell_root / context_package).exists()
    if not exists:
        return _action(
            ACTION_BLOCKED,
            reason="context_package_path_missing",
            path=context_package,
            row_index=row.get("index"),
            role=row.get("role"),
        )
    return _action(
        ACTION_EXECUTE_CONTEXT_PACKAGE,
        path=context_package,
        row_index=row.get("index"),
        role=row.get("role"),
        context_load_receipt_path=row.get("context_load_receipt_path"),
        required_return_heading="### CONTEXT PROOF",
    )


def _rejected_steward_repair_action(shell_root: Path, steward_queue: Mapping[str, Any]) -> dict[str, Any]:
    items = steward_queue.get("items")
    if not isinstance(items, list):
        return _action(
            ACTION_BLOCKED,
            reason="rejected_steward_integration_queue_unreadable",
            queue_path=ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH.as_posix(),
        )
    rejected = [
        dict(item)
        for item in items
        if isinstance(item, Mapping) and item.get("status") == "STEWARD_INTEGRATION_REJECTED"
    ]
    if not rejected:
        return _action(
            ACTION_BLOCKED,
            reason="status_reports_rejected_steward_integration_but_no_rejected_queue_item_found",
            queue_path=ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH.as_posix(),
        )
    item = sorted(rejected, key=lambda value: int(value.get("index") or 0))[0]
    context_package = str(item.get("context_package_path") or "").strip()
    if not context_package:
        return _action(
            ACTION_BLOCKED,
            reason="rejected_steward_item_missing_context_package_path",
            queue_path=ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH.as_posix(),
            row_index=item.get("index"),
            role=item.get("role"),
        )
    if not (shell_root / context_package).exists():
        return _action(
            ACTION_BLOCKED,
            reason="rejected_steward_item_context_package_missing",
            path=context_package,
            queue_path=ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH.as_posix(),
            row_index=item.get("index"),
            role=item.get("role"),
        )
    return _action(
        ACTION_EXECUTE_CONTEXT_PACKAGE,
        reason="repair_rejected_steward_integration_return_with_template_action_proof",
        path=context_package,
        row_index=item.get("index"),
        role=item.get("role"),
        context_load_receipt_path=item.get("context_load_receipt_path"),
        rejected_task_output_path=item.get("task_output_path"),
        steward_receipt_path=item.get("steward_receipt_path"),
        steward_gate_findings=list(item.get("steward_gate_findings") or []),
        required_return_headings=["### CONTEXT PROOF", "### TEMPLATE ACTION PROOF"],
    )


def build_carrier_tick(root: str | Path | None = None, *, carrier: str = "codex_extension") -> dict[str, Any]:
    """Return the single next action a mounted carrier should take."""

    shell_root = resolve_shell_root_from_ion_root(root)
    status = build_ion_status(shell_root)
    work_packet = _read_json(shell_root / ACTIVE_PACKET_RELATIVE_PATH) or {}
    active_onboarding, active_onboarding_rel, active_onboarding_source = _active_onboarding_packet_for_carrier(
        shell_root,
        carrier,
    )
    turn_packet = _read_json(shell_root / ACTIVE_TURN_PACKET_RELATIVE_PATH) or {}
    spawn_plan = _read_json(shell_root / ACTIVE_SPAWN_PLAN_RELATIVE_PATH) or {}
    steward_queue = _read_json(shell_root / ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH) or {}
    task_return_ledger = _read_json(shell_root / ACTIVE_TASK_RETURN_LEDGER_RELATIVE_PATH) or {}
    profile_rel = _profile_path_for_carrier(carrier)
    carrier_profile = _read_simple_yaml(shell_root / profile_rel)
    findings: list[str] = []

    if status.get("missing_state_surfaces"):
        findings.append("status_reports_missing_state_surfaces")
    if active_onboarding and _normalize_carrier(active_onboarding.get("carrier_id")) != _normalize_carrier(carrier):
        findings.append("active_onboarding_packet_carrier_mismatch")
    if turn_packet and _normalize_carrier(turn_packet.get("carrier")) != _normalize_carrier(carrier):
        findings.append("active_turn_packet_carrier_mismatch")
    if spawn_plan and _normalize_carrier(spawn_plan.get("carrier")) != _normalize_carrier(carrier):
        findings.append("active_spawn_plan_carrier_mismatch")

    open_gates = status.get("open_human_gates")
    if isinstance(open_gates, list) and open_gates:
        gate = open_gates[0] if isinstance(open_gates[0], Mapping) else {}
        next_action = _action(
            ACTION_WAIT_FOR_HUMAN_GATE,
            gate_id=gate.get("id"),
            prompt=gate.get("prompt"),
            gate_queue_path=ACTIVE_HUMAN_GATE_QUEUE_RELATIVE_PATH.as_posix(),
        )
    else:
        conflicts = _capability_conflicts(work_packet, carrier_profile)
        if conflicts:
            next_action = _action(
                ACTION_CAPABILITY_CONFLICT,
                reason="carrier_profile_conflicts_with_active_work_packet",
                conflicts=conflicts,
                active_work_packet_path=ACTIVE_PACKET_RELATIVE_PATH.as_posix(),
                carrier_profile_path=profile_rel.as_posix(),
            )
        else:
            if status.get("next_lawful_action") == "spawn_steward_integration_from_accepted_queue":
                next_action = _action(
                    ACTION_RUN_COMMAND,
                    reason="accepted_task_return_requires_steward_integration_before_reexecuting_spawn_rows",
                    **_steward_integrate_queue_command(),
                )
            elif status.get("next_lawful_action") == "repair_rejected_steward_integration":
                next_action = _rejected_steward_repair_action(shell_root, steward_queue)
            else:
                active_rows = _active_spawn_rows_needing_return(spawn_plan, task_return_ledger)
                if active_rows:
                    next_action = _first_context_package_action(shell_root, active_rows)
                elif int(status.get("deferred_spawn_count") or 0) > 0:
                    next_action = _action(
                        ACTION_RUN_COMMAND,
                        reason="deferred_spawn_rows_require_context_package_materialization_or_advancement",
                        **_carrier_continue_command(carrier=carrier),
                    )
                elif status.get("next_lawful_action") == "run_ion_carrier_continue_with_consume_operator_queue":
                    next_action = _action(
                        ACTION_RUN_COMMAND,
                        reason="pending_operator_queue_item",
                        **_carrier_continue_command(carrier=carrier, consume_operator_queue=True),
                    )
                elif status.get("next_lawful_action") == "execute_spawn_rows_and_run_task_return_intake":
                    next_action = _action(
                        ACTION_SUBMIT_TASK_RETURN,
                        reason="spawn_rows_exist_but_task_returns_are_not_complete",
                        expected_path="ION/05_context/current/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json",
                    )
                elif status.get("missing_state_surfaces"):
                    missing = list(status.get("missing_state_surfaces") or [])
                    next_action = _action(
                        ACTION_READ_PACKET,
                        reason="missing_state_surface_requires_repair",
                        path=missing[0] if missing else None,
                    )
                elif status.get("next_lawful_action") == "continue_or_queue_new_work":
                    next_action = _action(ACTION_NO_WORK, reason="no_active_spawn_rows_no_open_gates_no_pending_queue")
                else:
                    next_action = _action(
                        ACTION_BLOCKED,
                        reason="unhandled_status_next_lawful_action",
                        status_next_lawful_action=status.get("next_lawful_action"),
                    )

    return {
        "schema_id": SCHEMA_ID,
        "version_line": VERSION_LINE,
        "generated_at": _now(),
        "carrier": carrier,
        "objective": status.get("objective") or turn_packet.get("objective") or spawn_plan.get("objective") or work_packet.get("objective"),
        "status_verdict": status.get("verdict"),
        "status_next_lawful_action": status.get("next_lawful_action"),
        "active_work_packet_path": ACTIVE_PACKET_RELATIVE_PATH.as_posix(),
        "active_carrier_onboarding_packet_path": active_onboarding_rel.as_posix(),
        "active_carrier_onboarding_packet_source": active_onboarding_source,
        "active_turn_packet_path": ACTIVE_TURN_PACKET_RELATIVE_PATH.as_posix(),
        "active_spawn_plan_path": ACTIVE_SPAWN_PLAN_RELATIVE_PATH.as_posix(),
        "carrier_profile_path": profile_rel.as_posix(),
        "next_action": next_action,
        "findings": findings,
        "production_authority": False,
        "live_execution_authority": False,
    }


def write_carrier_tick(
    root: str | Path | None = None,
    *,
    carrier: str = "codex_extension",
    output: str | Path | None = None,
) -> dict[str, Any]:
    shell_root = resolve_shell_root_from_ion_root(root)
    result = build_carrier_tick(shell_root, carrier=carrier)
    out = shell_root / (Path(output) if output else OUTPUT_RELATIVE_PATH)
    _write_json(out, result)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compute one next lawful ION carrier action.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--carrier", default="codex_extension")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = (
        write_carrier_tick(args.ion_root, carrier=args.carrier, output=args.output)
        if args.write
        else build_carrier_tick(args.ion_root, carrier=args.carrier)
    )
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        action = result["next_action"]
        print(action["action"])
        if action.get("path"):
            print(f"path: {action['path']}")
        if action.get("command_text"):
            print(action["command_text"])
        if action.get("reason"):
            print(f"reason: {action['reason']}")
    return 0 if result["next_action"]["action"] not in {ACTION_BLOCKED, ACTION_CAPABILITY_CONFLICT} else 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
