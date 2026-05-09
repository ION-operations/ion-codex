"""Focused tests for AI Assistant Work agent boot/template spec candidate.

These tests validate current-context candidate artifacts only. They do not claim
accepted agent runtime, template-law promotion, registry landing, product-front-door
mutation, external IDE/CLI/cloud/PR/background-agent execution, or human acceptance.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

for _p in [
    "/opt/pyvenv/lib/python3.13/site-packages",
    "/opt/pyvenv/lib/python3.13/dist-packages",
    "/usr/local/lib/python3.13/dist-packages",
]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

import yaml

ROOT = Path(__file__).resolve().parents[2]
AIW = ROOT / "ION/05_context/current/ai_assistant_work"
BOOT_DIR = AIW / "agent_boots"
SPEC_DIR = AIW / "template_specs"
REG = AIW / "registries"
SIM = AIW / "simulations/AI_ASSISTANT_WORK_AGENT_BOOT_TEMPLATE_DISPATCH_SIMULATION_REPORT_LATEST.json"
VAL = AIW / "validation/AI_ASSISTANT_WORK_AGENT_BOOT_TEMPLATE_SPEC_VALIDATION_NOTE_LATEST.json"

REQUIRED_AGENT_BOOTS = {
    "UI_STATE_MODELER": "screen_state_matrix_packet",
    "PR_REVIEW_STEWARD": "pr_review_packet",
    "BACKGROUND_QUEUE_STEWARD": "background_queue_result_intake_packet",
    "TERMINAL_PROOF_CURATOR": "terminal_proof_receipt_packet",
    "EXAMPLE_RUNNER": "api_docs_example_validation_packet",
    "RELEASE_EVIDENCE_CURATOR": "release_readiness_matrix_packet",
    "MIGRATION_MASON": "migration_plan_and_rollback_packet",
}


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_agent_boot_index_has_required_specialists_and_candidate_boundary():
    index = load_yaml(BOOT_DIR / "AI_ASSISTANT_WORK_AGENT_BOOT_DRAFTS_INDEX_V0_1.yaml")
    assert index["status"] == "candidate_current_state_not_accepted_canon"
    assert index["authority_boundary"]["candidate_only"] is True
    assert index["authority_boundary"]["mutates_ION_03_registry"] is False
    assert index["authority_boundary"]["requires_explicit_acceptance_to_land"] is True
    assert index["agent_boot_count"] >= len(REQUIRED_AGENT_BOOTS)

    boot_ids = {item["role_id"] for item in index["agent_boots"]}
    assert set(REQUIRED_AGENT_BOOTS) <= boot_ids


def test_each_agent_boot_loads_template_state_surfaces_proof_and_non_claims():
    known_agents = {
        item["role_id"]
        for item in load_yaml(REG / "AI_ASSISTANT_WORK_AGENT_REGISTRY_CANDIDATE_V0_2.yaml")["agents"]
    }

    for role_id, template_id in REQUIRED_AGENT_BOOTS.items():
        boot = load_yaml(BOOT_DIR / f"{role_id}.agent_boot.yaml")
        assert boot["schema"] == "ion.ai_assistant_work.agent_boot.v0_1"
        assert boot["status"] == "candidate_agent_boot_draft_not_accepted_canon"
        assert boot["authority_boundary"]["candidate_only"] is True
        assert boot["authority_boundary"]["mutates_ION_03_registry"] is False
        assert boot["authority_boundary"]["external_execution_authority"] is False
        assert template_id in boot["owned_template_specs"]
        assert boot["state_surfaces_owned"]
        assert boot["protocols_required"]
        assert boot["proof_obligations"]
        assert boot["return_contract"]["must_include_template_id"] is True
        assert "generic coding assistant is enough for this work class" in boot["must_not_claim"]
        assert boot["role_id"] in known_agents


def test_template_spec_index_and_specs_are_machine_checkable_candidates():
    index = load_yaml(SPEC_DIR / "AI_ASSISTANT_WORK_TEMPLATE_SPEC_INDEX_V0_1.yaml")
    assert index["status"] == "candidate_current_state_not_accepted_canon"
    assert index["authority_boundary"]["candidate_only"] is True
    assert index["authority_boundary"]["mutates_ION_03_registry"] is False
    spec_ids = {item["template_id"] for item in index["template_specs"]}
    assert set(REQUIRED_AGENT_BOOTS.values()) <= spec_ids

    for template_id in REQUIRED_AGENT_BOOTS.values():
        spec = load_yaml(SPEC_DIR / f"{template_id}.template_spec.yaml")
        assert spec["schema"] == "ion.ai_assistant_work.template_spec.v0_1"
        assert spec["status"] == "candidate_machine_checkable_template_spec_not_accepted_canon"
        assert spec["authority_boundary"]["candidate_only"] is True
        assert spec["machine_required_sections"]
        assert spec["state_inputs"]
        assert spec["state_outputs"]
        gates = {gate["gate_id"] for gate in spec["proof_gates"]}
        assert "candidate_boundary_named" in gates
        assert "required_sections_present" in gates
        assert spec["route_binding"]["dispatch_before_generic_implementation"] is True
        assert spec["route_binding"]["fallback_agent_forbidden_until_specialist_check"] is True


def test_agent_boot_template_bindings_resolve_both_directions():
    boot_index = load_yaml(BOOT_DIR / "AI_ASSISTANT_WORK_AGENT_BOOT_DRAFTS_INDEX_V0_1.yaml")
    spec_index = load_yaml(SPEC_DIR / "AI_ASSISTANT_WORK_TEMPLATE_SPEC_INDEX_V0_1.yaml")
    boot_templates = {
        template_id
        for boot in boot_index["agent_boots"]
        for template_id in boot["owned_template_specs"]
    }
    spec_templates = {spec["template_id"] for spec in spec_index["template_specs"]}
    assert boot_templates <= spec_templates

    for spec in spec_index["template_specs"]:
        assert spec["primary_agent"] in {boot["role_id"] for boot in boot_index["agent_boots"]}


def test_dispatch_simulation_blocks_generic_implementation_before_specialist_check():
    report = load_json(SIM)
    assert report["status"] == "candidate_simulation_not_accepted_canon"
    assert report["result"] == "accepted"
    assert report["accepted_count"] == report["case_count"]
    assert report["summary"]["generic_implementation_blocked_until_specialist_check"] is True

    specialist_cases = [
        case for case in report["cases"]
        if case["expected_agent"] in REQUIRED_AGENT_BOOTS
    ]
    assert len(specialist_cases) >= len(REQUIRED_AGENT_BOOTS)
    for case in specialist_cases:
        assert case["accepted"] is True
        assert case["generic_agent_allowed"] is False
        assert case["expected_template"] == REQUIRED_AGENT_BOOTS[case["expected_agent"]]


def test_validation_note_and_state_index_preserve_non_claims():
    validation = load_json(VAL)
    assert validation["status"] == "accepted_candidate_validation"
    assert validation["result"] == "accepted"
    assert validation["findings"] == []
    assert validation["authority_boundary"]["candidate_only"] is True
    assert validation["authority_boundary"]["mutates_ION_03_registry"] is False
    assert validation["validated_artifacts"]["agent_boot_count"] >= len(REQUIRED_AGENT_BOOTS)

    state = load_json(AIW / "AI_ASSISTANT_WORK_STATE_INDEX_V0_4.json")
    assert state["status"] == "candidate_current_state_not_accepted_canon"
    assert state["authority_boundary"]["candidate_only"] is True
    assert state["authority_boundary"]["requires_explicit_acceptance_to_land"] is True
    assert state["summary"]["agent_boot_draft_count"] >= len(REQUIRED_AGENT_BOOTS)
    assert state["summary"]["template_spec_count"] >= len(REQUIRED_AGENT_BOOTS)
    assert "No external IDE, CLI, cloud, PR, GitHub, MCP, Codex, daemon, or production action occurred." in state["non_claims"]
