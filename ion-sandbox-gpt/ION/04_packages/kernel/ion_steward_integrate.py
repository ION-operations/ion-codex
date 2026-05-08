"""ION deterministic Steward integration boundary.

V101 introduced the template/action gate for individual worker outputs. V107
adds a queue-consume path so accepted carrier returns can move from
PENDING_STEWARD_INTEGRATION to explicit integrated/rejected state with receipts.
"""
from __future__ import annotations
import argparse, hashlib, json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from .ion_template_action_gate import evaluate_template_action_proof

QUEUE_REL = Path("ION/05_context/current/ACTIVE_STEWARD_INTEGRATION_QUEUE.json")
TURN_PACKET_REL = Path("ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json")
RECEIPT_ROOT_REL = Path("ION/05_context/current/steward_integrations")

def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def _root(path: str | Path) -> Path:
    p = Path(path).expanduser().resolve()
    return p.parent if p.name == "ION" else p

def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))

def _read_queue(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"schema_id": "ion.steward_integration_queue.v1", "items": []}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data.get("items"), list):
            data["items"] = []
        return data
    except Exception:
        return {"schema_id": "ion.steward_integration_queue.v1", "items": [], "findings": ["previous_queue_unreadable"]}

def _safe_slug(value: str) -> str:
    import re
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")[:80] or "item"

def steward_integrate_return(*, ion_root: str | Path, worker_output: str, source: str = "local_autonomous_loop", cycle_id: str = "manual", step_index: int = 1, write: bool = False) -> dict[str, Any]:
    shell = _root(ion_root)
    created_at = _now()
    gate = evaluate_template_action_proof(worker_output=worker_output)
    accepted = bool(gate["accepted"])
    receipt_id = f"{cycle_id}_step_{step_index:02d}_steward_integration"
    receipt_rel = RECEIPT_ROOT_REL / f"{receipt_id}.json"
    receipt = {
        "schema_id": "ion.steward_integration_receipt.v1",
        "receipt_id": receipt_id,
        "created_at": created_at,
        "source": source,
        "cycle_id": cycle_id,
        "step_index": step_index,
        "accepted": accepted,
        "decision": "INTEGRATED_AS_ACCEPTED_STATE_DELTA" if accepted else "REJECTED_BY_TEMPLATE_ACTION_GATE",
        "gate": gate,
        "worker_output_sha256": hashlib.sha256(worker_output.encode("utf-8")).hexdigest(),
        "worker_output_preview": worker_output[:1600],
        "production_authority": False,
        "external_execution_authority": False,
    }
    queue_path = shell / QUEUE_REL
    queue = _read_queue(queue_path)
    queue["last_updated_at"] = created_at
    queue["last_receipt_path"] = str(receipt_rel)
    queue["items"].append({
        "receipt_id": receipt_id,
        "created_at": created_at,
        "cycle_id": cycle_id,
        "step_index": step_index,
        "accepted": accepted,
        "decision": receipt["decision"],
        "receipt_path": str(receipt_rel),
        "template_id": gate.get("template_id"),
        "action_id": gate.get("action_id"),
        "touched_paths": gate.get("touched_paths", []),
    })
    if write:
        _write_json(shell / receipt_rel, receipt)
        _write_json(queue_path, queue)
    return {"schema_id": "ion.steward_integration_result.v1", "accepted": accepted, "receipt": receipt, "receipt_path": str(receipt_rel), "queue_path": str(QUEUE_REL), "write_performed": write}

def steward_integrate_return_file(*, ion_root: str | Path, worker_output_path: str | Path, source: str = "local_autonomous_loop", cycle_id: str = "manual", step_index: int = 1, write: bool = False) -> dict[str, Any]:
    return steward_integrate_return(ion_root=ion_root, worker_output=Path(worker_output_path).read_text(encoding="utf-8", errors="replace"), source=source, cycle_id=cycle_id, step_index=step_index, write=write)

def _queue_receipt_id(item: Mapping[str, Any], ordinal: int) -> str:
    role = _safe_slug(str(item.get("role", "unknown")))
    index = int(item.get("index", ordinal))
    source = str(item.get("task_output_sha256") or item.get("task_output_path") or item.get("created_at") or ordinal)
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()[:12]
    return f"queue_{index:02d}_{role}_{digest}_steward_integration"

def _update_turn_packet_after_queue_integration(shell: Path, *, accepted_count: int, rejected_count: int, pending_count: int) -> None:
    turn = _read_json(shell / TURN_PACKET_REL)
    if turn is None:
        return
    turn["steward_integration_state"] = {
        "schema_id": "ion.steward_integration_state.v1",
        "status": "STEWARD_INTEGRATION_COMPLETE" if pending_count == 0 and rejected_count == 0 else "STEWARD_INTEGRATION_REVIEW_REQUIRED",
        "accepted_count": accepted_count,
        "rejected_count": rejected_count,
        "pending_count": pending_count,
        "required_action": "Continue or queue new work after Steward integration is complete." if pending_count == 0 and rejected_count == 0 else "Review rejected or pending Steward integration items.",
    }
    intake = turn.get("return_intake_state")
    if isinstance(intake, dict):
        intake["steward_queue_count"] = pending_count
        if pending_count == 0 and rejected_count == 0:
            intake["status"] = "STEWARD_INTEGRATION_COMPLETE"
            intake["required_action"] = "Continue or queue new work; accepted returns have Steward integration receipts."
        turn["return_intake_state"] = intake
    _write_json(shell / TURN_PACKET_REL, turn)

def steward_integrate_pending_queue(*, ion_root: str | Path, write: bool = False) -> dict[str, Any]:
    """Consume pending Steward queue items with template/action receipts."""
    shell = _root(ion_root)
    created_at = _now()
    queue_path = shell / QUEUE_REL
    queue = _read_queue(queue_path)
    items = [item for item in queue.get("items", []) if isinstance(item, Mapping)]

    updated_items: list[dict[str, Any]] = []
    receipts: list[dict[str, Any]] = []
    accepted_count = 0
    rejected_count = 0
    skipped_count = 0

    for ordinal, item in enumerate(items, start=1):
        mutable = dict(item)
        if mutable.get("status") != "PENDING_STEWARD_INTEGRATION":
            updated_items.append(mutable)
            skipped_count += 1
            continue

        task_output_path = mutable.get("task_output_path")
        task_path = shell / task_output_path if isinstance(task_output_path, str) else None
        receipt_id = _queue_receipt_id(mutable, ordinal)
        receipt_rel = RECEIPT_ROOT_REL / f"{receipt_id}.json"

        if not task_path or not task_path.exists():
            gate = {
                "schema_id": "ion.template_action_gate_result.v1",
                "accepted": False,
                "findings": ["missing_task_output_for_steward_integration"],
                "integration_decision": "REJECT_RETURN_AND_RERUN_OR_REPAIR",
                "production_authority": False,
                "live_external_execution_authority": False,
            }
            worker_output = ""
        else:
            worker_output = task_path.read_text(encoding="utf-8", errors="replace")
            gate = evaluate_template_action_proof(worker_output=worker_output)

        accepted = bool(gate.get("accepted"))
        decision = "INTEGRATED_AS_ACCEPTED_STATE_DELTA" if accepted else "REJECTED_BY_TEMPLATE_ACTION_GATE"
        receipt = {
            "schema_id": "ion.steward_queue_integration_receipt.v1",
            "receipt_id": receipt_id,
            "created_at": created_at,
            "source": "active_steward_integration_queue",
            "accepted": accepted,
            "decision": decision,
            "role": mutable.get("role"),
            "index": mutable.get("index"),
            "task_output_path": task_output_path,
            "task_output_sha256": hashlib.sha256(worker_output.encode("utf-8")).hexdigest() if worker_output else None,
            "gate": gate,
            "worker_output_preview": worker_output[:1600],
            "production_authority": False,
            "external_execution_authority": False,
        }
        receipts.append({"receipt": receipt, "receipt_path": str(receipt_rel)})

        mutable["status"] = "STEWARD_INTEGRATED" if accepted else "STEWARD_INTEGRATION_REJECTED"
        mutable["steward_integrated_at"] = created_at
        mutable["steward_receipt_id"] = receipt_id
        mutable["steward_receipt_path"] = str(receipt_rel)
        mutable["steward_decision"] = decision
        mutable["steward_gate_findings"] = list(gate.get("findings", []))
        mutable["accepted"] = accepted
        updated_items.append(mutable)
        if accepted:
            accepted_count += 1
        else:
            rejected_count += 1

    pending_count = sum(1 for item in updated_items if item.get("status") == "PENDING_STEWARD_INTEGRATION")
    queue["items"] = updated_items
    queue["last_updated_at"] = created_at
    queue["last_queue_integration_at"] = created_at
    queue["steward_integration_counts"] = {
        "schema_id": "ion.steward_integration_counts.v1",
        "accepted": accepted_count,
        "rejected": rejected_count,
        "pending": pending_count,
        "skipped_existing": skipped_count,
    }
    if receipts:
        queue["last_receipt_path"] = receipts[-1]["receipt_path"]

    if write:
        for item in receipts:
            _write_json(shell / item["receipt_path"], item["receipt"])
        _write_json(queue_path, queue)
        _update_turn_packet_after_queue_integration(
            shell,
            accepted_count=accepted_count,
            rejected_count=rejected_count,
            pending_count=pending_count,
        )

    result = {
        "schema_id": "ion.steward_queue_integration_result.v1",
        "accepted": pending_count == 0 and rejected_count == 0,
        "processed_count": accepted_count + rejected_count,
        "accepted_count": accepted_count,
        "rejected_count": rejected_count,
        "pending_count": pending_count,
        "skipped_existing_count": skipped_count,
        "receipts": receipts,
        "queue_path": str(QUEUE_REL),
        "write_performed": write,
        "production_authority": False,
        "live_execution_authority": False,
    }
    result["verdict"] = "ION_STEWARD_QUEUE_INTEGRATION_COMPLETE" if result["accepted"] else "ION_STEWARD_QUEUE_INTEGRATION_REVIEW_REQUIRED"
    return result

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Integrate an accepted ION worker return through Steward.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--worker-output", default=None)
    parser.add_argument("--cycle-id", default="manual")
    parser.add_argument("--step-index", type=int, default=1)
    parser.add_argument("--integrate-queue", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if args.integrate_queue:
        result = steward_integrate_pending_queue(ion_root=args.ion_root, write=args.write)
    else:
        if not args.worker_output:
            parser.error("--worker-output is required unless --integrate-queue is used")
        result = steward_integrate_return_file(ion_root=args.ion_root, worker_output_path=args.worker_output, cycle_id=args.cycle_id, step_index=args.step_index, write=args.write)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result.get("verdict") or ("ION_STEWARD_INTEGRATION_ACCEPTED" if result["accepted"] else "ION_STEWARD_INTEGRATION_REJECTED"))
    return 0 if result["accepted"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
