import json
from pathlib import Path

from kernel.ion_carrier_continue import (
    _classification_for_forced_objective,
    _latest_completed_role_history,
    build_carrier_turn_packet,
    initialize_empty_return_state,
)
from kernel.ion_carrier_onboard import build_active_work_packet, onboard_carrier
from kernel.ion_cycle_runner import build_cycle_plan, validate_cycle_plan
from kernel.ion_operator_message_classifier import classify_operator_message


def test_forced_objective_refresh_overrides_status_like_classification():
    classification = classify_operator_message("V106 runtime state repair")

    forced = _classification_for_forced_objective(classification, forced=True)

    assert classification["classification"] == "status_request"
    assert forced["classification"] == "new_work_directive"
    assert forced["action"] == "record_operator_work_item_and_refresh_carrier"
    assert forced["mutates_runtime"] is True
    assert forced["forced_objective_refresh"] is True
    assert forced["original_classification"] == "status_request"


def test_unforced_classification_is_preserved():
    classification = classify_operator_message("status")

    preserved = _classification_for_forced_objective(classification, forced=False)

    assert preserved["classification"] == "status_request"
    assert preserved["mutates_runtime"] is False


def test_plan_only_zero_spawn_rows_requires_no_task_returns():
    packet = build_carrier_turn_packet(
        carrier="codex_extension",
        operator_message="V111 current-state truth",
        interpretation="NEW_OR_UPDATED_OBJECTIVE_REFRESH_ACTIVE_PACKET",
        onboard_result={"findings": []},
        plan={
            "objective": "V111 current-state truth",
            "workstream": "implementation",
            "role_spawn_plan": [
                {"index": 1, "role": "STEWARD", "spawn": True},
                {"index": 2, "role": "RELAY", "spawn": True},
            ],
        },
        plan_findings=[],
        operator_message_classification={"classification": "new_work_directive"},
        source_operator_queue_item=None,
        human_gates=[],
        mode="plan-only",
        max_spawn_rows=0,
    )

    assert packet["spawn_queue"] == []
    assert packet["return_intake_state"]["pending_count"] == 0
    assert packet["return_intake_state"]["status"] == "NO_TASK_RETURNS_REQUIRED"


def test_zero_spawn_row_limit_defers_context_bundle_materialization(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    execution_root = tmp_path / "execution_cycles" / "zero_spawn"

    plan = build_cycle_plan(
        repo,
        workstream="implementation",
        objective="V113 zero spawn materialization guard",
        carrier="codex_extension",
        spawn_row_limit=0,
        execution_root=execution_root,
        source_task="test:zero_spawn",
    )
    valid, findings = validate_cycle_plan(plan)

    assert valid, findings
    assert plan["active_spawn_count"] == 0
    assert plan["deferred_spawn_count"] >= 1
    assert plan["execution_bundle_materialized"] is False
    assert plan["trace_path"] is None
    assert plan["session_paths"] == []
    assert plan["handoff_paths"] == []
    assert not execution_root.exists()
    assert all(row["spawn"] is False for row in plan["role_spawn_plan"])
    assert all(row["context_package_path"] is None for row in plan["role_spawn_plan"])
    assert any(row["spawn_deferral_reason"] == "deferred_by_spawn_row_limit" for row in plan["role_spawn_plan"])


def test_spawned_context_package_requires_template_action_proof(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    execution_root = tmp_path / "execution_cycles" / "template_action_contract"

    plan = build_cycle_plan(
        repo,
        workstream="implementation",
        objective="V125 template-action return contract",
        carrier="codex_extension",
        spawn_row_limit=1,
        execution_root=execution_root,
        source_task="test:template_action_contract",
    )
    spawned = [row for row in plan["role_spawn_plan"] if row["spawn"] is True]
    assert spawned
    row = spawned[0]
    prompt = repo / row["context_package_path"]
    receipt = repo / row["context_load_receipt_path"]

    prompt_text = prompt.read_text(encoding="utf-8")
    receipt_text = receipt.read_text(encoding="utf-8")

    assert "### TEMPLATE ACTION PROOF" in prompt_text
    assert "kernel.ion_template_action_gate" in prompt_text
    assert "Approved `template_id` values" in prompt_text
    assert "ion.template.audit_observation.v1" in prompt_text
    assert "Do not use binding file paths" in prompt_text
    assert "TASK_OUTPUT_MUST_BEGIN_WITH_CONTEXT_PROOF_AND_INCLUDE_TEMPLATE_ACTION_PROOF" in receipt_text
    assert "template_action_allowed_template_ids" in receipt_text
    assert row["template_action_return_gate"] == "kernel.ion_template_action_gate"
    assert "### TEMPLATE ACTION PROOF" in row["return_contract"]


def test_completed_integrated_role_advances_next_spawn_row(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    execution_root = tmp_path / "execution_cycles" / "completed_steward"

    plan = build_cycle_plan(
        repo,
        workstream="implementation",
        objective="V120 connector loop",
        carrier="codex_extension",
        spawn_row_limit=1,
        execution_root=execution_root,
        source_task="test:completed_steward",
        completed_role_indexes={1},
        completed_role_evidence={
            1: {
                "role": "steward",
                "index": 1,
                "status": "STEWARD_INTEGRATED",
                "steward_receipt_path": "ION/05_context/current/steward_integrations/steward.json",
            }
        },
    )
    valid, findings = validate_cycle_plan(plan)

    assert valid, findings
    assert plan["completed_role_indexes"] == [1]
    assert plan["completed_role_count"] == 1
    assert plan["active_spawn_count"] == 1
    assert plan["deferred_spawn_count"] == 1
    rows = plan["role_spawn_plan"]
    assert rows[0]["role"] == "steward"
    assert rows[0]["spawn"] is False
    assert rows[0]["completion_status"] == "ALREADY_INTEGRATED"
    assert rows[0]["authority"] == "ALREADY_INTEGRATED"
    assert rows[1]["role"] == "vizier"
    assert rows[1]["spawn"] is True
    assert rows[1]["context_package_path"].endswith("02_vizier_cursor_task_prompt.md")
    assert rows[2]["role"] == "mason"
    assert rows[2]["spawn"] is False
    assert rows[2]["spawn_deferral_reason"] == "deferred_by_spawn_row_limit"


def test_completed_history_extraction_requires_steward_integration():
    history = _latest_completed_role_history(
        steward_queue={
            "items": [
                {"index": 1, "role": "steward", "status": "PENDING_STEWARD_INTEGRATION", "accepted": True},
                {
                    "index": 1,
                    "role": "steward",
                    "status": "STEWARD_INTEGRATED",
                    "accepted": True,
                    "steward_receipt_path": "ION/05_context/current/steward_integrations/steward.json",
                },
            ]
        },
        ledger={"records": [{"index": 1, "role": "steward", "accepted": True, "task_output_path": "out.md"}]},
    )

    assert history["completed_role_indexes"] == {1}
    assert history["completed_role_evidence"][1]["status"] == "STEWARD_INTEGRATED"
    assert history["completed_role_evidence"][1]["task_output_path"] == "out.md"
    assert history["completed_steward_items"][0]["steward_receipt_path"].endswith("steward.json")


def test_completed_history_carries_forward_completed_items_and_records():
    history = _latest_completed_role_history(
        steward_queue={
            "items": [
                {"index": 2, "role": "vizier", "status": "STEWARD_INTEGRATED", "accepted": True},
            ],
            "completed_items": [
                {"index": 1, "role": "steward", "status": "STEWARD_INTEGRATED", "accepted": True},
            ],
        },
        ledger={
            "records": [{"index": 2, "role": "vizier", "accepted": True, "task_output_path": "vizier.md"}],
            "completed_records": [{"index": 1, "role": "steward", "accepted": True, "task_output_path": "steward.md"}],
        },
    )

    assert history["completed_role_indexes"] == {1, 2}
    assert history["completed_role_evidence"][1]["task_output_path"] == "steward.md"
    assert history["completed_role_evidence"][2]["task_output_path"] == "vizier.md"


def test_completed_history_can_recover_from_historical_steward_receipts(tmp_path):
    receipts = tmp_path / "ION/05_context/current/steward_integrations"
    receipts.mkdir(parents=True)
    (receipts / "queue_01_steward_current_steward_integration.json").write_text(
        json.dumps(
            {
                "accepted": True,
                "created_at": "2026-05-04T04:45:51+00:00",
                "decision": "INTEGRATED_AS_ACCEPTED_STATE_DELTA",
                "role": "steward",
                "index": 1,
                "receipt_id": "queue_01_steward_current_steward_integration",
                "task_output_path": "ION/05_context/current/task_returns/steward.md",
                "task_output_sha256": "abc",
                "gate": {"template_id": "ion.template.audit_observation.v1", "action_id": "steward.review"},
            }
        ),
        encoding="utf-8",
    )

    history = _latest_completed_role_history(steward_queue={"items": []}, ledger={"records": []}, shell_root=tmp_path)

    assert history["completed_role_indexes"] == {1}
    assert history["completed_role_evidence"][1]["role"] == "steward"
    assert history["completed_role_evidence"][1]["steward_receipt_path"].endswith("queue_01_steward_current_steward_integration.json")


def test_completed_history_dedupes_to_latest_receipt_per_role_index(tmp_path):
    receipts = tmp_path / "ION/05_context/current/steward_integrations"
    receipts.mkdir(parents=True)
    receipt_rows = [
        {
            "path": "queue_01_steward_old_steward_integration.json",
            "created_at": "2026-05-04T04:01:00+00:00",
            "role": "steward",
            "index": 1,
            "receipt_id": "old_steward",
            "task_output_path": "old_steward.md",
        },
        {
            "path": "queue_01_steward_current_steward_integration.json",
            "created_at": "2026-05-04T05:01:00+00:00",
            "role": "steward",
            "index": 1,
            "receipt_id": "current_steward",
            "task_output_path": "current_steward.md",
        },
        {
            "path": "queue_02_relay_old_steward_integration.json",
            "created_at": "2026-05-04T04:02:00+00:00",
            "role": "relay",
            "index": 2,
            "receipt_id": "old_relay",
            "task_output_path": "old_relay.md",
        },
        {
            "path": "queue_02_vizier_current_steward_integration.json",
            "created_at": "2026-05-04T05:02:00+00:00",
            "role": "vizier",
            "index": 2,
            "receipt_id": "current_vizier",
            "task_output_path": "current_vizier.md",
        },
    ]
    for row in receipt_rows:
        payload = {
            "accepted": True,
            "created_at": row["created_at"],
            "decision": "INTEGRATED_AS_ACCEPTED_STATE_DELTA",
            "role": row["role"],
            "index": row["index"],
            "receipt_id": row["receipt_id"],
            "task_output_path": row["task_output_path"],
            "task_output_sha256": row["receipt_id"],
            "gate": {"template_id": "ion.template.audit_observation.v1", "action_id": f"{row['role']}.review"},
        }
        (receipts / row["path"]).write_text(json.dumps(payload), encoding="utf-8")

    history = _latest_completed_role_history(steward_queue={"items": []}, ledger={"records": []}, shell_root=tmp_path)

    assert history["completed_role_indexes"] == {1, 2}
    assert len(history["completed_steward_items"]) == 2
    assert history["completed_role_evidence"][1]["role"] == "steward"
    assert history["completed_role_evidence"][1]["task_output_path"] == "current_steward.md"
    assert history["completed_role_evidence"][2]["role"] == "vizier"
    assert history["completed_role_evidence"][2]["task_output_path"] == "current_vizier.md"


def test_historical_receipt_recovery_is_scoped_to_execution_bundle(tmp_path):
    receipts = tmp_path / "ION/05_context/current/steward_integrations"
    receipts.mkdir(parents=True)
    current_bundle = "ION/05_context/current/execution_cycles/current_objective"
    old_bundle = "ION/05_context/current/execution_cycles/old_objective"
    rows = [
        ("queue_01_steward_current_steward_integration.json", "steward", 1, current_bundle),
        ("queue_02_vizier_old_steward_integration.json", "vizier", 2, old_bundle),
        ("queue_03_mason_old_steward_integration.json", "mason", 3, old_bundle),
    ]
    for filename, role, index, bundle in rows:
        payload = {
            "accepted": True,
            "created_at": f"2026-05-04T05:0{index}:00+00:00",
            "decision": "INTEGRATED_AS_ACCEPTED_STATE_DELTA",
            "role": role,
            "index": index,
            "receipt_id": filename.removesuffix(".json"),
            "task_output_path": f"ION/05_context/current/task_returns/{role}.md",
            "task_output_sha256": role,
            "gate": {
                "template_id": "ion.template.audit_observation.v1",
                "action_id": f"{role}.review",
                "touched_paths": [f"{bundle}/0{index}_{role}_cursor_task_prompt.md"],
            },
        }
        (receipts / filename).write_text(json.dumps(payload), encoding="utf-8")

    history = _latest_completed_role_history(
        steward_queue={"items": []},
        ledger={"records": []},
        shell_root=tmp_path,
        execution_bundle_root=current_bundle,
    )

    assert history["completed_role_indexes"] == {1}
    assert history["completed_role_evidence"][1]["role"] == "steward"
    assert 2 not in history["completed_role_evidence"]
    assert 3 not in history["completed_role_evidence"]


def test_completed_queue_history_is_scoped_to_execution_bundle():
    current_bundle = "ION/05_context/current/execution_cycles/current_objective"
    old_bundle = "ION/05_context/current/execution_cycles/old_objective"
    history = _latest_completed_role_history(
        steward_queue={
            "completed_items": [
                {
                    "index": 1,
                    "role": "steward",
                    "status": "STEWARD_INTEGRATED",
                    "accepted": True,
                    "touched_paths": [f"{current_bundle}/01_steward_cursor_task_prompt.md"],
                },
                {
                    "index": 2,
                    "role": "vizier",
                    "status": "STEWARD_INTEGRATED",
                    "accepted": True,
                    "touched_paths": [f"{old_bundle}/02_vizier_cursor_task_prompt.md"],
                },
            ],
        },
        ledger={
            "completed_records": [
                {
                    "index": 1,
                    "role": "steward",
                    "accepted": True,
                    "task_output_path": "steward.md",
                    "touched_paths": [f"{current_bundle}/01_steward_cursor_task_prompt.md"],
                },
                {
                    "index": 2,
                    "role": "vizier",
                    "accepted": True,
                    "task_output_path": "vizier.md",
                    "touched_paths": [f"{old_bundle}/02_vizier_cursor_task_prompt.md"],
                },
            ],
        },
        execution_bundle_root=current_bundle,
    )

    assert history["completed_role_indexes"] == {1}
    assert history["completed_records"] == [
        {
            "index": 1,
            "role": "steward",
            "accepted": True,
            "task_output_path": "steward.md",
            "touched_paths": [f"{current_bundle}/01_steward_cursor_task_prompt.md"],
        }
    ]
    assert history["completed_steward_items"][0]["role"] == "steward"


def test_completed_history_uses_stable_objective_slug_across_regenerated_bundles():
    old_timestamped_bundle = (
        "ION/05_context/current/execution_cycles/"
        "2026-05-04T053817Z0000_carrier_continue_v120_cloudflare_tunnel_chatgpt_browser_connector_deployment_path"
    )
    new_timestamped_bundle = (
        "ION/05_context/current/execution_cycles/"
        "2026-05-04T054514Z0000_carrier_continue_v120_cloudflare_tunnel_chatgpt_browser_connector_deployment_path"
    )
    unrelated_bundle = (
        "ION/05_context/current/execution_cycles/"
        "2026-05-04T050331Z0000_carrier_continue_v120_chatgpt_browser_mcp_connector_and_correct_carrier_onboarding"
    )
    history = _latest_completed_role_history(
        steward_queue={
            "completed_items": [
                {
                    "index": 1,
                    "role": "steward",
                    "status": "STEWARD_INTEGRATED",
                    "accepted": True,
                    "touched_paths": [f"{old_timestamped_bundle}/01_steward_cursor_task_prompt.md"],
                },
                {
                    "index": 2,
                    "role": "vizier",
                    "status": "STEWARD_INTEGRATED",
                    "accepted": True,
                    "touched_paths": [f"{unrelated_bundle}/02_vizier_cursor_task_prompt.md"],
                },
            ],
        },
        ledger={},
        execution_bundle_root=new_timestamped_bundle,
    )

    assert history["completed_role_indexes"] == {1}
    assert history["completed_role_evidence"][1]["role"] == "steward"
    assert 2 not in history["completed_role_evidence"]


def test_multiple_completed_roles_advance_to_mason(tmp_path):
    repo = Path(__file__).resolve().parents[2]
    execution_root = tmp_path / "execution_cycles" / "completed_steward_vizier"

    plan = build_cycle_plan(
        repo,
        workstream="implementation",
        objective="V120 connector loop",
        carrier="codex_extension",
        spawn_row_limit=1,
        execution_root=execution_root,
        source_task="test:completed_steward_vizier",
        completed_role_indexes={1, 2},
    )
    valid, findings = validate_cycle_plan(plan)

    assert valid, findings
    rows = plan["role_spawn_plan"]
    assert plan["completed_role_indexes"] == [1, 2]
    assert rows[0]["role"] == "steward"
    assert rows[0]["completion_status"] == "ALREADY_INTEGRATED"
    assert rows[1]["role"] == "vizier"
    assert rows[1]["completion_status"] == "ALREADY_INTEGRATED"
    assert rows[2]["role"] == "mason"
    assert rows[2]["spawn"] is True
    assert rows[2]["context_package_path"].endswith("03_mason_cursor_task_prompt.md")


def test_return_state_preserves_completed_history_outside_active_records(tmp_path):
    plan = {"execution_bundle_root": "ION/05_context/current/execution_cycles/current"}

    initialize_empty_return_state(
        tmp_path,
        plan,
        completed_records=[{"index": 1, "role": "steward", "accepted": True}],
        completed_steward_items=[{"index": 1, "role": "steward", "status": "STEWARD_INTEGRATED"}],
    )

    ledger = (tmp_path / "ION/05_context/current/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json").read_text(encoding="utf-8")
    queue = (tmp_path / "ION/05_context/current/ACTIVE_STEWARD_INTEGRATION_QUEUE.json").read_text(encoding="utf-8")
    assert '"records": []' in ledger
    assert '"completed_records"' in ledger
    assert '"completed_items"' in queue
    assert '"items": []' in queue


def test_codex_extension_active_work_packet_is_edit_and_test_capable():
    repo = Path(__file__).resolve().parents[2]

    packet = build_active_work_packet(
        repo,
        carrier="codex_extension",
        objective="V125 carrier capability reconciliation",
    )

    assert packet["carrier_capabilities"]["can_edit_files"] is True
    assert packet["carrier_capabilities"]["can_run_tests"] is True


def test_onboard_carrier_loads_codex_extension_registry_capabilities(tmp_path):
    (tmp_path / "pyproject.toml").write_text("[project]\nname = \"ion-test\"\n", encoding="utf-8")
    authority = tmp_path / "ION/REPO_AUTHORITY.md"
    authority.parent.mkdir(parents=True, exist_ok=True)
    authority.write_text("# authority\n", encoding="utf-8")
    (tmp_path / "ION/03_registry/boots").mkdir(parents=True, exist_ok=True)
    (tmp_path / "ION/04_packages/kernel").mkdir(parents=True, exist_ok=True)
    profile = tmp_path / "ION/03_registry/codex_extension_carrier_profile.yaml"
    profile.write_text(
        "carrier_id: CODEX_EXTENSION_CARRIER\n"
        "can_read_files: true\n"
        "can_edit_files: true\n"
        "can_run_tests: true\n"
        "can_use_mcp: true\n",
        encoding="utf-8",
    )

    result = onboard_carrier(
        tmp_path,
        carrier="codex_extension",
        objective="V125 registry capability load",
        force=True,
    )

    assert result["valid"] is True
    assert result["packet"]["carrier_capabilities"]["can_edit_files"] is True
    assert result["packet"]["carrier_capabilities"]["can_run_tests"] is True
