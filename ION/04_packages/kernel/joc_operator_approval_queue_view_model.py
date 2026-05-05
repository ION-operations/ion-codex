"""V62 JOC operator approval queue and dry-run dispatch handoff view model.

This module turns a V61 dispatch authorization view model into an operator-visible
approval queue entry. It is deliberately non-executing: it cannot call providers,
mutate browser sessions, access credentials, launch paid cloud resources, or grant
production authority. An approved entry may only create a dry-run handoff preview.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Literal, Mapping

VERSION = "V62_OPERATOR_APPROVAL_QUEUE_AND_DRY_RUN_HANDOFF"
AUTHORITY_SCOPE = "OPERATOR_APPROVAL_QUEUE_VIEW_MODEL_RECEIPT_ONLY"

ApprovalVerdict = Literal[
    "QUEUED_FOR_OPERATOR_REVIEW",
    "BLOCKED_AUTHORIZATION_NOT_APPROVABLE",
    "BLOCKED_MISSING_AUTHORIZATION_EVIDENCE",
    "BLOCKED_MISSING_OPERATOR_APPROVAL_EVIDENCE",
    "OPERATOR_DENIED",
    "DRY_RUN_HANDOFF_READY",
    "EXPIRED_REQUIRES_REVIEW_REFRESH",
]

OperatorDecision = Literal["PENDING", "APPROVED", "DENIED", "EXPIRED"]
ExecutionMode = Literal["DRY_RUN_HANDOFF_ONLY", "VIEW_ONLY_BLOCKED"]

APPROVABLE_AUTHORIZATION_VERDICTS = {"NEEDS_SUPERVISED_APPROVAL", "AUTHORIZATION_PREVIEW_READY"}
REQUIRED_VIEW_SURFACES = (
    "OPERATOR_APPROVAL_QUEUE",
    "GOVERNOR_EVIDENCE_RAIL",
    "APPROVAL_DECISION_CARD",
    "DENIAL_REASON_LANE",
    "DRY_RUN_HANDOFF_PREVIEW",
    "NON_AUTHORITY_BOUNDARY_STRIP",
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
class OperatorApprovalInput:
    mission_id: str
    authorization_view_model_ref: str
    route_preview_id: str
    selected_target: str
    authorization_verdict: str
    approval_mode: str
    operator_decision: OperatorDecision
    operator_id: str | None
    approval_evidence_refs: List[str]
    denial_reason: str | None = None
    requested_action_summary: str = "Request supervised dispatch authorization."
    estimated_cost_usd: float = 0.0
    estimated_latency_band: str = "unknown"
    quality_band: str = "unknown"
    view_surfaces: List[str] = field(default_factory=lambda: list(REQUIRED_VIEW_SURFACES))
    blocked_capabilities: Mapping[str, bool] = field(default_factory=lambda: FORBIDDEN_CAPABILITIES.copy())


@dataclass(frozen=True)
class OperatorApprovalQueueViewModel:
    version: str
    mission_id: str
    authorization_view_model_ref: str
    route_preview_id: str
    selected_target: str
    approval_verdict: ApprovalVerdict
    authority_scope: str
    execution_mode: ExecutionMode
    operator_decision: OperatorDecision
    operator_id: str | None
    requested_action_summary: str
    estimated_cost_usd: float
    estimated_latency_band: str
    quality_band: str
    view_surfaces: List[str]
    approval_evidence_refs: List[str]
    denial_reason: str | None
    operator_reason: str
    next_required_action: str
    dry_run_handoff_preview: Dict[str, Any]
    forbidden_capabilities: Mapping[str, bool]
    production_authority: bool = False
    live_dispatch_claim: bool = False
    external_model_call_authorized: bool = False

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


def build_operator_approval_queue_view_model(
    data: OperatorApprovalInput | Mapping[str, Any]
) -> OperatorApprovalQueueViewModel:
    if isinstance(data, Mapping):
        data = OperatorApprovalInput(**dict(data))

    missing_auth = [
        name for name in (
            "mission_id",
            "authorization_view_model_ref",
            "route_preview_id",
            "selected_target",
            "authorization_verdict",
            "approval_mode",
        ) if _missing(getattr(data, name))
    ]

    if missing_auth:
        verdict: ApprovalVerdict = "BLOCKED_MISSING_AUTHORIZATION_EVIDENCE"
        execution: ExecutionMode = "VIEW_ONLY_BLOCKED"
        reason = "Missing authorization evidence: " + ", ".join(missing_auth) + "."
        next_action = "Attach V61 authorization evidence before queuing operator review."
    elif data.authorization_verdict not in APPROVABLE_AUTHORIZATION_VERDICTS or data.approval_mode == "VIEW_ONLY_BLOCKED":
        verdict = "BLOCKED_AUTHORIZATION_NOT_APPROVABLE"
        execution = "VIEW_ONLY_BLOCKED"
        reason = f"Authorization verdict {data.authorization_verdict} is not approvable."
        next_action = "Resolve the upstream authorization block before requesting operator approval."
    elif data.operator_decision == "EXPIRED":
        verdict = "EXPIRED_REQUIRES_REVIEW_REFRESH"
        execution = "VIEW_ONLY_BLOCKED"
        reason = "Approval request expired before action."
        next_action = "Refresh route, budget, API-rate, and capability evidence before re-queueing."
    elif data.operator_decision == "DENIED":
        verdict = "OPERATOR_DENIED"
        execution = "VIEW_ONLY_BLOCKED"
        reason = data.denial_reason or "Operator denied approval without detailed reason."
        next_action = "Record denial, do not dispatch, and route back to planning or repair."
    elif data.operator_decision == "APPROVED":
        if _missing(data.operator_id) or not data.approval_evidence_refs:
            verdict = "BLOCKED_MISSING_OPERATOR_APPROVAL_EVIDENCE"
            execution = "VIEW_ONLY_BLOCKED"
            reason = "Approval is marked APPROVED but lacks operator id or approval evidence references."
            next_action = "Attach explicit operator id and approval evidence before dry-run handoff."
        else:
            verdict = "DRY_RUN_HANDOFF_READY"
            execution = "DRY_RUN_HANDOFF_ONLY"
            reason = "Operator approval is explicit and evidenced; V62 may prepare dry-run handoff only."
            next_action = "Emit dry-run handoff preview. A later branch must separately authorize live execution."
    else:
        verdict = "QUEUED_FOR_OPERATOR_REVIEW"
        execution = "DRY_RUN_HANDOFF_ONLY"
        reason = "Authorization is approvable and queued for supervised operator decision."
        next_action = "Show operator the target, governors, evidence, blocked capabilities, and dry-run-only boundary."

    handoff = {
        "version": VERSION,
        "mission_id": data.mission_id,
        "authorization_view_model_ref": data.authorization_view_model_ref,
        "route_preview_id": data.route_preview_id,
        "selected_target": data.selected_target,
        "approval_verdict": verdict,
        "execution_mode": execution,
        "operator_id": data.operator_id,
        "authority_scope": AUTHORITY_SCOPE,
        "external_model_call_authorized": False,
        "live_dispatch_claim": False,
        "production_authority": False,
    }

    return OperatorApprovalQueueViewModel(
        version=VERSION,
        mission_id=data.mission_id,
        authorization_view_model_ref=data.authorization_view_model_ref,
        route_preview_id=data.route_preview_id,
        selected_target=data.selected_target,
        approval_verdict=verdict,
        authority_scope=AUTHORITY_SCOPE,
        execution_mode=execution,
        operator_decision=data.operator_decision,
        operator_id=data.operator_id,
        requested_action_summary=data.requested_action_summary,
        estimated_cost_usd=float(data.estimated_cost_usd),
        estimated_latency_band=data.estimated_latency_band,
        quality_band=data.quality_band,
        view_surfaces=list(data.view_surfaces),
        approval_evidence_refs=list(data.approval_evidence_refs),
        denial_reason=data.denial_reason,
        operator_reason=reason,
        next_required_action=next_action,
        dry_run_handoff_preview=handoff,
        forbidden_capabilities=dict(data.blocked_capabilities),
    )


def build_fixture_operator_approval_input(**overrides: Any) -> OperatorApprovalInput:
    base = OperatorApprovalInput(
        mission_id="M-062",
        authorization_view_model_ref="V61_DISPATCH_AUTHORIZATION_VIEW_MODEL:M-061",
        route_preview_id="route-preview-v59-001",
        selected_target="gemini-cli",
        authorization_verdict="NEEDS_SUPERVISED_APPROVAL",
        approval_mode="SUPERVISED_REQUIRED",
        operator_decision="PENDING",
        operator_id=None,
        approval_evidence_refs=[
            "ION/04_packages/kernel/joc_dispatch_authorization_view_model.py",
            "ION/03_registry/joc_dispatch_authorization_policy.yaml",
        ],
        requested_action_summary="Approve dry-run handoff for supervised mission dispatch preview.",
        estimated_cost_usd=0.02,
        estimated_latency_band="interactive_seconds",
        quality_band="high",
    )
    values = asdict(base)
    values.update(overrides)
    return OperatorApprovalInput(**values)


def validate_operator_approval_queue_view_model(model: OperatorApprovalQueueViewModel) -> Dict[str, Any]:
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
    missing_surfaces = [surface for surface in REQUIRED_VIEW_SURFACES if surface not in model.view_surfaces]
    if missing_surfaces:
        findings.append("missing_view_surfaces:" + ",".join(missing_surfaces))
    findings.extend(_forbidden_findings(model.forbidden_capabilities))
    if model.approval_verdict.startswith("BLOCKED") and model.execution_mode != "VIEW_ONLY_BLOCKED":
        findings.append("blocked_verdict_requires_view_only_blocked")
    if model.approval_verdict == "DRY_RUN_HANDOFF_READY" and model.execution_mode != "DRY_RUN_HANDOFF_ONLY":
        findings.append("dry_run_ready_requires_dry_run_handoff_only")

    return {
        "version": VERSION,
        "validation_verdict": "VALID_OPERATOR_APPROVAL_QUEUE_VIEW_MODEL" if not findings else "INVALID_OPERATOR_APPROVAL_QUEUE_VIEW_MODEL",
        "authority_scope": AUTHORITY_SCOPE,
        "approval_verdict": model.approval_verdict,
        "execution_mode": model.execution_mode,
        "findings": findings,
        "production_authority": False,
        "live_dispatch_claim": False,
        "external_model_call_authorized": False,
    }


if __name__ == "__main__":
    model = build_operator_approval_queue_view_model(build_fixture_operator_approval_input())
    print(model.to_dict())
    print(validate_operator_approval_queue_view_model(model))
