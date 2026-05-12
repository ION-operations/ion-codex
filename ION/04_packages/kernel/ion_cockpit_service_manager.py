"""Operator-facing local service console helpers for ION cockpit surfaces."""

from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

SCHEMA_ID = "ion.cockpit_service_console.v1"
RESTART_CONFIRMATION = "ION_SERVICE_CONTROL_APPROVED"

SERVICE_SPECS = (
    {
        "id": "chatops",
        "unit": "ion-chatops.service",
        "label": "ChatOps daemon",
        "role": "Browser extension API, Docs ZIPs, asset capture, Codex tab proxy.",
        "critical": True,
        "fix_label": "Restart daemon",
    },
    {
        "id": "cockpit",
        "unit": "ion-cockpit-app.service",
        "label": "Local cockpit",
        "role": "Local cockpit app and Codex chat surface.",
        "critical": False,
        "fix_label": "Restart cockpit",
    },
    {
        "id": "helixion",
        "unit": "ion-mcp-preview.service",
        "label": "Helixion public cockpit",
        "role": "Public Helixion URL, auth wrapper, MCP preview, remote cockpit chat.",
        "critical": True,
        "fix_label": "Restart Helixion",
    },
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _resolve_root(root: str | Path | None) -> Path:
    return Path(root or ".").expanduser().resolve()


def _systemctl_is_active(unit: str) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            ["systemctl", "--user", "is-active", unit],
            check=False,
            capture_output=True,
            text=True,
            timeout=8,
        )
    except Exception as exc:
        return {
            "ok": False,
            "status": "unknown",
            "finding": exc.__class__.__name__,
            "returncode": None,
        }
    status = (completed.stdout or completed.stderr or "unknown").strip() or "unknown"
    return {
        "ok": completed.returncode == 0 and status == "active",
        "status": status,
        "finding": "active" if completed.returncode == 0 and status == "active" else "service_not_active",
        "returncode": completed.returncode,
    }


def build_service_console_model(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    services: list[dict[str, Any]] = []
    required_issue_count = 0
    warning_count = 0
    for spec in SERVICE_SPECS:
        state = _systemctl_is_active(str(spec["unit"]))
        critical = bool(spec.get("critical"))
        if not state["ok"] and critical:
            required_issue_count += 1
        elif not state["ok"]:
            warning_count += 1
        services.append({
            **spec,
            "active": bool(state["ok"]),
            "status": state["status"],
            "finding": state["finding"],
            "severity": "ready" if state["ok"] else "blocked" if critical else "warning",
            "restart_confirmation": RESTART_CONFIRMATION,
        })
    verdict = "ready" if required_issue_count == 0 and warning_count == 0 else "blocked" if required_issue_count else "warning"
    headline = (
        "All operator services are active."
        if verdict == "ready"
        else "One or more required local services need attention."
        if verdict == "blocked"
        else "Optional cockpit service needs attention."
    )
    return {
        "schema_id": SCHEMA_ID,
        "ok": verdict == "ready",
        "verdict": verdict,
        "headline": headline,
        "required_issue_count": required_issue_count,
        "warning_count": warning_count,
        "services": services,
        "generated_at": _now(),
        "shell_root": shell_root.as_posix(),
        "operator_message": "Use the visible Fix buttons; no terminal command is required for normal recovery.",
        "production_authority": False,
        "live_execution_authority": False,
    }


def _receipt_dir(root: Path) -> Path:
    return root / "ION/05_context/current/chatops_bridge/receipts"


def _write_service_receipt(root: Path, payload: Mapping[str, Any]) -> str:
    receipt_dir = _receipt_dir(root)
    receipt_dir.mkdir(parents=True, exist_ok=True)
    receipt_id = f"service_control_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ%f')}"
    path = receipt_dir / f"{receipt_id}.json"
    path.write_text(json.dumps({"receipt_id": receipt_id, **payload}, indent=2, sort_keys=True), encoding="utf-8")
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def restart_service(root: str | Path | None, packet: Mapping[str, Any]) -> dict[str, Any]:
    shell_root = _resolve_root(root)
    unit = str(packet.get("unit") or "").strip()
    confirmation = str(packet.get("confirmation") or "").strip()
    allowed = {str(spec["unit"]) for spec in SERVICE_SPECS}
    if confirmation != RESTART_CONFIRMATION:
        result = {"ok": False, "finding": "service_restart_confirmation_required", "required_confirmation": RESTART_CONFIRMATION}
    elif unit not in allowed:
        result = {"ok": False, "finding": "service_unit_not_allowed", "allowed_units": sorted(allowed)}
    elif unit == "ion-mcp-preview.service":
        try:
            subprocess.Popen(
                ["systemctl", "--user", "restart", unit],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                text=True,
            )
            result = {
                "ok": True,
                "finding": "service_restart_dispatched",
                "unit": unit,
                "note": "Helixion service restarts itself asynchronously; refresh the page after a few seconds.",
                "state": _systemctl_is_active(unit),
            }
        except Exception as exc:
            result = {"ok": False, "finding": "service_restart_exception", "unit": unit, "error": exc.__class__.__name__}
    else:
        try:
            completed = subprocess.run(
                ["systemctl", "--user", "restart", unit],
                check=False,
                capture_output=True,
                text=True,
                timeout=25,
            )
            state = _systemctl_is_active(unit)
            result = {
                "ok": completed.returncode == 0 and state["ok"],
                "finding": "service_restart_completed" if completed.returncode == 0 and state["ok"] else "service_restart_failed",
                "unit": unit,
                "returncode": completed.returncode,
                "stdout": (completed.stdout or "").strip()[-1600:],
                "stderr": (completed.stderr or "").strip()[-1600:],
                "state": state,
            }
        except Exception as exc:
            result = {"ok": False, "finding": "service_restart_exception", "unit": unit, "error": exc.__class__.__name__}
    receipt_path = _write_service_receipt(
        shell_root,
        {
            "schema_id": "ion.cockpit_service_control_receipt.v1",
            "created_at": _now(),
            "operation": "systemctl_user_restart",
            "unit": unit,
            "result": result,
            "production_authority": False,
            "live_execution_authority": False,
        },
    )
    return {
        "schema_id": "ion.cockpit_service_restart_result.v1",
        **result,
        "receipt_path": receipt_path,
        "service_console": build_service_console_model(shell_root),
        "production_authority": False,
        "live_execution_authority": False,
    }
