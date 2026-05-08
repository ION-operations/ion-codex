"""Carrier continuation control loop for ION role-phase execution.

This is the safe ``continue/proceed/resume`` entrypoint. It does not perform
live external execution, does not call optional worker surfaces itself, and does not grant
production authority. It refreshes the file-backed carrier state that the declared carrier
must follow:

1. ACTIVE_WORK_PACKET.json
2. ACTIVE_ROLE_SPAWN_PLAN.json
3. ACTIVE_CARRIER_TURN_PACKET.json
4. ACTIVE_CARRIER_TASK_RETURN_LEDGER.json
5. ACTIVE_STEWARD_INTEGRATION_QUEUE.json
6. ACTIVE_OPERATOR_MESSAGE_QUEUE.json
7. ACTIVE_HUMAN_GATE_QUEUE.json

V88 adds durable operator-message classification/queueing and human gate state.
Cursor no longer has to infer whether "continue" is a new task, a queued work
advance, a gate answer, or a status request.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .ion_carrier_onboard import (
    ACTIVE_PACKET_RELATIVE_PATH,
    onboard_carrier,
    resolve_shell_root_from_ion_root,
)
from .ion_cycle_runner import (
    ACTIVE_SPAWN_PLAN_RELATIVE_PATH,
    build_cycle_plan,
    validate_cycle_plan,
    write_cycle_plan,
)
from .ion_human_gate_queue import (
    ACTIVE_HUMAN_GATE_QUEUE_RELATIVE_PATH,
    load_human_gate_queue,
    resolve_human_gate,
    unresolved_human_gates,
)
from .ion_operator_message_classifier import classify_operator_message
from .ion_operator_message_queue import (
    ACTIVE_OPERATOR_MESSAGE_QUEUE_RELATIVE_PATH,
    claim_next_operator_message,
    complete_operator_message,
    enqueue_operator_message,
    load_operator_message_queue,
)

ACTIVE_TURN_PACKET_RELATIVE_PATH = Path("ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json")
ACTIVE_TASK_RETURN_LEDGER_RELATIVE_PATH = Path("ION/05_context/current/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json")
ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH = Path("ION/05_context/current/ACTIVE_STEWARD_INTEGRATION_QUEUE.json")

CONTINUATION_SIGNALS = {
    "",
    "continue",
    "proceed",
    "resume",
    "keep going",
    "carry on",
    "next",
    "run next",
    "continue.",
    "proceed.",
    "resume.",
}


def _default_mode_for_carrier(carrier: str) -> str:
    """Return the operator-facing carrier mode label without granting authority."""
    normalized = (carrier or "").lower().strip()
    if normalized in {
        "gpt_sandbox",
        "gpt_sandbox_carrier",
        "gpt_sandbox_runtime",
        "gpt_uploaded_zip",
        "gpt_full_ion_package",
        "ion_gpt",
        "ion_gpt_sandbox",
        "single_carrier_sandbox",
        "self_contained_sandbox",
        "gpt-5.5 thinking",
        "gpt-5.5",
    }:
        return "gpt-sandbox"
    return "manual-cursor"


def _iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _normalize_operator_message(message: str | None) -> str:
    return " ".join((message or "").strip().lower().split())


def _safe_slug(value: str) -> str:
    import re
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")[:80] or "continue"


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _safe_relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _workstream_from_packet(packet: Mapping[str, Any] | None) -> str:
    if not packet:
        return "implementation"
    route_source = packet.get("route_source", {})
    if isinstance(route_source, Mapping):
        workstream = route_source.get("workstream")
        if isinstance(workstream, str) and workstream:
            return workstream
    return "implementation"


def _objective_from_packet(packet: Mapping[str, Any] | None) -> str:
    if packet and isinstance(packet.get("objective"), str) and packet["objective"].strip():
        return str(packet["objective"]).strip()
    return "continue the current ION work cycle through the active carrier packet"


def _is_continuation_signal(operator_message: str | None) -> bool:
    return _normalize_operator_message(operator_message) in CONTINUATION_SIGNALS


def _classification_for_forced_objective(classification: Mapping[str, Any], *, forced: bool) -> dict[str, Any]:
    """Make forced objective refresh explicit even when text resembles status."""

    updated = dict(classification)
    if not forced:
        return updated
    original = str(updated.get("classification") or "")
    updated.update(
        {
            "classification": "new_work_directive",
            "action": "record_operator_work_item_and_refresh_carrier",
            "confidence": max(float(updated.get("confidence", 0.0) or 0.0), 0.9),
            "mutates_runtime": True,
            "forced_objective_refresh": True,
            "original_classification": original,
        }
    )
    return updated


def _read_operator_message_file(path: str | Path | None) -> str | None:
    if not path:
        return None
    return Path(path).read_text(encoding="utf-8").strip()


def _limited_spawn_rows(plan: Mapping[str, Any], max_spawn_rows: int | None) -> list[dict[str, Any]]:
    spawned_rows = [
        {
            "index": row.get("index"),
            "role": row.get("role"),
            "carrier_slot": row.get("carrier_slot"),
            "context_package_path": row.get("context_package_path"),
            "context_load_receipt_path": row.get("context_load_receipt_path"),
            "context_proof_return_gate": row.get("context_proof_return_gate"),
            "authority": row.get("authority"),
        }
        for row in plan.get("role_spawn_plan", [])
        if isinstance(row, Mapping) and row.get("spawn") is True
    ]
    if max_spawn_rows is not None and max_spawn_rows >= 0:
        return spawned_rows[:max_spawn_rows]
    return spawned_rows


def _role_index(item: Mapping[str, Any]) -> int | None:
    try:
        return int(item.get("index"))
    except (TypeError, ValueError):
        return None


def _execution_scope_markers(execution_bundle_root: str | None) -> tuple[str, ...]:
    if not execution_bundle_root:
        return ()
    markers = [execution_bundle_root]
    marker = "_carrier_continue_"
    if marker in execution_bundle_root:
        markers.append(f"carrier_continue_{execution_bundle_root.rsplit(marker, 1)[1]}")
    return tuple(dict.fromkeys(markers))


def _path_refs_execution_scope(value: Any, execution_bundle_root: str | None) -> bool:
    markers = _execution_scope_markers(execution_bundle_root)
    if not markers:
        return True
    if isinstance(value, str):
        return any(marker in value for marker in markers)
    if isinstance(value, Mapping):
        return any(_path_refs_execution_scope(nested, execution_bundle_root) for nested in value.values())
    if isinstance(value, list):
        return any(_path_refs_execution_scope(nested, execution_bundle_root) for nested in value)
    return False


def _historical_steward_integration_items(
    shell_root: Path | None,
    *,
    execution_bundle_root: str | None = None,
) -> list[dict[str, Any]]:
    if shell_root is None:
        return []
    receipts_root = shell_root / "ION/05_context/current/steward_integrations"
    if not receipts_root.exists():
        return []
    items: list[dict[str, Any]] = []
    for path in sorted(receipts_root.glob("*_steward_integration.json")):
        receipt = _read_json(path)
        if not receipt or receipt.get("accepted") is not True:
            continue
        index = _role_index(receipt)
        role = receipt.get("role")
        if index is None or not role:
            continue
        if execution_bundle_root and not _path_refs_execution_scope(receipt, execution_bundle_root):
            continue
        items.append(
            {
                "schema_id": "ion.steward_integration_queue_item.v1",
                "created_at": receipt.get("created_at"),
                "status": "STEWARD_INTEGRATED",
                "role": role,
                "index": index,
                "accepted": True,
                "task_output_path": receipt.get("task_output_path"),
                "task_output_sha256": receipt.get("task_output_sha256"),
                "steward_receipt_id": receipt.get("receipt_id"),
                "steward_receipt_path": _safe_relative(path, shell_root),
                "steward_decision": receipt.get("decision"),
                "template_id": (receipt.get("gate") or {}).get("template_id") if isinstance(receipt.get("gate"), Mapping) else None,
                "action_id": (receipt.get("gate") or {}).get("action_id") if isinstance(receipt.get("gate"), Mapping) else None,
                "touched_paths": (receipt.get("gate") or {}).get("touched_paths", []) if isinstance(receipt.get("gate"), Mapping) else [],
            }
        )
    return items


def _history_sort_key(item: Mapping[str, Any]) -> tuple[str, str]:
    timestamp = str(
        item.get("steward_integrated_at")
        or item.get("accepted_at")
        or item.get("created_at")
        or item.get("updated_at")
        or ""
    )
    path = str(item.get("steward_receipt_path") or item.get("task_output_path") or item.get("receipt_id") or "")
    return (timestamp, path)


def _keep_latest_by_index(target: dict[int, dict[str, Any]], index: int, item: dict[str, Any]) -> None:
    existing = target.get(index)
    if existing is None or _history_sort_key(item) >= _history_sort_key(existing):
        target[index] = item


def _latest_completed_role_history(
    *,
    steward_queue: Mapping[str, Any] | None,
    ledger: Mapping[str, Any] | None,
    shell_root: Path | None = None,
    execution_bundle_root: str | None = None,
) -> dict[str, Any]:
    """Return completed role rows proven by Steward integration.

    Completed rows are not copied into the next active return ledger as pending
    work. They are carried as completed history so the planner can advance to
    the next deferred role without making the carrier re-run integrated work.
    """

    latest_integrated_by_index: dict[int, dict[str, Any]] = {}
    steward_candidates: list[Any] = []
    if steward_queue:
        for key in ("completed_items", "items"):
            if isinstance(steward_queue.get(key), list):
                steward_candidates.extend(steward_queue.get(key, []))
    steward_candidates.extend(
        _historical_steward_integration_items(
            shell_root,
            execution_bundle_root=execution_bundle_root,
        )
    )
    if steward_candidates:
        for item in steward_candidates:
            if not isinstance(item, Mapping):
                continue
            if execution_bundle_root and not _path_refs_execution_scope(item, execution_bundle_root):
                continue
            index = _role_index(item)
            if index is None:
                continue
            if item.get("status") == "STEWARD_INTEGRATED" and item.get("accepted") is True:
                mutable = dict(item)
                _keep_latest_by_index(latest_integrated_by_index, index, mutable)

    accepted_records_by_index: dict[int, dict[str, Any]] = {}
    record_candidates: list[Any] = []
    if ledger:
        for key in ("completed_records", "records"):
            if isinstance(ledger.get(key), list):
                record_candidates.extend(ledger.get(key, []))
    if record_candidates:
        for record in record_candidates:
            if not isinstance(record, Mapping):
                continue
            if execution_bundle_root and not _path_refs_execution_scope(record, execution_bundle_root):
                continue
            index = _role_index(record)
            if index is None:
                continue
            if record.get("accepted") is True:
                mutable = dict(record)
                _keep_latest_by_index(accepted_records_by_index, index, mutable)

    completed_indexes = sorted(latest_integrated_by_index)
    completed_steward_items = [
        latest_integrated_by_index[index]
        for index in completed_indexes
    ]
    completed_records = [
        accepted_records_by_index[index]
        for index in sorted(accepted_records_by_index)
    ]
    evidence: dict[int, dict[str, Any]] = {}
    for index in completed_indexes:
        steward_item = latest_integrated_by_index[index]
        record = accepted_records_by_index.get(index, {})
        evidence[index] = {
            "role": steward_item.get("role") or record.get("role"),
            "index": index,
            "status": steward_item.get("status"),
            "accepted": steward_item.get("accepted"),
            "task_output_path": steward_item.get("task_output_path") or record.get("task_output_path"),
            "task_output_sha256": steward_item.get("task_output_sha256") or record.get("task_output_sha256"),
            "steward_receipt_path": steward_item.get("steward_receipt_path"),
            "steward_decision": steward_item.get("steward_decision"),
            "template_id": steward_item.get("template_id") or record.get("template_id"),
            "action_id": steward_item.get("action_id") or record.get("action_id"),
        }

    return {
        "completed_role_indexes": set(completed_indexes),
        "completed_role_evidence": evidence,
        "completed_steward_items": completed_steward_items,
        "completed_records": completed_records,
    }


def build_carrier_turn_packet(
    *,
    carrier: str,
    operator_message: str,
    interpretation: str,
    onboard_result: Mapping[str, Any],
    plan: Mapping[str, Any],
    plan_findings: list[str],
    operator_message_classification: Mapping[str, Any],
    source_operator_queue_item: Mapping[str, Any] | None,
    human_gates: list[Mapping[str, Any]],
    mode: str,
    max_spawn_rows: int | None,
) -> dict[str, Any]:
    spawned_rows = _limited_spawn_rows(plan, max_spawn_rows)
    blocked = bool(onboard_result.get("findings")) or bool(plan_findings) or bool(human_gates)
    if human_gates:
        intake_status = "BLOCKED_BY_HUMAN_GATE"
        intake_required_action = "Resolve open human gates before executing scheduled role phases or optional role workers."
    elif spawned_rows:
        intake_status = "WAITING_FOR_TASK_RETURNS"
        intake_required_action = "Capture every scheduled role-phase return and run kernel.ion_carrier_task_return before Steward integration."
    else:
        intake_status = "NO_TASK_RETURNS_REQUIRED"
        intake_required_action = "No active spawn rows were emitted for this carrier turn; continue or queue new work."
    return {
        "schema_id": "ion.carrier_turn_packet.v1",
        "created_at": _iso_now(),
        "carrier": carrier,
        "mode": mode,
        "operator_message": operator_message,
        "operator_message_interpretation": interpretation,
        "operator_message_classification": dict(operator_message_classification),
        "source_operator_queue_item": dict(source_operator_queue_item) if source_operator_queue_item else None,
        "active_work_packet_path": str(ACTIVE_PACKET_RELATIVE_PATH),
        "active_spawn_plan_path": str(ACTIVE_SPAWN_PLAN_RELATIVE_PATH),
        "active_turn_packet_path": str(ACTIVE_TURN_PACKET_RELATIVE_PATH),
        "task_return_ledger_path": str(ACTIVE_TASK_RETURN_LEDGER_RELATIVE_PATH),
        "steward_integration_queue_path": str(ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH),
        "operator_message_queue_path": str(ACTIVE_OPERATOR_MESSAGE_QUEUE_RELATIVE_PATH),
        "human_gate_queue_path": str(ACTIVE_HUMAN_GATE_QUEUE_RELATIVE_PATH),
        "execution_bundle_root": plan.get("execution_bundle_root"),
        "spawn_policy": plan.get("spawn_policy"),
        "workstream": plan.get("workstream"),
        "objective": plan.get("objective"),
        "spawn_row_limit": max_spawn_rows,
        "completed_role_indexes": list(plan.get("completed_role_indexes", [])),
        "completed_role_count": plan.get("completed_role_count", 0),
        "carrier_next_actions": [
            "Read this ACTIVE_CARRIER_TURN_PACKET.json.",
            "If human_gates is non-empty, stop spawning and request/record the gate answer.",
            "Read ACTIVE_ROLE_SPAWN_PLAN.json.",
            "Execute only role_spawn_plan rows where spawn=true, in ascending index order.",
            "For each row, execute the generated context_package_path through the current authorized carrier mode; in single-carrier sandbox mode, mount the role phase yourself; in Cursor/worker mode, give it to the authorized worker. Do not use session_packet_path alone.",
            "Reject any role/task return that does not begin with ### CONTEXT PROOF and include ### TEMPLATE ACTION PROOF.",
            "Validate each role/task return against its context_load_receipt_path using kernel.ion_context_proof_gate.",
            "Validate each role/task return's template/action section using kernel.ion_template_action_gate.",
            "Record each role/task return with kernel.ion_carrier_task_return before Steward integration.",
            "Forward accepted returns to STEWARD integration; use RELAY only for visible reporting.",
            "Use kernel.ion_status for status requests; do not infer status from chat memory.",
            "Stop and request human decision only when blocked_by_findings=true or an explicit human gate appears in the active packet.",
        ],
        "forbidden_parent_chat_actions": [
            "Do not perform STEWARD/MASON/VIZIER/NEMESIS/etc. work outside a scheduled spawn=true row and its context package; in single-carrier sandbox mode, the parent chat may execute the scheduled row as a bounded role-phase mount.",
            "Do not ask the operator which ION agents to spawn when a valid spawn plan exists.",
            "Do not spawn roles from boot files, MINI.md, CAPSULE.md, or session_packet_path alone.",
            "Do not treat path-list acknowledgment as context loading.",
            "Do not continue from stale ACTIVE_ROLE_SPAWN_PLAN.json when this entrypoint can regenerate it.",
            "Do not ignore ACTIVE_OPERATOR_MESSAGE_QUEUE.json or ACTIVE_HUMAN_GATE_QUEUE.json.",
        ],
        "spawn_queue": [] if human_gates else spawned_rows,
        "human_gates": [dict(gate) for gate in human_gates],
        "return_intake_state": {
            "schema_id": "ion.carrier_return_intake_state.v1",
            "status": intake_status,
            "accepted_count": 0,
            "rejected_count": 0,
            "pending_count": 0 if human_gates else len(spawned_rows),
            "required_action": intake_required_action,
        },
        "blocked_by_findings": blocked,
        "blocked_by_human_gate": bool(human_gates),
        "findings": {
            "onboard": list(onboard_result.get("findings", [])),
            "cycle_plan": list(plan_findings),
            "human_gates": [str(gate.get("id")) for gate in human_gates],
        },
        "production_authority": False,
        "live_execution_authority": False,
    }


def initialize_empty_return_state(
    shell_root: Path,
    plan: Mapping[str, Any],
    *,
    completed_records: list[dict[str, Any]] | None = None,
    completed_steward_items: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Reset V85 Task-return intake state for the freshly generated active plan."""

    now = _iso_now()
    ledger = {
        "schema_id": "ion.carrier_task_return_ledger.v1",
        "created_at": now,
        "updated_at": now,
        "active_spawn_plan_path": str(ACTIVE_SPAWN_PLAN_RELATIVE_PATH),
        "execution_bundle_root": plan.get("execution_bundle_root"),
        "records": [],
        "completed_records": list(completed_records or []),
        "production_authority": False,
        "live_execution_authority": False,
    }
    queue = {
        "schema_id": "ion.steward_integration_queue.v1",
        "created_at": now,
        "updated_at": now,
        "active_spawn_plan_path": str(ACTIVE_SPAWN_PLAN_RELATIVE_PATH),
        "execution_bundle_root": plan.get("execution_bundle_root"),
        "items": [],
        "completed_items": list(completed_steward_items or []),
        "production_authority": False,
        "live_execution_authority": False,
    }
    ledger_path = shell_root / ACTIVE_TASK_RETURN_LEDGER_RELATIVE_PATH
    queue_path = shell_root / ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH
    _write_json(ledger_path, ledger)
    _write_json(queue_path, queue)
    return {
        "ledger": ledger,
        "queue": queue,
        "task_return_ledger_path": str(ACTIVE_TASK_RETURN_LEDGER_RELATIVE_PATH),
        "steward_integration_queue_path": str(ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH),
    }


def continue_carrier(
    root: str | Path | None = None,
    *,
    carrier: str = "cursor",
    operator_message: str | None = "continue",
    operator_message_file: str | Path | None = None,
    objective: str | None = None,
    spawn_policy: str = "required",
    force_new_objective: bool = False,
    consume_operator_queue: bool = False,
    max_spawn_rows: int | None = None,
    mode: str | None = None,
) -> dict[str, Any]:
    """Refresh active carrier state and return the next lawful carrier packet."""

    mode = mode or _default_mode_for_carrier(carrier)
    shell_root = resolve_shell_root_from_ion_root(root)
    active_packet_path = shell_root / ACTIVE_PACKET_RELATIVE_PATH
    previous_packet = _read_json(active_packet_path)
    previous_plan = _read_json(shell_root / ACTIVE_SPAWN_PLAN_RELATIVE_PATH)
    previous_ledger = _read_json(shell_root / ACTIVE_TASK_RETURN_LEDGER_RELATIVE_PATH)
    previous_steward_queue = _read_json(shell_root / ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH)

    file_message = _read_operator_message_file(operator_message_file)
    effective_message = file_message if file_message is not None else (operator_message or "continue")

    # Ensure V88 durable queues exist before classification.
    load_operator_message_queue(shell_root)
    load_human_gate_queue(shell_root)
    open_gates = unresolved_human_gates(shell_root)

    classification = classify_operator_message(effective_message, active_human_gates=open_gates)
    source_queue_item: Mapping[str, Any] | None = None
    gate_resolution: Mapping[str, Any] | None = None

    if classification["classification"] == "human_gate_answer" and open_gates:
        gate_resolution = resolve_human_gate(shell_root, gate_id=None, answer=effective_message)
        open_gates = unresolved_human_gates(shell_root)
        classification = classify_operator_message("continue", active_human_gates=open_gates)
        effective_message = "continue"

    if consume_operator_queue:
        claimed = claim_next_operator_message(shell_root)
        if claimed is not None:
            source_queue_item = claimed
            effective_message = str(claimed.get("message", "")).strip() or effective_message
            classification = classify_operator_message(effective_message, active_human_gates=open_gates)

    classification = _classification_for_forced_objective(
        classification,
        forced=bool(force_new_objective or objective),
    )

    if classification["classification"] == "new_work_directive" and source_queue_item is None:
        enqueue_result = enqueue_operator_message(
            shell_root,
            message=effective_message,
            source="operator_directive_current_turn",
            status="in_progress",
            priority=75,
            classification=classification,
        )
        source_queue_item = enqueue_result["item"]

    is_continuation = (
        _is_continuation_signal(effective_message)
        and not force_new_objective
        and not objective
        and classification["classification"] == "continuation_signal"
    )

    if is_continuation:
        resolved_objective = _objective_from_packet(previous_packet)
        interpretation = "CONTINUATION_SIGNAL_REUSE_ACTIVE_OBJECTIVE"
        force_onboard = previous_packet is None
    else:
        resolved_objective = (objective or effective_message or "").strip() or _objective_from_packet(previous_packet)
        interpretation = "NEW_OR_UPDATED_OBJECTIVE_REFRESH_ACTIVE_PACKET"
        force_onboard = True

    onboard_result = onboard_carrier(
        shell_root,
        carrier=carrier,
        objective=resolved_objective,
        force=force_onboard,
    )
    active_packet = onboard_result.get("packet") if isinstance(onboard_result.get("packet"), Mapping) else previous_packet
    workstream = _workstream_from_packet(active_packet)
    completed_history = (
        _latest_completed_role_history(
            steward_queue=previous_steward_queue,
            ledger=previous_ledger,
            shell_root=shell_root,
            execution_bundle_root=(
                str(previous_plan.get("execution_bundle_root"))
                if isinstance(previous_plan, Mapping) and previous_plan.get("execution_bundle_root")
                else None
            ),
        )
        if is_continuation
        else {
            "completed_role_indexes": set(),
            "completed_role_evidence": {},
            "completed_records": [],
            "completed_steward_items": [],
        }
    )

    execution_root = (
        Path("ION/05_context/current/execution_cycles")
        / f"{_iso_now().replace(':', '').replace('+', 'Z')}_carrier_continue_{_safe_slug(resolved_objective)}"
    )
    plan = build_cycle_plan(
        shell_root,
        workstream=workstream,
        objective=resolved_objective,
        carrier=carrier,
        spawn_policy=spawn_policy,
        spawn_row_limit=max_spawn_rows,
        execution_root=execution_root,
        source_task=f"carrier_continue:{_normalize_operator_message(effective_message)}",
        completed_role_indexes=completed_history["completed_role_indexes"],
        completed_role_evidence=completed_history["completed_role_evidence"],
    )
    plan_valid, plan_findings = validate_cycle_plan(plan)
    plan_path = write_cycle_plan(plan, shell_root)
    return_state = initialize_empty_return_state(
        shell_root,
        plan,
        completed_records=completed_history["completed_records"],
        completed_steward_items=completed_history["completed_steward_items"],
    )

    turn_packet = build_carrier_turn_packet(
        carrier=carrier,
        operator_message=effective_message or "",
        interpretation=interpretation,
        onboard_result=onboard_result,
        plan=plan,
        plan_findings=plan_findings,
        operator_message_classification=classification,
        source_operator_queue_item=source_queue_item,
        human_gates=open_gates,
        mode=mode,
        max_spawn_rows=max_spawn_rows,
    )
    turn_path = shell_root / ACTIVE_TURN_PACKET_RELATIVE_PATH
    _write_json(turn_path, turn_packet)

    if source_queue_item is not None and not open_gates:
        try:
            complete_operator_message(shell_root, item_id=str(source_queue_item.get("id")), status="carrier_packet_generated")
        except Exception:
            # Queue state should never prevent the carrier packet from being written.
            pass

    blocked = turn_packet["blocked_by_findings"]
    ready = onboard_result.get("valid") and plan_valid and not blocked
    verdict = "ION_CARRIER_CONTINUE_READY" if ready else (
        "ION_CARRIER_BLOCKED_BY_HUMAN_GATE" if open_gates else "ION_CARRIER_CONTINUE_BLOCKED"
    )

    return {
        "schema_id": "ion.carrier_continue_result.v1",
        "verdict": verdict,
        "active_work_packet_path": str(ACTIVE_PACKET_RELATIVE_PATH),
        "active_spawn_plan_path": str(ACTIVE_SPAWN_PLAN_RELATIVE_PATH),
        "active_turn_packet_path": str(ACTIVE_TURN_PACKET_RELATIVE_PATH),
        "task_return_ledger_path": str(ACTIVE_TASK_RETURN_LEDGER_RELATIVE_PATH),
        "steward_integration_queue_path": str(ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH),
        "operator_message_queue_path": str(ACTIVE_OPERATOR_MESSAGE_QUEUE_RELATIVE_PATH),
        "human_gate_queue_path": str(ACTIVE_HUMAN_GATE_QUEUE_RELATIVE_PATH),
        "plan_written_to": str(plan_path.relative_to(shell_root)),
        "turn_packet_written_to": str(turn_path.relative_to(shell_root)),
        "active_task_return_ledger_path": return_state["task_return_ledger_path"],
        "active_steward_integration_queue_path": return_state["steward_integration_queue_path"],
        "operator_message_interpretation": interpretation,
        "operator_message_classification": classification,
        "source_operator_queue_item": dict(source_queue_item) if source_queue_item else None,
        "gate_resolution": dict(gate_resolution) if gate_resolution else None,
        "objective": resolved_objective,
        "workstream": workstream,
        "mode": mode,
        "max_spawn_rows": max_spawn_rows,
        "completed_role_indexes": plan.get("completed_role_indexes", []),
        "completed_role_count": plan.get("completed_role_count", 0),
        "spawn_queue": turn_packet["spawn_queue"],
        "human_gates": turn_packet["human_gates"],
        "findings": turn_packet["findings"],
        "blocked_by_findings": turn_packet["blocked_by_findings"],
        "blocked_by_human_gate": turn_packet["blocked_by_human_gate"],
        "production_authority": False,
        "live_execution_authority": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Refresh ION carrier state for a continue/proceed/resume turn.")
    parser.add_argument("--ion-root", default=None, help="Shell root containing ION/, or ION/ itself.")
    parser.add_argument("--carrier", default="cursor")
    parser.add_argument("--operator-message", default="continue")
    parser.add_argument("--operator-message-file", default=None)
    parser.add_argument("--objective", default=None)
    parser.add_argument("--spawn-policy", default="required", choices=("required", "full", "objective"))
    parser.add_argument("--force-new-objective", action="store_true")
    parser.add_argument("--consume-operator-queue", action="store_true")
    parser.add_argument("--max-spawn-rows", type=int, default=None)
    parser.add_argument("--mode", default=None, choices=("plan-only", "manual-cursor", "cursor-sdk", "gpt-sandbox"))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = continue_carrier(
        args.ion_root,
        carrier=args.carrier,
        operator_message=args.operator_message,
        operator_message_file=args.operator_message_file,
        objective=args.objective,
        spawn_policy=args.spawn_policy,
        force_new_objective=args.force_new_objective,
        consume_operator_queue=args.consume_operator_queue,
        max_spawn_rows=args.max_spawn_rows,
        mode=args.mode,
    )
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["verdict"])
        print(f"objective: {result['objective']}")
        print(f"classification: {result['operator_message_classification']['classification']}")
        print(f"active_work_packet_path: {result['active_work_packet_path']}")
        print(f"active_spawn_plan_path: {result['active_spawn_plan_path']}")
        print(f"active_turn_packet_path: {result['active_turn_packet_path']}")
        print(f"operator_message_queue_path: {result['operator_message_queue_path']}")
        print(f"human_gate_queue_path: {result['human_gate_queue_path']}")
        print("spawn_queue:")
        for item in result["spawn_queue"]:
            print(f"- {item['index']}. {item['role']} -> {item['context_package_path']}")
        if result["human_gates"]:
            print("human_gates:")
            for gate in result["human_gates"]:
                print(f"- {gate.get('id')}: {gate.get('prompt')}")
        if result["blocked_by_findings"]:
            print("findings:")
            for lane, findings in result["findings"].items():
                for finding in findings:
                    print(f"- {lane}: {finding}")
    return 0 if result["verdict"] == "ION_CARRIER_CONTINUE_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
