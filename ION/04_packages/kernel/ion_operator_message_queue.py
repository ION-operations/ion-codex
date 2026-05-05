"""Durable operator message queue for ION carrier-control.

V88 introduces this queue so long-duration work is not trapped in Cursor chat
scrollback. The queue records operator directives, continuation requests, and
queued future work as kernel state that the carrier can consume deterministically.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .ion_carrier_onboard import resolve_shell_root_from_ion_root
from .ion_operator_message_classifier import classify_operator_message

ACTIVE_OPERATOR_MESSAGE_QUEUE_RELATIVE_PATH = Path("ION/05_context/current/ACTIVE_OPERATOR_MESSAGE_QUEUE.json")


def _iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _safe_slug(value: str) -> str:
    import re

    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")[:48] or "operator_message"


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
        "schema_id": "ion.operator_message_queue.v1",
        "created_at": now,
        "updated_at": now,
        "items": [],
        "production_authority": False,
        "live_execution_authority": False,
    }


def load_operator_message_queue(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = resolve_shell_root_from_ion_root(root)
    path = shell_root / ACTIVE_OPERATOR_MESSAGE_QUEUE_RELATIVE_PATH
    queue = _read_json(path)
    if queue is None:
        queue = _new_queue()
        _write_json(path, queue)
    return queue


def save_operator_message_queue(root: str | Path | None, queue: Mapping[str, Any]) -> None:
    shell_root = resolve_shell_root_from_ion_root(root)
    value = dict(queue)
    value["updated_at"] = _iso_now()
    _write_json(shell_root / ACTIVE_OPERATOR_MESSAGE_QUEUE_RELATIVE_PATH, value)


def enqueue_operator_message(
    root: str | Path | None = None,
    *,
    message: str,
    source: str = "operator",
    status: str = "pending",
    priority: int = 50,
    classification: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    shell_root = resolve_shell_root_from_ion_root(root)
    queue = load_operator_message_queue(shell_root)
    now = _iso_now()
    classification_record = dict(classification or classify_operator_message(message))
    item_id = f"opmsg_{now.replace(':', '').replace('+', 'Z')}_{_safe_slug(message)}"
    item = {
        "id": item_id,
        "created_at": now,
        "updated_at": now,
        "source": source,
        "status": status,
        "priority": int(priority),
        "message": message,
        "classification": classification_record.get("classification"),
        "classification_record": classification_record,
        "consumed_at": None,
        "completed_at": None,
    }
    queue.setdefault("items", []).append(item)
    save_operator_message_queue(shell_root, queue)
    return {
        "schema_id": "ion.operator_message_queue_result.v1",
        "verdict": "ION_OPERATOR_MESSAGE_ENQUEUED",
        "queue_path": str(ACTIVE_OPERATOR_MESSAGE_QUEUE_RELATIVE_PATH),
        "item": item,
    }


def claim_next_operator_message(
    root: str | Path | None = None,
    *,
    allowed_statuses: tuple[str, ...] = ("pending",),
) -> dict[str, Any] | None:
    shell_root = resolve_shell_root_from_ion_root(root)
    queue = load_operator_message_queue(shell_root)
    pending = [
        item for item in queue.get("items", [])
        if isinstance(item, dict) and item.get("status") in allowed_statuses
    ]
    if not pending:
        return None
    pending.sort(key=lambda item: (-int(item.get("priority", 50)), str(item.get("created_at", ""))))
    chosen = pending[0]
    now = _iso_now()
    chosen["status"] = "in_progress"
    chosen["updated_at"] = now
    chosen["consumed_at"] = now
    save_operator_message_queue(shell_root, queue)
    return chosen


def complete_operator_message(
    root: str | Path | None = None,
    *,
    item_id: str,
    status: str = "completed",
) -> dict[str, Any]:
    shell_root = resolve_shell_root_from_ion_root(root)
    queue = load_operator_message_queue(shell_root)
    now = _iso_now()
    for item in queue.get("items", []):
        if isinstance(item, dict) and item.get("id") == item_id:
            item["status"] = status
            item["updated_at"] = now
            item["completed_at"] = now
            save_operator_message_queue(shell_root, queue)
            return {
                "schema_id": "ion.operator_message_queue_result.v1",
                "verdict": "ION_OPERATOR_MESSAGE_UPDATED",
                "queue_path": str(ACTIVE_OPERATOR_MESSAGE_QUEUE_RELATIVE_PATH),
                "item": item,
            }
    raise ValueError(f"No operator message queue item found for id={item_id!r}")


def queue_counts(queue: Mapping[str, Any]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in queue.get("items", []):
        if isinstance(item, dict):
            status = str(item.get("status", "unknown"))
            counts[status] = counts.get(status, 0) + 1
    return counts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Manage the ION operator message queue.")
    parser.add_argument("--ion-root", default=None)
    parser.add_argument("--add", default=None, help="Add a message to the queue.")
    parser.add_argument("--status", default="pending", help="Status for --add.")
    parser.add_argument("--priority", type=int, default=50)
    parser.add_argument("--claim-next", action="store_true")
    parser.add_argument("--complete", default=None, help="Complete queue item id.")
    parser.add_argument("--complete-status", default="completed")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.add is not None:
        result = enqueue_operator_message(args.ion_root, message=args.add, status=args.status, priority=args.priority)
    elif args.claim_next:
        item = claim_next_operator_message(args.ion_root)
        result = {
            "schema_id": "ion.operator_message_queue_result.v1",
            "verdict": "ION_OPERATOR_MESSAGE_CLAIMED" if item else "ION_OPERATOR_MESSAGE_QUEUE_EMPTY",
            "queue_path": str(ACTIVE_OPERATOR_MESSAGE_QUEUE_RELATIVE_PATH),
            "item": item,
        }
    elif args.complete is not None:
        result = complete_operator_message(args.ion_root, item_id=args.complete, status=args.complete_status)
    else:
        queue = load_operator_message_queue(args.ion_root)
        result = {
            "schema_id": "ion.operator_message_queue_result.v1",
            "verdict": "ION_OPERATOR_MESSAGE_QUEUE_READY",
            "queue_path": str(ACTIVE_OPERATOR_MESSAGE_QUEUE_RELATIVE_PATH),
            "counts": queue_counts(queue),
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
