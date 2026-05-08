import json
from pathlib import Path

from kernel.ion_agent_invocation_broker import (
    agent_queue,
    agent_result,
    build_agent_broker_status,
    build_agent_spawn_plan,
    cancel_agent_invocation,
    invoke_agent,
    list_agents,
    swarm_step_once,
)
from kernel.ion_codex_queue_runner import build_codex_queue_runner_status


def _seed_root(root: Path) -> None:
    (root / "pyproject.toml").write_text("[project]\nname = \"ion-test\"\n", encoding="utf-8")
    (root / "ION/REPO_AUTHORITY.md").parent.mkdir(parents=True)
    (root / "ION/REPO_AUTHORITY.md").write_text("# authority\n", encoding="utf-8")
    (root / "ION/05_context/current/chatgpt_connector/codex_work_requests").mkdir(parents=True, exist_ok=True)
    (root / "ION/05_context/current/chatgpt_connector/task_returns").mkdir(parents=True, exist_ok=True)
    for rel in [
        "ION/03_registry/codex_cli_carrier_profile.yaml",
        "ION/07_templates/carriers/CODEX_CLI_EXECUTION_PACKET.md",
        "ION/02_architecture/ION_FULL_CARRIER_MCP_PARITY_PROTOCOL.md",
        "ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py",
        "ION/04_packages/kernel/ion_codex_queue_runner.py",
        "ION/04_packages/kernel/ion_agent_invocation_broker.py",
    ]:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"{rel}\n", encoding="utf-8")
    (root / "ION/03_registry/agent_context_system_registry.yaml").write_text(
        "\n".join([
            "registry_id: ion.agent_context_system_registry.v1",
            "agents:",
            "  - role_id: role.mason",
            "    display_name: MASON",
            "    context_system_card: ION/05_context/current/agent_context_systems/MASON.context_system.md",
            "    base_sources:",
            "      - ION/03_registry/boots/MASON.boot.md",
            "    primary_templates:",
            "      - ION/07_templates/bindings/MASON__CODE.md",
            "context_specialists:",
            "  - role_id: role.template_curator",
            "    context_system_card: ION/05_context/current/agent_context_systems/TEMPLATE_CURATOR.context_system.md",
            "  - role_id: role.context_cartographer",
            "    context_system_card: ION/05_context/current/agent_context_systems/CONTEXT_CARTOGRAPHER.context_system.md",
            "",
        ]),
        encoding="utf-8",
    )
    (root / "ION/03_registry/agent_roster_registry.yaml").write_text(
        "\n".join([
            "registry_id: current_phase.agent_roster_registry",
            "roster_records:",
            "  - entity_id: role.mason",
            "    display_name: Mason",
            "    live_status: ACTIVE_CURRENT_PHASE",
            "    template_bindings:",
            "      - ION/07_templates/bindings/MASON__CODE.md",
            "    source_refs:",
            "      - ION/03_registry/boots/MASON.boot.md",
            "",
        ]),
        encoding="utf-8",
    )
    for rel in [
        "ION/05_context/current/agent_context_systems/MASON.context_system.md",
        "ION/05_context/current/agent_context_systems/TEMPLATE_CURATOR.context_system.md",
        "ION/05_context/current/agent_context_systems/CONTEXT_CARTOGRAPHER.context_system.md",
        "ION/03_registry/boots/MASON.boot.md",
        "ION/07_templates/bindings/MASON__CODE.md",
    ]:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# {Path(rel).stem}\n", encoding="utf-8")


def test_agent_broker_lists_roster_and_context_specialists(tmp_path):
    _seed_root(tmp_path)

    result = list_agents(tmp_path)
    role_ids = {agent["role_id"] for agent in result["agents"]}

    assert result["schema_id"] == "ion.agent_invocation_broker_agent_list.v1"
    assert "role.mason" in role_ids
    assert "role.template_curator" in role_ids
    assert "role.context_cartographer" in role_ids
    assert all(agent["backend_carrier_id"] == "CODEX_CLI_CARRIER" for agent in result["agents"])


def test_agent_invoke_prepare_only_writes_invocation_and_nonqueued_work_request(tmp_path):
    _seed_root(tmp_path)

    result = invoke_agent(tmp_path, agent="MASON", objective="prepare broker smoke", queue=False)

    assert result["ok"] is True
    assert result["queued_for_codex_carrier"] is False
    invocation_path = tmp_path / result["invocation_path"]
    work_path = tmp_path / result["codex_work_request_path"]
    assert invocation_path.exists()
    assert work_path.exists()
    work = json.loads(work_path.read_text(encoding="utf-8"))
    assert work["status"] == "PREPARED_FOR_CODEX_CARRIER_NOT_QUEUED"
    assert work["agent_role_id"] == "role.mason"
    assert "ION has one core engine" in work["objective"]
    assert build_codex_queue_runner_status(tmp_path)["queued_request_count"] == 0


def test_agent_invoke_queue_and_swarm_step_prepare_existing_runner_packet(tmp_path):
    _seed_root(tmp_path)
    invoked = invoke_agent(tmp_path, agent="template_curator", objective="queued broker smoke", queue=True)

    result = swarm_step_once(tmp_path, start=False)

    assert invoked["ok"] is True
    assert result["ok"] is True
    assert result["backend_result"]["ok"] is True
    assert result["backend_result"]["prepared_only"] is True
    run = result["backend_result"]["run"]
    receipt = json.loads((tmp_path / run["context_receipt_path"]).read_text(encoding="utf-8"))
    required_paths = [item["path"] for item in receipt["required_context_reads"]]
    assert invoked["invocation_path"] in required_paths
    assert "ION/05_context/current/agent_context_systems/TEMPLATE_CURATOR.context_system.md" in required_paths


def test_agent_status_result_queue_cancel_and_spawn_plan(tmp_path):
    _seed_root(tmp_path)
    invoked = invoke_agent(tmp_path, agent="context_cartographer", objective="status smoke", queue=True)
    invocation_id = invoked["invocation"]["invocation_id"]

    status = build_agent_broker_status(tmp_path)
    queue = agent_queue(tmp_path)
    result = agent_result(tmp_path, invocation_id=invocation_id)
    spawn_plan = build_agent_spawn_plan(tmp_path, objective="status smoke")
    cancelled = cancel_agent_invocation(tmp_path, invocation_id=invocation_id)

    assert status["accepted"] is True
    assert status["queued_agent_codex_work_request_count"] == 1
    assert queue["invocation_count"] == 1
    assert result["ok"] is True
    assert spawn_plan["no_parallel_agent_system_created"] is True
    assert cancelled["ok"] is True
    assert json.loads((tmp_path / invoked["codex_work_request_path"]).read_text(encoding="utf-8"))["status"] == "CANCELLED_BY_AGENT_INVOCATION_BROKER"


def test_agent_cancel_rejects_completed_invocation(tmp_path):
    _seed_root(tmp_path)
    invoked = invoke_agent(tmp_path, agent="MASON", objective="completed cancel smoke", queue=True)
    invocation_path = tmp_path / invoked["invocation_path"]
    work_path = tmp_path / invoked["codex_work_request_path"]
    invocation = json.loads(invocation_path.read_text(encoding="utf-8"))
    work = json.loads(work_path.read_text(encoding="utf-8"))
    invocation["status"] = "RETURN_RECORDED_PROOF_ACCEPTED"
    work["status"] = "RETURN_RECORDED_PROOF_ACCEPTED"
    invocation_path.write_text(json.dumps(invocation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    work_path.write_text(json.dumps(work, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    cancelled = cancel_agent_invocation(tmp_path, invocation_id=invoked["invocation"]["invocation_id"])

    assert cancelled["ok"] is False
    assert cancelled["finding"] == "can_cancel_only_prepared_or_queued_invocations"
    assert json.loads(work_path.read_text(encoding="utf-8"))["status"] == "RETURN_RECORDED_PROOF_ACCEPTED"


def test_swarm_step_rejects_non_agent_or_nonqueued_request_path(tmp_path):
    _seed_root(tmp_path)
    non_agent_path = tmp_path / "ION/05_context/current/chatgpt_connector/codex_work_requests/non_agent.json"
    non_agent_path.write_text(
        json.dumps(
            {
                "schema_id": "ion.chatgpt_browser_connector_codex_work_request.v1",
                "request_id": "codex_req_non_agent",
                "objective": "ordinary queued work",
                "status": "QUEUED_FOR_CODEX_CARRIER",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    prepared = invoke_agent(tmp_path, agent="MASON", objective="prepared only smoke", queue=False)

    non_agent = swarm_step_once(
        tmp_path,
        request_path="ION/05_context/current/chatgpt_connector/codex_work_requests/non_agent.json",
        start=False,
    )
    nonqueued = swarm_step_once(tmp_path, request_path=prepared["codex_work_request_path"], start=False)

    assert non_agent["ok"] is False
    assert non_agent["finding"] == "request_path_is_not_agent_invocation_work"
    assert nonqueued["ok"] is False
    assert nonqueued["finding"] == "agent_invocation_work_request_not_queued"
