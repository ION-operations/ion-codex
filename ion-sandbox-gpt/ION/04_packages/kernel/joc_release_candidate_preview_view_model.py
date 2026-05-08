"""V70 JOC release-candidate preview and preflight verifier view model.

Binds the V69 handoff package assembly plan to a release-candidate preview and
preflight verifier checklist. It does not create release archives, write files,
read source bytes for real checksums, export artifacts, transfer externally,
mutate memory or graph state, or claim production authority.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Mapping

VERSION = "V70_RELEASE_CANDIDATE_PREVIEW_AND_PREFLIGHT_VERIFIER_VIEW_MODEL"
AUTHORITY_SCOPE = "RELEASE_CANDIDATE_PREVIEW_AND_PREFLIGHT_VERIFIER_RECEIPT_ONLY"

REQUIRED_PACKAGE_PLAN_VERDICTS = {"PACKAGE_ASSEMBLY_PLAN_PREVIEW_READY"}
REQUIRED_UPSTREAM_EXECUTION_MODES = {"PACKAGE_ASSEMBLY_PLAN_PREVIEW_ONLY"}

REQUIRED_RC_SECTIONS = (
    "RELEASE_SUMMARY",
    "PACKAGE_PLAN_REF",
    "CHECKSUM_PREVIEW_LEDGER",
    "EVIDENCE_BUNDLE_INDEX_PREVIEW",
    "OPERATOR_ACCEPTANCE_CRITERIA",
    "PREFLIGHT_VERIFIER_CHECKLIST",
    "BLOCKED_CAPABILITIES",
    "FUTURE_RELEASE_AUTHORITY_REQUIREMENTS",
)

REQUIRED_PREFLIGHT_CHECKS = (
    "package_plan_ready",
    "checksum_previews_present",
    "evidence_refs_present",
    "operator_review_lane_present",
    "blocked_capabilities_preserved",
    "no_file_write_authority",
    "no_zip_creation_authority",
    "no_external_transfer_authority",
    "no_production_authority",
)

REQUIRED_VIEW_SURFACES = (
    "RELEASE_CANDIDATE_PREVIEW_PANEL",
    "PREFLIGHT_VERIFIER_CHECKLIST_RAIL",
    "CHECKSUM_PREVIEW_LEDGER_TABLE",
    "PACKAGE_PLAN_REFERENCE_STRIP",
    "EVIDENCE_BUNDLE_INDEX_PREVIEW",
    "OPERATOR_ACCEPTANCE_CRITERIA_RAIL",
    "BLOCKED_CAPABILITY_LEDGER",
    "FUTURE_RELEASE_AUTHORITY_RAIL",
)

REQUIRED_REVIEW_FLAGS = (
    "operator_review_required",
    "release_candidate_preview_only",
    "preflight_verifier_preview_only",
    "no_release_archive_creation",
    "no_file_write",
    "no_zip_creation",
    "no_real_checksum_claim",
    "no_artifact_export",
    "no_external_transfer",
    "no_memory_write",
    "no_graph_commit",
    "no_source_summary_rewrite",
    "no_production_authority",
)

FORBIDDEN_RC_CAPABILITIES = {
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
    "checksum_file_write": False,
    "release_archive_creation": False,
    "package_materialization": False,
    "external_transfer": False,
    "canonical_graph_write": False,
    "source_summary_rewrite": False,
    "form_submission": False,
    "paid_cloud_launch": False,
    "unrestricted_agent_activation": False,
    "production_authority": False,
}

ALLOWED_RC_INTENTS = (
    "USER_REVIEW_RELEASE_CANDIDATE_PREVIEW",
    "FUTURE_AGENT_HANDOFF_RELEASE_PREVIEW",
    "FUTURE_RELEASE_ARCHIVE_PREVIEW",
    "FUTURE_PREFLIGHT_VERIFIER_REHEARSAL",
)

@dataclass(frozen=True)
class ReleaseCandidatePreviewInput:
    mission_id: str
    package_plan_ref: str
    package_plan_verdict: str
    upstream_execution_mode: str
    package_plan_id: str
    release_intents: List[str]
    release_sections: List[str]
    package_item_refs: List[str]
    checksum_preview_records: List[Mapping[str, Any]]
    evidence_refs: List[str]
    operator_review_ref: str
    review_policy_flags: Mapping[str, bool]
    preflight_checks: List[str] = field(default_factory=lambda: list(REQUIRED_PREFLIGHT_CHECKS))
    live_release_requested: bool = False
    release_archive_creation_requested: bool = False
    file_write_requested: bool = False
    zip_creation_requested: bool = False
    checksum_file_write_requested: bool = False
    artifact_export_requested: bool = False
    external_transfer_requested: bool = False
    memory_write_requested: bool = False
    canonical_graph_write_requested: bool = False
    source_summary_rewrite_requested: bool = False
    production_authority_requested: bool = False
    view_surfaces: List[str] = field(default_factory=lambda: list(REQUIRED_VIEW_SURFACES))
    blocked_capabilities: Mapping[str, bool] = field(default_factory=lambda: FORBIDDEN_RC_CAPABILITIES.copy())

@dataclass(frozen=True)
class ReleaseCandidatePreviewViewModel:
    version: str
    mission_id: str
    package_plan_ref: str
    package_plan_verdict: str
    release_candidate_preview_verdict: str
    authority_scope: str
    execution_mode: str
    release_candidate_preview_id: str
    package_plan_id: str
    release_intents: List[str]
    release_sections: List[Mapping[str, Any]]
    package_item_refs: List[str]
    checksum_preview_ledger: List[Mapping[str, Any]]
    preflight_verifier_checklist: List[Mapping[str, Any]]
    evidence_refs: List[str]
    view_surfaces: List[str]
    review_policy_flags: Mapping[str, bool]
    blocked_capabilities: Mapping[str, bool]
    operator_review_ref: str
    operator_reason: str
    next_required_action: str
    production_authority: bool = False
    live_dispatch_claim: bool = False
    live_write_claim: bool = False
    live_export_claim: bool = False
    live_package_claim: bool = False
    live_release_claim: bool = False
    external_model_call_authorized: bool = False
    real_provider_output_claim: bool = False
    browser_session_mutation_authorized: bool = False
    credential_access_authorized: bool = False
    memory_write_authorized: bool = False
    document_write_authorized: bool = False
    artifact_export_authorized: bool = False
    file_system_write_authorized: bool = False
    zip_creation_authorized: bool = False
    checksum_file_write_authorized: bool = False
    release_archive_creation_authorized: bool = False
    package_materialization_authorized: bool = False
    external_transfer_authorized: bool = False
    canonical_graph_write_authorized: bool = False
    source_summary_rewrite_authorized: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _missing(v: Any) -> bool:
    return v is None or v == "" or v == [] or v == {}


def _forbidden_findings(blocked: Mapping[str, bool]) -> List[str]:
    findings: List[str] = []
    for key, expected in FORBIDDEN_RC_CAPABILITIES.items():
        if blocked.get(key) is not expected:
            findings.append(f"forbidden rc capability {key!r} expected {expected!r} got {blocked.get(key)!r}")
    for key, value in blocked.items():
        if value is not False:
            findings.append(f"rc capability {key!r} is not blocked")
    return findings


def _review_findings(flags: Mapping[str, bool]) -> List[str]:
    return [f"review_policy_{name}_must_be_true" for name in REQUIRED_REVIEW_FLAGS if flags.get(name) is not True]


def _section_findings(sections: List[str]) -> List[str]:
    allowed = set(REQUIRED_RC_SECTIONS)
    findings = [f"release_section_{section}_not_allowed" for section in sections if section not in allowed]
    missing = [section for section in REQUIRED_RC_SECTIONS if section not in sections]
    findings.extend(f"release_section_{section}_missing" for section in missing)
    return findings


def _intent_findings(intents: List[str]) -> List[str]:
    allowed = set(ALLOWED_RC_INTENTS)
    return [f"release_intent_{intent}_not_allowed" for intent in intents if intent not in allowed]


def _preflight_findings(checks: List[str]) -> List[str]:
    allowed = set(REQUIRED_PREFLIGHT_CHECKS)
    findings = [f"preflight_check_{check}_not_allowed" for check in checks if check not in allowed]
    missing = [check for check in REQUIRED_PREFLIGHT_CHECKS if check not in checks]
    findings.extend(f"preflight_check_{check}_missing" for check in missing)
    return findings


def _checksum_preview_findings(records: List[Mapping[str, Any]]) -> List[str]:
    findings: List[str] = []
    if not records:
        return ["checksum_preview_records_missing"]
    for idx, record in enumerate(records):
        if _missing(record.get("checksum_preview_id")):
            findings.append(f"checksum_preview_{idx}_id_missing")
        if _missing(record.get("checksum_preview")):
            findings.append(f"checksum_preview_{idx}_value_missing")
        if record.get("real_checksum_claim") is not False:
            findings.append(f"checksum_preview_{idx}_real_checksum_claim_must_be_false")
        if record.get("checksum_file_written") is not False:
            findings.append(f"checksum_preview_{idx}_checksum_file_written_must_be_false")
        if record.get("source_bytes_read") is not False:
            findings.append(f"checksum_preview_{idx}_source_bytes_read_must_be_false")
    return findings


def _future_authority_for_section(section: str) -> str:
    return {
        "RELEASE_SUMMARY": "FUTURE_RELEASE_CANDIDATE_AUTHORITY_REQUIRED",
        "PACKAGE_PLAN_REF": "FUTURE_PACKAGE_PLAN_MATERIALIZATION_AUTHORITY_REQUIRED",
        "CHECKSUM_PREVIEW_LEDGER": "FUTURE_REAL_CHECKSUM_AUTHORITY_REQUIRED",
        "EVIDENCE_BUNDLE_INDEX_PREVIEW": "FUTURE_EVIDENCE_BUNDLE_ASSEMBLY_AUTHORITY_REQUIRED",
        "OPERATOR_ACCEPTANCE_CRITERIA": "FUTURE_OPERATOR_RELEASE_ACCEPTANCE_AUTHORITY_REQUIRED",
        "PREFLIGHT_VERIFIER_CHECKLIST": "FUTURE_RELEASE_VERIFIER_AUTHORITY_REQUIRED",
        "BLOCKED_CAPABILITIES": "FUTURE_BOUNDARY_AUDIT_AUTHORITY_REQUIRED",
        "FUTURE_RELEASE_AUTHORITY_REQUIREMENTS": "FUTURE_RELEASE_AUTHORITY_RATIFICATION_REQUIRED",
    }.get(section, "FUTURE_RELEASE_AUTHORITY_REQUIRED")


def _build_release_section_cards(sections: List[str], evidence_refs: List[str], preview_id: str) -> List[Dict[str, Any]]:
    return [
        {
            "section_id": f"{preview_id}:{idx+1}",
            "section": section,
            "preview_only": True,
            "materialized": False,
            "write_authorized": False,
            "release_authorized": False,
            "required_future_authority": _future_authority_for_section(section),
            "evidence_refs": list(evidence_refs),
        }
        for idx, section in enumerate(sections)
    ]


def _build_preflight_checklist(checks: List[str], preview_id: str) -> List[Dict[str, Any]]:
    return [
        {
            "check_id": f"{preview_id}:CHECK:{idx+1}",
            "check": check,
            "preview_status": "WOULD_CHECK",
            "passed_claim": False,
            "executed": False,
            "requires_future_authority": "FUTURE_PREFLIGHT_VERIFIER_EXECUTION_AUTHORITY_REQUIRED",
        }
        for idx, check in enumerate(checks)
    ]


def build_release_candidate_preview_view_model(data: ReleaseCandidatePreviewInput | Mapping[str, Any]) -> ReleaseCandidatePreviewViewModel:
    if isinstance(data, Mapping):
        data = ReleaseCandidatePreviewInput(**dict(data))

    missing = [name for name in (
        "mission_id",
        "package_plan_ref",
        "package_plan_verdict",
        "upstream_execution_mode",
        "package_plan_id",
        "operator_review_ref",
    ) if _missing(getattr(data, name))]
    if not data.release_intents:
        missing.append("release_intents")
    if not data.release_sections:
        missing.append("release_sections")
    if not data.package_item_refs:
        missing.append("package_item_refs")
    if not data.checksum_preview_records:
        missing.append("checksum_preview_records")
    if not data.evidence_refs:
        missing.append("evidence_refs")
    if not data.review_policy_flags:
        missing.append("review_policy_flags")

    forbidden = _forbidden_findings(data.blocked_capabilities)
    review = _review_findings(data.review_policy_flags)
    sections = _section_findings(data.release_sections)
    intents = _intent_findings(data.release_intents)
    preflight = _preflight_findings(data.preflight_checks)
    checksum = _checksum_preview_findings(data.checksum_preview_records)

    if data.live_release_requested:
        verdict, reason = "BLOCKED_LIVE_RELEASE_REQUESTED", "Live release requested; V70 is release-candidate preview only."
    elif data.release_archive_creation_requested:
        verdict, reason = "BLOCKED_RELEASE_ARCHIVE_CREATION_REQUESTED", "Release archive creation requested; V70 cannot create release archives."
    elif data.file_write_requested:
        verdict, reason = "BLOCKED_FILE_WRITE_REQUESTED", "File write requested; V70 cannot write files."
    elif data.zip_creation_requested:
        verdict, reason = "BLOCKED_ZIP_CREATION_REQUESTED", "Zip creation requested; V70 cannot create zips."
    elif data.checksum_file_write_requested:
        verdict, reason = "BLOCKED_CHECKSUM_FILE_WRITE_REQUESTED", "Checksum file write requested; V70 cannot write checksum files."
    elif data.artifact_export_requested:
        verdict, reason = "BLOCKED_ARTIFACT_EXPORT_REQUESTED", "Artifact export requested; V70 cannot export artifacts."
    elif data.external_transfer_requested:
        verdict, reason = "BLOCKED_EXTERNAL_TRANSFER_REQUESTED", "External transfer requested; V70 cannot transfer data."
    elif data.memory_write_requested:
        verdict, reason = "BLOCKED_MEMORY_WRITE_REQUESTED", "Memory write requested; V70 cannot write memory."
    elif data.canonical_graph_write_requested:
        verdict, reason = "BLOCKED_CANONICAL_GRAPH_WRITE_REQUESTED", "Canonical graph write requested; V70 cannot commit graph state."
    elif data.source_summary_rewrite_requested:
        verdict, reason = "BLOCKED_SOURCE_SUMMARY_REWRITE_REQUESTED", "Source-summary rewrite requested; V70 cannot rewrite summaries."
    elif data.production_authority_requested:
        verdict, reason = "BLOCKED_PRODUCTION_AUTHORITY_REQUESTED", "Production authority requested; V70 cannot grant production authority."
    elif missing:
        verdict, reason = "BLOCKED_MISSING_RELEASE_PREVIEW_EVIDENCE", "Missing release-candidate preview evidence: " + ", ".join(missing) + "."
    elif data.package_plan_verdict not in REQUIRED_PACKAGE_PLAN_VERDICTS or data.upstream_execution_mode not in REQUIRED_UPSTREAM_EXECUTION_MODES:
        verdict, reason = "BLOCKED_PACKAGE_PLAN_NOT_READY", "V69 package plan is not ready for release-candidate preview."
    elif forbidden:
        verdict, reason = "BLOCKED_FORBIDDEN_RELEASE_CAPABILITY", "Forbidden release capability evidence detected: " + ", ".join(forbidden) + "."
    elif review:
        verdict, reason = "BLOCKED_MISSING_OPERATOR_REVIEW_POLICY", "Operator review policy missing: " + ", ".join(review) + "."
    elif sections:
        verdict, reason = "BLOCKED_INVALID_RELEASE_SECTION", "Release section issue: " + ", ".join(sections) + "."
    elif intents:
        verdict, reason = "BLOCKED_INVALID_RELEASE_INTENT", "Invalid release intent: " + ", ".join(intents) + "."
    elif preflight:
        verdict, reason = "BLOCKED_INVALID_PREFLIGHT_CHECKLIST", "Preflight checklist issue: " + ", ".join(preflight) + "."
    elif checksum:
        verdict, reason = "BLOCKED_INVALID_CHECKSUM_PREVIEW_LEDGER", "Checksum preview issue: " + ", ".join(checksum) + "."
    else:
        verdict, reason = "RELEASE_CANDIDATE_PREVIEW_READY", "V69 package plan may be rendered as a non-materializing release-candidate preview and preflight-verifier checklist only."

    execution = "RELEASE_CANDIDATE_PREVIEW_ONLY" if verdict == "RELEASE_CANDIDATE_PREVIEW_READY" else "VIEW_ONLY_BLOCKED"
    preview_id = f"RELEASE_CANDIDATE_PREVIEW:{data.mission_id}"

    return ReleaseCandidatePreviewViewModel(
        version=VERSION,
        mission_id=data.mission_id,
        package_plan_ref=data.package_plan_ref,
        package_plan_verdict=data.package_plan_verdict,
        release_candidate_preview_verdict=verdict,
        authority_scope=AUTHORITY_SCOPE,
        execution_mode=execution,
        release_candidate_preview_id=preview_id,
        package_plan_id=data.package_plan_id,
        release_intents=list(data.release_intents),
        release_sections=_build_release_section_cards(data.release_sections, data.evidence_refs, preview_id),
        package_item_refs=list(data.package_item_refs),
        checksum_preview_ledger=[dict(record) for record in data.checksum_preview_records],
        preflight_verifier_checklist=_build_preflight_checklist(data.preflight_checks, preview_id),
        evidence_refs=list(data.evidence_refs),
        view_surfaces=list(data.view_surfaces),
        review_policy_flags=dict(data.review_policy_flags),
        blocked_capabilities=dict(data.blocked_capabilities),
        operator_review_ref=data.operator_review_ref,
        operator_reason=reason,
        next_required_action="Operator may inspect release-candidate preview; real release archive creation requires separate materialization and verifier authority.",
    )


def build_fixture_release_candidate_preview_input(**overrides: Any) -> ReleaseCandidatePreviewInput:
    base = ReleaseCandidatePreviewInput(
        mission_id="M-070",
        package_plan_ref="PACKAGE_ASSEMBLY_PLAN_PREVIEW:M-069",
        package_plan_verdict="PACKAGE_ASSEMBLY_PLAN_PREVIEW_READY",
        upstream_execution_mode="PACKAGE_ASSEMBLY_PLAN_PREVIEW_ONLY",
        package_plan_id="PACKAGE_ASSEMBLY_PLAN_PREVIEW:M-069",
        release_intents=["USER_REVIEW_RELEASE_CANDIDATE_PREVIEW", "FUTURE_AGENT_HANDOFF_RELEASE_PREVIEW", "FUTURE_PREFLIGHT_VERIFIER_REHEARSAL"],
        release_sections=list(REQUIRED_RC_SECTIONS),
        package_item_refs=["ITEM:M-069:manifest", "ITEM:M-069:evidence", "ITEM:M-069:boundary"],
        checksum_preview_records=[
            {"checksum_preview_id": "CHECKSUM_PREVIEW:ITEM:M-069:manifest", "checksum_preview": "0001001", "real_checksum_claim": False, "checksum_file_written": False, "source_bytes_read": False},
            {"checksum_preview_id": "CHECKSUM_PREVIEW:ITEM:M-069:evidence", "checksum_preview": "0001002", "real_checksum_claim": False, "checksum_file_written": False, "source_bytes_read": False},
        ],
        evidence_refs=["V68_HANDOFF_MANIFEST_PREVIEW:M-068", "V69_PACKAGE_ASSEMBLY_PLAN_PREVIEW:M-069"],
        operator_review_ref="OPERATOR_REVIEW_REQUIRED:M-070",
        review_policy_flags={
            "operator_review_required": True,
            "release_candidate_preview_only": True,
            "preflight_verifier_preview_only": True,
            "no_release_archive_creation": True,
            "no_file_write": True,
            "no_zip_creation": True,
            "no_real_checksum_claim": True,
            "no_artifact_export": True,
            "no_external_transfer": True,
            "no_memory_write": True,
            "no_graph_commit": True,
            "no_source_summary_rewrite": True,
            "no_production_authority": True,
        },
    )
    values = asdict(base)
    values.update(overrides)
    return ReleaseCandidatePreviewInput(**values)


def validate_release_candidate_preview_view_model(model: ReleaseCandidatePreviewViewModel) -> Dict[str, Any]:
    findings: List[str] = []
    false_attrs = (
        "production_authority",
        "live_dispatch_claim",
        "live_write_claim",
        "live_export_claim",
        "live_package_claim",
        "live_release_claim",
        "external_model_call_authorized",
        "real_provider_output_claim",
        "browser_session_mutation_authorized",
        "credential_access_authorized",
        "memory_write_authorized",
        "document_write_authorized",
        "artifact_export_authorized",
        "file_system_write_authorized",
        "zip_creation_authorized",
        "checksum_file_write_authorized",
        "release_archive_creation_authorized",
        "package_materialization_authorized",
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
    findings.extend(_intent_findings(model.release_intents))
    if model.release_candidate_preview_verdict == "RELEASE_CANDIDATE_PREVIEW_READY" and model.execution_mode != "RELEASE_CANDIDATE_PREVIEW_ONLY":
        findings.append("ready_state_requires_release_candidate_preview_only")
    if model.release_candidate_preview_verdict.startswith("BLOCKED") and model.execution_mode != "VIEW_ONLY_BLOCKED":
        findings.append("blocked_state_requires_view_only_blocked")
    for section in model.release_sections:
        if section.get("preview_only") is not True:
            findings.append("release_section_preview_only_must_be_true")
        if section.get("materialized") is not False:
            findings.append("release_section_materialized_must_be_false")
        if section.get("write_authorized") is not False:
            findings.append("release_section_write_authorized_must_be_false")
        if section.get("release_authorized") is not False:
            findings.append("release_section_release_authorized_must_be_false")
    for record in model.checksum_preview_ledger:
        if record.get("real_checksum_claim") is not False:
            findings.append("checksum_preview_real_checksum_claim_must_be_false")
        if record.get("checksum_file_written") is not False:
            findings.append("checksum_file_written_must_be_false")
        if record.get("source_bytes_read") is not False:
            findings.append("checksum_source_bytes_read_must_be_false")
    for check in model.preflight_verifier_checklist:
        if check.get("preview_status") != "WOULD_CHECK":
            findings.append("preflight_preview_status_must_be_would_check")
        if check.get("passed_claim") is not False:
            findings.append("preflight_passed_claim_must_be_false")
        if check.get("executed") is not False:
            findings.append("preflight_executed_must_be_false")
    return {
        "version": VERSION,
        "validation_verdict": "VALID_RELEASE_CANDIDATE_PREVIEW_VIEW_MODEL" if not findings else "INVALID_RELEASE_CANDIDATE_PREVIEW_VIEW_MODEL",
        "authority_scope": AUTHORITY_SCOPE,
        "release_candidate_preview_verdict": model.release_candidate_preview_verdict,
        "execution_mode": model.execution_mode,
        "release_candidate_preview_id": model.release_candidate_preview_id,
        "release_section_count": len(model.release_sections),
        "checksum_preview_count": len(model.checksum_preview_ledger),
        "preflight_check_count": len(model.preflight_verifier_checklist),
        "view_surface_count": len(model.view_surfaces),
        "findings": findings,
        "production_authority": False,
        "live_dispatch_claim": False,
        "live_write_claim": False,
        "live_export_claim": False,
        "live_package_claim": False,
        "live_release_claim": False,
        "file_system_write_authorized": False,
        "zip_creation_authorized": False,
        "checksum_file_write_authorized": False,
        "release_archive_creation_authorized": False,
        "package_materialization_authorized": False,
        "external_transfer_authorized": False,
        "canonical_graph_write_authorized": False,
    }


if __name__ == "__main__":
    model = build_release_candidate_preview_view_model(build_fixture_release_candidate_preview_input())
    print(model.to_dict())
    print(validate_release_candidate_preview_view_model(model))
