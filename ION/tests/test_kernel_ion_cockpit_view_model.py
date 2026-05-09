import json
from pathlib import Path

from kernel.ion_cockpit_view_model import build_cockpit_view_model, write_cockpit_view_model


def write_json(root: Path, rel: str, payload: dict):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def seed_runtime(root: Path):
    (root / "pyproject.toml").write_text("[project]\nname = \"ion-cockpit-test\"\n", encoding="utf-8")
    (root / "ION/REPO_AUTHORITY.md").parent.mkdir(parents=True, exist_ok=True)
    (root / "ION/REPO_AUTHORITY.md").write_text("# authority\n", encoding="utf-8")
    current = "ION/05_context/current"
    write_json(root, f"{current}/ACTIVE_CURSOR_HOOK_STATE.json", {"schema_id": "ion.cursor_hook_state.v1", "status": "ready"})
    write_json(root, f"{current}/ACTIVE_WORK_PACKET.json", {"carrier": "cursor", "objective": "test cockpit"})
    write_json(root, f"{current}/ACTIVE_ROLE_SPAWN_PLAN.json", {
        "role_spawn_plan": [
            {"index": 1, "role": "STEWARD", "spawn": True, "context_package_path": "pkg/steward.md", "context_load_receipt_path": "pkg/steward_receipt.json"},
            {"index": 2, "role": "MASON", "spawn": False, "context_package_path": "pkg/mason.md"},
        ]
    })
    write_json(root, f"{current}/ACTIVE_CARRIER_TURN_PACKET.json", {"carrier": "cursor", "objective": "test cockpit", "blocked_by_findings": False})
    write_json(root, f"{current}/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json", {"records": [{"role": "STEWARD", "index": 1, "decision": "accepted", "task_output_path": "returns/steward.md"}]})
    write_json(root, f"{current}/ACTIVE_STEWARD_INTEGRATION_QUEUE.json", {"items": [{"role": "STEWARD", "path": "returns/steward.md"}]})
    write_json(root, f"{current}/ACTIVE_OPERATOR_MESSAGE_QUEUE.json", {"items": [{"id": "op1", "text": "continue", "status": "pending"}]})
    write_json(root, f"{current}/ACTIVE_HUMAN_GATE_QUEUE.json", {"gates": []})
    write_json(root, f"{current}/ACTIVE_FRONT_DOOR_PROOF_TRACE.json", {"schema_id": "ion.front_door_proof_trace.v1", "proof_complete": True, "verdict": "ION_FRONT_DOOR_PROOF_TRACE_READY"})
    write_json(root, f"{current}/ACTIVE_LANE_TIMELINE_VIEW_MODEL.json", {"schema_id": "ion.lane_timeline_view_model.v1", "events": []})
    write_json(root, f"{current}/ACTIVE_RECEIPT_HYDRATION_VIEW_MODEL.json", {"schema_id": "ion.receipt_hydration_view_model.v1", "records": []})
    write_json(root, f"{current}/ACTIVE_RUNTIME_DEBUG_OVERLAY.json", {"schema_id": "ion.runtime_debug_overlay.v1", "status": "degraded"})
    write_json(root, f"{current}/SAFE_FULL_PROJECT_PACKAGE_RESULT_V110.json", {
        "schema_id": "ion.safe_full_project_package_result.v1",
        "accepted": True,
        "zip_root_audit": {"verdict": "ZIP_ROOT_CONFIRMED", "archive_root_mode": "CANONICAL_ARCHIVE_ROOT"},
        "preservation_report": {"packaging_verdict": "PASS", "removed_files": 0, "protected_removed_files": 0, "unexpected_removed_files": 0},
    })
    write_json(root, f"{current}/V108_V72_MCP_DONOR_RECONCILIATION_AUDIT.json", {
        "schema_id": "ion.v72_mcp_donor_reconciliation_audit.v1",
        "reconciliation_verdict": "V72_MCP_DONOR_RECONCILIATION_PASS",
        "restored_donor_surface_count": 38,
        "missing_donor_surface_count": 0,
        "forbidden_runtime_file_count": 0,
        "production_authority": False,
        "live_execution_authority": False,
    })


def test_build_cockpit_view_model_summarizes_v88_runtime(tmp_path):
    seed_runtime(tmp_path)
    model = build_cockpit_view_model(tmp_path)
    assert model["schema_id"] == "ion.cockpit_view_model.v1"
    assert model["runtime"]["status"] == "ready"
    assert model["top_bar"]["objective"] == "test cockpit"
    assert model["top_bar"]["spawn_count"] == 1
    assert model["top_bar"]["plan_spawn_count"] == 1
    assert model["top_bar"]["deferred_spawn_count"] == 0
    assert model["top_bar"]["spawn_rows_total"] == 2
    assert model["top_bar"]["return_counts"]["accepted"] == 1
    assert model["top_bar"]["operator_queue_pending"] == 1
    assert model["top_bar"]["sandbox_return_count"] == 0
    assert model["top_bar"]["local_service_count"] == 6
    assert model["local_services"]["schema_id"] == "ion.local_service_status.v1"
    assert model["local_services"]["install_authority"] is False
    assert model["top_bar"]["gate_count"] == 0
    assert model["agents"]["spawn_rows"][0]["role"] == "STEWARD"
    assert model["agents"]["spawn_rows"][0]["return_recorded"] is True
    assert model["agents"]["returns"][0]["authority_class"] == "ACCEPTED_TASK_RETURN"
    assert model["front_door_proof_trace"]["schema_id"] == "ion.front_door_proof_trace.v1"
    assert model["lane_timeline"]["schema_id"] == "ion.lane_timeline_view_model.v1"
    assert model["receipt_hydration"]["schema_id"] == "ion.receipt_hydration_view_model.v1"
    assert model["runtime_debug_overlay"]["schema_id"] == "ion.runtime_debug_overlay.v1"
    assert model["safe_full_project_package"]["zip_root_audit"]["verdict"] == "ZIP_ROOT_CONFIRMED"
    assert model["v72_mcp_donor_reconciliation"]["reconciliation_verdict"] == "V72_MCP_DONOR_RECONCILIATION_PASS"
    assert any(event["source"] == "safe_full_project_package" for event in model["timeline"])
    assert any(event["source"] == "v72_mcp_donor_reconciliation" for event in model["timeline"])


def test_human_gate_blocks_cockpit_runtime(tmp_path):
    seed_runtime(tmp_path)
    write_json(tmp_path, "ION/05_context/current/ACTIVE_HUMAN_GATE_QUEUE.json", {"gates": [{"id": "gate1", "status": "open", "reason": "operator approval"}]})
    model = build_cockpit_view_model(tmp_path)
    assert model["runtime"]["status"] == "blocked"
    assert model["top_bar"]["gate_count"] == 1


def test_cockpit_counts_boolean_accepted_task_returns(tmp_path):
    seed_runtime(tmp_path)
    write_json(tmp_path, "ION/05_context/current/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json", {
        "records": [
            {"role": "STEWARD", "index": 1, "accepted": True, "task_output_path": "returns/steward.md"},
            {"role": "RELAY", "index": 2, "accepted": False, "task_output_path": "returns/relay.md"},
        ]
    })

    model = build_cockpit_view_model(tmp_path)

    assert model["top_bar"]["return_counts"]["accepted"] == 1
    assert model["top_bar"]["return_counts"]["rejected"] == 1
    assert model["top_bar"]["return_counts"]["pending"] == 0
    assert model["agents"]["returns"][0]["authority_class"] == "ACCEPTED_TASK_RETURN"
    assert model["agents"]["returns"][1]["authority_class"] == "REJECTED_TASK_RETURN"


def test_cockpit_spawn_count_uses_active_turn_spawn_queue_when_present(tmp_path):
    seed_runtime(tmp_path)
    write_json(tmp_path, "ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json", {
        "execution_bundle_materialized": False,
        "role_spawn_plan": [
            {"index": 1, "role": "STEWARD", "spawn_intent": True, "spawn": False, "spawn_deferral_reason": "deferred_by_spawn_row_limit"},
            {"index": 2, "role": "MASON", "spawn_intent": True, "spawn": False, "spawn_deferral_reason": "deferred_by_spawn_row_limit"},
        ],
    })
    write_json(tmp_path, "ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json", {
        "carrier": "cursor",
        "objective": "plan only",
        "blocked_by_findings": False,
        "spawn_row_limit": 0,
        "spawn_queue": [],
    })

    model = build_cockpit_view_model(tmp_path)

    assert model["top_bar"]["spawn_count"] == 0
    assert model["top_bar"]["plan_spawn_count"] == 0
    assert model["top_bar"]["deferred_spawn_count"] == 2
    assert model["top_bar"]["spawn_rows_total"] == 2
    assert model["top_bar"]["execution_bundle_materialized"] is False


def test_write_cockpit_view_model(tmp_path):
    seed_runtime(tmp_path)
    model = write_cockpit_view_model(tmp_path)
    out = tmp_path / "ION/05_context/current/ACTIVE_COCKPIT_VIEW_MODEL.json"
    assert out.exists()
    loaded = json.loads(out.read_text())
    assert loaded["schema_id"] == model["schema_id"]


def test_cockpit_projects_chatgpt_browser_callsign(tmp_path):
    seed_runtime(tmp_path)
    (tmp_path / "ION/03_registry").mkdir(parents=True, exist_ok=True)
    (tmp_path / "ION/03_registry/chatgpt_browser_carrier_profile.yaml").write_text(
        "\n".join([
            "carrier_id: CHATGPT_BROWSER_CARRIER",
            "project_facing_callsign: Sev",
            "callsign_authority: carrier_continuity_label_only_not_ion_authority",
            "callsign_decision_receipt: ION/05_context/current/chatgpt_connector/decisions/decision.json",
            "",
        ]),
        encoding="utf-8",
    )
    write_json(tmp_path, "ION/05_context/current/CHATGPT_BROWSER_MCP_CONNECTOR_CONTRACT_V120.json", {
        "allowed_tools": ["ion_status", "ion_tool_manifest"],
        "verdict": "ION_CHATGPT_BROWSER_MCP_CONNECTOR_CONTRACT_READY",
    })

    model = build_cockpit_view_model(tmp_path)

    summary = model["chatgpt_browser_mcp"]
    assert summary["carrier_id"] == "CHATGPT_BROWSER_CARRIER"
    assert summary["project_facing_callsign"] == "Sev"
    assert summary["callsign_authority"] == "carrier_continuity_label_only_not_ion_authority"
    assert summary["codex_queue_runner"]["schema_id"] == "ion.codex_queue_runner.v1"
    assert summary["codex_queue_runner"]["reconciliation"]["write"] is False


def test_cockpit_projects_chatgpt_sandbox_returns(tmp_path):
    seed_runtime(tmp_path)
    return_root = tmp_path / "ION/05_context/inbox/chatgpt_sandbox_returns/sev-20260505-041500-chatops-ui-return"
    return_root.mkdir(parents=True)
    (return_root / "SANDBOX_RETURN_MANIFEST.json").write_text(
        json.dumps(
            {
                "schema_id": "ion.chatgpt_sandbox_return.v1",
                "return_id": "sev-20260505-041500-chatops-ui-return",
                "changed_paths": ["ION/09_integrations/browser_extension/ion_chatops_bridge/README.md"],
            }
        ),
        encoding="utf-8",
    )

    model = build_cockpit_view_model(tmp_path)

    assert model["top_bar"]["sandbox_return_count"] == 1
    assert model["chatgpt_sandbox_returns"]["return_count"] == 1
    assert model["chatgpt_sandbox_returns"]["direct_apply_authority"] is False
