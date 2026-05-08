"""Focused tests for ION self-knowledge onboarding-wiring candidate evidence.

These tests validate sandbox-local onboarding trace behavior. They do not
accept the candidate into onboarding law or ION/03_registry.
"""
from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
SK = ROOT / "ION/05_context/current/self_knowledge"
PROMO = SK / "promotion_candidate"
REPORT = PROMO / "SELF_KNOWLEDGE_ONBOARDING_WIRING_SIMULATION_REPORT_20260508T045721Z.json"
OVERLAY = PROMO / "SELF_KNOWLEDGE_ONBOARDING_WIRING_OVERLAY_V0_2.json"
SCRIPT = SK / "simulate_self_knowledge_onboarding_wiring.py"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_onboarding_overlay_is_candidate_only_and_no_mutation_authority():
    overlay = load_json(OVERLAY)
    assert overlay["status"] == "candidate_current_state_not_accepted_canon"
    boundary = overlay["authority_boundary"]
    assert boundary["candidate_only"] is True
    assert boundary["mutates_active_onboarding_packets"] is False
    assert boundary["mutates_ION_03_registry"] is False
    assert boundary["requires_explicit_acceptance_to_land"] is True
    required = overlay["candidate_route_intercept"]["required_sequence_for_matching_tasks"]
    assert "mount_active_self_knowledge_mount_packet" in required
    assert "load_self_knowledge_route_registry" in required


def test_onboarding_simulation_report_passed_and_exercises_two_carriers():
    report = load_json(REPORT)
    assert report["accepted"] is True
    assert report["status"] == "accepted_candidate_evidence"
    assert report["simulation_mode"] == "sandbox_local_onboarding_trace_not_external_codex"
    assert report["coverage"]["cases_accepted"] == report["coverage"]["carrier_cases"]
    assert set(report["coverage"]["carriers_exercised"]) >= {"GPT_SANDBOX_CARRIER", "CODEX_CLI_CARRIER"}
    assert report["authority_boundary"]["mutated_active_onboarding_packets"] is False
    assert report["authority_boundary"]["mutated_ION_03_registry"] is False


def test_ion_about_ion_cases_mount_self_knowledge_before_answer():
    report = load_json(REPORT)
    ion_cases = [case for case in report["cases"] if case["expected_ion_about_ion"]]
    assert ion_cases
    for case in ion_cases:
        actions = [step["action"] for step in case["trace"]]
        assert "classify_operator_task" in actions
        assert "mount_active_self_knowledge_mount_packet" in actions
        assert "load_self_knowledge_route_registry" in actions
        assert "select_self_knowledge_route" in actions
        assert "load_required_domain_packets" in actions
        assert "answer_or_act_with_non_claims" in actions
        assert actions.index("classify_operator_task") < actions.index("mount_active_self_knowledge_mount_packet")
        assert actions.index("mount_active_self_knowledge_mount_packet") < actions.index("load_self_knowledge_route_registry")
        assert actions.index("load_self_knowledge_route_registry") < actions.index("answer_or_act_with_non_claims")
        assert case["matched_route_id"] == case["expected_route_id"]
        assert case["loaded_domains"]


def test_non_ion_case_bypasses_self_knowledge_route():
    report = load_json(REPORT)
    non_ion_cases = [case for case in report["cases"] if not case["expected_ion_about_ion"]]
    assert len(non_ion_cases) == 1
    actions = [step["action"] for step in non_ion_cases[0]["trace"]]
    assert "skip_self_knowledge_route" in actions
    assert "continue_normal_active_packet_route" in actions
    assert "mount_active_self_knowledge_mount_packet" not in actions
    assert "load_self_knowledge_route_registry" not in actions
    assert non_ion_cases[0]["matched_route_id"] is None


def test_onboarding_simulation_covers_all_candidate_routes_and_domains():
    report = load_json(REPORT)
    route_registry = yaml.safe_load((SK / "candidate_registries/route_registry.candidate.yaml").read_text(encoding="utf-8"))
    domain_registry = yaml.safe_load((SK / "candidate_registries/domain_registry.candidate.yaml").read_text(encoding="utf-8"))
    route_ids = {route["route_id"] for route in route_registry["routes"]}
    domain_ids = {domain["domain_id"] for domain in domain_registry["domains"]}
    assert route_ids <= set(report["coverage"]["matched_routes"])
    assert domain_ids <= set(report["coverage"]["loaded_domain_union"])


def test_onboarding_wiring_script_is_present_but_not_a_landing_action():
    text = SCRIPT.read_text(encoding="utf-8")
    assert "does not mutate active carrier" in text
    assert "onboarding" in text
    assert "does not land ION/03_registry/self_knowledge" in text
    assert "external Codex/MCP/daemon invocation" in text
