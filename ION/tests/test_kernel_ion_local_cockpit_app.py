import json
from pathlib import Path

from kernel.ion_local_cockpit_app import build_cockpit_health, build_cockpit_html


def test_local_cockpit_health_is_visibility_only(tmp_path: Path):
    result = build_cockpit_health(tmp_path)

    assert result["schema_id"] == "ion.local_cockpit_app.v1"
    assert result["verdict"] == "ION_LOCAL_COCKPIT_APP_READY"
    assert result["visibility_only"] is True
    assert result["production_authority"] is False
    assert result["live_execution_authority"] is False


def test_local_cockpit_html_renders_codex_and_service_state():
    model = {
        "runtime": {"status": "ready", "shell_root": "/tmp/ion", "blocked": False},
        "top_bar": {"objective": "cockpit smoke", "gate_count": 0, "steward_queue_count": 0, "operator_queue_pending": 0},
        "local_services": {
            "status": "ready",
            "services": [
                {
                    "unit_name": "ion-cockpit-app.service",
                    "status": "ready",
                    "health_url": "http://127.0.0.1:8788/health",
                    "findings": [],
                }
            ],
        },
        "chatgpt_browser_mcp": {
            "transport_state": "TUNNEL_RUNNING_VERIFIED",
            "active_connector_url": "https://ion.helixion.net/mcp",
            "codex_queue_runner": {
                "verdict": "ION_CODEX_QUEUE_RUNNER_READY",
                "queued_request_count": 0,
                "active_process_running": False,
                "next_request_path": None,
                "reconciliation": {"write": False},
            },
            "agent_invocation_broker": {"verdict": "ION_AGENT_INVOCATION_BROKER_READY"},
        },
        "queues": {"human_gates": [], "steward_integration": []},
        "timeline": [{"source": "work", "event_type": "packet", "status": "ready", "detail": "visible"}],
        "receipts": [{"name": "receipt.json", "path": "ION/receipt.json", "authority_class": "WITNESS"}],
        "source_paths": {"work": "ION/05_context/current/ACTIVE_WORK_PACKET.json"},
    }

    html = build_cockpit_html(json.loads(json.dumps(model)))

    assert "ION LOCAL COCKPIT" in html
    assert "cockpit smoke" in html
    assert "ION_CODEX_QUEUE_RUNNER_READY" in html
    assert "ion-cockpit-app.service" in html
    assert "Reconciliation write" in html
