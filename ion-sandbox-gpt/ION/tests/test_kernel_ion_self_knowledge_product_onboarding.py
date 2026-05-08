"""Focused tests for ION self-knowledge product/front-door onboarding audit.

These tests validate sandbox-local product onboarding audit evidence and the
candidate overlay. They do not accept product-law, Custom GPT instruction, or
registry mutations.
"""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SK = ROOT / "ION/05_context/current/self_knowledge"
PROMO = SK / "promotion_candidate"
OVERLAY = PROMO / "SELF_KNOWLEDGE_PRODUCT_ONBOARDING_OVERLAY_V0_2.json"
SCRIPT = SK / "audit_self_knowledge_product_onboarding.py"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def latest_report() -> Path:
    reports = sorted(PROMO.glob("SELF_KNOWLEDGE_PRODUCT_ONBOARDING_AUDIT_REPORT_*.json"))
    assert reports, "product onboarding audit report missing"
    return reports[-1]


def latest_patchset() -> Path:
    patchsets = sorted((PROMO / "product_onboarding_overlay").glob("PRODUCT_ONBOARDING_SELF_KNOWLEDGE_WIRING_PATCHSET_*.json"))
    assert patchsets, "product onboarding patchset missing"
    return patchsets[-1]


def test_product_onboarding_audit_report_is_candidate_evidence_not_landing():
    report = load_json(latest_report())
    assert report["accepted"] is True
    assert report["status"] == "accepted_candidate_evidence_product_overlay_prepared"
    assert report["simulation_mode"] == "sandbox_local_product_frontdoor_audit_not_product_mutation"
    boundary = report["authority_boundary"]
    assert boundary["mutated_product_surfaces"] is False
    assert boundary["mutated_custom_gpt_instructions"] is False
    assert boundary["mutated_product_manifest"] is False
    assert boundary["mutated_ION_03_registry"] is False
    assert boundary["production_authority"] is False
    assert boundary["live_execution_authority"] is False
    assert boundary["explicit_acceptance_observed"] is False


def test_product_onboarding_audit_confirms_candidate_package_surfaces_present():
    report = load_json(latest_report())
    inclusion = report["package_inclusion"]
    assert inclusion["active_self_knowledge_mount_packet_exists"] is True
    assert inclusion["self_knowledge_current_dir_exists"] is True
    assert inclusion["candidate_domain_count"] >= 14
    assert inclusion["candidate_route_registry_exists"] is True
    assert report["coverage"]["required_package_surfaces_present"] is True


def test_product_frontdoor_current_surfaces_are_not_silently_mutated():
    report = load_json(latest_report())
    # In this non-acceptance packet the audit may prepare a patchset, but it may
    # not rewrite product front-door files in place.
    assert report["frontdoor_explicit_self_knowledge_surface_count"] == 0
    for surface in report["frontdoor_surfaces"]:
        if surface["path"].startswith("product/") or surface["path"] in {"START_HERE.md", "README.md", "PRODUCT_MANIFEST.json"}:
            assert surface["contains_active_self_knowledge_mount_packet"] is False


def test_product_onboarding_overlay_is_candidate_only_and_requires_acceptance():
    overlay = load_json(OVERLAY)
    assert overlay["status"] == "candidate_current_state_not_accepted_product_law"
    boundary = overlay["authority_boundary"]
    assert boundary["candidate_only"] is True
    assert boundary["mutates_active_product_files"] is False
    assert boundary["mutates_product_surfaces"] is False
    assert boundary["mutates_custom_gpt_instructions"] is False
    assert boundary["mutates_product_manifest"] is False
    assert boundary["requires_explicit_acceptance_to_land"] is True
    assert "mount_active_self_knowledge_mount_packet" in overlay["required_sequence_for_product_carriers"]
    assert "single_carrier_is_fallback_not_base" in overlay["anti_drift_guards"]
    assert "do_not_call_gpt_reduced_ion" in overlay["anti_drift_guards"]


def test_product_onboarding_patchset_targets_frontdoor_surfaces_and_preserves_guards():
    patchset = load_json(latest_patchset())
    assert patchset["status"] == "candidate_overlay_pending_explicit_acceptance"
    assert patchset["authority_boundary"]["mutates_product_surfaces"] is False
    assert patchset["authority_boundary"]["requires_explicit_acceptance_to_land"] is True
    targets = {op["target_path"] for op in patchset["patch_operations"]}
    required_targets = {
        "START_HERE.md",
        "README.md",
        "PRODUCT_MANIFEST.json",
        "product/custom_gpt_adapter/CUSTOM_GPT_INSTRUCTIONS_8000.md",
        "product/custom_gpt_adapter/GPT_INSTRUCTIONS.md",
        "product/custom_gpt_adapter/STARTUP_BEHAVIOR.md",
        "product/custom_gpt_adapter/knowledge_manifest.json",
        "product/package_guides/ION_FULL_GPT_SANDBOX_AGENT_PACKAGE.md",
    }
    assert required_targets <= targets

    serialized = json.dumps(patchset)
    assert "ION-about-ION" in serialized
    assert "ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET.md" in serialized
    assert "Single-carrier sequential mode is a host-limited fallback" in serialized
    assert "not reduced ION" in serialized


def test_acceptance_gate_records_product_overlay_ready_but_not_landed():
    gate = load_json(PROMO / "SELF_KNOWLEDGE_ACCEPTANCE_GATE_STATUS_V0_2.json")
    criteria = {item["id"]: item for item in gate["acceptance_criteria"]}
    assert 12 in criteria
    assert criteria[12]["status"] == "ready_candidate_overlay_prepared_not_landed"
    assert "product files not mutated" in criteria[12]["evidence"]
    assert gate["status"] == "promotion_ready_candidate_blocked_on_explicit_acceptance_only"


def test_promotion_manifest_records_product_onboarding_audit_evidence():
    manifest = load_json(PROMO / "PROMOTION_CANDIDATE_MANIFEST_V0_2.json")
    evidence = manifest["product_onboarding_audit_evidence"]
    assert evidence["status"] == "passed_candidate_audit_overlay_prepared"
    assert evidence["mutated_product_surfaces"] is False
    assert evidence["external_carrier_claimed"] is False
    assert evidence["candidate_patch_operation_count"] >= 8


def test_product_onboarding_audit_script_is_present_but_not_a_landing_action():
    text = SCRIPT.read_text(encoding="utf-8")
    assert "does not mutate product files" in text
    assert "does not mutate product" in text
    assert "mutated_product_surfaces" in text
    assert "external Codex/MCP" in text
