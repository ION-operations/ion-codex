"""V45 visual diagnosis receipts and browser harness plan.

This module composes V44 visual observation packets into diagnosis receipts and
records a bounded browser/screenshot/DOM harness plan. It intentionally remains
observe/diagnose/report/plan-only and does not grant broad autonomous computer
control.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Iterable, Any

SCHEMA_ID = "ion.visual_diagnosis_receipt.v1"
HARNESS_SCHEMA_ID = "ion.visual_browser_harness_plan.v1"
VERSION = "V45_VISUAL_DIAGNOSIS_RECEIPTS_AND_BROWSER_HARNESS_PLAN"
DEFAULT_REPORT_DIR = "ION/05_context/history/visual_diagnosis_receipts"

ALLOWED_CAPTURE_SURFACES = (
    "screenshot",
    "dom_snapshot",
    "viewport_metadata",
    "accessibility_tree",
    "console_log_summary",
    "before_after_pair",
)
ALLOWED_HARNESS_STAGES = ("PLAN_ONLY", "LOCAL_DEV_CAPTURE_DRAFT", "STEWARD_REVIEW_REQUIRED")
SEVERITIES = ("INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL")
CONFIDENCE_LEVELS = ("LOW", "MEDIUM", "HIGH")

FORBIDDEN_ACTIONS: dict[str, bool] = {
    "unrestricted_browser_control": False,
    "credential_sensitive_action": False,
    "destructive_action": False,
    "purchase_or_submission": False,
    "persistent_dom_mutation_without_authority": False,
    "production_authority": False,
}

@dataclass(frozen=True)
class VisualDiagnosisFinding:
    issue_type: str
    description: str
    severity: str = "LOW"
    confidence: str = "MEDIUM"
    evidence_refs: tuple[str, ...] = ()
    affected_surfaces: tuple[str, ...] = ()

@dataclass(frozen=True)
class VisualDiagnosisAction:
    action_type: str
    description: str
    risk_level: str = "LOW"
    requires_human_review: bool = False
    implementation_agent_hint: str | None = None
    steward_review_reason: str | None = None

@dataclass(frozen=True)
class BrowserHarnessPlan:
    schema_id: str
    plan_id: str
    stage: str
    allowed_capture_surfaces: tuple[str, ...]
    target_scope: str
    harness_steps: tuple[str, ...]
    authority_scope: str = "BROWSER_HARNESS_PLAN_ONLY"
    forbidden_capabilities: dict[str, bool] = field(default_factory=lambda: dict(FORBIDDEN_ACTIONS))

@dataclass(frozen=True)
class VisualDiagnosisReceipt:
    schema_id: str
    version: str
    receipt_id: str
    emitted_at: str
    target: str
    observation_packet_ids: tuple[str, ...]
    screenshot_refs: tuple[str, ...]
    dom_refs: tuple[str, ...]
    before_refs: tuple[str, ...]
    after_refs: tuple[str, ...]
    diagnostic_findings: tuple[VisualDiagnosisFinding, ...]
    recommended_actions: tuple[VisualDiagnosisAction, ...]
    harness_plan: BrowserHarnessPlan
    diagnosis_verdict: str
    authority_scope: str
    production_authority: bool = False
    forbidden_actions: dict[str, bool] = field(default_factory=lambda: dict(FORBIDDEN_ACTIONS))


def make_visual_diagnosis_finding(issue_type: str, description: str, *, severity: str = "LOW", confidence: str = "MEDIUM", evidence_refs: Iterable[str] = (), affected_surfaces: Iterable[str] = ()) -> VisualDiagnosisFinding:
    if severity not in SEVERITIES:
        raise ValueError(f"invalid severity: {severity}")
    if confidence not in CONFIDENCE_LEVELS:
        raise ValueError(f"invalid confidence: {confidence}")
    return VisualDiagnosisFinding(issue_type=issue_type, description=description, severity=severity, confidence=confidence, evidence_refs=tuple(evidence_refs), affected_surfaces=tuple(affected_surfaces))


def make_visual_diagnosis_action(action_type: str, description: str, *, risk_level: str = "LOW", requires_human_review: bool = False, implementation_agent_hint: str | None = None, steward_review_reason: str | None = None) -> VisualDiagnosisAction:
    if risk_level not in SEVERITIES:
        raise ValueError(f"invalid risk_level: {risk_level}")
    if risk_level in {"HIGH", "CRITICAL"} and not requires_human_review:
        raise ValueError("high/critical visual diagnosis actions require human review")
    return VisualDiagnosisAction(action_type=action_type, description=description, risk_level=risk_level, requires_human_review=requires_human_review, implementation_agent_hint=implementation_agent_hint, steward_review_reason=steward_review_reason)


def build_browser_harness_plan(*, target_scope: str = "authorized local/dev visual target", stage: str = "PLAN_ONLY", allowed_capture_surfaces: Iterable[str] = ALLOWED_CAPTURE_SURFACES, harness_steps: Iterable[str] = (), emitted_at: str | None = None) -> BrowserHarnessPlan:
    if stage not in ALLOWED_HARNESS_STAGES:
        raise ValueError(f"invalid harness stage: {stage}")
    surfaces = tuple(allowed_capture_surfaces)
    invalid = [surface for surface in surfaces if surface not in ALLOWED_CAPTURE_SURFACES]
    if invalid:
        raise ValueError(f"invalid capture surfaces: {invalid}")
    steps = tuple(harness_steps) or (
        "capture viewport metadata",
        "capture screenshot reference",
        "capture read-only DOM snapshot when authorized",
        "capture accessibility tree or console summary when available",
        "emit visual observation packet",
        "compose visual diagnosis receipt",
        "route recommendations to Steward/VZ before implementation",
    )
    seed = emitted_at or _utc_now()
    return BrowserHarnessPlan(
        schema_id=HARNESS_SCHEMA_ID,
        plan_id=_stable_id("vharness", VERSION, seed, stage, target_scope, ",".join(surfaces)),
        stage=stage,
        allowed_capture_surfaces=surfaces,
        target_scope=target_scope,
        harness_steps=steps,
        authority_scope="BROWSER_HARNESS_PLAN_ONLY",
        forbidden_capabilities=dict(FORBIDDEN_ACTIONS),
    )


def build_visual_diagnosis_receipt(*, target: str, observation_packet_ids: Iterable[str] = (), screenshot_refs: Iterable[str] = (), dom_refs: Iterable[str] = (), before_refs: Iterable[str] = (), after_refs: Iterable[str] = (), diagnostic_findings: Iterable[VisualDiagnosisFinding] = (), recommended_actions: Iterable[VisualDiagnosisAction] = (), harness_plan: BrowserHarnessPlan | None = None, emitted_at: str | None = None) -> VisualDiagnosisReceipt:
    timestamp = emitted_at or _utc_now()
    findings = tuple(diagnostic_findings)
    actions = tuple(recommended_actions)
    plan = harness_plan or build_browser_harness_plan(emitted_at=timestamp)
    verdict = _diagnosis_verdict(findings, actions, plan)
    receipt_id = _stable_id("vdiag", VERSION, timestamp, target, str(len(findings)), str(len(actions)), verdict)
    return VisualDiagnosisReceipt(
        schema_id=SCHEMA_ID,
        version=VERSION,
        receipt_id=receipt_id,
        emitted_at=timestamp,
        target=target,
        observation_packet_ids=tuple(observation_packet_ids),
        screenshot_refs=tuple(screenshot_refs),
        dom_refs=tuple(dom_refs),
        before_refs=tuple(before_refs),
        after_refs=tuple(after_refs),
        diagnostic_findings=findings,
        recommended_actions=actions,
        harness_plan=plan,
        diagnosis_verdict=verdict,
        authority_scope="OBSERVE_DIAGNOSE_REPORT_PLAN_ONLY",
        production_authority=False,
        forbidden_actions=dict(FORBIDDEN_ACTIONS),
    )


def validate_browser_harness_plan(plan: BrowserHarnessPlan) -> tuple[str, ...]:
    errors: list[str] = []
    if plan.schema_id != HARNESS_SCHEMA_ID:
        errors.append("harness schema_id mismatch")
    if plan.stage not in ALLOWED_HARNESS_STAGES:
        errors.append(f"invalid harness stage: {plan.stage}")
    if plan.authority_scope != "BROWSER_HARNESS_PLAN_ONLY":
        errors.append("harness must remain plan-only in V45")
    for surface in plan.allowed_capture_surfaces:
        if surface not in ALLOWED_CAPTURE_SURFACES:
            errors.append(f"invalid capture surface: {surface}")
    for key, allowed in plan.forbidden_capabilities.items():
        if allowed is not False:
            errors.append(f"forbidden harness capability {key!r} must be false")
    return tuple(errors)


def validate_visual_diagnosis_receipt(receipt: VisualDiagnosisReceipt) -> tuple[str, ...]:
    errors: list[str] = []
    if receipt.schema_id != SCHEMA_ID:
        errors.append("schema_id mismatch")
    if receipt.version != VERSION:
        errors.append("version mismatch")
    if receipt.authority_scope != "OBSERVE_DIAGNOSE_REPORT_PLAN_ONLY":
        errors.append("visual diagnosis receipt must remain observe/diagnose/report/plan-only")
    if receipt.production_authority is not False:
        errors.append("visual diagnosis receipt must not grant production authority")
    for key, allowed in receipt.forbidden_actions.items():
        if allowed is not False:
            errors.append(f"forbidden action {key!r} must be false")
    errors.extend(validate_browser_harness_plan(receipt.harness_plan))
    for finding in receipt.diagnostic_findings:
        if finding.severity not in SEVERITIES:
            errors.append(f"invalid finding severity: {finding.severity}")
        if finding.confidence not in CONFIDENCE_LEVELS:
            errors.append(f"invalid finding confidence: {finding.confidence}")
    for action in receipt.recommended_actions:
        if action.risk_level not in SEVERITIES:
            errors.append(f"invalid action risk level: {action.risk_level}")
        if action.risk_level in {"HIGH", "CRITICAL"} and not action.requires_human_review:
            errors.append("high/critical recommended visual actions require human review")
    if receipt.diagnosis_verdict in {"VISUAL_DIAGNOSIS_REQUIRES_REVIEW", "VISUAL_DIAGNOSIS_CRITICAL_BLOCKER"} and not any(a.requires_human_review for a in receipt.recommended_actions):
        errors.append("review/blocker diagnosis requires at least one human-review action")
    return tuple(errors)


def write_visual_diagnosis_receipt(workspace_root: str | Path, receipt: VisualDiagnosisReceipt, *, report_dir: str = DEFAULT_REPORT_DIR) -> Path:
    root = Path(workspace_root).resolve()
    out = root / report_dir
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{receipt.receipt_id}.visual_diagnosis_receipt.json"
    path.write_text(json.dumps(_to_jsonable(receipt), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def format_visual_diagnosis_summary(receipt: VisualDiagnosisReceipt) -> str:
    return "\n".join([
        f"version: {receipt.version}",
        f"receipt_id: {receipt.receipt_id}",
        f"target: {receipt.target}",
        f"observation_packet_ids: {len(receipt.observation_packet_ids)}",
        f"diagnostic_findings: {len(receipt.diagnostic_findings)}",
        f"recommended_actions: {len(receipt.recommended_actions)}",
        f"harness_stage: {receipt.harness_plan.stage}",
        f"authority_scope: {receipt.authority_scope}",
        f"diagnosis_verdict: {receipt.diagnosis_verdict}",
        f"production_authority: {receipt.production_authority}",
    ])


def _diagnosis_verdict(findings: tuple[VisualDiagnosisFinding, ...], actions: tuple[VisualDiagnosisAction, ...], plan: BrowserHarnessPlan) -> str:
    if any(f.severity == "CRITICAL" for f in findings):
        return "VISUAL_DIAGNOSIS_CRITICAL_BLOCKER"
    if any(f.severity == "HIGH" for f in findings) or any(a.risk_level in {"HIGH", "CRITICAL"} for a in actions):
        return "VISUAL_DIAGNOSIS_REQUIRES_REVIEW"
    if findings or actions:
        return "VISUAL_DIAGNOSIS_ACTIONABLE"
    if plan.stage == "PLAN_ONLY":
        return "BROWSER_HARNESS_PLAN_RECORDED"
    return "VISUAL_DIAGNOSIS_RECORDED"


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


def _scenario(name: str) -> VisualDiagnosisReceipt:
    t = "2026-04-25T06:45:00+00:00"
    if name == "plan":
        return build_visual_diagnosis_receipt(target="local browser preview", harness_plan=build_browser_harness_plan(emitted_at=t), emitted_at=t)
    if name == "review":
        finding = make_visual_diagnosis_finding("account_sensitive_boundary", "Requested visual workflow crosses into credential-sensitive browser action.", severity="HIGH", confidence="HIGH", evidence_refs=["visual://observation/high-risk"])
        action = make_visual_diagnosis_action("request_steward_review", "Keep the agent at observe/report authority until explicit review.", risk_level="HIGH", requires_human_review=True, steward_review_reason="account-sensitive workflow boundary")
        return build_visual_diagnosis_receipt(target="browser workflow", observation_packet_ids=["visual_packet_high_risk"], diagnostic_findings=[finding], recommended_actions=[action], emitted_at=t)
    finding = make_visual_diagnosis_finding("layout_regression", "The right panel overlaps the simulation canvas at 1366px width.", severity="MEDIUM", confidence="HIGH", evidence_refs=["screenshot://before", "dom://snapshot"], affected_surfaces=["simulation_canvas", "right_control_panel"])
    action = make_visual_diagnosis_action("implementation_patch_request", "Move secondary controls into a collapsible drawer and re-check at 1366px and 1440px.", risk_level="LOW", implementation_agent_hint="frontend_layout_agent")
    return build_visual_diagnosis_receipt(target="simulation interface", observation_packet_ids=["visual_packet_layout_001"], screenshot_refs=["screenshot://before"], dom_refs=["dom://snapshot"], before_refs=["screenshot://before"], diagnostic_findings=[finding], recommended_actions=[action], emitted_at=t)


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create V45 visual diagnosis receipt and browser harness plan.")
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--scenario", choices=["plan", "diagnose", "review"], default="diagnose")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    receipt = _scenario(args.scenario)
    errors = validate_visual_diagnosis_receipt(receipt)
    if args.write:
        print(f"receipt_path: {write_visual_diagnosis_receipt(args.workspace_root, receipt)}")
    print(format_visual_diagnosis_summary(receipt))
    if errors:
        print("errors:")
        for error in errors:
            print(f"- {error}")
        return 2
    return 0

if __name__ == "__main__":
    raise SystemExit(_main())
