"""ION V106 lane timeline view-model projection.

Projects requested lane, effective lane, organ events, authority verdicts, and
receipt references from the active runtime packet layer. The projection is
deterministic and intentionally tolerant of partial packet shapes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CURRENT = Path("ION/05_context/current")
OUTPUT = CURRENT / "ACTIVE_LANE_TIMELINE_VIEW_MODEL.json"

ACTIVE_FILES = {
    "operator_queue": CURRENT / "ACTIVE_OPERATOR_MESSAGE_QUEUE.json",
    "turn": CURRENT / "ACTIVE_CARRIER_TURN_PACKET.json",
    "spawn": CURRENT / "ACTIVE_ROLE_SPAWN_PLAN.json",
    "ledger": CURRENT / "ACTIVE_CARRIER_TASK_RETURN_LEDGER.json",
    "steward": CURRENT / "ACTIVE_STEWARD_INTEGRATION_QUEUE.json",
    "human_gates": CURRENT / "ACTIVE_HUMAN_GATE_QUEUE.json",
    "front_door_proof_trace": CURRENT / "ACTIVE_FRONT_DOOR_PROOF_TRACE.json",
    "receipt_hydration": CURRENT / "ACTIVE_RECEIPT_HYDRATION_VIEW_MODEL.json",
}


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


def compact(value: Any, fallback: str = "unknown") -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    if isinstance(value, (int, float, bool)):
        return str(value)
    return fallback


def _stable_event_id(*parts: str) -> str:
    digest = hashlib.sha256("|".join(parts).encode("utf-8")).hexdigest()[:12]
    return f"lane-event-{digest}"


def _timestamp(payload: dict[str, Any], fallback: str) -> str:
    return compact(
        payload.get("timestamp")
        or payload.get("emitted_at")
        or payload.get("created_at")
        or payload.get("updated_at")
        or payload.get("time"),
        fallback,
    )


def _message_id(payload: dict[str, Any], fallback: str = "runtime") -> str:
    return compact(
        payload.get("message_id")
        or payload.get("operator_message_id")
        or payload.get("utterance_id")
        or payload.get("id"),
        fallback,
    )


def _status_from_decision(value: Any, fallback: str = "accepted") -> str:
    decision = compact(value, fallback).lower()
    if "block" in decision or "gate" in decision:
        return "blocked"
    if "reject" in decision or "fail" in decision:
        return "failed"
    if "repair" in decision:
        return "repaired"
    if "hydrat" in decision:
        return "hydrated"
    if "downgrade" in decision:
        return "downgraded"
    if "request" in decision or "queue" in decision or "pending" in decision:
        return "requested"
    return "accepted"


def _event(
    *,
    source: str,
    sequence: int,
    timestamp: str,
    organ: str,
    status: str,
    message_id: str = "runtime",
    utterance_id: str | None = None,
    atom_id: str | None = None,
    requested_lane: str | None = None,
    effective_lane: str | None = None,
    lane_change_reason: str | None = None,
    claim_class: str | None = None,
    authority_verdict: str | None = None,
    receipt_id: str | None = None,
    repair_id: str | None = None,
    source_path: str | None = None,
    latency_ms: int | float | None = None,
) -> dict[str, Any]:
    event_id = _stable_event_id(source, str(sequence), timestamp, organ, message_id, receipt_id or "")
    return {
        "id": event_id,
        "sequence": sequence,
        "message_id": message_id,
        "utterance_id": utterance_id,
        "atom_id": atom_id,
        "timestamp": timestamp,
        "organ": organ,
        "requested_lane": requested_lane,
        "effective_lane": effective_lane,
        "lane_change_reason": lane_change_reason,
        "claim_class": claim_class,
        "authority_verdict": authority_verdict,
        "receipt_id": receipt_id,
        "repair_id": repair_id,
        "source_path": source_path,
        "status": status,
        "latency_ms": latency_ms,
    }


def _operator_events(queue: dict[str, Any], source_path: str, fallback_time: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for index, item in enumerate([i for i in listify(queue.get("items")) if isinstance(i, dict)], start=1):
        requested = item.get("requested_lane") or item.get("lane") or item.get("classification")
        effective = item.get("effective_lane") or item.get("resolved_lane") or requested
        events.append(
            _event(
                source="operator_queue",
                sequence=index,
                timestamp=_timestamp(item, fallback_time),
                organ="operator",
                message_id=_message_id(item, f"operator-{index}"),
                utterance_id=item.get("utterance_id"),
                atom_id=item.get("atom_id"),
                requested_lane=compact(requested, "unchecked"),
                effective_lane=compact(effective, "unchecked"),
                lane_change_reason=item.get("lane_change_reason"),
                claim_class=item.get("claim_class"),
                authority_verdict=item.get("authority_verdict"),
                receipt_id=item.get("receipt_id"),
                source_path=source_path,
                status=_status_from_decision(item.get("status"), "requested"),
                latency_ms=item.get("latency_ms"),
            )
        )
    return events


def _carrier_events(turn: dict[str, Any], source_path: str, fallback_time: str) -> list[dict[str, Any]]:
    if not turn:
        return []
    classification = turn.get("operator_message_classification")
    if not isinstance(classification, dict):
        classification = {}
    requested = turn.get("requested_lane") or classification.get("classification")
    effective = turn.get("effective_lane") or turn.get("lane") or requested
    status = "blocked" if turn.get("blocked_by_findings") else "accepted"
    return [
        _event(
            source="carrier_turn",
            sequence=100,
            timestamp=_timestamp(turn, fallback_time),
            organ="carrier",
            message_id=_message_id(turn, "carrier-turn"),
            requested_lane=compact(requested, "continuation"),
            effective_lane=compact(effective, "continuation"),
            lane_change_reason=turn.get("lane_change_reason") or turn.get("next_lawful_action"),
            authority_verdict=turn.get("authority_verdict") or turn.get("verdict"),
            source_path=source_path,
            status=status,
            latency_ms=turn.get("latency_ms"),
        )
    ]


def _spawn_rows(spawn: dict[str, Any], turn: dict[str, Any]) -> list[dict[str, Any]]:
    rows = [row for row in listify(spawn.get("role_spawn_plan")) if isinstance(row, dict)]
    if rows:
        return rows
    return [row for row in listify(turn.get("spawn_queue")) if isinstance(row, dict)]


def _spawn_events(rows: list[dict[str, Any]], source_path: str, fallback_time: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        role = compact(row.get("role") or row.get("display_name"), "worker")
        events.append(
            _event(
                source="spawn_plan",
                sequence=200 + index,
                timestamp=_timestamp(row, fallback_time),
                organ="worker",
                message_id=_message_id(row, f"spawn-{index}"),
                requested_lane=compact(row.get("requested_lane"), "worker_spawn"),
                effective_lane=compact(row.get("effective_lane") or row.get("authority"), "worker_spawn"),
                lane_change_reason=row.get("lane_change_reason"),
                claim_class=row.get("claim_class"),
                authority_verdict=row.get("authority"),
                receipt_id=row.get("context_load_receipt_path"),
                source_path=row.get("context_package_path") or source_path,
                status="requested" if row.get("spawn") is True or str(row.get("spawn", "")).lower() == "true" else "blocked",
                latency_ms=row.get("latency_ms"),
            )
        )
    return events


def _ledger_events(ledger: dict[str, Any], source_path: str, fallback_time: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for index, record in enumerate([r for r in listify(ledger.get("records")) if isinstance(r, dict)], start=1):
        events.append(
            _event(
                source="task_return_ledger",
                sequence=300 + index,
                timestamp=_timestamp(record, fallback_time),
                organ="worker",
                message_id=_message_id(record, f"return-{index}"),
                requested_lane=compact(record.get("requested_lane"), "task_return"),
                effective_lane=compact(record.get("effective_lane") or record.get("decision"), "task_return"),
                lane_change_reason=record.get("lane_change_reason"),
                claim_class=record.get("claim_class"),
                authority_verdict=record.get("decision") or record.get("status"),
                receipt_id=record.get("receipt_id") or record.get("task_output_path") or record.get("output_path"),
                source_path=record.get("task_output_path") or record.get("output_path") or source_path,
                status=_status_from_decision(record.get("decision") or record.get("status"), "requested"),
                latency_ms=record.get("latency_ms"),
            )
        )
    return events


def _steward_events(steward: dict[str, Any], source_path: str, fallback_time: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for index, item in enumerate([i for i in listify(steward.get("items")) if isinstance(i, dict)], start=1):
        events.append(
            _event(
                source="steward_queue",
                sequence=400 + index,
                timestamp=_timestamp(item, fallback_time),
                organ="steward",
                message_id=_message_id(item, f"steward-{index}"),
                requested_lane=compact(item.get("requested_lane"), "integration"),
                effective_lane=compact(item.get("effective_lane") or item.get("status"), "integration"),
                lane_change_reason=item.get("lane_change_reason"),
                claim_class=item.get("claim_class"),
                authority_verdict=item.get("authority_verdict") or item.get("status"),
                receipt_id=item.get("receipt_id") or item.get("path"),
                source_path=item.get("path") or source_path,
                status=_status_from_decision(item.get("status"), "accepted"),
                latency_ms=item.get("latency_ms"),
            )
        )
    return events


def _gate_events(gates: dict[str, Any], source_path: str, fallback_time: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for index, gate in enumerate([g for g in listify(gates.get("gates")) if isinstance(g, dict)], start=1):
        gate_status = compact(gate.get("status"), "open").lower()
        blocked = gate_status not in {"closed", "resolved", "accepted"}
        events.append(
            _event(
                source="human_gate_queue",
                sequence=500 + index,
                timestamp=_timestamp(gate, fallback_time),
                organ="steward",
                message_id=_message_id(gate, f"gate-{index}"),
                requested_lane=compact(gate.get("requested_lane"), "human_gate"),
                effective_lane="blocked" if blocked else "accepted",
                lane_change_reason=gate.get("reason") or gate.get("lane_change_reason"),
                authority_verdict=gate.get("authority_verdict") or gate_status,
                receipt_id=gate.get("receipt_id"),
                source_path=source_path,
                status="blocked" if blocked else "accepted",
                latency_ms=gate.get("latency_ms"),
            )
        )
    return events


def _hydration_events(hydration: dict[str, Any], source_path: str, fallback_time: str) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for index, record in enumerate([r for r in listify(hydration.get("records")) if isinstance(r, dict)], start=1):
        events.append(
            _event(
                source="receipt_hydration",
                sequence=600 + index,
                timestamp=_timestamp(record, fallback_time),
                organ="ui",
                message_id=compact(record.get("resolved_bubble_id") or record.get("utterance_id"), f"receipt-{index}"),
                utterance_id=record.get("utterance_id"),
                atom_id=record.get("atom_id"),
                requested_lane=compact(record.get("requested_lane"), "receipt_hydration"),
                effective_lane=compact(record.get("resolution_method"), "unresolved"),
                lane_change_reason=record.get("warning"),
                claim_class=record.get("claim_class"),
                authority_verdict=record.get("authority_verdict"),
                receipt_id=record.get("receipt_id"),
                repair_id=record.get("repair_id"),
                source_path=record.get("source_receipt_path") or source_path,
                status="hydrated" if record.get("resolved_bubble_id") else "failed",
                latency_ms=record.get("latency_ms"),
            )
        )
    return events


def _front_door_events(trace: dict[str, Any], source_path: str, fallback_time: str) -> list[dict[str, Any]]:
    if not trace:
        return []
    boundary = trace.get("boundary_proof") if isinstance(trace.get("boundary_proof"), dict) else {}
    verdict = trace.get("steward_verdict") if isinstance(trace.get("steward_verdict"), dict) else {}
    message_id = compact(boundary.get("persona_ingress_id") or trace.get("trace_id"), "front-door")
    events: list[dict[str, Any]] = []
    for index, stage in enumerate([s for s in listify(trace.get("stage_sequence")) if isinstance(s, dict)], start=1):
        events.append(
            _event(
                source="front_door_proof_trace",
                sequence=700 + int(stage.get("sequence", index)),
                timestamp=compact(trace.get("generated_at"), fallback_time),
                organ=compact(stage.get("organ"), "kernel"),
                message_id=message_id,
                requested_lane="front_door_runtime",
                effective_lane=compact(stage.get("stage"), "front_door_runtime"),
                lane_change_reason=stage.get("detail"),
                claim_class=verdict.get("claim_class"),
                authority_verdict=stage.get("status") or verdict.get("verdict"),
                receipt_id=stage.get("receipt_id"),
                source_path=stage.get("witness_path") or source_path,
                status=_status_from_decision(stage.get("status"), "accepted"),
            )
        )
    return events


def _group_messages(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for event in events:
        groups.setdefault(compact(event.get("message_id"), "runtime"), []).append(event)
    messages = []
    for message_id in sorted(groups):
        grouped = groups[message_id]
        statuses = {compact(event.get("status")) for event in grouped}
        if "blocked" in statuses or "failed" in statuses:
            state = "unresolved"
        elif "repaired" in statuses:
            state = "repaired"
        elif "downgraded" in statuses:
            state = "downgraded"
        else:
            state = "clean"
        messages.append(
            {
                "message_id": message_id,
                "event_count": len(grouped),
                "current_state": state,
                "requested_lanes": sorted({compact(event.get("requested_lane")) for event in grouped}),
                "effective_lanes": sorted({compact(event.get("effective_lane")) for event in grouped}),
                "events": grouped,
            }
        )
    return messages


def build_lane_timeline_view_model(ion_root: str | Path = ".") -> dict[str, Any]:
    root = Path(ion_root).resolve()
    generated_at = utc_now()
    data = {name: read_json(root / rel) for name, rel in ACTIVE_FILES.items()}
    events: list[dict[str, Any]] = []
    events.extend(_operator_events(data["operator_queue"], ACTIVE_FILES["operator_queue"].as_posix(), generated_at))
    events.extend(_carrier_events(data["turn"], ACTIVE_FILES["turn"].as_posix(), generated_at))
    events.extend(_spawn_events(_spawn_rows(data["spawn"], data["turn"]), ACTIVE_FILES["spawn"].as_posix(), generated_at))
    events.extend(_ledger_events(data["ledger"], ACTIVE_FILES["ledger"].as_posix(), generated_at))
    events.extend(_steward_events(data["steward"], ACTIVE_FILES["steward"].as_posix(), generated_at))
    events.extend(_gate_events(data["human_gates"], ACTIVE_FILES["human_gates"].as_posix(), generated_at))
    events.extend(_front_door_events(data["front_door_proof_trace"], ACTIVE_FILES["front_door_proof_trace"].as_posix(), generated_at))
    events.extend(_hydration_events(data["receipt_hydration"], ACTIVE_FILES["receipt_hydration"].as_posix(), generated_at))
    events.sort(key=lambda event: (compact(event.get("timestamp")), int(event.get("sequence", 0)), compact(event.get("id"))))
    return {
        "schema_id": "ion.lane_timeline_view_model.v1",
        "generated_at": generated_at,
        "source_paths": {name: rel.as_posix() for name, rel in ACTIVE_FILES.items()},
        "event_count": len(events),
        "events": events,
        "messages": _group_messages(events),
        "projection_mode": "ACTIVE_PACKET_PROJECTION",
        "production_authority": False,
    }


def write_lane_timeline_view_model(ion_root: str | Path = ".", output: str | Path | None = None) -> dict[str, Any]:
    root = Path(ion_root).resolve()
    model = build_lane_timeline_view_model(root)
    out = root / (Path(output) if output else OUTPUT)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(model, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return model


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build ION lane timeline view model.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    model = write_lane_timeline_view_model(args.ion_root, args.output) if args.write else build_lane_timeline_view_model(args.ion_root)
    if args.json:
        print(json.dumps(model, indent=2, sort_keys=True))
    else:
        print(f"ION_LANE_TIMELINE_EVENTS={model['event_count']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
