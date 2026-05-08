from pathlib import Path

from kernel.ion_chatgpt_browser_mcp_http_preview import (
    BOUNDED_QUEUE_RECEIPT_TOOLS,
    APP_PATHS,
    READY_VERDICT,
    WRITE_CONFIRMATION_TOKEN,
    audit_http_mcp_preview,
    handle_mcp_jsonrpc,
    http_mcp_tool_list,
    render_ion_connector_landing,
    write_http_mcp_preview_audit,
)


def _seed_root(root: Path) -> None:
    (root / "pyproject.toml").write_text("[project]\nname = \"ion-test\"\n", encoding="utf-8")
    (root / "ION/REPO_AUTHORITY.md").parent.mkdir(parents=True)
    (root / "ION/REPO_AUTHORITY.md").write_text("# authority\n", encoding="utf-8")


def test_http_preview_audit_ready_on_current_tree():
    result = audit_http_mcp_preview(Path.cwd())

    assert result["schema_id"] == "ion.chatgpt_browser_http_mcp_preview.v1"
    assert result["verdict"] == READY_VERDICT
    assert result["connector_state"] == "LOCAL_HTTP_PREVIEW_NOT_PUBLIC_CONNECTOR"
    assert result["write_confirmation_required"] is True
    assert result["production_authority"] is False
    assert result["live_execution_authority"] is False
    assert result["deployment_authority"] is False


def test_tools_list_exposes_only_v120_contract_tools():
    tools = http_mcp_tool_list()
    names = {tool["name"] for tool in tools}

    assert "ion_status" in names
    assert "ion_carrier_onboarding_packet" in names
    assert "ion_codex_work_queue" in names
    assert "ion_file_read" in names
    assert "ion_tool_manifest" in names
    assert "ion_daemon_status" in names
    assert "ion_codex_queue_process_once" in names
    assert "ion_agent_list" in names
    assert "ion_agent_invoke" in names
    assert "ion_swarm_step_once" in names
    assert "ion_queue_operator_message" in names
    assert "arbitrary_shell" not in names
    for tool in tools:
        if tool["name"] in BOUNDED_QUEUE_RECEIPT_TOOLS:
            assert "confirmation" in tool["inputSchema"]["properties"]
            assert tool["annotations"]["readOnlyHint"] is False
            assert tool["annotations"]["destructiveHint"] is False


def test_jsonrpc_tools_list_shape():
    response = handle_mcp_jsonrpc(Path.cwd(), {"jsonrpc": "2.0", "id": 1, "method": "tools/list"})

    assert response["jsonrpc"] == "2.0"
    assert response["id"] == 1
    assert any(tool["name"] == "ion_status" for tool in response["result"]["tools"])


def test_status_tool_call_works_without_write_confirmation():
    response = handle_mcp_jsonrpc(
        Path.cwd(),
        {"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "ion_status", "arguments": {}}},
    )

    result = response["result"]
    assert result["isError"] is False
    assert result["structuredContent"]["ok"] is True
    assert result["structuredContent"]["data"]["schema_id"] == "ion.status.v1"


def test_read_tool_call_works_without_write_confirmation(tmp_path):
    _seed_root(tmp_path)
    target = tmp_path / "ION/02_architecture/NOTE.md"
    target.parent.mkdir(parents=True)
    target.write_text("browser read smoke\n", encoding="utf-8")
    response = handle_mcp_jsonrpc(
        tmp_path,
        {
            "jsonrpc": "2.0",
            "id": 21,
            "method": "tools/call",
            "params": {"name": "ion_file_read", "arguments": {"path": "ION/02_architecture/NOTE.md"}},
        },
    )

    result = response["result"]
    assert result["isError"] is False
    assert result["structuredContent"]["ok"] is True
    assert "browser read smoke" in result["structuredContent"]["data"]["text"]


def test_carrier_onboarding_tool_call_works_without_write_confirmation():
    response = handle_mcp_jsonrpc(
        Path.cwd(),
        {
            "jsonrpc": "2.0",
            "id": 20,
            "method": "tools/call",
            "params": {"name": "ion_carrier_onboarding_packet", "arguments": {"carrier": "chatgpt_browser"}},
        },
    )

    result = response["result"]
    assert result["isError"] is False
    assert result["structuredContent"]["ok"] is True
    assert result["structuredContent"]["data"]["schema_id"] == "ion.carrier_onboarding_packet.v1"
    assert result["structuredContent"]["data"]["root_markdown_onboarding_authority"] is False


def test_bounded_write_tool_requires_confirmation(tmp_path):
    _seed_root(tmp_path)
    response = handle_mcp_jsonrpc(
        tmp_path,
        {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {"name": "ion_queue_operator_message", "arguments": {"message": "queue without confirmation"}},
        },
    )

    result = response["result"]
    assert result["isError"] is True
    assert result["structuredContent"]["finding"] == "bounded_write_confirmation_required"
    assert not (tmp_path / "ION/05_context/current/ACTIVE_OPERATOR_MESSAGE_QUEUE.json").exists()


def test_bounded_write_tool_with_confirmation_writes_only_queue(tmp_path):
    _seed_root(tmp_path)
    response = handle_mcp_jsonrpc(
        tmp_path,
        {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "ion_queue_operator_message",
                "arguments": {
                    "message": "queue with confirmation",
                    "priority": 60,
                    "confirmation": WRITE_CONFIRMATION_TOKEN,
                },
            },
        },
    )

    queue = tmp_path / "ION/05_context/current/ACTIVE_OPERATOR_MESSAGE_QUEUE.json"
    result = response["result"]
    assert result["isError"] is False
    assert result["structuredContent"]["ok"] is True
    assert queue.exists()
    assert "queue with confirmation" in queue.read_text(encoding="utf-8")


def test_forbidden_tool_is_blocked_even_with_confirmation():
    response = handle_mcp_jsonrpc(
        Path.cwd(),
        {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {"name": "arbitrary_shell", "arguments": {"confirmation": WRITE_CONFIRMATION_TOKEN}},
        },
    )

    result = response["result"]
    assert result["isError"] is True
    assert result["structuredContent"]["finding"] == "forbidden_capability"


def test_write_http_preview_audit(tmp_path):
    output = tmp_path / "CHATGPT_BROWSER_HTTP_MCP_PREVIEW_V121.json"

    result = write_http_mcp_preview_audit(Path.cwd(), output=output)

    assert output.exists()
    assert result["verdict"] == READY_VERDICT
    assert result["write_confirmation_required"] is True


def test_connector_landing_page_is_safe_human_ui():
    html = render_ion_connector_landing(Path.cwd(), public_base_url="https://ion.example.test")

    assert "<title>ION Connector</title>" in html
    assert "https://ion.example.test/mcp" in html
    assert "ION_STATUS_READY" not in html
    assert "production_authority" not in html
    assert "Production authority" in html
    assert "ion_status" in html
    assert "arbitrary_shell" in html
    assert "/home/sev" not in html


def test_connector_landing_paths_include_root_app_and_ion():
    assert {"/", "/app", "/ion"} <= APP_PATHS
