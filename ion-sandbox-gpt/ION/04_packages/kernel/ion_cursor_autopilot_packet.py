"""Build the active Cursor /ion autopilot packet.

This module is intentionally lightweight and independent: it summarizes the
host-side contract Cursor must follow before running carrier continuation.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CURRENT = Path("ION/05_context/current")
PACKET_PATH = CURRENT / "ACTIVE_CURSOR_AUTOPILOT_PACKET.json"
STATE_PATH = CURRENT / "ACTIVE_CURSOR_AUTOPILOT_STATE.json"

CONTINUATION_TERMS = {"", "/ion", "continue", "proceed", "resume", "keep going", "next"}
STATUS_TERMS = {"status", "where are we", "what remains", "state"}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _read_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _classify(message: str) -> str:
    normalized = " ".join((message or "").strip().lower().split())
    if normalized.startswith("/ion"):
        tail = normalized[4:].strip()
        if not tail:
            return "continuation_signal"
        normalized = tail
    if normalized in CONTINUATION_TERMS:
        return "continuation_signal"
    if normalized in STATUS_TERMS or normalized.endswith(" status"):
        return "status_request"
    if normalized in {"yes", "approved", "approve", "no", "reject", "denied"}:
        return "human_gate_answer_or_short_directive"
    return "new_work_directive"


def _count_list(obj: Any, *keys: str) -> int:
    cur = obj
    for key in keys:
        if not isinstance(cur, dict):
            return 0
        cur = cur.get(key)
    if isinstance(cur, list):
        return len(cur)
    return 0


def build_autopilot_packet(root: Path, operator_message: str = "continue") -> dict[str, Any]:
    current = root / CURRENT
    classification = _classify(operator_message)
    turn = _read_json(current / "ACTIVE_CARRIER_TURN_PACKET.json") or {}
    spawn = _read_json(current / "ACTIVE_ROLE_SPAWN_PLAN.json") or {}
    queue = _read_json(current / "ACTIVE_OPERATOR_MESSAGE_QUEUE.json") or {}
    gates = _read_json(current / "ACTIVE_HUMAN_GATE_QUEUE.json") or {}
    ledger = _read_json(current / "ACTIVE_CARRIER_TASK_RETURN_LEDGER.json") or {}
    steward = _read_json(current / "ACTIVE_STEWARD_INTEGRATION_QUEUE.json") or {}
    mcp = _read_json(current / "ACTIVE_MCP_BRIDGE_STATE.json") or {}

    spawn_rows = turn.get("spawn_queue") or spawn.get("spawn_rows") or spawn.get("roles") or []
    if not isinstance(spawn_rows, list):
        spawn_rows = []

    open_gates = []
    for item in gates.get("gates", []) if isinstance(gates, dict) else []:
        if isinstance(item, dict) and item.get("status") in {None, "open", "blocking"}:
            open_gates.append(item)

    accepted_returns = _count_list(ledger, "accepted_returns") + _count_list(steward, "accepted_returns")
    rejected_returns = _count_list(ledger, "rejected_returns")

    return {
        "schema_id": "ion.cursor_autopilot_packet.v1",
        "generated_at": _now(),
        "operator_message": operator_message or "continue",
        "operator_message_classification": classification,
        "cursor_parent_identity": "CURSOR_CARRIER_CONTROL_SURFACE",
        "not_ion_roles": [
            "STEWARD",
            "RELAY",
            "PERSONA_INTERFACE",
            "MASON",
            "NEMESIS",
            "CONTEXT_CARTOGRAPHER",
            "RUNTIME_CARTOGRAPHER",
        ],
        "command_semantics": {
            "/ion": "continue when no argument; otherwise queue/classify argument and run carrier workflow",
            "continue/proceed/resume": "aliases for /ion in an ION shell root",
        },
        "mandatory_sequence": [
            "resolve_shell_root",
            "build_autopilot_packet",
            "run_ion_carrier_continue",
            "read_active_carrier_turn_packet",
            "execute_spawn_true_rows_only",
            "capture_full_worker_returns",
            "run_ion_carrier_task_return_for_each_return",
            "queue_accepted_returns_for_steward",
            "report_accepted_state_or_human_gate",
        ],
        "mcp": {
            "project_server": "ion-control",
            "state_present": bool(mcp),
            "preferred_tools": [
                "ion_status",
                "ion_continue",
                "ion_context_plan",
                "ion_cockpit_view",
                "ion_workflow_audit",
                "ion_read_active_packet",
                "ion_task_return",
            ],
        },
        "subagents": {
            "policy": "Cursor subagents are carrier slots only and must receive generated ION context packages.",
            "project_agents": [
                "ion-steward",
                "ion-relay",
                "ion-persona-interface",
                "ion-mason",
                "ion-nemesis",
                "ion-context-cartographer",
                "ion-runtime-cartographer",
                "ion-scribe",
            ],
            "required_first_output_heading": "### CONTEXT PROOF",
        },
        "live_counts": {
            "spawn_rows": len(spawn_rows),
            "open_human_gates": len(open_gates),
            "operator_queue_items": _count_list(queue, "items"),
            "accepted_returns": accepted_returns,
            "rejected_returns": rejected_returns,
        },
        "stop_conditions": [
            "open_human_gate",
            "workflow_audit_findings",
            "rejected_return_without_safe_rerun",
            "missing_required_tooling",
            "no_open_work_and_no_self_audit_or_evolution_task",
        ],
        "no_user_upkeep_law": "Do not ask the user to choose routine agents, refresh packets, organize context, update files, or sequence normal ION work.",
        "extension_direction": {
            "future_primary_user_surface": "ION Cursor cockpit/persona extension",
            "parent_chat_future_role": "mostly host automation lane triggered by /ion or extension command",
        },
        "paths": {
            "autopilot_packet": str(PACKET_PATH),
            "carrier_turn_packet": str(CURRENT / "ACTIVE_CARRIER_TURN_PACKET.json"),
            "role_spawn_plan": str(CURRENT / "ACTIVE_ROLE_SPAWN_PLAN.json"),
            "operator_queue": str(CURRENT / "ACTIVE_OPERATOR_MESSAGE_QUEUE.json"),
            "human_gate_queue": str(CURRENT / "ACTIVE_HUMAN_GATE_QUEUE.json"),
            "task_return_ledger": str(CURRENT / "ACTIVE_CARRIER_TASK_RETURN_LEDGER.json"),
            "steward_queue": str(CURRENT / "ACTIVE_STEWARD_INTEGRATION_QUEUE.json"),
        },
    }


def write_packet(root: Path, packet: dict[str, Any]) -> None:
    current = root / CURRENT
    current.mkdir(parents=True, exist_ok=True)
    (root / PACKET_PATH).write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    state = {
        "schema_id": "ion.cursor_autopilot_state.v1",
        "updated_at": packet["generated_at"],
        "status": "ION_CURSOR_AUTOPILOT_READY",
        "packet_path": str(PACKET_PATH),
        "operator_message_classification": packet["operator_message_classification"],
        "live_counts": packet["live_counts"],
    }
    (root / STATE_PATH).write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build ION Cursor /ion autopilot packet")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--operator-message", default="continue")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    root = Path(args.ion_root).resolve()
    message = args.operator_message if args.operator_message.strip() else "continue"
    packet = build_autopilot_packet(root, message)
    if args.write:
        write_packet(root, packet)
    if args.json:
        print(json.dumps(packet, indent=2, sort_keys=True))
    else:
        print("ION_CURSOR_AUTOPILOT_READY")
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
