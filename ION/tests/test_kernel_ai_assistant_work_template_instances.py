"""Focused tests for AI Assistant Work template instance corpus and agent boot exercises.

These tests validate current-context candidate artifacts only. They do not claim
accepted template law, real isolated agent execution, registry landing,
product-front-door mutation, external IDE/CLI/cloud/PR/background-agent execution,
or human acceptance.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
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
INSTANCE_DIR = AIW / "template_instances"
EXERCISE_DIR = AIW / "agent_boot_exercises"
SPEC_DIR = AIW / "template_specs"
BOOT_DIR = AIW / "agent_boots"
SIM = AIW / "simulations/AI_ASSISTANT_WORK_TEMPLATE_INSTANCE_AGENT_BOOT_EXERCISE_SIMULATION_REPORT_LATEST.json"
VAL = AIW / "validation/AI_ASSISTANT_WORK_TEMPLATE_INSTANCE_AGENT_BOOT_EXERCISE_VALIDATION_NOTE_LATEST.json"

REQUIRED_TEMPLATE_IDS = {
    "screen_state_matrix_packet",
    "pr_review_packet",
    "background_queue_result_intake_packet",
    "terminal_proof_receipt_packet",
    "api_docs_example_validation_packet",
    "release_readiness_matrix_packet",
    "migration_plan_and_rollback_packet",
    "joc_work_surface_ui_packet",
}

REQUIRED_ROLE_IDS = {
    "UI_STATE_MODELER",
    "PR_REVIEW_STEWARD",
    "BACKGROUND_QUEUE_STEWARD",
    "TERMINAL_PROOF_CURATOR",
    "EXAMPLE_RUNNER",
    "RELEASE_EVIDENCE_CURATOR",
    "MIGRATION_MASON",
    "FRONTEND_WORK_SURFACE_ARCHITECT",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_instance_corpus_index_has_candidate_boundary_and_complete_coverage():
    index = load_yaml(INSTANCE_DIR / "AI_ASSISTANT_WORK_TEMPLATE_INSTANCE_CORPUS_INDEX_V0_1.yaml")
    assert index["status"] == "candidate_current_state_not_accepted_canon"
    assert index["authority_boundary"]["candidate_only"] is True
    assert index["authority_boundary"]["mutates_ION_03_registry"] is False
    assert index["authority_boundary"]["requires_explicit_acceptance_to_land"] is True
    assert index["template_spec_count"] == len(REQUIRED_TEMPLATE_IDS)
    assert index["valid_instance_count"] == len(REQUIRED_TEMPLATE_IDS)
    assert index["expected_rejection_count"] == len(REQUIRED_TEMPLATE_IDS)
    assert set(index["template_ids"]) == REQUIRED_TEMPLATE_IDS


def test_every_template_spec_has_valid_and_rejection_instance_with_matching_boundary():
    for template_id in REQUIRED_TEMPLATE_IDS:
        spec = load_yaml(SPEC_DIR / f"{template_id}.template_spec.yaml")
        valid = load_json(INSTANCE_DIR / f"{template_id}.minimal_valid.instance.json")
        rejection = load_json(INSTANCE_DIR / f"{template_id}.expected_rejection.instance.json")
        assert valid["template_id"] == template_id
        assert rejection["template_id"] == template_id
        assert valid["primary_agent"] == spec["primary_agent"]
        assert rejection["primary_agent"] == spec["primary_agent"]
        assert valid["authority_boundary"]["candidate_only"] is True
        assert rejection["authority_boundary"]["candidate_only"] is True
        assert valid["expected_validation"]["should_pass"] is True
        assert rejection["expected_validation"]["should_pass"] is False
        assert "NON_CLAIMS" in valid["sections"]
        non_claims = " ".join(valid["sections"]["NON_CLAIMS"]).lower()
        assert "candidate" in non_claims or "not accepted" in non_claims or "not claimed" in non_claims


def test_agent_boot_exercise_index_has_specialist_first_coverage():
    index = load_yaml(EXERCISE_DIR / "AI_ASSISTANT_WORK_AGENT_BOOT_EXERCISE_INDEX_V0_1.yaml")
    assert index["status"] == "candidate_current_state_not_accepted_canon"
    assert index["authority_boundary"]["candidate_only"] is True
    assert index["exercise_count"] == len(REQUIRED_ROLE_IDS)
    assert set(index["role_ids"]) == REQUIRED_ROLE_IDS
    for rel in index["exercise_files"]:
        exercise = load_json(ROOT / rel)
        assert exercise["role_id"] in REQUIRED_ROLE_IDS
        assert exercise["dispatch_assertion"]["specialist_first"] is True
        assert exercise["dispatch_assertion"]["generic_implementation_first"] is False
        assert Path(ROOT / exercise["valid_instance_ref"]).exists()
        assert Path(ROOT / exercise["rejection_case_ref"]).exists()


def test_each_agent_boot_exercise_matches_owned_template_spec():
    for role_id in REQUIRED_ROLE_IDS:
        exercise = load_json(EXERCISE_DIR / f"{role_id}.boot_exercise.json")
        boot = load_yaml(BOOT_DIR / f"{role_id}.agent_boot.yaml")
        spec = load_yaml(SPEC_DIR / f"{exercise['template_id']}.template_spec.yaml")
        assert spec["primary_agent"] == role_id
        assert exercise["template_id"] in boot["owned_template_specs"]
        assert exercise["dispatch_assertion"]["selected_agent"] == role_id
        assert exercise["dispatch_assertion"]["selected_template"] == exercise["template_id"]
        assert exercise["expected_result"]["valid_instance_should_pass"] is True
        assert exercise["expected_result"]["rejection_case_should_fail"] is True


def test_validation_report_accepts_valid_instances_expected_rejections_and_boot_exercises():
    report = load_json(SIM)
    assert report["status"] == "accepted_candidate_validation"
    assert report["candidate_only"] is True
    assert report["template_spec_count"] == len(REQUIRED_TEMPLATE_IDS)
    assert report["valid_instance_count"] == len(REQUIRED_TEMPLATE_IDS)
    assert report["expected_rejection_count"] == len(REQUIRED_TEMPLATE_IDS)
    assert report["agent_boot_exercise_count"] == len(REQUIRED_ROLE_IDS)
    assert report["valid_instances_accepted"] == len(REQUIRED_TEMPLATE_IDS)
    assert report["expected_rejections_accepted"] == len(REQUIRED_TEMPLATE_IDS)
    assert report["agent_boot_exercises_accepted"] == len(REQUIRED_ROLE_IDS)
    assert report["findings"] == []


def test_latest_validation_note_and_state_index_preserve_non_claims():
    note = load_json(VAL)
    assert note["status"] == "accepted_candidate_validation"
    assert note["candidate_only"] is True
    assert note["external_execution_authority"] is False
    state = load_json(AIW / "AI_ASSISTANT_WORK_STATE_INDEX_V0_5.json")
    assert state["status"] == "candidate_current_state_not_accepted_canon"
    assert state["authority_boundary"]["candidate_only"] is True
    assert state["authority_boundary"]["mutates_ION_03_registry"] is False
    assert "AI_ASSISTANT_WORK_NEXT_PACKET_ROUTE_COMPILER_AND_PROMOTION_PLAN" in state["recommended_next_packet"]


def test_validator_script_exits_successfully():
    result = subprocess.run(
        [sys.executable, "-S", str(AIW / "validate_ai_assistant_work_template_instances.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert report["status"] == "accepted_candidate_validation"
