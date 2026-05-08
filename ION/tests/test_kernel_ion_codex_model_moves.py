from kernel.ion_codex_model_moves import (
    build_codex_model_move_plan,
    codex_exec_args_from_model_move,
    infer_codex_work_class,
    list_codex_model_profiles,
)


def test_model_profiles_mark_usage_limits_as_advisory():
    profiles = list_codex_model_profiles()

    assert profiles["verdict"] == "ION_CODEX_CLI_MODEL_MOVES_READY"
    assert profiles["usage_limits_authoritative"] is False
    assert profiles["profiles"]["gpt-5.3-codex-spark"]["usage_pool_authority"] == "operator_observed_pending_verification"
    assert profiles["profiles"]["gpt-5.5"]["reasoning_efforts_supported"] == ["low", "medium", "high", "xhigh"]


def test_conserve_main_bank_routes_low_risk_status_to_spark():
    move = build_codex_model_move_plan(
        lane_id="codex_general",
        objective="Read-only smoke status check.",
    )

    assert move["selected_model"] == "gpt-5.3-codex-spark"
    assert move["selected_reasoning_effort"] == "low"
    assert move["usage_limits_authoritative"] is False
    assert codex_exec_args_from_model_move(move) == ["-m", "gpt-5.3-codex-spark", "-c", "model_reasoning_effort=low"]


def test_model_move_escalates_authority_and_architecture_to_gpt55():
    steward = build_codex_model_move_plan(
        lane_id="ion_system",
        stage_id="steward_route",
        objective="Classify public URL and privacy policy authority.",
    )
    architecture = build_codex_model_move_plan(
        lane_id="codex_general",
        objective="Plan architecture and schema changes for the router.",
    )

    assert steward["selected_model"] == "gpt-5.5"
    assert steward["selected_reasoning_effort"] == "high"
    assert architecture["work_class"] == "architecture_design"
    assert architecture["selected_model"] == "gpt-5.5"


def test_normal_codex_implementation_uses_primary_codex_lane():
    move = build_codex_model_move_plan(
        lane_id="codex_general",
        objective="Implement a focused parser fix.",
    )

    assert infer_codex_work_class(lane_id="codex_general", objective="Implement a focused parser fix.") == "code_patch"
    assert move["selected_model"] == "gpt-5.3-codex"
    assert move["selected_reasoning_effort"] == "medium"
