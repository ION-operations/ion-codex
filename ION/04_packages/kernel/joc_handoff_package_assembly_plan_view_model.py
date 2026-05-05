"""V69 JOC handoff package assembly plan and checksum preview view model.

Binds V68 handoff manifest preview to a non-materializing package assembly
plan. It does not write files, create zips, emit checksum files, export
artifacts, transfer data, mutate memory, or claim production authority.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Mapping

VERSION = "V69_HANDOFF_PACKAGE_ASSEMBLY_PLAN_AND_CHECKSUM_PREVIEW"
AUTHORITY_SCOPE = "HANDOFF_PACKAGE_ASSEMBLY_PLAN_PREVIEW_RECEIPT_ONLY"

REQUIRED_HANDOFF_VERDICTS = {"HANDOFF_MANIFEST_PREVIEW_READY"}
REQUIRED_UPSTREAM_EXECUTION_MODES = {"HANDOFF_MANIFEST_PREVIEW_ONLY"}

REQUIRED_PACKAGE_SECTIONS = (
    "PACKAGE_SUMMARY",
    "ITEM_PLAN",
    "CHECKSUM_PLAN",
    "EVIDENCE_INDEX",
    "BOUNDARY_LEDGER",
    "OPERATOR_REVIEW_LANE",
    "FUTURE_MATERIALIZATION_AUTHORITY",
)

REQUIRED_VIEW_SURFACES = (
    "PACKAGE_ASSEMBLY_PLAN_PANEL",
    "PACKAGE_ITEM_TABLE",
    "CHECKSUM_PREVIEW_RAIL",
    "MANIFEST_REFERENCE_STRIP",
    "BOUNDARY_LEDGER_STRIP",
    "FUTURE_MATERIALIZATION_AUTHORITY_RAIL",
    "OPERATOR_REVIEW_LANE",
)

REQUIRED_REVIEW_FLAGS = (
    "operator_review_required",
    "package_plan_preview_only",
    "no_file_write",
    "no_zip_creation",
    "no_checksum_file_write",
    "no_artifact_export",
    "no_external_transfer",
    "no_memory_write",
    "no_graph_commit",
    "no_source_summary_rewrite",
)

FORBIDDEN_PACKAGE_CAPABILITIES = {
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
    "package_materialization": False,
    "external_transfer": False,
    "canonical_graph_write": False,
    "source_summary_rewrite": False,
    "form_submission": False,
    "paid_cloud_launch": False,
    "unrestricted_agent_activation": False,
    "production_authority": False,
}

ALLOWED_PACKAGE_INTENTS = (
    "USER_REVIEW_PACKAGE_PLAN_PREVIEW",
    "FUTURE_AGENT_HANDOFF_PACKAGE_PREVIEW",
    "FUTURE_RELEASE_PACKAGE_PREVIEW",
    "FUTURE_DOCUMENT_EXPORT_PACKAGE_PREVIEW",
)

@dataclass(frozen=True)
class PackageItemPlan:
    item_id: str
    item_kind: str
    source_ref: str
    planned_path: str
    include_in_future_package: bool = True
    materialized: bool = False
    write_authorized: bool = False
    checksum_written: bool = False

@dataclass(frozen=True)
class HandoffPackageAssemblyPlanInput:
    mission_id: str
    handoff_manifest_ref: str
    handoff_manifest_verdict: str
    upstream_execution_mode: str
    manifest_preview_id: str
    package_intents: List[str]
    package_sections: List[str]
    package_items: List[Mapping[str, Any]]
    evidence_refs: List[str]
    operator_review_ref: str
    review_policy_flags: Mapping[str, bool]
    live_package_requested: bool = False
    file_write_requested: bool = False
    zip_creation_requested: bool = False
    checksum_file_write_requested: bool = False
    artifact_export_requested: bool = False
    external_transfer_requested: bool = False
    memory_write_requested: bool = False
    canonical_graph_write_requested: bool = False
    source_summary_rewrite_requested: bool = False
    view_surfaces: List[str] = field(default_factory=lambda: list(REQUIRED_VIEW_SURFACES))
    blocked_capabilities: Mapping[str, bool] = field(default_factory=lambda: FORBIDDEN_PACKAGE_CAPABILITIES.copy())

@dataclass(frozen=True)
class HandoffPackageAssemblyPlanViewModel:
    version: str
    mission_id: str
    handoff_manifest_ref: str
    handoff_manifest_verdict: str
    package_plan_verdict: str
    authority_scope: str
    execution_mode: str
    package_plan_id: str
    manifest_preview_id: str
    package_intents: List[str]
    package_sections: List[Mapping[str, Any]]
    package_items: List[Mapping[str, Any]]
    checksum_preview_records: List[Mapping[str, Any]]
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
    for key, expected in FORBIDDEN_PACKAGE_CAPABILITIES.items():
        if blocked.get(key) is not expected:
            findings.append(f"forbidden package capability {key!r} expected {expected!r} got {blocked.get(key)!r}")
    for key, value in blocked.items():
        if value is not False:
            findings.append(f"package capability {key!r} is not blocked")
    return findings


def _review_findings(flags: Mapping[str, bool]) -> List[str]:
    return [f"review_policy_{name}_must_be_true" for name in REQUIRED_REVIEW_FLAGS if flags.get(name) is not True]


def _section_findings(sections: List[str]) -> List[str]:
    allowed = set(REQUIRED_PACKAGE_SECTIONS)
    findings = [f"package_section_{section}_not_allowed" for section in sections if section not in allowed]
    missing = [section for section in REQUIRED_PACKAGE_SECTIONS if section not in sections]
    findings.extend(f"package_section_{section}_missing" for section in missing)
    return findings


def _intent_findings(intents: List[str]) -> List[str]:
    allowed = set(ALLOWED_PACKAGE_INTENTS)
    return [f"package_intent_{intent}_not_allowed" for intent in intents if intent not in allowed]


def _item_findings(items: List[Mapping[str, Any]]) -> List[str]:
    findings: List[str] = []
    required = ("item_id", "item_kind", "source_ref", "planned_path")
    for idx, item in enumerate(items):
        for name in required:
            if _missing(item.get(name)):
                findings.append(f"package_item_{idx}_{name}_missing")
        for bool_name in ("materialized", "write_authorized", "checksum_written"):
            if item.get(bool_name, False) is not False:
                findings.append(f"package_item_{idx}_{bool_name}_must_be_false")
    return findings


def _future_authority_for_section(section: str) -> str:
    return {
        "PACKAGE_SUMMARY": "FUTURE_PACKAGE_MATERIALIZATION_AUTHORITY_REQUIRED",
        "ITEM_PLAN": "FUTURE_FILE_PLAN_MATERIALIZATION_AUTHORITY_REQUIRED",
        "CHECKSUM_PLAN": "FUTURE_CHECKSUM_WRITE_AUTHORITY_REQUIRED",
        "EVIDENCE_INDEX": "FUTURE_EVIDENCE_PACKAGE_AUTHORITY_REQUIRED",
        "BOUNDARY_LEDGER": "FUTURE_BOUNDARY_AUDIT_AUTHORITY_REQUIRED",
        "OPERATOR_REVIEW_LANE": "FUTURE_OPERATOR_PACKAGE_APPROVAL_AUTHORITY_REQUIRED",
        "FUTURE_MATERIALIZATION_AUTHORITY": "FUTURE_PACKAGE_AUTHORITY_RATIFICATION_REQUIRED",
    }.get(section, "FUTURE_PACKAGE_AUTHORITY_REQUIRED")


def _checksum_preview(item: Mapping[str, Any], package_plan_id: str) -> Dict[str, Any]:
    seed = f"{package_plan_id}|{item.get('item_id','')}|{item.get('source_ref','')}|{item.get('planned_path','')}"
    # Deterministic preview token, intentionally not a filesystem checksum.
    token = str(abs(hash(seed)) % 10_000_000).zfill(7)
    return {
        "checksum_preview_id": f"CHECKSUM_PREVIEW:{item.get('item_id','UNKNOWN')}",
        "item_id": item.get("item_id"),
        "algorithm_preview": "sha256-preview-token-only",
        "checksum_preview": token,
        "real_checksum_claim": False,
        "checksum_file_written": False,
        "source_bytes_read": False,
    }


def build_handoff_package_assembly_plan_view_model(data: HandoffPackageAssemblyPlanInput | Mapping[str, Any]) -> HandoffPackageAssemblyPlanViewModel:
    if isinstance(data, Mapping):
        data = HandoffPackageAssemblyPlanInput(**dict(data))

    missing = [name for name in (
        "mission_id",
        "handoff_manifest_ref",
        "handoff_manifest_verdict",
        "upstream_execution_mode",
        "manifest_preview_id",
        "operator_review_ref",
    ) if _missing(getattr(data, name))]
    if not data.package_intents:
        missing.append("package_intents")
    if not data.package_sections:
        missing.append("package_sections")
    if not data.package_items:
        missing.append("package_items")
    if not data.evidence_refs:
        missing.append("evidence_refs")
    if not data.review_policy_flags:
        missing.append("review_policy_flags")

    forbidden = _forbidden_findings(data.blocked_capabilities)
    review = _review_findings(data.review_policy_flags)
    sections = _section_findings(data.package_sections)
    intents = _intent_findings(data.package_intents)
    item_findings = _item_findings(data.package_items)

    if data.live_package_requested:
        verdict, reason = "BLOCKED_LIVE_PACKAGE_REQUESTED", "Live package materialization requested; V69 is package-plan preview only."
    elif data.file_write_requested:
        verdict, reason = "BLOCKED_FILE_WRITE_REQUESTED", "File write requested; V69 cannot write files."
    elif data.zip_creation_requested:
        verdict, reason = "BLOCKED_ZIP_CREATION_REQUESTED", "Zip creation requested; V69 cannot create packages."
    elif data.checksum_file_write_requested:
        verdict, reason = "BLOCKED_CHECKSUM_FILE_WRITE_REQUESTED", "Checksum file write requested; V69 cannot write checksum files."
    elif data.artifact_export_requested:
        verdict, reason = "BLOCKED_ARTIFACT_EXPORT_REQUESTED", "Artifact export requested; V69 cannot export artifacts."
    elif data.external_transfer_requested:
        verdict, reason = "BLOCKED_EXTERNAL_TRANSFER_REQUESTED", "External transfer requested; V69 cannot transfer data."
    elif data.memory_write_requested:
        verdict, reason = "BLOCKED_MEMORY_WRITE_REQUESTED", "Memory write requested; V69 cannot write memory."
    elif data.canonical_graph_write_requested:
        verdict, reason = "BLOCKED_CANONICAL_GRAPH_WRITE_REQUESTED", "Canonical graph write requested; V69 cannot commit graph state."
    elif data.source_summary_rewrite_requested:
        verdict, reason = "BLOCKED_SOURCE_SUMMARY_REWRITE_REQUESTED", "Source-summary rewrite requested; V69 cannot rewrite summaries."
    elif missing:
        verdict, reason = "BLOCKED_MISSING_PACKAGE_PLAN_EVIDENCE", "Missing package-plan evidence: " + ", ".join(missing) + "."
    elif data.handoff_manifest_verdict not in REQUIRED_HANDOFF_VERDICTS or data.upstream_execution_mode not in REQUIRED_UPSTREAM_EXECUTION_MODES:
        verdict, reason = "BLOCKED_HANDOFF_MANIFEST_NOT_READY", "V68 handoff manifest preview is not ready for package-plan preview."
    elif forbidden:
        verdict, reason = "BLOCKED_FORBIDDEN_PACKAGE_CAPABILITY", "Forbidden package capability evidence detected: " + ", ".join(forbidden) + "."
    elif review:
        verdict, reason = "BLOCKED_MISSING_OPERATOR_REVIEW_POLICY", "Operator review policy missing: " + ", ".join(review) + "."
    elif sections:
        verdict, reason = "BLOCKED_INVALID_PACKAGE_SECTION", "Package section issue: " + ", ".join(sections) + "."
    elif intents:
        verdict, reason = "BLOCKED_INVALID_PACKAGE_INTENT", "Invalid package intent: " + ", ".join(intents) + "."
    elif item_findings:
        verdict, reason = "BLOCKED_INVALID_PACKAGE_ITEM", "Package item issue: " + ", ".join(item_findings) + "."
    else:
        verdict, reason = "PACKAGE_ASSEMBLY_PLAN_PREVIEW_READY", "V68 handoff manifest may be rendered as a non-materializing package assembly plan and checksum preview only."

    execution = "PACKAGE_ASSEMBLY_PLAN_PREVIEW_ONLY" if verdict == "PACKAGE_ASSEMBLY_PLAN_PREVIEW_READY" else "VIEW_ONLY_BLOCKED"
    package_plan_id = f"PACKAGE_ASSEMBLY_PLAN_PREVIEW:{data.mission_id}"
    section_cards = [
        {
            "section_id": f"{package_plan_id}:{idx+1}",
            "section": section,
            "preview_only": True,
            "materialized": False,
            "write_authorized": False,
            "zip_authorized": False,
            "required_future_authority": _future_authority_for_section(section),
            "evidence_refs": list(data.evidence_refs),
        }
        for idx, section in enumerate(data.package_sections)
    ]
    item_cards = [
        {
            "item_id": item.get("item_id"),
            "item_kind": item.get("item_kind"),
            "source_ref": item.get("source_ref"),
            "planned_path": item.get("planned_path"),
            "include_in_future_package": item.get("include_in_future_package", True),
            "materialized": False,
            "write_authorized": False,
            "checksum_written": False,
        }
        for item in data.package_items
    ]
    checksums = [_checksum_preview(item, package_plan_id) for item in item_cards]

    return HandoffPackageAssemblyPlanViewModel(
        version=VERSION,
        mission_id=data.mission_id,
        handoff_manifest_ref=data.handoff_manifest_ref,
        handoff_manifest_verdict=data.handoff_manifest_verdict,
        package_plan_verdict=verdict,
        authority_scope=AUTHORITY_SCOPE,
        execution_mode=execution,
        package_plan_id=package_plan_id,
        manifest_preview_id=data.manifest_preview_id,
        package_intents=list(data.package_intents),
        package_sections=section_cards,
        package_items=item_cards,
        checksum_preview_records=checksums,
        evidence_refs=list(data.evidence_refs),
        view_surfaces=list(data.view_surfaces),
        review_policy_flags=dict(data.review_policy_flags),
        blocked_capabilities=dict(data.blocked_capabilities),
        operator_review_ref=data.operator_review_ref,
        operator_reason=reason,
        next_required_action="Operator may inspect package plan; future materialization requires separate export/package authority.",
    )


def build_fixture_handoff_package_assembly_plan_input(**overrides: Any) -> HandoffPackageAssemblyPlanInput:
    base = HandoffPackageAssemblyPlanInput(
        mission_id="M-069",
        handoff_manifest_ref="HANDOFF_MANIFEST_PREVIEW:M-068",
        handoff_manifest_verdict="HANDOFF_MANIFEST_PREVIEW_READY",
        upstream_execution_mode="HANDOFF_MANIFEST_PREVIEW_ONLY",
        manifest_preview_id="HANDOFF_MANIFEST_PREVIEW:M-068",
        package_intents=["USER_REVIEW_PACKAGE_PLAN_PREVIEW", "FUTURE_AGENT_HANDOFF_PACKAGE_PREVIEW", "FUTURE_RELEASE_PACKAGE_PREVIEW"],
        package_sections=list(REQUIRED_PACKAGE_SECTIONS),
        package_items=[
            {"item_id": "ITEM:M-069:manifest", "item_kind": "manifest_preview", "source_ref": "HANDOFF_MANIFEST_PREVIEW:M-068", "planned_path": "manifest/preview.json"},
            {"item_id": "ITEM:M-069:evidence", "item_kind": "evidence_index", "source_ref": "V68_EVIDENCE_INDEX", "planned_path": "evidence/index.preview.json"},
            {"item_id": "ITEM:M-069:boundary", "item_kind": "boundary_ledger", "source_ref": "V68_BLOCKED_CAPABILITIES", "planned_path": "boundary/blocked-capabilities.preview.yaml"},
        ],
        evidence_refs=["V67_RESULT_SAVE_PROPOSAL:M-067", "V68_HANDOFF_MANIFEST_PREVIEW:M-068"],
        operator_review_ref="OPERATOR_REVIEW_REQUIRED:M-069",
        review_policy_flags={
            "operator_review_required": True,
            "package_plan_preview_only": True,
            "no_file_write": True,
            "no_zip_creation": True,
            "no_checksum_file_write": True,
            "no_artifact_export": True,
            "no_external_transfer": True,
            "no_memory_write": True,
            "no_graph_commit": True,
            "no_source_summary_rewrite": True,
        },
    )
    values = asdict(base)
    values.update(overrides)
    return HandoffPackageAssemblyPlanInput(**values)


def validate_handoff_package_assembly_plan_view_model(model: HandoffPackageAssemblyPlanViewModel) -> Dict[str, Any]:
    findings: List[str] = []
    false_attrs = (
        "production_authority",
        "live_dispatch_claim",
        "live_write_claim",
        "live_export_claim",
        "live_package_claim",
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
    findings.extend(_intent_findings(model.package_intents))
    if model.package_plan_verdict == "PACKAGE_ASSEMBLY_PLAN_PREVIEW_READY" and model.execution_mode != "PACKAGE_ASSEMBLY_PLAN_PREVIEW_ONLY":
        findings.append("ready_state_requires_package_assembly_plan_preview_only")
    if model.package_plan_verdict.startswith("BLOCKED") and model.execution_mode != "VIEW_ONLY_BLOCKED":
        findings.append("blocked_state_requires_view_only_blocked")
    for section in model.package_sections:
        if section.get("preview_only") is not True:
            findings.append("package_section_preview_only_must_be_true")
        if section.get("materialized") is not False:
            findings.append("package_section_materialized_must_be_false")
        if section.get("write_authorized") is not False:
            findings.append("package_section_write_authorized_must_be_false")
        if section.get("zip_authorized") is not False:
            findings.append("package_section_zip_authorized_must_be_false")
    for item in model.package_items:
        if item.get("materialized") is not False:
            findings.append("package_item_materialized_must_be_false")
        if item.get("write_authorized") is not False:
            findings.append("package_item_write_authorized_must_be_false")
        if item.get("checksum_written") is not False:
            findings.append("package_item_checksum_written_must_be_false")
    for checksum in model.checksum_preview_records:
        if checksum.get("real_checksum_claim") is not False:
            findings.append("checksum_preview_real_checksum_claim_must_be_false")
        if checksum.get("checksum_file_written") is not False:
            findings.append("checksum_file_written_must_be_false")
        if checksum.get("source_bytes_read") is not False:
            findings.append("checksum_source_bytes_read_must_be_false")
    return {
        "version": VERSION,
        "validation_verdict": "VALID_HANDOFF_PACKAGE_ASSEMBLY_PLAN_VIEW_MODEL" if not findings else "INVALID_HANDOFF_PACKAGE_ASSEMBLY_PLAN_VIEW_MODEL",
        "authority_scope": AUTHORITY_SCOPE,
        "package_plan_verdict": model.package_plan_verdict,
        "execution_mode": model.execution_mode,
        "package_plan_id": model.package_plan_id,
        "package_item_count": len(model.package_items),
        "checksum_preview_count": len(model.checksum_preview_records),
        "package_section_count": len(model.package_sections),
        "view_surface_count": len(model.view_surfaces),
        "findings": findings,
        "production_authority": False,
        "live_dispatch_claim": False,
        "live_write_claim": False,
        "live_export_claim": False,
        "live_package_claim": False,
        "file_system_write_authorized": False,
        "zip_creation_authorized": False,
        "checksum_file_write_authorized": False,
        "package_materialization_authorized": False,
        "external_transfer_authorized": False,
        "canonical_graph_write_authorized": False,
    }


if __name__ == "__main__":
    model = build_handoff_package_assembly_plan_view_model(build_fixture_handoff_package_assembly_plan_input())
    print(model.to_dict())
    print(validate_handoff_package_assembly_plan_view_model(model))
