"""Read-only projection of the local ION operator service stack.

This module describes the user-level services that keep the local transport
surface durable. It does not install, enable, stop, start, or restart services.
Optional localhost probes are visibility-only and disabled unless requested.
"""

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_ID = "ion.local_service_status.v1"
READY_VERDICT = "ION_LOCAL_SERVICE_STATUS_PROJECTED"
DEFAULT_PROBE_TIMEOUT_SECONDS = 0.35
SYSTEMD_TEMPLATE_ROOT = Path("ION/09_integrations/systemd/user")


@dataclass(frozen=True)
class LocalServiceSpec:
    service_id: str
    unit_name: str
    role: str
    local_url: str | None
    health_url: str | None
    public_url: str | None
    tunnel_name: str | None
    template_name: str
    command_summary: str


LOCAL_SERVICE_SPECS = [
    LocalServiceSpec(
        service_id="chatops",
        unit_name="ion-chatops.service",
        role="ChatOps localhost bridge for browser extension approvals and local operator actions.",
        local_url="http://127.0.0.1:8767",
        health_url="http://127.0.0.1:8767/health",
        public_url=None,
        tunnel_name=None,
        template_name="ion-chatops.service.template",
        command_summary="python3 -S -m kernel.ion_chatops_bridge --ion-root . --host 127.0.0.1 --port 8767 --serve",
    ),
    LocalServiceSpec(
        service_id="mcp_preview",
        unit_name="ion-mcp-preview.service",
        role="Local HTTP MCP preview backing the public ChatGPT browser connector.",
        local_url="http://127.0.0.1:8765",
        health_url="http://127.0.0.1:8765/health",
        public_url="https://ion.helixion.net/mcp",
        tunnel_name=None,
        template_name="ion-mcp-preview.service.template",
        command_summary="python3 -S -m kernel.ion_chatgpt_browser_mcp_http_preview --ion-root . --host 127.0.0.1 --port 8765 --serve",
    ),
    LocalServiceSpec(
        service_id="mcp_tunnel",
        unit_name="ion-mcp-tunnel.service",
        role="Cloudflare named tunnel for ion.helixion.net to the local MCP preview.",
        local_url="http://127.0.0.1:8765",
        health_url=None,
        public_url="https://ion.helixion.net/mcp",
        tunnel_name="ion-browser",
        template_name="ion-mcp-tunnel.service.template",
        command_summary="cloudflared tunnel run --url http://127.0.0.1:8765 ion-browser",
    ),
    LocalServiceSpec(
        service_id="action_gateway",
        unit_name="ion-action-gateway.service",
        role="Local Custom GPT Action Gateway with bearer-authenticated bounded action intake.",
        local_url="http://127.0.0.1:8777",
        health_url="http://127.0.0.1:8777/health",
        public_url="https://ion-actions.helixion.net",
        tunnel_name=None,
        template_name="ion-action-gateway.service.template",
        command_summary="python3 -u -S -m kernel.ion_custom_gpt_action_gateway --ion-root . --host 127.0.0.1 --port 8777 --serve",
    ),
    LocalServiceSpec(
        service_id="action_tunnel",
        unit_name="ion-action-tunnel.service",
        role="Cloudflare named tunnel for ion-actions.helixion.net to the local Action Gateway.",
        local_url="http://127.0.0.1:8777",
        health_url=None,
        public_url="https://ion-actions.helixion.net",
        tunnel_name="ion-actions",
        template_name="ion-action-tunnel.service.template",
        command_summary="cloudflared tunnel run --url http://127.0.0.1:8777 ion-actions",
    ),
    LocalServiceSpec(
        service_id="cockpit_app",
        unit_name="ion-cockpit-app.service",
        role="Local-only browser cockpit app for ION runtime, service, Codex queue, and receipt visibility.",
        local_url="http://127.0.0.1:8788",
        health_url="http://127.0.0.1:8788/health",
        public_url=None,
        tunnel_name=None,
        template_name="ion-cockpit-app.service.template",
        command_summary="python3 -S -m kernel.ion_local_cockpit_app --ion-root . --host 127.0.0.1 --port 8788 --serve",
    ),
]


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _probe_health(url: str, timeout_seconds: float) -> dict[str, Any]:
    try:
        request = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            status_code = int(getattr(response, "status", 0) or 0)
            return {
                "status": "ready" if 200 <= status_code < 300 else "degraded",
                "http_status": status_code,
                "finding": None if 200 <= status_code < 300 else "health_endpoint_non_2xx",
            }
    except urllib.error.HTTPError as exc:
        return {"status": "degraded", "http_status": exc.code, "finding": "health_endpoint_http_error"}
    except Exception as exc:  # pragma: no cover - precise socket failure varies by host
        return {"status": "not_running", "http_status": None, "finding": exc.__class__.__name__}


def _template_state(root: Path, spec: LocalServiceSpec) -> dict[str, Any]:
    rel = SYSTEMD_TEMPLATE_ROOT / spec.template_name
    path = root / rel
    return {
        "template_path": rel.as_posix(),
        "template_present": path.exists(),
    }


def _service_row(root: Path, spec: LocalServiceSpec, *, probe_http: bool, timeout_seconds: float) -> dict[str, Any]:
    template = _template_state(root, spec)
    probe = {"status": "not_probed", "http_status": None, "finding": None}
    if probe_http and spec.health_url:
        probe = _probe_health(spec.health_url, timeout_seconds)
    findings = []
    if not template["template_present"]:
        findings.append("systemd_template_missing")
    if probe.get("finding"):
        findings.append(probe["finding"])
    return {
        "service_id": spec.service_id,
        "unit_name": spec.unit_name,
        "role": spec.role,
        "local_url": spec.local_url,
        "health_url": spec.health_url,
        "public_url": spec.public_url,
        "tunnel_name": spec.tunnel_name,
        "command_summary": spec.command_summary,
        "systemd": template,
        "health": probe,
        "status": probe["status"] if probe_http and spec.health_url else ("configured" if template["template_present"] else "missing_template"),
        "findings": findings,
        "production_authority": False,
        "live_execution_authority": False,
    }


def build_local_service_status(
    ion_root: str | Path = ".",
    *,
    probe_http: bool | None = None,
    timeout_seconds: float = DEFAULT_PROBE_TIMEOUT_SECONDS,
) -> dict[str, Any]:
    root = Path(ion_root).resolve()
    if probe_http is None:
        probe_http = os.environ.get("ION_LOCAL_SERVICE_PROBE_HTTP") == "1"
    services = [_service_row(root, spec, probe_http=probe_http, timeout_seconds=timeout_seconds) for spec in LOCAL_SERVICE_SPECS]
    service_count = len(services)
    missing_template_count = sum(1 for row in services if row["status"] == "missing_template")
    not_running_count = sum(1 for row in services if row["health"]["status"] == "not_running")
    degraded_count = sum(1 for row in services if row["health"]["status"] == "degraded")
    ready_count = sum(1 for row in services if row["health"]["status"] == "ready")
    if missing_template_count:
        status = "missing_template"
    elif probe_http and (not_running_count or degraded_count):
        status = "degraded"
    elif probe_http:
        status = "ready"
    else:
        status = "configured"
    return {
        "schema_id": SCHEMA_ID,
        "generated_at": utc_now(),
        "verdict": READY_VERDICT,
        "status": status,
        "probe_http": probe_http,
        "probe_timeout_seconds": timeout_seconds,
        "service_count": service_count,
        "ready_count": ready_count,
        "not_running_count": not_running_count,
        "degraded_count": degraded_count,
        "missing_template_count": missing_template_count,
        "services": services,
        "systemd_template_root": SYSTEMD_TEMPLATE_ROOT.as_posix(),
        "install_authority": False,
        "production_authority": False,
        "live_execution_authority": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Project ION local service status without service control authority.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--probe-http", action="store_true", help="Probe localhost health endpoints.")
    parser.add_argument("--timeout-seconds", type=float, default=DEFAULT_PROBE_TIMEOUT_SECONDS)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = build_local_service_status(args.ion_root, probe_http=args.probe_http, timeout_seconds=args.timeout_seconds)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
