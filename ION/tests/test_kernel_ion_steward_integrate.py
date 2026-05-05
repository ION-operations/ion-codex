from pathlib import Path

import json

from kernel.ion_steward_integrate import steward_integrate_pending_queue, steward_integrate_return


def _accepted_output():
    return """### CONTEXT PROOF
- ION/REPO_AUTHORITY.md excerpt line sha256 abc

### TEMPLATE ACTION PROOF
template_id: ion.template.autonomous_loop.local_worker.v1
action_id: v101.step_01
touched_paths:
  - ION/05_context/current/LAST_ION_AUTONOMOUS_LOOP_RESULT.json
result: accepted_state_delta_candidate
"""


def test_steward_integrate_writes_receipt_and_queue(tmp_path):
    (tmp_path / "ION" / "05_context" / "current").mkdir(parents=True)
    result = steward_integrate_return(
        ion_root=tmp_path,
        worker_output=_accepted_output(),
        cycle_id="cycle",
        step_index=1,
        write=True,
    )
    assert result["accepted"] is True
    assert (tmp_path / result["receipt_path"]).exists()
    queue = tmp_path / result["queue_path"]
    assert queue.exists()
    assert "cycle_step_01_steward_integration" in queue.read_text(encoding="utf-8")


def test_steward_integrate_rejects_failed_gate(tmp_path):
    result = steward_integrate_return(
        ion_root=tmp_path,
        worker_output="### CONTEXT PROOF\nno template proof\n",
        cycle_id="cycle",
        step_index=1,
        write=False,
    )
    assert result["accepted"] is False
    assert result["receipt"]["decision"] == "REJECTED_BY_TEMPLATE_ACTION_GATE"


def test_steward_integrate_pending_queue_marks_items_integrated(tmp_path):
    current = tmp_path / "ION/05_context/current"
    current.mkdir(parents=True)
    task_output = current / "task_returns/worker.md"
    task_output.parent.mkdir(parents=True)
    task_output.write_text(_accepted_output(), encoding="utf-8")
    queue = {
        "schema_id": "ion.steward_integration_queue.v1",
        "items": [
            {
                "schema_id": "ion.steward_integration_queue_item.v1",
                "status": "PENDING_STEWARD_INTEGRATION",
                "role": "steward",
                "index": 1,
                "task_output_path": "ION/05_context/current/task_returns/worker.md",
                "task_output_sha256": "abc",
            }
        ],
        "production_authority": False,
        "live_execution_authority": False,
    }
    (current / "ACTIVE_STEWARD_INTEGRATION_QUEUE.json").write_text(json.dumps(queue), encoding="utf-8")
    turn = {
        "schema_id": "ion.carrier_turn_packet.v1",
        "return_intake_state": {
            "schema_id": "ion.carrier_return_intake_state.v1",
            "status": "ALL_ACCEPTED_READY_FOR_STEWARD",
            "steward_queue_count": 1,
        },
    }
    (current / "ACTIVE_CARRIER_TURN_PACKET.json").write_text(json.dumps(turn), encoding="utf-8")

    result = steward_integrate_pending_queue(ion_root=tmp_path, write=True)

    assert result["accepted"] is True
    assert result["processed_count"] == 1
    updated = json.loads((current / "ACTIVE_STEWARD_INTEGRATION_QUEUE.json").read_text(encoding="utf-8"))
    assert updated["items"][0]["status"] == "STEWARD_INTEGRATED"
    receipt_path = tmp_path / updated["items"][0]["steward_receipt_path"]
    assert receipt_path.exists()
    updated_turn = json.loads((current / "ACTIVE_CARRIER_TURN_PACKET.json").read_text(encoding="utf-8"))
    assert updated_turn["steward_integration_state"]["status"] == "STEWARD_INTEGRATION_COMPLETE"
    assert updated_turn["return_intake_state"]["status"] == "STEWARD_INTEGRATION_COMPLETE"


def test_steward_integrate_pending_queue_rejects_missing_task_output(tmp_path):
    current = tmp_path / "ION/05_context/current"
    current.mkdir(parents=True)
    queue = {
        "schema_id": "ion.steward_integration_queue.v1",
        "items": [
            {
                "schema_id": "ion.steward_integration_queue_item.v1",
                "status": "PENDING_STEWARD_INTEGRATION",
                "role": "relay",
                "index": 2,
                "task_output_path": "ION/05_context/current/task_returns/missing.md",
            }
        ],
    }
    (current / "ACTIVE_STEWARD_INTEGRATION_QUEUE.json").write_text(json.dumps(queue), encoding="utf-8")

    result = steward_integrate_pending_queue(ion_root=tmp_path, write=True)

    assert result["accepted"] is False
    assert result["rejected_count"] == 1
    updated = json.loads((current / "ACTIVE_STEWARD_INTEGRATION_QUEUE.json").read_text(encoding="utf-8"))
    assert updated["items"][0]["status"] == "STEWARD_INTEGRATION_REJECTED"
    assert updated["items"][0]["steward_gate_findings"] == ["missing_task_output_for_steward_integration"]
