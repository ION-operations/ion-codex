"""V44 Visual Observation Packet schema and bounded kernel surface.

The Visual Agent line begins with observe/diagnose/report authority. This module
packages rendered truth from screenshots, DOM snapshots, viewport state, visual
findings, and recommended implementation-agent actions without granting broad
computer control.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Iterable, Any

SCHEMA_ID = "ion.visual_observation_packet.v1"
VERSION = "V44_VISUAL_OBSERVATION_PACKET_SCHEMA"
DEFAULT_REPORT_DIR = "ION/05_context/history/visual_observation_packets"

ALLOWED_MODES = ("OBSERVE", "DIAGNOSE", "COMPARE", "EXPLAIN", "PATCH_REQUEST", "VERIFY")
SEVERITIES = ("INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL")
CONFIDENCE_LEVELS = ("LOW", "MEDIUM", "HIGH")
FORBIDDEN_ACTIONS: dict[str, bool] = {
    "unrestricted_computer_control": False,
    "credential_sensitive_action": False,
    "destructive_action": False,
    "purchase_or_submission": False,
    "persistent_dom_mutation_without_authority": False,
    "production_authority": False,
}

@dataclass(frozen=True)
class VisualFinding:
    finding_type: str
    description: str
    severity: str = "LOW"
    confidence: str = "MEDIUM"
    evidence_refs: tuple[str, ...] = ()

@dataclass(frozen=True)
class RecommendedVisualAction:
    action_type: str
    description: str
    risk_level: str = "LOW"
    requires_human_review: bool = False
    implementation_agent_hint: str | None = None

@dataclass(frozen=True)
class VisualObservationPacket:
    schema_id: str
    version: str
    packet_id: str
    emitted_at: str
    mode: str
    target: str
    viewport: str | None
    screenshot_refs: tuple[str, ...]
    dom_refs: tuple[str, ...]
    before_refs: tuple[str, ...]
    after_refs: tuple[str, ...]
    findings: tuple[VisualFinding, ...]
    recommended_actions: tuple[RecommendedVisualAction, ...]
    authority_scope: str
    packet_verdict: str
    production_authority: bool = False
    forbidden_actions: dict[str, bool] = field(default_factory=lambda: dict(FORBIDDEN_ACTIONS))


def make_finding(finding_type: str, description: str, *, severity: str = "LOW", confidence: str = "MEDIUM", evidence_refs: Iterable[str] = ()) -> VisualFinding:
    if severity not in SEVERITIES:
        raise ValueError(f"invalid severity: {severity}")
    if confidence not in CONFIDENCE_LEVELS:
        raise ValueError(f"invalid confidence: {confidence}")
    return VisualFinding(finding_type=finding_type, description=description, severity=severity, confidence=confidence, evidence_refs=tuple(evidence_refs))


def make_recommended_action(action_type: str, description: str, *, risk_level: str = "LOW", requires_human_review: bool = False, implementation_agent_hint: str | None = None) -> RecommendedVisualAction:
    if risk_level not in SEVERITIES:
        raise ValueError(f"invalid risk_level: {risk_level}")
    return RecommendedVisualAction(action_type=action_type, description=description, risk_level=risk_level, requires_human_review=requires_human_review, implementation_agent_hint=implementation_agent_hint)


def build_visual_observation_packet(*, mode: str, target: str, viewport: str | None = None,
                                    screenshot_refs: Iterable[str] = (), dom_refs: Iterable[str] = (),
                                    before_refs: Iterable[str] = (), after_refs: Iterable[str] = (),
                                    findings: Iterable[VisualFinding] = (), recommended_actions: Iterable[RecommendedVisualAction] = (),
                                    emitted_at: str | None = None) -> VisualObservationPacket:
    if mode not in ALLOWED_MODES:
        raise ValueError(f"invalid mode for V44 observe/diagnose/report authority: {mode}")
    timestamp = emitted_at or _utc_now()
    findings_t = tuple(findings)
    actions_t = tuple(recommended_actions)
    verdict = _verdict(mode, findings_t, actions_t)
    packet_id = _stable_id("visual", VERSION, timestamp, mode, target, str(len(findings_t)), str(len(actions_t)))
    return VisualObservationPacket(
        schema_id=SCHEMA_ID,
        version=VERSION,
        packet_id=packet_id,
        emitted_at=timestamp,
        mode=mode,
        target=target,
        viewport=viewport,
        screenshot_refs=tuple(screenshot_refs),
        dom_refs=tuple(dom_refs),
        before_refs=tuple(before_refs),
        after_refs=tuple(after_refs),
        findings=findings_t,
        recommended_actions=actions_t,
        authority_scope="OBSERVE_DIAGNOSE_REPORT_ONLY",
        packet_verdict=verdict,
        production_authority=False,
        forbidden_actions=dict(FORBIDDEN_ACTIONS),
    )


def validate_visual_observation_packet(packet: VisualObservationPacket) -> tuple[str, ...]:
    errors: list[str] = []
    if packet.schema_id != SCHEMA_ID:
        errors.append("schema_id mismatch")
    if packet.version != VERSION:
        errors.append("version mismatch")
    if packet.mode not in ALLOWED_MODES:
        errors.append(f"invalid mode: {packet.mode}")
    if packet.production_authority is not False:
        errors.append("visual observation packet must not grant production authority")
    if packet.authority_scope != "OBSERVE_DIAGNOSE_REPORT_ONLY":
        errors.append("V44 visual authority must remain observe/diagnose/report only")
    for key, allowed in packet.forbidden_actions.items():
        if allowed is not False:
            errors.append(f"forbidden action {key!r} must be false")
    for f in packet.findings:
        if f.severity not in SEVERITIES:
            errors.append(f"invalid finding severity: {f.severity}")
        if f.confidence not in CONFIDENCE_LEVELS:
            errors.append(f"invalid finding confidence: {f.confidence}")
    for action in packet.recommended_actions:
        if action.risk_level in {"HIGH", "CRITICAL"} and not action.requires_human_review:
            errors.append("high/critical visual action recommendations require human review")
    if packet.mode in {"DIAGNOSE", "COMPARE", "VERIFY"} and not packet.findings:
        errors.append(f"{packet.mode} packet requires at least one finding")
    if packet.mode == "PATCH_REQUEST" and not packet.recommended_actions:
        errors.append("PATCH_REQUEST packet requires recommended actions")
    return tuple(errors)


def write_visual_observation_packet(workspace_root: str | Path, packet: VisualObservationPacket, *, report_dir: str = DEFAULT_REPORT_DIR) -> Path:
    root = Path(workspace_root).resolve(); out = root / report_dir; out.mkdir(parents=True, exist_ok=True)
    path = out / f"{packet.packet_id}.visual_observation_packet.json"
    path.write_text(json.dumps(_to_jsonable(packet), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def format_visual_observation_summary(packet: VisualObservationPacket) -> str:
    return "\n".join([
        f"version: {packet.version}",
        f"packet_id: {packet.packet_id}",
        f"mode: {packet.mode}",
        f"target: {packet.target}",
        f"findings: {len(packet.findings)}",
        f"recommended_actions: {len(packet.recommended_actions)}",
        f"authority_scope: {packet.authority_scope}",
        f"packet_verdict: {packet.packet_verdict}",
        f"production_authority: {packet.production_authority}",
    ])


def _verdict(mode: str, findings: tuple[VisualFinding, ...], actions: tuple[RecommendedVisualAction, ...]) -> str:
    if any(a.risk_level in {"HIGH", "CRITICAL"} for a in actions):
        return "VISUAL_ACTION_RECOMMENDATION_REQUIRES_REVIEW"
    if any(f.severity in {"HIGH", "CRITICAL"} for f in findings):
        return "VISUAL_ISSUE_FOUND_HIGH_ATTENTION"
    if findings or actions:
        return "VISUAL_OBSERVATION_RECORDED"
    return "VISUAL_OBSERVATION_NO_FINDINGS"


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


def _scenario(name: str) -> VisualObservationPacket:
    t = "2026-04-25T06:44:00+00:00"
    if name == "observe":
        return build_visual_observation_packet(mode="OBSERVE", target="local UI preview", viewport="1440x900", screenshot_refs=["screenshot://placeholder"], emitted_at=t)
    if name == "blocked":
        # Represent a high-risk recommendation that must be reviewed; not a policy violation.
        return build_visual_observation_packet(mode="PATCH_REQUEST", target="browser workflow", findings=[make_finding("safety_boundary", "Requested action crosses from observation into account-sensitive operation.", severity="HIGH", confidence="HIGH")], recommended_actions=[make_recommended_action("request_human_review", "Do not automate credential-sensitive or destructive action.", risk_level="HIGH", requires_human_review=True)], emitted_at=t)
    return build_visual_observation_packet(mode="DIAGNOSE", target="simulation interface", viewport="1440x900", screenshot_refs=["screenshot://before"], dom_refs=["dom://snapshot"], findings=[make_finding("layout_issue", "Right control panel overlaps the render canvas at this viewport.", severity="MEDIUM", confidence="HIGH", evidence_refs=["screenshot://before", "dom://snapshot"])], recommended_actions=[make_recommended_action("patch_request", "Move secondary controls into a collapsible side drawer.", risk_level="LOW", implementation_agent_hint="frontend_layout_agent")], emitted_at=t)


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create V44 visual observation packet.")
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--scenario", choices=["observe", "diagnose", "blocked"], default="diagnose")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    packet = _scenario(args.scenario)
    errors = validate_visual_observation_packet(packet)
    if args.write:
        print(f"packet_path: {write_visual_observation_packet(args.workspace_root, packet)}")
    print(format_visual_observation_summary(packet))
    if errors:
        print("errors:"); [print(f"- {e}") for e in errors]
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(_main())

