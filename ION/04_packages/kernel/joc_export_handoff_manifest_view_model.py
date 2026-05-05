"""V68 JOC operator-reviewed export/handoff manifest preview view model.

Binds V67 result-save proposal preview to a non-writing, non-exporting
handoff manifest preview. It does not create files, write memory, export
artifacts, mutate graph state, transfer data externally, or claim provider truth.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Mapping

VERSION = "V68_OPERATOR_REVIEWED_EXPORT_HANDOFF_MANIFEST_PREVIEW"
AUTHORITY_SCOPE = "EXPORT_HANDOFF_MANIFEST_PREVIEW_RECEIPT_ONLY"

REQUIRED_SAVE_PROPOSAL_VERDICTS = {"RESULT_SAVE_PROPOSAL_READY"}
REQUIRED_UPSTREAM_EXECUTION_MODES = {"SAVE_PROPOSAL_PREVIEW_ONLY"}

REQUIRED_MANIFEST_SECTIONS = (
    "MISSION_SUMMARY",
    "SYNTHETIC_RESULT_BOUNDARY",
    "SAVE_PROPOSAL_CARDS",
    "EVIDENCE_REFS",
    "GOVERNOR_SNAPSHOT_REFS",
    "BLOCKED_CAPABILITIES",
    "FUTURE_AUTHORITY_REQUIREMENTS",
    "OPERATOR_DECISION_LANE",
)

REQUIRED_VIEW_SURFACES = (
    "EXPORT_HANDOFF_MANIFEST_PANEL",
    "MANIFEST_SECTION_RAIL",
    "SAVE_PROPOSAL_REFERENCE_RAIL",
    "EVIDENCE_REFERENCE_TABLE",
    "GOVERNOR_SNAPSHOT_STRIP",
    "NO_EXPORT_BOUNDARY_STRIP",
    "FUTURE_AUTHORITY_REQUIREMENTS_RAIL",
    "OPERATOR_DECISION_LANE",
)

REQUIRED_REVIEW_FLAGS = (
    "operator_review_required",
    "manifest_preview_only",
    "no_file_write",
    "no_artifact_export",
    "no_memory_write",
    "no_external_transfer",
    "no_graph_commit",
)

FORBIDDEN_EXPORT_CAPABILITIES = {
    "external_model_call": False,
    "real_provider_output_claim": False,
    "live_dispatch": False,
    "browser_session_mutation": False,
    "credential_access": False,
    "memory_write": False,
    "document_write": False,
    "artifact_export": False,
    "file_system_write": False,
    "zip_creation": False,
    "external_transfer": False,
    "canonical_graph_write": False,
    "source_summary_rewrite": False,
    "form_submission": False,
    "paid_cloud_launch": False,
    "unrestricted_agent_activation": False,
    "production_authority": False,
}

ALLOWED_HANDOFF_INTENTS = (
    "USER_REVIEW_PREVIEW",
    "FUTURE_AGENT_REVIEW_PACKET_PREVIEW",
    "FUTURE_DOCUMENT_DRAFT_PREVIEW",
    "FUTURE_MEMORY_DRY_RUN_PREVIEW",
    "FUTURE_RELEASE_NOTE_DRAFT_PREVIEW",
)

@dataclass(frozen=True)
class ExportHandoffManifestInput:
    mission_id: str
    result_save_proposal_ref: str
    result_save_proposal_verdict: str
    upstream_execution_mode: str
    synthetic_summary_preview: str
    save_proposal_card_refs: List[str]
    manifest_sections: List[str]
    evidence_refs: List[str]
    governor_snapshot_refs: List[str]
    operator_review_ref: str
    handoff_intents: List[str]
    review_policy_flags: Mapping[str, bool]
    live_export_requested: bool = False
    file_write_requested: bool = False
    zip_creation_requested: bool = False
    external_transfer_requested: bool = False
    memory_write_requested: bool = False
    document_write_requested: bool = False
    artifact_export_requested: bool = False
    canonical_graph_write_requested: bool = False
    source_summary_rewrite_requested: bool = False
    view_surfaces: List[str] = field(default_factory=lambda: list(REQUIRED_VIEW_SURFACES))
    blocked_capabilities: Mapping[str, bool] = field(default_factory=lambda: FORBIDDEN_EXPORT_CAPABILITIES.copy())

@dataclass(frozen=True)
class ExportHandoffManifestViewModel:
    version: str
    mission_id: str
    result_save_proposal_ref: str
    result_save_proposal_verdict: str
    handoff_manifest_verdict: str
    authority_scope: str
    execution_mode: str
    manifest_preview_id: str
    manifest_sections: List[Mapping[str, Any]]
    synthetic_summary_preview: str
    save_proposal_card_refs: List[str]
    handoff_intents: List[str]
    view_surfaces: List[str]
    evidence_refs: List[str]
    governor_snapshot_refs: List[str]
    review_policy_flags: Mapping[str, bool]
    blocked_capabilities: Mapping[str, bool]
    operator_review_ref: str
    operator_reason: str
    next_required_action: str
    production_authority: bool = False
    live_dispatch_claim: bool = False
    live_write_claim: bool = False
    live_export_claim: bool = False
    external_model_call_authorized: bool = False
    real_provider_output_claim: bool = False
    browser_session_mutation_authorized: bool = False
    credential_access_authorized: bool = False
    memory_write_authorized: bool = False
    document_write_authorized: bool = False
    artifact_export_authorized: bool = False
    file_system_write_authorized: bool = False
    zip_creation_authorized: bool = False
    external_transfer_authorized: bool = False
    canonical_graph_write_authorized: bool = False
    source_summary_rewrite_authorized: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _missing(v: Any) -> bool:
    return v is None or v == "" or v == [] or v == {}


def _forbidden_findings(blocked: Mapping[str, bool]) -> List[str]:
    findings: List[str] = []
    for key, expected in FORBIDDEN_EXPORT_CAPABILITIES.items():
        if blocked.get(key) is not expected:
            findings.append(f"forbidden export capability {key!r} expected {expected!r} got {blocked.get(key)!r}")
    for key, value in blocked.items():
        if value is not False:
            findings.append(f"export capability {key!r} is not blocked")
    return findings


def _review_findings(flags: Mapping[str, bool]) -> List[str]:
    return [f"review_policy_{name}_must_be_true" for name in REQUIRED_REVIEW_FLAGS if flags.get(name) is not True]


def _section_findings(sections: List[str]) -> List[str]:
    allowed = set(REQUIRED_MANIFEST_SECTIONS)
    findings = [f"manifest_section_{section}_not_allowed" for section in sections if section not in allowed]
    missing = [section for section in REQUIRED_MANIFEST_SECTIONS if section not in sections]
    findings.extend(f"manifest_section_{section}_missing" for section in missing)
    return findings


def _intent_findings(intents: List[str]) -> List[str]:
    allowed = set(ALLOWED_HANDOFF_INTENTS)
    return [f"handoff_intent_{intent}_not_allowed" for intent in intents if intent not in allowed]


def _future_authority_for_section(section: str) -> str:
    return {
        "MISSION_SUMMARY": "FUTURE_HANDOFF_EXPORT_AUTHORITY_REQUIRED",
        "SYNTHETIC_RESULT_BOUNDARY": "FUTURE_REAL_OUTPUT_AUTHORITY_REQUIRED_BEFORE_TRUTH_CLAIMS",
        "SAVE_PROPOSAL_CARDS": "FUTURE_SAVE_AUTHORITY_REQUIRED",
        "EVIDENCE_REFS": "FUTURE_EVIDENCE_PACKAGE_AUTHORITY_REQUIRED",
        "GOVERNOR_SNAPSHOT_REFS": "FUTURE_GOVERNOR_SNAPSHOT_EXPORT_AUTHORITY_REQUIRED",
        "BLOCKED_CAPABILITIES": "FUTURE_CAPABILITY_UNBLOCK_AUTHORITY_REQUIRED",
        "FUTURE_AUTHORITY_REQUIREMENTS": "FUTURE_AUTHORITY_REVIEW_REQUIRED",
        "OPERATOR_DECISION_LANE": "FUTURE_OPERATOR_DECISION_AUTHORITY_REQUIRED",
    }.get(section, "FUTURE_HANDOFF_AUTHORITY_REQUIRED")


def build_export_handoff_manifest_view_model(data: ExportHandoffManifestInput | Mapping[str, Any]) -> ExportHandoffManifestViewModel:
    if isinstance(data, Mapping):
        data = ExportHandoffManifestInput(**dict(data))

    missing = [
        name for name in (
            "mission_id",
            "result_save_proposal_ref",
            "result_save_proposal_verdict",
            "upstream_execution_mode",
            "synthetic_summary_preview",
            "operator_review_ref",
        ) if _missing(getattr(data, name))
    ]
    if not data.save_proposal_card_refs:
        missing.append("save_proposal_card_refs")
    if not data.manifest_sections:
        missing.append("manifest_sections")
    if not data.evidence_refs:
        missing.append("evidence_refs")
    if not data.governor_snapshot_refs:
        missing.append("governor_snapshot_refs")
    if not data.handoff_intents:
        missing.append("handoff_intents")
    if not data.review_policy_flags:
        missing.append("review_policy_flags")

    forbidden = _forbidden_findings(data.blocked_capabilities)
    review = _review_findings(data.review_policy_flags)
    sections = _section_findings(data.manifest_sections)
    intents = _intent_findings(data.handoff_intents)

    if data.live_export_requested:
        verdict, reason = "BLOCKED_LIVE_EXPORT_REQUESTED", "Live export requested; V68 is manifest preview only."
    elif data.file_write_requested:
        verdict, reason = "BLOCKED_FILE_WRITE_REQUESTED", "File write requested; V68 cannot write files."
    elif data.zip_creation_requested:
        verdict, reason = "BLOCKED_ZIP_CREATION_REQUESTED", "Zip/package creation requested; V68 cannot create packages."
    elif data.external_transfer_requested:
        verdict, reason = "BLOCKED_EXTERNAL_TRANSFER_REQUESTED", "External transfer requested; V68 cannot transfer data."
    elif data.memory_write_requested:
        verdict, reason = "BLOCKED_MEMORY_WRITE_REQUESTED", "Memory write requested; V68 cannot write memory."
    elif data.document_write_requested:
        verdict, reason = "BLOCKED_DOCUMENT_WRITE_REQUESTED", "Document write requested; V68 cannot write documents."
    elif data.artifact_export_requested:
        verdict, reason = "BLOCKED_ARTIFACT_EXPORT_REQUESTED", "Artifact export requested; V68 cannot export artifacts."
    elif data.canonical_graph_write_requested:
        verdict, reason = "BLOCKED_CANONICAL_GRAPH_WRITE_REQUESTED", "Canonical graph write requested; V68 cannot commit graph state."
    elif data.source_summary_rewrite_requested:
        verdict, reason = "BLOCKED_SOURCE_SUMMARY_REWRITE_REQUESTED", "Source-summary rewrite requested; V68 cannot rewrite summaries."
    elif missing:
        verdict, reason = "BLOCKED_MISSING_HANDOFF_EVIDENCE", "Missing handoff-manifest evidence: " + ", ".join(missing) + "."
    elif data.result_save_proposal_verdict not in REQUIRED_SAVE_PROPOSAL_VERDICTS or data.upstream_execution_mode not in REQUIRED_UPSTREAM_EXECUTION_MODES:
        verdict, reason = "BLOCKED_SAVE_PROPOSAL_NOT_READY", "V67 result-save proposal is not ready for handoff manifest preview."
    elif forbidden:
        verdict, reason = "BLOCKED_FORBIDDEN_EXPORT_CAPABILITY", "Forbidden export capability evidence detected: " + ", ".join(forbidden) + "."
    elif review:
        verdict, reason = "BLOCKED_MISSING_OPERATOR_REVIEW_POLICY", "Operator review policy missing: " + ", ".join(review) + "."
    elif sections:
        verdict, reason = "BLOCKED_INVALID_MANIFEST_SECTION", "Manifest section issue: " + ", ".join(sections) + "."
    elif intents:
        verdict, reason = "BLOCKED_INVALID_HANDOFF_INTENT", "Invalid handoff intent: " + ", ".join(intents) + "."
    else:
        verdict, reason = "HANDOFF_MANIFEST_PREVIEW_READY", "V67 save proposal may be rendered as a non-writing handoff manifest preview only."

    execution = "HANDOFF_MANIFEST_PREVIEW_ONLY" if verdict == "HANDOFF_MANIFEST_PREVIEW_READY" else "VIEW_ONLY_BLOCKED"
    manifest_preview_id = f"HANDOFF_MANIFEST_PREVIEW:{data.mission_id}"
    section_cards = [
        {
            "section_id": f"{manifest_preview_id}:{idx+1}",
            "section": section,
            "preview_only": True,
            "materialized": False,
            "write_authorized": False,
            "export_authorized": False,
            "required_future_authority": _future_authority_for_section(section),
            "evidence_refs": list(data.evidence_refs),
        }
        for idx, section in enumerate(data.manifest_sections)
    ]

    return ExportHandoffManifestViewModel(
        version=VERSION,
        mission_id=data.mission_id,
        result_save_proposal_ref=data.result_save_proposal_ref,
        result_save_proposal_verdict=data.result_save_proposal_verdict,
        handoff_manifest_verdict=verdict,
        authority_scope=AUTHORITY_SCOPE,
        execution_mode=execution,
        manifest_preview_id=manifest_preview_id,
        manifest_sections=section_cards,
        synthetic_summary_preview=data.synthetic_summary_preview,
        save_proposal_card_refs=list(data.save_proposal_card_refs),
        handoff_intents=list(data.handoff_intents),
        view_surfaces=list(data.view_surfaces),
        evidence_refs=list(data.evidence_refs),
        governor_snapshot_refs=list(data.governor_snapshot_refs),
        review_policy_flags=dict(data.review_policy_flags),
        blocked_capabilities=dict(data.blocked_capabilities),
        operator_review_ref=data.operator_review_ref,
        operator_reason=reason,
        next_required_action="Operator may inspect manifest sections; future materialization/export requires separate authority.",
    )


def build_fixture_export_handoff_manifest_input(**overrides: Any) -> ExportHandoffManifestInput:
    base = ExportHandoffManifestInput(
        mission_id="M-068",
        result_save_proposal_ref="SAVE_PROPOSAL:M-067",
        result_save_proposal_verdict="RESULT_SAVE_PROPOSAL_READY",
        upstream_execution_mode="SAVE_PROPOSAL_PREVIEW_ONLY",
        synthetic_summary_preview="Synthetic synthesis preview only; no provider was contacted and no result truth is claimed.",
        save_proposal_card_refs=["SAVE_PROPOSAL:M-067:1", "SAVE_PROPOSAL:M-067:2", "SAVE_PROPOSAL:M-067:3"],
        manifest_sections=list(REQUIRED_MANIFEST_SECTIONS),
        evidence_refs=["V66_SYNTHETIC_SYNTHESIS_PREVIEW:M-066", "V67_RESULT_SAVE_PROPOSAL:M-067"],
        governor_snapshot_refs=["V58_BUDGET_GOVERNOR:ok", "V58_API_RATE_GOVERNOR:ok"],
        operator_review_ref="OPERATOR_REVIEW_REQUIRED:M-068",
        handoff_intents=["USER_REVIEW_PREVIEW", "FUTURE_AGENT_REVIEW_PACKET_PREVIEW", "FUTURE_RELEASE_NOTE_DRAFT_PREVIEW"],
        review_policy_flags={
            "operator_review_required": True,
            "manifest_preview_only": True,
            "no_file_write": True,
            "no_artifact_export": True,
            "no_memory_write": True,
            "no_external_transfer": True,
            "no_graph_commit": True,
        },
    )
    values = asdict(base)
    values.update(overrides)
    return ExportHandoffManifestInput(**values)


def validate_export_handoff_manifest_view_model(model: ExportHandoffManifestViewModel) -> Dict[str, Any]:
    findings: List[str] = []
    false_attrs = (
        "production_authority",
        "live_dispatch_claim",
        "live_write_claim",
        "live_export_claim",
        "external_model_call_authorized",
        "real_provider_output_claim",
        "browser_session_mutation_authorized",
        "credential_access_authorized",
        "memory_write_authorized",
        "document_write_authorized",
        "artifact_export_authorized",
        "file_system_write_authorized",
        "zip_creation_authorized",
        "external_transfer_authorized",
        "canonical_graph_write_authorized",
        "source_summary_rewrite_authorized",
    )
    for attr in false_attrs:
        if getattr(model, attr):
            findings.append(attr + "_must_be_false")
    if model.version != VERSION:
        findings.append("invalid_version")
    if model.authority_scope != AUTHORITY_SCOPE:
        findings.append("invalid_authority_scope")
    missing_surfaces = [surface for surface in REQUIRED_VIEW_SURFACES if surface not in model.view_surfaces]
    if missing_surfaces:
        findings.append("missing_view_surfaces:" + ",".join(missing_surfaces))
    findings.extend(_forbidden_findings(model.blocked_capabilities))
    findings.extend(_review_findings(model.review_policy_flags))
    findings.extend(_intent_findings(model.handoff_intents))
    if model.handoff_manifest_verdict == "HANDOFF_MANIFEST_PREVIEW_READY" and model.execution_mode != "HANDOFF_MANIFEST_PREVIEW_ONLY":
        findings.append("ready_state_requires_handoff_manifest_preview_only")
    if model.handoff_manifest_verdict.startswith("BLOCKED") and model.execution_mode != "VIEW_ONLY_BLOCKED":
        findings.append("blocked_state_requires_view_only_blocked")
    for section in model.manifest_sections:
        if section.get("preview_only") is not True:
            findings.append("manifest_section_preview_only_must_be_true")
        if section.get("materialized") is not False:
            findings.append("manifest_section_materialized_must_be_false")
        if section.get("write_authorized") is not False:
            findings.append("manifest_section_write_authorized_must_be_false")
        if section.get("export_authorized") is not False:
            findings.append("manifest_section_export_authorized_must_be_false")
    return {
        "version": VERSION,
        "validation_verdict": "VALID_EXPORT_HANDOFF_MANIFEST_VIEW_MODEL" if not findings else "INVALID_EXPORT_HANDOFF_MANIFEST_VIEW_MODEL",
        "authority_scope": AUTHORITY_SCOPE,
        "handoff_manifest_verdict": model.handoff_manifest_verdict,
        "execution_mode": model.execution_mode,
        "manifest_preview_id": model.manifest_preview_id,
        "manifest_section_count": len(model.manifest_sections),
        "save_proposal_ref_count": len(model.save_proposal_card_refs),
        "handoff_intent_count": len(model.handoff_intents),
        "view_surface_count": len(model.view_surfaces),
        "findings": findings,
        "production_authority": False,
        "live_dispatch_claim": False,
        "live_write_claim": False,
        "live_export_claim": False,
        "memory_write_authorized": False,
        "document_write_authorized": False,
        "artifact_export_authorized": False,
        "file_system_write_authorized": False,
        "zip_creation_authorized": False,
        "external_transfer_authorized": False,
        "canonical_graph_write_authorized": False,
    }


if __name__ == "__main__":
    model = build_export_handoff_manifest_view_model(build_fixture_export_handoff_manifest_input())
    print(model.to_dict())
    print(validate_export_handoff_manifest_view_model(model))
