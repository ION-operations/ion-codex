from __future__ import annotations

import importlib.util
import io
import json
import sys
import tomllib
from pathlib import Path

from kernel.ion_mcp_local_bridge import IonMcpLocalBridge


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def test_project_codex_config_is_project_scoped_and_hook_enabled():
    root = _repo_root()
    config_path = root / ".codex" / "config.toml"

    config = tomllib.loads(config_path.read_text(encoding="utf-8"))

    assert not (root / "AGENTS.md").exists()
    assert config["sandbox_mode"] == "workspace-write"
    assert config["approval_policy"] == "on-request"
    assert config["features"]["codex_hooks"] is True
    assert config["sandbox_workspace_write"]["network_access"] is False
    assert "ION/05_context/current/codex_solo" in config["sandbox_workspace_write"]["writable_roots"]
    assert config["mcp_servers"]["ion_local"]["enabled"] is True
    assert config["mcp_servers"]["ion_local"]["required"] is False
    assert "--stdio" in config["mcp_servers"]["ion_local"]["args"]
    assert "ION/05_context/current/codex_solo/HOT_CONTEXT.md" in config["developer_instructions"]
    bridge_tools = {tool["name"] for tool in IonMcpLocalBridge(root).tool_descriptors()}
    assert set(config["mcp_servers"]["ion_local"]["enabled_tools"]).issubset(bridge_tools)


def test_session_start_hook_outputs_additional_context(monkeypatch, capsys):
    root = _repo_root()
    hook_path = root / ".codex" / "hooks" / "ion_session_start_context.py"
    spec = importlib.util.spec_from_file_location("ion_session_start_context", hook_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules["ion_session_start_context"] = module
    spec.loader.exec_module(module)

    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps({"cwd": str(root), "hook_event_name": "SessionStart"})))

    assert module.main() == 0
    payload = json.loads(capsys.readouterr().out)
    context = payload["hookSpecificOutput"]["additionalContext"]
    assert payload["continue"] is True
    assert "ION Codex Solo Boot Context" in context
    assert "Capsule is minimum working context" in context


def test_session_start_hook_fails_soft_outside_active_root(monkeypatch, capsys):
    root = _repo_root()
    hook_path = root / ".codex" / "hooks" / "ion_session_start_context.py"
    spec = importlib.util.spec_from_file_location("ion_session_start_context_outside", hook_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    monkeypatch.setattr(sys, "stdin", io.StringIO(json.dumps({"cwd": "/tmp", "hook_event_name": "SessionStart"})))

    assert module.main() == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["continue"] is True
    assert "outside active ION root" in payload["systemMessage"]
