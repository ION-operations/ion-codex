"""Durable human gate queue for ION carrier-control.

Human gates are first-class runtime objects. The carrier must stop at open
blocking gates and resume only after an explicit operator answer is recorded.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .ion_carrier_onboard import resolve_shell_root_from_ion_root

ACTIVE_HUMAN_GATE_QUEUE_RELATIVE_PATH = Path("ION/05_context/current/ACTIVE_HUMAN_GATE_QUEUE.json")


def _iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _safe_slug(value: str) -> str:
    import re

    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")[:48] or "human_gate"


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _new_queue() -> dict[str, Any]:
    now = _iso_now()
    return {
        "schema_id": "ion.human_gate_queue.v1",
        "created_at": now,
        "updated_at": now,
        "gates": [],
        "production_authority": False,
        "live_execution_authority": False,
    }


def load_human_gate_queue(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = resolve_shell_root_from_ion_root(root)
    path = shell_root / ACTIVE_HUMAN_GATE_QUEUE_RELATIVE_PATH
    queue = _read_json(path)
    if queue is None:
        queue = _new_queue()
        _write_json(path, queue)
    return queue


def save_human_gate_queue(root: str | Path | None, queue: Mapping[str, Any]) -> None:
    shell_root = resolve_shell_root_from_ion_root(root)
    value = dict(queue)
    value["updated_at"] = _iso_now()
    _write_json(shell_root / ACTIVE_HUMAN_GATE_QUEUE_RELATIVE_PATH, value)


def add_human_gate(
    root: str | Path | None = None,
    *,
    prompt: str,
    gate_type: str = "operator_decision",
    blocking: bool = True,
    source: str = "carrier",
    metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    shell_root = resolve_shell_root_from_ion_root(root)
    queue = load_human_gate_queue(shell_root)
    now = _iso_now()
    gate = {
        "id": f"hgate_{now.replace(':', '').replace('+', 'Z')}_{_safe_slug(prompt)}",
        "created_at": now,
        "updated_at": now,
        "status": "open",
        "gate_type": gate_type,
        "blocking": bool(blocking),
        "source": source,
        "prompt": prompt,
        "answer": None,
        "resolved_at": None,
        "metadata": dict(metadata or {}),
    }
    queue.setdefault("gates", []).append(gate)
    save_human_gate_queue(shell_root, queue)
    return {
        "schema_id": "ion.human_gate_queue_result.v1",
        "verdict": "ION_HUMAN_GATE_ADDED",
        "queue_path": str(ACTIVE_HUMAN_GATE_QUEUE_RELATIVE_PATH),
        "gate": gate,
    }


def unresolved_human_gates(root: str | Path | None = None, *, blocking_only: bool = True) -> list[dict[str, Any]]:
    queue = load_human_gate_queue(root)
    gates: list[dict[str, Any]] = []
    for gate in queue.get("gates", []):
        if not isinstance(gate, dict):
            continue
        if gate.get("status") != "open":
            continue
        if blocking_only and gate.get("blocking") is not True:
            continue
        gates.append(gate)
    return gates


def resolve_human_gate(
    root: str | Path | None = None,
    *,
    gate_id: str | None = None,
    answer: str,
) -> dict[str, Any]:
    shell_root = resolve_shell_root_from_ion_root(root)
    queue = load_human_gate_queue(shell_root)
    candidates = [
        gate for gate in queue.get("gates", [])
        if isinstance(gate, dict)
        and gate.get("status") == "open"
        and (gate_id is None or gate.get("id") == gate_id)
    ]
    if not candidates:
        raise ValueError(f"No open human gate found for id={gate_id!r}")
    gate = candidates[0]
    now = _iso_now()
    gate["status"] = "resolved"
    gate["answer"] = answer
    gate["resolved_at"] = now
    gate["updated_at"] = now
    save_human_gate_queue(shell_root, queue)
    return {
        "schema_id": "ion.human_gate_queue_result.v1",
        "verdict": "ION_HUMAN_GATE_RESOLVED",
        "queue_path": str(ACTIVE_HUMAN_GATE_QUEUE_RELATIVE_PATH),
        "gate": gate,
    }


def gate_counts(queue: Mapping[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for gate in queue.get("gates", []):
        if isinstance(gate, dict):
            status = str(gate.get("status", "unknown"))
            counts[status] = counts.get(status, 0) + 1
    return counts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Manage the ION human gate queue.")
    parser.add_argument("--ion-root", default=None)
    parser.add_argument("--add", default=None, help="Add an open human gate with this prompt.")
    parser.add_argument("--type", default="operator_decision")
    parser.add_argument("--nonblocking", action="store_true")
    parser.add_argument("--resolve", default=None, help="Resolve this gate id, or FIRST_OPEN.")
    parser.add_argument("--answer", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.add:
        result = add_human_gate(args.ion_root, prompt=args.add, gate_type=args.type, blocking=not args.nonblocking)
    elif args.resolve:
        gate_id = None if args.resolve == "FIRST_OPEN" else args.resolve
        result = resolve_human_gate(args.ion_root, gate_id=gate_id, answer=args.answer or "")
    else:
        queue = load_human_gate_queue(args.ion_root)
        result = {
            "schema_id": "ion.human_gate_queue_result.v1",
            "verdict": "ION_HUMAN_GATE_QUEUE_READY",
            "queue_path": str(ACTIVE_HUMAN_GATE_QUEUE_RELATIVE_PATH),
            "counts": gate_counts(queue),
            "open_blocking_gates": unresolved_human_gates(args.ion_root),
            "queue": queue,
        }

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["verdict"])
        if result.get("counts"):
            print(result["counts"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
