import base64
import hashlib
import json
from pathlib import Path

from kernel.ion_chatgpt_browser_mcp_connector_contract import (
    BOUNDED_QUEUE_RECEIPT_TOOLS,
    FORBIDDEN_CAPABILITIES,
    STATUS_READ_TOOLS,
    audit_chatgpt_browser_mcp_connector_contract,
    call_chatgpt_connector_tool,
    write_chatgpt_browser_mcp_connector_contract,
)
from kernel.ion_chatgpt_browser_mcp_http_preview import documented_launch_requests_serve


def _seed_root(root: Path) -> None:
    (root / "pyproject.toml").write_text("[project]\nname = \"ion-test\"\n", encoding="utf-8")
    (root / "ION/REPO_AUTHORITY.md").parent.mkdir(parents=True)
    (root / "ION/REPO_AUTHORITY.md").write_text("# authority\n", encoding="utf-8")


def test_v120_contract_policy_blocks_unsafe_tools():
    root = Path.cwd()
    result = audit_chatgpt_browser_mcp_connector_contract(root)

    assert result["schema_id"] == "ion.chatgpt_browser_mcp_connector_contract.v1"
    assert result["verdict"] == "ION_CHATGPT_BROWSER_MCP_CONNECTOR_CONTRACT_READY"
    assert "arbitrary_shell" in result["forbidden_tools"]
    assert not (set(result["allowed_tools"]) & set(result["forbidden_tools"]))
    assert set(result["status_read_tools"]) == STATUS_READ_TOOLS
    assert set(result["bounded_queue_receipt_tools"]) == BOUNDED_QUEUE_RECEIPT_TOOLS
    assert result["production_authority"] is False
    assert result["live_execution_authority"] is False


def test_status_and_current_packet_tools_read_without_shell_access():
    root = Path.cwd()

    status = call_chatgpt_connector_tool(root, "ion_status", {})
    packet = call_chatgpt_connector_tool(root, "ion_current_operating_packet", {})
    onboarding = call_chatgpt_connector_tool(root, "ion_carrier_onboarding_packet", {"carrier": "chatgpt_browser"})
    forbidden = call_chatgpt_connector_tool(root, "arbitrary_shell", {})

    assert status["ok"] is True
    assert status["data"]["schema_id"] == "ion.status.v1"
    assert packet["ok"] is True
    assert "ION Current Operating Packet" in packet["data"]["content"]["text"]
    assert onboarding["ok"] is True
    assert onboarding["data"]["schema_id"] == "ion.carrier_onboarding_packet.v1"
    assert onboarding["data"]["root_markdown_onboarding_authority"] is False
    assert onboarding["data"]["carrier_profile"]["path"] == "ION/03_registry/chatgpt_browser_carrier_profile.yaml"
    queue = call_chatgpt_connector_tool(root, "ion_codex_work_queue", {"limit": 10})
    manifest = call_chatgpt_connector_tool(root, "ion_tool_manifest", {})
    daemon = call_chatgpt_connector_tool(root, "ion_daemon_status", {})
    live_status = call_chatgpt_connector_tool(root, "ion_codex_worker_live_status", {})
    agent_status = call_chatgpt_connector_tool(root, "ion_agent_status", {})
    assert queue["ok"] is True
    assert queue["data"]["schema_id"] == "ion.chatgpt_browser_connector_codex_work_queue.v1"
    assert manifest["ok"] is True
    assert "ion_file_read" in manifest["data"]["allowed_tools"]
    assert "ion_codex_queue_process_once" in manifest["data"]["allowed_tools"]
    assert "ion_agent_invoke" in manifest["data"]["allowed_tools"]
    assert daemon["ok"] is True
    assert daemon["data"]["schema_id"] == "ion.codex_queue_runner.v1"
    assert live_status["ok"] is True
    assert live_status["data"]["schema_id"] == "ion.codex_queue_runner.v1"
    assert live_status["data"]["live_worker_telemetry"]["schema_id"] == "ion.codex_worker_live_status.v1"
    assert agent_status["ok"] is True
    assert agent_status["data"]["schema_id"] == "ion.agent_invocation_broker.v1"
    assert forbidden["ok"] is False
    assert forbidden["finding"] == "forbidden_capability"


def test_live_status_preview_refuses_non_public_target(tmp_path):
    _seed_root(tmp_path)

    status = call_chatgpt_connector_tool(
        tmp_path,
        "ion_codex_worker_live_status",
        {"include_preview": True, "preview_target": ".env", "max_preview_bytes": 128},
    )

    assert status["ok"] is True
    preview = status["data"]["live_worker_telemetry"]["preview"]
    assert preview["requested"] is True
    assert preview["included"] is False
    assert preview["finding"] == "preview_target_not_allowed_public_log_only"


def test_queue_tool_writes_only_bounded_operator_queue(tmp_path):
    _seed_root(tmp_path)

    result = call_chatgpt_connector_tool(
        tmp_path,
        "ion_queue_operator_message",
        {"message": "V120 bounded connector queue test", "priority": 70},
    )

    queue_path = tmp_path / "ION/05_context/current/ACTIVE_OPERATOR_MESSAGE_QUEUE.json"
    assert result["ok"] is True
    assert result["mutates_active_state"] is True
    assert result["data"]["queue_path"] == "ION/05_context/current/ACTIVE_OPERATOR_MESSAGE_QUEUE.json"
    assert queue_path.exists()
    assert "chatgpt_browser_connector" in queue_path.read_text(encoding="utf-8")


def test_connector_timeout_policy_enforces_minimum_for_agent_invoke(tmp_path, monkeypatch):
    import kernel.ion_chatgpt_browser_mcp_connector_contract as contract

    _seed_root(tmp_path)
    captured: dict[str, int] = {}

    def fake_invoke_agent(_root, **kwargs):
        captured["timeout_seconds"] = int(kwargs["timeout_seconds"])
        return {"ok": True, "result": "QUEUED"}

    monkeypatch.setattr(contract, "invoke_agent", fake_invoke_agent)
    result = call_chatgpt_connector_tool(
        tmp_path,
        "ion_agent_invoke",
        {
            "agent": "context_cartographer",
            "objective": "cartography proof packet timeout policy smoke",
            "start": True,
            "timeout_seconds": 30,
        },
    )

    assert result["ok"] is True
    assert captured["timeout_seconds"] == 900


def test_connector_timeout_policy_enforces_minimum_for_cartography_queue_run(tmp_path, monkeypatch):
    import kernel.ion_chatgpt_browser_mcp_connector_contract as contract

    _seed_root(tmp_path)
    request_rel = "ION/05_context/current/chatgpt_connector/codex_work_requests/cartography_timeout_test.json"
    request_path = tmp_path / request_rel
    request_path.parent.mkdir(parents=True, exist_ok=True)
    request_path.write_text(
        json.dumps(
            {
                "schema_id": "ion.chatgpt_browser_connector_codex_work_request.v1",
                "request_id": "codex_req_cartography_timeout_test",
                "objective": "Runtime cartography proof run",
                "request_kind": "runtime_cartography",
                "status": "QUEUED_FOR_CODEX_CARRIER",
                "requested_by": "chatgpt_browser_connector",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    captured: dict[str, int] = {}

    def fake_process_codex_queue_once(_root, **kwargs):
        captured["timeout_seconds"] = int(kwargs["timeout_seconds"])
        return {"ok": True, "result": "PREPARED"}

    monkeypatch.setattr(contract, "process_codex_queue_once", fake_process_codex_queue_once)
    result = call_chatgpt_connector_tool(
        tmp_path,
        "ion_codex_queue_process_once",
        {"request_path": request_rel, "start": True, "timeout_seconds": 180},
    )

    assert result["ok"] is True
    assert captured["timeout_seconds"] == 900


def test_task_return_requires_context_and_template_action_proof(tmp_path):
    _seed_root(tmp_path)
    receipt = {
        "schema_id": "ion.context_load_receipt.v1",
        "required_context_reads": [
            {"kind": "file", "path": "ION/REPO_AUTHORITY.md", "required": True}
        ],
    }
    missing_template = """### CONTEXT PROOF
- ION/REPO_AUTHORITY.md excerpt: authority line read.

### RESULT
No template proof.
"""
    valid = """### CONTEXT PROOF
path: ION/REPO_AUTHORITY.md
sha256: testhash
excerpt: "authority line read."

### TEMPLATE ACTION PROOF
template_id: ion.template.patch_proposal.v1
action_id: v120-chatgpt-connector-test
result: validated bounded connector return
touched_paths:
  - ION/docs/setup/CHATGPT_BROWSER_MCP_CONNECTOR_SETUP_V120.md

### VALIDATION
- unit test

### RESULT
Validated.

### WORKLOAD DIFF
- ION/docs/setup/CHATGPT_BROWSER_MCP_CONNECTOR_SETUP_V120.md

### BLOCKERS
- none

### RECOMMENDED NEXT PACKET
NEXT_PACKET_EXAMPLE
"""

    blocked = call_chatgpt_connector_tool(
        tmp_path,
        "ion_submit_task_return",
        {"task_output_text": missing_template, "context_receipt": receipt},
    )
    accepted = call_chatgpt_connector_tool(
        tmp_path,
        "ion_submit_task_return",
        {"task_output_text": valid, "context_receipt": receipt},
    )

    assert blocked["ok"] is True
    assert blocked["data"]["accepted_for_carrier_intake"] is False
    assert blocked["data"]["context_proof_accepted"] is True
    assert blocked["data"]["template_action_proof_accepted"] is False
    assert accepted["ok"] is True
    assert accepted["data"]["accepted_for_carrier_intake"] is True
    packet = tmp_path / accepted["data"]["packet_path"]
    assert packet.exists()
    assert "RECORDED_FOR_CARRIER_INTAKE" in packet.read_text(encoding="utf-8")


def test_task_return_requires_workload_diff_when_request_contract_declares_it(tmp_path):
    _seed_root(tmp_path)
    request_rel = "ION/05_context/current/chatgpt_connector/codex_work_requests/workload_diff_required.json"
    request_path = tmp_path / request_rel
    request_path.parent.mkdir(parents=True, exist_ok=True)
    request_path.write_text(
        json.dumps(
            {
                "schema_id": "ion.chatgpt_browser_connector_codex_work_request.v1",
                "request_id": "codex_req_workload_diff_required",
                "objective": "Agent cartography proof run",
                "requested_by": "ion_agent_invocation_broker",
                "status": "QUEUED_FOR_CODEX_CARRIER",
                "return_contract_sections": [
                    "### CONTEXT PROOF",
                    "### TEMPLATE ACTION PROOF",
                    "### VALIDATION",
                    "### RESULT",
                    "### WORKLOAD DIFF",
                ],
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    receipt = {
        "schema_id": "ion.context_load_receipt.v1",
        "required_context_reads": [
            {"kind": "file", "path": "ION/REPO_AUTHORITY.md", "required": True}
        ],
    }
    missing_workload_diff = """### CONTEXT PROOF
- ION/REPO_AUTHORITY.md excerpt: authority line read.

### TEMPLATE ACTION PROOF
template_id: ion.template.autonomous_loop.local_worker.v1
action_id: workload-diff-required-test
result: tested required workload diff contract
touched_paths:
  - ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py

### VALIDATION
commands_run:
  - pytest targeted

### RESULT
Missing workload diff section.
"""

    blocked = call_chatgpt_connector_tool(
        tmp_path,
        "ion_submit_task_return",
        {
            "task_output_text": missing_workload_diff,
            "context_receipt": receipt,
            "work_request_path": request_rel,
        },
    )

    assert blocked["ok"] is True
    assert blocked["data"]["accepted_for_carrier_intake"] is False
    assert blocked["data"]["workload_diff_required"] is True
    assert blocked["data"]["workload_diff_present"] is False
    assert "missing_required_section:### WORKLOAD DIFF" in blocked["data"]["findings"]


def test_task_return_template_invalid_is_blocked_before_proof_intake_and_preserved(tmp_path):
    _seed_root(tmp_path)
    receipt = {
        "schema_id": "ion.context_load_receipt.v1",
        "required_context_reads": [
            {"kind": "file", "path": "ION/REPO_AUTHORITY.md", "required": True}
        ],
    }
    broken = """### RESULT
No required template headings.
"""

    blocked = call_chatgpt_connector_tool(
        tmp_path,
        "ion_submit_task_return",
        {"task_output_text": broken, "context_receipt": receipt},
    )

    assert blocked["ok"] is True
    assert blocked["data"]["accepted_for_carrier_intake"] is False
    assert blocked["data"]["return_template_valid"] is False
    assert blocked["data"]["blocked_but_preserved"] is True
    assert blocked["data"]["salvage_route"] == "ION/05_context/current/chatgpt_connector/task_returns"
    assert "missing_required_section:### CONTEXT PROOF" in blocked["data"]["findings"]
    packet = json.loads((tmp_path / blocked["data"]["packet_path"]).read_text(encoding="utf-8"))
    assert packet["result"] == "RETURN_TEMPLATE_INVALID"


def test_connector_does_not_crown_chatgpt_identity():
    result = audit_chatgpt_browser_mcp_connector_contract(Path.cwd())

    assert result["connector_id"] == "ION_CHATGPT_BROWSER_CONNECTOR"
    assert result["must_not_claim_ion_identity"] is True
    assert result["must_not_claim_steward_relay_persona"] is True
    assert result["deployment_authority"] is False


def test_write_contract_report(tmp_path):
    root = Path.cwd()
    output = tmp_path / "CHATGPT_BROWSER_MCP_CONNECTOR_CONTRACT_V120.json"

    result = write_chatgpt_browser_mcp_connector_contract(root, output=output)

    assert output.exists()
    assert result["verdict"] == "ION_CHATGPT_BROWSER_MCP_CONNECTOR_CONTRACT_READY"
    assert not (set(result["allowed_tools"]) & FORBIDDEN_CAPABILITIES)


def test_http_preview_documented_host_port_launch_serves():
    assert documented_launch_requests_serve(["--ion-root", ".", "--host", "127.0.0.1", "--port", "8765"]) is True
    assert documented_launch_requests_serve([]) is False
    assert documented_launch_requests_serve(["--json", "--host", "127.0.0.1"]) is False


def test_file_put_text_stages_artifact_with_receipt(tmp_path):
    _seed_root(tmp_path)
    text = "browser-created planning artifact\n"
    expected = hashlib.sha256(text.encode("utf-8")).hexdigest()

    result = call_chatgpt_connector_tool(
        tmp_path,
        "ion_file_put_text",
        {
            "target_path": "ION/05_context/current/chatgpt_connector/artifacts/browser_note.md",
            "text": text,
            "expected_sha256": expected,
        },
    )

    assert result["ok"] is True
    assert result["mutates_active_state"] is True
    assert result["data"]["sha256"] == expected
    assert (tmp_path / "ION/05_context/current/chatgpt_connector/artifacts/browser_note.md").read_text(encoding="utf-8") == text
    assert (tmp_path / result["data"]["receipt_path"]).exists()


def test_file_put_text_blocks_path_escape_and_overwrite(tmp_path):
    _seed_root(tmp_path)
    target = tmp_path / "ION/05_context/current/chatgpt_connector/artifacts/existing.md"
    target.parent.mkdir(parents=True)
    target.write_text("existing\n", encoding="utf-8")

    escaped = call_chatgpt_connector_tool(
        tmp_path,
        "ion_file_put_text",
        {"target_path": "../outside.md", "text": "bad"},
    )
    overwrite = call_chatgpt_connector_tool(
        tmp_path,
        "ion_file_put_text",
        {"target_path": "ION/05_context/current/chatgpt_connector/artifacts/existing.md", "text": "new"},
    )

    assert escaped["ok"] is False
    assert escaped["finding"] == "target_path_must_be_repo_relative_without_escape"
    assert overwrite["ok"] is False
    assert overwrite["finding"] == "target_exists_requires_lifecycle_receipt"
    assert target.read_text(encoding="utf-8") == "existing\n"


def test_chunked_artifact_upload_commit_verifies_sha256(tmp_path):
    _seed_root(tmp_path)
    data = b"chunk-one::chunk-two"
    expected = hashlib.sha256(data).hexdigest()

    init = call_chatgpt_connector_tool(
        tmp_path,
        "ion_artifact_upload_init",
        {
            "artifact_name": "payload.bin",
            "target_path": "ION/05_context/current/chatgpt_connector/artifacts/payload.bin",
            "expected_sha256": expected,
            "total_bytes": len(data),
        },
    )
    upload_id = init["data"]["upload_id"]
    chunk = call_chatgpt_connector_tool(
        tmp_path,
        "ion_artifact_upload_chunk",
        {
            "upload_id": upload_id,
            "chunk_index": 0,
            "data_base64": base64.b64encode(data).decode("ascii"),
            "chunk_sha256": expected,
        },
    )
    commit = call_chatgpt_connector_tool(tmp_path, "ion_artifact_upload_commit", {"upload_id": upload_id})

    assert init["ok"] is True
    assert chunk["ok"] is True
    assert commit["ok"] is True
    assert commit["data"]["sha256"] == expected
    assert (tmp_path / "ION/05_context/current/chatgpt_connector/artifacts/payload.bin").read_bytes() == data


def test_carrier_message_send_poll_ack_uses_active_queue(tmp_path):
    _seed_root(tmp_path)

    sent = call_chatgpt_connector_tool(
        tmp_path,
        "ion_carrier_message_send",
        {
            "sender_carrier_id": "CHATGPT_BROWSER_CARRIER",
            "recipient": "CODEX_CLI_CARRIER",
            "body": "handoff ready",
            "context_refs": ["ION/02_architecture/ION_FULL_CARRIER_MCP_PARITY_PROTOCOL.md"],
        },
    )
    message_id = sent["data"]["message_id"]
    polled = call_chatgpt_connector_tool(
        tmp_path,
        "ion_carrier_message_poll",
        {"recipient": "CODEX_CLI_CARRIER"},
    )
    acked = call_chatgpt_connector_tool(
        tmp_path,
        "ion_carrier_message_ack",
        {"message_id": message_id, "ack_by_carrier": "CODEX_CLI_CARRIER"},
    )

    assert sent["ok"] is True
    assert sent["mutates_active_state"] is True
    assert polled["ok"] is True
    assert polled["data"]["message_count"] == 1
    assert polled["data"]["messages"][0]["message_id"] == message_id
    assert acked["ok"] is True
    assert (tmp_path / "ION/05_context/current/ACTIVE_CARRIER_MESSAGE_QUEUE.json").exists()


def test_bounded_project_visibility_tools_read_search_and_tree(tmp_path):
    _seed_root(tmp_path)
    note = tmp_path / "ION/02_architecture/VISIBILITY_NOTE.md"
    note.parent.mkdir(parents=True)
    note.write_text("full carrier visibility token\n", encoding="utf-8")
    registry = tmp_path / "ION/03_registry/sample_registry.yaml"
    registry.parent.mkdir(parents=True)
    registry.write_text("schema_id: sample\n", encoding="utf-8")
    template = tmp_path / "ION/07_templates/sample_template.md"
    template.parent.mkdir(parents=True)
    template.write_text("# Template\n", encoding="utf-8")

    read = call_chatgpt_connector_tool(tmp_path, "ion_file_read", {"path": "ION/02_architecture/VISIBILITY_NOTE.md"})
    search = call_chatgpt_connector_tool(tmp_path, "ion_file_search", {"query": "visibility token", "roots": ["ION/02_architecture"]})
    tree = call_chatgpt_connector_tool(tmp_path, "ion_tree_list", {"path": "ION", "max_depth": 2})
    reg = call_chatgpt_connector_tool(tmp_path, "ion_registry_read", {"path": "ION/03_registry/sample_registry.yaml"})
    tmpl = call_chatgpt_connector_tool(tmp_path, "ion_template_read", {"path": "ION/07_templates/sample_template.md"})
    blocked = call_chatgpt_connector_tool(tmp_path, "ion_file_read", {"path": ".git/config"})

    assert read["ok"] is True
    assert "visibility token" in read["data"]["text"]
    assert search["ok"] is True
    assert search["data"]["match_count"] == 1
    assert tree["ok"] is True
    assert any(item["path"] == "ION/02_architecture/VISIBILITY_NOTE.md" for item in tree["data"]["entries"])
    assert reg["ok"] is True
    assert "schema_id: sample" in reg["data"]["text"]
    assert tmpl["ok"] is True
    assert "# Template" in tmpl["data"]["text"]
    assert blocked["ok"] is False
    assert blocked["finding"] == "path_forbidden_by_read_policy"


def test_context_compile_receipt_hydrate_and_onboarding_alias(tmp_path):
    _seed_root(tmp_path)
    required = [
        "ION/02_architecture/ION_MOUNT_CONTRACT.md",
        "ION/02_architecture/ION_FULL_CARRIER_MCP_PARITY_PROTOCOL.md",
        "ION/02_architecture/ION_CARRIER_TO_CARRIER_COMMUNICATION_PROTOCOL.md",
        "ION/03_registry/chatgpt_browser_carrier_profile.yaml",
        "ION/03_registry/carrier_capability_registry.yaml",
        "ION/03_registry/mcp_full_carrier_tool_registry.yaml",
        "ION/05_context/current/CHATGPT_BROWSER_MCP_CONNECTOR_CONTRACT_V120.json",
        "ION/05_context/current/CHATGPT_BROWSER_CLOUDFLARE_TUNNEL_V122.json",
        "ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json",
        "ION/05_context/current/ACTIVE_CARRIER_MESSAGE_QUEUE.json",
    ]
    for rel in required:
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}\n" if path.suffix == ".json" else "surface\n", encoding="utf-8")

    compiled = call_chatgpt_connector_tool(tmp_path, "ion_context_compile", {"profile": "full_carrier_mcp_parity"})
    hydrated = call_chatgpt_connector_tool(tmp_path, "ion_receipt_hydrate", {"limit": 5})
    onboarding = call_chatgpt_connector_tool(Path.cwd(), "ion_carrier_onboarding_packet", {"carrier": "full_carrier_mcp_parity"})

    assert compiled["ok"] is True
    assert compiled["data"]["profile"] == "full_carrier_mcp_parity"
    assert compiled["data"]["surface_count"] >= len(required)
    assert hydrated["ok"] is True
    assert hydrated["data"]["schema_id"] == "ion.receipt_hydration_view_model.v1"
    assert onboarding["ok"] is True
    assert onboarding["data"]["carrier_profile"]["path"] == "ION/03_registry/chatgpt_browser_carrier_profile.yaml"


def test_codex_runner_reconcile_tool_clears_terminal_stale_active_reference(tmp_path):
    _seed_root(tmp_path)
    run_rel = "ION/05_context/current/chatgpt_connector/codex_queue_runs/run_test/run.json"
    run_path = tmp_path / run_rel
    run_path.parent.mkdir(parents=True, exist_ok=True)
    run_path.write_text(
        json.dumps(
            {
                "schema_id": "ion.codex_queue_runner_run.v1",
                "run_id": "run_test",
                "request_id": "req_test",
                "status": "CODEX_CLI_EXIT_NONZERO",
                "failure_classification": "CODEX_CLI_FAILURE",
                "run_packet_path": run_rel,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    state_path = tmp_path / "ION/05_context/current/chatgpt_connector/runtime/codex_queue_runner_state.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(
            {
                "schema_id": "ion.codex_queue_runner_state.v1",
                "active_run": {
                    "run_id": "run_test",
                    "pid": 999999999,
                    "run_packet_path": run_rel,
                    "request_path": "ION/05_context/current/chatgpt_connector/codex_work_requests/req_test.json",
                    "started_at": "2026-05-09T00:00:00+00:00",
                },
                "latest_run": run_rel,
                "production_authority": False,
                "live_execution_authority": False,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    reconciled = call_chatgpt_connector_tool(tmp_path, "ion_codex_runner_reconcile", {"write": True})

    updated_state = json.loads(state_path.read_text(encoding="utf-8"))
    assert reconciled["ok"] is True
    assert reconciled["mutates_active_state"] is True
    assert reconciled["data"]["reconciliation"]["action"] == "clear_terminal_active_reference"
    assert updated_state["active_run"] is None


def test_codex_worker_live_status_exposes_worker_lifecycle_events(tmp_path):
    _seed_root(tmp_path)
    run_rel = "ION/05_context/current/chatgpt_connector/codex_queue_runs/run_lifecycle/run.json"
    run_path = tmp_path / run_rel
    run_path.parent.mkdir(parents=True, exist_ok=True)
    task_return_rel = "ION/05_context/current/chatgpt_connector/task_returns/return_lifecycle.json"
    run_path.write_text(
        json.dumps(
            {
                "schema_id": "ion.codex_queue_runner_run.v1",
                "run_id": "run_lifecycle",
                "request_id": "req_lifecycle",
                "request_path": "ION/05_context/current/chatgpt_connector/codex_work_requests/req_lifecycle.json",
                "run_packet_path": run_rel,
                "run_dir": "ION/05_context/current/chatgpt_connector/codex_queue_runs/run_lifecycle",
                "status": "RETURN_RECORDED_PROOF_ACCEPTED",
                "started_at": "2026-05-10T17:00:00+00:00",
                "completed_at": "2026-05-10T17:01:00+00:00",
                "submit_result": {
                    "accepted_for_carrier_intake": True,
                    "context_proof_accepted": True,
                    "template_action_proof_accepted": True,
                    "packet_path": task_return_rel,
                },
                "worker_lifecycle_events": [
                    {
                        "event": "worker_boot",
                        "at": "2026-05-10T17:00:01+00:00",
                        "run_id": "run_lifecycle",
                        "request_id": "req_lifecycle",
                        "status": "CODEX_CLI_RUNNING",
                        "pid": 123,
                        "production_authority": False,
                        "live_execution_authority": False,
                    },
                    {
                        "event": "worker_terminal",
                        "at": "2026-05-10T17:01:00+00:00",
                        "run_id": "run_lifecycle",
                        "request_id": "req_lifecycle",
                        "status": "RETURN_RECORDED_PROOF_ACCEPTED",
                        "pid": 123,
                        "terminal_state": "accepted",
                        "task_return_packet_path": task_return_rel,
                        "context_proof_accepted": True,
                        "template_action_proof_accepted": True,
                        "production_authority": False,
                        "live_execution_authority": False,
                    },
                ],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    state_path = tmp_path / "ION/05_context/current/chatgpt_connector/runtime/codex_queue_runner_state.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        json.dumps(
            {
                "schema_id": "ion.codex_queue_runner_state.v1",
                "active_run": None,
                "latest_run": run_rel,
                "production_authority": False,
                "live_execution_authority": False,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    status = call_chatgpt_connector_tool(tmp_path, "ion_codex_worker_live_status", {})

    telemetry = status["data"]["live_worker_telemetry"]
    assert status["ok"] is True
    assert telemetry["run_status"] == "RETURN_RECORDED_PROOF_ACCEPTED"
    assert telemetry["latest_worker_lifecycle_event"]["event"] == "worker_terminal"
    assert telemetry["latest_worker_lifecycle_event"]["terminal_state"] == "accepted"
    assert telemetry["worker_lifecycle_events"][0]["event"] == "worker_boot"
    assert telemetry["worker_lifecycle_events"][1]["task_return_packet_path"] == task_return_rel


def test_capsule_status_reads_paths_without_exposing_secret_text(tmp_path):
    _seed_root(tmp_path)
    for rel, text in {
        "ION/05_context/current/codex_solo/CAPSULE.md": "# Capsule\nsecret_token_should_not_leak\n",
        "ION/05_context/current/codex_solo/MINI.md": "mini index\nsecret_token_should_not_leak\n",
        "ION/05_context/current/codex_solo/HOT_CONTEXT.md": "hot context\nsecret_token_should_not_leak\n",
        "ION/05_context/current/codex_capsule_chat/state.json": "{\"lanes\": {\"codex_general\": {\"turns\": [], \"queue_links\": []}}}\n",
    }.items():
        path = tmp_path / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    status = call_chatgpt_connector_tool(tmp_path, "ion_codex_capsule_chat_status", {})

    status_text = json.dumps(status, sort_keys=True)
    assert status["ok"] is True
    assert status["data"]["paths"]["capsule"]["path"] == "ION/05_context/current/codex_solo/CAPSULE.md"
    assert status["data"]["paths"]["mini"]["path"] == "ION/05_context/current/codex_solo/MINI.md"
    assert status["data"]["paths"]["hot_context"]["path"] == "ION/05_context/current/codex_solo/HOT_CONTEXT.md"
    assert "secret_token_should_not_leak" not in status_text


def test_capsule_message_send_writes_bounded_state_and_packet_only(tmp_path):
    _seed_root(tmp_path)

    sent = call_chatgpt_connector_tool(
        tmp_path,
        "ion_codex_capsule_message_send",
        {"message": "Capsule bridge hello", "author": "user"},
    )
    polled = call_chatgpt_connector_tool(
        tmp_path,
        "ion_codex_capsule_message_poll",
        {"lane_id": "codex_general", "limit": 10},
    )

    state_path = tmp_path / "ION/05_context/current/codex_capsule_chat/state.json"
    queue_dir = tmp_path / "ION/05_context/current/chatgpt_connector/codex_work_requests"
    assert sent["ok"] is True
    assert sent["mutates_active_state"] is True
    assert state_path.exists()
    assert "Capsule bridge hello" in state_path.read_text(encoding="utf-8")
    assert (tmp_path / sent["data"]["packet_path"]).exists()
    assert polled["ok"] is True
    assert polled["data"]["message_count"] >= 1
    assert not queue_dir.exists() or not list(queue_dir.glob("*.json"))
