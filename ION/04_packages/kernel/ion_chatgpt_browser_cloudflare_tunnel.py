"""V122 Cloudflare Tunnel bridge for the ChatGPT browser MCP connector.

This module exposes the V121 local HTTP MCP preview through a Cloudflare Tunnel
without adding arbitrary shell or file access to ION. It records the tunnel URL
as connector status evidence and keeps ChatGPT as a carrier, not ION identity.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import signal
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from urllib import error, request

from .ion_chatgpt_browser_mcp_http_preview import (
    BOUNDED_QUEUE_RECEIPT_TOOLS,
    DEFAULT_BIND_HOST,
    DEFAULT_PORT,
    FORBIDDEN_CAPABILITIES,
    READY_VERDICT as HTTP_PREVIEW_READY_VERDICT,
    STATUS_READ_TOOLS,
    WRITE_CONFIRMATION_TOKEN,
    audit_http_mcp_preview,
)

SCHEMA_ID = "ion.chatgpt_browser_cloudflare_tunnel.v1"
STATUS_SCHEMA_ID = "ion.chatgpt_browser_cloudflare_tunnel_status.v1"
VERSION_LINE = "V122_CHATGPT_BROWSER_CLOUDFLARE_TUNNEL"
READY_VERDICT = "ION_CHATGPT_BROWSER_CLOUDFLARE_TUNNEL_READY"
SETUP_REQUIRED_VERDICT = "ION_CHATGPT_BROWSER_CLOUDFLARE_TUNNEL_SETUP_REQUIRED"
BLOCKED_VERDICT = "ION_CHATGPT_BROWSER_CLOUDFLARE_TUNNEL_BLOCKED"
DEFAULT_ENDPOINT_PATH = "/mcp"
OUTPUT_RELATIVE_PATH = Path("ION/05_context/current/CHATGPT_BROWSER_CLOUDFLARE_TUNNEL_V122.json")
STATUS_RELATIVE_PATH = Path("ION/05_context/current/ACTIVE_CHATGPT_BROWSER_CLOUDFLARE_TUNNEL.json")

TRANSPORT_NOT_INSTALLED = "NOT_INSTALLED"
TRANSPORT_INSTALLED_NOT_RUNNING = "INSTALLED_NOT_RUNNING"
TRANSPORT_LOCAL_HTTP_RUNNING_ONLY = "LOCAL_HTTP_RUNNING_ONLY"
TRANSPORT_TUNNEL_RUNNING_NOT_VERIFIED = "TUNNEL_RUNNING_NOT_VERIFIED"
TRANSPORT_TUNNEL_RUNNING_VERIFIED = "TUNNEL_RUNNING_VERIFIED"
TRANSPORT_STABLE_HOSTNAME_NOT_ACTIVE = "STABLE_HOSTNAME_NOT_ACTIVE"
TRANSPORT_CHATGPT_CONNECTOR_ADDED_NOT_TESTED = "CHATGPT_CONNECTOR_ADDED_NOT_TESTED"
TRANSPORT_CHATGPT_CONNECTOR_TESTED_READY = "CHATGPT_CONNECTOR_TESTED_READY"


def _resolve_existing_ion_root(root: str | Path) -> Path:
    shell_root = Path(root).expanduser().resolve()
    required = (
        shell_root / "ION/03_registry/boots",
        shell_root / "ION/04_packages/kernel",
    )
    missing = [path.as_posix() for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(
            "Refusing to write Cloudflare tunnel status outside an existing ION root. "
            f"root={shell_root.as_posix()} missing={missing}"
        )
    return shell_root


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def default_local_url(host: str = DEFAULT_BIND_HOST, port: int = DEFAULT_PORT) -> str:
    return f"http://{host}:{port}"


def find_cloudflared(binary: str = "cloudflared") -> str | None:
    path = Path(binary).expanduser()
    if (path.is_absolute() or "/" in binary) and path.is_file() and os.access(path, os.X_OK):
        return path.as_posix()
    found = shutil.which(binary)
    if found:
        return found
    user_local = Path.home() / ".local/bin/cloudflared"
    if binary == "cloudflared" and user_local.is_file() and os.access(user_local, os.X_OK):
        return user_local.as_posix()
    return None


def extract_tunnel_url(line: str) -> str | None:
    trycloudflare = re.search(r"(https://[a-zA-Z0-9-]+\.trycloudflare\.com)", line)
    if trycloudflare:
        return trycloudflare.group(1)
    if "trycloudflare" not in line.lower() and "tunnel" not in line.lower():
        return None
    custom = re.search(r"(https://[a-zA-Z0-9][a-zA-Z0-9.-]+\.[a-zA-Z]{2,})", line)
    if custom:
        candidate = custom.group(1)
        blocked_hosts = ("localhost", "127.0.0.1", "cloudflare.com", "developers.cloudflare.com")
        if not any(host in candidate for host in blocked_hosts):
            return candidate
    return None


def connector_url_from_tunnel_url(tunnel_url: str, endpoint_path: str = DEFAULT_ENDPOINT_PATH) -> str:
    normalized_endpoint = endpoint_path if endpoint_path.startswith("/") else f"/{endpoint_path}"
    return f"{tunnel_url.rstrip('/')}{normalized_endpoint}"


def normalize_stable_hostname(value: str | None) -> str | None:
    if not value:
        return None
    stripped = value.strip()
    stripped = stripped.removeprefix("https://").removeprefix("http://")
    host = stripped.split("/", 1)[0].strip()
    return host or None


def build_cloudflared_command(
    *,
    local_url: str,
    cloudflared_binary: str = "cloudflared",
    tunnel_name: str | None = None,
    config_path: str | None = None,
    credentials_file: str | None = None,
) -> list[str]:
    if tunnel_name:
        command = [cloudflared_binary, "tunnel"]
        if config_path:
            command.extend(["--config", config_path])
        command.append("run")
        if credentials_file:
            command.extend(["--credentials-file", credentials_file])
        command.extend(["--url", local_url, tunnel_name])
        return command
    return [cloudflared_binary, "tunnel", "--url", local_url]


def build_cloudflared_route_dns_command(
    *,
    tunnel_name: str,
    hostname: str,
    cloudflared_binary: str = "cloudflared",
) -> list[str]:
    return [cloudflared_binary, "tunnel", "route", "dns", tunnel_name, hostname]


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def _pid_running(pid: Any) -> bool:
    try:
        parsed = int(pid)
    except (TypeError, ValueError):
        return False
    if parsed <= 0:
        return False
    try:
        os.kill(parsed, 0)
    except OSError:
        return False
    return True


def _http_json_request(
    url: str,
    *,
    payload: Mapping[str, Any] | None = None,
    timeout: float = 3.0,
) -> dict[str, Any]:
    headers = {"Accept": "application/json", "User-Agent": "ION-Connector-Health/1.0"}
    data: bytes | None = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = request.Request(url, data=data, headers=headers)
    try:
        with request.urlopen(req, timeout=timeout) as response:  # noqa: S310 - bounded operator-provided connector URL
            body = response.read().decode("utf-8", errors="replace")
            parsed: Any = json.loads(body) if body else None
            return {
                "ok": 200 <= int(response.status) < 300,
                "status_code": int(response.status),
                "json": parsed,
                "error": None,
            }
    except error.HTTPError as exc:
        return {"ok": False, "status_code": int(exc.code), "json": None, "error": str(exc)}
    except Exception as exc:  # pragma: no cover - exact network failures vary by host
        return {"ok": False, "status_code": None, "json": None, "error": str(exc)}


def _tool_names_from_jsonrpc(value: Mapping[str, Any] | None) -> list[str]:
    if not isinstance(value, Mapping):
        return []
    result = value.get("result")
    if not isinstance(result, Mapping):
        return []
    tools = result.get("tools")
    if not isinstance(tools, list):
        return []
    names: list[str] = []
    for tool in tools:
        if isinstance(tool, Mapping) and isinstance(tool.get("name"), str):
            names.append(tool["name"])
    return sorted(names)


def _tool_list_check(response: Mapping[str, Any]) -> dict[str, Any]:
    expected = sorted(STATUS_READ_TOOLS | BOUNDED_QUEUE_RECEIPT_TOOLS)
    names = _tool_names_from_jsonrpc(response.get("json") if isinstance(response.get("json"), Mapping) else None)
    missing = sorted(set(expected) - set(names))
    unexpected_forbidden = sorted(set(names) & FORBIDDEN_CAPABILITIES)
    return {
        "ok": bool(response.get("ok")) and not missing and not unexpected_forbidden,
        "tool_count": len(names),
        "expected_tool_count": len(expected),
        "missing_tools": missing,
        "forbidden_tools_exposed": unexpected_forbidden,
        "status_code": response.get("status_code"),
        "error": response.get("error"),
    }


def _write_confirmation_check(response: Mapping[str, Any]) -> dict[str, Any]:
    payload = response.get("json")
    structured: Mapping[str, Any] | None = None
    if isinstance(payload, Mapping):
        result = payload.get("result")
        if isinstance(result, Mapping) and isinstance(result.get("structuredContent"), Mapping):
            structured = result["structuredContent"]
    return {
        "ok": bool(response.get("ok"))
        and bool(structured)
        and structured.get("ok") is False
        and structured.get("finding") == "bounded_write_confirmation_required"
        and structured.get("required_confirmation") == WRITE_CONFIRMATION_TOKEN,
        "status_code": response.get("status_code"),
        "finding": structured.get("finding") if structured else None,
        "required_confirmation": structured.get("required_confirmation") if structured else None,
        "error": response.get("error"),
    }


def check_connector_health(
    *,
    local_url: str,
    connector_url: str | None = None,
    timeout: float = 3.0,
) -> dict[str, Any]:
    """Probe the bounded connector transport without performing a confirmed write."""

    local_root = local_url.rstrip("/")
    local_mcp_url = f"{local_root}{DEFAULT_ENDPOINT_PATH}"
    local_health = _http_json_request(f"{local_root}/health", timeout=timeout)
    local_tools = _http_json_request(
        local_mcp_url,
        payload={"jsonrpc": "2.0", "id": "health-local-tools", "method": "tools/list", "params": {}},
        timeout=timeout,
    )
    local_tools_check = _tool_list_check(local_tools)

    public_tools_check: dict[str, Any] = {
        "ok": False,
        "tool_count": 0,
        "expected_tool_count": len(STATUS_READ_TOOLS | BOUNDED_QUEUE_RECEIPT_TOOLS),
        "missing_tools": sorted(STATUS_READ_TOOLS | BOUNDED_QUEUE_RECEIPT_TOOLS),
        "forbidden_tools_exposed": [],
        "status_code": None,
        "error": "connector_url_absent",
    }
    write_confirmation = {
        "ok": False,
        "status_code": None,
        "finding": None,
        "required_confirmation": None,
        "error": "connector_url_absent",
    }
    if connector_url:
        public_tools = _http_json_request(
            connector_url,
            payload={"jsonrpc": "2.0", "id": "health-public-tools", "method": "tools/list", "params": {}},
            timeout=timeout,
        )
        public_tools_check = _tool_list_check(public_tools)
        write_response = _http_json_request(
            connector_url,
            payload={
                "jsonrpc": "2.0",
                "id": "health-write-confirmation",
                "method": "tools/call",
                "params": {
                    "name": "ion_request_codex_work_packet",
                    "arguments": {"objective": "transport health check should not write without confirmation"},
                },
            },
            timeout=timeout,
        )
        write_confirmation = _write_confirmation_check(write_response)

    return {
        "schema_id": "ion.chatgpt_browser_connector_transport_health.v1",
        "local_url": local_url,
        "connector_url": connector_url,
        "local_http_preview": {
            "ok": bool(local_health.get("ok")),
            "status_code": local_health.get("status_code"),
            "error": local_health.get("error"),
        },
        "local_mcp_tools_list": local_tools_check,
        "public_mcp_tools_list": public_tools_check,
        "public_write_confirmation_required": write_confirmation,
        "production_authority": False,
        "live_execution_authority": False,
        "deployment_authority": False,
    }


def write_tunnel_status(
    root: str | Path,
    *,
    tunnel_url: str | None,
    running: bool,
    local_url: str,
    endpoint_path: str = DEFAULT_ENDPOINT_PATH,
    transport_mode: str = "quick_tunnel",
    tunnel_name: str | None = None,
    stable_hostname: str | None = None,
    error: str | None = None,
    process_id: int | None = None,
    output: str | Path | None = None,
) -> dict[str, Any]:
    shell_root = _resolve_existing_ion_root(root)
    status_path = shell_root / (Path(output) if output else STATUS_RELATIVE_PATH)
    connector_url = connector_url_from_tunnel_url(tunnel_url, endpoint_path) if tunnel_url else None
    status = {
        "schema_id": STATUS_SCHEMA_ID,
        "version_line": VERSION_LINE,
        "method": "cloudflare_tunnel",
        "transport_mode": transport_mode,
        "running": running,
        "local_url": local_url,
        "endpoint_path": endpoint_path,
        "tunnel_name": tunnel_name,
        "stable_hostname": stable_hostname,
        "tunnel_url": tunnel_url,
        "connector_url": connector_url,
        "error": error,
        "process_id": process_id,
        "updated_at": utc_now(),
        "production_authority": False,
        "live_execution_authority": False,
        "deployment_authority": False,
    }
    status_path.parent.mkdir(parents=True, exist_ok=True)
    status_path.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return status


def audit_cloudflare_tunnel(
    root: str | Path | None = None,
    *,
    local_url: str | None = None,
    endpoint_path: str = DEFAULT_ENDPOINT_PATH,
    cloudflared_binary: str = "cloudflared",
    tunnel_name: str | None = None,
    stable_hostname: str | None = None,
    config_path: str | None = None,
    credentials_file: str | None = None,
) -> dict[str, Any]:
    shell_root = Path(root or ".").expanduser().resolve()
    preview = audit_http_mcp_preview(shell_root)
    cloudflared_path = find_cloudflared(cloudflared_binary)
    active_status = _read_json(shell_root / STATUS_RELATIVE_PATH)
    findings: list[str] = []
    resolved_local_url = local_url or default_local_url()
    normalized_stable_hostname = normalize_stable_hostname(stable_hostname)
    stable_tunnel_url = f"https://{normalized_stable_hostname}" if normalized_stable_hostname else None
    stable_connector_url = connector_url_from_tunnel_url(stable_tunnel_url, endpoint_path) if stable_tunnel_url else None
    status_connector_url = active_status.get("connector_url") if active_status else None
    status_tunnel_url = active_status.get("tunnel_url") if active_status else None
    status_running = bool(active_status.get("running")) if active_status else False
    active_process_running = _pid_running(active_status.get("process_id") if active_status else None)
    candidate_connector_url = status_connector_url if status_running and active_process_running else None
    health = check_connector_health(local_url=resolved_local_url, connector_url=candidate_connector_url)

    preview_ready = preview.get("verdict") == HTTP_PREVIEW_READY_VERDICT
    if not preview_ready:
        findings.append("v121_http_mcp_preview_not_ready")
    if not cloudflared_path:
        findings.append("cloudflared_not_found_on_path")
    if normalized_stable_hostname and not tunnel_name:
        findings.append("stable_hostname_requires_named_tunnel")
    if tunnel_name and not (credentials_file or config_path or (Path.home() / ".cloudflared/cert.pem").exists()):
        findings.append("named_tunnel_credentials_or_config_not_found_locally")
    if status_connector_url and not candidate_connector_url:
        findings.append("stale_active_connector_url_not_currently_running")
    if status_running and not active_process_running:
        findings.append("active_tunnel_status_pid_not_running")
    local_http_running = bool(health["local_http_preview"]["ok"] and health["local_mcp_tools_list"]["ok"])
    public_verified = bool(
        candidate_connector_url
        and health["public_mcp_tools_list"]["ok"]
        and health["public_write_confirmation_required"]["ok"]
    )
    write_tools_require_confirmation = bool(health["public_write_confirmation_required"]["ok"]) if candidate_connector_url else False
    if not local_http_running:
        findings.append("local_http_mcp_preview_runtime_not_running")
    if candidate_connector_url and not public_verified:
        findings.append("public_tunnel_mcp_not_verified")

    if not cloudflared_path:
        transport_state = TRANSPORT_NOT_INSTALLED
    elif candidate_connector_url:
        transport_state = TRANSPORT_TUNNEL_RUNNING_VERIFIED if public_verified else TRANSPORT_TUNNEL_RUNNING_NOT_VERIFIED
    elif local_http_running:
        transport_state = TRANSPORT_LOCAL_HTTP_RUNNING_ONLY
    else:
        transport_state = TRANSPORT_INSTALLED_NOT_RUNNING

    active_connector_url = candidate_connector_url
    active_tunnel_url = status_tunnel_url if candidate_connector_url else None
    stable_connector_active = bool(stable_connector_url and active_connector_url == stable_connector_url)
    if stable_connector_url and not stable_connector_active:
        findings.append("stable_connector_url_not_active")
    active_running = transport_state in {TRANSPORT_TUNNEL_RUNNING_NOT_VERIFIED, TRANSPORT_TUNNEL_RUNNING_VERIFIED}
    accepted = preview_ready
    if not preview_ready:
        verdict = BLOCKED_VERDICT
        connector_state = "BLOCKED"
    elif stable_connector_url and not stable_connector_active:
        verdict = SETUP_REQUIRED_VERDICT
        connector_state = TRANSPORT_STABLE_HOSTNAME_NOT_ACTIVE
    elif transport_state == TRANSPORT_TUNNEL_RUNNING_VERIFIED:
        verdict = READY_VERDICT
        connector_state = transport_state
    else:
        verdict = SETUP_REQUIRED_VERDICT
        connector_state = transport_state

    return {
        "schema_id": SCHEMA_ID,
        "version_line": VERSION_LINE,
        "verdict": verdict,
        "accepted": accepted,
        "connector_state": connector_state,
        "transport_state": transport_state,
        "local_url": resolved_local_url,
        "endpoint_path": endpoint_path,
        "required_public_connector_path": connector_url_from_tunnel_url("https://<cloudflare-tunnel-host>", endpoint_path),
        "cloudflared_found": bool(cloudflared_path),
        "cloudflared_path": cloudflared_path,
        "stable_hostname": normalized_stable_hostname,
        "stable_tunnel_url": stable_tunnel_url,
        "stable_connector_url": stable_connector_url,
        "stable_connector_active": stable_connector_active,
        "tunnel_name": tunnel_name,
        "named_tunnel_route_dns_command": build_cloudflared_route_dns_command(
            tunnel_name=tunnel_name,
            hostname=normalized_stable_hostname,
            cloudflared_binary=cloudflared_path or cloudflared_binary,
        ) if tunnel_name and normalized_stable_hostname else None,
        "cloudflared_command": build_cloudflared_command(
            local_url=resolved_local_url,
            cloudflared_binary=cloudflared_path or cloudflared_binary,
            tunnel_name=tunnel_name,
            config_path=config_path,
            credentials_file=credentials_file,
        ),
        "active_status_path": str(STATUS_RELATIVE_PATH),
        "active_tunnel_url": active_tunnel_url,
        "active_connector_url": active_connector_url,
        "active_running": active_running,
        "active_process_running": active_process_running,
        "active_process_id": active_status.get("process_id") if active_status else None,
        "local_http_running": local_http_running,
        "public_tunnel_verified": public_verified,
        "write_tools_require_confirmation": write_tools_require_confirmation,
        "stale_tunnel_url": status_tunnel_url if status_tunnel_url and not active_tunnel_url else None,
        "stale_connector_url": status_connector_url if status_connector_url and not active_connector_url else None,
        "http_preview_verdict": preview.get("verdict"),
        "health_checks": health,
        "findings": findings,
        "production_authority": False,
        "live_execution_authority": False,
        "deployment_authority": False,
    }


def write_cloudflare_tunnel_audit(
    root: str | Path | None = None,
    *,
    local_url: str | None = None,
    endpoint_path: str = DEFAULT_ENDPOINT_PATH,
    cloudflared_binary: str = "cloudflared",
    tunnel_name: str | None = None,
    stable_hostname: str | None = None,
    config_path: str | None = None,
    credentials_file: str | None = None,
    output: str | Path | None = None,
) -> dict[str, Any]:
    shell_root = Path(root or ".").expanduser().resolve()
    result = audit_cloudflare_tunnel(
        shell_root,
        local_url=local_url,
        endpoint_path=endpoint_path,
        cloudflared_binary=cloudflared_binary,
        tunnel_name=tunnel_name,
        stable_hostname=stable_hostname,
        config_path=config_path,
        credentials_file=credentials_file,
    )
    out = shell_root / (Path(output) if output else OUTPUT_RELATIVE_PATH)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return result


def run_cloudflare_tunnel(
    root: str | Path,
    *,
    local_url: str,
    endpoint_path: str = DEFAULT_ENDPOINT_PATH,
    cloudflared_binary: str = "cloudflared",
    tunnel_name: str | None = None,
    stable_hostname: str | None = None,
    config_path: str | None = None,
    credentials_file: str | None = None,
) -> int:
    shell_root = Path(root).expanduser().resolve()
    cloudflared_path = find_cloudflared(cloudflared_binary)
    if not cloudflared_path:
        write_tunnel_status(
            shell_root,
            tunnel_url=None,
            running=False,
            local_url=local_url,
            endpoint_path=endpoint_path,
            transport_mode="named_tunnel" if tunnel_name else "quick_tunnel",
            tunnel_name=tunnel_name,
            stable_hostname=stable_hostname,
            error="cloudflared_not_found_on_path",
        )
        print("cloudflared not found on PATH; install it before starting the tunnel.", file=sys.stderr)
        return 2

    command = build_cloudflared_command(
        local_url=local_url,
        cloudflared_binary=cloudflared_path,
        tunnel_name=tunnel_name,
        config_path=config_path,
        credentials_file=credentials_file,
    )
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    tunnel_url: str | None = None
    normalized_stable_hostname = normalize_stable_hostname(stable_hostname)
    if tunnel_name and normalized_stable_hostname:
        tunnel_url = f"https://{normalized_stable_hostname}"
        status = write_tunnel_status(
            shell_root,
            tunnel_url=tunnel_url,
            running=True,
            local_url=local_url,
            endpoint_path=endpoint_path,
            transport_mode="named_tunnel",
            tunnel_name=tunnel_name,
            stable_hostname=normalized_stable_hostname,
            process_id=proc.pid,
        )
        print(json.dumps(status, indent=2, sort_keys=True), flush=True)

    def shutdown(*_: object) -> None:
        write_tunnel_status(
            shell_root,
            tunnel_url=tunnel_url,
            running=False,
            local_url=local_url,
            endpoint_path=endpoint_path,
            transport_mode="named_tunnel" if tunnel_name else "quick_tunnel",
            tunnel_name=tunnel_name,
            stable_hostname=normalized_stable_hostname,
            error="shutdown",
            process_id=proc.pid,
        )
        proc.terminate()
        raise SystemExit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)
    try:
        assert proc.stdout is not None
        for raw_line in proc.stdout:
            line = raw_line.rstrip()
            print(line, flush=True)
            if not tunnel_url:
                parsed = extract_tunnel_url(line)
                if parsed:
                    tunnel_url = parsed
                    status = write_tunnel_status(
                        shell_root,
                        tunnel_url=tunnel_url,
                        running=True,
                        local_url=local_url,
                        endpoint_path=endpoint_path,
                        transport_mode="named_tunnel" if tunnel_name else "quick_tunnel",
                        tunnel_name=tunnel_name,
                        stable_hostname=normalized_stable_hostname,
                        process_id=proc.pid,
                    )
                    print(json.dumps(status, indent=2, sort_keys=True), flush=True)
        returncode = proc.wait()
        write_tunnel_status(
            shell_root,
            tunnel_url=tunnel_url,
            running=False,
            local_url=local_url,
            endpoint_path=endpoint_path,
            transport_mode="named_tunnel" if tunnel_name else "quick_tunnel",
            tunnel_name=tunnel_name,
            stable_hostname=normalized_stable_hostname,
            error=f"cloudflared_exited:{returncode}",
            process_id=proc.pid,
        )
        return returncode
    finally:
        if proc.poll() is None:
            proc.terminate()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ION ChatGPT browser Cloudflare Tunnel bridge.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--host", default=DEFAULT_BIND_HOST)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--local-url", default=None)
    parser.add_argument("--endpoint-path", default=DEFAULT_ENDPOINT_PATH)
    parser.add_argument("--cloudflared-binary", default="cloudflared")
    parser.add_argument("--tunnel-name", default=None)
    parser.add_argument("--stable-hostname", default=None)
    parser.add_argument("--cloudflared-config", default=None)
    parser.add_argument("--credentials-file", default=None)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output", default=None)
    parser.add_argument("--start", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    local_url = args.local_url or default_local_url(args.host, args.port)
    if args.start:
        return run_cloudflare_tunnel(
            args.ion_root,
            local_url=local_url,
            endpoint_path=args.endpoint_path,
            cloudflared_binary=args.cloudflared_binary,
            tunnel_name=args.tunnel_name,
            stable_hostname=args.stable_hostname,
            config_path=args.cloudflared_config,
            credentials_file=args.credentials_file,
        )

    if args.write:
        result = write_cloudflare_tunnel_audit(
            args.ion_root,
            local_url=local_url,
            endpoint_path=args.endpoint_path,
            cloudflared_binary=args.cloudflared_binary,
            tunnel_name=args.tunnel_name,
            stable_hostname=args.stable_hostname,
            config_path=args.cloudflared_config,
            credentials_file=args.credentials_file,
            output=args.output,
        )
    else:
        result = audit_cloudflare_tunnel(
            args.ion_root,
            local_url=local_url,
            endpoint_path=args.endpoint_path,
            cloudflared_binary=args.cloudflared_binary,
            tunnel_name=args.tunnel_name,
            stable_hostname=args.stable_hostname,
            config_path=args.cloudflared_config,
            credentials_file=args.credentials_file,
        )
    print(json.dumps(result, indent=2, sort_keys=True) if args.json or args.self_test else result["verdict"])
    return 0 if result["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
