"""Focused tests for candidate ION self-knowledge route usage.

These tests validate sandbox-local route-usage evidence. They do not claim
external Codex execution or accepted registry law.
"""
from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
SK = ROOT / "ION/05_context/current/self_knowledge"
PROMOTION = SK / "promotion_candidate"
TARGET_REGISTRY = ROOT / "ION/03_registry/self_knowledge"
REPORT = PROMOTION / "SELF_KNOWLEDGE_ROUTE_USAGE_SIMULATION_REPORT_20260508T043119Z.json"
GATE = PROMOTION / "SELF_KNOWLEDGE_ACCEPTANCE_GATE_STATUS_V0_2.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_self_knowledge_route_usage_report_exercises_every_candidate_route():
    report = load_json(REPORT)
    assert report["accepted"] is True
    assert report["status"] == "accepted_candidate_evidence"
    assert report["simulation_mode"] == "sandbox_local_route_usage_not_external_codex"
    assert report["coverage"]["missing_route_coverage"] == []
    assert report["coverage"]["route_count"] == 7
    assert report["coverage"]["case_count"] == 7
    assert report["coverage"]["cases_accepted"] == 7
    assert report["coverage"]["loaded_domain_count"] == 14
    assert report["findings"] == []


def test_self_knowledge_route_usage_criterion_7_is_ready_candidate_not_acceptance():
    gate = load_json(GATE)
    criteria = {item["id"]: item for item in gate["acceptance_criteria"]}
    assert criteria[7]["status"] == "ready_candidate"
    assert "external Codex not claimed" in criteria[7]["evidence"]
    assert gate["status"] == "promotion_ready_candidate_blocked_on_explicit_acceptance_only"
    assert "No explicit human/Steward acceptance in this turn." in gate["landing_blockers"]


def test_self_knowledge_route_usage_preserves_no_registry_landing():
    report = load_json(REPORT)
    assert TARGET_REGISTRY.exists() is False
    assert report["production_authority"] is False
    assert report["live_execution_authority"] is False
    assert "This simulation does not accept or land ION/03_registry/self_knowledge." in report["non_claims"]


def test_self_knowledge_route_registry_now_routes_recovery_anti_regression_domain():
    candidate = load_yaml(SK / "candidate_registries/route_registry.candidate.yaml")
    mirror = load_yaml(PROMOTION / "apply_tree/ION/03_registry/self_knowledge/route_registry.yaml")
    for registry in (candidate, mirror):
        routes = {route["route_id"]: route for route in registry["routes"]}
        assert "route.ion_recovery_anti_regression" in routes
        recovery = routes["route.ion_recovery_anti_regression"]
        assert "ion_recovery_anti_regression" in recovery["required_domains"]
        assert "no_stale_resurfacing" in recovery["anti_drift_required"]
        assert "no_hallucinated_replacement" in recovery["anti_drift_required"]


def test_self_knowledge_route_usage_answers_block_known_reductions():
    report = load_json(REPORT)
    by_route = {case["matched_route_id"]: case["answer_draft"] for case in report["cases"]}
    assert "not the intended center" in by_route["route.full_local_codex_api_ion"]
    assert "API-like backend" in by_route["route.full_local_codex_api_ion"]
    assert "not reduced ION" in by_route["route.gpt_sandbox_adaptation"]
    assert "no external spawn claim" in by_route["route.gpt_sandbox_adaptation"]
    assert "donor material is not active authority" in by_route["route.ion_authority_classification"]
