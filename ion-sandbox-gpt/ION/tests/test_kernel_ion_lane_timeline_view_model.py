import json
from pathlib import Path

from kernel.ion_lane_timeline_view_model import build_lane_timeline_view_model, write_lane_timeline_view_model


def write_json(root: Path, rel: str, payload: dict):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_lane_timeline_projects_requested_effective_lane_and_organ_order(tmp_path):
    current = "ION/05_context/current"
    write_json(
        tmp_path,
        f"{current}/ACTIVE_OPERATOR_MESSAGE_QUEUE.json",
        {
            "items": [
                {
                    "id": "msg-1",
                    "timestamp": "2026-05-02T00:00:01+00:00",
                    "requested_lane": "realtime",
                    "effective_lane": "checked",
                    "lane_change_reason": "high-risk claim",
                    "status": "downgraded",
                }
            ]
        },
    )
    write_json(
        tmp_path,
        f"{current}/ACTIVE_CARRIER_TURN_PACKET.json",
        {
            "message_id": "msg-1",
            "timestamp": "2026-05-02T00:00:02+00:00",
            "requested_lane": "realtime",
            "effective_lane": "checked",
            "verdict": "CARRIER_TURN_ACCEPTED",
        },
    )
    write_json(
        tmp_path,
        f"{current}/ACTIVE_ROLE_SPAWN_PLAN.json",
        {"role_spawn_plan": [{"index": 1, "role": "STEWARD", "spawn": True, "message_id": "msg-1", "authority": "ORCHESTRATION_BOUNDED"}]},
    )

    model = build_lane_timeline_view_model(tmp_path)

    assert model["schema_id"] == "ion.lane_timeline_view_model.v1"
    assert model["event_count"] == 3
    assert [event["organ"] for event in model["events"]] == ["operator", "carrier", "worker"]
    first = model["events"][0]
    assert first["requested_lane"] == "realtime"
    assert first["effective_lane"] == "checked"
    assert first["status"] == "downgraded"
    assert model["messages"][0]["current_state"] == "downgraded"


def test_lane_timeline_marks_human_gate_as_blocked(tmp_path):
    current = "ION/05_context/current"
    write_json(
        tmp_path,
        f"{current}/ACTIVE_HUMAN_GATE_QUEUE.json",
        {"gates": [{"id": "gate-1", "message_id": "msg-2", "status": "open", "reason": "operator approval"}]},
    )

    model = build_lane_timeline_view_model(tmp_path)

    assert model["events"][0]["status"] == "blocked"
    assert model["messages"][0]["current_state"] == "unresolved"


def test_lane_timeline_adds_receipt_hydration_warning_event(tmp_path):
    current = "ION/05_context/current"
    write_json(
        tmp_path,
        f"{current}/ACTIVE_RECEIPT_HYDRATION_VIEW_MODEL.json",
        {
            "records": [
                {
                    "receipt_id": "r1",
                    "utterance_id": "u-missing",
                    "resolution_method": "unresolved",
                    "warning": "receipt utterance_id does not resolve",
                }
            ]
        },
    )

    model = build_lane_timeline_view_model(tmp_path)

    assert model["events"][0]["organ"] == "ui"
    assert model["events"][0]["status"] == "failed"
    assert model["events"][0]["receipt_id"] == "r1"


def test_lane_timeline_projects_front_door_proof_trace_organs(tmp_path):
    current = "ION/05_context/current"
    write_json(
        tmp_path,
        f"{current}/ACTIVE_FRONT_DOOR_PROOF_TRACE.json",
        {
            "trace_id": "fdproof-1",
            "generated_at": "2026-05-02T00:00:01+00:00",
            "boundary_proof": {"persona_ingress_id": "fdmsg-1"},
            "steward_verdict": {"claim_class": "C2", "verdict": "APPROVED_WITH_SCOPE"},
            "stage_sequence": [
                {"sequence": 10, "stage": "operator_message_received", "organ": "operator", "status": "accepted", "receipt_id": "r-ingress"},
                {"sequence": 20, "stage": "relay_semantic_boundary_packet", "organ": "relay", "status": "accepted", "receipt_id": "r-ingress"},
                {"sequence": 30, "stage": "steward_routing_envelope", "organ": "steward", "status": "approved_with_scope", "receipt_id": "r-council"},
                {"sequence": 40, "stage": "persona_response_package", "organ": "persona", "status": "accepted", "receipt_id": "r-return"},
            ],
        },
    )

    model = build_lane_timeline_view_model(tmp_path)

    assert [event["organ"] for event in model["events"]] == ["operator", "relay", "steward", "persona"]
    assert model["events"][2]["claim_class"] == "C2"
    assert model["messages"][0]["current_state"] == "clean"


def test_write_lane_timeline_view_model(tmp_path):
    model = write_lane_timeline_view_model(tmp_path)
    out = tmp_path / "ION/05_context/current/ACTIVE_LANE_TIMELINE_VIEW_MODEL.json"
    assert out.exists()
    assert json.loads(out.read_text(encoding="utf-8"))["schema_id"] == model["schema_id"]
