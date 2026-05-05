import json
from pathlib import Path

from kernel.ion_carrier_workflow_audit import audit_carrier_workflow


def write_json(root: Path, rel: str, payload: dict):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def seed_zero_spawn_runtime(root: Path):
    current = "ION/05_context/current"
    write_json(root, f"{current}/ACTIVE_WORK_PACKET.json", {"schema_id": "ion.carrier_onboard_packet.v1", "objective": "zero spawn"})
    write_json(root, f"{current}/ACTIVE_ROLE_SPAWN_PLAN.json", {
        "schema_id": "ion.carrier_cycle_plan.v1",
        "carrier": "codex_extension",
        "workstream": "implementation",
        "objective": "zero spawn",
        "spawn_policy": "required",
        "spawn_row_limit": 0,
        "active_spawn_count": 0,
        "deferred_spawn_count": 1,
        "required_surfaces_ok": True,
        "missing_required_surfaces": {},
        "execution_bundle_root": "ION/05_context/current/execution_cycles/deferred",
        "execution_bundle_materialized": False,
        "trace_path": None,
        "session_paths": [],
        "handoff_paths": [],
        "role_spawn_plan": [
            {
                "index": 1,
                "role": "steward",
                "required_by_kernel": True,
                "spawn_intent": True,
                "spawn": False,
                "spawn_deferral_reason": "deferred_by_spawn_row_limit",
                "authority": "DEFERRED_BY_SPAWN_ROW_LIMIT",
            }
        ],
        "production_authority": False,
        "live_execution_authority": False,
    })
    write_json(root, f"{current}/ACTIVE_CARRIER_TURN_PACKET.json", {
        "schema_id": "ion.carrier_turn_packet.v1",
        "carrier": "codex_extension",
        "mode": "plan-only",
        "objective": "zero spawn",
        "active_spawn_plan_path": f"{current}/ACTIVE_ROLE_SPAWN_PLAN.json",
        "task_return_ledger_path": f"{current}/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json",
        "steward_integration_queue_path": f"{current}/ACTIVE_STEWARD_INTEGRATION_QUEUE.json",
        "operator_message_queue_path": f"{current}/ACTIVE_OPERATOR_MESSAGE_QUEUE.json",
        "human_gate_queue_path": f"{current}/ACTIVE_HUMAN_GATE_QUEUE.json",
        "operator_message_classification": {"classification": "new_work_directive"},
        "spawn_row_limit": 0,
        "spawn_queue": [],
        "return_intake_state": {
            "schema_id": "ion.carrier_return_intake_state.v1",
            "status": "NO_TASK_RETURNS_REQUIRED",
            "accepted_count": 0,
            "rejected_count": 0,
            "pending_count": 0,
        },
        "blocked_by_findings": False,
        "blocked_by_human_gate": False,
        "production_authority": False,
        "live_execution_authority": False,
    })
    write_json(root, f"{current}/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json", {
        "schema_id": "ion.carrier_task_return_ledger.v1",
        "active_spawn_plan_path": f"{current}/ACTIVE_ROLE_SPAWN_PLAN.json",
        "records": [],
        "production_authority": False,
        "live_execution_authority": False,
    })
    write_json(root, f"{current}/ACTIVE_STEWARD_INTEGRATION_QUEUE.json", {
        "schema_id": "ion.steward_integration_queue.v1",
        "active_spawn_plan_path": f"{current}/ACTIVE_ROLE_SPAWN_PLAN.json",
        "items": [],
        "production_authority": False,
        "live_execution_authority": False,
    })
    write_json(root, f"{current}/ACTIVE_OPERATOR_MESSAGE_QUEUE.json", {
        "schema_id": "ion.operator_message_queue.v1",
        "items": [],
        "production_authority": False,
        "live_execution_authority": False,
    })
    write_json(root, f"{current}/ACTIVE_HUMAN_GATE_QUEUE.json", {
        "schema_id": "ion.human_gate_queue.v1",
        "gates": [],
        "production_authority": False,
        "live_execution_authority": False,
    })
    (root / "pyproject.toml").write_text("[project]\nname='workflow-audit-test'\n", encoding="utf-8")
    (root / "ION/03_registry/boots").mkdir(parents=True, exist_ok=True)
    (root / "ION/04_packages/kernel").mkdir(parents=True, exist_ok=True)
    authority = root / "ION/REPO_AUTHORITY.md"
    authority.parent.mkdir(parents=True, exist_ok=True)
    authority.write_text("authority\n", encoding="utf-8")


def test_carrier_workflow_audit_accepts_lawful_zero_spawn_plan_only_turn(tmp_path):
    seed_zero_spawn_runtime(tmp_path)

    result = audit_carrier_workflow(tmp_path)

    assert result["verdict"] == "ION_CARRIER_WORKFLOW_READY"
    assert result["accepted"] is True
    assert result["findings"] == []
