import json
from pathlib import Path

from kernel.ion_chatgpt_browser_mcp_http_preview import (
    WRITE_CONFIRMATION_TOKEN,
    handle_mcp_jsonrpc,
)


def _write(root: Path, rel: str, text: str = "surface\n") -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _seed_connector_root(root: Path) -> None:
    _write(root, "pyproject.toml", "[project]\nname = \"ion-test\"\n")
    _write(root, "ION/REPO_AUTHORITY.md", "# authority\n")
    (root / "ION/04_packages/kernel").mkdir(parents=True, exist_ok=True)
    (root / "ION/03_registry/boots").mkdir(parents=True, exist_ok=True)
    _write(root, "ION/docs/setup/ION_CURRENT_OPERATING_PACKET_V119.md", "# ION Current Operating Packet\n")
    _write(root, "ION/02_architecture/ION_MOUNT_CONTRACT.md", "# mount contract\n")
    _write(root, "ION/03_registry/chatgpt_browser_carrier_profile.yaml", "carrier_id: CHATGPT_BROWSER_CARRIER\n")
    _write(root, "ION/03_registry/boots/RELAY.boot.md")
    _write(root, "ION/03_registry/boots/STEWARD.boot.md")
    _write(root, "ION/05_context/current/agent_context_systems/RELAY.context_system.md")
    _write(root, "ION/05_context/current/agent_context_systems/STEWARD.context_system.md")
    _write(root, "ION/05_context/current/execution_cycles/2026-test/01_COMPILED_STEWARD_CONTEXT_BUNDLE.md")
    _write(root, "ION/05_context/current/ACTIVE_WORK_PACKET.json", "{}\n")
    _write(root, "ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json", "{}\n")
    _write(root, "ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json", "{}\n")
    _write(root, "ION/07_templates/carriers/CARRIER_MOUNT_PROOF.md")
    _write(root, "ION/07_templates/carriers/CARRIER_SESSION_PACKET.md")
    _write(root, "ION/07_templates/carriers/CHATGPT_BROWSER_CONNECTOR_SESSION_PACKET.md")


def _call(root: Path, msg_id: int, name: str, arguments: dict):
    response = handle_mcp_jsonrpc(
        root,
        {
            "jsonrpc": "2.0",
            "id": msg_id,
            "method": "tools/call",
            "params": {"name": name, "arguments": arguments},
        },
    )
    return response["result"]["structuredContent"]


def test_chatgpt_browser_connector_complete_bounded_codex_work_loop(tmp_path):
    _seed_connector_root(tmp_path)

    onboarding = _call(tmp_path, 1, "ion_carrier_onboarding_packet", {"carrier": "chatgpt_browser"})
    status = _call(tmp_path, 2, "ion_status", {})

    assert onboarding["ok"] is True
    assert onboarding["data"]["onboarding_verdict"] == "ION_CARRIER_ONBOARDING_PACKET_READY"
    assert onboarding["data"]["carrier_profile"]["path"] == "ION/03_registry/chatgpt_browser_carrier_profile.yaml"
    assert onboarding["data"]["mount_contract"]["path"] == "ION/02_architecture/ION_MOUNT_CONTRACT.md"
    assert onboarding["data"]["root_markdown_onboarding_authority"] is False
    assert status["ok"] is True
    assert status["data"]["schema_id"] == "ion.status.v1"

    queued = _call(
        tmp_path,
        3,
        "ion_request_codex_work_packet",
        {
            "objective": "E2E connector queue and return proof",
            "confirmation": WRITE_CONFIRMATION_TOKEN,
            "request_kind": "codex_chat_response",
            "ion_skill_activation": {"skill_id": "codex-chat-answer", "display_name": "Codex Chat Answer"},
            "ion_chat_engine_turn": {"response_mode": "answer", "carrier_strategy": {"mode": "gpt_5_5_codex_chat_response_contract"}},
        },
    )

    assert queued["ok"] is True
    request_path = queued["data"]["packet_path"]
    request_id = queued["data"]["request_id"]
    assert (tmp_path / request_path).exists()
    request_packet = json.loads((tmp_path / request_path).read_text(encoding="utf-8"))
    assert request_packet["request_kind"] == "codex_chat_response"
    assert request_packet["ion_skill_activation"]["skill_id"] == "codex-chat-answer"
    assert request_packet["ion_chat_engine_turn"]["response_mode"] == "answer"
    assert (tmp_path / "ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json").exists()

    queue = _call(tmp_path, 4, "ion_codex_work_queue", {"limit": 10})
    local_queue = _call(tmp_path, 5, "ion_read_active_packet", {"packet": "chatgpt_codex_work_queue"})

    assert queue["ok"] is True
    assert queue["data"]["request_count"] == 1
    assert queue["data"]["requests"][0]["request_id"] == request_id
    assert queue["data"]["requests"][0]["status"] == "QUEUED_FOR_CODEX_CARRIER"
    assert local_queue["ok"] is True
    assert local_queue["data"]["path"] == "ION/05_context/current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json"

    receipt = {
        "schema_id": "ion.context_load_receipt.v1",
        "required_context_reads": [
            {"kind": "file", "path": "ION/REPO_AUTHORITY.md", "required": True}
        ],
    }
    task_return = """### CONTEXT PROOF
- ION/REPO_AUTHORITY.md excerpt: authority line read.

### TEMPLATE ACTION PROOF
template_id: ion.template.patch_proposal.v1
action_id: e2e-chatgpt-connector-return
result: validated bounded connector return flow
touched_paths:
  - ION/05_context/current/chatgpt_connector/codex_work_requests/request.json

### RESULT
Codex returned bounded proof for the queued connector request.
"""
    returned = _call(
        tmp_path,
        6,
        "ion_submit_task_return",
        {
            "task_output_text": task_return,
            "context_receipt": receipt,
            "work_request_path": request_path,
            "confirmation": WRITE_CONFIRMATION_TOKEN,
        },
    )

    assert returned["ok"] is True
    assert returned["data"]["accepted_for_carrier_intake"] is True
    assert returned["data"]["work_request_updated"] is True
    assert (tmp_path / returned["data"]["packet_path"]).exists()

    queue_after = _call(tmp_path, 7, "ion_codex_work_queue", {"limit": 10})
    receipt_state = _call(tmp_path, 8, "ion_receipt_search", {"query": request_id, "limit": 10})
    forbidden = _call(
        tmp_path,
        9,
        "arbitrary_shell",
        {"cmd": "echo nope", "confirmation": WRITE_CONFIRMATION_TOKEN},
    )

    assert queue_after["ok"] is True
    assert queue_after["data"]["requests"][0]["status"] == "RETURN_RECORDED_PROOF_ACCEPTED"
    assert queue_after["data"]["requests"][0]["linked_return_count"] == 1
    assert queue_after["data"]["requests"][0]["accepted_return_count"] == 1
    assert receipt_state["ok"] is True
    assert any("task_returns" in match["path"] for match in receipt_state["data"]["matches"])
    assert forbidden["ok"] is False
    assert forbidden["finding"] == "forbidden_capability"


def test_task_return_rejects_unbounded_work_request_path(tmp_path):
    _seed_connector_root(tmp_path)
    receipt = {
        "schema_id": "ion.context_load_receipt.v1",
        "required_context_reads": [
            {"kind": "file", "path": "ION/REPO_AUTHORITY.md", "required": True}
        ],
    }

    returned = _call(
        tmp_path,
        10,
        "ion_submit_task_return",
        {
            "task_output_text": "### CONTEXT PROOF\n- ION/REPO_AUTHORITY.md excerpt: authority line read.\n\n### TEMPLATE ACTION PROOF\nproof\n\n### RESULT\nblocked\n",
            "context_receipt": receipt,
            "work_request_path": "ION/REPO_AUTHORITY.md",
            "confirmation": WRITE_CONFIRMATION_TOKEN,
        },
    )

    assert returned["ok"] is False
    assert returned["finding"] == "work_request_path_not_bounded_to_codex_work_requests"
