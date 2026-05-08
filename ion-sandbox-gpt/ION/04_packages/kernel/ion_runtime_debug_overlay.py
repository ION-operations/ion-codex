"""ION V106 runtime debug overlay projection.

Projects SSE, render, hydration, kernel, and watcher timing data without
pretending unavailable live channels are connected.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CURRENT = Path("ION/05_context/current")
OUTPUT = CURRENT / "ACTIVE_RUNTIME_DEBUG_OVERLAY.json"

ACTIVE_FILES = {
    "sse": CURRENT / "ACTIVE_SSE_EVENT_METRICS.json",
    "render": CURRENT / "ACTIVE_RENDER_TIMING_METRICS.json",
    "hydration": CURRENT / "ACTIVE_DB_HYDRATION_METRICS.json",
    "kernel": CURRENT / "ACTIVE_KERNEL_PROJECTION_TIMINGS.json",
    "watcher": CURRENT / "ACTIVE_FILE_WATCHER_METRICS.json",
    "receipt_hydration": CURRENT / "ACTIVE_RECEIPT_HYDRATION_VIEW_MODEL.json",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_json(path: Path) -> dict[str, Any]:
    try:
        if not path.exists():
            return {}
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except Exception as exc:  # pragma: no cover - defensive projection
        return {"_read_error": str(exc), "_path": str(path)}


def number(value: Any, fallback: float = 0.0) -> float:
    try:
        if value is None:
            return fallback
        return float(value)
    except (TypeError, ValueError):
        return fallback


def integer(value: Any, fallback: int = 0) -> int:
    return int(number(value, fallback))


def _sse(data: dict[str, Any], window_seconds: int) -> dict[str, Any]:
    if not data:
        return {
            "measurement_mode": "NOT_CONNECTED",
            "events_total": 0,
            "events_per_second": 0.0,
            "dropped_events": 0,
            "reconnect_count": 0,
            "last_event_at": None,
        }
    events_total = integer(data.get("events_total"))
    window = number(data.get("window_seconds"), float(window_seconds)) or float(window_seconds)
    eps = number(data.get("events_per_second"), events_total / window if window else 0.0)
    return {
        "measurement_mode": data.get("measurement_mode") or "LIVE_OR_ADAPTER_REPORTED",
        "events_total": events_total,
        "events_per_second": eps,
        "dropped_events": integer(data.get("dropped_events")),
        "reconnect_count": integer(data.get("reconnect_count")),
        "last_event_at": data.get("last_event_at"),
    }


def _render(data: dict[str, Any]) -> dict[str, Any]:
    if not data:
        return {
            "measurement_mode": "PROJECTED_ONLY",
            "last_render_ms": None,
            "p50_render_ms": None,
            "p95_render_ms": None,
            "slow_component": None,
        }
    return {
        "measurement_mode": data.get("measurement_mode") or "ADAPTER_REPORTED",
        "last_render_ms": data.get("last_render_ms"),
        "p50_render_ms": data.get("p50_render_ms"),
        "p95_render_ms": data.get("p95_render_ms"),
        "slow_component": data.get("slow_component"),
    }


def _hydration(db_data: dict[str, Any], receipt_model: dict[str, Any]) -> dict[str, Any]:
    unresolved = integer(receipt_model.get("unresolved_count"))
    conflicts = integer(receipt_model.get("hydration_conflict_count"))
    mode = "PROJECTED_ONLY"
    if db_data:
        mode = db_data.get("measurement_mode") or "ADAPTER_REPORTED"
    return {
        "measurement_mode": mode,
        "db_hydration_ms": db_data.get("db_hydration_ms") if db_data else None,
        "receipt_hydration_ms": db_data.get("receipt_hydration_ms") if db_data else None,
        "unresolved_receipts": unresolved,
        "hydration_conflicts": conflicts,
    }


def _kernel(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "measurement_mode": data.get("measurement_mode") if data else "PROJECTED_ONLY",
        "cockpit_projection_ms": data.get("cockpit_projection_ms") if data else None,
        "lane_timeline_projection_ms": data.get("lane_timeline_projection_ms") if data else None,
        "context_lifecycle_audit_ms": data.get("context_lifecycle_audit_ms") if data else None,
    }


def _watcher(data: dict[str, Any]) -> dict[str, Any]:
    return {
        "measurement_mode": data.get("measurement_mode") if data else "NOT_CONNECTED",
        "refresh_ms": data.get("refresh_ms") if data else None,
        "files_changed": integer(data.get("files_changed")) if data else 0,
        "last_refresh_at": data.get("last_refresh_at") if data else None,
    }


def _status(sse: dict[str, Any], render: dict[str, Any], hydration: dict[str, Any]) -> str:
    if hydration["hydration_conflicts"]:
        return "blocked"
    p95 = number(render.get("p95_render_ms"), 0.0)
    db_ms = number(hydration.get("db_hydration_ms"), 0.0)
    if p95 > 250 or db_ms > 250:
        return "slow"
    if sse.get("measurement_mode") == "NOT_CONNECTED" or hydration["unresolved_receipts"]:
        return "degraded"
    return "healthy"


def build_runtime_debug_overlay(ion_root: str | Path = ".", *, window_seconds: int = 60) -> dict[str, Any]:
    root = Path(ion_root).resolve()
    data = {name: read_json(root / rel) for name, rel in ACTIVE_FILES.items()}
    sse = _sse(data["sse"], window_seconds)
    render = _render(data["render"])
    hydration = _hydration(data["hydration"], data["receipt_hydration"])
    kernel = _kernel(data["kernel"])
    watcher = _watcher(data["watcher"])
    return {
        "schema_id": "ion.runtime_debug_overlay.v1",
        "generated_at": utc_now(),
        "window_seconds": window_seconds,
        "source_paths": {name: rel.as_posix() for name, rel in ACTIVE_FILES.items()},
        "sse": sse,
        "render": render,
        "hydration": hydration,
        "kernel": kernel,
        "watcher": watcher,
        "status": _status(sse, render, hydration),
        "production_authority": False,
    }


def write_runtime_debug_overlay(ion_root: str | Path = ".", output: str | Path | None = None) -> dict[str, Any]:
    root = Path(ion_root).resolve()
    model = build_runtime_debug_overlay(root)
    out = root / (Path(output) if output else OUTPUT)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(model, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return model


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build ION runtime debug overlay.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    model = write_runtime_debug_overlay(args.ion_root, args.output) if args.write else build_runtime_debug_overlay(args.ion_root)
    if args.json:
        print(json.dumps(model, indent=2, sort_keys=True))
    else:
        print(f"ION_RUNTIME_DEBUG_OVERLAY_{model['status'].upper()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
