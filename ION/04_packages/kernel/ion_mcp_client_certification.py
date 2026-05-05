"""V66 local MCP client certification surface for ION.

This module certifies the V64/V65 local MCP bridge as a stable, bounded
agent-facing socket for local MCP-capable clients.

It does not connect to real external clients. Instead it defines ION-owned
client profiles and validates the bridge contract those clients must receive:
read-only mount, dry-run planning, approval-required dry-run submission, and
refusal of live execution.

V66 law:
    Client certification proves compatibility posture, not execution authority.
    A certified client may mount, inspect, plan, and queue dry-runs only.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import argparse
import json
from pathlib import Path
from typing import Any, Mapping

from .ion_mcp_local_bridge import (
    ALLOWED_RESOLUTIONS,
    DRY_RUN_TOOLS,
    FORBIDDEN_TOOL_NAMES,
    READ_ONLY_TOOLS,
    VERSION as BRIDGE_VERSION,
    IonMcpLocalBridge,
    IonMcpToolResult,
)

VERSION = "V66_LOCAL_MCP_SDK_COMPATIBILITY_AND_CLIENT_CERTIFICATION"

REQUIRED_BASELINE_TOOLS = tuple(sorted({
    "ion.mount",
    "ion.status",
    "ion.boot_packet",
    "ion.horizon.current",
    "ion.receipts.list",
    "ion.approvals.list",
    "ion.job.plan",
    "ion.job.submit_dry_run",
    "ion.daemon.dry_run_step",
    "ion.bundle.export_preview",
}))

FORBIDDEN_BASELINE_TOOLS = tuple(sorted(FORBIDDEN_TOOL_NAMES | {
    "ion.job.execute_live",
    "ion.execute",
    "ion.shell.run",
    "ion.provider.dispatch",
}))


@dataclass(frozen=True)
class IonMcpClientProfile:
    """ION-owned profile for a local MCP-capable client."""

    profile_id: str
    display_name: str
    transport: str
    config_path: str
    certification_mode: str = "local_stdio_contract"
    required_tools: tuple[str, ...] = REQUIRED_BASELINE_TOOLS
    forbidden_tools: tuple[str, ...] = FORBIDDEN_BASELINE_TOOLS
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


DEFAULT_CLIENT_PROFILES = (
    IonMcpClientProfile(
        profile_id="generic_stdio",
        display_name="Generic stdio MCP client",
        transport="stdio",
        config_path="ION/examples/mcp/generic-stdio.json",
        notes="Baseline JSON-RPC stdio contract used by the V65 smoke harness.",
    ),
    IonMcpClientProfile(
        profile_id="cursor_local_stdio",
        display_name="Cursor local MCP profile",
        transport="stdio",
        config_path="ION/examples/mcp/cursor.mcp.json",
        notes="Cursor-style local stdio configuration example; certification is contract-level, not live IDE attestation.",
    ),
    IonMcpClientProfile(
        profile_id="vscode_local_stdio",
        display_name="VS Code local MCP profile",
        transport="stdio",
        config_path="ION/examples/mcp/vscode.mcp.json",
        notes="VS Code-style local stdio configuration example; certification is contract-level, not live IDE attestation.",
    ),
    IonMcpClientProfile(
        profile_id="codex_local_stdio",
        display_name="Codex local MCP profile",
        transport="stdio",
        config_path="ION/examples/mcp/codex.config.toml",
        notes="Codex-style local stdio configuration example; certification is contract-level, not live Codex attestation.",
    ),
)


@dataclass(frozen=True)
class IonMcpCertificationCheck:
    check_id: str
    ok: bool
    detail: str
    evidence: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IonMcpClientCertification:
    profile: IonMcpClientProfile
    passed: bool
    checks: tuple[IonMcpCertificationCheck, ...]

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["profile"] = self.profile.to_dict()
        payload["checks"] = tuple(check.to_dict() for check in self.checks)
        return payload


@dataclass(frozen=True)
class IonMcpClientCertificationReport:
    version: str
    bridge_version: str
    created_at: str
    ion_root: str
    state_store_root: str
    passed: bool
    profiles: tuple[IonMcpClientCertification, ...]
    allowed_resolutions: tuple[str, ...]
    forbidden_resolution_seen: bool
    live_execution_authorized_seen: bool
    kernel_truth_mutation_seen: bool
    certification_scope: str = "contract-level local bridge certification"
    live_client_attestation: bool = False
    hosted_chatgpt_certified: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["profiles"] = tuple(profile.to_dict() for profile in self.profiles)
        return payload


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _as_payload(result: IonMcpToolResult) -> dict[str, Any]:
    payload = result.to_dict()
    payload.setdefault("payload", {})
    return payload


def _check_tool_surface(bridge: IonMcpLocalBridge, profile: IonMcpClientProfile) -> IonMcpCertificationCheck:
    descriptors = bridge.tool_descriptors()
    tool_names = {descriptor.get("name") for descriptor in descriptors}
    missing_required = sorted(set(profile.required_tools) - tool_names)
    exposed_forbidden = sorted(set(profile.forbidden_tools) & tool_names)
    ok = not missing_required and not exposed_forbidden
    return IonMcpCertificationCheck(
        check_id="tool_surface",
        ok=ok,
        detail="required tools exposed and forbidden tools absent" if ok else "tool surface mismatch",
        evidence={
            "required_count": len(profile.required_tools),
            "available_count": len(tool_names),
            "missing_required": missing_required,
            "exposed_forbidden": exposed_forbidden,
            "read_only_tools": sorted(READ_ONLY_TOOLS),
            "dry_run_tools": sorted(DRY_RUN_TOOLS),
        },
    )


def _check_config_example(ion_root: Path, profile: IonMcpClientProfile) -> IonMcpCertificationCheck:
    snapshot_root = ion_root.parent if ion_root.name == "ION" else ion_root
    path = snapshot_root / profile.config_path
    exists = path.exists() and path.is_file()
    content = path.read_text(encoding="utf-8", errors="replace")[:4000] if exists else ""
    mentions_bridge = "ion_mcp_local_bridge" in content or "kernel.ion_mcp_local_bridge" in content
    mentions_stdio = "stdio" in content.lower() or profile.transport == "stdio"
    ok = exists and mentions_bridge and mentions_stdio
    return IonMcpCertificationCheck(
        check_id="config_example",
        ok=ok,
        detail="client config example exists and points to the local bridge" if ok else "client config example is missing or incomplete",
        evidence={
            "path": str(path),
            "exists": exists,
            "mentions_bridge": mentions_bridge,
            "mentions_stdio": mentions_stdio,
            "transport": profile.transport,
        },
    )


def _check_mount_and_boundary(bridge: IonMcpLocalBridge, profile: IonMcpClientProfile) -> IonMcpCertificationCheck:
    mount = bridge.call_tool("ion.mount", {
        "client_name": profile.profile_id,
        "transport": profile.transport,
        "requested_mode": "dry_run",
        "workspace_id": "local-founder",
    })
    payload = _as_payload(mount)
    session_id = payload.get("session_id")
    plan = bridge.call_tool("ion.job.plan", {
        "session_id": session_id,
        "task": {"summary": f"V66 certification plan for {profile.profile_id}"},
    })
    submit = bridge.call_tool("ion.job.submit_dry_run", {
        "session_id": session_id,
        "task": {"summary": f"V66 certification dry-run submit for {profile.profile_id}"},
    })
    live = bridge.call_tool("ion.job.execute_live", {"session_id": session_id})

    result_payloads = [_as_payload(result) for result in (mount, plan, submit, live)]
    resolutions = [payload.get("execution_resolution") for payload in result_payloads]
    live_flags = [bool(payload.get("live_execution_authorized")) for payload in result_payloads]
    mutation_flags = [bool(payload.get("kernel_truth_mutated")) for payload in result_payloads]

    ok = (
        payload.get("execution_resolution") == "READ_ONLY"
        and bool(session_id)
        and _as_payload(plan).get("execution_resolution") == "DRY_RUN"
        and _as_payload(submit).get("execution_resolution") == "APPROVAL_REQUIRED"
        and _as_payload(live).get("execution_resolution") == "REFUSED"
        and not any(live_flags)
        and not any(mutation_flags)
        and all(resolution in ALLOWED_RESOLUTIONS for resolution in resolutions)
    )
    return IonMcpCertificationCheck(
        check_id="mount_plan_submit_refuse_boundary",
        ok=ok,
        detail="mount, dry-run plan, approval-required submit, and live refusal all behaved lawfully" if ok else "mount/dry-run/refusal boundary failed",
        evidence={
            "session_id": session_id,
            "resolutions": resolutions,
            "live_execution_authorized_flags": live_flags,
            "kernel_truth_mutated_flags": mutation_flags,
            "allowed_resolutions": sorted(ALLOWED_RESOLUTIONS),
        },
    )


def certify_client_profile(
    ion_root: str | Path,
    profile: IonMcpClientProfile,
    state_store_root: str | Path | None = None,
) -> IonMcpClientCertification:
    """Certify one client profile against the local ION bridge contract."""

    ion_root = Path(ion_root).resolve()
    if ion_root.name != "ION" and (ion_root / "ION").exists():
        ion_root = (ion_root / "ION").resolve()
    bridge_state = Path(state_store_root).resolve() / profile.profile_id if state_store_root else None
    bridge = IonMcpLocalBridge(ion_root=ion_root, state_store_root=bridge_state)
    checks = (
        _check_tool_surface(bridge, profile),
        _check_config_example(ion_root, profile),
        _check_mount_and_boundary(bridge, profile),
    )
    return IonMcpClientCertification(
        profile=profile,
        passed=all(check.ok for check in checks),
        checks=checks,
    )


def certify_all_clients(
    ion_root: str | Path,
    state_store_root: str | Path | None = None,
    profiles: tuple[IonMcpClientProfile, ...] = DEFAULT_CLIENT_PROFILES,
) -> IonMcpClientCertificationReport:
    """Run contract-level V66 certification for all known local client profiles."""

    ion_root = Path(ion_root).resolve()
    if ion_root.name != "ION" and (ion_root / "ION").exists():
        ion_root = (ion_root / "ION").resolve()
    state_root = Path(state_store_root).resolve() if state_store_root else (
        ion_root / "05_context" / "runtime_state" / "v66_local_client_certification"
    )
    state_root.mkdir(parents=True, exist_ok=True)

    certifications = tuple(
        certify_client_profile(ion_root=ion_root, profile=profile, state_store_root=state_root)
        for profile in profiles
    )
    all_payloads: list[Mapping[str, Any]] = []
    for certification in certifications:
        for check in certification.checks:
            all_payloads.append(check.evidence)

    forbidden_resolution_seen = any(
        resolution not in ALLOWED_RESOLUTIONS or resolution == "LIVE_EXECUTED"
        for payload in all_payloads
        for resolution in payload.get("resolutions", [])
    )
    live_execution_authorized_seen = any(
        flag
        for payload in all_payloads
        for flag in payload.get("live_execution_authorized_flags", [])
    )
    kernel_truth_mutation_seen = any(
        flag
        for payload in all_payloads
        for flag in payload.get("kernel_truth_mutated_flags", [])
    )
    passed = (
        all(certification.passed for certification in certifications)
        and not forbidden_resolution_seen
        and not live_execution_authorized_seen
        and not kernel_truth_mutation_seen
    )
    return IonMcpClientCertificationReport(
        version=VERSION,
        bridge_version=BRIDGE_VERSION,
        created_at=_utc_now(),
        ion_root=str(ion_root),
        state_store_root=str(state_root),
        passed=passed,
        profiles=certifications,
        allowed_resolutions=tuple(sorted(ALLOWED_RESOLUTIONS)),
        forbidden_resolution_seen=forbidden_resolution_seen,
        live_execution_authorized_seen=live_execution_authorized_seen,
        kernel_truth_mutation_seen=kernel_truth_mutation_seen,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run V66 local MCP client certification.")
    parser.add_argument("--ion-root", default=".", help="Path to ION/ or snapshot root containing ION/")
    parser.add_argument("--state-store-root", default=None, help="Optional certification state root")
    parser.add_argument("--json", action="store_true", help="Emit JSON certification report")
    args = parser.parse_args(argv)
    report = certify_all_clients(args.ion_root, args.state_store_root)
    payload = report.to_dict()
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(f"ION MCP client certification passed: {report.passed}")
        for certification in report.profiles:
            print(f"- {certification.profile.profile_id}: {'OK' if certification.passed else 'FAIL'}")
            for check in certification.checks:
                print(f"  - {check.check_id}: {'OK' if check.ok else 'FAIL'} — {check.detail}")
    return 0 if report.passed else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
