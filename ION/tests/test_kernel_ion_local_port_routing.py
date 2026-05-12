import json
from pathlib import Path

from kernel.ion_local_port_routing import (
    EXPECTED_CANONICAL_PORTS,
    REGISTRY_RELATIVE_PATH,
    build_local_port_routing_truth,
)


def test_local_port_routing_registry_declares_collision_free_split():
    result = build_local_port_routing_truth(Path.cwd())

    assert result["schema_id"] == "ion.local_port_routing_truth.v1"
    assert result["status"] == "ready"
    assert result["findings"] == []
    assert result["canonical_ports"] == dict(sorted(EXPECTED_CANONICAL_PORTS.items()))
    assert result["production_authority"] is False
    assert result["deployment_authority"] is False
    assert result["live_execution_authority"] is False


def test_local_port_routing_registry_preserves_mcp_and_daimon_split():
    payload = json.loads(Path(REGISTRY_RELATIVE_PATH).read_text(encoding="utf-8"))
    assignments = {row["service_id"]: row for row in payload["assignments"]}

    assert assignments["ion_mcp_preview"]["local_port"] == 8765
    assert assignments["ion_mcp_preview"]["endpoint_path"] == "/mcp"
    assert assignments["ion_mcp_preview"]["tunnel_name"] == "ion-browser"
    assert assignments["ion_action_gateway"]["local_port"] == 8777
    assert assignments["ion_local_cockpit"]["local_port"] == 8788
    assert assignments["daimon_gemini_bridge"]["local_port"] == 8795
    assert assignments["daimon_gemini_bridge"]["migration_required"] is True


def test_local_service_status_embeds_port_routing_truth():
    from kernel.ion_local_service_status import build_local_service_status

    result = build_local_service_status(Path.cwd(), probe_http=False)

    assert result["port_routing"]["status"] == "ready"
    assert result["port_routing"]["canonical_ports"]["ion_mcp_preview"] == 8765
    assert result["port_routing"]["canonical_ports"]["daimon_gemini_bridge"] == 8795
