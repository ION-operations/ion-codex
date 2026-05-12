import json
import os
from pathlib import Path

from kernel.ion_codex_queue_runner import (
    build_codex_queue_runner_status,
    prepare_codex_queue_run,
    process_codex_queue_once,
    reconcile_codex_queue_runner_state,
)


def _seed_root(root: Path) -> None:
    (root / "pyproject.toml").write_text("[project]\nname = \"ion-test\"\n", encoding="utf-8")
    (root / "ION/REPO_AUTHORITY.md").parent.mkdir(parents=True)
    (root / "ION/REPO_AUTHORITY.md").write_text("# authority\n", encoding="utf-8")


def _seed_request(root: Path) -> str:
    rel = "ION/05_context/current/chatgpt_connector/codex_work_requests/2026-05-04T000000Z0000_runner_test.json"
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_id": "ion.chatgpt_browser_connector_codex_work_request.v1",
        "request_id": "codex_req_runner_test",
        "objective": "Runner test objective",
        "requested_by": "chatgpt_browser_connector",
        "status": "QUEUED_FOR_CODEX_CARRIER",
        "created_at": "2026-05-04T00:00:00+00:00",
        "updated_at": "2026-05-04T00:00:00+00:00",
        "return_packet_paths": [],
        "latest_return_packet_path": None,
        "request_kind": "codex_chat_response",
        "ion_skill_activation": {
            "skill_id": "codex-chat-answer",
            "display_name": "Codex Chat Answer",
            "activates_templates": ["ION/07_templates/context/ION_CONTEXT_LOAD_PROOF.md"],
        },
        "ion_chat_engine_turn": {
            "response_mode": "answer",
            "carrier_strategy": {"mode": "gpt_5_5_codex_chat_response_contract"},
            "native_lenses": [{"display_name": "Persona", "purpose": "User-facing clarity."}],
        },
        "codex_model_move": {
            "selected_model": "gpt-5.3-codex-spark",
            "selected_reasoning_effort": "low",
            "work_class": "cheap_classification",
            "ion_stage_id": "relay_ingress",
            "usage_pool_id": "codex_spark_observed",
            "usage_pool_authority": "operator_observed_pending_verification",
        },
        "production_authority": False,
        "live_execution_authority": False,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return rel


def _seed_agent_cartography_request(root: Path) -> str:
    rel = "ION/05_context/current/chatgpt_connector/codex_work_requests/2026-05-04T000100Z0000_runner_agent_cartography_test.json"
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "schema_id": "ion.chatgpt_browser_connector_codex_work_request.v1",
        "request_id": "codex_req_runner_agent_cartography_test",
        "objective": "Agent cartography proof run",
        "requested_by": "ion_agent_invocation_broker",
        "status": "QUEUED_FOR_CODEX_CARRIER",
        "created_at": "2026-05-04T00:01:00+00:00",
        "updated_at": "2026-05-04T00:01:00+00:00",
        "return_packet_paths": [],
        "latest_return_packet_path": None,
        "request_kind": "runtime_cartography",
        "production_authority": False,
        "live_execution_authority": False,
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return rel


def _valid_task_return(required_paths: list[str]) -> str:
    proof_lines = ["### CONTEXT PROOF"]
    proof_lines.extend(f"path: {path}\nsha256: testhash\nexcerpt: \"line evidence\"" for path in required_paths)
    return "\n".join([
        *proof_lines,
        "",
        "### TEMPLATE ACTION PROOF",
        "template_id: ion.template.autonomous_loop.local_worker.v1",
        "action_id: codex_queue_runner_test",
        "result: validated queue runner task return",
        "touched_paths:",
        "  - ION/04_packages/kernel/ion_codex_queue_runner.py",
        "",
        "### VALIDATION",
        "commands_run:",
        "  - focused queue runner unit test",
        "tests_passed: queue runner proof gate smoke",
        "tests_failed: none",
        "",
        "### RESULT",
        "implementation_result: queue runner smoke accepted",
        "remaining_blockers: none for unit test",
        "next_lawful_moves: continue",
        "",
        "### WORKLOAD DIFF",
        "- ION/04_packages/kernel/ion_codex_queue_runner.py",
        "",
        "### BLOCKERS",
        "- none",
        "",
        "### RECOMMENDED NEXT PACKET",
        "NEXT_PACKET_EXAMPLE",
        "",
    ])


def test_codex_queue_runner_status_reports_pending_request(tmp_path):
    _seed_root(tmp_path)
    request_rel = _seed_request(tmp_path)

    status = build_codex_queue_runner_status(tmp_path)

    assert status["schema_id"] == "ion.codex_queue_runner.v1"
    assert status["queued_request_count"] == 1
    assert status["next_request_path"] == request_rel
    assert status["manual_proceed_relay_required"] is False


def test_live_status_reports_idle_when_no_active_or_latest_run(tmp_path):
    _seed_root(tmp_path)

    status = build_codex_queue_runner_status(tmp_path, reconcile=False)

    live = status["live_worker_telemetry"]
    assert live["phase_status"] == "idle"
    assert live["active_worker_pid"] is None
    assert live["run_packet_path"] is None
    assert live["artifacts"]["run_packet"]["exists"] is False


def test_live_status_reports_active_run_with_log_sizes(tmp_path):
    _seed_root(tmp_path)
    request_rel = _seed_request(tmp_path)
    prepared = prepare_codex_queue_run(tmp_path, request_path=request_rel, claim=True)
    run = dict(prepared["run"])
    run["status"] = "CODEX_CLI_RUNNING"
    run["pid"] = os.getpid()
    run["started_at"] = "2026-05-04T00:00:00+00:00"
    run_path = tmp_path / run["run_packet_path"]
    run_path.write_text(json.dumps(run, indent=2), encoding="utf-8")
    (tmp_path / run["stdout_path"]).write_text("stdout-bytes\n", encoding="utf-8")
    (tmp_path / run["stderr_path"]).write_text("stderr-bytes\n", encoding="utf-8")
    (tmp_path / run["last_message_path"]).write_text("last-return\n", encoding="utf-8")
    run_dir = tmp_path / run["run_dir"]
    (run_dir / "worker_stdout.log").write_text("worker-stdout\n", encoding="utf-8")
    (run_dir / "worker_stderr.log").write_text("worker-stderr\n", encoding="utf-8")
    state_path = tmp_path / "ION/05_context/current/chatgpt_connector/runtime/codex_queue_runner_state.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(
            {
                "schema_id": "ion.codex_queue_runner_state.v1",
                "active_run": {
                    "run_id": run["run_id"],
                    "pid": os.getpid(),
                    "run_packet_path": run["run_packet_path"],
                    "request_path": request_rel,
                    "started_at": "2026-05-04T00:00:00+00:00",
                },
                "latest_run": run["run_packet_path"],
                "production_authority": False,
                "live_execution_authority": False,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    status = build_codex_queue_runner_status(tmp_path, reconcile=False)

    live = status["live_worker_telemetry"]
    assert live["phase_status"] == "active"
    assert live["active_worker_pid"] == os.getpid()
    assert live["request_path"] == request_rel
    assert live["worker_lifecycle_events"] == []
    assert live["latest_worker_lifecycle_event"] is None
    assert live["artifacts"]["stdout"]["exists"] is True
    assert live["artifacts"]["stderr"]["exists"] is True
    assert live["artifacts"]["latest_return"]["exists"] is True
    assert live["artifacts"]["worker_stdout"]["exists"] is True
    assert live["artifacts"]["worker_stderr"]["exists"] is True
    assert live["artifacts"]["worker_stdout"]["bytes"] == len("worker-stdout\n".encode("utf-8"))
    assert live["terminal_intake_result"]["state"] == "not-completed"
    assert isinstance(live["elapsed_seconds"], int)


def test_live_status_classifies_terminal_accepted_and_blocked(tmp_path):
    _seed_root(tmp_path)
    request_rel = _seed_request(tmp_path)
    prepared = prepare_codex_queue_run(tmp_path, request_path=request_rel, claim=True)
    run = dict(prepared["run"])
    run["started_at"] = "2026-05-04T00:00:00+00:00"
    run["completed_at"] = "2026-05-04T00:05:00+00:00"
    run_path = tmp_path / run["run_packet_path"]
    state_path = tmp_path / "ION/05_context/current/chatgpt_connector/runtime/codex_queue_runner_state.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(
            {
                "schema_id": "ion.codex_queue_runner_state.v1",
                "active_run": None,
                "latest_run": run["run_packet_path"],
                "production_authority": False,
                "live_execution_authority": False,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    run["status"] = "RETURN_RECORDED_PROOF_ACCEPTED"
    run["submit_result"] = {
        "accepted_for_carrier_intake": True,
        "context_proof_accepted": True,
        "template_action_proof_accepted": True,
    }
    run_path.write_text(json.dumps(run, indent=2), encoding="utf-8")
    accepted_status = build_codex_queue_runner_status(tmp_path, reconcile=False)
    accepted_live = accepted_status["live_worker_telemetry"]
    assert accepted_live["phase_status"] == "terminal-accepted"
    assert accepted_live["terminal_intake_result"]["state"] == "accepted"
    assert accepted_live["terminal_intake_result"]["accepted_for_carrier_intake"] is True

    run["status"] = "RETURN_RECORDED_PROOF_BLOCKED"
    run["submit_result"] = {
        "accepted_for_carrier_intake": False,
        "context_proof_accepted": False,
        "template_action_proof_accepted": True,
    }
    run_path.write_text(json.dumps(run, indent=2), encoding="utf-8")
    blocked_status = build_codex_queue_runner_status(tmp_path, reconcile=False)
    blocked_live = blocked_status["live_worker_telemetry"]
    assert blocked_live["phase_status"] == "terminal-blocked"
    assert blocked_live["terminal_intake_result"]["state"] == "blocked"
    assert blocked_live["terminal_intake_result"]["accepted_for_carrier_intake"] is False


def test_prepare_codex_queue_run_writes_prompt_and_receipt_without_claiming(tmp_path):
    _seed_root(tmp_path)
    request_rel = _seed_request(tmp_path)

    prepared = prepare_codex_queue_run(tmp_path)

    assert prepared["ok"] is True
    assert prepared["prepared_only"] is True
    run = prepared["run"]
    assert (tmp_path / run["prompt_path"]).exists()
    assert (tmp_path / run["context_receipt_path"]).exists()
    prompt = (tmp_path / run["prompt_path"]).read_text(encoding="utf-8")
    assert request_rel in prompt
    assert 'request_kind: "codex_chat_response"' in prompt
    assert "ion_chat_engine:" in prompt
    assert 'selected_skill: "Codex Chat Answer"' in prompt
    assert "Persona: User-facing clarity." in prompt
    assert "codex_model_move:" in prompt
    assert 'selected_model: "gpt-5.3-codex-spark"' in prompt
    assert "worker_spawn_contract:" in prompt
    assert "ion_runtime_budget:" in prompt
    assert "return_template: |" in prompt
    assert "result: <one-line result>" in prompt
    assert "touched_paths as a non-empty YAML list" in prompt
    assert run["codex_model_move"]["selected_model"] == "gpt-5.3-codex-spark"
    assert run["codex_command"][:6] == ["codex", "exec", "-m", "gpt-5.3-codex-spark", "-c", "model_reasoning_effort=low"]
    request = json.loads((tmp_path / request_rel).read_text(encoding="utf-8"))
    assert request["status"] == "QUEUED_FOR_CODEX_CARRIER"


def test_prepare_codex_queue_run_includes_workload_diff_for_agent_cartography_contract(tmp_path):
    _seed_root(tmp_path)
    _seed_request(tmp_path)
    request_rel = _seed_agent_cartography_request(tmp_path)

    prepared = prepare_codex_queue_run(tmp_path, request_path=request_rel)

    assert prepared["ok"] is True
    prompt = (tmp_path / prepared["run"]["prompt_path"]).read_text(encoding="utf-8")
    assert "### WORKLOAD DIFF" in prompt


def test_process_once_inline_records_proof_gated_task_return(tmp_path):
    _seed_root(tmp_path)
    request_rel = _seed_request(tmp_path)
    prepared = prepare_codex_queue_run(tmp_path)
    required_paths = [item["path"] for item in prepared["context_receipt"]["required_context_reads"]]
    task_output = _valid_task_return(required_paths)

    result = process_codex_queue_once(
        tmp_path,
        request_path=request_rel,
        start=True,
        background=False,
        task_output_override=task_output,
    )

    assert result["ok"] is True
    assert result["result"] == "RETURN_RECORDED_PROOF_ACCEPTED"
    assert result["run"]["pid"] > 0
    event_names = [event["event"] for event in result["run"]["worker_lifecycle_events"]]
    assert event_names == ["worker_boot", "worker_terminal"]
    assert result["run"]["worker_lifecycle_events"][-1]["terminal_state"] == "accepted"
    assert result["run"]["worker_lifecycle_events"][-1]["context_proof_accepted"] is True
    assert result["run"]["worker_lifecycle_events"][-1]["template_action_proof_accepted"] is True
    status = build_codex_queue_runner_status(tmp_path, reconcile=False)
    live = status["live_worker_telemetry"]
    assert live["latest_worker_lifecycle_event"]["event"] == "worker_terminal"
    assert live["latest_worker_lifecycle_event"]["terminal_state"] == "accepted"
    request = json.loads((tmp_path / request_rel).read_text(encoding="utf-8"))
    assert request["status"] == "RETURN_RECORDED_PROOF_ACCEPTED"
    assert request["latest_context_proof_accepted"] is True
    assert request["latest_template_action_proof_accepted"] is True
    assert (tmp_path / request["latest_return_packet_path"]).exists()


def test_process_once_inline_reports_proof_blocked_return_as_backend_failure(tmp_path):
    _seed_root(tmp_path)
    request_rel = _seed_request(tmp_path)

    result = process_codex_queue_once(
        tmp_path,
        request_path=request_rel,
        start=True,
        background=False,
        task_output_override="### RESULT\nmissing required proof sections\n",
    )

    assert result["ok"] is False
    assert result["result"] == "RETURN_TEMPLATE_INVALID"
    assert result["run"]["failure_classification"] == "BACKEND_CODEX_FAILURE"
    assert result["run"]["worker_lifecycle_events"][-1]["event"] == "worker_terminal"
    assert result["run"]["worker_lifecycle_events"][-1]["terminal_state"] == "template_invalid"
    request = json.loads((tmp_path / request_rel).read_text(encoding="utf-8"))
    assert request["status"] == "RETURN_TEMPLATE_INVALID"
    assert request["failure_classification"] == "BACKEND_CODEX_FAILURE"
    assert request["latest_context_proof_accepted"] is False
    assert request["latest_template_action_proof_accepted"] is False


def test_reconcile_marks_dead_active_worker_failed_and_clears_state(tmp_path):
    _seed_root(tmp_path)
    request_rel = _seed_request(tmp_path)
    prepared = prepare_codex_queue_run(tmp_path, request_path=request_rel, claim=True)
    run = dict(prepared["run"])
    run_path = tmp_path / run["run_packet_path"]
    run["status"] = "CODEX_CLI_RUNNING"
    run["pid"] = 999999999
    run_path.write_text(json.dumps(run, indent=2), encoding="utf-8")
    state_path = tmp_path / "ION/05_context/current/chatgpt_connector/runtime/codex_queue_runner_state.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(
            {
                "schema_id": "ion.codex_queue_runner_state.v1",
                "active_run": {
                    "run_id": run["run_id"],
                    "pid": 999999999,
                    "run_packet_path": run["run_packet_path"],
                    "request_path": request_rel,
                    "started_at": "2026-05-04T00:00:00+00:00",
                },
                "latest_run": run["run_packet_path"],
                "production_authority": False,
                "live_execution_authority": False,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = reconcile_codex_queue_runner_state(tmp_path, write=True)

    assert result["ok"] is True
    assert result["stale_active_run_detected"] is True
    assert result["action"] == "mark_daemon_failure_and_clear_active"
    updated_run = json.loads(run_path.read_text(encoding="utf-8"))
    assert updated_run["status"] == "DAEMON_WORKER_EXITED_WITHOUT_FINALIZATION"
    assert updated_run["failure_classification"] == "DAEMON_FAILURE"
    assert updated_run["daemon_reconciliation"]["output_presence"] == {
        "stdout_exists": False,
        "stderr_exists": False,
        "last_message_exists": False,
    }
    updated_request = json.loads((tmp_path / request_rel).read_text(encoding="utf-8"))
    assert updated_request["status"] == "CODEX_QUEUE_RUNNER_FAILED"
    assert updated_request["failure_classification"] == "DAEMON_FAILURE"
    runner_state = json.loads(state_path.read_text(encoding="utf-8"))
    assert runner_state["active_run"] is None


def test_status_classifies_latest_proof_blocked_run_without_accepting(tmp_path):
    _seed_root(tmp_path)
    request_rel = _seed_request(tmp_path)
    prepared = prepare_codex_queue_run(tmp_path, request_path=request_rel, claim=True)
    run = dict(prepared["run"])
    run_path = tmp_path / run["run_packet_path"]
    run["status"] = "RETURN_RECORDED_PROOF_BLOCKED"
    run["failure_classification"] = None
    run_path.write_text(json.dumps(run, indent=2), encoding="utf-8")
    state_path = tmp_path / "ION/05_context/current/chatgpt_connector/runtime/codex_queue_runner_state.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(
            {
                "schema_id": "ion.codex_queue_runner_state.v1",
                "active_run": None,
                "latest_run": run["run_packet_path"],
                "production_authority": False,
                "live_execution_authority": False,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    status = build_codex_queue_runner_status(tmp_path)

    assert status["reconciliation"]["latest_run_failure_classification_updated"] is True
    updated_run = json.loads(run_path.read_text(encoding="utf-8"))
    assert updated_run["status"] == "RETURN_RECORDED_PROOF_BLOCKED"
    assert updated_run["failure_classification"] == "BACKEND_CODEX_FAILURE"
    updated_request = json.loads((tmp_path / request_rel).read_text(encoding="utf-8"))
    assert updated_request["status"] == "RETURN_RECORDED_PROOF_BLOCKED"
    assert updated_request["failure_classification"] == "BACKEND_CODEX_FAILURE"


def test_reconcile_terminal_failed_run_clears_active_without_starting_new_work(tmp_path):
    _seed_root(tmp_path)
    request_rel = _seed_request(tmp_path)
    prepared = prepare_codex_queue_run(tmp_path, request_path=request_rel, claim=True)
    run = dict(prepared["run"])
    run_path = tmp_path / run["run_packet_path"]
    run["status"] = "CODEX_CLI_EXIT_NONZERO"
    run["failure_classification"] = "CODEX_CLI_FAILURE"
    run["pid"] = 999999999
    run_path.write_text(json.dumps(run, indent=2), encoding="utf-8")
    request_path = tmp_path / request_rel
    request = json.loads(request_path.read_text(encoding="utf-8"))
    request["status"] = "CODEX_QUEUE_RUNNER_FAILED"
    request["failure_classification"] = "CODEX_CLI_FAILURE"
    request_path.write_text(json.dumps(request, indent=2), encoding="utf-8")
    state_path = tmp_path / "ION/05_context/current/chatgpt_connector/runtime/codex_queue_runner_state.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(
            {
                "schema_id": "ion.codex_queue_runner_state.v1",
                "active_run": {
                    "run_id": run["run_id"],
                    "pid": 999999999,
                    "run_packet_path": run["run_packet_path"],
                    "request_path": request_rel,
                    "started_at": "2026-05-04T00:00:00+00:00",
                },
                "latest_run": run["run_packet_path"],
                "production_authority": False,
                "live_execution_authority": False,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    run_count_before = len(list((tmp_path / "ION/05_context/current/chatgpt_connector/codex_queue_runs").rglob("run.json")))

    result = reconcile_codex_queue_runner_state(tmp_path, write=True)

    run_count_after = len(list((tmp_path / "ION/05_context/current/chatgpt_connector/codex_queue_runs").rglob("run.json")))
    assert result["ok"] is True
    assert result["action"] == "clear_terminal_active_reference"
    assert result["stale_active_run_detected"] is False
    assert run_count_after == run_count_before
    updated_run = json.loads(run_path.read_text(encoding="utf-8"))
    assert updated_run["status"] == "CODEX_CLI_EXIT_NONZERO"
    updated_request = json.loads(request_path.read_text(encoding="utf-8"))
    assert updated_request["status"] == "CODEX_QUEUE_RUNNER_FAILED"
    runner_state = json.loads(state_path.read_text(encoding="utf-8"))
    assert runner_state["active_run"] is None


def test_reconcile_non_terminal_running_process_is_not_marked_complete(tmp_path):
    _seed_root(tmp_path)
    request_rel = _seed_request(tmp_path)
    prepared = prepare_codex_queue_run(tmp_path, request_path=request_rel, claim=True)
    run = dict(prepared["run"])
    run_path = tmp_path / run["run_packet_path"]
    run["status"] = "CODEX_CLI_RUNNING"
    run["pid"] = os.getpid()
    run_path.write_text(json.dumps(run, indent=2), encoding="utf-8")
    state_path = tmp_path / "ION/05_context/current/chatgpt_connector/runtime/codex_queue_runner_state.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(
            {
                "schema_id": "ion.codex_queue_runner_state.v1",
                "active_run": {
                    "run_id": run["run_id"],
                    "pid": os.getpid(),
                    "run_packet_path": run["run_packet_path"],
                    "request_path": request_rel,
                    "started_at": "2026-05-04T00:00:00+00:00",
                },
                "latest_run": run["run_packet_path"],
                "production_authority": False,
                "live_execution_authority": False,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    result = reconcile_codex_queue_runner_state(tmp_path, write=True)

    runner_state = json.loads(state_path.read_text(encoding="utf-8"))
    updated_run = json.loads(run_path.read_text(encoding="utf-8"))
    assert result["ok"] is True
    assert result["action"] == "active_run_still_running"
    assert result["active_process_running"] is True
    assert result["stale_active_run_detected"] is False
    assert updated_run["status"] == "CODEX_CLI_RUNNING"
    assert runner_state["active_run"] is not None
