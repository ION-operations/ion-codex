"""V68 official MCP SDK wrapper decision and hosted HTTP alpha boundary for ION.

V68 is a boundary branch. It does not promote the official MCP SDK to a hard
runtime dependency, and it does not certify a hosted cloud service, OAuth flow,
or live execution path. Instead, it defines the adapter seam and proves that the
same local bridge contract can be projected into a hosted-HTTP-alpha shape while
preserving ION's V62/V67 dry-run/refusal invariants.

V68 law:
    The dependency-free local bridge remains the canonical founder/local path.
    The official MCP SDK is an optional wrapper boundary, not a new authority.
    Hosted HTTP alpha is a contract preview, not a cloud certification.
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
    FORBIDDEN_TOOL_NAMES,
    PROTOCOL_VERSION,
    VERSION as LOCAL_BRIDGE_VERSION,
    IonMcpLocalBridge,
    handle_jsonrpc_message,
)
from .ion_mcp_transport_preview import (
    handle_streamable_http_preview_request,
    get_sdk_adapter_status,
)

VERSION = "V68_OFFICIAL_MCP_SDK_WRAPPER_OR_HOSTED_HTTP_ALPHA_BOUNDARY"
HOSTED_ALPHA_TRANSPORT = "streamable-http-alpha-boundary"
HOSTED_ALPHA_ENDPOINT = "/mcp"
OFFICIAL_SDK_IMPORT_NAME = "mcp"

REQUIRED_ALPHA_SEQUENCE = (
    ("initialize", {}),
    ("tools/list", {}),
    ("tools/call", {"name": "ion.mount", "arguments": {
        "client_name": "v68-hosted-http-alpha-boundary",
        "transport": HOSTED_ALPHA_TRANSPORT,
        "requested_mode": "dry_run",
        "requested_scopes": [
            "ion.mount.basic",
            "ion.state.read",
            "ion.receipts.read",
            "ion.approvals.read",
            "ion.jobs.plan",
            "ion.jobs.execute.dry_run",
            "ion.bundles.export",
        ],
    }}),
    ("tools/call", {"name": "ion.status", "arguments": {}}),
    ("tools/call", {"name": "ion.boot_packet", "arguments": {}}),
    ("tools/call", {"name": "ion.job.plan", "arguments": {
        "task": {"summary": "V68 hosted HTTP alpha boundary plan check"}
    }}),
    ("tools/call", {"name": "ion.job.submit_dry_run", "arguments": {
        "task": {"summary": "V68 hosted HTTP alpha dry-run submission check"}
    }}),
    ("tools/call", {"name": "ion.daemon.dry_run_step", "arguments": {
        "task": {"summary": "V68 daemon preview must remain dry-run only"}
    }}),
    ("tools/call", {"name": "ion.job.execute_live", "arguments": {
        "task": {"summary": "V68 must refuse live execution"}
    }}),
    ("tools/call", {"name": "ion.provider.dispatch", "arguments": {
        "task": {"summary": "V68 must refuse provider dispatch"}
    }}),
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
class IonMcpSdkWrapperDecision:
    version: str
    official_sdk_available: bool
    official_sdk_import_name: str
    official_sdk_required_for_local: bool
    local_bridge_remains_canonical: bool
    adapter_mode: str
    decision: str
    reasons: tuple[str, ...]
    live_execution_authorized: bool = False
    hosted_cloud_certified: bool = False
    oauth_certified: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IonMcpHostedHttpAlphaProfile:
    profile_id: str
    transport: str
    endpoint_path: str
    mode: str
    public_hosting_certified: bool
    oauth_certified: bool
    tls_required_before_public_exposure: bool
    reverse_proxy_required_before_public_exposure: bool
    allowed_resolutions: tuple[str, ...]
    forbidden_tool_names: tuple[str, ...]
    note: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IonMcpSdkToolContract:
    name: str
    description: str
    input_schema: Mapping[str, Any]
    local_bridge_backed: bool
    live_execution_authorized: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IonMcpHostedHttpAlphaStep:
    step_id: str
    ok: bool
    method: str
    http_status_code: int | None
    execution_resolution: str | None
    live_execution_authorized: bool
    kernel_truth_mutated: bool
    detail: str
    evidence: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IonMcpHostedHttpAlphaBoundaryReport:
    version: str
    bridge_version: str
    protocol_version: str
    created_at: str
    ion_root: str
    state_store_root: str
    passed: bool
    sdk_decision: IonMcpSdkWrapperDecision
    hosted_http_alpha_profile: IonMcpHostedHttpAlphaProfile
    tool_contracts: tuple[IonMcpSdkToolContract, ...]
    steps: tuple[IonMcpHostedHttpAlphaStep, ...]
    allowed_resolutions: tuple[str, ...]
    forbidden_resolution_seen: bool
    live_execution_authorized_seen: bool
    kernel_truth_mutation_seen: bool
    official_sdk_runtime_required: bool = False
    hosted_cloud_certified: bool = False
    oauth_certified: bool = False
    public_endpoint_certified: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["sdk_decision"] = self.sdk_decision.to_dict()
        payload["hosted_http_alpha_profile"] = self.hosted_http_alpha_profile.to_dict()
        payload["tool_contracts"] = tuple(contract.to_dict() for contract in self.tool_contracts)
        payload["steps"] = tuple(step.to_dict() for step in self.steps)
        return payload


def build_sdk_wrapper_decision(import_name: str = OFFICIAL_SDK_IMPORT_NAME) -> IonMcpSdkWrapperDecision:
    sdk_status = get_sdk_adapter_status(import_name)
    available = importlib.util.find_spec(import_name) is not None
    return IonMcpSdkWrapperDecision(
        version=VERSION,
        official_sdk_available=available and sdk_status.official_sdk_available,
        official_sdk_import_name=import_name,
        official_sdk_required_for_local=False,
        local_bridge_remains_canonical=True,
        adapter_mode="official_sdk_optional_wrapper_ready" if available else "official_sdk_absent_contract_boundary",
        decision="KEEP_NO_DEPENDENCY_LOCAL_BRIDGE_CANONICAL_AND_WRAP_SDK_OPTIONALLY",
        reasons=(
            "V64-V67 already prove a dependency-free local bridge contract for founder/local use.",
            "The official MCP SDK is valuable for hosted/client compatibility but must not become a new authority center.",
            "ION must preserve deterministic local operation even when external SDK packages are unavailable.",
            "Hosted HTTP alpha requires OAuth, TLS, proxy, tenant isolation, and receipt hardening before public certification.",
        ),
        live_execution_authorized=False,
        hosted_cloud_certified=False,
        oauth_certified=False,
    )


def build_hosted_http_alpha_profile() -> IonMcpHostedHttpAlphaProfile:
    return IonMcpHostedHttpAlphaProfile(
        profile_id="hosted_http_alpha_boundary_contract",
        transport=HOSTED_ALPHA_TRANSPORT,
        endpoint_path=HOSTED_ALPHA_ENDPOINT,
        mode="contract_preview_only",
        public_hosting_certified=False,
        oauth_certified=False,
        tls_required_before_public_exposure=True,
        reverse_proxy_required_before_public_exposure=True,
        allowed_resolutions=tuple(sorted(ALLOWED_RESOLUTIONS)),
        forbidden_tool_names=tuple(sorted(FORBIDDEN_TOOL_NAMES)),
        note="V68 previews the hosted HTTP shape only. It is not a public cloud endpoint, OAuth certification, or live execution path.",
    )


def build_sdk_tool_contracts(bridge: IonMcpLocalBridge) -> tuple[IonMcpSdkToolContract, ...]:
    contracts: list[IonMcpSdkToolContract] = []
    for descriptor in bridge.tool_descriptors():
        contracts.append(IonMcpSdkToolContract(
            name=str(descriptor.get("name")),
            description=str(descriptor.get("description", "")),
            input_schema=descriptor.get("inputSchema", {"type": "object"}),
            local_bridge_backed=True,
            live_execution_authorized=False,
        ))
    return tuple(contracts)


def _response_step(
    *,
    step_id: str,
    method: str,
    response: Mapping[str, Any],
    http_status_code: int | None,
    expect_refusal: bool = False,
) -> IonMcpHostedHttpAlphaStep:
    tool_result = _extract_tool_result(response)
    resolution = tool_result.get("execution_resolution") if tool_result else None
    live = bool(tool_result.get("live_execution_authorized")) if tool_result else False
    mutated = bool(tool_result.get("kernel_truth_mutated")) if tool_result else False
    has_error = "error" in response
    if expect_refusal:
        ok = tool_result is not None and resolution == "REFUSED" and not live and not mutated
    else:
        ok = not has_error and not live and not mutated
        if resolution is not None:
            ok = ok and resolution in ALLOWED_RESOLUTIONS
    detail = "ok" if ok else "failed"
    return IonMcpHostedHttpAlphaStep(
        step_id=step_id,
        ok=ok,
        method=method,
        http_status_code=http_status_code,
        execution_resolution=resolution,
        live_execution_authorized=live,
        kernel_truth_mutated=mutated,
        detail=detail,
        evidence={"response": dict(response) if isinstance(response, Mapping) else response},
    )


def build_hosted_http_alpha_boundary_report(
    ion_root: str | Path,
    state_store_root: str | Path | None = None,
) -> IonMcpHostedHttpAlphaBoundaryReport:
    ion_root_path = Path(ion_root).resolve()
    if ion_root_path.name != "ION" and (ion_root_path / "ION").exists():
        ion_root_path = (ion_root_path / "ION").resolve()
    state_root = Path(state_store_root).resolve() if state_store_root else (
        ion_root_path / "05_context" / "runtime_state" / "v68_hosted_http_alpha_boundary"
    )
    bridge = IonMcpLocalBridge(ion_root_path, state_root)

    steps: list[IonMcpHostedHttpAlphaStep] = []

    # Basic HTTP boundary hardening preview: the alpha endpoint is POST-only and
    # path-bound even before public deployment, OAuth, or reverse-proxy hardening.
    wrong_method = handle_streamable_http_preview_request(
        bridge,
        method="GET",
        path=HOSTED_ALPHA_ENDPOINT,
        headers={},
        body=None,
    )
    steps.append(IonMcpHostedHttpAlphaStep(
        step_id="reject_get_mcp",
        ok=wrong_method.status_code == 405 and not bool(wrong_method.body.get("live_execution_authorized")),
        method="GET /mcp",
        http_status_code=wrong_method.status_code,
        execution_resolution=None,
        live_execution_authorized=False,
        kernel_truth_mutated=False,
        detail="GET /mcp rejected as expected" if wrong_method.status_code == 405 else "GET /mcp was not rejected as expected",
        evidence=wrong_method.to_dict(),
    ))

    wrong_path = handle_streamable_http_preview_request(
        bridge,
        method="POST",
        path="/wrong",
        headers={"content-type": "application/json"},
        body={},
    )
    steps.append(IonMcpHostedHttpAlphaStep(
        step_id="reject_wrong_path",
        ok=wrong_path.status_code == 404 and not bool(wrong_path.body.get("live_execution_authorized")),
        method="POST /wrong",
        http_status_code=wrong_path.status_code,
        execution_resolution=None,
        live_execution_authorized=False,
        kernel_truth_mutated=False,
        detail="wrong path rejected as expected" if wrong_path.status_code == 404 else "wrong path was not rejected as expected",
        evidence=wrong_path.to_dict(),
    ))

    for index, (method, params) in enumerate(REQUIRED_ALPHA_SEQUENCE, start=1):
        message = _jsonrpc_message(index, method, params)
        http_response = handle_streamable_http_preview_request(
            bridge,
            method="POST",
            path=HOSTED_ALPHA_ENDPOINT,
            headers={"content-type": "application/json", "origin": "http://localhost"},
            body=message,
        )
        response = http_response.body
        tool_name = params.get("name", "") if isinstance(params, Mapping) else ""
        expect_refusal = tool_name in FORBIDDEN_TOOL_NAMES or tool_name.endswith(".execute_live")
        steps.append(_response_step(
            step_id=f"alpha_sequence_{index}_{method}_{tool_name}".rstrip("_"),
            method=f"{method}:{tool_name}".rstrip(":"),
            response=response,
            http_status_code=http_response.status_code,
            expect_refusal=expect_refusal,
        ))

    # A live-candidate mount must be refused through the same bridge path.
    live_mount_message = _jsonrpc_message(900, "tools/call", {
        "name": "ion.mount",
        "arguments": {
            "client_name": "v68-live-candidate-refusal-check",
            "transport": HOSTED_ALPHA_TRANSPORT,
            "requested_mode": "live_candidate",
        },
    })
    live_mount = handle_streamable_http_preview_request(
        bridge,
        method="POST",
        path=HOSTED_ALPHA_ENDPOINT,
        headers={"content-type": "application/json"},
        body=live_mount_message,
    )
    steps.append(_response_step(
        step_id="refuse_live_candidate_mount",
        method="tools/call:ion.mount(live_candidate)",
        response=live_mount.body,
        http_status_code=live_mount.status_code,
        expect_refusal=True,
    ))

    forbidden_resolution_seen = any(
        step.execution_resolution is not None and step.execution_resolution not in ALLOWED_RESOLUTIONS
        for step in steps
    )
    live_execution_authorized_seen = any(step.live_execution_authorized for step in steps)
    kernel_truth_mutation_seen = any(step.kernel_truth_mutated for step in steps)
    passed = all(step.ok for step in steps) and not forbidden_resolution_seen and not live_execution_authorized_seen and not kernel_truth_mutation_seen

    return IonMcpHostedHttpAlphaBoundaryReport(
        version=VERSION,
        bridge_version=LOCAL_BRIDGE_VERSION,
        protocol_version=PROTOCOL_VERSION,
        created_at=_utc_now(),
        ion_root=str(ion_root_path),
        state_store_root=str(state_root),
        passed=passed,
        sdk_decision=build_sdk_wrapper_decision(),
        hosted_http_alpha_profile=build_hosted_http_alpha_profile(),
        tool_contracts=build_sdk_tool_contracts(bridge),
        steps=tuple(steps),
        allowed_resolutions=tuple(sorted(ALLOWED_RESOLUTIONS)),
        forbidden_resolution_seen=forbidden_resolution_seen,
        live_execution_authorized_seen=live_execution_authorized_seen,
        kernel_truth_mutation_seen=kernel_truth_mutation_seen,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run V68 ION MCP SDK wrapper and hosted HTTP alpha boundary report.")
    parser.add_argument("--ion-root", default=".", help="Path to ION/ or a snapshot root containing ION/")
    parser.add_argument("--state-store-root", default=None, help="Optional state store root for boundary receipts")
    parser.add_argument("--json", action="store_true", help="Print full JSON report")
    parser.add_argument("--sdk-decision", action="store_true", help="Print SDK wrapper decision only")
    args = parser.parse_args(argv)
    if args.sdk_decision:
        print(json.dumps(build_sdk_wrapper_decision().to_dict(), indent=2, sort_keys=True))
        return 0
    report = build_hosted_http_alpha_boundary_report(args.ion_root, args.state_store_root)
    print(json.dumps(report.to_dict(), indent=2 if args.json else None, sort_keys=True))
    return 0 if report.passed else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
