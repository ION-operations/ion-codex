"""Focused tests for AI Assistant Work candidate domain system.

These tests validate current-context candidate artifacts only. They do not
claim registry landing, product-law mutation, external IDE execution, or human
acceptance.
"""
from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
AIW = ROOT / "ION/05_context/current/ai_assistant_work"
REG = AIW / "registries"
DOMAINS = AIW / "domains"

REQUIRED_DOMAINS = {
    "ai_assistant_identity_embodiment",
    "chat_work_domain",
    "ide_work_domain",
    "codebase_understanding_domain",
    "planning_and_task_breakdown_domain",
    "implementation_domain",
    "ui_ux_domain",
    "documentation_writing_domain",
    "testing_quality_domain",
    "review_security_domain",
    "debugging_observability_domain",
    "devops_release_domain",
    "data_analysis_domain",
    "product_requirements_domain",
    "knowledge_context_memory_domain",
    "dependency_package_domain",
    "workflow_automation_tool_domain",
    "assistant_learning_dataset_domain",
    "cross_domain_settlement_domain",
}

REQUIRED_SPECIALIST_AGENTS = {
    "UI_ARCHITECT",
    "COMPONENT_BUILDER",
    "ACCESSIBILITY_AUDITOR",
    "DOCS_ARCHITECT",
    "TECHNICAL_WRITER",
    "API_DOCS_SCRIBE",
    "IDE_CARTOGRAPHER",
    "CODEBASE_CARTOGRAPHER",
    "PATCH_MASON",
    "TEST_RUNNER",
    "SECURITY_NEMESIS",
    "WORK_PATTERN_ETHNOGRAPHER",
    "STATE_TAXONOMIST",
    "TEMPLATE_MINER",
    "SETTLEMENT_STEWARD",
}


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_domain_registry_contains_ai_assistant_work_domains_and_is_candidate_only():
    registry = load_yaml(REG / "AI_ASSISTANT_WORK_DOMAIN_REGISTRY_CANDIDATE_V0_1.yaml")
    assert registry["status"] == "candidate_current_state_not_accepted_canon"
    assert registry["authority_boundary"]["candidate_only"] is True
    assert registry["authority_boundary"]["mutates_ION_03_registry"] is False
    domains = {item["domain_id"] for item in registry["domains"]}
    assert REQUIRED_DOMAINS <= domains
    assert len(domains) >= 19


def test_agent_registry_contains_ui_docs_ide_dataset_and_settlement_specialists():
    registry = load_yaml(REG / "AI_ASSISTANT_WORK_AGENT_REGISTRY_CANDIDATE_V0_1.yaml")
    assert registry["status"] == "candidate_current_state_not_accepted_canon"
    agents = {item["role_id"] for item in registry["agents"]}
    assert REQUIRED_SPECIALIST_AGENTS <= agents
    assert registry["agent_count"] >= 40
    for role in ["UI_ARCHITECT", "TECHNICAL_WRITER", "IDE_CARTOGRAPHER"]:
        item = next(a for a in registry["agents"] if a["role_id"] == role)
        assert item["status"] == "candidate_specialist_agent"
        assert item["domain_ids"]


def test_every_required_domain_packet_has_agents_states_templates_and_anti_drift_notes():
    for domain_id in REQUIRED_DOMAINS:
        packet = load_yaml(DOMAINS / f"{domain_id}.domain_packet.yaml")
        assert packet["status"] == "seed_candidate"
        assert packet["specialist_agents"]
        assert packet["state_families"]
        assert packet["template_families"]
        notes = "\n".join(packet["anti_drift_notes"])
        assert "generic coding assistant" in notes
        assert "candidate" in notes


def test_route_registry_routes_ui_docs_ide_dataset_and_cross_domain_work():
    registry = load_yaml(REG / "AI_ASSISTANT_WORK_ROUTE_REGISTRY_CANDIDATE_V0_1.yaml")
    routes = {item["route_id"]: item for item in registry["routes"]}
    for route_id in [
        "route.assistant_identity_definition",
        "route.ide_agent_work_map",
        "route.ui_specialist_work",
        "route.documentation_specialist_work",
        "route.assistant_work_dataset_build",
        "route.cross_domain_feature_delivery",
    ]:
        assert route_id in routes
        assert routes[route_id]["required_domains"]
        assert routes[route_id]["primary_agents"]
    assert "ui_ux_domain" in routes["route.ui_specialist_work"]["required_domains"]
    assert "documentation_writing_domain" in routes["route.documentation_specialist_work"]["required_domains"]


def test_state_template_protocol_registries_are_large_enough_to_start_dataset_work():
    state_registry = load_yaml(REG / "AI_ASSISTANT_WORK_STATE_REGISTRY_CANDIDATE_V0_1.yaml")
    template_registry = load_yaml(REG / "AI_ASSISTANT_WORK_TEMPLATE_REGISTRY_CANDIDATE_V0_1.yaml")
    protocol_registry = load_yaml(REG / "AI_ASSISTANT_WORK_PROTOCOL_REGISTRY_CANDIDATE_V0_1.yaml")
    assert state_registry["state_family_count"] >= 30
    assert template_registry["template_family_count"] >= 30
    assert protocol_registry["protocol_count"] >= 30


def test_dataset_entry_schema_tracks_domains_states_templates_agents_and_settlement():
    schema = load_yaml(REG / "AI_ASSISTANT_WORK_DATASET_ENTRY_SCHEMA_V0_1.yaml")
    fields = schema["required_fields"]
    for field in [
        "assistant_embodiment",
        "domains_involved",
        "state_surfaces",
        "templates_required",
        "specialist_agents_required",
        "settlement_path",
    ]:
        assert field in fields


def test_route_simulation_report_passed_without_external_execution_claims():
    report = load_json(AIW / "simulations/AI_ASSISTANT_WORK_ROUTE_SIMULATION_REPORT_20260508T143500Z.json")
    assert report["accepted"] is True
    assert report["status"] == "accepted_candidate_evidence"
    assert report["case_count"] == 6
    assert report["cases_accepted"] == 6
    assert report["simulation_mode"] == "sandbox_local_route_usage_not_external_ide_or_codex"
    assert "No external IDE execution occurred." in report["non_claims"]


def test_validation_note_passed_and_preserves_non_claims():
    note = load_json(AIW / "AI_ASSISTANT_WORK_VALIDATION_NOTE_20260508T143500Z.json")
    assert note["accepted"] is True
    assert note["domain_count"] >= 19
    assert note["agent_count"] >= 40
    assert note["route_count"] >= 6
    assert "No product-front-door or registry mutation is claimed." in note["non_claims"]


def test_receipt_state_index_and_next_packet_preserve_candidate_boundary():
    receipt = load_json(AIW / "AI_ASSISTANT_WORK_ACTIVATION_RECEIPT_20260508T143500Z.json")
    index = load_json(AIW / "AI_ASSISTANT_WORK_STATE_INDEX_V0_1.json")
    next_packet = load_json(AIW / "AI_ASSISTANT_WORK_NEXT_PACKET_20260508T143500Z.json")
    sync = load_json(AIW / "AI_ASSISTANT_WORK_STATE_SURFACE_SYNC_REPORT_20260508T143500Z.json")
    assert receipt["status"] == "candidate_current_state_receipt_not_accepted_canon"
    assert receipt["authority"]["mutated_ION_03_registry"] is False
    assert receipt["authority"]["candidate_only"] is True
    assert index["status"] == "candidate_current_state_not_accepted_canon"
    assert next_packet["status"] == "candidate_next_packet"
    assert "AI_ASSISTANT_WORK_DATASET_GENESIS_V0_1.jsonl" in next_packet["deliverables"]
    assert sync["accepted"] is True
    assert sync["alignment"]["no_registry_landing_claim"] is True
