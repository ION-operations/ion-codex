"""V42 conversational receipts and live repair.

This module records provisional utterances, live correction, retraction, and final
ratification for low-latency Persona workflows. It does not grant production
authority and it never treats provisional speech as ratified truth.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Iterable, Any

SCHEMA_ID = "ion.conversational_receipt.v1"
VERSION = "V42_CONVERSATIONAL_RECEIPTS_AND_LIVE_REPAIR"
DEFAULT_REPORT_DIR = "ION/05_context/history/conversational_receipts"

EVENT_TYPES = (
    "BACKCHANNEL",
    "PROVISIONAL_UTTERANCE",
    "SELF_INTERRUPTION",
    "CORRECTION",
    "RETRACTION",
    "RATIFICATION",
    "BLOCK",
)
CONVERSATION_STATUSES = ("OPEN_PROVISIONAL", "REPAIRED", "RATIFIED", "BLOCKED")
FORBIDDEN_CLAIMS: dict[str, bool] = {
    "provisional_speech_is_ratified_truth": False,
    "unrestricted_live_persona_speech": False,
    "hidden_memory_claim": False,
    "persona_total_ion_identity": False,
    "production_authority": False,
}

@dataclass(frozen=True)
class ConversationalEvent:
    event_type: str
    text: str
    claim_class: str = "C3"
    timestamp: str = ""
    provisional: bool = True
    repair_of: str | None = None
    council_receipt_id: str | None = None

@dataclass(frozen=True)
class ConversationalReceipt:
    schema_id: str
    version: str
    receipt_id: str
    emitted_at: str
    conversation_status: str
    repair_required: bool
    provisional_events_open: int
    final_claim: str | None
    events: tuple[ConversationalEvent, ...]
    repair_obligations: tuple[str, ...]
    production_authority: bool = False
    forbidden_claims: dict[str, bool] = field(default_factory=lambda: dict(FORBIDDEN_CLAIMS))


def make_event(event_type: str, text: str, *, claim_class: str = "C3", timestamp: str | None = None,
               provisional: bool = True, repair_of: str | None = None,
               council_receipt_id: str | None = None) -> ConversationalEvent:
    if event_type not in EVENT_TYPES:
        raise ValueError(f"invalid event_type: {event_type}")
    return ConversationalEvent(
        event_type=event_type,
        text=text,
        claim_class=claim_class,
        timestamp=timestamp or _utc_now(),
        provisional=provisional,
        repair_of=repair_of,
        council_receipt_id=council_receipt_id,
    )


def build_conversational_receipt(*, events: Iterable[ConversationalEvent], emitted_at: str | None = None,
                                 final_claim: str | None = None) -> ConversationalReceipt:
    event_tuple = tuple(events)
    timestamp = emitted_at or _utc_now()
    status, repair_required, open_count, obligations = _classify(event_tuple, final_claim)
    receipt_id = _stable_id("conv", VERSION, timestamp, status, str(len(event_tuple)), final_claim or "")
    return ConversationalReceipt(
        schema_id=SCHEMA_ID,
        version=VERSION,
        receipt_id=receipt_id,
        emitted_at=timestamp,
        conversation_status=status,
        repair_required=repair_required,
        provisional_events_open=open_count,
        final_claim=final_claim,
        events=event_tuple,
        repair_obligations=obligations,
        production_authority=False,
        forbidden_claims=dict(FORBIDDEN_CLAIMS),
    )


def validate_conversational_receipt(receipt: ConversationalReceipt) -> tuple[str, ...]:
    errors: list[str] = []
    if receipt.schema_id != SCHEMA_ID:
        errors.append("schema_id mismatch")
    if receipt.version != VERSION:
        errors.append("version mismatch")
    if receipt.production_authority is not False:
        errors.append("conversational receipt must not grant production authority")
    if receipt.conversation_status not in CONVERSATION_STATUSES:
        errors.append(f"invalid conversation_status: {receipt.conversation_status}")
    for key, allowed in receipt.forbidden_claims.items():
        if allowed is not False:
            errors.append(f"forbidden claim {key!r} must be false")
    for event in receipt.events:
        if event.event_type not in EVENT_TYPES:
            errors.append(f"invalid event_type: {event.event_type}")
        if event.event_type == "BLOCK" and receipt.conversation_status != "BLOCKED":
            errors.append("BLOCK event requires BLOCKED status")
    if receipt.conversation_status == "OPEN_PROVISIONAL" and receipt.provisional_events_open < 1:
        errors.append("open provisional status requires open provisional events")
    if receipt.conversation_status == "RATIFIED" and not receipt.final_claim:
        errors.append("ratified receipt requires final_claim")
    if receipt.conversation_status == "BLOCKED" and not receipt.repair_required:
        errors.append("blocked receipt must require repair")
    return tuple(errors)


def write_conversational_receipt(workspace_root: str | Path, receipt: ConversationalReceipt, *, report_dir: str = DEFAULT_REPORT_DIR) -> Path:
    root = Path(workspace_root).resolve()
    out = root / report_dir
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{receipt.receipt_id}.conversational_receipt.json"
    path.write_text(json.dumps(_to_jsonable(receipt), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def format_conversational_summary(receipt: ConversationalReceipt) -> str:
    return "\n".join([
        f"version: {receipt.version}",
        f"receipt_id: {receipt.receipt_id}",
        f"conversation_status: {receipt.conversation_status}",
        f"repair_required: {receipt.repair_required}",
        f"provisional_events_open: {receipt.provisional_events_open}",
        f"events: {len(receipt.events)}",
        f"production_authority: {receipt.production_authority}",
    ])


def _classify(events: tuple[ConversationalEvent, ...], final_claim: str | None) -> tuple[str, bool, int, tuple[str, ...]]:
    if any(e.event_type == "BLOCK" for e in events):
        return "BLOCKED", True, sum(1 for e in events if e.provisional and e.event_type == "PROVISIONAL_UTTERANCE"), ("do_not_emit_further", "request_steward_repair", "record_retraction")
    provisional_count = sum(1 for e in events if e.provisional and e.event_type == "PROVISIONAL_UTTERANCE")
    repair_count = sum(1 for e in events if e.event_type in {"CORRECTION", "RETRACTION"})
    ratified = any(e.event_type == "RATIFICATION" for e in events)
    if ratified and final_claim:
        return "RATIFIED", False, 0, ()
    if provisional_count and repair_count:
        return "REPAIRED", False, 0, ("preserve_repair_trace",)
    if provisional_count:
        return "OPEN_PROVISIONAL", True, provisional_count, ("await_relay_or_steward_update", "do_not_present_as_ratified")
    return "RATIFIED" if final_claim else "REPAIRED", False, 0, ()


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stable_id(*parts: str) -> str:
    return hashlib.sha256("::".join(parts).encode("utf-8")).hexdigest()[:24]


def _to_jsonable(obj: Any) -> Any:
    if hasattr(obj, "__dataclass_fields__"):
        return {k: _to_jsonable(v) for k, v in asdict(obj).items()}
    if isinstance(obj, tuple):
        return [_to_jsonable(v) for v in obj]
    if isinstance(obj, dict):
        return {k: _to_jsonable(v) for k, v in obj.items()}
    return obj


def _scenario(name: str) -> ConversationalReceipt:
    t = "2026-04-25T06:42:00+00:00"
    if name == "open":
        return build_conversational_receipt(events=[make_event("PROVISIONAL_UTTERANCE", "My first read is that this is a visual packet issue.", timestamp=t)], emitted_at=t)
    if name == "blocked":
        return build_conversational_receipt(events=[make_event("PROVISIONAL_UTTERANCE", "ION is production ready.", claim_class="C5", timestamp=t), make_event("BLOCK", "Blocked forbidden production claim.", claim_class="C5", timestamp=t)], emitted_at=t)
    return build_conversational_receipt(events=[make_event("PROVISIONAL_UTTERANCE", "My first read is broad.", timestamp=t), make_event("CORRECTION", "Correction: the checked surface is narrower.", timestamp=t, provisional=False, repair_of="initial")], emitted_at=t, final_claim="The checked surface is narrower than the provisional first read.")


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create or inspect V42 conversational receipt.")
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--scenario", choices=["open", "repaired", "blocked"], default="repaired")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    receipt = _scenario(args.scenario)
    errors = validate_conversational_receipt(receipt)
    if args.write:
        print(f"receipt_path: {write_conversational_receipt(args.workspace_root, receipt)}")
    print(format_conversational_summary(receipt))
    if errors:
        print("errors:")
        for e in errors:
            print(f"- {e}")
        return 3 if receipt.conversation_status == "BLOCKED" else 2
    return 3 if receipt.conversation_status == "BLOCKED" else 0

if __name__ == "__main__":
    raise SystemExit(_main())

