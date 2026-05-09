"""Focused tests for candidate ION self-knowledge domain-state artifacts.

These tests validate the current-context candidate and promotion mirror. They do
not assert that the candidate has become accepted registry law.
"""
from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
SK = ROOT / "ION/05_context/current/self_knowledge"
MOUNT = ROOT / "ION/05_context/current/ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET.md"
PROMOTION = SK / "promotion_candidate"
TARGET_REGISTRY = ROOT / "ION/03_registry/self_knowledge"

REQUIRED_DOMAINS = {
    "ion_identity",
    "ion_canon_authority",
    "ion_architecture",
    "ion_agent_role",
    "ion_full_multi_agent_runtime",
    "ion_carrier_embodiment",
    "ion_context_system",
    "ion_template_law",
    "ion_state_steward_receipt",
    "ion_product_package",
    "ion_workpacket",
    "ion_stale_donor_historical",
    "ion_recovery_anti_regression",
    "ion_operations_build",
}


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_self_knowledge_domain_registry_parses_and_covers_required_domains():
    registry = load_yaml(SK / "candidate_registries/domain_registry.candidate.yaml")
    domains = {item["domain_id"] for item in registry["domains"]}
    assert REQUIRED_DOMAINS <= domains
    assert registry["status"] == "candidate_current_state_not_accepted_canon"
    for item in registry["domains"]:
        assert item["state_class"] == "candidate_current_state"
        assert isinstance(item["authority_rank"], int)
        assert item["authority_rank"] >= 1


def test_self_knowledge_route_registry_blocks_known_reductions():
    route_registry = load_yaml(SK / "candidate_registries/route_registry.candidate.yaml")
    routes = route_registry["routes"]
    all_guards = {
        guard
        for route in routes
        for guard in route.get("anti_drift_required", [])
    }
    assert "single_carrier_is_fallback_not_base" in all_guards
    assert "do_not_call_gpt_reduced_ion" in all_guards
    assert "no_donor_as_active_authority" in all_guards


def test_self_knowledge_mount_packet_contains_route_selector_and_anti_drift_rules():
    text = MOUNT.read_text(encoding="utf-8")
    required = [
        "What ION is",
        "What ION is not",
        "Current source ranking",
        "Available self-knowledge domains",
        "Do not treat single-carrier mode as ION's intended center.",
        "Do not call the GPT package",
        "Do not let historical donor material become active authority.",
    ]
    for phrase in required:
        assert phrase in text


def test_self_knowledge_state_classes_require_authority_or_receipt_boundaries():
    state_classes = load_yaml(SK / "candidate_registries/state_classification.candidate.yaml")
    by_id = {item["id"]: item for item in state_classes["classes"]}
    assert "canonical_active" in by_id
    assert "candidate_current_state" in by_id
    assert "acceptance_or_receipt" in by_id["canonical_active"]["requires"]
    assert "human_or_steward_acceptance_for_landing" in by_id["candidate_current_state"]["requires"]


def test_self_knowledge_no_donor_class_is_accepted_authority():
    state_classes = load_yaml(SK / "candidate_registries/state_classification.candidate.yaml")
    donorish = [
        item for item in state_classes["classes"]
        if item["id"] in {"witness", "donor", "deprecated", "quarantined"}
    ]
    assert donorish
    for item in donorish:
        assert item["may_be_inherited_as"] != "law"


def test_self_knowledge_promotion_mirror_is_pending_and_does_not_mutate_registry():
    manifest = json.loads((PROMOTION / "PROMOTION_CANDIDATE_MANIFEST_V0_2.json").read_text(encoding="utf-8"))
    assert manifest["status"] in {
        "promotion_proposal_pending_human_steward_acceptance",
        "promotion_ready_candidate_blocked_on_explicit_acceptance_only",
    }
    assert manifest["authority_boundary"]["direct_registry_mutation_authorized"] is False
    assert manifest["authority_boundary"]["actual_target_namespace_mutated"] is False
    assert TARGET_REGISTRY.exists() is False
    for entry in manifest["prepared_mappings"]:
        mirror = ROOT / entry["mirror_path"]
        assert mirror.exists()
        mirrored_yaml = load_yaml(mirror)
        assert mirrored_yaml["status"] == "promotion_proposal_pending_human_steward_acceptance"
        assert mirrored_yaml["non_claim"].startswith("This mirror is not accepted registry law")
