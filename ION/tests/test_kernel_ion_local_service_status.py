from pathlib import Path

from kernel.ion_local_service_status import LOCAL_SERVICE_SPECS, build_local_service_status


def _seed_templates(root: Path) -> None:
    template_root = root / "ION/09_integrations/systemd/user"
    template_root.mkdir(parents=True, exist_ok=True)
    for spec in LOCAL_SERVICE_SPECS:
        (template_root / spec.template_name).write_text(
            "\n".join(
                [
                    "[Unit]",
                    f"Description={spec.unit_name}",
                    "[Service]",
                    f"ExecStart={spec.command_summary}",
                    "",
                ]
            ),
            encoding="utf-8",
        )


def test_local_service_status_projects_expected_transport_stack(tmp_path):
    _seed_templates(tmp_path)

    result = build_local_service_status(tmp_path, probe_http=False)

    assert result["schema_id"] == "ion.local_service_status.v1"
    assert result["status"] == "configured"
    assert result["service_count"] == 6
    assert result["install_authority"] is False
    assert result["production_authority"] is False
    assert result["live_execution_authority"] is False
    unit_names = {service["unit_name"] for service in result["services"]}
    assert unit_names == {
        "ion-chatops.service",
        "ion-mcp-preview.service",
        "ion-mcp-tunnel.service",
        "ion-action-gateway.service",
        "ion-action-tunnel.service",
        "ion-cockpit-app.service",
    }
    assert {service["tunnel_name"] for service in result["services"] if service["tunnel_name"]} == {"ion-browser", "ion-actions"}
    assert "secret" not in str(result).lower()


def test_local_service_status_reports_missing_templates(tmp_path):
    result = build_local_service_status(tmp_path, probe_http=False)

    assert result["status"] == "missing_template"
    assert result["missing_template_count"] == 6
    assert all("systemd_template_missing" in service["findings"] for service in result["services"])


def test_systemd_templates_match_transport_stack_contract():
    root = Path.cwd()
    template_root = root / "ION/09_integrations/systemd/user"
    expected = {
        "ion-chatops.service.template": ["--port 8767", "kernel.ion_chatops_bridge"],
        "ion-mcp-preview.service.template": ["--port 8765", "kernel.ion_chatgpt_browser_mcp_http_preview"],
        "ion-mcp-tunnel.service.template": ["http://127.0.0.1:8765", "ion-browser"],
        "ion-action-gateway.service.template": ["--port 8777", "kernel.ion_custom_gpt_action_gateway", "EnvironmentFile=__ION_ACTION_GATEWAY_ENV__"],
        "ion-action-tunnel.service.template": ["http://127.0.0.1:8777", "ion-actions"],
        "ion-cockpit-app.service.template": ["--port 8788", "kernel.ion_local_cockpit_app"],
    }

    for filename, needles in expected.items():
        text = (template_root / filename).read_text(encoding="utf-8")
        assert "__ION_ROOT__" in text
        assert "Restart=on-failure" in text
        for needle in needles:
            assert needle in text
        assert "ION_ACTION_GATEWAY_TOKEN=" not in text
        assert "ion_action_gateway.token" not in text
