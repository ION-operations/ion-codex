import subprocess
from pathlib import Path

from kernel.ion_codex_chat_response_carrier import (
    ENABLED_ENV,
    build_chat_response_carrier_status,
    build_chat_response_prompt,
    prepare_codex_chat_response_run,
    run_codex_chat_response_carrier,
)


def _engine_turn() -> dict:
    return {
        "schema_id": "ion.codex_chat_engine_turn.v1",
        "response_mode": "answer",
        "selected_skill": {"skill_id": "codex-chat-answer", "display_name": "Codex Chat Answer"},
        "skill_activation": {"skill_id": "codex-chat-answer", "display_name": "Codex Chat Answer"},
        "native_lenses": [
            {
                "lens_id": "persona",
                "display_name": "Persona",
                "role_id": "role.persona_interface",
                "purpose": "User-facing clarity.",
            },
            {
                "lens_id": "context_cartographer",
                "display_name": "Context Cartographer",
                "role_id": "role.context_cartographer",
                "purpose": "Context mount.",
            },
        ],
        "model_move": {
            "selected_model": "gpt-5.5",
            "selected_reasoning_effort": "medium",
            "work_class": "user_facing_answer",
            "routing_posture": "conserve_main_bank",
        },
        "carrier_strategy": {"mode": "gpt_5_5_codex_chat_response_contract", "request_kind": "codex_chat_response"},
        "context_mount": {
            "context_refs": [
                "ION/05_context/current/codex_solo/CAPSULE.md",
                "ION/05_context/current/codex_solo/MINI.md",
            ],
        },
    }


def _solo_context() -> dict:
    return {
        "ok": True,
        "capsule": {
            "recent_rows": [
                {"id": "C-021", "status": "IMPLEMENTED", "summary": "Chat engine implemented."},
                {"id": "C-022", "status": "PLANNED", "summary": "Response carrier planned."},
            ],
        },
        "mini": {
            "text": "CODEX SOLO MINI INDEX\nLAST_RECEIPT: Response carrier planned.\nNEXT: Implement carrier.",
        },
        "context_packages": {
            "selected_by_default": ["minimum_working_capsule", "mission_active_package"],
            "packages": [
                {
                    "package_id": "minimum_working_capsule",
                    "context_type": "active_short_horizon",
                    "load_policy": "always_inline_first",
                    "path_refs": ["ION/05_context/current/codex_solo/CAPSULE.md"],
                },
                {
                    "package_id": "mission_active_package",
                    "context_type": "current_objective",
                    "load_policy": "injected_per_queue_or_chat_turn",
                    "path_refs": ["ION/05_context/current/codex_solo/HOT_CONTEXT.md"],
                },
            ],
        },
    }


def test_carrier_status_is_disabled_until_env_enabled(tmp_path: Path):
    disabled = build_chat_response_carrier_status(tmp_path, env={})
    enabled = build_chat_response_carrier_status(tmp_path, env={ENABLED_ENV: "1"})

    assert disabled["verdict"] == "ION_CODEX_CHAT_RESPONSE_CARRIER_DISABLED"
    assert disabled["enabled"] is False
    assert disabled["fallback_when_disabled"] == "local_chat_engine_response_contract"
    assert enabled["verdict"] == "ION_CODEX_CHAT_RESPONSE_CARRIER_READY"
    assert enabled["enabled"] is True
    assert enabled["sandbox"] == "workspace-write"
    assert enabled["ephemeral"] is True
    assert enabled["response_only_no_write_policy"] is True
    assert enabled["worktree_drift_detection"] is True
    assert enabled["direct_provider_api"] is False


def test_prompt_mounts_capsule_and_hides_internal_reasoning(tmp_path: Path):
    hot_context = tmp_path / "ION/05_context/current/codex_solo/HOT_CONTEXT.md"
    hot_context.parent.mkdir(parents=True, exist_ok=True)
    hot_context.write_text("# hot context\nCurrent mission: improve chat response quality.\n", encoding="utf-8")

    prompt = build_chat_response_prompt(
        tmp_path,
        operator_message="What is next?",
        chat_engine_turn=_engine_turn(),
        codex_solo_context=_solo_context(),
    )

    assert str(tmp_path) in prompt
    assert "Chat engine implemented." in prompt
    assert "CODEX SOLO MINI INDEX" in prompt
    assert "HOT CONTEXT EXCERPT" in prompt
    assert "Current mission: improve chat response quality." in prompt
    assert "CONTEXT PACKAGE SELECTOR" in prompt
    assert "minimum_working_capsule [selected" in prompt
    assert "Do not expose hidden chain of thought." in prompt
    assert "Do not edit files." in prompt
    assert "What is next?" in prompt


def test_prepare_run_uses_workspace_write_ephemeral_codex_exec(tmp_path: Path):
    prepared = prepare_codex_chat_response_run(
        tmp_path,
        operator_message="Summarize status.",
        chat_engine_turn=_engine_turn(),
        codex_solo_context=_solo_context(),
        env={ENABLED_ENV: "1"},
    )
    run = prepared["run"]
    command = run["codex_command"]

    assert prepared["ok"] is True
    assert command[:2] == ["codex", "exec"]
    assert "-m" in command
    assert "gpt-5.5" in command
    assert "--sandbox" in command
    assert "workspace-write" in command
    assert "--ephemeral" in command
    assert "--output-last-message" in command
    assert "--json" in command
    assert (tmp_path / run["prompt_path"]).exists()
    assert (tmp_path / run["run_packet_path"]).exists()


def test_fake_response_override_records_response_artifact(tmp_path: Path):
    result = run_codex_chat_response_carrier(
        tmp_path,
        operator_message="Say hello.",
        chat_engine_turn=_engine_turn(),
        codex_solo_context=_solo_context(),
        enabled=True,
        response_override="Hello from the fake Codex response carrier.",
    )

    assert result["ok"] is True
    assert result["status"] == "RETURN_CAPTURED_FAKE"
    assert result["response_text"] == "Hello from the fake Codex response carrier."
    assert result["response_sha256"]
    run_path = tmp_path / result["run_packet_path"]
    assert run_path.exists()
    assert "RETURN_CAPTURED_FAKE" in run_path.read_text(encoding="utf-8")


def test_subprocess_runner_records_latest_return_and_events(tmp_path: Path):
    def fake_runner(command, *, cwd, input, text, capture_output, timeout, check):
        latest_return = Path(cwd) / command[command.index("--output-last-message") + 1]
        latest_return.parent.mkdir(parents=True, exist_ok=True)
        latest_return.write_text("A real carrier-shaped response.", encoding="utf-8")
        return subprocess.CompletedProcess(
            command,
            0,
            stdout='{"type":"agent_message","message":"event"}\n',
            stderr="",
        )

    result = run_codex_chat_response_carrier(
        tmp_path,
        operator_message="Answer from runner.",
        chat_engine_turn=_engine_turn(),
        codex_solo_context=_solo_context(),
        enabled=True,
        subprocess_runner=fake_runner,
    )

    assert result["ok"] is True
    assert result["status"] == "RETURN_CAPTURED"
    assert result["response_text"] == "A real carrier-shaped response."
    events_path = tmp_path / result["run"]["events_path"]
    assert "agent_message" in events_path.read_text(encoding="utf-8")


def test_disabled_carrier_returns_fallback_finding_without_run(tmp_path: Path):
    result = run_codex_chat_response_carrier(
        tmp_path,
        operator_message="Do not run.",
        chat_engine_turn=_engine_turn(),
        codex_solo_context=_solo_context(),
        env={},
    )

    assert result["ok"] is False
    assert result["status"] == "CARRIER_DISABLED"
    assert result["finding"] == "chat_response_carrier_disabled"
    assert not (tmp_path / "ION/05_context/current/codex_capsule_chat/response_runs").exists()
