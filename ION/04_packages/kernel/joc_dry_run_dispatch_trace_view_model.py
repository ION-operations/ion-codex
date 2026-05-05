"""V63 JOC dry-run dispatch execution trace view model.

This module turns a V62 dry-run handoff into a cockpit-visible dispatch trace.
It is deliberately non-executing: it cannot call providers, mutate browser
sessions, touch credentials, submit forms, launch paid cloud resources, or grant
production authority.

The model exists so the UI can show the exact sequence ION would attempt in a
future live-dispatch branch while preserving the current dry-run-only boundary.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Literal, Mapping

VERSION = "V63_DRY_RUN_DISPATCH_EXECUTION_TRACE_VIEW_MODEL"
AUTHORITY_SCOPE = "DRY_RUN_DISPATCH_TRACE_VIEW_MODEL_RECEIPT_ONLY"

TraceVerdict = Literal[
    "DRY_RUN_TRACE_READY",
    "BLOCKED_HANDOFF_NOT_READY",
    "BLOCKED_LIVE_EXECUTION_REQUESTED",
    "BLOCKED_MISSING_TRACE_EVIDENCE",
    "BLOCKED_FORBIDDEN_CAPABILITY",
    "BLOCKED_UNSUPPORTED_EXECUTION_MODE",
]

ExecutionMode = Literal["TRACE_ONLY_NON_EXECUTING", "VIEW_ONLY_BLOCKED"]

REQUIRED_UPSTREAM_APPROVAL_VERDICTS = {"DRY_RUN_HANDOFF_READY"}
REQUIRED_UPSTREAM_EXECUTION_MODES = {"DRY_RUN_HANDOFF_ONLY"}

TRACE_PHASES = (
    "VALIDATE_OPERATOR_HANDOFF",
    "RECHECK_GOVERNORS",
    "COMPILE_CONTEXT_PREVIEW",
    "BUILD_PROVIDER_ADAPTER_NOOP",
    "SIMULATE_PROMPT_INJECTION",
    "SIMULATE_RESPONSE_WAIT",
    "SIMULATE_EXTRACTION_RECEIPT",
    "EMIT_TRACE_RECEIPT",
)

REQUIRED_VIEW_SURFACES = (
    "DRY_RUN_EXECUTION_TRACE",
    "PROVIDER_ADAPTER_NOOP_LANE",
    "CONTEXT_INJECTION_PREVIEW",
    "GOVERNOR_RECHECK_SNAPSHOT",
    "TIMELINE_EVENT_RAIL",
    "NON_EXECUTION_BOUNDARY_STRIP",
    "OPERATOR_HANDOFF_LINK",
    "RECEIPT_PREVIEW",
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
class DryRunTraceInput:
    mission_id: str
    dry_run_handoff_ref: str
    operator_approval_ref: str
    operator_approval_verdict: str
    upstream_execution_mode: str
    route_preview_id: str
    selected_target: str
    provider_adapter: str
    access_method: str
    context_bundle_ref: str
    prompt_envelope_ref: str
    governor_snapshot_refs: List[str]
    approval_evidence_refs: List[str]
    live_execution_requested: bool = False
    trace_steps: List[Mapping[str, Any]] = field(default_factory=list)
    view_surfaces: List[str] = field(default_factory=lambda: list(REQUIRED_VIEW_SURFACES))
    blocked_capabilities: Mapping[str, bool] = field(default_factory=lambda: FORBIDDEN_CAPABILITIES.copy())


@dataclass(frozen=True)
class DryRunTraceStep:
    phase: str
    status: str
    title: str
    detail: str
    evidence_refs: List[str]
    live_effect: bool = False
    network_call: bool = False
    credential_touch: bool = False
    browser_mutation: bool = False
    external_model_call: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DryRunDispatchTraceViewModel:
    version: str
    mission_id: str
    dry_run_handoff_ref: str
    operator_approval_ref: str
    operator_approval_verdict: str
    route_preview_id: str
    selected_target: str
    provider_adapter: str
    access_method: str
    trace_verdict: TraceVerdict
    authority_scope: str
    execution_mode: ExecutionMode
    trace_steps: List[Dict[str, Any]]
    view_surfaces: List[str]
    context_bundle_ref: str
    prompt_envelope_ref: str
    governor_snapshot_refs: List[str]
    approval_evidence_refs: List[str]
    blocked_capabilities: Mapping[str, bool]
    operator_reason: str
    next_required_action: str
    production_authority: bool = False
    live_dispatch_claim: bool = False
    external_model_call_authorized: bool = False
    browser_session_mutation_authorized: bool = False
    credential_access_authorized: bool = False

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


def _step_is_non_executing(step: Mapping[str, Any]) -> bool:
    return not any(
        bool(step.get(key))
        for key in (
            "live_effect",
            "network_call",
            "credential_touch",
            "browser_mutation",
            "external_model_call",
        )
    )


def _default_trace_steps(data: DryRunTraceInput) -> List[DryRunTraceStep]:
    refs = {
        "handoff": [data.dry_run_handoff_ref, data.operator_approval_ref],
        "governors": list(data.governor_snapshot_refs),
        "context": [data.context_bundle_ref],
        "prompt": [data.prompt_envelope_ref],
        "approval": list(data.approval_evidence_refs),
    }
    return [
        DryRunTraceStep(
            phase="VALIDATE_OPERATOR_HANDOFF",
            status="READY",
            title="Validate operator handoff",
            detail="Confirm V62 produced a dry-run handoff and no live execution authority.",
            evidence_refs=refs["handoff"] + refs["approval"],
        ),
        DryRunTraceStep(
            phase="RECHECK_GOVERNORS",
            status="READY",
            title="Recheck budget and API-rate governors",
            detail="Display governor snapshots that would gate a later live dispatch.",
            evidence_refs=refs["governors"],
        ),
        DryRunTraceStep(
            phase="COMPILE_CONTEXT_PREVIEW",
            status="READY",
            title="Compile context preview",
            detail="Render the context bundle reference without sending it to a provider.",
            evidence_refs=refs["context"],
        ),
        DryRunTraceStep(
            phase="BUILD_PROVIDER_ADAPTER_NOOP",
            status="NOOP",
            title="Build provider adapter no-op",
            detail=f"Prepare a non-executing {data.provider_adapter} adapter lane for {data.selected_target}.",
            evidence_refs=[data.route_preview_id],
        ),
        DryRunTraceStep(
            phase="SIMULATE_PROMPT_INJECTION",
            status="SIMULATED",
            title="Simulate prompt injection",
            detail="Show the prompt envelope that would be injected, with all external calls blocked.",
            evidence_refs=refs["prompt"],
        ),
        DryRunTraceStep(
            phase="SIMULATE_RESPONSE_WAIT",
            status="SIMULATED",
            title="Simulate response wait",
            detail="Render the wait/monitoring phase without opening network or browser mutation paths.",
            evidence_refs=[],
        ),
        DryRunTraceStep(
            phase="SIMULATE_EXTRACTION_RECEIPT",
            status="SIMULATED",
            title="Simulate extraction receipt",
            detail="Preview the receipt fields that a future live extraction would need to emit.",
            evidence_refs=[],
        ),
        DryRunTraceStep(
            phase="EMIT_TRACE_RECEIPT",
            status="READY",
            title="Emit dry-run trace receipt",
            detail="Close the trace as non-executing evidence for operator review.",
            evidence_refs=[data.dry_run_handoff_ref],
        ),
    ]


def build_dry_run_dispatch_trace_view_model(
    data: DryRunTraceInput | Mapping[str, Any]
) -> DryRunDispatchTraceViewModel:
    if isinstance(data, Mapping):
        data = DryRunTraceInput(**dict(data))

    missing = [
        name for name in (
            "mission_id",
            "dry_run_handoff_ref",
            "operator_approval_ref",
            "operator_approval_verdict",
            "upstream_execution_mode",
            "route_preview_id",
            "selected_target",
            "provider_adapter",
            "access_method",
            "context_bundle_ref",
            "prompt_envelope_ref",
        ) if _missing(getattr(data, name))
    ]
    if not data.governor_snapshot_refs:
        missing.append("governor_snapshot_refs")
    if not data.approval_evidence_refs:
        missing.append("approval_evidence_refs")

    forbidden_findings = _forbidden_findings(data.blocked_capabilities)

    raw_steps = list(data.trace_steps)
    if not raw_steps:
        raw_steps = [step.to_dict() for step in _default_trace_steps(data)]

    step_findings = [
        f"executing_step:{step.get('phase', '<unknown>')}"
        for step in raw_steps
        if not _step_is_non_executing(step)
    ]

    phases_present = {str(step.get("phase")) for step in raw_steps}
    missing_phases = [phase for phase in TRACE_PHASES if phase not in phases_present]

    if data.live_execution_requested:
        verdict: TraceVerdict = "BLOCKED_LIVE_EXECUTION_REQUESTED"
        execution: ExecutionMode = "VIEW_ONLY_BLOCKED"
        reason = "Live execution was requested, but V63 only permits dry-run trace rendering."
        next_action = "Route to a future live-execution authority branch; do not dispatch."
    elif missing:
        verdict = "BLOCKED_MISSING_TRACE_EVIDENCE"
        execution = "VIEW_ONLY_BLOCKED"
        reason = "Missing dry-run trace evidence: " + ", ".join(missing) + "."
        next_action = "Attach missing handoff, route, context, prompt, governor, and approval evidence."
    elif data.operator_approval_verdict not in REQUIRED_UPSTREAM_APPROVAL_VERDICTS:
        verdict = "BLOCKED_HANDOFF_NOT_READY"
        execution = "VIEW_ONLY_BLOCKED"
        reason = f"Operator approval verdict {data.operator_approval_verdict} is not a dry-run handoff verdict."
        next_action = "Return to V62 operator approval queue."
    elif data.upstream_execution_mode not in REQUIRED_UPSTREAM_EXECUTION_MODES:
        verdict = "BLOCKED_UNSUPPORTED_EXECUTION_MODE"
        execution = "VIEW_ONLY_BLOCKED"
        reason = f"Upstream execution mode {data.upstream_execution_mode} is not supported by V63."
        next_action = "Require V62 DRY_RUN_HANDOFF_ONLY before trace rendering."
    elif forbidden_findings or step_findings:
        verdict = "BLOCKED_FORBIDDEN_CAPABILITY"
        execution = "VIEW_ONLY_BLOCKED"
        reason = "Forbidden capability evidence detected: " + ", ".join(forbidden_findings + step_findings) + "."
        next_action = "Remove live effects/network/credential/browser/provider authority from the trace."
    elif missing_phases:
        verdict = "BLOCKED_MISSING_TRACE_EVIDENCE"
        execution = "VIEW_ONLY_BLOCKED"
        reason = "Missing required trace phases: " + ", ".join(missing_phases) + "."
        next_action = "Complete all dry-run trace phases before showing trace-ready state."
    else:
        verdict = "DRY_RUN_TRACE_READY"
        execution = "TRACE_ONLY_NON_EXECUTING"
        reason = "Dry-run trace is complete and non-executing; it may be rendered for operator review only."
        next_action = "Show trace receipt. A later branch must separately authorize any live dispatch."

    return DryRunDispatchTraceViewModel(
        version=VERSION,
        mission_id=data.mission_id,
        dry_run_handoff_ref=data.dry_run_handoff_ref,
        operator_approval_ref=data.operator_approval_ref,
        operator_approval_verdict=data.operator_approval_verdict,
        route_preview_id=data.route_preview_id,
        selected_target=data.selected_target,
        provider_adapter=data.provider_adapter,
        access_method=data.access_method,
        trace_verdict=verdict,
        authority_scope=AUTHORITY_SCOPE,
        execution_mode=execution,
        trace_steps=[dict(step) for step in raw_steps],
        view_surfaces=list(data.view_surfaces),
        context_bundle_ref=data.context_bundle_ref,
        prompt_envelope_ref=data.prompt_envelope_ref,
        governor_snapshot_refs=list(data.governor_snapshot_refs),
        approval_evidence_refs=list(data.approval_evidence_refs),
        blocked_capabilities=dict(data.blocked_capabilities),
        operator_reason=reason,
        next_required_action=next_action,
    )


def build_fixture_dry_run_trace_input(**overrides: Any) -> DryRunTraceInput:
    base = DryRunTraceInput(
        mission_id="M-063",
        dry_run_handoff_ref="V62_DRY_RUN_HANDOFF:M-062",
        operator_approval_ref="V62_OPERATOR_APPROVAL:M-062",
        operator_approval_verdict="DRY_RUN_HANDOFF_READY",
        upstream_execution_mode="DRY_RUN_HANDOFF_ONLY",
        route_preview_id="route-preview-v59-001",
        selected_target="gemini-cli",
        provider_adapter="GeminiCLIDriver.NOOP",
        access_method="cli_noop",
        context_bundle_ref="V58_CONTEXT_ROUTE:route-preview-v58-001",
        prompt_envelope_ref="PROMPT_ENVELOPE_PREVIEW:M-063",
        governor_snapshot_refs=[
            "V58_BUDGET_GOVERNOR:ok",
            "V58_API_RATE_GOVERNOR:ok",
            "V61_DISPATCH_AUTHORIZATION:NEEDS_SUPERVISED_APPROVAL",
        ],
        approval_evidence_refs=[
            "V62_OPERATOR_APPROVAL:operator:braden",
            "V62_DRY_RUN_HANDOFF:ready",
        ],
    )
    values = asdict(base)
    values.update(overrides)
    return DryRunTraceInput(**values)


def validate_dry_run_dispatch_trace_view_model(model: DryRunDispatchTraceViewModel) -> Dict[str, Any]:
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

    missing_surfaces = [surface for surface in REQUIRED_VIEW_SURFACES if surface not in model.view_surfaces]
    if missing_surfaces:
        findings.append("missing_view_surfaces:" + ",".join(missing_surfaces))

    findings.extend(_forbidden_findings(model.blocked_capabilities))

    phases_present = {str(step.get("phase")) for step in model.trace_steps}
    missing_phases = [phase for phase in TRACE_PHASES if phase not in phases_present]
    if missing_phases:
        findings.append("missing_trace_phases:" + ",".join(missing_phases))

    executing_steps = [
        str(step.get("phase", "<unknown>"))
        for step in model.trace_steps
        if not _step_is_non_executing(step)
    ]
    if executing_steps:
        findings.append("trace_steps_have_live_effects:" + ",".join(executing_steps))

    if model.trace_verdict == "DRY_RUN_TRACE_READY" and model.execution_mode != "TRACE_ONLY_NON_EXECUTING":
        findings.append("trace_ready_requires_trace_only_non_executing")
    if model.trace_verdict.startswith("BLOCKED") and model.execution_mode != "VIEW_ONLY_BLOCKED":
        findings.append("blocked_trace_requires_view_only_blocked")

    return {
        "version": VERSION,
        "validation_verdict": "VALID_DRY_RUN_DISPATCH_TRACE_VIEW_MODEL" if not findings else "INVALID_DRY_RUN_DISPATCH_TRACE_VIEW_MODEL",
        "authority_scope": AUTHORITY_SCOPE,
        "trace_verdict": model.trace_verdict,
        "execution_mode": model.execution_mode,
        "trace_step_count": len(model.trace_steps),
        "view_surface_count": len(model.view_surfaces),
        "findings": findings,
        "production_authority": False,
        "live_dispatch_claim": False,
        "external_model_call_authorized": False,
        "browser_session_mutation_authorized": False,
        "credential_access_authorized": False,
    }


if __name__ == "__main__":
    model = build_dry_run_dispatch_trace_view_model(build_fixture_dry_run_trace_input())
    print(model.to_dict())
    print(validate_dry_run_dispatch_trace_view_model(model))
