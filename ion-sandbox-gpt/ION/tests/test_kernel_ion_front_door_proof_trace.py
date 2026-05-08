import json
from pathlib import Path

from kernel.ion_front_door_proof_trace import (
    build_front_door_proof_trace,
    write_front_door_proof_trace,
)


def test_front_door_proof_trace_materializes_full_boundary(tmp_path: Path):
    trace = build_front_door_proof_trace(
        tmp_path,
        operator_message="prove front-door runtime path",
        controlled_system_output="front-door proof response",
        created_at="2026-05-02T00:00:00+00:00",
    )

    assert trace["schema_id"] == "ion.front_door_proof_trace.v1"
    assert trace["projection_mode"] == "DETERMINISTIC_FRONT_DOOR_PROOF_TRACE"
    assert trace["proof_complete"] is True
    assert trace["verdict"] == "ION_FRONT_DOOR_PROOF_TRACE_READY"
    assert trace["production_authority"] is False
    assert trace["live_execution_authority"] is False
    assert trace["steward_verdict"]["live_steward_reasoning"] is False
    assert trace["steward_verdict"]["verdict"] == "APPROVED_WITH_SCOPE"
    assert trace["boundary_proof"]["persona_ingress_id"].startswith("fdmsg-")
    assert trace["boundary_proof"]["relay_packet_id"].startswith("fdrelay-")
    assert trace["boundary_proof"]["steward_envelope_id"].startswith("fdsteward-")
    assert trace["boundary_proof"]["dispatch_packet_path"].endswith(".dispatch_packet.json")
    assert trace["missing_witness_paths"] == []
    assert trace["validation_errors"] == []
    assert [stage["sequence"] for stage in trace["stage_sequence"]] == sorted(
        stage["sequence"] for stage in trace["stage_sequence"]
    )
    assert {stage["stage"] for stage in trace["stage_sequence"]} >= {
        "operator_message_received",
        "relay_semantic_boundary_packet",
        "steward_routing_envelope",
        "queue_item_dispatched",
        "persona_response_package",
        "front_stage_council_receipt",
        "conversational_receipt",
    }
    for witness in trace["witness_paths"]:
        assert (tmp_path / witness).exists(), witness


def test_front_door_proof_trace_blocks_when_dispatch_is_absent(tmp_path: Path):
    trace = build_front_door_proof_trace(
        tmp_path,
        operator_message="prove front-door without dispatch",
        controlled_system_output="front-door proof response",
        created_at="2026-05-02T00:00:00+00:00",
        dispatch=False,
    )

    assert trace["proof_complete"] is False
    assert trace["verdict"] == "ION_FRONT_DOOR_PROOF_TRACE_BLOCKED"
    assert trace["boundary_proof"]["dispatch_packet_path"] is None


def test_write_front_door_proof_trace_writes_active_and_history(tmp_path: Path):
    trace = write_front_door_proof_trace(
        tmp_path,
        operator_message="write front-door proof",
        controlled_system_output="front-door proof response",
        created_at="2026-05-02T00:00:00+00:00",
    )

    active = tmp_path / "ION/05_context/current/ACTIVE_FRONT_DOOR_PROOF_TRACE.json"
    history = tmp_path / trace["proof_trace_path"]
    assert active.exists()
    assert history.exists()
    loaded = json.loads(active.read_text(encoding="utf-8"))
    assert loaded["trace_id"] == trace["trace_id"]
