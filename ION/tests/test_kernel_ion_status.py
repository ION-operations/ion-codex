import json
from pathlib import Path

from kernel.ion_status import build_ion_status


def write_json(root: Path, rel: str, payload: dict):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_current_status_surfaces_v108_preservation_and_mcp_donor_reconciliation():
    repo = Path(__file__).resolve().parents[2]
    status = build_ion_status(repo)

    assert status["schema_id"] == "ion.status.v1"
    assert status["production_authority"] is False
    assert status["live_execution_authority"] is False
    package = status["safe_full_project_package"]
    assert package["path_pattern"] == "ION/05_context/current/SAFE_FULL_PROJECT_PACKAGE_RESULT_V*.json"
    if package["present"]:
        assert package["accepted"] is True
        assert package["zip_root_verdict"] == "ZIP_ROOT_CONFIRMED"
    else:
        assert package["path"] is None
        assert package["accepted"] is None
        assert package["zip_root_verdict"] is None
    assert status["v72_mcp_donor_reconciliation"]["verdict"] == "V72_MCP_DONOR_RECONCILIATION_PASS"
    assert status["v72_mcp_donor_reconciliation"]["missing_donor_surface_count"] == 0
    assert status["v72_mcp_donor_reconciliation"]["forbidden_runtime_file_count"] == 0
    assert status["v72_mcp_donor_reconciliation"]["production_authority"] is False


def test_status_does_not_require_generated_package_sidecar_evidence_for_mount_ready(tmp_path):
    current = "ION/05_context/current"
    write_json(tmp_path, f"{current}/ACTIVE_CURSOR_HOOK_STATE.json", {"status": "projected_not_connected"})
    write_json(tmp_path, f"{current}/ACTIVE_WORK_PACKET.json", {"objective": "fresh package mount"})
    write_json(tmp_path, f"{current}/ACTIVE_ROLE_SPAWN_PLAN.json", {
        "execution_bundle_materialized": False,
        "role_spawn_plan": [
            {"role": "STEWARD", "spawn_intent": True, "spawn": False, "spawn_deferral_reason": "deferred_by_spawn_row_limit"},
        ],
    })
    write_json(tmp_path, f"{current}/ACTIVE_CARRIER_TURN_PACKET.json", {"objective": "fresh package mount"})
    write_json(tmp_path, f"{current}/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json", {"records": []})
    write_json(tmp_path, f"{current}/ACTIVE_STEWARD_INTEGRATION_QUEUE.json", {"items": []})
    write_json(tmp_path, f"{current}/ACTIVE_OPERATOR_MESSAGE_QUEUE.json", {"items": []})
    write_json(tmp_path, f"{current}/ACTIVE_HUMAN_GATE_QUEUE.json", {"gates": []})
    write_json(tmp_path, f"{current}/V108_V72_MCP_DONOR_RECONCILIATION_AUDIT.json", {
        "reconciliation_verdict": "V72_MCP_DONOR_RECONCILIATION_PASS",
        "restored_donor_surface_count": 38,
        "missing_donor_surface_count": 0,
        "forbidden_runtime_file_count": 0,
        "cursor_bridge_preserved": True,
        "donor_runtime_receipts_restored": False,
        "production_authority": False,
        "live_execution_authority": False,
    })
    (tmp_path / "pyproject.toml").write_text("[project]\nname='mount-test'\n", encoding="utf-8")
    (tmp_path / "ION/03_registry/boots").mkdir(parents=True, exist_ok=True)
    (tmp_path / "ION/04_packages/kernel").mkdir(parents=True, exist_ok=True)
    authority = tmp_path / "ION/REPO_AUTHORITY.md"
    authority.parent.mkdir(parents=True, exist_ok=True)
    authority.write_text("authority\n", encoding="utf-8")

    status = build_ion_status(tmp_path)

    assert status["verdict"] == "ION_STATUS_READY"
    assert status["missing_state_surfaces"] == []
    assert status["trunk_preservation"]["present"] is False
    assert status["safe_full_project_package"]["present"] is False
    assert status["spawn_queue_count"] == 0
    assert status["plan_spawn_count"] == 0
    assert status["deferred_spawn_count"] == 1
    assert status["execution_bundle_materialized"] is False
    assert status["safe_full_project_package"]["path"] is None
    assert status["safe_full_project_package"]["path_pattern"] == "ION/05_context/current/SAFE_FULL_PROJECT_PACKAGE_RESULT_V*.json"
    assert "trunk_preservation_report" in status["optional_evidence_paths"]
    assert status["optional_evidence_paths"]["safe_full_project_package_result"] == "ION/05_context/current/SAFE_FULL_PROJECT_PACKAGE_RESULT_V*.json"


def test_status_surfaces_rejected_steward_integration_as_next_action(tmp_path):
    current = "ION/05_context/current"
    write_json(tmp_path, f"{current}/ACTIVE_CURSOR_HOOK_STATE.json", {"status": "projected_not_connected"})
    write_json(tmp_path, f"{current}/ACTIVE_WORK_PACKET.json", {"objective": "rejected steward repair"})
    write_json(tmp_path, f"{current}/ACTIVE_ROLE_SPAWN_PLAN.json", {"role_spawn_plan": []})
    write_json(tmp_path, f"{current}/ACTIVE_CARRIER_TURN_PACKET.json", {"objective": "rejected steward repair", "spawn_queue": []})
    write_json(tmp_path, f"{current}/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json", {"records": []})
    write_json(
        tmp_path,
        f"{current}/ACTIVE_STEWARD_INTEGRATION_QUEUE.json",
        {
            "items": [
                {
                    "index": 1,
                    "role": "steward",
                    "status": "STEWARD_INTEGRATION_REJECTED",
                    "steward_gate_findings": ["missing_template_action_proof_heading"],
                }
            ]
        },
    )
    write_json(tmp_path, f"{current}/ACTIVE_OPERATOR_MESSAGE_QUEUE.json", {"items": []})
    write_json(tmp_path, f"{current}/ACTIVE_HUMAN_GATE_QUEUE.json", {"gates": []})
    write_json(
        tmp_path,
        f"{current}/V108_V72_MCP_DONOR_RECONCILIATION_AUDIT.json",
        {
            "reconciliation_verdict": "V72_MCP_DONOR_RECONCILIATION_PASS",
            "missing_donor_surface_count": 0,
            "forbidden_runtime_file_count": 0,
            "production_authority": False,
            "live_execution_authority": False,
        },
    )
    (tmp_path / "pyproject.toml").write_text("[project]\nname='mount-test'\n", encoding="utf-8")
    (tmp_path / "ION/03_registry/boots").mkdir(parents=True, exist_ok=True)
    (tmp_path / "ION/04_packages/kernel").mkdir(parents=True, exist_ok=True)
    authority = tmp_path / "ION/REPO_AUTHORITY.md"
    authority.parent.mkdir(parents=True, exist_ok=True)
    authority.write_text("authority\n", encoding="utf-8")

    status = build_ion_status(tmp_path)

    assert status["verdict"] == "ION_STATUS_READY"
    assert status["steward_queue_rejected_count"] == 1
    assert status["next_lawful_action"] == "repair_rejected_steward_integration"


def test_status_treats_later_integrated_steward_item_as_superseding_rejection(tmp_path):
    current = "ION/05_context/current"
    write_json(tmp_path, f"{current}/ACTIVE_CURSOR_HOOK_STATE.json", {"status": "projected_not_connected"})
    write_json(tmp_path, f"{current}/ACTIVE_WORK_PACKET.json", {"objective": "repaired steward return"})
    write_json(tmp_path, f"{current}/ACTIVE_ROLE_SPAWN_PLAN.json", {"role_spawn_plan": []})
    write_json(tmp_path, f"{current}/ACTIVE_CARRIER_TURN_PACKET.json", {"objective": "repaired steward return", "spawn_queue": []})
    write_json(tmp_path, f"{current}/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json", {"records": []})
    write_json(
        tmp_path,
        f"{current}/ACTIVE_STEWARD_INTEGRATION_QUEUE.json",
        {
            "items": [
                {"index": 1, "role": "steward", "status": "STEWARD_INTEGRATION_REJECTED"},
                {"index": 1, "role": "steward", "status": "STEWARD_INTEGRATED", "accepted": True},
            ]
        },
    )
    write_json(tmp_path, f"{current}/ACTIVE_OPERATOR_MESSAGE_QUEUE.json", {"items": []})
    write_json(tmp_path, f"{current}/ACTIVE_HUMAN_GATE_QUEUE.json", {"gates": []})
    write_json(
        tmp_path,
        f"{current}/V108_V72_MCP_DONOR_RECONCILIATION_AUDIT.json",
        {
            "reconciliation_verdict": "V72_MCP_DONOR_RECONCILIATION_PASS",
            "missing_donor_surface_count": 0,
            "forbidden_runtime_file_count": 0,
            "production_authority": False,
            "live_execution_authority": False,
        },
    )
    (tmp_path / "pyproject.toml").write_text("[project]\nname='mount-test'\n", encoding="utf-8")
    (tmp_path / "ION/03_registry/boots").mkdir(parents=True, exist_ok=True)
    (tmp_path / "ION/04_packages/kernel").mkdir(parents=True, exist_ok=True)
    authority = tmp_path / "ION/REPO_AUTHORITY.md"
    authority.parent.mkdir(parents=True, exist_ok=True)
    authority.write_text("authority\n", encoding="utf-8")

    status = build_ion_status(tmp_path)

    assert status["steward_queue_rejected_count"] == 0
    assert status["next_lawful_action"] == "continue_or_queue_new_work"


def test_status_does_not_count_completed_role_as_deferred(tmp_path):
    current = "ION/05_context/current"
    write_json(tmp_path, f"{current}/ACTIVE_CURSOR_HOOK_STATE.json", {"status": "projected_not_connected"})
    write_json(tmp_path, f"{current}/ACTIVE_WORK_PACKET.json", {"objective": "completed role projection"})
    write_json(
        tmp_path,
        f"{current}/ACTIVE_ROLE_SPAWN_PLAN.json",
        {
            "execution_bundle_materialized": True,
            "role_spawn_plan": [
                {"index": 1, "role": "steward", "spawn": False, "spawn_intent": True, "completion_status": "ALREADY_INTEGRATED"},
                {"index": 2, "role": "vizier", "spawn": True, "spawn_intent": True},
                {"index": 3, "role": "mason", "spawn": False, "spawn_intent": True, "spawn_deferral_reason": "deferred_by_spawn_row_limit"},
            ],
        },
    )
    write_json(
        tmp_path,
        f"{current}/ACTIVE_CARRIER_TURN_PACKET.json",
        {"objective": "completed role projection", "spawn_queue": [{"index": 2, "role": "vizier"}]},
    )
    write_json(tmp_path, f"{current}/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json", {"records": []})
    write_json(tmp_path, f"{current}/ACTIVE_STEWARD_INTEGRATION_QUEUE.json", {"items": []})
    write_json(tmp_path, f"{current}/ACTIVE_OPERATOR_MESSAGE_QUEUE.json", {"items": []})
    write_json(tmp_path, f"{current}/ACTIVE_HUMAN_GATE_QUEUE.json", {"gates": []})
    write_json(
        tmp_path,
        f"{current}/V108_V72_MCP_DONOR_RECONCILIATION_AUDIT.json",
        {
            "reconciliation_verdict": "V72_MCP_DONOR_RECONCILIATION_PASS",
            "missing_donor_surface_count": 0,
            "forbidden_runtime_file_count": 0,
            "production_authority": False,
            "live_execution_authority": False,
        },
    )
    (tmp_path / "pyproject.toml").write_text("[project]\nname='mount-test'\n", encoding="utf-8")
    (tmp_path / "ION/03_registry/boots").mkdir(parents=True, exist_ok=True)
    (tmp_path / "ION/04_packages/kernel").mkdir(parents=True, exist_ok=True)
    authority = tmp_path / "ION/REPO_AUTHORITY.md"
    authority.parent.mkdir(parents=True, exist_ok=True)
    authority.write_text("authority\n", encoding="utf-8")

    status = build_ion_status(tmp_path)

    assert status["completed_role_count"] == 1
    assert status["plan_spawn_count"] == 1
    assert status["deferred_spawn_count"] == 1
    assert status["next_lawful_action"] == "execute_spawn_rows_and_run_task_return_intake"
