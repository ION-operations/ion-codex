"""V65 JOC synthetic response capture and extraction receipt preview view model.

This module binds V64 provider adapter readiness to a synthetic response
capture/extraction receipt preview for cockpit rendering. It is deliberately
non-executing: it cannot call providers, mutate browser sessions, touch
credentials, submit forms, launch paid cloud resources, or grant production
authority.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Literal, Mapping

VERSION = "V65_SYNTHETIC_RESPONSE_CAPTURE_AND_EXTRACTION_RECEIPT_PREVIEW"
AUTHORITY_SCOPE = "SYNTHETIC_RESPONSE_CAPTURE_VIEW_MODEL_RECEIPT_ONLY"

CaptureVerdict = Literal[
    "SYNTHETIC_RESPONSE_CAPTURE_PREVIEW_READY",
    "BLOCKED_PROVIDER_READINESS_NOT_READY",
    "BLOCKED_MISSING_CAPTURE_EVIDENCE",
    "BLOCKED_FORBIDDEN_CAPABILITY",
    "BLOCKED_LIVE_CAPTURE_REQUESTED",
    "BLOCKED_SYNTHETIC_PAYLOAD_INVALID",
]
ExecutionMode = Literal["CAPTURE_PREVIEW_ONLY", "VIEW_ONLY_BLOCKED"]

REQUIRED_UPSTREAM_READINESS_VERDICTS = {"PROVIDER_ADAPTER_READY_FOR_DRY_RUN_SELECTION"}
REQUIRED_UPSTREAM_EXECUTION_MODES = {"READINESS_VIEW_ONLY"}

REQUIRED_VIEW_SURFACES = (
    "SYNTHETIC_RESPONSE_CAPTURE_PANEL",
    "EXTRACTION_RECEIPT_PREVIEW_RAIL",
    "NO_LIVE_PROVIDER_CALL_STRIP",
    "QUALITY_FLAG_LEDGER",
    "PROVIDER_READY_LINK",
    "TRACE_LINEAGE_LINKS",
    "RAW_PAYLOAD_PREVIEW",
    "NEXT_ACTION_CALLOUT",
)

REQUIRED_QUALITY_FLAGS = (
    "synthetic_payload",
    "no_provider_origin",
    "no_network_call",
    "not_model_truth",
    "operator_visible",
)

FORBIDDEN_CAPABILITIES = {
    "live_external_model_dispatch": False,
    "browser_session_mutation": False,
    "credential_access": False,
    "form_submission": False,
    "paid_cloud_launch": False,
    "source_summary_rewrite": False,
    "canonical_graph_write": False,
    "unrestricted_agent_activation": False,
    "production_authority": False,
}


@dataclass(frozen=True)
class SyntheticResponseCaptureInput:
    mission_id: str
    provider_readiness_ref: str
    provider_readiness_verdict: str
    upstream_execution_mode: str
    route_preview_id: str
    selected_target: str
    provider_id: str
    provider_adapter: str
    access_method: str
    compute_ring: str
    dry_run_trace_ref: str
    synthetic_response_payload: Mapping[str, Any]
    extraction_zones: List[Mapping[str, Any]]
    provider_evidence_refs: List[str]
    trace_evidence_refs: List[str]
    governor_snapshot_refs: List[str]
    quality_flags: Mapping[str, bool]
    live_capture_requested: bool = False
    view_surfaces: List[str] = field(default_factory=lambda: list(REQUIRED_VIEW_SURFACES))
    blocked_capabilities: Mapping[str, bool] = field(default_factory=lambda: FORBIDDEN_CAPABILITIES.copy())


@dataclass(frozen=True)
class SyntheticExtractionReceiptPreview:
    receipt_id: str
    mission_id: str
    provider_id: str
    provider_adapter: str
    selected_target: str
    synthetic: bool
    provider_origin_claim: bool
    extracted_text_preview: str
    token_estimate: int
    extraction_zones: List[Mapping[str, Any]]
    evidence_refs: List[str]
    quality_flags: Mapping[str, bool]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SyntheticResponseCaptureViewModel:
    version: str
    mission_id: str
    provider_readiness_ref: str
    route_preview_id: str
    selected_target: str
    provider_id: str
    provider_adapter: str
    access_method: str
    compute_ring: str
    dry_run_trace_ref: str
    capture_verdict: CaptureVerdict
    authority_scope: str
    execution_mode: ExecutionMode
    synthetic_response_payload: Mapping[str, Any]
    extraction_receipt_preview: Mapping[str, Any]
    extraction_zones: List[Mapping[str, Any]]
    view_surfaces: List[str]
    provider_evidence_refs: List[str]
    trace_evidence_refs: List[str]
    governor_snapshot_refs: List[str]
    quality_flags: Mapping[str, bool]
    blocked_capabilities: Mapping[str, bool]
    operator_reason: str
    next_required_action: str
    production_authority: bool = False
    live_dispatch_claim: bool = False
    external_model_call_authorized: bool = False
    browser_session_mutation_authorized: bool = False
    credential_access_authorized: bool = False
    paid_cloud_launch_authorized: bool = False
    provider_origin_claim: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _missing(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def _forbidden_findings(blocked: Mapping[str, bool]) -> List[str]:
    findings: List[str] = []
    for key, expected in FORBIDDEN_CAPABILITIES.items():
        if blocked.get(key) is not expected:
            findings.append(f"forbidden capability {key!r} expected {expected!r} got {blocked.get(key)!r}")
    for key, value in blocked.items():
        if value is not False:
            findings.append(f"capability {key!r} is not blocked")
    return findings


def _payload_findings(payload: Mapping[str, Any]) -> List[str]:
    findings: List[str] = []
    if not payload.get("synthetic"):
        findings.append("payload_must_be_marked_synthetic")
    if payload.get("provider_origin_claim"):
        findings.append("payload_must_not_claim_provider_origin")
    text = payload.get("text")
    if not isinstance(text, str) or not text.strip():
        findings.append("payload_text_required")
    if bool(payload.get("network_call")):
        findings.append("payload_must_not_record_network_call")
    return findings


def _quality_findings(flags: Mapping[str, bool]) -> List[str]:
    findings: List[str] = []
    for key in REQUIRED_QUALITY_FLAGS:
        if flags.get(key) is not True:
            findings.append(f"quality_flag_{key}_must_be_true")
    return findings


def _estimate_tokens(text: str) -> int:
    return max(1, round(len(text.split()) * 1.33))


def build_synthetic_response_capture_view_model(
    data: SyntheticResponseCaptureInput | Mapping[str, Any]
) -> SyntheticResponseCaptureViewModel:
    if isinstance(data, Mapping):
        data = SyntheticResponseCaptureInput(**dict(data))

    missing = [name for name in (
        "mission_id", "provider_readiness_ref", "provider_readiness_verdict",
        "upstream_execution_mode", "route_preview_id", "selected_target",
        "provider_id", "provider_adapter", "access_method", "compute_ring",
        "dry_run_trace_ref",
    ) if _missing(getattr(data, name))]
    if not data.provider_evidence_refs:
        missing.append("provider_evidence_refs")
    if not data.trace_evidence_refs:
        missing.append("trace_evidence_refs")
    if not data.governor_snapshot_refs:
        missing.append("governor_snapshot_refs")
    if not data.extraction_zones:
        missing.append("extraction_zones")
    if not data.synthetic_response_payload:
        missing.append("synthetic_response_payload")

    forbidden_findings = _forbidden_findings(data.blocked_capabilities)
    payload_findings = _payload_findings(data.synthetic_response_payload) if data.synthetic_response_payload else ["payload_missing"]
    quality_findings = _quality_findings(data.quality_flags)

    if data.live_capture_requested:
        verdict: CaptureVerdict = "BLOCKED_LIVE_CAPTURE_REQUESTED"
        execution: ExecutionMode = "VIEW_ONLY_BLOCKED"
        reason = "Live response capture was requested; V65 only renders synthetic capture preview state."
        next_action = "Route to a future live extraction authority branch; do not call provider or read browser output."
    elif missing:
        verdict = "BLOCKED_MISSING_CAPTURE_EVIDENCE"
        execution = "VIEW_ONLY_BLOCKED"
        reason = "Missing synthetic capture evidence: " + ", ".join(missing) + "."
        next_action = "Attach provider readiness, trace, governor, synthetic payload, and extraction-zone evidence."
    elif data.provider_readiness_verdict not in REQUIRED_UPSTREAM_READINESS_VERDICTS:
        verdict = "BLOCKED_PROVIDER_READINESS_NOT_READY"
        execution = "VIEW_ONLY_BLOCKED"
        reason = f"Provider readiness verdict {data.provider_readiness_verdict} is not ready for capture preview."
        next_action = "Return to V64 provider readiness and selector health."
    elif data.upstream_execution_mode not in REQUIRED_UPSTREAM_EXECUTION_MODES:
        verdict = "BLOCKED_PROVIDER_READINESS_NOT_READY"
        execution = "VIEW_ONLY_BLOCKED"
        reason = f"Upstream execution mode {data.upstream_execution_mode} is not supported by V65."
        next_action = "Require V64 READINESS_VIEW_ONLY before synthetic capture preview."
    elif forbidden_findings:
        verdict = "BLOCKED_FORBIDDEN_CAPABILITY"
        execution = "VIEW_ONLY_BLOCKED"
        reason = "Forbidden capability evidence detected: " + ", ".join(forbidden_findings) + "."
        next_action = "Remove live/network/browser/credential/provider authority from the capture model."
    elif payload_findings or quality_findings:
        verdict = "BLOCKED_SYNTHETIC_PAYLOAD_INVALID"
        execution = "VIEW_ONLY_BLOCKED"
        reason = "Synthetic payload or quality flags invalid: " + ", ".join(payload_findings + quality_findings) + "."
        next_action = "Mark payload synthetic, remove provider-origin claims, and show no-network/no-truth flags."
    else:
        verdict = "SYNTHETIC_RESPONSE_CAPTURE_PREVIEW_READY"
        execution = "CAPTURE_PREVIEW_ONLY"
        reason = "Synthetic response capture and extraction receipt may be rendered for non-executing cockpit preview only."
        next_action = "Show extraction preview. Future live capture requires a separate execution authority branch."

    text = str(data.synthetic_response_payload.get("text", "")) if data.synthetic_response_payload else ""
    receipt = SyntheticExtractionReceiptPreview(
        receipt_id=f"SYNTHETIC_EXTRACTION_RECEIPT:{data.mission_id}",
        mission_id=data.mission_id,
        provider_id=data.provider_id,
        provider_adapter=data.provider_adapter,
        selected_target=data.selected_target,
        synthetic=True,
        provider_origin_claim=False,
        extracted_text_preview=text[:420],
        token_estimate=_estimate_tokens(text),
        extraction_zones=list(data.extraction_zones),
        evidence_refs=list(data.provider_evidence_refs) + list(data.trace_evidence_refs),
        quality_flags=dict(data.quality_flags),
    ).to_dict()

    return SyntheticResponseCaptureViewModel(
        version=VERSION,
        mission_id=data.mission_id,
        provider_readiness_ref=data.provider_readiness_ref,
        route_preview_id=data.route_preview_id,
        selected_target=data.selected_target,
        provider_id=data.provider_id,
        provider_adapter=data.provider_adapter,
        access_method=data.access_method,
        compute_ring=data.compute_ring,
        dry_run_trace_ref=data.dry_run_trace_ref,
        capture_verdict=verdict,
        authority_scope=AUTHORITY_SCOPE,
        execution_mode=execution,
        synthetic_response_payload=dict(data.synthetic_response_payload),
        extraction_receipt_preview=receipt,
        extraction_zones=list(data.extraction_zones),
        view_surfaces=list(data.view_surfaces),
        provider_evidence_refs=list(data.provider_evidence_refs),
        trace_evidence_refs=list(data.trace_evidence_refs),
        governor_snapshot_refs=list(data.governor_snapshot_refs),
        quality_flags=dict(data.quality_flags),
        blocked_capabilities=dict(data.blocked_capabilities),
        operator_reason=reason,
        next_required_action=next_action,
    )


def build_fixture_synthetic_response_capture_input(**overrides: Any) -> SyntheticResponseCaptureInput:
    base = SyntheticResponseCaptureInput(
        mission_id="M-065",
        provider_readiness_ref="V64_PROVIDER_READINESS:M-064",
        provider_readiness_verdict="PROVIDER_ADAPTER_READY_FOR_DRY_RUN_SELECTION",
        upstream_execution_mode="READINESS_VIEW_ONLY",
        route_preview_id="route-preview-v59-001",
        selected_target="gemini-cli",
        provider_id="gemini",
        provider_adapter="GeminiCLIDriver.NOOP",
        access_method="cli_noop",
        compute_ring="RING_2_API_CLI_LOCAL",
        dry_run_trace_ref="V63_DRY_RUN_TRACE:M-063",
        synthetic_response_payload={
            "synthetic": True,
            "provider_origin_claim": False,
            "network_call": False,
            "text": "Synthetic response preview: no provider was contacted. This payload exists only to show how extraction receipts will render in the cockpit.",
            "model": "NOOP_SYNTHETIC_MODEL",
        },
        extraction_zones=[
            {"zone_id": "response_text", "selector_class": "noop.synthetic.response", "status": "PREVIEW_READY"},
            {"zone_id": "metadata", "selector_class": "noop.synthetic.metadata", "status": "PREVIEW_READY"},
        ],
        provider_evidence_refs=["V64_PROVIDER_READINESS:gemini-cli", "NOOP_PROVIDER_ADAPTER:gemini-cli:v64"],
        trace_evidence_refs=["V63_TRACE_STEP:SIMULATE_EXTRACTION_RECEIPT", "V63_TRACE_STEP:EMIT_TRACE_RECEIPT"],
        governor_snapshot_refs=["V58_BUDGET_GOVERNOR:ok", "V58_API_RATE_GOVERNOR:ok"],
        quality_flags={
            "synthetic_payload": True,
            "no_provider_origin": True,
            "no_network_call": True,
            "not_model_truth": True,
            "operator_visible": True,
        },
    )
    values = asdict(base)
    values.update(overrides)
    return SyntheticResponseCaptureInput(**values)


def validate_synthetic_response_capture_view_model(model: SyntheticResponseCaptureViewModel) -> Dict[str, Any]:
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
    if model.paid_cloud_launch_authorized:
        findings.append("paid_cloud_launch_authorized_must_be_false")
    if model.provider_origin_claim:
        findings.append("provider_origin_claim_must_be_false")

    missing_surfaces = [surface for surface in REQUIRED_VIEW_SURFACES if surface not in model.view_surfaces]
    if missing_surfaces:
        findings.append("missing_view_surfaces:" + ",".join(missing_surfaces))

    findings.extend(_forbidden_findings(model.blocked_capabilities))
    findings.extend(_payload_findings(model.synthetic_response_payload))
    findings.extend(_quality_findings(model.quality_flags))

    if model.capture_verdict == "SYNTHETIC_RESPONSE_CAPTURE_PREVIEW_READY" and model.execution_mode != "CAPTURE_PREVIEW_ONLY":
        findings.append("ready_state_requires_capture_preview_only")
    if model.capture_verdict.startswith("BLOCKED") and model.execution_mode != "VIEW_ONLY_BLOCKED":
        findings.append("blocked_state_requires_view_only_blocked")

    return {
        "version": VERSION,
        "validation_verdict": "VALID_SYNTHETIC_RESPONSE_CAPTURE_VIEW_MODEL" if not findings else "INVALID_SYNTHETIC_RESPONSE_CAPTURE_VIEW_MODEL",
        "authority_scope": AUTHORITY_SCOPE,
        "capture_verdict": model.capture_verdict,
        "execution_mode": model.execution_mode,
        "provider_id": model.provider_id,
        "provider_adapter": model.provider_adapter,
        "selected_target": model.selected_target,
        "view_surface_count": len(model.view_surfaces),
        "extraction_zone_count": len(model.extraction_zones),
        "quality_flag_count": len(model.quality_flags),
        "receipt_preview_id": model.extraction_receipt_preview.get("receipt_id"),
        "findings": findings,
        "production_authority": False,
        "live_dispatch_claim": False,
        "external_model_call_authorized": False,
        "browser_session_mutation_authorized": False,
        "credential_access_authorized": False,
    }


if __name__ == "__main__":
    model = build_synthetic_response_capture_view_model(build_fixture_synthetic_response_capture_input())
    print(model.to_dict())
    print(validate_synthetic_response_capture_view_model(model))
