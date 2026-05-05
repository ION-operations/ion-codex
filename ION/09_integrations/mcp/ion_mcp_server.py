#!/usr/bin/env python3
"""ION MCP Control Bridge.

A minimal stdio MCP server that exposes bounded ION kernel commands to Cursor.
It intentionally does not expose arbitrary shell access.
"""
from __future__ import annotations

import argparse
import json
import os
import pathlib
import subprocess
import sys
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple

SERVER_NAME = "ion-control"
SERVER_VERSION = "0.1.0-v92"
PROTOCOL_VERSION = "2024-11-05"

ACTIVE_PACKET_ALLOWLIST = {
    "hook": "ION/05_context/current/ACTIVE_CURSOR_HOOK_STATE.json",
    "work": "ION/05_context/current/ACTIVE_WORK_PACKET.json",
    "spawn_plan": "ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json",
    "carrier_turn": "ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json",
    "task_return_ledger": "ION/05_context/current/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json",
    "steward_queue": "ION/05_context/current/ACTIVE_STEWARD_INTEGRATION_QUEUE.json",
    "operator_queue": "ION/05_context/current/ACTIVE_OPERATOR_MESSAGE_QUEUE.json",
    "human_gates": "ION/05_context/current/ACTIVE_HUMAN_GATE_QUEUE.json",
    "cockpit": "ION/05_context/current/ACTIVE_COCKPIT_VIEW_MODEL.json",
    "context_window": "ION/05_context/current/ACTIVE_AGENT_CONTEXT_WINDOW_PLAN.json",
    "front_door": "ION/05_context/current/ACTIVE_FRONT_DOOR_TEAM_PLAN.json",
}

@dataclass
class IonResult:
    ok: bool
    text: str
    data: Any = None


def _json_text(data: Any) -> str:
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)


def _find_root(candidate: str | pathlib.Path) -> pathlib.Path:
    root = pathlib.Path(candidate).expanduser().resolve()
    if (root / "ION" / "REPO_AUTHORITY.md").exists() and (root / "pyproject.toml").exists():
        return root
    # Some update/package roots may not contain pyproject during isolated tests; accept ION directory only.
    if (root / "ION").exists():
        return root
    raise RuntimeError(f"Not an ION shell root: {root}")


def _env(root: pathlib.Path) -> Dict[str, str]:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    ion_packages = str(root / "ION" / "04_packages")
    old = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = ion_packages if not old else ion_packages + os.pathsep + old
    return env


def _run_kernel(root: pathlib.Path, module: str, args: List[str], timeout_s: int = 120) -> IonResult:
    cmd = [sys.executable or "python3", "-S", "-m", module, *args]
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(root),
            env=_env(root),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_s,
        )
    except subprocess.TimeoutExpired as exc:
        return IonResult(False, f"ION kernel command timed out: {' '.join(cmd)}\n{exc}")
    except Exception as exc:  # pragma: no cover - defensive
        return IonResult(False, f"ION kernel command failed to launch: {' '.join(cmd)}\n{exc}")

    out = proc.stdout.strip()
    err = proc.stderr.strip()
    combined = out if not err else out + "\n\n[stderr]\n" + err
    data: Any = None
    if out:
        try:
            data = json.loads(out)
        except Exception:
            data = None
    if proc.returncode != 0:
        return IonResult(False, combined or f"Command exited {proc.returncode}", data)
    return IonResult(True, combined or "OK", data)


def tool_ion_status(root: pathlib.Path, args: Dict[str, Any]) -> IonResult:
    cmd = ["--ion-root", ".", "--json"]
    return _run_kernel(root, "kernel.ion_status", cmd)


def tool_ion_continue(root: pathlib.Path, args: Dict[str, Any]) -> IonResult:
    message = str(args.get("operator_message") or "continue")
    cmd = ["--ion-root", ".", "--carrier", "cursor", "--operator-message", message, "--json"]
    if bool(args.get("consume_operator_queue")):
        cmd.append("--consume-operator-queue")
    return _run_kernel(root, "kernel.ion_carrier_continue", cmd)


def tool_ion_context_plan(root: pathlib.Path, args: Dict[str, Any]) -> IonResult:
    message = str(args.get("operator_message") or "continue")
    cmd = ["--ion-root", ".", "--operator-message", message, "--write", "--json"]
    return _run_kernel(root, "kernel.ion_agent_context_dynamics", cmd)


def tool_ion_cockpit_view(root: pathlib.Path, args: Dict[str, Any]) -> IonResult:
    cmd = ["--ion-root", ".", "--json"]
    if bool(args.get("write", True)):
        cmd.append("--write")
    return _run_kernel(root, "kernel.ion_cockpit_view_model", cmd)


def tool_ion_workflow_audit(root: pathlib.Path, args: Dict[str, Any]) -> IonResult:
    return _run_kernel(root, "kernel.ion_carrier_workflow_audit", ["--ion-root", ".", "--json"])


def tool_ion_task_return(root: pathlib.Path, args: Dict[str, Any]) -> IonResult:
    role = str(args.get("role") or "").strip()
    index = str(args.get("index") or "").strip()
    task_output = str(args.get("task_output_path") or "").strip()
    if not role or not index or not task_output:
        return IonResult(False, "role, index, and task_output_path are required")
    output_path = pathlib.Path(task_output)
    if output_path.is_absolute():
        try:
            output_path.relative_to(root)
        except ValueError:
            return IonResult(False, "task_output_path must be inside the ION workspace")
    cmd = ["--ion-root", ".", "--role", role, "--index", index, "--task-output", task_output, "--json"]
    return _run_kernel(root, "kernel.ion_carrier_task_return", cmd)


def tool_ion_read_active_packet(root: pathlib.Path, args: Dict[str, Any]) -> IonResult:
    packet = str(args.get("packet") or "").strip()
    rel = ACTIVE_PACKET_ALLOWLIST.get(packet)
    if not rel:
        return IonResult(False, f"Unknown packet '{packet}'. Allowed: {', '.join(sorted(ACTIVE_PACKET_ALLOWLIST))}")
    path = root / rel
    if not path.exists():
        return IonResult(False, f"Packet not found: {rel}")
    text = path.read_text(encoding="utf-8")
    try:
        data = json.loads(text)
        return IonResult(True, _json_text({"path": rel, "json": data}), {"path": rel, "json": data})
    except Exception:
        return IonResult(True, text, {"path": rel, "text": text})


TOOLS = {
    "ion_status": {
        "description": "Read unified ION runtime status from active packets.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
        "handler": tool_ion_status,
    },
    "ion_continue": {
        "description": "Run ION carrier continuation for Cursor and refresh active work/spawn/turn packets.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "operator_message": {"type": "string", "default": "continue"},
                "consume_operator_queue": {"type": "boolean", "default": False},
            },
            "additionalProperties": False,
        },
        "handler": tool_ion_continue,
    },
    "ion_context_plan": {
        "description": "Emit the dynamic agent context-window plan and front-door team plan.",
        "inputSchema": {
            "type": "object",
            "properties": {"operator_message": {"type": "string", "default": "continue"}},
            "additionalProperties": False,
        },
        "handler": tool_ion_context_plan,
    },
    "ion_cockpit_view": {
        "description": "Build the ION cockpit runtime view model from active packets.",
        "inputSchema": {
            "type": "object",
            "properties": {"write": {"type": "boolean", "default": True}},
            "additionalProperties": False,
        },
        "handler": tool_ion_cockpit_view,
    },
    "ion_workflow_audit": {
        "description": "Audit the carrier-control workflow surfaces and packet bindings.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
        "handler": tool_ion_workflow_audit,
    },
    "ion_read_active_packet": {
        "description": "Read one whitelisted active ION packet by name.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "packet": {
                    "type": "string",
                    "enum": sorted(ACTIVE_PACKET_ALLOWLIST.keys()),
                }
            },
            "required": ["packet"],
            "additionalProperties": False,
        },
        "handler": tool_ion_read_active_packet,
    },
    "ion_task_return": {
        "description": "Run proof-gated intake for a captured Cursor Task return file.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "role": {"type": "string"},
                "index": {"type": "integer"},
                "task_output_path": {"type": "string"},
            },
            "required": ["role", "index", "task_output_path"],
            "additionalProperties": False,
        },
        "handler": tool_ion_task_return,
    },
}


class MCPServer:
    def __init__(self, root: pathlib.Path):
        self.root = root

    def tool_list(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": name,
                "description": spec["description"],
                "inputSchema": spec["inputSchema"],
            }
            for name, spec in TOOLS.items()
        ]

    def handle(self, message: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        method = message.get("method")
        msg_id = message.get("id")
        params = message.get("params") or {}
        if method and method.startswith("notifications/"):
            return None
        try:
            if method == "initialize":
                result = {
                    "protocolVersion": params.get("protocolVersion") or PROTOCOL_VERSION,
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": SERVER_NAME, "version": SERVER_VERSION},
                }
            elif method == "tools/list":
                result = {"tools": self.tool_list()}
            elif method == "tools/call":
                name = params.get("name")
                args = params.get("arguments") or {}
                spec = TOOLS.get(name)
                if not spec:
                    raise ValueError(f"Unknown tool: {name}")
                ion_result = spec["handler"](self.root, args)
                result = {
                    "content": [{"type": "text", "text": ion_result.text}],
                    "isError": not ion_result.ok,
                }
            elif method in {"resources/list", "prompts/list"}:
                key = "resources" if method == "resources/list" else "prompts"
                result = {key: []}
            elif method == "ping":
                result = {}
            else:
                raise ValueError(f"Unsupported method: {method}")
            return {"jsonrpc": "2.0", "id": msg_id, "result": result}
        except Exception as exc:
            return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32000, "message": str(exc)}}


def read_message(stdin) -> Optional[Dict[str, Any]]:
    headers: Dict[str, str] = {}
    while True:
        line = stdin.buffer.readline()
        if not line:
            return None
        line = line.decode("ascii", errors="replace").strip()
        if line == "":
            break
        if ":" in line:
            k, v = line.split(":", 1)
            headers[k.lower()] = v.strip()
    length = int(headers.get("content-length", "0"))
    if length <= 0:
        return None
    body = stdin.buffer.read(length)
    return json.loads(body.decode("utf-8"))


def write_message(stdout, message: Dict[str, Any]) -> None:
    body = json.dumps(message, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    stdout.buffer.write(f"Content-Length: {len(body)}\r\n\r\n".encode("ascii") + body)
    stdout.buffer.flush()


def self_test(root: pathlib.Path) -> int:
    server = MCPServer(root)
    tools = server.tool_list()
    print(_json_text({
        "schema_id": "ion.mcp_control_bridge_self_test.v1",
        "status": "ION_MCP_CONTROL_BRIDGE_READY",
        "root": str(root),
        "tools": [t["name"] for t in tools],
    }))
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="ION MCP Control Bridge")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args(argv)
    root = _find_root(args.ion_root)
    if args.self_test:
        return self_test(root)
    server = MCPServer(root)
    while True:
        message = read_message(sys.stdin)
        if message is None:
            return 0
        response = server.handle(message)
        if response is not None:
            write_message(sys.stdout, response)

if __name__ == "__main__":
    raise SystemExit(main())
