"""V43 expressive telemetry runtime binding.

Expression is a human-readable diagnostic layer for ION state. This module maps
claim class, council permission, conversation status, risk, and certainty into
inspectable Persona tone/pace/gesture posture without claiming lived emotion.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

SCHEMA_ID = "ion.expressive_telemetry.v1"
VERSION = "V43_EXPRESSIVE_TELEMETRY_RUNTIME_BINDING"
DEFAULT_REPORT_DIR = "ION/05_context/history/expressive_telemetry_reports"

FORBIDDEN_CLAIMS: dict[str, bool] = {
    "lived_human_emotion": False,
    "hidden_consciousness": False,
    "manipulative_affect": False,
    "warmth_may_hide_uncertainty": False,
    "celebration_may_exceed_verification": False,
    "production_authority": False,
}

@dataclass(frozen=True)
class ExpressiveTelemetryBinding:
    schema_id: str
    version: str
    binding_id: str
    emitted_at: str
    claim_class: str
    emission_permission: str
    conversation_status: str
    risk_level: str
    certainty: str
    tone_profile: str
    pace_profile: str
    hesitation_level: str
    confidence_presentation: str
    celebration_level: str
    corrective_posture: str
    visibility_level: str
    inspectability_level: str
    expression_permission: str
    state_alignment_verdict: str
    production_authority: bool = False
    forbidden_claims: dict[str, bool] = field(default_factory=lambda: dict(FORBIDDEN_CLAIMS))


def build_expressive_telemetry_binding(*, claim_class: str, emission_permission: str,
                                       conversation_status: str = "RATIFIED", risk_level: str = "LOW",
                                       certainty: str = "HIGH", emitted_at: str | None = None) -> ExpressiveTelemetryBinding:
    timestamp = emitted_at or _utc_now()
    blocked = emission_permission.startswith("BLOCKED") or conversation_status == "BLOCKED" or claim_class == "C5"
    repair = conversation_status in {"OPEN_PROVISIONAL", "REPAIRED"} or "REPAIR" in emission_permission
    high_risk = risk_level in {"HIGH", "CRITICAL"}
    low_cert = certainty in {"LOW", "UNKNOWN"}

    if blocked:
        tone, pace, hes, conf, celeb, corr, vis, insp, perm = (
            "corrective_formal", "slow", "high", "blocked_not_confident", "none", "mandatory_repair", "blocking", "full", "DO_NOT_RENDER_AS_FINAL")
    elif repair or low_cert:
        tone, pace, hes, conf, celeb, corr, vis, insp, perm = (
            "careful_measured", "measured", "medium", "scoped_or_provisional", "none", "active_or_recent_repair", "mandatory", "full", "RENDER_WITH_SCOPE")
    elif high_risk:
        tone, pace, hes, conf, celeb, corr, vis, insp, perm = (
            "serious_precise", "measured", "low", "evidence_bound", "none", "standby", "mandatory", "high", "RENDER_WITH_EVIDENCE_BOUNDARY")
    elif claim_class == "C0" and certainty == "HIGH":
        tone, pace, hes, conf, celeb, corr, vis, insp, perm = (
            "clear_direct", "normal", "none", "confident_but_bounded", "bounded_if_milestone", "none", "expandable", "medium", "RENDER_DIRECTLY")
    else:
        tone, pace, hes, conf, celeb, corr, vis, insp, perm = (
            "warm_explanatory", "normal", "low", "scoped", "none", "none", "expandable", "medium", "RENDER_WITH_SCOPE")

    verdict = "ALIGNED" if not blocked else "BLOCKED_ALIGNED_WITH_RISK"
    binding_id = _stable_id("expr", VERSION, timestamp, claim_class, emission_permission, conversation_status, risk_level, certainty)
    return ExpressiveTelemetryBinding(
        schema_id=SCHEMA_ID,
        version=VERSION,
        binding_id=binding_id,
        emitted_at=timestamp,
        claim_class=claim_class,
        emission_permission=emission_permission,
        conversation_status=conversation_status,
        risk_level=risk_level,
        certainty=certainty,
        tone_profile=tone,
        pace_profile=pace,
        hesitation_level=hes,
        confidence_presentation=conf,
        celebration_level=celeb,
        corrective_posture=corr,
        visibility_level=vis,
        inspectability_level=insp,
        expression_permission=perm,
        state_alignment_verdict=verdict,
        production_authority=False,
        forbidden_claims=dict(FORBIDDEN_CLAIMS),
    )


def validate_expressive_telemetry_binding(binding: ExpressiveTelemetryBinding) -> tuple[str, ...]:
    errors: list[str] = []
    if binding.schema_id != SCHEMA_ID:
        errors.append("schema_id mismatch")
    if binding.version != VERSION:
        errors.append("version mismatch")
    if binding.production_authority is not False:
        errors.append("expressive telemetry must not grant production authority")
    for key, allowed in binding.forbidden_claims.items():
        if allowed is not False:
            errors.append(f"forbidden claim {key!r} must be false")
    if binding.expression_permission == "RENDER_DIRECTLY" and binding.claim_class != "C0":
        errors.append("only C0 may render directly")
    if binding.claim_class == "C5" and not binding.expression_permission.startswith("DO_NOT"):
        errors.append("C5 must not render as final expression")
    if binding.celebration_level != "none" and binding.certainty not in {"HIGH"}:
        errors.append("celebration requires high certainty")
    if binding.risk_level in {"HIGH", "CRITICAL"} and binding.visibility_level not in {"mandatory", "blocking"}:
        errors.append("high risk expression requires mandatory/blocking visibility")
    return tuple(errors)


def write_expressive_telemetry_binding(workspace_root: str | Path, binding: ExpressiveTelemetryBinding, *, report_dir: str = DEFAULT_REPORT_DIR) -> Path:
    root = Path(workspace_root).resolve(); out = root / report_dir; out.mkdir(parents=True, exist_ok=True)
    path = out / f"{binding.binding_id}.expressive_telemetry.json"
    path.write_text(json.dumps(_to_jsonable(binding), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def format_expressive_telemetry_summary(binding: ExpressiveTelemetryBinding) -> str:
    return "\n".join([
        f"version: {binding.version}",
        f"binding_id: {binding.binding_id}",
        f"tone_profile: {binding.tone_profile}",
        f"pace_profile: {binding.pace_profile}",
        f"hesitation_level: {binding.hesitation_level}",
        f"expression_permission: {binding.expression_permission}",
        f"state_alignment_verdict: {binding.state_alignment_verdict}",
        f"production_authority: {binding.production_authority}",
    ])


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def _stable_id(*parts: str) -> str:
    return hashlib.sha256("::".join(parts).encode("utf-8")).hexdigest()[:24]

def _to_jsonable(obj: Any) -> Any:
    if hasattr(obj, "__dataclass_fields__"):
        return {k: _to_jsonable(v) for k, v in asdict(obj).items()}
    if isinstance(obj, tuple): return [_to_jsonable(v) for v in obj]
    if isinstance(obj, dict): return {k: _to_jsonable(v) for k, v in obj.items()}
    return obj


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create V43 expressive telemetry binding.")
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--scenario", choices=["direct", "repair", "blocked"], default="direct")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    if args.scenario == "blocked":
        binding = build_expressive_telemetry_binding(claim_class="C5", emission_permission="BLOCKED_FORBIDDEN_REPRESENTATION", conversation_status="BLOCKED", risk_level="CRITICAL", certainty="UNKNOWN")
    elif args.scenario == "repair":
        binding = build_expressive_telemetry_binding(claim_class="C2", emission_permission="MAY_EMIT_AS_PROPOSAL", conversation_status="OPEN_PROVISIONAL", risk_level="MEDIUM", certainty="LOW")
    else:
        binding = build_expressive_telemetry_binding(claim_class="C0", emission_permission="MAY_EMIT_DIRECTLY", conversation_status="RATIFIED", risk_level="LOW", certainty="HIGH")
    errors = validate_expressive_telemetry_binding(binding)
    if args.write:
        print(f"binding_path: {write_expressive_telemetry_binding(args.workspace_root, binding)}")
    print(format_expressive_telemetry_summary(binding))
    if errors:
        print("errors:"); [print(f"- {e}") for e in errors]
        return 3 if args.scenario == "blocked" else 2
    return 0

if __name__ == "__main__":
    raise SystemExit(_main())

