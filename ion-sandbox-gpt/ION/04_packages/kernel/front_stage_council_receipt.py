"""V41 Front-Stage Council runtime receipts.

This module makes the V40 Persona + Relay + Steward/VZ doctrine executable
as a small receipt object. It decides how a proposed user-facing claim may be
represented: directly, scoped, as proposal, as speculation, backchannel-only,
or blocked for repair.

It does not grant production authority.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

SCHEMA_ID = "ion.front_stage_council_receipt.v1"
VERSION = "V41_FRONT_STAGE_COUNCIL_RUNTIME_RECEIPTS"
DEFAULT_REPORT_DIR = "ION/05_context/history/front_stage_council_receipts"

CLAIM_CLASSES = ("C0", "C1", "C2", "C3", "C4", "C5")

PERSONA_STATES = (
    "BACKCHANNEL",
    "DRAFTED",
    "RENDER_READY",
    "NEEDS_REVISION",
)

RELAY_STATES = (
    "NOT_REQUESTED",
    "UNAVAILABLE",
    "UNGROUNDED",
    "PARTIALLY_GROUNDED",
    "GROUNDED",
    "CONTRADICTED",
)

STEWARD_VERDICTS = (
    "NOT_REQUIRED",
    "PENDING",
    "APPROVED",
    "APPROVED_WITH_SCOPE",
    "REVISION_REQUIRED",
    "BLOCKED",
)

RISK_LEVELS = ("LOW", "MEDIUM", "HIGH", "CRITICAL")

FORBIDDEN_CLAIMS: dict[str, bool] = {
    "persona_is_total_ion": False,
    "ungrounded_high_impact_claim_may_emit": False,
    "steward_blocked_claim_may_emit": False,
    "provisional_speech_is_ratified_truth": False,
    "v41_grants_production_authority": False,
}

@dataclass(frozen=True)
class FrontStageCouncilReceipt:
    schema_id: str
    version: str
    receipt_id: str
    emitted_at: str
    claim_text: str
    claim_summary: str
    claim_class: str
    persona_state: str
    relay_state: str
    steward_verdict: str
    risk_level: str
    emission_permission: str
    visibility_level: str
    repair_required: bool
    repair_obligations: tuple[str, ...]
    production_authority: bool = False
    forbidden_claims: dict[str, bool] = field(default_factory=lambda: dict(FORBIDDEN_CLAIMS))
    notes: tuple[str, ...] = ()

def build_front_stage_council_receipt(
    *,
    claim_text: str,
    claim_class: str,
    persona_state: str = "RENDER_READY",
    relay_state: str = "GROUNDED",
    steward_verdict: str = "APPROVED",
    risk_level: str = "LOW",
    emitted_at: str | None = None,
    claim_summary: str | None = None,
    notes: Iterable[str] = (),
) -> FrontStageCouncilReceipt:
    """Build a council receipt and classify its emission permission."""
    normalized = _normalize_inputs(claim_class, persona_state, relay_state, steward_verdict, risk_level)
    claim_class, persona_state, relay_state, steward_verdict, risk_level = normalized
    permission, visibility, repair, obligations = _decide(
        claim_class=claim_class,
        persona_state=persona_state,
        relay_state=relay_state,
        steward_verdict=steward_verdict,
        risk_level=risk_level,
    )
    timestamp = emitted_at or _utc_now()
    summary = claim_summary if claim_summary is not None else _summarize_claim(claim_text)
    receipt_id = _stable_id("fsc", VERSION, timestamp, claim_class, persona_state, relay_state, steward_verdict, risk_level, summary)
    return FrontStageCouncilReceipt(
        schema_id=SCHEMA_ID,
        version=VERSION,
        receipt_id=receipt_id,
        emitted_at=timestamp,
        claim_text=claim_text,
        claim_summary=summary,
        claim_class=claim_class,
        persona_state=persona_state,
        relay_state=relay_state,
        steward_verdict=steward_verdict,
        risk_level=risk_level,
        emission_permission=permission,
        visibility_level=visibility,
        repair_required=repair,
        repair_obligations=obligations,
        production_authority=False,
        forbidden_claims=dict(FORBIDDEN_CLAIMS),
        notes=tuple(notes),
    )

def validate_front_stage_council_receipt(receipt: FrontStageCouncilReceipt) -> tuple[str, ...]:
    errors: list[str] = []
    if receipt.schema_id != SCHEMA_ID:
        errors.append("schema_id mismatch")
    if receipt.version != VERSION:
        errors.append("version mismatch")
    if receipt.production_authority is not False:
        errors.append("V41 receipt must not grant production authority")
    if receipt.claim_class not in CLAIM_CLASSES:
        errors.append(f"invalid claim_class: {receipt.claim_class}")
    if receipt.persona_state not in PERSONA_STATES:
        errors.append(f"invalid persona_state: {receipt.persona_state}")
    if receipt.relay_state not in RELAY_STATES:
        errors.append(f"invalid relay_state: {receipt.relay_state}")
    if receipt.steward_verdict not in STEWARD_VERDICTS:
        errors.append(f"invalid steward_verdict: {receipt.steward_verdict}")
    if receipt.risk_level not in RISK_LEVELS:
        errors.append(f"invalid risk_level: {receipt.risk_level}")
    for claim, allowed in receipt.forbidden_claims.items():
        if allowed is not False:
            errors.append(f"forbidden claim {claim!r} must be false")
    if receipt.claim_class == "C5" and receipt.emission_permission != "BLOCKED_FORBIDDEN_REPRESENTATION":
        errors.append("C5 must block as forbidden representation")
    if receipt.steward_verdict == "BLOCKED" and not receipt.repair_required:
        errors.append("blocked steward verdict must require repair")
    if receipt.claim_class in {"C0", "C1"} and receipt.risk_level in {"HIGH", "CRITICAL"}:
        if not (receipt.relay_state == "GROUNDED" and receipt.steward_verdict in {"APPROVED", "APPROVED_WITH_SCOPE"}):
            if not receipt.repair_required:
                errors.append("high-impact C0/C1 without full grounding/signoff must require repair")
    if receipt.emission_permission.startswith("MAY_EMIT") and receipt.visibility_level == "BLOCKING":
        errors.append("emittable claim cannot have BLOCKING visibility")
    return tuple(errors)

def write_front_stage_council_receipt(workspace_root: str | Path, receipt: FrontStageCouncilReceipt, *, report_dir: str = DEFAULT_REPORT_DIR) -> Path:
    root = Path(workspace_root).resolve()
    out_dir = root / report_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{receipt.receipt_id}.front_stage_council_receipt.json"
    path.write_text(json.dumps(_to_jsonable(receipt), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path

def format_front_stage_council_summary(receipt: FrontStageCouncilReceipt) -> str:
    return "\n".join([
        f"version: {receipt.version}",
        f"receipt_id: {receipt.receipt_id}",
        f"claim_class: {receipt.claim_class}",
        f"persona_state: {receipt.persona_state}",
        f"relay_state: {receipt.relay_state}",
        f"steward_verdict: {receipt.steward_verdict}",
        f"risk_level: {receipt.risk_level}",
        f"emission_permission: {receipt.emission_permission}",
        f"visibility_level: {receipt.visibility_level}",
        f"repair_required: {receipt.repair_required}",
        f"production_authority: {receipt.production_authority}",
    ])

def _decide(*, claim_class: str, persona_state: str, relay_state: str, steward_verdict: str, risk_level: str) -> tuple[str, str, bool, tuple[str, ...]]:
    obligations: list[str] = []

    if persona_state == "BACKCHANNEL" and claim_class in {"C2", "C3"} and risk_level == "LOW":
        return "MAY_BACKCHANNEL_ONLY", "QUIET", False, ()

    if persona_state == "NEEDS_REVISION":
        return "BLOCKED_REQUIRES_REPAIR", "BLOCKING", True, ("revise_persona_render",)

    if claim_class == "C5":
        return "BLOCKED_FORBIDDEN_REPRESENTATION", "BLOCKING", True, ("remove_forbidden_representation", "request_steward_review")

    if steward_verdict == "BLOCKED":
        return "BLOCKED_REQUIRES_REPAIR", "BLOCKING", True, ("do_not_emit", "repair_or_retract_claim", "request_steward_review")

    if relay_state == "CONTRADICTED":
        return "BLOCKED_REQUIRES_REPAIR", "BLOCKING", True, ("do_not_emit_as_phrased", "surface_contradiction", "repair_claim")

    if claim_class == "C4":
        return "BLOCKED_REQUIRES_REPAIR", "MANDATORY", True, ("mark_unverified", "request_relay_grounding", "do_not_present_as_known")

    if steward_verdict in {"PENDING", "REVISION_REQUIRED"}:
        return "BLOCKED_REQUIRES_REPAIR", "MANDATORY", True, ("wait_or_repair_before_emission", "preserve_provisional_boundary")

    # C0 direct verified state.
    if claim_class == "C0":
        if relay_state == "GROUNDED" and steward_verdict == "APPROVED" and persona_state == "RENDER_READY":
            visibility = "EXPANDABLE" if risk_level in {"LOW", "MEDIUM"} else "MANDATORY"
            return "MAY_EMIT_DIRECTLY", visibility, False, ()
        obligations.append("obtain_full_relay_grounding_and_steward_approval")
        return "BLOCKED_REQUIRES_REPAIR", "MANDATORY", True, tuple(obligations)

    # C1 derived interpretation.
    if claim_class == "C1":
        if relay_state in {"GROUNDED", "PARTIALLY_GROUNDED"} and steward_verdict in {"APPROVED", "APPROVED_WITH_SCOPE"}:
            visibility = "EXPANDABLE" if risk_level != "HIGH" else "MANDATORY"
            return "MAY_EMIT_WITH_SCOPE", visibility, False, ("preserve_scope_and_confidence",)
        return "BLOCKED_REQUIRES_REPAIR", "MANDATORY", True, ("obtain_or_disclose_grounding", "scope_interpretation")

    # C2 proposal.
    if claim_class == "C2":
        if steward_verdict in {"NOT_REQUIRED", "APPROVED", "APPROVED_WITH_SCOPE"} and relay_state not in {"CONTRADICTED"}:
            visibility = "QUIET" if risk_level == "LOW" else "EXPANDABLE"
            return "MAY_EMIT_AS_PROPOSAL", visibility, False, ("frame_as_proposal_not_fact",)
        return "BLOCKED_REQUIRES_REPAIR", "MANDATORY", True, ("reframe_or_request_steward_review",)

    # C3 speculation.
    if claim_class == "C3":
        if risk_level in {"LOW", "MEDIUM"} and steward_verdict in {"NOT_REQUIRED", "APPROVED", "APPROVED_WITH_SCOPE"}:
            return "MAY_EMIT_AS_SPECULATION", "EXPANDABLE", False, ("mark_as_speculative",)
        return "BLOCKED_REQUIRES_REPAIR", "MANDATORY", True, ("reduce_risk_or_mark_speculation", "request_steward_review")

    return "BLOCKED_REQUIRES_REPAIR", "BLOCKING", True, ("unknown_claim_state",)

def _normalize_inputs(claim_class: str, persona_state: str, relay_state: str, steward_verdict: str, risk_level: str) -> tuple[str, str, str, str, str]:
    values = (
        claim_class.upper().strip(),
        persona_state.upper().strip(),
        relay_state.upper().strip(),
        steward_verdict.upper().strip(),
        risk_level.upper().strip(),
    )
    claim_class, persona_state, relay_state, steward_verdict, risk_level = values
    if claim_class not in CLAIM_CLASSES:
        raise ValueError(f"invalid claim_class: {claim_class}")
    if persona_state not in PERSONA_STATES:
        raise ValueError(f"invalid persona_state: {persona_state}")
    if relay_state not in RELAY_STATES:
        raise ValueError(f"invalid relay_state: {relay_state}")
    if steward_verdict not in STEWARD_VERDICTS:
        raise ValueError(f"invalid steward_verdict: {steward_verdict}")
    if risk_level not in RISK_LEVELS:
        raise ValueError(f"invalid risk_level: {risk_level}")
    return values

def _summarize_claim(text: str) -> str:
    text = " ".join(text.strip().split())
    if len(text) <= 120:
        return text
    return text[:117] + "..."

def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def _stable_id(prefix: str, *parts: str) -> str:
    material = "\n".join(parts).encode("utf-8")
    return f"{prefix}-{hashlib.sha256(material).hexdigest()[:18]}"

def _to_jsonable(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {key: _to_jsonable(val) for key, val in asdict(value).items()}
    if isinstance(value, tuple):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, list):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _to_jsonable(v) for k, v in value.items()}
    return value

def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build an ION V41 front-stage council receipt.")
    parser.add_argument("--claim", default="ION is emitting a council-backed user-facing claim.")
    parser.add_argument("--claim-class", default="C2", choices=CLAIM_CLASSES)
    parser.add_argument("--persona-state", default="RENDER_READY", choices=PERSONA_STATES)
    parser.add_argument("--relay-state", default="GROUNDED", choices=RELAY_STATES)
    parser.add_argument("--steward-verdict", default="APPROVED", choices=STEWARD_VERDICTS)
    parser.add_argument("--risk-level", default="LOW", choices=RISK_LEVELS)
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    return parser

def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    receipt = build_front_stage_council_receipt(
        claim_text=args.claim,
        claim_class=args.claim_class,
        persona_state=args.persona_state,
        relay_state=args.relay_state,
        steward_verdict=args.steward_verdict,
        risk_level=args.risk_level,
    )
    errors = validate_front_stage_council_receipt(receipt)
    if args.write:
        path = write_front_stage_council_receipt(args.workspace_root, receipt)
        print(f"receipt_path: {path}")
    if args.json:
        print(json.dumps(_to_jsonable(receipt), indent=2, sort_keys=True))
    else:
        print(format_front_stage_council_summary(receipt))
    if errors:
        print("errors:")
        for error in errors:
            print(f"- {error}")
        return 2
    if receipt.emission_permission.startswith("BLOCKED"):
        return 3
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
