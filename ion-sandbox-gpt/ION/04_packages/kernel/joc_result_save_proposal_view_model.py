"""V67 JOC operator-reviewed result save proposal view model.

Binds V66 synthetic synthesis/route-result preview to a non-writing save
proposal surface. It does not write memory, documents, artifacts, graph state,
source summaries, call providers, mutate browser sessions, or claim real output.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Mapping

VERSION = "V67_OPERATOR_REVIEWED_RESULT_SAVE_PROPOSAL_VIEW_MODEL"
AUTHORITY_SCOPE = "RESULT_SAVE_PROPOSAL_VIEW_MODEL_RECEIPT_ONLY"
REQUIRED_SYNTHESIS_VERDICTS = {"SYNTHETIC_SYNTHESIS_PREVIEW_READY"}
REQUIRED_EXECUTION_MODES = {"SYNTHESIS_ROUTE_PREVIEW_ONLY"}
REQUIRED_VIEW_SURFACES = (
    "RESULT_REVIEW_PANEL", "SAVE_PROPOSAL_QUEUE", "MEMORY_WRITE_PROPOSAL_PREVIEW",
    "DOCUMENT_DRAFT_SAVE_PREVIEW", "ARTIFACT_EXPORT_PREVIEW", "AGENT_REVIEW_PACKET_PREVIEW",
    "FOLLOWUP_MISSION_DRAFT_PREVIEW", "NO_WRITE_BOUNDARY_STRIP", "OPERATOR_DECISION_REQUIRED_STRIP",
)
ALLOWED_TARGETS = (
    "MEMORY_DRY_RUN_PROPOSAL", "DOCUMENT_DRAFT_SAVE_PREVIEW", "ARTIFACT_EXPORT_PREVIEW",
    "AGENT_REVIEW_PACKET_PREVIEW", "FOLLOWUP_MISSION_DRAFT_PREVIEW",
)
REQUIRED_REVIEW_FLAGS = (
    "operator_review_required", "no_auto_save", "no_memory_write", "no_document_write",
    "no_artifact_export", "no_graph_commit",
)
FORBIDDEN_COMMIT_CAPABILITIES = {
    "external_model_call": False, "real_provider_output_claim": False, "live_dispatch": False,
    "browser_session_mutation": False, "credential_access": False, "memory_write": False,
    "document_write": False, "artifact_export": False, "canonical_graph_write": False,
    "source_summary_rewrite": False, "form_submission": False, "paid_cloud_launch": False,
    "unrestricted_agent_activation": False, "production_authority": False,
}

@dataclass(frozen=True)
class ResultSaveProposalInput:
    mission_id: str
    synthesis_ref: str
    synthesis_verdict: str
    upstream_execution_mode: str
    synthesis_preview_id: str
    route_result_preview_id: str
    synthetic_summary_preview: str
    proposed_targets: List[str]
    review_policy_flags: Mapping[str, bool]
    evidence_refs: List[str]
    governor_snapshot_refs: List[str]
    operator_review_ref: str
    followup_prompt_preview: str
    live_save_requested: bool = False
    memory_write_requested: bool = False
    document_write_requested: bool = False
    artifact_export_requested: bool = False
    canonical_graph_write_requested: bool = False
    source_summary_rewrite_requested: bool = False
    view_surfaces: List[str] = field(default_factory=lambda: list(REQUIRED_VIEW_SURFACES))
    blocked_capabilities: Mapping[str, bool] = field(default_factory=lambda: FORBIDDEN_COMMIT_CAPABILITIES.copy())

@dataclass(frozen=True)
class ResultSaveProposalViewModel:
    version: str
    mission_id: str
    synthesis_ref: str
    synthesis_verdict: str
    synthesis_preview_id: str
    route_result_preview_id: str
    save_proposal_verdict: str
    authority_scope: str
    execution_mode: str
    synthetic_summary_preview: str
    proposal_cards: List[Mapping[str, Any]]
    proposed_targets: List[str]
    view_surfaces: List[str]
    evidence_refs: List[str]
    governor_snapshot_refs: List[str]
    review_policy_flags: Mapping[str, bool]
    blocked_capabilities: Mapping[str, bool]
    operator_review_ref: str
    operator_reason: str
    next_required_action: str
    followup_prompt_preview: str
    production_authority: bool = False
    live_dispatch_claim: bool = False
    live_write_claim: bool = False
    external_model_call_authorized: bool = False
    real_provider_output_claim: bool = False
    browser_session_mutation_authorized: bool = False
    credential_access_authorized: bool = False
    memory_write_authorized: bool = False
    document_write_authorized: bool = False
    artifact_export_authorized: bool = False
    canonical_graph_write_authorized: bool = False
    source_summary_rewrite_authorized: bool = False
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

def _missing(v: Any) -> bool:
    return v is None or v == "" or v == [] or v == {}

def _forbidden_findings(blocked: Mapping[str, bool]) -> List[str]:
    out: List[str] = []
    for k, expected in FORBIDDEN_COMMIT_CAPABILITIES.items():
        if blocked.get(k) is not expected:
            out.append(f"forbidden commit capability {k!r} expected {expected!r} got {blocked.get(k)!r}")
    for k, v in blocked.items():
        if v is not False:
            out.append(f"commit capability {k!r} is not blocked")
    return out

def _review_findings(flags: Mapping[str, bool]) -> List[str]:
    return [f"review_policy_{f}_must_be_true" for f in REQUIRED_REVIEW_FLAGS if flags.get(f) is not True]

def _target_findings(targets: List[str]) -> List[str]:
    allowed = set(ALLOWED_TARGETS)
    return [f"proposal_target_{t}_not_allowed" for t in targets if t not in allowed]

def _future_auth(t: str) -> str:
    return {
        "MEMORY_DRY_RUN_PROPOSAL": "FUTURE_MEMORY_WRITE_AUTHORITY_REQUIRED",
        "DOCUMENT_DRAFT_SAVE_PREVIEW": "FUTURE_DOCUMENT_SAVE_AUTHORITY_REQUIRED",
        "ARTIFACT_EXPORT_PREVIEW": "FUTURE_ARTIFACT_EXPORT_AUTHORITY_REQUIRED",
        "AGENT_REVIEW_PACKET_PREVIEW": "FUTURE_AGENT_REVIEW_ROUTE_AUTHORITY_REQUIRED",
        "FOLLOWUP_MISSION_DRAFT_PREVIEW": "FUTURE_MISSION_CREATION_AUTHORITY_REQUIRED",
    }.get(t, "FUTURE_ROUTE_AUTHORITY_REQUIRED")

def build_result_save_proposal_view_model(data: ResultSaveProposalInput | Mapping[str, Any]) -> ResultSaveProposalViewModel:
    if isinstance(data, Mapping):
        data = ResultSaveProposalInput(**dict(data))
    missing = [n for n in ("mission_id","synthesis_ref","synthesis_verdict","upstream_execution_mode","synthesis_preview_id","route_result_preview_id","synthetic_summary_preview","operator_review_ref","followup_prompt_preview") if _missing(getattr(data,n))]
    if not data.proposed_targets: missing.append("proposed_targets")
    if not data.evidence_refs: missing.append("evidence_refs")
    if not data.governor_snapshot_refs: missing.append("governor_snapshot_refs")
    if not data.review_policy_flags: missing.append("review_policy_flags")
    forbidden = _forbidden_findings(data.blocked_capabilities)
    review = _review_findings(data.review_policy_flags)
    targets = _target_findings(data.proposed_targets)
    if data.live_save_requested: verdict, reason = "BLOCKED_LIVE_SAVE_REQUESTED", "Live save requested; V67 is proposal preview only."
    elif data.memory_write_requested: verdict, reason = "BLOCKED_MEMORY_WRITE_REQUESTED", "Memory write requested; V67 cannot write memory."
    elif data.document_write_requested: verdict, reason = "BLOCKED_DOCUMENT_WRITE_REQUESTED", "Document write requested; V67 cannot write documents."
    elif data.artifact_export_requested: verdict, reason = "BLOCKED_ARTIFACT_EXPORT_REQUESTED", "Artifact export requested; V67 cannot export artifacts."
    elif data.canonical_graph_write_requested: verdict, reason = "BLOCKED_CANONICAL_GRAPH_WRITE_REQUESTED", "Canonical graph write requested; V67 cannot commit graph state."
    elif data.source_summary_rewrite_requested: verdict, reason = "BLOCKED_SOURCE_SUMMARY_REWRITE_REQUESTED", "Source-summary rewrite requested; V67 cannot rewrite summaries."
    elif missing: verdict, reason = "BLOCKED_MISSING_RESULT_EVIDENCE", "Missing result-save proposal evidence: " + ", ".join(missing) + "."
    elif data.synthesis_verdict not in REQUIRED_SYNTHESIS_VERDICTS or data.upstream_execution_mode not in REQUIRED_EXECUTION_MODES:
        verdict, reason = "BLOCKED_SYNTHESIS_NOT_READY", "V66 synthesis preview is not ready for save proposal."
    elif forbidden: verdict, reason = "BLOCKED_FORBIDDEN_COMMIT_CAPABILITY", "Forbidden commit capability evidence detected: " + ", ".join(forbidden) + "."
    elif review: verdict, reason = "BLOCKED_MISSING_OPERATOR_REVIEW_POLICY", "Operator review policy missing: " + ", ".join(review) + "."
    elif targets: verdict, reason = "BLOCKED_INVALID_PROPOSAL_SCOPE", "Invalid proposal target scope: " + ", ".join(targets) + "."
    else: verdict, reason = "RESULT_SAVE_PROPOSAL_READY", "V66 route-result preview may be rendered as operator-reviewed save proposal cards only."
    execution = "SAVE_PROPOSAL_PREVIEW_ONLY" if verdict == "RESULT_SAVE_PROPOSAL_READY" else "VIEW_ONLY_BLOCKED"
    cards = [{"proposal_id": f"SAVE_PROPOSAL:{data.mission_id}:{i+1}", "target": t, "target_label": t, "preview_only": True, "write_authorized": False, "required_future_authority": _future_auth(t), "evidence_refs": list(data.evidence_refs)} for i,t in enumerate(data.proposed_targets)]
    return ResultSaveProposalViewModel(VERSION, data.mission_id, data.synthesis_ref, data.synthesis_verdict, data.synthesis_preview_id, data.route_result_preview_id, verdict, AUTHORITY_SCOPE, execution, data.synthetic_summary_preview, cards, list(data.proposed_targets), list(data.view_surfaces), list(data.evidence_refs), list(data.governor_snapshot_refs), dict(data.review_policy_flags), dict(data.blocked_capabilities), data.operator_review_ref, reason, "Operator may inspect proposal cards; future writes require separate authority.", data.followup_prompt_preview)

def build_fixture_result_save_proposal_input(**overrides: Any) -> ResultSaveProposalInput:
    base = ResultSaveProposalInput(
        mission_id="M-067", synthesis_ref="V66_SYNTHETIC_SYNTHESIS_PREVIEW:M-066", synthesis_verdict="SYNTHETIC_SYNTHESIS_PREVIEW_READY", upstream_execution_mode="SYNTHESIS_ROUTE_PREVIEW_ONLY", synthesis_preview_id="SYNTHETIC_SYNTHESIS_PREVIEW:M-066", route_result_preview_id="ROUTE_RESULT_PREVIEW:M-066", synthetic_summary_preview="Synthetic synthesis preview only; no provider was contacted.", proposed_targets=["MEMORY_DRY_RUN_PROPOSAL","DOCUMENT_DRAFT_SAVE_PREVIEW","ARTIFACT_EXPORT_PREVIEW","FOLLOWUP_MISSION_DRAFT_PREVIEW"], review_policy_flags={"operator_review_required": True, "no_auto_save": True, "no_memory_write": True, "no_document_write": True, "no_artifact_export": True, "no_graph_commit": True}, evidence_refs=["V66_SYNTHETIC_SYNTHESIS_PREVIEW:M-066", "V66_ROUTE_RESULT_PREVIEW:M-066"], governor_snapshot_refs=["V58_BUDGET_GOVERNOR:ok", "V58_API_RATE_GOVERNOR:ok"], operator_review_ref="OPERATOR_REVIEW_REQUIRED:M-067", followup_prompt_preview="Prepare future live dispatch only after authority is granted.")
    values = asdict(base); values.update(overrides); return ResultSaveProposalInput(**values)

def validate_result_save_proposal_view_model(model: ResultSaveProposalViewModel) -> Dict[str, Any]:
    findings: List[str] = []
    for attr in ("production_authority","live_dispatch_claim","live_write_claim","external_model_call_authorized","real_provider_output_claim","browser_session_mutation_authorized","credential_access_authorized","memory_write_authorized","document_write_authorized","artifact_export_authorized","canonical_graph_write_authorized","source_summary_rewrite_authorized"):
        if getattr(model, attr): findings.append(attr + "_must_be_false")
    if model.version != VERSION: findings.append("invalid_version")
    if model.authority_scope != AUTHORITY_SCOPE: findings.append("invalid_authority_scope")
    missing = [s for s in REQUIRED_VIEW_SURFACES if s not in model.view_surfaces]
    if missing: findings.append("missing_view_surfaces:" + ",".join(missing))
    findings.extend(_forbidden_findings(model.blocked_capabilities)); findings.extend(_review_findings(model.review_policy_flags)); findings.extend(_target_findings(model.proposed_targets))
    if model.save_proposal_verdict == "RESULT_SAVE_PROPOSAL_READY" and model.execution_mode != "SAVE_PROPOSAL_PREVIEW_ONLY": findings.append("ready_state_requires_save_proposal_preview_only")
    if model.save_proposal_verdict.startswith("BLOCKED") and model.execution_mode != "VIEW_ONLY_BLOCKED": findings.append("blocked_state_requires_view_only_blocked")
    for c in model.proposal_cards:
        if c.get("preview_only") is not True: findings.append("proposal_card_preview_only_must_be_true")
        if c.get("write_authorized") is not False: findings.append("proposal_card_write_authorized_must_be_false")
    return {"version": VERSION, "validation_verdict": "VALID_RESULT_SAVE_PROPOSAL_VIEW_MODEL" if not findings else "INVALID_RESULT_SAVE_PROPOSAL_VIEW_MODEL", "authority_scope": AUTHORITY_SCOPE, "save_proposal_verdict": model.save_proposal_verdict, "execution_mode": model.execution_mode, "proposal_card_count": len(model.proposal_cards), "proposed_target_count": len(model.proposed_targets), "view_surface_count": len(model.view_surfaces), "review_policy_flag_count": len(model.review_policy_flags), "findings": findings, "production_authority": False, "live_dispatch_claim": False, "live_write_claim": False, "memory_write_authorized": False, "document_write_authorized": False, "artifact_export_authorized": False, "canonical_graph_write_authorized": False}

if __name__ == "__main__":
    m = build_result_save_proposal_view_model(build_fixture_result_save_proposal_input())
    print(m.to_dict())
    print(validate_result_save_proposal_view_model(m))
