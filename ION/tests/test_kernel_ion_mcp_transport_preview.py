from pathlib import Path

from kernel.ion_mcp_transport_preview import (
    build_transport_preview_report,
    get_sdk_adapter_status,
    handle_streamable_http_preview_request,
)
from kernel.ion_mcp_local_bridge import IonMcpLocalBridge


def ion_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_sdk_adapter_status_is_non_authorizing():
    status = get_sdk_adapter_status()
    assert status.version.startswith("V67_")
    assert status.live_execution_authorized is False
    assert status.adapter_mode in {"official_sdk_available_optional_adapter", "dependency_absent_contract_only"}


def test_streamable_http_preview_rejects_non_post_or_wrong_path(tmp_path):
    bridge = IonMcpLocalBridge(ion_root(), tmp_path / "state")
    wrong_path = handle_streamable_http_preview_request(bridge, method="POST", path="/wrong", headers={}, body={})
    assert wrong_path.status_code == 404
    assert wrong_path.body["live_execution_authorized"] is False
    wrong_method = handle_streamable_http_preview_request(bridge, method="GET", path="/mcp", headers={}, body={})
    assert wrong_method.status_code == 405
    assert wrong_method.body["live_execution_authorized"] is False


def test_streamable_http_preview_supports_tools_call_and_refuses_live(tmp_path):
    bridge = IonMcpLocalBridge(ion_root(), tmp_path / "state")
    mount = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": "ion.mount", "arguments": {"client_name": "pytest-http-preview", "transport": "streamable-http-preview"}},
    }
    response = handle_streamable_http_preview_request(bridge, method="POST", path="/mcp", headers={}, body=mount)
    assert response.status_code == 200
    assert "result" in response.body

    live = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/call",
        "params": {"name": "ion.job.execute_live", "arguments": {}},
    }
    refused = handle_streamable_http_preview_request(bridge, method="POST", path="/mcp", headers={}, body=live)
    assert refused.status_code == 200
    text = refused.body["result"]["content"][0]["text"]
    assert '"execution_resolution": "REFUSED"' in text
    assert '"live_execution_authorized": false' in text


def test_transport_preview_report_preserves_boundary(tmp_path):
    report = build_transport_preview_report(ion_root(), tmp_path / "state")
    assert report.passed is True
    assert set(report.transports) == {"stdio", "streamable_http_preview"}
    assert report.forbidden_resolution_seen is False
    assert report.live_execution_authorized_seen is False
    assert report.kernel_truth_mutation_seen is False
    assert any(step.transport == "stdio" for step in report.steps)
    assert any(step.transport == "streamable_http_preview" for step in report.steps)
    refused = [step for step in report.steps if "ion.job.execute_live" in step.method]
    assert refused
    assert all(step.execution_resolution == "REFUSED" for step in refused)
