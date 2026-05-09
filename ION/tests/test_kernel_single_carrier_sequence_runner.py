import json
from pathlib import Path

from kernel.ion_single_carrier_sequence_runner import (
    PACKET_TEMPLATE_ID,
    build_single_carrier_sequence_packet,
    default_phase_order,
    evaluate_single_carrier_sequence_output,
    write_single_carrier_sequence_packet,
)
from kernel.ion_template_action_gate import evaluate_template_action_proof


def _repo_root() -> Path:
    root = Path.cwd()
    assert (root / "pyproject.toml").exists()
    assert (root / "ION/REPO_AUTHORITY.md").exists()
    return root


def _sample_completed_output(packet: dict) -> str:
    context_paths = "\n".join(
        f"- {path}: heading/excerpt evidence" for path in packet["context_read_paths"]
    )
    phases = "\n\n".join(f"{heading}\n\ncompleted." for heading in packet["phase_headings"])
    return f"""### CONTEXT PROOF

{context_paths}

### TEMPLATE ACTION PROOF

template_id: {PACKET_TEMPLATE_ID}
action_id: {packet["sequence_id"]}
result: candidate_sequence_return
touched_paths:
  - ION/05_context/current/ACTIVE_SINGLE_CARRIER_SEQUENCE_RECEIPT.json

{phases}
"""


def test_default_phase_order_binds_persona_relay_and_final_persona():
    phases = default_phase_order()
    phase_ids = [phase["phase_id"] for phase in phases]

    assert phase_ids[0] == "PERSONA_INTERFACE_INGRESS"
    assert phase_ids[1] == "RELAY"
    assert "STEWARD" in phase_ids
    assert "VIZIER" in phase_ids
    assert "MASON" in phase_ids
    assert "NEMESIS_OR_VICE_REVIEW" in phase_ids
    assert "SCRIBE" in phase_ids
    assert phase_ids[-2] == "STEWARD_FINAL"
    assert phase_ids[-1] == "PERSONA_INTERFACE_RESPONSE"


def test_single_carrier_packet_ready_without_external_dependencies():
    root = _repo_root()
    packet = build_single_carrier_sequence_packet(
        root,
        carrier="GPT_SANDBOX_CARRIER",
        objective="test single carrier sequence",
    )

    assert packet["verdict"] == "ION_SINGLE_CARRIER_SEQUENCE_PACKET_READY"
    assert packet["missing_required_surfaces"] == []
    assert packet["external_dependencies"]["codex"] is False
    assert packet["external_dependencies"]["mcp"] is False
    assert packet["external_dependencies"]["github"] is False
    assert packet["external_dependencies"]["daemon"] is False
    assert packet["external_dependencies"]["browser_extension"] is False
    assert packet["external_dependencies"]["external_agent_spawn"] is False
    assert packet["phase_headings"][0] == "### ROLE PHASE: PERSONA_INTERFACE_INGRESS"
    assert packet["phase_headings"][-1] == "### ROLE PHASE: PERSONA_INTERFACE_RESPONSE"


def test_single_carrier_packet_write_receipt_candidate():
    root = _repo_root()
    result = write_single_carrier_sequence_packet(
        root,
        carrier="GPT_SANDBOX_CARRIER",
        objective="write sequence packet test",
    )

    assert result["verdict"] == "ION_SINGLE_CARRIER_SEQUENCE_PACKET_READY"
    assert (root / "ION/05_context/current/ACTIVE_SINGLE_CARRIER_SEQUENCE_PACKET.md").exists()
    receipt_path = root / "ION/05_context/current/ACTIVE_SINGLE_CARRIER_SEQUENCE_RECEIPT.json"
    assert receipt_path.exists()

    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    assert receipt["receipt_status"] == "SEQUENCE_PACKET_READY_AWAITING_CARRIER_OUTPUT"
    assert receipt["steward_review_required"] is True
    assert receipt["production_authority"] is False
    assert receipt["live_execution_authority"] is False


def test_single_carrier_sequence_output_evaluation_accepts_complete_return():
    root = _repo_root()
    packet = build_single_carrier_sequence_packet(root, objective="complete output test")
    output = _sample_completed_output(packet)

    evaluation = evaluate_single_carrier_sequence_output(packet=packet, carrier_output=output)

    assert evaluation["accepted"] is True
    assert evaluation["missing_phase_headings"] == []
    assert evaluation["integration_decision"] == "ALLOW_STEWARD_REVIEW"


def test_single_carrier_sequence_output_evaluation_blocks_missing_persona_response():
    root = _repo_root()
    packet = build_single_carrier_sequence_packet(root, objective="missing output test")
    output = _sample_completed_output(packet).replace(
        "### ROLE PHASE: PERSONA_INTERFACE_RESPONSE",
        "### ROLE PHASE: OMITTED_PERSONA_RESPONSE",
    )

    evaluation = evaluate_single_carrier_sequence_output(packet=packet, carrier_output=output)

    assert evaluation["accepted"] is False
    assert "missing_role_phase_heading:### ROLE PHASE: PERSONA_INTERFACE_RESPONSE" in evaluation["findings"]


def test_default_template_action_gate_accepts_single_carrier_template_id():
    root = _repo_root()
    packet = build_single_carrier_sequence_packet(root, objective="template gate test")
    output = _sample_completed_output(packet)

    evaluation = evaluate_template_action_proof(worker_output=output)

    assert evaluation["accepted"] is True
