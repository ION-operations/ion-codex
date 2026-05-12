from pathlib import Path

from kernel.ion_chatgpt_browser_mcp_http_preview import (
    BOUNDED_QUEUE_RECEIPT_TOOLS,
    APP_PATHS,
    READY_VERDICT,
    WRITE_CONFIRMATION_TOKEN,
    audit_http_mcp_preview,
    handle_mcp_jsonrpc,
    http_mcp_tool_list,
    render_codex_worker_live_status_html,
    render_helixion_site_bar,
    render_ion_connector_landing,
    render_public_cockpit_login,
    wrap_helixion_site_shell,
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
    assert result["public_cockpit_auth"]["schema_id"] == "ion.public_cockpit_auth_status.v1"


def test_tools_list_exposes_only_v120_contract_tools():
    tools = http_mcp_tool_list()
    names = {tool["name"] for tool in tools}

    assert "ion_status" in names
    assert "ion_carrier_onboarding_packet" in names
    assert "ion_codex_work_queue" in names
    assert "ion_file_read" in names
    assert "ion_tool_manifest" in names
    assert "ion_daemon_status" in names
    assert "ion_codex_worker_live_status" in names
    assert "ion_codex_runner_reconcile" in names
    assert "ion_codex_capsule_chat_status" in names
    assert "ion_codex_capsule_message_send" in names
    assert "ion_codex_capsule_message_poll" in names
    assert "ion_codex_capsule_sync_to_queue" in names
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


def test_worker_live_status_tool_call_exposes_lifecycle_events(tmp_path):
    _seed_root(tmp_path)
    run_rel = "ION/05_context/current/chatgpt_connector/codex_queue_runs/run_lifecycle/run.json"
    run_path = tmp_path / run_rel
    run_path.parent.mkdir(parents=True, exist_ok=True)
    run_path.write_text(
        """
{
  "schema_id": "ion.codex_queue_runner_run.v1",
  "run_id": "run_lifecycle",
  "request_id": "req_lifecycle",
  "request_path": "ION/05_context/current/chatgpt_connector/codex_work_requests/req_lifecycle.json",
  "run_packet_path": "ION/05_context/current/chatgpt_connector/codex_queue_runs/run_lifecycle/run.json",
  "run_dir": "ION/05_context/current/chatgpt_connector/codex_queue_runs/run_lifecycle",
  "status": "RETURN_RECORDED_PROOF_ACCEPTED",
  "started_at": "2026-05-10T17:00:00+00:00",
  "completed_at": "2026-05-10T17:01:00+00:00",
  "submit_result": {
    "accepted_for_carrier_intake": true,
    "context_proof_accepted": true,
    "template_action_proof_accepted": true,
    "packet_path": "ION/05_context/current/chatgpt_connector/task_returns/return_lifecycle.json"
  },
  "worker_lifecycle_events": [
    {
      "event": "worker_boot",
      "at": "2026-05-10T17:00:01+00:00",
      "run_id": "run_lifecycle",
      "request_id": "req_lifecycle",
      "status": "CODEX_CLI_RUNNING",
      "pid": 123,
      "production_authority": false,
      "live_execution_authority": false
    },
    {
      "event": "worker_terminal",
      "at": "2026-05-10T17:01:00+00:00",
      "run_id": "run_lifecycle",
      "request_id": "req_lifecycle",
      "status": "RETURN_RECORDED_PROOF_ACCEPTED",
      "pid": 123,
      "terminal_state": "accepted",
      "context_proof_accepted": true,
      "template_action_proof_accepted": true,
      "production_authority": false,
      "live_execution_authority": false
    }
  ]
}
""".strip()
        + "\n",
        encoding="utf-8",
    )
    state_path = tmp_path / "ION/05_context/current/chatgpt_connector/runtime/codex_queue_runner_state.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(
        f'{{"schema_id":"ion.codex_queue_runner_state.v1","active_run":null,"latest_run":"{run_rel}","production_authority":false,"live_execution_authority":false}}\n',
        encoding="utf-8",
    )

    response = handle_mcp_jsonrpc(
        tmp_path,
        {
            "jsonrpc": "2.0",
            "id": 22,
            "method": "tools/call",
            "params": {"name": "ion_codex_worker_live_status", "arguments": {}},
        },
    )

    telemetry = response["result"]["structuredContent"]["data"]["live_worker_telemetry"]
    assert response["result"]["isError"] is False
    assert telemetry["latest_worker_lifecycle_event"]["event"] == "worker_terminal"
    assert telemetry["worker_lifecycle_events"][0]["event"] == "worker_boot"


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
    assert "https://ion.example.test/cockpit" in html
    assert "https://ion.example.test/cockpit/chat" in html
    assert "https://ion.example.test/cockpit/worker" in html
    assert "https://ion.example.test/app/status.json" in html
    assert "HelixION route directory" in html
    assert "HELIXION" in html
    assert "ION_STATUS_READY" not in html
    assert "production_authority" not in html
    assert "Production authority" in html
    assert "ion_status" in html
    assert "arbitrary_shell" in html
    assert "/home/sev" not in html


def test_connector_landing_paths_include_root_app_and_ion():
    assert {"/", "/app", "/ion"} <= APP_PATHS


def test_codex_worker_live_status_page_is_bounded_polling_ui():
    html = render_codex_worker_live_status_html(Path.cwd(), auth_token="test-token")

    assert "<title>ION Codex Worker</title>" in html
    assert "ion_codex_worker_live_status" in html
    assert "/cockpit/worker/model.json?token=test-token" in html
    assert "/cockpit/chat?token=test-token" in html
    assert "/cockpit?token=test-token" in html
    assert "setInterval(poll, 5000)" in html
    assert "model private reasoning" in html
    assert "raw broad logs" in html
    assert "/home/sev" not in html


def test_helixion_site_bar_marks_active_and_preserves_token():
    html = render_helixion_site_bar("chat", auth_token="abc123")

    assert 'aria-label="HelixION site pages"' in html
    assert 'href="/cockpit/chat?token=abc123"' in html
    assert 'href="/cockpit/worker?token=abc123"' in html
    assert 'aria-current="page"' in html


def test_wrap_helixion_site_shell_adds_bar_to_existing_page():
    html = wrap_helixion_site_shell(
        "<html><head><style>body{}</style></head><body><main>page</main></body></html>",
        "cockpit",
        auth_token="abc123",
    )

    assert "helix-sitebar" in html
    assert 'href="/cockpit?token=abc123"' in html
    assert "body{}" in html
    assert "<main>page</main>" in html


def test_public_cockpit_csp_allows_bundled_chat_script():
    class DummyHandler:
        headers = {}
        sent_headers: dict[str, str] = {}

        def send_response(self, _status):
            return None

        def send_header(self, key, value):
            self.sent_headers[key] = value

        def end_headers(self):
            return None

        @property
        def wfile(self):
            class Writer:
                def write(self, _body):
                    return None

            return Writer()

    handler = DummyHandler()
    from kernel.ion_chatgpt_browser_mcp_http_preview import IonChatGPTPreviewHandler

    IonChatGPTPreviewHandler._send_html(handler, 200, "<html></html>")

    csp = handler.sent_headers["Content-Security-Policy"]
    assert "script-src 'unsafe-inline'" in csp
    assert "connect-src 'self'" in csp


def test_public_cockpit_login_renders_token_and_google_controls():
    html = render_public_cockpit_login(
        next_path="/cockpit/chat",
        env={
            "ION_COCKPIT_PUBLIC_TOKEN": "abc123-private-token",
            "ION_GOOGLE_OAUTH_CLIENT_ID": "client",
            "ION_GOOGLE_OAUTH_CLIENT_SECRET": "secret",
            "ION_COCKPIT_ALLOWED_GOOGLE_EMAILS": "sev@example.com",
        },
    )

    assert "<title>ION Cockpit Login</title>" in html
    assert "/cockpit/auth/token" in html
    assert "/cockpit/auth/google/start" in html
    assert "Continue with Google" in html
    assert "Allowed Google emails: 1" in html
    assert "ION_COCKPIT_ALLOWED_GOOGLE_EMAILS" in html
    assert "abc123-private-token" not in html


def test_public_cockpit_login_explains_google_oauth_setup_gap():
    html = render_public_cockpit_login(
        next_path="/cockpit/chat",
        env={
            "ION_COCKPIT_PUBLIC_TOKEN": "abc123-private-token",
            "ION_COCKPIT_ALLOWED_GOOGLE_EMAILS": "crinkedart@gmail.com",
        },
    )

    assert "Google OAuth setup needed" in html
    assert "Allowed Google emails already listed: 1" in html
    assert "crinkedart@gmail.com" not in html


def test_public_cockpit_login_translates_google_state_error():
    html = render_public_cockpit_login(
        next_path="/cockpit/chat",
        finding="google_oauth_state_missing_or_invalid",
        env={"ION_COCKPIT_PUBLIC_TOKEN": "abc123-private-token"},
    )

    assert "Google login is not enabled yet. Use the permission token for now." in html
    assert "google_oauth_state_missing_or_invalid" not in html
