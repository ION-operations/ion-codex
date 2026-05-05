"""ION V108 V72 MCP donor reconciliation audit.

This audit records the bounded restoration of V72's MCP substrate into the
current protected trunk. It is deliberately narrow: it imports/restores MCP
source surfaces only, excludes old runtime session receipts, grants no live MCP
execution authority, and preserves the current Cursor/MCP control bridge as the
active carrier-facing surface.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VERSION_LINE = "V108_V72_MCP_DONOR_RECONCILIATION"
SCHEMA_ID = "ion.v72_mcp_donor_reconciliation_audit.v1"
REPORT_REL = Path("ION/05_context/current/V108_V72_MCP_DONOR_RECONCILIATION_AUDIT.json")

REQUIRED_DONOR_SURFACES: tuple[str, ...] = (
    "ION/00_BOOTSTRAP/V63_ION_MCP_MOUNT_AND_ACCOUNT_CONNECTION_PROTOCOL_LOCK.md",
    "ION/00_BOOTSTRAP/V64_LOCAL_MCP_BRIDGE_LOCK.md",
    "ION/00_BOOTSTRAP/V65_LOCAL_MCP_CLIENT_CONFIG_AND_SMOKE_HARNESS_LOCK.md",
    "ION/00_BOOTSTRAP/V66_LOCAL_MCP_SDK_COMPATIBILITY_AND_CLIENT_CERTIFICATION_LOCK.md",
    "ION/00_BOOTSTRAP/V67_MCP_SDK_ADAPTER_AND_STREAMABLE_HTTP_PREVIEW_LOCK.md",
    "ION/00_BOOTSTRAP/V68_MCP_SDK_WRAPPER_AND_HOSTED_HTTP_ALPHA_BOUNDARY_LOCK.md",
    "ION/00_BOOTSTRAP/V69_HOSTED_MCP_AUTH_AND_ACCOUNT_WORKSPACE_ALPHA_LOCK.md",
    "ION/00_BOOTSTRAP/V70_HOSTED_MCP_OAUTH_AND_STREAMABLE_HTTP_IMPLEMENTATION_PREVIEW_LOCK.md",
    "ION/02_architecture/ION_MCP_FRONT_DOOR_AND_MOUNT_SESSION_PROTOCOL.md",
    "ION/02_architecture/ION_LOCAL_MCP_BRIDGE_TO_KERNEL_AND_DAEMON_PROTOCOL.md",
    "ION/02_architecture/ION_ACCOUNT_WORKSPACE_AND_STATE_ROOT_PROTOCOL.md",
    "ION/02_architecture/ION_V66_LOCAL_MCP_CLIENT_CERTIFICATION_PROTOCOL.md",
    "ION/02_architecture/ION_V67_MCP_SDK_ADAPTER_AND_STREAMABLE_HTTP_PREVIEW_PROTOCOL.md",
    "ION/02_architecture/ION_V68_MCP_SDK_WRAPPER_AND_HOSTED_HTTP_ALPHA_BOUNDARY_PROTOCOL.md",
    "ION/02_architecture/ION_V69_HOSTED_MCP_AUTH_AND_ACCOUNT_WORKSPACE_ALPHA_PROTOCOL.md",
    "ION/02_architecture/ION_V70_HOSTED_MCP_OAUTH_AND_STREAMABLE_HTTP_IMPLEMENTATION_PREVIEW_PROTOCOL.md",
    "ION/03_registry/ion_mcp_mount_session.schema.json",
    "ION/03_registry/ion_mcp_local_bridge_tool_policy.yaml",
    "ION/03_registry/ion_mcp_client_config_policy.yaml",
    "ION/03_registry/ion_mcp_client_certification_policy.yaml",
    "ION/03_registry/ion_mcp_transport_preview_policy.yaml",
    "ION/03_registry/ion_mcp_hosted_auth_alpha_policy.yaml",
    "ION/04_packages/kernel/ion_mcp_local_bridge.py",
    "ION/04_packages/kernel/ion_mcp_client_configs.py",
    "ION/04_packages/kernel/ion_mcp_client_certification.py",
    "ION/04_packages/kernel/ion_mcp_transport_preview.py",
    "ION/04_packages/kernel/ion_mcp_sdk_wrapper_boundary.py",
    "ION/04_packages/kernel/ion_mcp_hosted_auth_alpha.py",
    "ION/docs/mcp/LOCAL_MCP_BRIDGE_CLIENT_CONFIGURATION_GUIDE.md",
    "ION/docs/mcp/LOCAL_MCP_CLIENT_CERTIFICATION_GUIDE.md",
    "ION/docs/mcp/LOCAL_MCP_TRANSPORT_PREVIEW_GUIDE.md",
    "ION/examples/mcp/cursor.mcp.json",
    "ION/examples/mcp/codex.config.toml",
    "ION/tests/test_kernel_ion_mcp_local_bridge.py",
    "ION/tests/test_kernel_ion_mcp_client_certification.py",
    "ION/tests/test_kernel_ion_mcp_transport_preview.py",
    "ION/tests/test_kernel_ion_mcp_sdk_wrapper_boundary.py",
    "ION/tests/test_kernel_ion_mcp_hosted_auth_alpha.py",
)

CURRENT_TRUNK_MCP_SURFACES: tuple[str, ...] = (
    ".cursor/mcp.json",
    "ION/09_integrations/mcp/ion_mcp_server.py",
    "ION/09_integrations/mcp/README.md",
    "ION/04_packages/kernel/ion_mcp_bridge_audit.py",
    "ION/tests/test_kernel_ion_mcp_bridge_audit.py",
)

FORBIDDEN_DONOR_RUNTIME_PREFIXES: tuple[str, ...] = (
    "ION/05_context/runtime_state/v64_local_mcp_bridge/",
)

DONOR_SCOPE = (
    "V72 MCP donor reconciliation imports protocol, registry, kernel, test, docs, and example surfaces only; "
    "old runtime-session receipts remain forensic donor evidence and are not restored into current hot trunk."
)


@dataclass(frozen=True)
class V72McpDonorReconciliationAudit:
    schema_id: str
    version_line: str
    generated_at: str
    root: str
    donor_branch: str
    donor_scope: str
    required_donor_surface_count: int
    restored_donor_surface_count: int
    missing_donor_surface_count: int
    missing_donor_surfaces: tuple[str, ...]
    current_trunk_mcp_surface_count: int
    current_trunk_mcp_surfaces_present: tuple[str, ...]
    current_trunk_mcp_surfaces_missing: tuple[str, ...]
    forbidden_runtime_prefixes: tuple[str, ...]
    forbidden_runtime_file_count: int
    forbidden_runtime_files: tuple[str, ...]
    local_bridge_present: bool
    client_certification_present: bool
    transport_preview_present: bool
    hosted_auth_alpha_present: bool
    cursor_bridge_preserved: bool
    donor_runtime_receipts_restored: bool
    live_execution_authority: bool
    production_authority: bool
    reconciliation_verdict: str
    findings: tuple[str, ...]


def _shell_root(path: str | Path) -> Path:
    p = Path(path).expanduser().resolve()
    return p.parent if p.name == "ION" else p


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _asdict(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {k: _asdict(v) for k, v in asdict(value).items()}
    if isinstance(value, tuple):
        return [_asdict(v) for v in value]
    if isinstance(value, list):
        return [_asdict(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _asdict(v) for k, v in value.items()}
    return value


def audit_to_dict(audit: V72McpDonorReconciliationAudit) -> dict[str, Any]:
    value = _asdict(audit)
    assert isinstance(value, dict)
    return value


def _present(root: Path, rels: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(rel for rel in rels if (root / rel).exists())


def _missing(root: Path, rels: tuple[str, ...]) -> tuple[str, ...]:
    return tuple(rel for rel in rels if not (root / rel).exists())


def _runtime_files(root: Path) -> tuple[str, ...]:
    found: list[str] = []
    for prefix in FORBIDDEN_DONOR_RUNTIME_PREFIXES:
        base = root / prefix
        if base.exists():
            for child in sorted(base.rglob("*")):
                if child.is_file() and not child.is_symlink():
                    found.append(child.relative_to(root).as_posix())
    return tuple(found)


def build_v72_mcp_donor_reconciliation_audit(
    root: str | Path,
    *,
    generated_at: str | None = None,
) -> V72McpDonorReconciliationAudit:
    shell = _shell_root(root)
    missing = _missing(shell, REQUIRED_DONOR_SURFACES)
    restored = _present(shell, REQUIRED_DONOR_SURFACES)
    current_present = _present(shell, CURRENT_TRUNK_MCP_SURFACES)
    current_missing = _missing(shell, CURRENT_TRUNK_MCP_SURFACES)
    runtime_files = _runtime_files(shell)

    findings: list[str] = []
    if not missing:
        findings.append("required_v72_mcp_donor_surfaces_present")
    else:
        findings.append("missing_required_v72_mcp_donor_surfaces")
    if not current_missing:
        findings.append("current_v105_v107_cursor_mcp_bridge_preserved")
    else:
        findings.append("current_cursor_mcp_bridge_surface_missing")
    if runtime_files:
        findings.append("forbidden_v72_runtime_receipts_were_restored_to_hot_trunk")
    else:
        findings.append("old_v72_runtime_session_receipts_not_restored_to_hot_trunk")

    verdict = "V72_MCP_DONOR_RECONCILIATION_PASS"
    if missing or current_missing or runtime_files:
        verdict = "V72_MCP_DONOR_RECONCILIATION_REVIEW_REQUIRED"

    return V72McpDonorReconciliationAudit(
        schema_id=SCHEMA_ID,
        version_line=VERSION_LINE,
        generated_at=generated_at or _now(),
        root=shell.as_posix(),
        donor_branch="ION_MASTER_CURRENT_3_V72_HOSTED_MCP_BUNDLE_IMPORT_EXPORT_AND_REPLAY_ALPHA_20260426",
        donor_scope=DONOR_SCOPE,
        required_donor_surface_count=len(REQUIRED_DONOR_SURFACES),
        restored_donor_surface_count=len(restored),
        missing_donor_surface_count=len(missing),
        missing_donor_surfaces=missing,
        current_trunk_mcp_surface_count=len(current_present),
        current_trunk_mcp_surfaces_present=current_present,
        current_trunk_mcp_surfaces_missing=current_missing,
        forbidden_runtime_prefixes=FORBIDDEN_DONOR_RUNTIME_PREFIXES,
        forbidden_runtime_file_count=len(runtime_files),
        forbidden_runtime_files=runtime_files,
        local_bridge_present=(shell / "ION/04_packages/kernel/ion_mcp_local_bridge.py").exists(),
        client_certification_present=(shell / "ION/04_packages/kernel/ion_mcp_client_certification.py").exists(),
        transport_preview_present=(shell / "ION/04_packages/kernel/ion_mcp_transport_preview.py").exists(),
        hosted_auth_alpha_present=(shell / "ION/04_packages/kernel/ion_mcp_hosted_auth_alpha.py").exists(),
        cursor_bridge_preserved=(shell / "ION/04_packages/kernel/ion_mcp_bridge_audit.py").exists(),
        donor_runtime_receipts_restored=bool(runtime_files),
        live_execution_authority=False,
        production_authority=False,
        reconciliation_verdict=verdict,
        findings=tuple(findings),
    )


def write_v72_mcp_donor_reconciliation_audit(
    root: str | Path,
    audit: V72McpDonorReconciliationAudit,
    *,
    output: str | Path | None = None,
) -> Path:
    shell = _shell_root(root)
    out = shell / (Path(output) if output else REPORT_REL)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit_to_dict(audit), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the V108 V72 MCP donor reconciliation audit.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    audit = build_v72_mcp_donor_reconciliation_audit(args.ion_root)
    if args.write:
        write_v72_mcp_donor_reconciliation_audit(args.ion_root, audit, output=args.output)
    if args.json:
        print(json.dumps(audit_to_dict(audit), indent=2, sort_keys=True))
    else:
        print(audit.reconciliation_verdict)
    return 0 if audit.reconciliation_verdict == "V72_MCP_DONOR_RECONCILIATION_PASS" else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
