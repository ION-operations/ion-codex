"""V67 MCP transport preview and SDK-adapter seam for ION.

Compares the existing dependency-free local MCP bridge across stdio JSON-RPC
and a local Streamable-HTTP-style POST preview. Exposes an official-SDK adapter
status seam without requiring the SDK at runtime. V67 remains preview-only: no
OAuth, cloud hosting, live execution, shell execution, provider calls, browser
mutation, credential access, or canonical governed-write authority.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any, Mapping

from .ion_mcp_local_bridge import (
    ALLOWED_RESOLUTIONS,
    PROTOCOL_VERSION,
    VERSION as LOCAL_BRIDGE_VERSION,
    IonMcpLocalBridge,
    handle_jsonrpc_message,
)

VERSION = "V67_OFFICIAL_MCP_SDK_ADAPTER_AND_STREAMABLE_HTTP_PREVIEW"
SUPPORTED_TRANSPORTS = ("stdio", "streamable_http_preview")
REQUIRED_SEQUENCE = (
    ("initialize", {}),
    ("tools/list", {}),
    ("tools/call", {"name": "ion.mount", "arguments": {"client_name": "v67-transport-preview", "transport": "stdio", "requested_mode": "dry_run"}}),
    ("tools/call", {"name": "ion.status", "arguments": {}}),
    ("tools/call", {"name": "ion.job.plan", "arguments": {"task": {"summary": "V67 transport equivalence dry-run plan"}}}),
    ("tools/call", {"name": "ion.job.submit_dry_run", "arguments": {"task": {"summary": "V67 transport equivalence dry-run submission"}}}),
    ("tools/call", {"name": "ion.job.execute_live", "arguments": {"task": {"summary": "must be refused"}}}),
)


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _jsonrpc_message(message_id: int, method: str, params: Mapping[str, Any] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"jsonrpc": "2.0", "id": message_id, "method": method}
    if params is not None:
        payload["params"] = dict(params)
    return payload


def _extract_tool_result(response: Mapping[str, Any]) -> dict[str, Any] | None:
    try:
        result = response.get("result")
        if not isinstance(result, Mapping):
            return None
        content = result.get("content")
        if not isinstance(content, list) or not content:
            return None
        first = content[0]
        if not isinstance(first, Mapping):
            return None
        text = first.get("text")
        if not isinstance(text, str):
            return None
        parsed = json.loads(text)
        return parsed if isinstance(parsed, dict) else None
    except Exception:
        return None


@dataclass(frozen=True)
class IonMcpSdkAdapterStatus:
    version: str
    official_sdk_available: bool
    import_name_checked: str
    adapter_mode: str
    live_execution_authorized: bool = False
    note: str = "V67 exposes an adapter seam only; official SDK is optional and not required for local dry-run transport preview."

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IonMcpHttpPreviewResponse:
    status_code: int
    headers: Mapping[str, str]
    body: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IonMcpTransportStep:
    transport: str
    method: str
    ok: bool
    status_code: int | None
    response: Mapping[str, Any]
    execution_resolution: str | None
    live_execution_authorized: bool
    kernel_truth_mutated: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IonMcpTransportPreviewReport:
    version: str
    bridge_version: str
    protocol_version: str
    created_at: str
    ion_root: str
    state_store_root: str
    passed: bool
    sdk_adapter: IonMcpSdkAdapterStatus
    transports: tuple[str, ...]
    steps: tuple[IonMcpTransportStep, ...]
    allowed_resolutions: tuple[str, ...]
    forbidden_resolution_seen: bool
    live_execution_authorized_seen: bool
    kernel_truth_mutation_seen: bool
    streamable_http_preview_only: bool = True
    hosted_cloud_certified: bool = False
    oauth_certified: bool = False
    official_sdk_runtime_required: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["sdk_adapter"] = self.sdk_adapter.to_dict()
        payload["steps"] = tuple(step.to_dict() for step in self.steps)
        return payload


def get_sdk_adapter_status(import_name: str = "mcp") -> IonMcpSdkAdapterStatus:
    available = importlib.util.find_spec(import_name) is not None
    return IonMcpSdkAdapterStatus(
        version=VERSION,
        official_sdk_available=available,
        import_name_checked=import_name,
        adapter_mode="official_sdk_available_optional_adapter" if available else "dependency_absent_contract_only",
    )


def handle_streamable_http_preview_request(
    bridge: IonMcpLocalBridge,
    *,
    method: str,
    path: str,
    headers: Mapping[str, str] | None,
    body: str | bytes | Mapping[str, Any] | None,
) -> IonMcpHttpPreviewResponse:
    """Handle a local Streamable-HTTP-style JSON-RPC request."""
    response_headers = {
        "content-type": "application/json",
        "x-ion-mcp-transport": "streamable-http-preview",
        "x-ion-live-execution-authorized": "false",
    }
    if method.upper() != "POST" or path != "/mcp":
        return IonMcpHttpPreviewResponse(
            status_code=405 if path == "/mcp" else 404,
            headers=response_headers,
            body={"error": "V67 preview supports POST /mcp only", "live_execution_authorized": False},
        )
    try:
        if isinstance(body, Mapping):
            message = dict(body)
        elif isinstance(body, bytes):
            message = json.loads(body.decode("utf-8"))
        elif isinstance(body, str):
            message = json.loads(body or "{}")
        else:
            message = {}
    except Exception as exc:
        return IonMcpHttpPreviewResponse(
            status_code=400,
            headers=response_headers,
            body={"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": "invalid JSON", "data": str(exc)}},
        )
    response = handle_jsonrpc_message(bridge, message)
    if response is None:
        return IonMcpHttpPreviewResponse(status_code=202, headers=response_headers, body={"accepted": True})
    status = 200 if not (isinstance(response, Mapping) and response.get("error")) else 400
    return IonMcpHttpPreviewResponse(status_code=status, headers=response_headers, body=response)


def _run_stdio_sequence(bridge: IonMcpLocalBridge) -> list[IonMcpTransportStep]:
    steps: list[IonMcpTransportStep] = []
    for index, (method, params) in enumerate(REQUIRED_SEQUENCE, start=1):
        message = _jsonrpc_message(index, method, params)
        response = handle_jsonrpc_message(bridge, message) or {"notification_accepted": True}
        tool_result = _extract_tool_result(response)
        resolution = tool_result.get("execution_resolution") if tool_result else None
        live = bool(tool_result.get("live_execution_authorized")) if tool_result else False
        mutated = bool(tool_result.get("kernel_truth_mutated")) if tool_result else False
        ok = "error" not in response and not live and not mutated
        if method == "tools/call" and params.get("name") == "ion.job.execute_live":
            ok = tool_result is not None and resolution == "REFUSED" and not live and not mutated
        steps.append(IonMcpTransportStep("stdio", f"{method}:{params.get('name', '')}".rstrip(":"), ok, None, response, resolution, live, mutated))
    return steps


def _run_http_sequence(bridge: IonMcpLocalBridge) -> list[IonMcpTransportStep]:
    steps: list[IonMcpTransportStep] = []
    for index, (method, params) in enumerate(REQUIRED_SEQUENCE, start=1):
        http_params = dict(params)
        if method == "tools/call" and isinstance(http_params.get("arguments"), Mapping):
            args = dict(http_params["arguments"])
            if http_params.get("name") == "ion.mount":
                args["transport"] = "streamable-http-preview"
            http_params["arguments"] = args
        message = _jsonrpc_message(index, method, http_params)
        http_response = handle_streamable_http_preview_request(
            bridge,
            method="POST",
            path="/mcp",
            headers={"content-type": "application/json"},
            body=message,
        )
        response = http_response.body
        tool_result = _extract_tool_result(response)
        resolution = tool_result.get("execution_resolution") if tool_result else None
        live = bool(tool_result.get("live_execution_authorized")) if tool_result else False
        mutated = bool(tool_result.get("kernel_truth_mutated")) if tool_result else False
        ok = http_response.status_code in {200, 202} and "error" not in response and not live and not mutated
        if method == "tools/call" and http_params.get("name") == "ion.job.execute_live":
            ok = tool_result is not None and resolution == "REFUSED" and not live and not mutated
        steps.append(IonMcpTransportStep(
            "streamable_http_preview",
            f"{method}:{http_params.get('name', '')}".rstrip(":"),
            ok,
            http_response.status_code,
            response,
            resolution,
            live,
            mutated,
        ))
    return steps


def build_transport_preview_report(ion_root: str | Path, state_store_root: str | Path | None = None) -> IonMcpTransportPreviewReport:
    ion_root_path = Path(ion_root).resolve()
    if ion_root_path.name != "ION" and (ion_root_path / "ION").exists():
        ion_root_path = (ion_root_path / "ION").resolve()
    state_root = Path(state_store_root).resolve() if state_store_root else (ion_root_path / "05_context" / "runtime_state" / "v67_mcp_transport_preview")
    stdio_bridge = IonMcpLocalBridge(ion_root_path, state_root / "stdio")
    http_bridge = IonMcpLocalBridge(ion_root_path, state_root / "streamable_http_preview")
    steps = tuple([*_run_stdio_sequence(stdio_bridge), *_run_http_sequence(http_bridge)])
    forbidden_resolution_seen = any(step.execution_resolution not in {None, *ALLOWED_RESOLUTIONS} for step in steps)
    live_execution_authorized_seen = any(step.live_execution_authorized for step in steps)
    kernel_truth_mutation_seen = any(step.kernel_truth_mutated for step in steps)
    passed = all(step.ok for step in steps) and not forbidden_resolution_seen and not live_execution_authorized_seen and not kernel_truth_mutation_seen
    return IonMcpTransportPreviewReport(
        version=VERSION,
        bridge_version=LOCAL_BRIDGE_VERSION,
        protocol_version=PROTOCOL_VERSION,
        created_at=_utc_now(),
        ion_root=str(ion_root_path),
        state_store_root=str(state_root),
        passed=passed,
        sdk_adapter=get_sdk_adapter_status(),
        transports=SUPPORTED_TRANSPORTS,
        steps=steps,
        allowed_resolutions=tuple(sorted(ALLOWED_RESOLUTIONS)),
        forbidden_resolution_seen=forbidden_resolution_seen,
        live_execution_authorized_seen=live_execution_authorized_seen,
        kernel_truth_mutation_seen=kernel_truth_mutation_seen,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run V67 ION MCP transport preview certification.")
    parser.add_argument("--ion-root", default=".", help="Path to ION/ or a snapshot root containing ION/")
    parser.add_argument("--state-store-root", default=None, help="Optional state store root for preview receipts")
    parser.add_argument("--json", action="store_true", help="Print full JSON report")
    parser.add_argument("--sdk-status", action="store_true", help="Print official SDK adapter status only")
    args = parser.parse_args(argv)
    if args.sdk_status:
        print(json.dumps(get_sdk_adapter_status().to_dict(), indent=2, sort_keys=True))
        return 0
    report = build_transport_preview_report(args.ion_root, args.state_store_root)
    print(json.dumps(report.to_dict(), indent=2 if args.json else None, sort_keys=True))
    return 0 if report.passed else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
