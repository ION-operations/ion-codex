"""V66 JOC synthetic synthesis and route-result preview view model.

This module binds V65 synthetic response capture/extraction receipt preview to
a non-executing synthesis and route-result preview. It deliberately does not
claim real provider output, consensus truth, memory writes, graph writes,
browser mutation, external model calls, or production authority.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Literal, Mapping

VERSION = "V66_SYNTHETIC_SYNTHESIS_AND_ROUTE_RESULT_PREVIEW"
AUTHORITY_SCOPE = "SYNTHETIC_SYNTHESIS_ROUTE_RESULT_VIEW_MODEL_RECEIPT_ONLY"

SynthesisVerdict = Literal[
    "SYNTHETIC_SYNTHESIS_PREVIEW_READY",
    "BLOCKED_CAPTURE_NOT_READY",
    "BLOCKED_MISSING_SYNTHESIS_EVIDENCE",
    "BLOCKED_FORBIDDEN_ROUTE_CAPABILITY",
    "BLOCKED_LIVE_SYNTHESIS_REQUESTED",
    "BLOCKED_ROUTE_RESULT_MUTATION_REQUESTED",
    "BLOCKED_INVALID_SYNTHETIC_RECEIPT",
]
ExecutionMode = Literal["SYNTHESIS_ROUTE_PREVIEW_ONLY", "VIEW_ONLY_BLOCKED"]

REQUIRED_UPSTREAM_CAPTURE_VERDICTS = {"SYNTHETIC_RESPONSE_CAPTURE_PREVIEW_READY"}
REQUIRED_UPSTREAM_EXECUTION_MODES = {"CAPTURE_PREVIEW_ONLY"}

REQUIRED_VIEW_SURFACES = (
    "SYNTHETIC_SYNTHESIS_PREVIEW_PANEL",
    "ROUTE_RESULT_PREVIEW_RAIL",
    "EXTRACTION_RECEIPT_LINK",
    "NO_CONSENSUS_TRUTH_STRIP",
    "NO_MEMORY_WRITE_STRIP",
    "NO_GRAPH_COMMIT_STRIP",
    "FOLLOWUP_DRAFT_PREVIEW",
    "OPERATOR_REVIEW_NEXT_ACTION",
)

REQUIRED_SYNTHESIS_FLAGS = (
    "synthetic_source_only",
    "single_provider_preview",
    "no_consensus_claim",
    "no_memory_write",
    "no_graph_commit",
    "operator_visible",
)

FORBIDDEN_ROUTE_CAPABILITIES = {
    "live_external_model_dispatch": False,
    "real_provider_output_claim": False,
    "consensus_truth_claim": False,
    "memory_write": False,
    "canonical_graph_write": False,
    "source_summary_rewrite": False,
    "browser_session_mutation": False,
    "credential_access": False,
    "form_submission": False,
    "paid_cloud_launch": False,
    "unrestricted_agent_activation": False,
    "production_authority": False,
}

ALLOWED_ROUTE_PREVIEW_ACTIONS = (
    "SHOW_SYNTHESIS_PREVIEW",
    "SHOW_DISAGREEMENT_PLACEHOLDER",
    "CREATE_FOLLOWUP_DRAFT_PREVIEW",
    "ROUTE_TO_OPERATOR_REVIEW_PREVIEW",
    "STORE_MEMORY_DRY_RUN_PREVIEW",
)


@dataclass(frozen=True)
class SyntheticSynthesisRouteInput:
    mission_id: str
    capture_ref: str
    capture_verdict: str
    upstream_execution_mode: str
    extraction_receipt_preview_id: str
    selected_target: str
    provider_id: str
    provider_adapter: str
    synthetic_extracted_text: str
    extraction_quality_flags: Mapping[str, bool]
    synthesis_flags: Mapping[str, bool]
    evidence_refs: List[str]
    governor_snapshot_refs: List[str]
    route_preview_actions: List[str]
    followup_prompt_preview: str
    live_synthesis_requested: bool = False
    route_result_mutation_requested: bool = False
    view_surfaces: List[str] = field(default_factory=lambda: list(REQUIRED_VIEW_SURFACES))
    blocked_capabilities: Mapping[str, bool] = field(default_factory=lambda: FORBIDDEN_ROUTE_CAPABILITIES.copy())


@dataclass(frozen=True)
class SyntheticSynthesisPreview:
    synthesis_id: str
    mission_id: str
    provider_id: str
    selected_target: str
    synthetic: bool
    consensus_truth_claim: bool
    summary_preview: str
    agreement_points: List[str]
    disagreement_points: List[str]
    confidence_band: str
    evidence_refs: List[str]
    synthesis_flags: Mapping[str, bool]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RouteResultPreview:
    route_result_preview_id: str
    mission_id: str
    allowed_preview_actions: List[str]
    forbidden_mutations: Mapping[str, bool]
    followup_prompt_preview: str
    next_required_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SyntheticSynthesisRouteResultViewModel:
    version: str
    mission_id: str
    capture_ref: str
    capture_verdict: str
    extraction_receipt_preview_id: str
    selected_target: str
    provider_id: str
    provider_adapter: str
    synthesis_verdict: SynthesisVerdict
    authority_scope: str
    execution_mode: ExecutionMode
    synthetic_extracted_text: str
    synthesis_preview: Mapping[str, Any]
    route_result_preview: Mapping[str, Any]
    route_preview_actions: List[str]
    view_surfaces: List[str]
    evidence_refs: List[str]
    governor_snapshot_refs: List[str]
    extraction_quality_flags: Mapping[str, bool]
    synthesis_flags: Mapping[str, bool]
    blocked_capabilities: Mapping[str, bool]
    operator_reason: str
    next_required_action: str
    production_authority: bool = False
    live_dispatch_claim: bool = False
    external_model_call_authorized: bool = False
    browser_session_mutation_authorized: bool = False
    credential_access_authorized: bool = False
    memory_write_authorized: bool = False
    canonical_graph_write_authorized: bool = False
    source_summary_rewrite_authorized: bool = False
    real_provider_output_claim: bool = False
    consensus_truth_claim: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _missing(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def _forbidden_findings(blocked: Mapping[str, bool]) -> List[str]:
    findings: List[str] = []
    for key, expected in FORBIDDEN_ROUTE_CAPABILITIES.items():
        if blocked.get(key) is not expected:
            findings.append(f"forbidden route capability {key!r} expected {expected!r} got {blocked.get(key)!r}")
    for key, value in blocked.items():
        if value is not False:
            findings.append(f"route capability {key!r} is not blocked")
    return findings


def _synthesis_flag_findings(flags: Mapping[str, bool]) -> List[str]:
    findings: List[str] = []
    for key in REQUIRED_SYNTHESIS_FLAGS:
        if flags.get(key) is not True:
            findings.append(f"synthesis_flag_{key}_must_be_true")
    return findings


def _route_action_findings(actions: List[str]) -> List[str]:
    allowed = set(ALLOWED_ROUTE_PREVIEW_ACTIONS)
    return [f"route_action_{action}_not_allowed" for action in actions if action not in allowed]


def _summarize(text: str) -> str:
    clean = " ".join(str(text).split())
    if not clean:
        return ""
    if len(clean) <= 360:
        return clean
    return clean[:357].rstrip() + "..."


def build_synthetic_synthesis_route_result_view_model(
    data: SyntheticSynthesisRouteInput | Mapping[str, Any]
) -> SyntheticSynthesisRouteResultViewModel:
    if isinstance(data, Mapping):
        data = SyntheticSynthesisRouteInput(**dict(data))

    missing = [name for name in (
        "mission_id", "capture_ref", "capture_verdict", "upstream_execution_mode",
        "extraction_receipt_preview_id", "selected_target", "provider_id",
        "provider_adapter", "synthetic_extracted_text", "followup_prompt_preview",
    ) if _missing(getattr(data, name))]
    if not data.evidence_refs:
        missing.append("evidence_refs")
    if not data.governor_snapshot_refs:
        missing.append("governor_snapshot_refs")
    if not data.route_preview_actions:
        missing.append("route_preview_actions")
    if not data.extraction_quality_flags:
        missing.append("extraction_quality_flags")
    if not data.synthesis_flags:
        missing.append("synthesis_flags")

    forbidden_findings = _forbidden_findings(data.blocked_capabilities)
    synthesis_findings = _synthesis_flag_findings(data.synthesis_flags)
    route_findings = _route_action_findings(list(data.route_preview_actions))

    if data.live_synthesis_requested:
        verdict: SynthesisVerdict = "BLOCKED_LIVE_SYNTHESIS_REQUESTED"
        execution: ExecutionMode = "VIEW_ONLY_BLOCKED"
        reason = "Live synthesis was requested; V66 renders synthetic synthesis and route-result preview only."
        next_action = "Route to a future live synthesis authority branch; do not call providers or synthesis services."
    elif data.route_result_mutation_requested:
        verdict = "BLOCKED_ROUTE_RESULT_MUTATION_REQUESTED"
        execution = "VIEW_ONLY_BLOCKED"
        reason = "A route-result mutation was requested; V66 cannot write memory, graph, docs, or external routes."
        next_action = "Keep result routing in preview mode until a later route commit authority branch exists."
    elif missing:
        verdict = "BLOCKED_MISSING_SYNTHESIS_EVIDENCE"
        execution = "VIEW_ONLY_BLOCKED"
        reason = "Missing synthesis preview evidence: " + ", ".join(missing) + "."
        next_action = "Attach V65 extraction preview, quality flags, governor snapshots, and route preview actions."
    elif data.capture_verdict not in REQUIRED_UPSTREAM_CAPTURE_VERDICTS:
        verdict = "BLOCKED_CAPTURE_NOT_READY"
        execution = "VIEW_ONLY_BLOCKED"
        reason = f"Capture verdict {data.capture_verdict} is not ready for synthesis preview."
        next_action = "Return to V65 synthetic response capture preview."
    elif data.upstream_execution_mode not in REQUIRED_UPSTREAM_EXECUTION_MODES:
        verdict = "BLOCKED_CAPTURE_NOT_READY"
        execution = "VIEW_ONLY_BLOCKED"
        reason = f"Upstream execution mode {data.upstream_execution_mode} is not supported by V66."
        next_action = "Require V65 CAPTURE_PREVIEW_ONLY before synthesis preview."
    elif forbidden_findings:
        verdict = "BLOCKED_FORBIDDEN_ROUTE_CAPABILITY"
        execution = "VIEW_ONLY_BLOCKED"
        reason = "Forbidden route capability evidence detected: " + ", ".join(forbidden_findings) + "."
        next_action = "Remove live/provider/memory/graph/source/browser/credential authority from the route preview."
    elif synthesis_findings or route_findings:
        verdict = "BLOCKED_INVALID_SYNTHETIC_RECEIPT"
        execution = "VIEW_ONLY_BLOCKED"
        reason = "Synthetic synthesis flags or route actions invalid: " + ", ".join(synthesis_findings + route_findings) + "."
        next_action = "Mark the synthesis as synthetic-only and restrict route actions to preview actions."
    else:
        verdict = "SYNTHETIC_SYNTHESIS_PREVIEW_READY"
        execution = "SYNTHESIS_ROUTE_PREVIEW_ONLY"
        reason = "Synthetic extraction may be rendered as a non-truth synthesis and route-result preview only."
        next_action = "Show synthesis preview and route-result rail. Future route commit requires separate authority."

    summary = _summarize(data.synthetic_extracted_text)
    synthesis = SyntheticSynthesisPreview(
        synthesis_id=f"SYNTHETIC_SYNTHESIS_PREVIEW:{data.mission_id}",
        mission_id=data.mission_id,
        provider_id=data.provider_id,
        selected_target=data.selected_target,
        synthetic=True,
        consensus_truth_claim=False,
        summary_preview=summary,
        agreement_points=["Synthetic payload is shaped correctly for cockpit rendering."],
        disagreement_points=["No cross-provider disagreement can be claimed from a single synthetic payload."],
        confidence_band="PREVIEW_ONLY_NOT_TRUTH",
        evidence_refs=list(data.evidence_refs),
        synthesis_flags=dict(data.synthesis_flags),
    ).to_dict()

    route_result = RouteResultPreview(
        route_result_preview_id=f"ROUTE_RESULT_PREVIEW:{data.mission_id}",
        mission_id=data.mission_id,
        allowed_preview_actions=list(data.route_preview_actions),
        forbidden_mutations=dict(data.blocked_capabilities),
        followup_prompt_preview=data.followup_prompt_preview,
        next_required_action=next_action,
    ).to_dict()

    return SyntheticSynthesisRouteResultViewModel(
        version=VERSION,
        mission_id=data.mission_id,
        capture_ref=data.capture_ref,
        capture_verdict=data.capture_verdict,
        extraction_receipt_preview_id=data.extraction_receipt_preview_id,
        selected_target=data.selected_target,
        provider_id=data.provider_id,
        provider_adapter=data.provider_adapter,
        synthesis_verdict=verdict,
        authority_scope=AUTHORITY_SCOPE,
        execution_mode=execution,
        synthetic_extracted_text=data.synthetic_extracted_text,
        synthesis_preview=synthesis,
        route_result_preview=route_result,
        route_preview_actions=list(data.route_preview_actions),
        view_surfaces=list(data.view_surfaces),
        evidence_refs=list(data.evidence_refs),
        governor_snapshot_refs=list(data.governor_snapshot_refs),
        extraction_quality_flags=dict(data.extraction_quality_flags),
        synthesis_flags=dict(data.synthesis_flags),
        blocked_capabilities=dict(data.blocked_capabilities),
        operator_reason=reason,
        next_required_action=next_action,
    )


def build_fixture_synthetic_synthesis_route_input(**overrides: Any) -> SyntheticSynthesisRouteInput:
    base = SyntheticSynthesisRouteInput(
        mission_id="M-066",
        capture_ref="V65_SYNTHETIC_CAPTURE:M-065",
        capture_verdict="SYNTHETIC_RESPONSE_CAPTURE_PREVIEW_READY",
        upstream_execution_mode="CAPTURE_PREVIEW_ONLY",
        extraction_receipt_preview_id="SYNTHETIC_EXTRACTION_RECEIPT:M-065",
        selected_target="gemini-cli",
        provider_id="gemini",
        provider_adapter="GeminiCLIDriver.NOOP",
        synthetic_extracted_text=(
            "Synthetic response preview: no provider was contacted. This payload exists only to show how "
            "extraction receipts, synthesis preview, and route-result rails will render in the cockpit."
        ),
        extraction_quality_flags={
            "synthetic_payload": True,
            "no_provider_origin": True,
            "no_network_call": True,
            "not_model_truth": True,
            "operator_visible": True,
        },
        synthesis_flags={
            "synthetic_source_only": True,
            "single_provider_preview": True,
            "no_consensus_claim": True,
            "no_memory_write": True,
            "no_graph_commit": True,
            "operator_visible": True,
        },
        evidence_refs=["V65_SYNTHETIC_EXTRACTION_RECEIPT:M-065", "V65_QUALITY_FLAGS:synthetic"],
        governor_snapshot_refs=["V58_BUDGET_GOVERNOR:ok", "V58_API_RATE_GOVERNOR:ok"],
        route_preview_actions=[
            "SHOW_SYNTHESIS_PREVIEW",
            "CREATE_FOLLOWUP_DRAFT_PREVIEW",
            "ROUTE_TO_OPERATOR_REVIEW_PREVIEW",
            "STORE_MEMORY_DRY_RUN_PREVIEW",
        ],
        followup_prompt_preview="Ask the selected provider for a real answer only after live execution authority is granted.",
    )
    values = asdict(base)
    values.update(overrides)
    return SyntheticSynthesisRouteInput(**values)


def validate_synthetic_synthesis_route_result_view_model(model: SyntheticSynthesisRouteResultViewModel) -> Dict[str, Any]:
    findings: List[str] = []
    if model.version != VERSION:
        findings.append("invalid_version")
    if model.authority_scope != AUTHORITY_SCOPE:
        findings.append("invalid_authority_scope")
    if model.production_authority:
        findings.append("production_authority_must_be_false")
    if model.live_dispatch_claim:
        findings.append("live_dispatch_claim_must_be_false")
    if model.external_model_call_authorized:
        findings.append("external_model_call_authorized_must_be_false")
    if model.browser_session_mutation_authorized:
        findings.append("browser_session_mutation_authorized_must_be_false")
    if model.credential_access_authorized:
        findings.append("credential_access_authorized_must_be_false")
    if model.memory_write_authorized:
        findings.append("memory_write_authorized_must_be_false")
    if model.canonical_graph_write_authorized:
        findings.append("canonical_graph_write_authorized_must_be_false")
    if model.source_summary_rewrite_authorized:
        findings.append("source_summary_rewrite_authorized_must_be_false")
    if model.real_provider_output_claim:
        findings.append("real_provider_output_claim_must_be_false")
    if model.consensus_truth_claim:
        findings.append("consensus_truth_claim_must_be_false")

    missing_surfaces = [surface for surface in REQUIRED_VIEW_SURFACES if surface not in model.view_surfaces]
    if missing_surfaces:
        findings.append("missing_view_surfaces:" + ",".join(missing_surfaces))

    findings.extend(_forbidden_findings(model.blocked_capabilities))
    findings.extend(_synthesis_flag_findings(model.synthesis_flags))
    findings.extend(_route_action_findings(model.route_preview_actions))

    if model.synthesis_verdict == "SYNTHETIC_SYNTHESIS_PREVIEW_READY" and model.execution_mode != "SYNTHESIS_ROUTE_PREVIEW_ONLY":
        findings.append("ready_state_requires_synthesis_route_preview_only")
    if model.synthesis_verdict.startswith("BLOCKED") and model.execution_mode != "VIEW_ONLY_BLOCKED":
        findings.append("blocked_state_requires_view_only_blocked")

    synthesis = model.synthesis_preview or {}
    if synthesis.get("consensus_truth_claim") is not False:
        findings.append("synthesis_preview_consensus_truth_claim_must_be_false")
    if synthesis.get("synthetic") is not True:
        findings.append("synthesis_preview_must_be_synthetic")

    return {
        "version": VERSION,
        "validation_verdict": "VALID_SYNTHETIC_SYNTHESIS_ROUTE_RESULT_VIEW_MODEL" if not findings else "INVALID_SYNTHETIC_SYNTHESIS_ROUTE_RESULT_VIEW_MODEL",
        "authority_scope": AUTHORITY_SCOPE,
        "synthesis_verdict": model.synthesis_verdict,
        "execution_mode": model.execution_mode,
        "provider_id": model.provider_id,
        "provider_adapter": model.provider_adapter,
        "selected_target": model.selected_target,
        "view_surface_count": len(model.view_surfaces),
        "route_preview_action_count": len(model.route_preview_actions),
        "synthesis_flag_count": len(model.synthesis_flags),
        "synthesis_id": model.synthesis_preview.get("synthesis_id"),
        "route_result_preview_id": model.route_result_preview.get("route_result_preview_id"),
        "findings": findings,
        "production_authority": False,
        "live_dispatch_claim": False,
        "external_model_call_authorized": False,
        "memory_write_authorized": False,
        "canonical_graph_write_authorized": False,
        "real_provider_output_claim": False,
        "consensus_truth_claim": False,
    }


if __name__ == "__main__":
    model = build_synthetic_synthesis_route_result_view_model(build_fixture_synthetic_synthesis_route_input())
    print(model.to_dict())
    print(validate_synthetic_synthesis_route_result_view_model(model))
