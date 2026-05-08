from pathlib import Path

from kernel.ion_deep_operational_cartography import (
    build_core_telemetry_requirements,
    build_deep_operational_cartography,
    build_long_horizon_plan,
    audit_to_dict,
)


def test_deep_operational_cartography_names_core_systems():
    root = Path(__file__).resolve().parents[2]
    audit = build_deep_operational_cartography(root, emitted_at="2026-05-02T00:00:00+00:00")
    data = audit_to_dict(audit)
    system_ids = {item["system_id"] for item in data["systems"]}
    assert data["schema_id"] == "ion.deep_operational_cartography.v105"
    assert "temporal_context_stack" in system_ids
    assert "context_lifecycle_and_metabolism" in system_ids
    assert "joc_cockpit_ui_and_core_telemetry" in system_ids
    assert "v72_mcp_donor_reconciliation_and_current_bridge" in system_ids
    assert "chatgpt_browser_carrier_surface" in system_ids
    assert data["production_authority"] is False


def test_cartography_records_requested_ui_telemetry_gap():
    root = Path(__file__).resolve().parents[2]
    audit = build_deep_operational_cartography(root, emitted_at="2026-05-02T00:00:00+00:00")
    ui = next(item for item in audit.systems if item.system_id == "joc_cockpit_ui_and_core_telemetry")
    joined = "\n".join(ui.disconnected + ui.next_required)
    assert "lane timeline" in joined.lower()
    assert "debug overlay" in joined.lower()
    assert "hydration" in joined.lower()


def test_long_horizon_plan_and_telemetry_requirements_are_non_production():
    root = Path(__file__).resolve().parents[2]
    audit = build_deep_operational_cartography(root, emitted_at="2026-05-02T00:00:00+00:00")
    plan = build_long_horizon_plan(audit)
    telemetry = build_core_telemetry_requirements("2026-05-02T00:00:00+00:00")
    assert plan["production_authority"] is False
    assert telemetry["production_authority"] is False
    assert any(req["id"] == "TEL-001" for req in telemetry["requirements"])
    assert any(phase["phase"] == "P2_front_door_receipt_hydration_and_lane_telemetry" for phase in plan["phase_order"])


def test_cartography_records_v108_mcp_donor_reconciliation_as_bounded_substrate():
    root = Path(__file__).resolve().parents[2]
    audit = build_deep_operational_cartography(root, emitted_at="2026-05-02T00:00:00+00:00")
    mcp = next(item for item in audit.systems if item.system_id == "v72_mcp_donor_reconciliation_and_current_bridge")
    joined = "\n".join(mcp.present + mcp.disconnected + mcp.next_required)
    assert "V108_V72_MCP_DONOR_RECONCILIATION_AUDIT.json" in joined
    assert "live MCP execution authority remains bounded" in joined
    assert audit.production_authority is False
