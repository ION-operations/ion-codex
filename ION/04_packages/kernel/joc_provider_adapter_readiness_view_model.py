"""V64 JOC provider adapter readiness and selector health view model.

This module binds a V63 non-executing dry-run dispatch trace to provider
adapter readiness and selector/session health for cockpit rendering.

It does not dispatch, open network calls, mutate browser sessions, read
credentials, submit forms, launch paid cloud resources, or grant production
authority. It only emits a readiness receipt suitable for operator review.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Literal, Mapping

VERSION = "V64_PROVIDER_ADAPTER_READINESS_AND_SELECTOR_HEALTH_VIEW_MODEL"
AUTHORITY_SCOPE = "PROVIDER_ADAPTER_READINESS_VIEW_MODEL_RECEIPT_ONLY"

ReadinessVerdict = Literal[
    "PROVIDER_ADAPTER_READY_FOR_DRY_RUN_SELECTION",
    "BLOCKED_TRACE_NOT_READY",
    "BLOCKED_MISSING_PROVIDER_EVIDENCE",
    "BLOCKED_PROVIDER_OR_SESSION_NOT_READY",
    "BLOCKED_FORBIDDEN_CAPABILITY",
    "BLOCKED_UNSUPPORTED_ACCESS_METHOD",
    "BLOCKED_LIVE_EXECUTION_REQUESTED",
]

ExecutionMode = Literal["READINESS_VIEW_ONLY", "VIEW_ONLY_BLOCKED"]

REQUIRED_UPSTREAM_TRACE_VERDICTS = {"DRY_RUN_TRACE_READY"}
REQUIRED_UPSTREAM_EXECUTION_MODES = {"TRACE_ONLY_NON_EXECUTING"}

ALLOWED_ACCESS_METHODS = {
    "browser_noop",
    "api_noop",
    "cli_noop",
    "local_noop",
    "cloud_noop",
}

ALLOWED_COMPUTE_RINGS = {
    "RING_1_BROWSER_SESSION",
    "RING_2_API_CLI_LOCAL",
    "RING_3_CLOUD_COMPUTE",
}

REQUIRED_VIEW_SURFACES = (
    "PROVIDER_ADAPTER_READINESS_RAIL",
    "SESSION_SELECTOR_HEALTH_PANEL",
    "NOOP_ADAPTER_INVARIANT_STRIP",
    "GOVERNOR_EVIDENCE_LINKS",
    "ACCESS_METHOD_BADGE",
    "COMPUTE_RING_BADGE",
    "BLOCKED_CAPABILITY_LEDGER",
    "NEXT_ACTION_CALLOUT",
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

READY_ADAPTER_HEALTH = {"READY", "NOOP_READY"}
BROWSER_READY_SESSION_HEALTH = {"HEALTHY"}
NON_BROWSER_READY_SESSION_HEALTH = {"HEALTHY", "NOT_REQUIRED"}


@dataclass(frozen=True)
class ProviderAdapterReadinessInput:
    mission_id: str
    dry_run_trace_ref: str
    dry_run_trace_verdict: str
    upstream_execution_mode: str
    route_preview_id: str
    selected_target: str
    provider_id: str
    provider_adapter: str
    access_method: str
    compute_ring: str
    adapter_health: str
    session_health: str
    selector_rank: int
    noop_adapter_ref: str
    provider_evidence_refs: List[str]
    governor_snapshot_refs: List[str]
    trace_evidence_refs: List[str]
    live_execution_requested: bool = False
    view_surfaces: List[str] = field(default_factory=lambda: list(REQUIRED_VIEW_SURFACES))
    blocked_capabilities: Mapping[str, bool] = field(default_factory=lambda: FORBIDDEN_CAPABILITIES.copy())


@dataclass(frozen=True)
class ProviderAdapterReadinessViewModel:
    version: str
    mission_id: str
    dry_run_trace_ref: str
    route_preview_id: str
    selected_target: str
    provider_id: str
    provider_adapter: str
    access_method: str
    compute_ring: str
    adapter_health: str
    session_health: str
    selector_rank: int
    noop_adapter_ref: str
    readiness_verdict: ReadinessVerdict
    authority_scope: str
    execution_mode: ExecutionMode
    view_surfaces: List[str]
    provider_evidence_refs: List[str]
    governor_snapshot_refs: List[str]
    trace_evidence_refs: List[str]
    blocked_capabilities: Mapping[str, bool]
    operator_reason: str
    next_required_action: str
    production_authority: bool = False
    live_dispatch_claim: bool = False
    external_model_call_authorized: bool = False
    browser_session_mutation_authorized: bool = False
    credential_access_authorized: bool = False
    paid_cloud_launch_authorized: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _missing(value: Any) -> bool:
    return value is None or value == "" or value == []


def _forbidden_findings(blocked: Mapping[str, bool]) -> List[str]:
    findings: List[str] = []
    for key, expected in FORBIDDEN_CAPABILITIES.items():
        if blocked.get(key) is not expected:
            findings.append(f"forbidden capability {key!r} expected {expected!r} got {blocked.get(key)!r}")
    for key, value in blocked.items():
        if value is not False:
            findings.append(f"capability {key!r} is not blocked")
    return findings


def _session_health_is_ready(access_method: str, session_health: str) -> bool:
    if access_method == "browser_noop":
        return session_health in BROWSER_READY_SESSION_HEALTH
    return session_health in NON_BROWSER_READY_SESSION_HEALTH


def build_provider_adapter_readiness_view_model(
    data: ProviderAdapterReadinessInput | Mapping[str, Any]
) -> ProviderAdapterReadinessViewModel:
    if isinstance(data, Mapping):
        data = ProviderAdapterReadinessInput(**dict(data))

    missing = [
        name for name in (
            "mission_id",
            "dry_run_trace_ref",
            "dry_run_trace_verdict",
            "upstream_execution_mode",
            "route_preview_id",
            "selected_target",
            "provider_id",
            "provider_adapter",
            "access_method",
            "compute_ring",
            "adapter_health",
            "session_health",
            "noop_adapter_ref",
        ) if _missing(getattr(data, name))
    ]
    if not data.provider_evidence_refs:
        missing.append("provider_evidence_refs")
    if not data.governor_snapshot_refs:
        missing.append("governor_snapshot_refs")
    if not data.trace_evidence_refs:
        missing.append("trace_evidence_refs")
    if data.selector_rank < 1:
        missing.append("selector_rank")

    forbidden_findings = _forbidden_findings(data.blocked_capabilities)

    if data.live_execution_requested:
        verdict: ReadinessVerdict = "BLOCKED_LIVE_EXECUTION_REQUESTED"
        execution: ExecutionMode = "VIEW_ONLY_BLOCKED"
        reason = "Live execution was requested; V64 only renders provider readiness for no-op dry-run state."
        next_action = "Route to a future live provider execution authority branch; do not dispatch."
    elif missing:
        verdict = "BLOCKED_MISSING_PROVIDER_EVIDENCE"
        execution = "VIEW_ONLY_BLOCKED"
        reason = "Missing provider readiness evidence: " + ", ".join(missing) + "."
        next_action = "Attach dry-run trace, provider, adapter, session, governor, and no-op evidence."
    elif data.dry_run_trace_verdict not in REQUIRED_UPSTREAM_TRACE_VERDICTS:
        verdict = "BLOCKED_TRACE_NOT_READY"
        execution = "VIEW_ONLY_BLOCKED"
        reason = f"Upstream trace verdict {data.dry_run_trace_verdict} is not ready."
        next_action = "Return to V63 dry-run dispatch trace."
    elif data.upstream_execution_mode not in REQUIRED_UPSTREAM_EXECUTION_MODES:
        verdict = "BLOCKED_TRACE_NOT_READY"
        execution = "VIEW_ONLY_BLOCKED"
        reason = f"Upstream execution mode {data.upstream_execution_mode} is not supported by V64."
        next_action = "Require V63 TRACE_ONLY_NON_EXECUTING before provider readiness rendering."
    elif data.access_method not in ALLOWED_ACCESS_METHODS or data.compute_ring not in ALLOWED_COMPUTE_RINGS:
        verdict = "BLOCKED_UNSUPPORTED_ACCESS_METHOD"
        execution = "VIEW_ONLY_BLOCKED"
        reason = f"Unsupported access method or compute ring: {data.access_method} / {data.compute_ring}."
        next_action = "Select an allowed no-op access method and compute ring."
    elif forbidden_findings:
        verdict = "BLOCKED_FORBIDDEN_CAPABILITY"
        execution = "VIEW_ONLY_BLOCKED"
        reason = "Forbidden capability evidence detected: " + ", ".join(forbidden_findings) + "."
        next_action = "Remove live/network/browser/credential/provider authority from the readiness model."
    elif data.adapter_health not in READY_ADAPTER_HEALTH or not _session_health_is_ready(data.access_method, data.session_health):
        verdict = "BLOCKED_PROVIDER_OR_SESSION_NOT_READY"
        execution = "VIEW_ONLY_BLOCKED"
        reason = f"Provider adapter/session health is not ready: adapter={data.adapter_health}, session={data.session_health}."
        next_action = "Repair provider adapter readiness or session health before any future live branch review."
    else:
        verdict = "PROVIDER_ADAPTER_READY_FOR_DRY_RUN_SELECTION"
        execution = "READINESS_VIEW_ONLY"
        reason = "Provider adapter readiness may be rendered for the non-executing dry-run selection path only."
        next_action = "Show readiness receipt. Future live dispatch still requires a separate execution authority branch."

    return ProviderAdapterReadinessViewModel(
        version=VERSION,
        mission_id=data.mission_id,
        dry_run_trace_ref=data.dry_run_trace_ref,
        route_preview_id=data.route_preview_id,
        selected_target=data.selected_target,
        provider_id=data.provider_id,
        provider_adapter=data.provider_adapter,
        access_method=data.access_method,
        compute_ring=data.compute_ring,
        adapter_health=data.adapter_health,
        session_health=data.session_health,
        selector_rank=data.selector_rank,
        noop_adapter_ref=data.noop_adapter_ref,
        readiness_verdict=verdict,
        authority_scope=AUTHORITY_SCOPE,
        execution_mode=execution,
        view_surfaces=list(data.view_surfaces),
        provider_evidence_refs=list(data.provider_evidence_refs),
        governor_snapshot_refs=list(data.governor_snapshot_refs),
        trace_evidence_refs=list(data.trace_evidence_refs),
        blocked_capabilities=dict(data.blocked_capabilities),
        operator_reason=reason,
        next_required_action=next_action,
    )


def build_fixture_provider_adapter_readiness_input(**overrides: Any) -> ProviderAdapterReadinessInput:
    base = ProviderAdapterReadinessInput(
        mission_id="M-064",
        dry_run_trace_ref="V63_DRY_RUN_TRACE:M-063",
        dry_run_trace_verdict="DRY_RUN_TRACE_READY",
        upstream_execution_mode="TRACE_ONLY_NON_EXECUTING",
        route_preview_id="route-preview-v59-001",
        selected_target="gemini-cli",
        provider_id="gemini",
        provider_adapter="GeminiCLIDriver.NOOP",
        access_method="cli_noop",
        compute_ring="RING_2_API_CLI_LOCAL",
        adapter_health="NOOP_READY",
        session_health="NOT_REQUIRED",
        selector_rank=1,
        noop_adapter_ref="NOOP_PROVIDER_ADAPTER:gemini-cli:v63",
        provider_evidence_refs=[
            "PROVIDER_REGISTRY:gemini-cli",
            "ADAPTER_HEALTH:NOOP_READY",
        ],
        governor_snapshot_refs=[
            "V58_BUDGET_GOVERNOR:ok",
            "V58_API_RATE_GOVERNOR:ok",
        ],
        trace_evidence_refs=[
            "V63_TRACE_STEP:BUILD_PROVIDER_ADAPTER_NOOP",
            "V63_TRACE_STEP:EMIT_TRACE_RECEIPT",
        ],
    )
    values = asdict(base)
    values.update(overrides)
    return ProviderAdapterReadinessInput(**values)


def validate_provider_adapter_readiness_view_model(model: ProviderAdapterReadinessViewModel) -> Dict[str, Any]:
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

    missing_surfaces = [surface for surface in REQUIRED_VIEW_SURFACES if surface not in model.view_surfaces]
    if missing_surfaces:
        findings.append("missing_view_surfaces:" + ",".join(missing_surfaces))

    findings.extend(_forbidden_findings(model.blocked_capabilities))

    if model.access_method not in ALLOWED_ACCESS_METHODS:
        findings.append("unsupported_access_method")
    if model.compute_ring not in ALLOWED_COMPUTE_RINGS:
        findings.append("unsupported_compute_ring")
    if model.readiness_verdict == "PROVIDER_ADAPTER_READY_FOR_DRY_RUN_SELECTION" and model.execution_mode != "READINESS_VIEW_ONLY":
        findings.append("ready_state_requires_readiness_view_only")
    if model.readiness_verdict.startswith("BLOCKED") and model.execution_mode != "VIEW_ONLY_BLOCKED":
        findings.append("blocked_state_requires_view_only_blocked")

    return {
        "version": VERSION,
        "validation_verdict": "VALID_PROVIDER_ADAPTER_READINESS_VIEW_MODEL" if not findings else "INVALID_PROVIDER_ADAPTER_READINESS_VIEW_MODEL",
        "authority_scope": AUTHORITY_SCOPE,
        "readiness_verdict": model.readiness_verdict,
        "execution_mode": model.execution_mode,
        "provider_id": model.provider_id,
        "provider_adapter": model.provider_adapter,
        "access_method": model.access_method,
        "compute_ring": model.compute_ring,
        "view_surface_count": len(model.view_surfaces),
        "provider_evidence_count": len(model.provider_evidence_refs),
        "governor_snapshot_count": len(model.governor_snapshot_refs),
        "trace_evidence_count": len(model.trace_evidence_refs),
        "findings": findings,
        "production_authority": False,
        "live_dispatch_claim": False,
        "external_model_call_authorized": False,
        "browser_session_mutation_authorized": False,
        "credential_access_authorized": False,
    }


if __name__ == "__main__":
    model = build_provider_adapter_readiness_view_model(build_fixture_provider_adapter_readiness_input())
    print(model.to_dict())
    print(validate_provider_adapter_readiness_view_model(model))
