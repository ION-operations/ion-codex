"""ION V106 receipt and repair hydration mapper.

The mapper resolves receipt rows to visible assistant bubbles by explicit
utterance_id and atom_id relationships. It never attaches by recency alone.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CURRENT = Path("ION/05_context/current")
BUBBLES_REL = CURRENT / "ACTIVE_ASSISTANT_BUBBLES.json"
RECEIPT_ROWS_REL = CURRENT / "ACTIVE_RECEIPT_SOURCE_ROWS.json"
OUTPUT = CURRENT / "ACTIVE_RECEIPT_HYDRATION_VIEW_MODEL.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    try:
        if not path.exists():
            return {}
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except Exception as exc:  # pragma: no cover - defensive projection
        return {"_read_error": str(exc), "_path": str(path)}


def listify(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


def compact(value: Any, fallback: str = "") -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    if isinstance(value, (int, float, bool)):
        return str(value)
    return fallback


def _bubble_id(bubble: dict[str, Any], index: int) -> str:
    return compact(bubble.get("bubble_id") or bubble.get("id") or bubble.get("message_id"), f"bubble-{index}")


def _build_indexes(assistant_bubbles: list[dict[str, Any]]) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    utterance_index: dict[str, set[str]] = {}
    atom_index: dict[str, set[str]] = {}
    for index, bubble in enumerate(assistant_bubbles, start=1):
        bubble_id = _bubble_id(bubble, index)
        utterance_id = compact(bubble.get("utterance_id"))
        if utterance_id:
            utterance_index.setdefault(utterance_id, set()).add(bubble_id)
        atom_ids = listify(bubble.get("atom_ids") or bubble.get("atoms") or bubble.get("atom_id"))
        for atom_id in atom_ids:
            atom = compact(atom_id)
            if atom:
                atom_index.setdefault(atom, set()).add(bubble_id)
    return utterance_index, atom_index


def _resolve_bubble(
    receipt: dict[str, Any],
    utterance_index: dict[str, set[str]],
    atom_index: dict[str, set[str]],
) -> tuple[str | None, str, str, str | None]:
    utterance_id = compact(receipt.get("utterance_id"))
    atom_id = compact(receipt.get("atom_id"))
    utterance_matches = utterance_index.get(utterance_id, set()) if utterance_id else set()
    atom_matches = atom_index.get(atom_id, set()) if atom_id else set()

    if utterance_id and atom_id:
        if len(utterance_matches) == 1 and len(atom_matches) == 1 and utterance_matches == atom_matches:
            return next(iter(utterance_matches)), "utterance_atom_agree", "high", None
        if utterance_matches or atom_matches:
            return None, "conflict", "blocked", "HYDRATION_CONFLICT: utterance_id and atom_id resolve to different or ambiguous bubbles"
        return None, "unresolved", "low", "receipt has utterance_id and atom_id but neither resolves to a visible assistant bubble"

    if utterance_id:
        if len(utterance_matches) == 1:
            return next(iter(utterance_matches)), "utterance_id", "high", None
        if len(utterance_matches) > 1:
            return None, "conflict", "blocked", "HYDRATION_CONFLICT: utterance_id resolves to multiple bubbles"
        return None, "unresolved", "low", "receipt utterance_id does not resolve to a visible assistant bubble"

    if atom_id:
        if len(atom_matches) == 1:
            return next(iter(atom_matches)), "atom_id", "high", None
        if len(atom_matches) > 1:
            return None, "conflict", "blocked", "HYDRATION_CONFLICT: atom_id resolves to multiple bubbles"
        return None, "unresolved", "low", "receipt atom_id does not resolve to a visible assistant bubble"

    return None, "unresolved", "low", "receipt has no utterance_id or atom_id; recency attachment is forbidden"


def hydrate_receipts(receipt_rows: list[dict[str, Any]], assistant_bubbles: list[dict[str, Any]]) -> list[dict[str, Any]]:
    utterance_index, atom_index = _build_indexes(assistant_bubbles)
    superseded_by: dict[str, str] = {}
    normalized_rows: list[dict[str, Any]] = []

    for index, row in enumerate(receipt_rows, start=1):
        receipt_id = compact(row.get("receipt_id") or row.get("id"), f"receipt-{index}")
        supersedes = [compact(item) for item in listify(row.get("supersedes")) if compact(item)]
        for target in supersedes:
            superseded_by[target] = receipt_id
        normalized_rows.append({**row, "receipt_id": receipt_id, "supersedes": supersedes})

    records: list[dict[str, Any]] = []
    for row in normalized_rows:
        receipt_id = row["receipt_id"]
        resolved_bubble_id, method, confidence, warning = _resolve_bubble(row, utterance_index, atom_index)
        if row.get("supersedes") and resolved_bubble_id and method not in {"conflict", "unresolved"}:
            method = "supersession"
        blocked = method in {"conflict", "unresolved"}
        records.append(
            {
                "receipt_id": receipt_id,
                "repair_id": row.get("repair_id"),
                "utterance_id": row.get("utterance_id"),
                "atom_id": row.get("atom_id"),
                "resolved_bubble_id": resolved_bubble_id,
                "resolution_method": method,
                "confidence": confidence,
                "claim_class": row.get("claim_class"),
                "authority_verdict": row.get("authority_verdict"),
                "latest_effective": receipt_id not in superseded_by and not blocked,
                "supersedes": row.get("supersedes", []),
                "superseded_by": superseded_by.get(receipt_id),
                "source_receipt_path": row.get("source_receipt_path"),
                "db_row_id": row.get("db_row_id"),
                "warning": warning,
                "timestamp": row.get("timestamp") or row.get("created_at"),
            }
        )
    return records


def _rows_from_payload(payload: dict[str, Any], key: str) -> list[dict[str, Any]]:
    rows = payload.get(key)
    if rows is None and key == "receipt_rows":
        rows = payload.get("receipts") or payload.get("records")
    if rows is None and key == "assistant_bubbles":
        rows = payload.get("bubbles") or payload.get("messages")
    return [row for row in listify(rows) if isinstance(row, dict)]


def build_receipt_hydration_view_model(
    ion_root: str | Path = ".",
    *,
    receipt_rows: list[dict[str, Any]] | None = None,
    assistant_bubbles: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    root = Path(ion_root).resolve()
    receipt_payload = read_json(root / RECEIPT_ROWS_REL)
    bubble_payload = read_json(root / BUBBLES_REL)
    rows = receipt_rows if receipt_rows is not None else _rows_from_payload(receipt_payload, "receipt_rows")
    bubbles = assistant_bubbles if assistant_bubbles is not None else _rows_from_payload(bubble_payload, "assistant_bubbles")
    records = hydrate_receipts(rows, bubbles)
    unresolved = sum(1 for record in records if record["resolution_method"] == "unresolved")
    conflicts = sum(1 for record in records if record["resolution_method"] == "conflict")
    return {
        "schema_id": "ion.receipt_hydration_view_model.v1",
        "generated_at": utc_now(),
        "source_paths": {
            "receipt_rows": RECEIPT_ROWS_REL.as_posix(),
            "assistant_bubbles": BUBBLES_REL.as_posix(),
        },
        "adapter_state": "JSON_FIXTURE_OR_DB_ADAPTER_INPUT",
        "recency_attachment_allowed": False,
        "assistant_bubble_count": len(bubbles),
        "receipt_count": len(records),
        "unresolved_count": unresolved,
        "hydration_conflict_count": conflicts,
        "records": records,
        "production_authority": False,
    }


def write_receipt_hydration_view_model(ion_root: str | Path = ".", output: str | Path | None = None) -> dict[str, Any]:
    root = Path(ion_root).resolve()
    model = build_receipt_hydration_view_model(root)
    out = root / (Path(output) if output else OUTPUT)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(model, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return model


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build ION receipt hydration view model.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    model = write_receipt_hydration_view_model(args.ion_root, args.output) if args.write else build_receipt_hydration_view_model(args.ion_root)
    if args.json:
        print(json.dumps(model, indent=2, sort_keys=True))
    else:
        print(f"ION_RECEIPT_HYDRATION_RECORDS={model['receipt_count']} CONFLICTS={model['hydration_conflict_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
