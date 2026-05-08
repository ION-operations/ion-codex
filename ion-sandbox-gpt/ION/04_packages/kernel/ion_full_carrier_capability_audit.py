"""Audit full-carrier MCP parity scaffolding without granting live authority."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .ion_carrier_onboard import resolve_shell_root_from_ion_root
from .ion_chatgpt_browser_mcp_connector_contract import audit_chatgpt_browser_mcp_connector_contract

SCHEMA_ID = "ion.full_carrier_capability_audit.v1"
READY_VERDICT = "ION_FULL_CARRIER_CAPABILITY_AUDIT_READY"
BLOCKED_VERDICT = "ION_FULL_CARRIER_CAPABILITY_AUDIT_BLOCKED"

REQUIRED_OWNER_PATHS = {
    "parity_protocol": "ION/02_architecture/ION_FULL_CARRIER_MCP_PARITY_PROTOCOL.md",
    "carrier_comms_protocol": "ION/02_architecture/ION_CARRIER_TO_CARRIER_COMMUNICATION_PROTOCOL.md",
    "capability_registry": "ION/03_registry/carrier_capability_registry.yaml",
    "mcp_tool_registry": "ION/03_registry/mcp_full_carrier_tool_registry.yaml",
    "connector_policy": "ION/03_registry/ion_chatgpt_browser_mcp_tool_policy.yaml",
    "full_mount_template": "ION/07_templates/carriers/FULL_CARRIER_MOUNT_PROOF.md",
    "action_receipt_template": "ION/07_templates/actions/FULL_CARRIER_ACTION_RECEIPT.md",
    "connector_contract": "ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py",
    "http_preview": "ION/04_packages/kernel/ion_chatgpt_browser_mcp_http_preview.py",
    "codex_queue_runner": "ION/04_packages/kernel/ion_codex_queue_runner.py",
    "agent_invocation_broker": "ION/04_packages/kernel/ion_agent_invocation_broker.py",
}

FIRST_FULL_CARRIER_TOOLS = {
    "ion_file_put_text",
    "ion_artifact_upload_init",
    "ion_artifact_upload_chunk",
    "ion_artifact_upload_commit",
    "ion_carrier_message_send",
    "ion_carrier_message_poll",
    "ion_carrier_message_ack",
}

BOUNDED_PROJECT_VISIBILITY_TOOLS = {
    "ion_file_read",
    "ion_file_search",
    "ion_tree_list",
    "ion_registry_read",
    "ion_template_read",
    "ion_context_compile",
    "ion_receipt_hydrate",
    "ion_tool_manifest",
}

CODEX_QUEUE_AUTOMATION_TOOLS = {
    "ion_daemon_status",
    "ion_codex_queue_autorun_status",
    "ion_codex_queue_process_once",
}

AGENT_INVOCATION_BROKER_TOOLS = {
    "ion_agent_list",
    "ion_agent_status",
    "ion_agent_result",
    "ion_agent_queue",
    "ion_agent_spawn_plan",
    "ion_swarm_status",
    "ion_agent_invoke",
    "ion_agent_cancel",
    "ion_swarm_step_once",
}

FAILURE_CLASSES = [
    "ION_CORE_FAILURE",
    "CARRIER_ADAPTER_FAILURE",
    "CODEX_CLI_FAILURE",
    "BACKEND_CODEX_FAILURE",
    "DAEMON_FAILURE",
    "AGENT_INVOCATION_FAILURE",
    "TRANSPORT_FAILURE",
    "AUTH_OR_CONFIRMATION_FAILURE",
    "CAPABILITY_NOT_YET_IMPLEMENTED",
    "POLICY_BLOCK_WORKING_AS_DESIGNED",
]


def _resolve_root(root: str | Path | None) -> Path:
    candidate = Path(root or ".").expanduser().resolve()
    for path in (candidate, *candidate.parents):
        if (path / "pyproject.toml").exists() and (path / "ION/REPO_AUTHORITY.md").exists():
            return path
    return resolve_shell_root_from_ion_root(root)


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def audit_full_carrier_capability(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    findings: list[str] = []
    owner_paths: dict[str, dict[str, Any]] = {}
    for label, rel in REQUIRED_OWNER_PATHS.items():
        path = shell_root / rel
        owner_paths[label] = {"path": rel, "exists": path.exists()}
        if not path.exists():
            findings.append(f"missing_owner_surface:{label}:{rel}")

    connector = audit_chatgpt_browser_mcp_connector_contract(shell_root)
    exposed_tools = set(connector.get("allowed_tools") or [])
    missing_first_tools = sorted(FIRST_FULL_CARRIER_TOOLS - exposed_tools)
    if missing_first_tools:
        findings.append(f"missing_first_full_carrier_tools:{','.join(missing_first_tools)}")
    missing_visibility_tools = sorted(BOUNDED_PROJECT_VISIBILITY_TOOLS - exposed_tools)
    if missing_visibility_tools:
        findings.append(f"missing_bounded_project_visibility_tools:{','.join(missing_visibility_tools)}")
    missing_automation_tools = sorted(CODEX_QUEUE_AUTOMATION_TOOLS - exposed_tools)
    if missing_automation_tools:
        findings.append(f"missing_codex_queue_automation_tools:{','.join(missing_automation_tools)}")
    missing_agent_tools = sorted(AGENT_INVOCATION_BROKER_TOOLS - exposed_tools)
    if missing_agent_tools:
        findings.append(f"missing_agent_invocation_broker_tools:{','.join(missing_agent_tools)}")

    parity_text = _read_text(shell_root / REQUIRED_OWNER_PATHS["parity_protocol"]) if owner_paths["parity_protocol"]["exists"] else ""
    required_phrases = [
        "ION has one core engine",
        "ChatGPT browser should be treated as a full ION carrier target",
        "Carrier Adapter Failure Is Not ION Core Failure",
        "File And Artifact Transfer From ChatGPT Browser",
        "Carrier-To-Carrier Communications",
        "No-Silent-Loss",
        "Bounded project visibility MCP slice",
        "Codex Queue Automation MCP slice",
        "Agent Invocation Broker MCP slice",
    ]
    for phrase in required_phrases:
        if phrase not in parity_text:
            findings.append(f"parity_protocol_missing_phrase:{phrase}")

    ready = not findings and bool(connector.get("accepted"))
    adapter_gaps = [
        {
            "capability_class": "command_test_process_git",
            "classification": "CAPABILITY_NOT_YET_IMPLEMENTED",
            "adapter": "CHATGPT_BROWSER_CARRIER",
            "ion_core_failure": False,
            "note": "No direct shell/git/process MCP tool is exposed in this staging slice.",
        }
    ]
    return {
        "schema_id": SCHEMA_ID,
        "verdict": READY_VERDICT if ready else BLOCKED_VERDICT,
        "accepted": ready,
        "root": str(shell_root),
        "owner_paths": owner_paths,
        "connector_contract_verdict": connector.get("verdict"),
        "first_full_carrier_tools": sorted(FIRST_FULL_CARRIER_TOOLS),
        "exposed_first_full_carrier_tools": sorted(FIRST_FULL_CARRIER_TOOLS & exposed_tools),
        "missing_first_full_carrier_tools": missing_first_tools,
        "bounded_project_visibility_tools": sorted(BOUNDED_PROJECT_VISIBILITY_TOOLS),
        "exposed_bounded_project_visibility_tools": sorted(BOUNDED_PROJECT_VISIBILITY_TOOLS & exposed_tools),
        "missing_bounded_project_visibility_tools": missing_visibility_tools,
        "codex_queue_automation_tools": sorted(CODEX_QUEUE_AUTOMATION_TOOLS),
        "exposed_codex_queue_automation_tools": sorted(CODEX_QUEUE_AUTOMATION_TOOLS & exposed_tools),
        "missing_codex_queue_automation_tools": missing_automation_tools,
        "agent_invocation_broker_tools": sorted(AGENT_INVOCATION_BROKER_TOOLS),
        "exposed_agent_invocation_broker_tools": sorted(AGENT_INVOCATION_BROKER_TOOLS & exposed_tools),
        "missing_agent_invocation_broker_tools": missing_agent_tools,
        "failure_classes": FAILURE_CLASSES,
        "adapter_gaps": adapter_gaps,
        "findings": findings,
        "production_authority": False,
        "live_execution_authority": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit ION full-carrier MCP parity scaffolding.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = audit_full_carrier_capability(args.ion_root)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["verdict"])
        for finding in result["findings"]:
            print(f"- {finding}")
    return 0 if result["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
