"""Record and proof-gate scheduled role/task returns for the ION carrier loop.

V84 gave the parent carrier chat a lawful role-phase queue. V85 closes the other half
of the loop: every scheduled role/task return must be captured, checked against the
role's generated context-load receipt, recorded in an active return ledger, and
forwarded to Steward only after the context proof passes.

This module does not perform live external automation. It gives the carrier a
deterministic file-backed intake transaction for returns produced by single-carrier
role-phase mounts or by optional authorized worker slots.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .ion_carrier_continue import ACTIVE_TURN_PACKET_RELATIVE_PATH
from .ion_carrier_onboard import resolve_shell_root_from_ion_root
from .ion_context_proof_gate import evaluate_context_proof_return_files
from .ion_cycle_runner import ACTIVE_SPAWN_PLAN_RELATIVE_PATH
from .ion_template_action_gate import evaluate_template_action_proof_file

ACTIVE_TASK_RETURN_LEDGER_RELATIVE_PATH = Path("ION/05_context/current/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json")
ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH = Path("ION/05_context/current/ACTIVE_STEWARD_INTEGRATION_QUEUE.json")
TASK_RETURN_CAPTURES_RELATIVE_DIR = Path("ION/05_context/current/task_returns")


def _iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _safe_slug(value: str) -> str:
    import re

    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")[:80] or "task_return"


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def _load_plan(shell_root: Path) -> dict[str, Any]:
    plan_path = shell_root / ACTIVE_SPAWN_PLAN_RELATIVE_PATH
    plan = _read_json(plan_path)
    if plan is None:
        raise FileNotFoundError(f"Missing active spawn plan: {ACTIVE_SPAWN_PLAN_RELATIVE_PATH}")
    return plan


def _spawn_rows(plan: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    rows = plan.get("role_spawn_plan", [])
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, Mapping) and row.get("spawn") is True]


def _select_spawn_row(plan: Mapping[str, Any], *, role: str | None, index: int | None) -> Mapping[str, Any]:
    rows = _spawn_rows(plan)
    matches: list[Mapping[str, Any]] = []
    for row in rows:
        role_matches = role is None or str(row.get("role", "")).lower() == role.lower()
        index_matches = index is None or int(row.get("index", -1)) == index
        if role_matches and index_matches:
            matches.append(row)
    if not matches:
        label = f"role={role!r} index={index!r}"
        raise ValueError(f"No spawned role row matched {label}")
    if len(matches) > 1:
        label = f"role={role!r} index={index!r}"
        raise ValueError(f"Ambiguous spawned role row for {label}; provide both --role and --index")
    return matches[0]


def _read_or_capture_task_output(
    shell_root: Path,
    *,
    row: Mapping[str, Any],
    task_output_path: str | Path | None,
    task_output_text: str | None,
) -> tuple[str, Path, str]:
    if task_output_path:
        source = Path(task_output_path)
        if not source.is_absolute():
            source = shell_root / source
        text = source.read_text(encoding="utf-8", errors="replace")
        return text, source, _safe_relative(source, shell_root)

    if task_output_text is None:
        raise ValueError("Either task_output_path or task_output_text is required")

    capture_dir = shell_root / TASK_RETURN_CAPTURES_RELATIVE_DIR
    capture_dir.mkdir(parents=True, exist_ok=True)
    role = _safe_slug(str(row.get("role", "unknown")))
    index = int(row.get("index", 0))
    capture = capture_dir / f"{_iso_now().replace(':', '').replace('+', 'Z')}_{index:02d}_{role}_task_return.md"
    capture.write_text(task_output_text, encoding="utf-8")
    return task_output_text, capture, _safe_relative(capture, shell_root)


def _new_ledger(plan: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_id": "ion.carrier_task_return_ledger.v1",
        "created_at": _iso_now(),
        "updated_at": _iso_now(),
        "active_spawn_plan_path": str(ACTIVE_SPAWN_PLAN_RELATIVE_PATH),
        "execution_bundle_root": plan.get("execution_bundle_root"),
        "records": [],
        "production_authority": False,
        "live_execution_authority": False,
    }


def _new_steward_queue(plan: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schema_id": "ion.steward_integration_queue.v1",
        "created_at": _iso_now(),
        "updated_at": _iso_now(),
        "active_spawn_plan_path": str(ACTIVE_SPAWN_PLAN_RELATIVE_PATH),
        "execution_bundle_root": plan.get("execution_bundle_root"),
        "items": [],
        "production_authority": False,
        "live_execution_authority": False,
    }


def initialize_task_return_state(root: str | Path | None = None) -> dict[str, Any]:
    """Create empty V85 return ledger and Steward queue for the active spawn plan."""

    shell_root = resolve_shell_root_from_ion_root(root)
    plan = _load_plan(shell_root)

    ledger = _new_ledger(plan)
    queue = _new_steward_queue(plan)

    _write_json(shell_root / ACTIVE_TASK_RETURN_LEDGER_RELATIVE_PATH, ledger)
    _write_json(shell_root / ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH, queue)

    turn_path = shell_root / ACTIVE_TURN_PACKET_RELATIVE_PATH
    turn = _read_json(turn_path)
    if turn is not None:
        turn["task_return_ledger_path"] = str(ACTIVE_TASK_RETURN_LEDGER_RELATIVE_PATH)
        turn["steward_integration_queue_path"] = str(ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH)
        turn["return_intake_state"] = {
            "schema_id": "ion.carrier_return_intake_state.v1",
            "status": "WAITING_FOR_TASK_RETURNS",
            "accepted_count": 0,
            "rejected_count": 0,
            "pending_count": len(turn.get("spawn_queue", [])) if isinstance(turn.get("spawn_queue"), list) else 0,
            "required_action": "Record each scheduled role/task output with kernel.ion_carrier_task_return before Steward integration.",
        }
        existing_actions = list(turn.get("carrier_next_actions", []))
        intake_action = "For each role/task return, save/capture the full output and run kernel.ion_carrier_task_return against the row's receipt before integration."
        if intake_action not in existing_actions:
            existing_actions.insert(6, intake_action)
        turn["carrier_next_actions"] = existing_actions
        _write_json(turn_path, turn)

    return {
        "schema_id": "ion.carrier_task_return_state_init.v1",
        "verdict": "ION_TASK_RETURN_STATE_READY",
        "active_task_return_ledger_path": str(ACTIVE_TASK_RETURN_LEDGER_RELATIVE_PATH),
        "active_steward_integration_queue_path": str(ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH),
        "execution_bundle_root": plan.get("execution_bundle_root"),
        "production_authority": False,
        "live_execution_authority": False,
    }


def record_task_return(
    root: str | Path | None = None,
    *,
    role: str | None = None,
    index: int | None = None,
    task_output_path: str | Path | None = None,
    task_output_text: str | None = None,
) -> dict[str, Any]:
    """Evaluate and record one scheduled role/task return for a spawned role row."""

    shell_root = resolve_shell_root_from_ion_root(root)
    plan = _load_plan(shell_root)
    row = _select_spawn_row(plan, role=role, index=index)

    receipt_rel = row.get("context_load_receipt_path")
    if not isinstance(receipt_rel, str) or not receipt_rel:
        raise ValueError(f"Spawn row lacks context_load_receipt_path: {row.get('role')}#{row.get('index')}")

    receipt_path = shell_root / receipt_rel
    if not receipt_path.exists():
        raise FileNotFoundError(f"Missing context-load receipt: {receipt_rel}")

    task_text, captured_path, captured_rel = _read_or_capture_task_output(
        shell_root,
        row=row,
        task_output_path=task_output_path,
        task_output_text=task_output_text,
    )

    context_evaluation = evaluate_context_proof_return_files(
        receipt_path=receipt_path,
        task_output_path=captured_path,
    )
    template_action_evaluation = evaluate_template_action_proof_file(captured_path)
    findings = [
        *(f"context_proof:{finding}" for finding in context_evaluation.get("findings", [])),
        *(f"template_action:{finding}" for finding in template_action_evaluation.get("findings", [])),
    ]
    accepted = bool(context_evaluation.get("accepted")) and bool(template_action_evaluation.get("accepted"))
    evaluation = {
        "schema_id": "ion.carrier_task_return_combined_evaluation.v1",
        "accepted": accepted,
        "findings": findings,
        "context_proof": context_evaluation,
        "template_action": template_action_evaluation,
        "integration_decision": "ALLOW_STEWARD_REVIEW" if accepted else "REJECT_RETURN_AND_RERUN_TASK",
        "production_authority": False,
        "live_execution_authority": False,
    }

    record = {
        "schema_id": "ion.carrier_task_return_record.v1",
        "created_at": _iso_now(),
        "role": row.get("role"),
        "index": row.get("index"),
        "carrier_slot": row.get("carrier_slot"),
        "context_package_path": row.get("context_package_path"),
        "context_load_receipt_path": receipt_rel,
        "task_output_path": captured_rel,
        "task_output_sha256": _sha256_text(task_text) if not task_output_path else _sha256_file(captured_path),
        "accepted": accepted,
        "findings": findings,
        "integration_decision": evaluation.get("integration_decision"),
        "required_paths_count": len(context_evaluation.get("required_paths", [])),
        "missing_paths_count": len(context_evaluation.get("missing_paths", [])),
        "template_id": template_action_evaluation.get("template_id"),
        "action_id": template_action_evaluation.get("action_id"),
        "touched_paths": list(template_action_evaluation.get("touched_paths", [])),
        "production_authority": False,
        "live_execution_authority": False,
    }

    ledger_path = shell_root / ACTIVE_TASK_RETURN_LEDGER_RELATIVE_PATH
    ledger = _read_json(ledger_path) or _new_ledger(plan)
    records = [item for item in ledger.get("records", []) if isinstance(item, Mapping)]
    records.append(record)
    ledger["records"] = records
    ledger["updated_at"] = _iso_now()
    ledger["execution_bundle_root"] = plan.get("execution_bundle_root")
    _write_json(ledger_path, ledger)

    queue_path = shell_root / ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH
    queue = _read_json(queue_path) or _new_steward_queue(plan)
    items = [item for item in queue.get("items", []) if isinstance(item, Mapping)]
    if accepted:
        items.append({
            "schema_id": "ion.steward_integration_queue_item.v1",
            "created_at": record["created_at"],
            "status": "PENDING_STEWARD_INTEGRATION",
            "role": row.get("role"),
            "index": row.get("index"),
            "task_output_path": captured_rel,
            "task_output_sha256": record["task_output_sha256"],
            "context_package_path": row.get("context_package_path"),
            "context_load_receipt_path": receipt_rel,
            "template_id": record.get("template_id"),
            "action_id": record.get("action_id"),
            "touched_paths": record.get("touched_paths", []),
            "integration_instruction": "STEWARD may review and integrate this return because the context-proof and template-action gates accepted it.",
        })
    queue["items"] = items
    queue["updated_at"] = _iso_now()
    queue["execution_bundle_root"] = plan.get("execution_bundle_root")
    _write_json(queue_path, queue)

    _update_turn_intake_state(shell_root=shell_root, plan=plan, ledger=ledger, queue=queue)

    return {
        "schema_id": "ion.carrier_task_return_result.v1",
        "verdict": "ION_TASK_RETURN_ACCEPTED_FOR_STEWARD" if accepted else "ION_TASK_RETURN_REJECTED_RERUN_REQUIRED",
        "accepted": accepted,
        "record": record,
        "evaluation": evaluation,
        "active_task_return_ledger_path": str(ACTIVE_TASK_RETURN_LEDGER_RELATIVE_PATH),
        "active_steward_integration_queue_path": str(ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH),
        "production_authority": False,
        "live_execution_authority": False,
    }


def _update_turn_intake_state(
    *,
    shell_root: Path,
    plan: Mapping[str, Any],
    ledger: Mapping[str, Any],
    queue: Mapping[str, Any],
) -> None:
    turn_path = shell_root / ACTIVE_TURN_PACKET_RELATIVE_PATH
    turn = _read_json(turn_path)
    if turn is None:
        return

    spawn_keys = {(str(row.get("role")), int(row.get("index", 0))) for row in _spawn_rows(plan)}
    latest_by_key: dict[tuple[str, int], Mapping[str, Any]] = {}
    for record in ledger.get("records", []):
        if not isinstance(record, Mapping):
            continue
        key = (str(record.get("role")), int(record.get("index", 0)))
        latest_by_key[key] = record

    accepted = sum(1 for key in spawn_keys if latest_by_key.get(key, {}).get("accepted") is True)
    rejected = sum(1 for key in spawn_keys if key in latest_by_key and latest_by_key[key].get("accepted") is not True)
    pending = max(0, len(spawn_keys) - accepted - rejected)

    queue_items = queue.get("items", [])
    queue_count = len(queue_items) if isinstance(queue_items, list) else 0

    turn["task_return_ledger_path"] = str(ACTIVE_TASK_RETURN_LEDGER_RELATIVE_PATH)
    turn["steward_integration_queue_path"] = str(ACTIVE_STEWARD_INTEGRATION_QUEUE_RELATIVE_PATH)
    turn["return_intake_state"] = {
        "schema_id": "ion.carrier_return_intake_state.v1",
        "status": "ALL_ACCEPTED_READY_FOR_STEWARD" if pending == 0 and rejected == 0 and accepted == len(spawn_keys) else "WAITING_OR_REJECTED_TASK_RETURNS",
        "accepted_count": accepted,
        "rejected_count": rejected,
        "pending_count": pending,
        "steward_queue_count": queue_count,
        "required_action": "Integrate accepted queue items with STEWARD; rerun rejected roles; do not ask the operator to choose agents.",
    }
    _write_json(turn_path, turn)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Record and proof-gate one scheduled ION role/task return.")
    parser.add_argument("--ion-root", default=None)
    parser.add_argument("--role", default=None)
    parser.add_argument("--index", type=int, default=None)
    parser.add_argument("--task-output", default=None, help="Path to captured Task output markdown/text.")
    parser.add_argument("--task-output-text", default=None, help="Literal Task output text; captured to ION/05_context/current/task_returns/.")
    parser.add_argument("--init", action="store_true", help="Initialize the active return ledger and Steward integration queue only.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.init:
        result = initialize_task_return_state(args.ion_root)
    else:
        result = record_task_return(
            args.ion_root,
            role=args.role,
            index=args.index,
            task_output_path=args.task_output,
            task_output_text=args.task_output_text,
        )

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["verdict"])
        if "record" in result:
            for finding in result["record"].get("findings", []):
                print(f"- {finding}")

    return 0 if result.get("accepted", True) or args.init else 1


if __name__ == "__main__":
    raise SystemExit(main())
