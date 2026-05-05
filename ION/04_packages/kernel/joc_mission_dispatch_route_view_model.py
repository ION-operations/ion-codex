"""V59 ION/JOC Mission Dispatch and Model Route view-model verifier.

This module validates a UI-facing route preview for mission dispatch. It does
not dispatch prompts, call model APIs, mutate browser sessions, access
credentials, launch cloud resources, or grant production authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

SCHEMA_ID = "ion.joc_mission_dispatch_route_view_model.v1"
VERSION = "V59_MISSION_DISPATCH_AND_MODEL_ROUTE_VIEW_MODEL"
AUTHORITY_SCOPE = "MISSION_DISPATCH_ROUTE_VIEW_MODEL_RECEIPT_ONLY"
DEFAULT_REPORT_DIR = "ION/05_context/history/joc_mission_dispatch_route_view_model_receipts"

REQUIRED_VIEW_SURFACES = (
    "MISSION_DISPATCH_PANEL",
    "MODEL_ROUTE_MATRIX",
    "COMPUTE_RING_SELECTOR",
    "COST_LATENCY_QUALITY_BAND",
    "CAPABILITY_MATCH_PANEL",
    "FALLBACK_CHAIN_PANEL",
    "HUMAN_APPROVAL_GATE",
    "DISPATCH_RECEIPT_PREVIEW",
)

REQUIRED_COMPUTE_RINGS = (
    "RING_1_BROWSER_SESSION",
    "RING_2_API_CLI_LOCAL",
    "RING_3_CLOUD_COMPUTE",
)

REQUIRED_ROUTE_FACTORS = (
    "TASK_CLASS",
    "CONTEXT_SIZE",
    "QUALITY_REQUIREMENT",
    "LATENCY_REQUIREMENT",
    "COST_SENSITIVITY",
    "CAPABILITY_MATCH",
    "RISK_CLASS",
    "FALLBACK_AVAILABILITY",
)

ALLOWED_TARGET_STATUSES = (
    "PRIMARY_RECOMMENDED",
    "FALLBACK_READY",
    "SUPERVISED_ONLY",
    "BLOCKED",
)

ALLOWED_ACCESS_METHODS = (
    "browser",
    "api",
    "cli",
    "local",
    "cloud_vm",
)

ALLOWED_VERDICTS = (
    "ROUTE_PREVIEW_READY",
    "BLOCKED_NO_TARGETS",
    "BLOCKED_MISSING_REQUIRED_RING",
    "BLOCKED_MISSING_ROUTE_FACTOR",
    "BLOCKED_MISSING_VIEW_SURFACE",
    "BLOCKED_UNAPPROVED_EXTERNAL_DISPATCH",
    "BLOCKED_FORBIDDEN_CAPABILITY",
)

FORBIDDEN_CAPABILITIES = {
    "production_authority": False,
    "live_external_model_dispatch": False,
    "browser_session_mutation": False,
    "credential_access": False,
    "form_submission": False,
    "paid_cloud_launch": False,
    "source_summary_rewrite": False,
    "canonical_graph_write": False,
    "unrestricted_agent_activation": False,
}


@dataclass(frozen=True)
class RouteTarget:
    target_id: str
    display_name: str
    compute_ring: str
    access_method: str
    status: str
    capability_tags: tuple[str, ...]
    cost_band: str
    latency_band: str
    quality_band: str
    risk_notes: tuple[str, ...] = tuple()


@dataclass(frozen=True)
class RouteFactor:
    factor_id: str
    value: str
    rationale: str


@dataclass(frozen=True)
class DispatchRouteCandidate:
    mission_id: str
    mission_title: str
    task_class: str
    context_route_ref: str
    primary_target: RouteTarget | None
    fallback_targets: tuple[RouteTarget, ...]
    route_factors: tuple[RouteFactor, ...]
    view_surfaces: tuple[str, ...]
    approval_gate: str
    route_reasoning: str
    dispatch_receipt_preview: str
    blocked_capabilities: Mapping[str, bool] = field(default_factory=lambda: FORBIDDEN_CAPABILITIES.copy())


@dataclass(frozen=True)
class MissionDispatchRouteReceipt:
    version: str
    schema_id: str
    receipt_id: str
    generated_at: str
    authority_scope: str
    route_verdict: str
    mission_id: str
    mission_title: str
    task_class: str
    context_route_ref: str
    target_count: int
    compute_ring_count: int
    route_factor_count: int
    view_surface_count: int
    primary_target: Mapping[str, Any] | None
    fallback_targets: tuple[Mapping[str, Any], ...]
    route_factors: tuple[Mapping[str, Any], ...]
    view_surfaces: tuple[str, ...]
    approval_gate: str
    estimated_cost_band: str
    estimated_latency_band: str
    quality_band: str
    route_reasoning: str
    dispatch_receipt_preview: str
    findings: tuple[str, ...]
    forbidden_capabilities: Mapping[str, bool]
    production_authority: bool = False
    live_dispatch_claim: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _hash_payload(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()[:24]


def _target_to_dict(target: RouteTarget | None) -> dict[str, Any] | None:
    return None if target is None else asdict(target)


def _all_targets(candidate: DispatchRouteCandidate) -> tuple[RouteTarget, ...]:
    if candidate.primary_target is None:
        return candidate.fallback_targets
    return (candidate.primary_target,) + candidate.fallback_targets


def _band_summary(candidate: DispatchRouteCandidate, attr: str) -> str:
    primary = candidate.primary_target
    if primary is None:
        return "UNKNOWN"
    return str(getattr(primary, attr))


def _validate_forbidden(candidate: DispatchRouteCandidate) -> tuple[str, ...]:
    findings: list[str] = []
    for key, expected in FORBIDDEN_CAPABILITIES.items():
        actual = candidate.blocked_capabilities.get(key)
        if actual is not expected:
            findings.append(f"forbidden capability {key!r} expected {expected!r} got {actual!r}")
    for key, value in candidate.blocked_capabilities.items():
        if value is not False:
            findings.append(f"capability {key!r} is not blocked")
    return tuple(findings)


def validate_dispatch_route(candidate: DispatchRouteCandidate) -> MissionDispatchRouteReceipt:
    findings: list[str] = []
    route_verdict = "ROUTE_PREVIEW_READY"
    targets = _all_targets(candidate)

    if not targets:
        findings.append("no dispatch targets are present")
        route_verdict = "BLOCKED_NO_TARGETS"

    target_rings = {target.compute_ring for target in targets}
    missing_rings = [ring for ring in REQUIRED_COMPUTE_RINGS if ring not in target_rings]
    if missing_rings:
        findings.append("missing required compute rings: " + ", ".join(missing_rings))
        route_verdict = "BLOCKED_MISSING_REQUIRED_RING"

    factor_ids = {factor.factor_id for factor in candidate.route_factors}
    missing_factors = [factor for factor in REQUIRED_ROUTE_FACTORS if factor not in factor_ids]
    if missing_factors:
        findings.append("missing required route factors: " + ", ".join(missing_factors))
        route_verdict = "BLOCKED_MISSING_ROUTE_FACTOR"

    missing_surfaces = [surface for surface in REQUIRED_VIEW_SURFACES if surface not in candidate.view_surfaces]
    if missing_surfaces:
        findings.append("missing required view surfaces: " + ", ".join(missing_surfaces))
        route_verdict = "BLOCKED_MISSING_VIEW_SURFACE"

    for target in targets:
        if target.compute_ring not in REQUIRED_COMPUTE_RINGS:
            findings.append(f"target {target.target_id!r} has invalid compute ring {target.compute_ring!r}")
        if target.access_method not in ALLOWED_ACCESS_METHODS:
            findings.append(f"target {target.target_id!r} has invalid access method {target.access_method!r}")
        if target.status not in ALLOWED_TARGET_STATUSES:
            findings.append(f"target {target.target_id!r} has invalid status {target.status!r}")
        if not target.capability_tags:
            findings.append(f"target {target.target_id!r} has no capability tags")

    if candidate.primary_target is None:
        findings.append("primary target is missing")
        route_verdict = "BLOCKED_NO_TARGETS"
    elif candidate.primary_target.status != "PRIMARY_RECOMMENDED":
        findings.append("primary target is not marked PRIMARY_RECOMMENDED")

    if candidate.approval_gate != "SUPERVISED_APPROVAL_REQUIRED":
        findings.append("approval gate must be SUPERVISED_APPROVAL_REQUIRED before live dispatch")
        route_verdict = "BLOCKED_UNAPPROVED_EXTERNAL_DISPATCH"

    if not candidate.context_route_ref.strip():
        findings.append("context route reference is empty")
    if not candidate.route_reasoning.strip():
        findings.append("route reasoning is empty")
    if not candidate.dispatch_receipt_preview.strip():
        findings.append("dispatch receipt preview is empty")

    forbidden_findings = _validate_forbidden(candidate)
    if forbidden_findings:
        findings.extend(forbidden_findings)
        route_verdict = "BLOCKED_FORBIDDEN_CAPABILITY"

    payload_for_id = {
        "mission_id": candidate.mission_id,
        "task_class": candidate.task_class,
        "primary_target": _target_to_dict(candidate.primary_target),
        "fallback_targets": [asdict(target) for target in candidate.fallback_targets],
        "route_factors": [asdict(factor) for factor in candidate.route_factors],
        "view_surfaces": list(candidate.view_surfaces),
        "findings": findings,
    }

    return MissionDispatchRouteReceipt(
        version=VERSION,
        schema_id=SCHEMA_ID,
        receipt_id=_hash_payload(payload_for_id),
        generated_at=datetime.now(timezone.utc).isoformat(),
        authority_scope=AUTHORITY_SCOPE,
        route_verdict=route_verdict,
        mission_id=candidate.mission_id,
        mission_title=candidate.mission_title,
        task_class=candidate.task_class,
        context_route_ref=candidate.context_route_ref,
        target_count=len(targets),
        compute_ring_count=len(target_rings),
        route_factor_count=len(factor_ids),
        view_surface_count=len(set(candidate.view_surfaces)),
        primary_target=_target_to_dict(candidate.primary_target),
        fallback_targets=tuple(asdict(target) for target in candidate.fallback_targets),
        route_factors=tuple(asdict(factor) for factor in candidate.route_factors),
        view_surfaces=tuple(candidate.view_surfaces),
        approval_gate=candidate.approval_gate,
        estimated_cost_band=_band_summary(candidate, "cost_band"),
        estimated_latency_band=_band_summary(candidate, "latency_band"),
        quality_band=_band_summary(candidate, "quality_band"),
        route_reasoning=candidate.route_reasoning,
        dispatch_receipt_preview=candidate.dispatch_receipt_preview,
        findings=tuple(findings),
        forbidden_capabilities=dict(candidate.blocked_capabilities),
        production_authority=False,
        live_dispatch_claim=False,
    )


def build_demo_candidate() -> DispatchRouteCandidate:
    primary = RouteTarget(
        target_id="target.gpt.reasoning_supervised",
        display_name="GPT reasoning lane",
        compute_ring="RING_2_API_CLI_LOCAL",
        access_method="api",
        status="PRIMARY_RECOMMENDED",
        capability_tags=("architectural_reasoning", "code_review", "receipt_synthesis"),
        cost_band="MEDIUM",
        latency_band="INTERACTIVE_SECONDS",
        quality_band="HIGH",
        risk_notes=("requires supervised approval before live dispatch",),
    )
    fallbacks = (
        RouteTarget(
            target_id="target.browser.chatgpt_manual",
            display_name="ChatGPT browser session",
            compute_ring="RING_1_BROWSER_SESSION",
            access_method="browser",
            status="SUPERVISED_ONLY",
            capability_tags=("interactive_chat", "visual_session_context", "manual_injection"),
            cost_band="SUBSCRIPTION_INCLUDED",
            latency_band="INTERACTIVE_10_60S",
            quality_band="HIGH_VARIANT",
            risk_notes=("browser mutation remains blocked in V59",),
        ),
        RouteTarget(
            target_id="target.local.small_classifier",
            display_name="Local small-model classifier",
            compute_ring="RING_2_API_CLI_LOCAL",
            access_method="local",
            status="FALLBACK_READY",
            capability_tags=("classification", "cheap_triage", "privacy_preserving"),
            cost_band="FREE_LOCAL",
            latency_band="LOW_SECONDS",
            quality_band="BOUNDED_LOW_RISK",
        ),
        RouteTarget(
            target_id="target.vertex.heavy_cloud",
            display_name="Cloud heavy compute lane",
            compute_ring="RING_3_CLOUD_COMPUTE",
            access_method="cloud_vm",
            status="SUPERVISED_ONLY",
            capability_tags=("heavy_simulation", "large_batch", "future_training"),
            cost_band="HIGH_PAID_APPROVAL_REQUIRED",
            latency_band="MINUTES_TO_HOURS",
            quality_band="SPECIALIZED_HEAVY",
            risk_notes=("paid launch remains blocked without explicit operator approval",),
        ),
    )
    factors = (
        RouteFactor("TASK_CLASS", "UI_ARCHITECTURE_AND_RUNTIME_VIEW_MODEL", "The mission asks for ION/JOC UI-runtime synthesis and scaffold work."),
        RouteFactor("CONTEXT_SIZE", "MEDIUM_PROJECT_ROUTE", "V58 selected exact files and citations; no full-repo prompt is needed."),
        RouteFactor("QUALITY_REQUIREMENT", "HIGH", "Architecture and runtime law should be handled by a strong reasoning lane."),
        RouteFactor("LATENCY_REQUIREMENT", "INTERACTIVE", "The branch is being developed in a live conversation loop."),
        RouteFactor("COST_SENSITIVITY", "CONTROLLED", "Use already-mounted local/interactive lanes before paid cloud."),
        RouteFactor("CAPABILITY_MATCH", "REASONING_PLUS_CODE_PATCH", "Primary lane must reason about architecture and produce project files/tests."),
        RouteFactor("RISK_CLASS", "C2_DESIGN_CANDIDATE", "Route preview is a design/runtime candidate, not production dispatch."),
        RouteFactor("FALLBACK_AVAILABILITY", "THREE_RING_FALLBACK_VISIBLE", "Browser, local/API/CLI, and cloud lanes are all represented."),
    )
    return DispatchRouteCandidate(
        mission_id="M-V59-ION-JOC-DISPATCH-ROUTE",
        mission_title="Route V58 cognitive context into supervised mission dispatch lanes",
        task_class="UI_ARCHITECTURE_AND_RUNTIME_VIEW_MODEL",
        context_route_ref="V58_COGNITIVE_EXPLORER_ROUTE_VIEW_MODEL_RECEIPT",
        primary_target=primary,
        fallback_targets=fallbacks,
        route_factors=factors,
        view_surfaces=REQUIRED_VIEW_SURFACES,
        approval_gate="SUPERVISED_APPROVAL_REQUIRED",
        route_reasoning=(
            "The V58 route has exact context, so V59 previews a supervised mission dispatch plan. "
            "A high-quality reasoning/code lane is primary; browser, local, and cloud lanes remain visible as "
            "fallbacks without enabling live dispatch."
        ),
        dispatch_receipt_preview=(
            "If approved by a later live driver branch, the dispatch receipt must record mission id, selected target, "
            "context route ref, cost/latency estimate, operator approval, response extraction status, and return routing."
        ),
    )


def write_receipt(receipt: MissionDispatchRouteReceipt, workspace_root: Path | str = ".") -> Path:
    root = Path(workspace_root)
    report_dir = root / DEFAULT_REPORT_DIR
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / f"{receipt.receipt_id}.joc_mission_dispatch_route_view_model_receipt.json"
    path.write_text(json.dumps(receipt.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
    return path


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate V59 ION/JOC mission dispatch route view model.")
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)

    receipt = validate_dispatch_route(build_demo_candidate())
    print(json.dumps(receipt.to_dict(), indent=2, sort_keys=True))
    if args.write:
        path = write_receipt(receipt, args.workspace_root)
        print(f"receipt_written={path}")
    return 0 if receipt.route_verdict == "ROUTE_PREVIEW_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
