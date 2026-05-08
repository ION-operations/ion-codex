from pathlib import Path

from kernel.ion_agent_context_dynamics import (
    build_agent_context_window_plan,
    build_front_door_team_plan,
    classify_message,
)


def test_classify_continue():
    assert classify_message("continue") == "continuation_signal"


def test_front_door_plan_keeps_cursor_parent_out_of_ion_roles(tmp_path: Path):
    plan = build_front_door_team_plan(tmp_path, operator_message="continue")
    assert plan["schema_id"] == "ion.front_door_team_plan.v1"
    assert plan["main_cursor_identity"]["is_ion_role"] is False
    assert "STEWARD" in plan["main_cursor_identity"]["must_not_claim_roles"]
    assert "which_agent_should_i_spawn" in plan["no_user_upkeep_law"]["forbidden_user_requests"]


def test_context_window_plan_writes_active_files(tmp_path: Path):
    current = tmp_path / "ION/05_context/current/agent_context_systems"
    current.mkdir(parents=True)
    (current / "STEWARD.context_system.md").write_text("# STEWARD\n", encoding="utf-8")
    plan = build_agent_context_window_plan(
        tmp_path,
        operator_message="continue with the workflow",
        roles=["steward", "relay", "persona_interface"],
        write=True,
    )
    assert plan["schema_id"] == "ion.agent_context_window_plan.v1"
    assert plan["operator_message_classification"] == "new_work_directive"
    assert (tmp_path / "ION/05_context/current/ACTIVE_AGENT_CONTEXT_WINDOW_PLAN.json").exists()
    assert (tmp_path / "ION/05_context/current/ACTIVE_FRONT_DOOR_TEAM_PLAN.json").exists()
    steward = next(item for item in plan["roles"] if item["role"] == "steward")
    assert steward["attention_lease"] in {"active", "warm"}
    assert steward["budget"]["estimated_tokens"] > 0
    assert "steward_integration_queue_only" in steward["drift_controls"]
