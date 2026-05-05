from __future__ import annotations

import json
from pathlib import Path

from kernel.ion_carrier_tick import build_carrier_tick


def _write_json(root: Path, rel: str, value: dict) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _write_text(root: Path, rel: str, text: str = "surface\n") -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _seed_root(root: Path, *, work_caps: dict | None = None, profile_caps: dict | None = None) -> None:
    _write_text(root, "pyproject.toml", "[project]\nname = \"ion-test\"\n")
    _write_text(root, "ION/REPO_AUTHORITY.md", "# ION authority\n")
    (root / "ION/03_registry/boots").mkdir(parents=True, exist_ok=True)
    (root / "ION/04_packages/kernel").mkdir(parents=True, exist_ok=True)
    current = "ION/05_context/current"
    caps = {
        "can_read_files": True,
        "can_edit_files": True,
        "can_run_tests": True,
        "can_use_mcp": True,
        "can_spawn_carrier_slots": False,
        "production_authority": False,
        "live_execution_authority": False,
    }
    if work_caps:
        caps.update(work_caps)
    profile = {
        "can_read_files": True,
        "can_edit_files": True,
        "can_run_tests": True,
        "production_authority": False,
        "live_execution_authority": False,
    }
    if profile_caps:
        profile.update(profile_caps)

    _write_text(
        root,
        "ION/03_registry/codex_extension_carrier_profile.yaml",
        "\n".join(
            [
                "schema_id: ion.codex_extension_carrier_profile.v1",
                "carrier_id: CODEX_EXTENSION_CARRIER",
                "host_family: codex_extension",
                *[f"{key}: {str(value).lower() if isinstance(value, bool) else value}" for key, value in profile.items()],
                "",
            ]
        ),
    )
    _write_json(
        root,
        f"{current}/ACTIVE_WORK_PACKET.json",
        {
            "schema_id": "ion.active_work_packet.v1",
            "carrier": "codex_extension",
            "objective": "carrier tick test",
            "carrier_capabilities": caps,
            "production_authority": False,
            "live_execution_authority": False,
        },
    )
    _write_json(
        root,
        f"{current}/ACTIVE_CARRIER_ONBOARDING_PACKET.json",
        {
            "schema_id": "ion.carrier_onboarding_packet.v1",
            "carrier_id": "codex_extension",
            "onboarding_verdict": "ION_CARRIER_ONBOARDING_PACKET_READY",
            "production_authority": False,
            "live_execution_authority": False,
        },
    )
    _write_json(
        root,
        f"{current}/ACTIVE_CARRIER_TURN_PACKET.json",
        {
            "schema_id": "ion.carrier_turn_packet.v1",
            "carrier": "codex_extension",
            "objective": "carrier tick test",
            "spawn_queue": [],
            "workstream": "implementation",
            "production_authority": False,
            "live_execution_authority": False,
        },
    )
    _write_json(
        root,
        f"{current}/ACTIVE_ROLE_SPAWN_PLAN.json",
        {
            "schema_id": "ion.carrier_cycle_plan.v1",
            "carrier": "codex_extension",
            "objective": "carrier tick test",
            "active_spawn_count": 0,
            "deferred_spawn_count": 0,
            "execution_bundle_materialized": False,
            "role_spawn_plan": [],
            "production_authority": False,
            "live_execution_authority": False,
        },
    )
    _write_json(root, f"{current}/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json", {"records": []})
    _write_json(root, f"{current}/ACTIVE_STEWARD_INTEGRATION_QUEUE.json", {"items": []})
    _write_json(root, f"{current}/ACTIVE_OPERATOR_MESSAGE_QUEUE.json", {"items": []})
    _write_json(root, f"{current}/ACTIVE_HUMAN_GATE_QUEUE.json", {"gates": []})
    _write_json(root, f"{current}/ACTIVE_CURSOR_HOOK_STATE.json", {"status": "projected_not_connected"})
    _write_json(
        root,
        f"{current}/V108_V72_MCP_DONOR_RECONCILIATION_AUDIT.json",
        {"reconciliation_verdict": "V72_MCP_DONOR_RECONCILIATION_PASS"},
    )


def test_tick_returns_execute_context_package_for_spawn_true_row(tmp_path: Path) -> None:
    _seed_root(tmp_path)
    context_path = "ION/05_context/current/execution_cycles/test/01_STEWARD_CONTEXT_PACKAGE.md"
    _write_text(tmp_path, context_path, "# context package\n")
    _write_json(
        tmp_path,
        "ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json",
        {
            "schema_id": "ion.carrier_cycle_plan.v1",
            "carrier": "codex_extension",
            "objective": "carrier tick test",
            "active_spawn_count": 1,
            "deferred_spawn_count": 0,
            "execution_bundle_materialized": True,
            "role_spawn_plan": [
                {
                    "index": 1,
                    "role": "steward",
                    "spawn": True,
                    "context_package_path": context_path,
                    "context_load_receipt_path": "ION/05_context/current/execution_cycles/test/01_receipt.json",
                }
            ],
        },
    )

    tick = build_carrier_tick(tmp_path, carrier="codex_extension")

    assert tick["next_action"]["action"] == "EXECUTE_CONTEXT_PACKAGE"
    assert tick["next_action"]["path"] == context_path
    assert tick["next_action"]["role"] == "steward"


def test_tick_integrates_pending_steward_queue_before_reexecuting_active_row(tmp_path: Path) -> None:
    _seed_root(tmp_path)
    context_path = "ION/05_context/current/execution_cycles/test/01_STEWARD_CONTEXT_PACKAGE.md"
    _write_text(tmp_path, context_path, "# context package\n")
    _write_json(
        tmp_path,
        "ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json",
        {
            "schema_id": "ion.carrier_turn_packet.v1",
            "carrier": "codex_extension",
            "objective": "carrier tick test",
            "spawn_queue": [{"index": 1, "role": "steward"}],
            "workstream": "implementation",
            "production_authority": False,
            "live_execution_authority": False,
        },
    )
    _write_json(
        tmp_path,
        "ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json",
        {
            "schema_id": "ion.carrier_cycle_plan.v1",
            "carrier": "codex_extension",
            "objective": "carrier tick test",
            "active_spawn_count": 1,
            "deferred_spawn_count": 2,
            "execution_bundle_materialized": True,
            "role_spawn_plan": [
                {
                    "index": 1,
                    "role": "steward",
                    "spawn": True,
                    "context_package_path": context_path,
                    "context_load_receipt_path": "ION/05_context/current/execution_cycles/test/01_receipt.json",
                }
            ],
        },
    )
    _write_json(
        tmp_path,
        "ION/05_context/current/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json",
        {
            "schema_id": "ion.carrier_task_return_ledger.v1",
            "records": [{"index": 1, "role": "steward", "accepted": True}],
        },
    )
    _write_json(
        tmp_path,
        "ION/05_context/current/ACTIVE_STEWARD_INTEGRATION_QUEUE.json",
        {
            "schema_id": "ion.steward_integration_queue.v1",
            "items": [
                {
                    "index": 1,
                    "role": "steward",
                    "status": "PENDING_STEWARD_INTEGRATION",
                    "task_output_path": "ION/05_context/current/task_returns/worker.md",
                }
            ],
        },
    )

    tick = build_carrier_tick(tmp_path, carrier="codex_extension")

    assert tick["status_next_lawful_action"] == "spawn_steward_integration_from_accepted_queue"
    assert tick["next_action"]["action"] == "RUN_COMMAND"
    assert tick["next_action"]["reason"] == "accepted_task_return_requires_steward_integration_before_reexecuting_spawn_rows"
    assert "kernel.ion_steward_integrate" in tick["next_action"]["command_text"]
    assert "--integrate-queue" in tick["next_action"]["command_text"]


def test_tick_reexecutes_rejected_steward_context_with_template_action_requirement(tmp_path: Path) -> None:
    _seed_root(tmp_path)
    context_path = "ION/05_context/current/execution_cycles/test/01_STEWARD_CONTEXT_PACKAGE.md"
    _write_text(tmp_path, context_path, "# context package\n")
    _write_json(
        tmp_path,
        "ION/05_context/current/ACTIVE_STEWARD_INTEGRATION_QUEUE.json",
        {
            "schema_id": "ion.steward_integration_queue.v1",
            "items": [
                {
                    "index": 1,
                    "role": "steward",
                    "status": "STEWARD_INTEGRATION_REJECTED",
                    "context_package_path": context_path,
                    "context_load_receipt_path": "ION/05_context/current/execution_cycles/test/01_receipt.json",
                    "task_output_path": "ION/05_context/current/task_returns/bad.md",
                    "steward_receipt_path": "ION/05_context/current/steward_integrations/rejected.json",
                    "steward_gate_findings": ["missing_template_action_proof_heading"],
                }
            ],
        },
    )

    tick = build_carrier_tick(tmp_path, carrier="codex_extension")

    assert tick["status_next_lawful_action"] == "repair_rejected_steward_integration"
    assert tick["next_action"]["action"] == "EXECUTE_CONTEXT_PACKAGE"
    assert tick["next_action"]["reason"] == "repair_rejected_steward_integration_return_with_template_action_proof"
    assert tick["next_action"]["path"] == context_path
    assert tick["next_action"]["required_return_headings"] == ["### CONTEXT PROOF", "### TEMPLATE ACTION PROOF"]
    assert tick["next_action"]["steward_gate_findings"] == ["missing_template_action_proof_heading"]


def test_tick_does_not_reexecute_active_row_with_accepted_latest_return(tmp_path: Path) -> None:
    _seed_root(tmp_path)
    context_path = "ION/05_context/current/execution_cycles/test/01_STEWARD_CONTEXT_PACKAGE.md"
    _write_text(tmp_path, context_path, "# context package\n")
    _write_json(
        tmp_path,
        "ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json",
        {
            "schema_id": "ion.carrier_turn_packet.v1",
            "carrier": "codex_extension",
            "objective": "carrier tick test",
            "spawn_queue": [{"index": 1, "role": "steward"}],
            "workstream": "implementation",
            "production_authority": False,
            "live_execution_authority": False,
        },
    )
    _write_json(
        tmp_path,
        "ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json",
        {
            "schema_id": "ion.carrier_cycle_plan.v1",
            "carrier": "codex_extension",
            "objective": "carrier tick test",
            "active_spawn_count": 1,
            "deferred_spawn_count": 0,
            "execution_bundle_materialized": True,
            "role_spawn_plan": [
                {
                    "index": 1,
                    "role": "steward",
                    "spawn": True,
                    "context_package_path": context_path,
                    "context_load_receipt_path": "ION/05_context/current/execution_cycles/test/01_receipt.json",
                }
            ],
        },
    )
    _write_json(
        tmp_path,
        "ION/05_context/current/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json",
        {
            "schema_id": "ion.carrier_task_return_ledger.v1",
            "records": [{"index": 1, "role": "steward", "accepted": True}],
        },
    )

    tick = build_carrier_tick(tmp_path, carrier="codex_extension")

    assert tick["next_action"]["action"] == "NO_WORK"


def test_tick_materializes_next_packet_when_only_deferred_spawn_rows_exist(tmp_path: Path) -> None:
    _seed_root(tmp_path)
    _write_json(
        tmp_path,
        "ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json",
        {
            "schema_id": "ion.carrier_cycle_plan.v1",
            "carrier": "codex_extension",
            "objective": "carrier tick test",
            "active_spawn_count": 0,
            "deferred_spawn_count": 3,
            "execution_bundle_materialized": False,
            "role_spawn_plan": [
                {"index": 1, "role": "steward", "spawn": False, "spawn_intent": True},
                {"index": 2, "role": "vizier", "spawn": False, "spawn_intent": True},
                {"index": 3, "role": "mason", "spawn": False, "spawn_intent": True},
            ],
        },
    )

    tick = build_carrier_tick(tmp_path, carrier="codex_extension")

    assert tick["next_action"]["action"] == "RUN_COMMAND"
    assert tick["next_action"]["reason"] == "deferred_spawn_rows_require_context_package_materialization_or_advancement"
    assert "kernel.ion_carrier_continue" in tick["next_action"]["command_text"]
    assert "--max-spawn-rows 1" in tick["next_action"]["command_text"]


def test_tick_advances_deferred_rows_after_active_row_return_is_integrated(tmp_path: Path) -> None:
    _seed_root(tmp_path)
    context_path = "ION/05_context/current/execution_cycles/test/01_STEWARD_CONTEXT_PACKAGE.md"
    _write_text(tmp_path, context_path, "# context package\n")
    _write_json(
        tmp_path,
        "ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json",
        {
            "schema_id": "ion.carrier_turn_packet.v1",
            "carrier": "codex_extension",
            "objective": "carrier tick test",
            "spawn_queue": [{"index": 1, "role": "steward"}],
            "workstream": "implementation",
            "production_authority": False,
            "live_execution_authority": False,
        },
    )
    _write_json(
        tmp_path,
        "ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json",
        {
            "schema_id": "ion.carrier_cycle_plan.v1",
            "carrier": "codex_extension",
            "objective": "carrier tick test",
            "active_spawn_count": 1,
            "deferred_spawn_count": 2,
            "execution_bundle_materialized": True,
            "role_spawn_plan": [
                {
                    "index": 1,
                    "role": "steward",
                    "spawn": True,
                    "context_package_path": context_path,
                    "context_load_receipt_path": "ION/05_context/current/execution_cycles/test/01_receipt.json",
                },
                {"index": 2, "role": "vizier", "spawn": False, "spawn_intent": True, "spawn_deferral_reason": "deferred_by_spawn_row_limit"},
                {"index": 3, "role": "mason", "spawn": False, "spawn_intent": True, "spawn_deferral_reason": "deferred_by_spawn_row_limit"},
            ],
        },
    )
    _write_json(
        tmp_path,
        "ION/05_context/current/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json",
        {
            "schema_id": "ion.carrier_task_return_ledger.v1",
            "records": [{"index": 1, "role": "steward", "accepted": True}],
        },
    )
    _write_json(
        tmp_path,
        "ION/05_context/current/ACTIVE_STEWARD_INTEGRATION_QUEUE.json",
        {
            "schema_id": "ion.steward_integration_queue.v1",
            "items": [{"index": 1, "role": "steward", "status": "STEWARD_INTEGRATED", "accepted": True}],
        },
    )

    tick = build_carrier_tick(tmp_path, carrier="codex_extension")

    assert tick["next_action"]["action"] == "RUN_COMMAND"
    assert tick["next_action"]["reason"] == "deferred_spawn_rows_require_context_package_materialization_or_advancement"
    assert "kernel.ion_carrier_continue" in tick["next_action"]["command_text"]


def test_tick_waits_for_open_human_gate(tmp_path: Path) -> None:
    _seed_root(tmp_path)
    _write_json(
        tmp_path,
        "ION/05_context/current/ACTIVE_HUMAN_GATE_QUEUE.json",
        {
            "schema_id": "ion.human_gate_queue.v1",
            "gates": [
                {
                    "id": "hgate_test",
                    "status": "open",
                    "blocking": True,
                    "prompt": "Approve carrier action?",
                }
            ],
        },
    )

    tick = build_carrier_tick(tmp_path, carrier="codex_extension")

    assert tick["next_action"]["action"] == "WAIT_FOR_HUMAN_GATE"
    assert tick["next_action"]["gate_id"] == "hgate_test"


def test_tick_reports_capability_conflict_instead_of_guessing(tmp_path: Path) -> None:
    _seed_root(tmp_path, work_caps={"can_edit_files": False, "can_run_tests": False})

    tick = build_carrier_tick(tmp_path, carrier="codex_extension")

    assert tick["next_action"]["action"] == "CAPABILITY_CONFLICT"
    conflicts = {item["capability"] for item in tick["next_action"]["conflicts"]}
    assert {"can_edit_files", "can_run_tests"} <= conflicts


def test_tick_projects_correct_carrier_onboarding_when_generic_packet_belongs_to_other_carrier(tmp_path: Path) -> None:
    _seed_root(tmp_path)
    _write_json(
        tmp_path,
        "ION/05_context/current/ACTIVE_CARRIER_ONBOARDING_PACKET.json",
        {
            "schema_id": "ion.carrier_onboarding_packet.v1",
            "carrier_id": "chatgpt_browser",
            "onboarding_verdict": "ION_CARRIER_ONBOARDING_PACKET_READY",
            "production_authority": False,
            "live_execution_authority": False,
        },
    )

    tick = build_carrier_tick(tmp_path, carrier="codex_extension")

    assert "active_onboarding_packet_carrier_mismatch" not in tick["findings"]
    assert tick["active_carrier_onboarding_packet_source"] == "projected_for_carrier"
    assert tick["active_carrier_onboarding_packet_path"].endswith("ACTIVE_CARRIER_ONBOARDING_PACKET.codex_extension.json")


def test_tick_prefers_carrier_specific_onboarding_packet(tmp_path: Path) -> None:
    _seed_root(tmp_path)
    _write_json(
        tmp_path,
        "ION/05_context/current/ACTIVE_CARRIER_ONBOARDING_PACKET.json",
        {
            "schema_id": "ion.carrier_onboarding_packet.v1",
            "carrier_id": "chatgpt_browser",
            "onboarding_verdict": "ION_CARRIER_ONBOARDING_PACKET_READY",
        },
    )
    _write_json(
        tmp_path,
        "ION/05_context/current/ACTIVE_CARRIER_ONBOARDING_PACKET.codex_extension.json",
        {
            "schema_id": "ion.carrier_onboarding_packet.v1",
            "carrier_id": "codex_extension",
            "onboarding_verdict": "ION_CARRIER_ONBOARDING_PACKET_READY",
        },
    )

    tick = build_carrier_tick(tmp_path, carrier="codex_extension")

    assert "active_onboarding_packet_carrier_mismatch" not in tick["findings"]
    assert tick["active_carrier_onboarding_packet_source"] == "carrier_specific_file"
    assert tick["active_carrier_onboarding_packet_path"].endswith("ACTIVE_CARRIER_ONBOARDING_PACKET.codex_extension.json")


def test_tick_returns_no_work_when_no_active_or_deferred_work_exists(tmp_path: Path) -> None:
    _seed_root(tmp_path)

    tick = build_carrier_tick(tmp_path, carrier="codex_extension")

    assert tick["next_action"]["action"] == "NO_WORK"
    assert tick["next_action"]["reason"] == "no_active_spawn_rows_no_open_gates_no_pending_queue"
