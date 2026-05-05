import json
from pathlib import Path

from kernel.ion_cursor_hook_state import build_cursor_hook_state, write_cursor_hook_state


def test_cursor_hook_state_projects_current_tree_without_live_claim():
    root = Path.cwd()
    state = build_cursor_hook_state(root)

    assert state["schema_id"] == "ion.cursor_hook_state.v1"
    assert state["cursor_hook_bridge_verdict"] == "ION_CURSOR_HOOK_BRIDGE_READY"
    assert state["status"] == "projected_not_connected"
    assert state["host_connection_state"] == "NOT_CONNECTED_OR_NOT_OBSERVED"
    assert state["live_hook_event_seen"] is False
    assert state["production_authority"] is False
    assert state["live_execution_authority"] is False


def test_cursor_hook_state_writes_blocked_projection_for_incomplete_root(tmp_path):
    (tmp_path / "ION/03_registry/boots").mkdir(parents=True)
    (tmp_path / "ION/04_packages/kernel").mkdir(parents=True)
    (tmp_path / "pyproject.toml").write_text("[project]\nname = \"ion-test\"\n", encoding="utf-8")
    (tmp_path / "ION" / "REPO_AUTHORITY.md").write_text("# authority\n", encoding="utf-8")

    state = write_cursor_hook_state(tmp_path)
    out = tmp_path / "ION/05_context/current/ACTIVE_CURSOR_HOOK_STATE.json"

    assert out.exists()
    assert json.loads(out.read_text(encoding="utf-8"))["schema_id"] == "ion.cursor_hook_state.v1"
    assert state["status"] == "blocked"
    assert state["cursor_hook_bridge_ready"] is False
