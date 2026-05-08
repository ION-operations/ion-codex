"""Focused tests for AI Assistant Work dataset genesis candidate.

These tests validate current-context candidate artifacts only. They do not claim
registry landing, product-law mutation, external IDE/CLI/cloud/PR/background-agent
execution, or human acceptance.
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

REQUIRED_FIELDS = {
    "entry_id",
    "observed_at",
    "source_class",
    "assistant_embodiment",
    "user_intent",
    "work_pattern",
    "domains_involved",
    "state_surfaces",
    "tools_or_actions",
    "protocols_required",
    "templates_required",
    "specialist_agents_required",
    "proof_required",
    "failure_modes_observed",
    "settlement_path",
    "candidate_improvements",
    "authority_notes",
    "candidate_route",
}

REQUIRED_EMBODIMENTS = {
    "chat",
    "ide",
    "cli",
    "cloud_agent",
    "pr_agent",
    "background_agent",
    "hybrid",
}


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_dataset():
    return [json.loads(line) for line in DATASET.read_text(encoding="utf-8").splitlines() if line.strip()]


def latest_summary():
    candidates = sorted((AIW / "dataset").glob("AI_ASSISTANT_WORK_DATASET_GENESIS_SUMMARY_*.json"))
    assert candidates
    return load_json(candidates[-1])


def test_dataset_genesis_has_minimum_entries_required_fields_and_candidate_boundary():
    entries = load_dataset()
    assert len(entries) >= 25
    for entry in entries:
        assert REQUIRED_FIELDS <= set(entry)
        assert entry["proof_required"]
        assert entry["authority_notes"]
    assert DATASET.exists()


def test_dataset_covers_required_assistant_embodiments_and_mass_work_patterns():
    entries = load_dataset()
    embodiments = {entry["assistant_embodiment"] for entry in entries}
    assert REQUIRED_EMBODIMENTS <= embodiments
    patterns = " ".join(entry["work_pattern"] for entry in entries)
    for expected in ["workspace", "component", "docs", "test", "dependency", "release", "dataset", "background"]:
        assert expected in patterns


def test_dataset_references_only_known_domains_states_templates_protocols_agents_and_failures():
    entries = load_dataset()
    domain_ids = {d["domain_id"] for d in load_yaml(REG / "AI_ASSISTANT_WORK_DOMAIN_REGISTRY_CANDIDATE_V0_1.yaml")["domains"]}
    state_ids = {s["state_family_id"] for s in load_yaml(REG / "AI_ASSISTANT_WORK_STATE_REGISTRY_CANDIDATE_V0_1.yaml")["state_families"]}
    template_ids = {t["template_family_id"] for t in load_yaml(REG / "AI_ASSISTANT_WORK_TEMPLATE_REGISTRY_CANDIDATE_V0_1.yaml")["template_families"]}
    protocol_ids = {p["protocol_id"] for p in load_yaml(REG / "AI_ASSISTANT_WORK_PROTOCOL_REGISTRY_CANDIDATE_V0_1.yaml")["protocols"]}
    agent_ids = {a["role_id"] for a in load_yaml(REG / "AI_ASSISTANT_WORK_AGENT_REGISTRY_CANDIDATE_V0_1.yaml")["agents"]}
    failure_ids = {f["failure_mode_id"] for f in load_yaml(REG / "AI_ASSISTANT_WORK_FAILURE_MODE_REGISTRY_CANDIDATE_V0_1.yaml")["failure_modes"]}
    route_ids = {r["route_id"] for r in load_yaml(REG / "AI_ASSISTANT_WORK_ROUTE_REGISTRY_CANDIDATE_V0_1.yaml")["routes"]}

    assert domain_ids <= {d for entry in entries for d in entry["domains_involved"]}
    assert agent_ids <= {a for entry in entries for a in entry["specialist_agents_required"]}

    for entry in entries:
        assert set(entry["domains_involved"]) <= domain_ids
        assert set(entry["state_surfaces"]) <= state_ids
        assert set(entry["templates_required"]) <= template_ids
        assert set(entry["protocols_required"]) <= protocol_ids
        assert set(entry["specialist_agents_required"]) <= agent_ids
        assert set(entry["failure_modes_observed"]) <= failure_ids
        assert entry["candidate_route"] in route_ids


def test_failure_registry_skill_binding_map_and_gap_analysis_are_candidate_and_large_enough():
    failures = load_yaml(REG / "AI_ASSISTANT_WORK_FAILURE_MODE_REGISTRY_CANDIDATE_V0_1.yaml")
    bindings = load_yaml(REG / "AI_ASSISTANT_WORK_SKILL_TO_AGENT_BINDING_MAP_V0_1.yaml")
    gaps = load_yaml(AIW / "gaps/AI_ASSISTANT_WORK_DATASET_GAP_ANALYSIS_V0_1.yaml")
    assert failures["status"] == "candidate_current_state_not_accepted_canon"
    assert failures["authority_boundary"]["mutates_ION_03_registry"] is False
    assert failures["failure_mode_count"] >= 10
    assert bindings["status"] == "candidate_current_state_not_accepted_canon"
    assert bindings["binding_count"] >= 10
    assert gaps["status"] == "candidate_current_state_not_accepted_canon"
    assert gaps["template_gap_count"] >= 10
    assert gaps["agent_domain_gap_count"] >= 10


def test_route_simulation_accepted_all_dataset_entries_without_external_execution_claims():
    entries = load_dataset()
    report = load_json(AIW / "simulations/AI_ASSISTANT_WORK_DATASET_ROUTE_SIMULATION_REPORT_LATEST.json")
    assert report["accepted"] is True
    assert report["status"] == "accepted_candidate_evidence"
    assert report["case_count"] == len(entries)
    assert report["cases_accepted"] == len(entries)
    assert report["simulation_mode"] == "sandbox_local_dataset_route_usage_not_external_ide_cli_cloud_pr_or_daemon_execution"
    assert "No external IDE execution occurred." in report["non_claims"]


def test_dataset_validation_note_and_summary_are_aligned():
    entries = load_dataset()
    note = load_json(AIW / "validation/AI_ASSISTANT_WORK_DATASET_GENESIS_VALIDATION_NOTE_LATEST.json")
    summary = latest_summary()
    assert note["accepted"] is True
    assert note["dataset_entry_count"] == len(entries)
    assert summary["entry_count"] == len(entries)
    assert summary["domain_coverage_missing"] == []
    assert summary["agent_coverage_missing"] == []
    assert summary["coverage_requirements"]["required_embodiments_missing"] == []
    assert note["failure_mode_count"] >= 10
    assert note["skill_binding_count"] >= 10


def test_state_index_sync_receipt_and_next_packet_preserve_candidate_boundary():
    index = load_json(AIW / "AI_ASSISTANT_WORK_STATE_INDEX_V0_2.json")
    sync_candidates = sorted(AIW.glob("AI_ASSISTANT_WORK_STATE_SURFACE_SYNC_REPORT_DATASET_GENESIS_*.json"))
    next_candidates = sorted(AIW.glob("AI_ASSISTANT_WORK_NEXT_PACKET_DATASET_MINING_TO_DOMAIN_FISSION_*.json"))
    receipt_candidates = sorted((AIW / "receipts").glob("AI_ASSISTANT_WORK_DATASET_GENESIS_RECEIPT_*.json"))
    assert sync_candidates
    assert next_candidates
    assert receipt_candidates
    sync = load_json(sync_candidates[-1])
    packet = load_json(next_candidates[-1])
    receipt = load_json(receipt_candidates[-1])

    assert index["status"] == "candidate_current_state_not_accepted_canon"
    assert index["authority_boundary"]["mutates_ION_03_registry"] is False
    assert sync["accepted"] is True
    assert sync["alignment"]["candidate_boundary_preserved"] is True
    assert receipt["status"] == "candidate_current_state_receipt_not_accepted_canon"
    assert receipt["authority"]["candidate_only"] is True
    assert receipt["authority"]["mutated_ION_03_registry"] is False
    assert packet["status"] == "candidate_next_packet"
    assert "candidate child-domain fission analysis" in packet["deliverables"]


def test_dataset_genesis_keeps_ui_docs_and_ide_as_specialist_domains_not_generic_skills():
    entries = load_dataset()
    ui_entries = [e for e in entries if "ui_ux_domain" in e["domains_involved"]]
    docs_entries = [e for e in entries if "documentation_writing_domain" in e["domains_involved"]]
    ide_entries = [e for e in entries if e["assistant_embodiment"] == "ide"]
    assert any("UI_ARCHITECT" in e["specialist_agents_required"] for e in ui_entries)
    assert any("DOCS_ARCHITECT" in e["specialist_agents_required"] for e in docs_entries)
    assert any("IDE_CARTOGRAPHER" in e["specialist_agents_required"] for e in ide_entries)
    for entry in ui_entries + docs_entries + ide_entries:
        assert entry["candidate_route"] != "generic_coding_assistant"
