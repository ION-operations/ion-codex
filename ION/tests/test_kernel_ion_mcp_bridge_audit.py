from __future__ import annotations

import pathlib

from kernel.ion_mcp_bridge_audit import audit_mcp_bridge


def test_mcp_bridge_audit_accepts_repository_root():
    root = pathlib.Path(__file__).resolve().parents[2]
    result = audit_mcp_bridge(root)
    assert result["schema_id"] == "ion.mcp_control_bridge_audit.v1"
    assert "ion_continue" in result["required_tools"]
    assert result["server_label"] == "ion-control"
