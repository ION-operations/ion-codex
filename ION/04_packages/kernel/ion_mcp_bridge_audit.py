from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from typing import Any, Dict, List

REQUIRED_FILES = [
    ".cursor/mcp.json",
    "ION/09_integrations/mcp/ion_mcp_server.py",
    "ION/09_integrations/mcp/README.md",
    "ION/02_architecture/ION_MCP_CONTROL_BRIDGE_PROTOCOL.md",
]
REQUIRED_TOOLS = {
    "ion_status",
    "ion_continue",
    "ion_context_plan",
    "ion_cockpit_view",
    "ion_workflow_audit",
    "ion_read_active_packet",
    "ion_task_return",
}


def read_json(path: pathlib.Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def audit_mcp_bridge(root: pathlib.Path) -> Dict[str, Any]:
    findings: List[Dict[str, Any]] = []
    missing = [p for p in REQUIRED_FILES if not (root / p).exists()]
    if missing:
        findings.append({"code": "missing_required_files", "paths": missing})

    mcp_path = root / ".cursor" / "mcp.json"
    server_command_ok = False
    if mcp_path.exists():
        try:
            config = read_json(mcp_path)
            server = (config.get("mcpServers") or {}).get("ion-control")
            if not server:
                findings.append({"code": "missing_ion_control_server", "path": ".cursor/mcp.json"})
            else:
                args = server.get("args") or []
                if "ION/09_integrations/mcp/ion_mcp_server.py" in args:
                    server_command_ok = True
                else:
                    findings.append({"code": "mcp_server_args_do_not_reference_ion_server", "args": args})
                if server.get("command") not in {"python3", "python"}:
                    findings.append({"code": "unexpected_mcp_command", "command": server.get("command")})
        except Exception as exc:
            findings.append({"code": "invalid_mcp_json", "error": str(exc)})

    server_path = root / "ION" / "09_integrations" / "mcp" / "ion_mcp_server.py"
    self_test = None
    if server_path.exists():
        try:
            proc = subprocess.run(
                [sys.executable, "-S", str(server_path), "--ion-root", str(root), "--self-test"],
                cwd=str(root),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=20,
            )
            self_test = {
                "returncode": proc.returncode,
                "stdout": proc.stdout.strip(),
                "stderr": proc.stderr.strip(),
            }
            if proc.returncode != 0:
                findings.append({"code": "mcp_server_self_test_failed", "stderr": proc.stderr.strip()})
            else:
                try:
                    payload = json.loads(proc.stdout)
                    tools = set(payload.get("tools") or [])
                    missing_tools = sorted(REQUIRED_TOOLS - tools)
                    if missing_tools:
                        findings.append({"code": "missing_mcp_tools", "tools": missing_tools})
                except Exception as exc:
                    findings.append({"code": "invalid_mcp_self_test_json", "error": str(exc)})
        except Exception as exc:
            findings.append({"code": "mcp_server_self_test_exception", "error": str(exc)})

    status = "ION_MCP_CONTROL_BRIDGE_READY" if not findings else "ION_MCP_CONTROL_BRIDGE_DEGRADED"
    return {
        "schema_id": "ion.mcp_control_bridge_audit.v1",
        "status": status,
        "accepted": not findings,
        "server_label": "ion-control",
        "server_command_ok": server_command_ok,
        "required_tools": sorted(REQUIRED_TOOLS),
        "findings": findings,
        "self_test": self_test,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = pathlib.Path(args.ion_root).resolve()
    result = audit_mcp_bridge(root)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
        for finding in result["findings"]:
            print(json.dumps(finding, sort_keys=True))
    return 0 if result["accepted"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
