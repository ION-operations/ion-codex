import json
from pathlib import Path

from kernel.ion_runtime_debug_overlay import build_runtime_debug_overlay, write_runtime_debug_overlay


def write_json(root: Path, rel: str, payload: dict):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_runtime_debug_overlay_marks_absent_live_channels_as_projected_or_not_connected(tmp_path):
    model = build_runtime_debug_overlay(tmp_path)

    assert model["schema_id"] == "ion.runtime_debug_overlay.v1"
    assert model["sse"]["measurement_mode"] == "NOT_CONNECTED"
    assert model["render"]["measurement_mode"] == "PROJECTED_ONLY"
    assert model["hydration"]["measurement_mode"] == "PROJECTED_ONLY"
    assert model["status"] == "degraded"


def test_runtime_debug_overlay_uses_metrics_and_blocks_on_hydration_conflicts(tmp_path):
    current = "ION/05_context/current"
    write_json(tmp_path, f"{current}/ACTIVE_SSE_EVENT_METRICS.json", {"events_total": 120, "window_seconds": 60, "dropped_events": 1, "reconnect_count": 2})
    write_json(tmp_path, f"{current}/ACTIVE_RENDER_TIMING_METRICS.json", {"last_render_ms": 20, "p95_render_ms": 80})
    write_json(tmp_path, f"{current}/ACTIVE_DB_HYDRATION_METRICS.json", {"db_hydration_ms": 40, "receipt_hydration_ms": 10})
    write_json(tmp_path, f"{current}/ACTIVE_RECEIPT_HYDRATION_VIEW_MODEL.json", {"unresolved_count": 0, "hydration_conflict_count": 1})

    model = build_runtime_debug_overlay(tmp_path)

    assert model["sse"]["events_per_second"] == 2.0
    assert model["hydration"]["hydration_conflicts"] == 1
    assert model["status"] == "blocked"


def test_runtime_debug_overlay_marks_slow_timings(tmp_path):
    current = "ION/05_context/current"
    write_json(tmp_path, f"{current}/ACTIVE_SSE_EVENT_METRICS.json", {"events_total": 60, "events_per_second": 1})
    write_json(tmp_path, f"{current}/ACTIVE_RENDER_TIMING_METRICS.json", {"p95_render_ms": 300})
    write_json(tmp_path, f"{current}/ACTIVE_RECEIPT_HYDRATION_VIEW_MODEL.json", {"unresolved_count": 0, "hydration_conflict_count": 0})

    model = build_runtime_debug_overlay(tmp_path)

    assert model["status"] == "slow"


def test_write_runtime_debug_overlay(tmp_path):
    model = write_runtime_debug_overlay(tmp_path)
    out = tmp_path / "ION/05_context/current/ACTIVE_RUNTIME_DEBUG_OVERLAY.json"
    assert out.exists()
    assert json.loads(out.read_text(encoding="utf-8"))["schema_id"] == model["schema_id"]
