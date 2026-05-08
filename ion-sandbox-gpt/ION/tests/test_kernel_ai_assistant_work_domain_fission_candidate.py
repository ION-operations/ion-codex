"""Focused tests for AI Assistant Work dataset-mining/domain-fission candidate.

These tests validate current-context candidate artifacts only. They do not claim
accepted domain fission, registry landing, product-front-door mutation, external
IDE/CLI/cloud/PR/background-agent execution, or human acceptance.
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
REG = AIW / "registries"
DATASET = AIW / "dataset/AI_ASSISTANT_WORK_DATASET_GENESIS_V0_1.jsonl"
FISSION = AIW / "fission/AI_ASSISTANT_WORK_DOMAIN_FISSION_CANDIDATES_V0_1.yaml"
TEMPLATE_DRAFTS = AIW / "template_packets/AI_ASSISTANT_WORK_CONCRETE_TEMPLATE_PACKET_DRAFTS_V0_1.yaml"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_dataset():
    return [json.loads(line) for line in DATASET.read_text(encoding="utf-8").splitlines() if line.strip()]


def test_domain_fission_candidate_has_candidate_boundary_and_minimum_scope():
    doc = load_yaml(FISSION)
    assert doc["status"] == "candidate_current_state_not_accepted_canon"
    assert doc["authority_boundary"]["candidate_only"] is True
    assert doc["authority_boundary"]["mutates_ION_03_registry"] is False
    assert doc["authority_boundary"]["requires_explicit_acceptance_to_land"] is True
    assert doc["candidate_count"] >= 10
    ids = {c["candidate_domain_id"] for c in doc["candidates"]}
    for required in {
        "pr_agent_work_domain",
        "background_queue_intake_domain",
        "terminal_proof_domain",
        "ui_state_modeling_domain",
        "documentation_example_validation_domain",
        "release_evidence_domain",
        "migration_work_domain",
    }:
        assert required in ids


def test_fission_candidates_have_dataset_evidence_agents_templates_and_settlement_routes():
    entries = {entry["entry_id"] for entry in load_dataset()}
    doc = load_yaml(FISSION)
    agents = {a["role_id"] for a in load_yaml(REG / "AI_ASSISTANT_WORK_AGENT_REGISTRY_CANDIDATE_V0_2.yaml")["agents"]}
    template_packets = {t["template_id"] for t in load_yaml(TEMPLATE_DRAFTS)["template_packets"]}

    for candidate in doc["candidates"]:
        assert candidate["evidence_entry_ids"]
        assert set(candidate["evidence_entry_ids"]) <= entries
        assert candidate["proposed_primary_agents"]
        assert set(candidate["proposed_primary_agents"]) <= agents
        assert candidate["proposed_template_packets"]
        assert set(candidate["proposed_template_packets"]) & template_packets
        assert candidate["settlement_route"]
        assert candidate["status"] == "fission_candidate_not_accepted_domain"


def test_v0_2_registries_expand_without_landing_active_registry_law():
    domain_v1 = load_yaml(REG / "AI_ASSISTANT_WORK_DOMAIN_REGISTRY_CANDIDATE_V0_1.yaml")
    domain_v2 = load_yaml(REG / "AI_ASSISTANT_WORK_DOMAIN_REGISTRY_CANDIDATE_V0_2.yaml")
    agent_v1 = load_yaml(REG / "AI_ASSISTANT_WORK_AGENT_REGISTRY_CANDIDATE_V0_1.yaml")
    agent_v2 = load_yaml(REG / "AI_ASSISTANT_WORK_AGENT_REGISTRY_CANDIDATE_V0_2.yaml")
    template_v1 = load_yaml(REG / "AI_ASSISTANT_WORK_TEMPLATE_REGISTRY_CANDIDATE_V0_1.yaml")
    template_v2 = load_yaml(REG / "AI_ASSISTANT_WORK_TEMPLATE_REGISTRY_CANDIDATE_V0_2.yaml")

    assert domain_v2["status"] == "candidate_current_state_not_accepted_canon"
    assert agent_v2["status"] == "candidate_current_state_not_accepted_canon"
    assert template_v2["status"] == "candidate_current_state_not_accepted_canon"
    assert len(domain_v2["domains"]) > len(domain_v1["domains"])
    assert len(agent_v2["agents"]) > len(agent_v1["agents"])
    assert len(template_v2["template_families"]) > len(template_v1["template_families"])

    role_ids = {a["role_id"] for a in agent_v2["agents"]}
    for required in {
        "UI_STATE_MODELER",
        "PR_REVIEW_STEWARD",
        "BACKGROUND_QUEUE_STEWARD",
        "TERMINAL_PROOF_CURATOR",
        "EXAMPLE_RUNNER",
        "RELEASE_EVIDENCE_CURATOR",
        "MIGRATION_MASON",
        "PROMPT_INJECTION_BOUNDARY_GUARDIAN",
    }:
        assert required in role_ids


def test_template_packet_drafts_are_concrete_and_specialist_owned():
    doc = load_yaml(TEMPLATE_DRAFTS)
    assert doc["status"] == "candidate_current_state_not_accepted_canon"
    assert doc["authority_boundary"]["mutates_ION_03_registry"] is False
    assert doc["template_packet_count"] >= 10

    packets = {p["template_id"]: p for p in doc["template_packets"]}
    required = {
        "screen_state_matrix_packet": "UI_STATE_MODELER",
        "api_docs_example_validation_packet": "EXAMPLE_RUNNER",
        "background_queue_result_intake_packet": "BACKGROUND_QUEUE_STEWARD",
        "terminal_proof_receipt_packet": "TERMINAL_PROOF_CURATOR",
        "release_readiness_matrix_packet": "RELEASE_EVIDENCE_CURATOR",
    }
    for template_id, primary_agent in required.items():
        packet = packets[template_id]
        assert packet["primary_agent"] == primary_agent
        assert packet["required_sections"]
        assert packet["proof_gates"]
        assert packet["settlement_route"]
        assert packet["status"] == "draft_template_packet_candidate"


def test_fission_route_simulation_validation_and_state_index_are_aligned():
    sim = load_json(AIW / "simulations/AI_ASSISTANT_WORK_DOMAIN_FISSION_ROUTE_SIMULATION_REPORT_LATEST.json")
    note = load_json(AIW / "validation/AI_ASSISTANT_WORK_DATASET_MINING_DOMAIN_FISSION_VALIDATION_NOTE_LATEST.json")
    index = load_json(AIW / "AI_ASSISTANT_WORK_STATE_INDEX_V0_3.json")
    receipt_candidates = sorted((AIW / "receipts").glob("AI_ASSISTANT_WORK_DATASET_MINING_TO_DOMAIN_FISSION_RECEIPT_*.json"))
    assert receipt_candidates
    receipt = load_json(receipt_candidates[-1])

    assert sim["accepted"] is True
    assert sim["cases_accepted"] == sim["case_count"]
    assert sim["candidate_domain_count"] == note["fission_candidate_count"]
    assert note["accepted"] is True
    assert note["findings"] == []
    assert index["status"] == "candidate_current_state_not_accepted_canon"
    assert index["summary"]["candidate_child_domain_count"] == note["fission_candidate_count"]
    assert index["authority_boundary"]["mutates_ION_03_registry"] is False
    assert receipt["authority"]["mutated_ION_03_registry"] is False
    assert receipt["authority"]["external_execution"] is False


def test_specialist_domains_route_before_generic_implementation():
    doc = load_yaml(FISSION)
    by_id = {candidate["candidate_domain_id"]: candidate for candidate in doc["candidates"]}

    ui = by_id["ui_state_modeling_domain"]
    assert "UI_STATE_MODELER" in ui["proposed_primary_agents"]
    assert "screen_state_matrix_packet" in ui["proposed_template_packets"]

    pr = by_id["pr_agent_work_domain"]
    assert "PR_REVIEW_STEWARD" in pr["proposed_primary_agents"]
    assert "PR_MERGE_SETTLEMENT_AUDITOR" in pr["proposed_primary_agents"]

    bg = by_id["background_queue_intake_domain"]
    assert "BACKGROUND_QUEUE_STEWARD" in bg["proposed_primary_agents"]
    assert "RESULT_INTAKE_AUDITOR" in bg["proposed_primary_agents"]

    docs = by_id["documentation_example_validation_domain"]
    assert "EXAMPLE_RUNNER" in docs["proposed_primary_agents"]
    assert "api_docs_example_validation_packet" in docs["proposed_template_packets"]
