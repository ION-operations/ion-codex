"""V124 legacy Cloudflare tunnel reuse audit.

This audit classifies older AIMOS Cloudflare tunnel scripts as donor evidence
without allowing their AIMOS identity, legacy status paths, or /sse endpoint to
become current ION authority. The only reusable donor pattern is the bounded
Cloudflare quick-tunnel transport that points at the current ChatGPT browser
HTTP MCP preview and its /mcp endpoint.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Sequence

from .ion_chatgpt_browser_cloudflare_tunnel import find_cloudflared

SCHEMA_ID = "ion.chatgpt_browser_legacy_tunnel_reuse_audit.v1"
VERSION_LINE = "V124_LEGACY_CLOUDFLARE_TUNNEL_REUSE"
READY_VERDICT = "ION_CHATGPT_BROWSER_LEGACY_TUNNEL_REUSE_READY"
SETUP_REQUIRED_VERDICT = "ION_CHATGPT_BROWSER_LEGACY_TUNNEL_REUSE_SETUP_REQUIRED"
BLOCKED_VERDICT = "ION_CHATGPT_BROWSER_LEGACY_TUNNEL_REUSE_BLOCKED"
OUTPUT_RELATIVE_PATH = Path("ION/05_context/current/CHATGPT_BROWSER_LEGACY_TUNNEL_REUSE_AUDIT_V124.json")

DEFAULT_DONOR_SCRIPT_PATHS = (
    Path("/home/sev/AIM-OS/scripts/cloudflare_tunnel.py"),
    Path("/home/sev/ION - Production/AIM-ION/scripts/cloudflare_tunnel.py"),
)
CURRENT_TUNNEL_MODULE = Path("ION/04_packages/kernel/ion_chatgpt_browser_cloudflare_tunnel.py")
CURRENT_SETUP_DOC = Path("ION/docs/setup/CHATGPT_BROWSER_CLOUDFLARE_TUNNEL_SETUP_V122.md")

DONOR_REUSABLE_PATTERNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("cloudflared_quick_tunnel_command", ("cloudflared", "tunnel", "--url")),
    ("trycloudflare_public_url_capture", ("trycloudflare.com",)),
    ("status_json_written", ("active_tunnel.json",)),
)

DONOR_FORBIDDEN_CURRENT_AUTHORITY_PATTERNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("legacy_sse_endpoint", ("/sse",)),
    ("aimos_identity", ("AIM-OS", "AIMOS")),
    ("legacy_status_path", ("data/mcp",)),
    ("legacy_default_port", ("8000",)),
    ("host_level_auto_install_hint", ("winget", "install_cloudflared")),
)

CURRENT_REQUIRED_PATTERNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("current_mcp_endpoint", ("DEFAULT_ENDPOINT_PATH", "/mcp")),
    ("current_cloudflared_quick_tunnel_command", ("tunnel", "--url")),
    ("current_active_tunnel_status_path", ("ACTIVE_CHATGPT_BROWSER_CLOUDFLARE_TUNNEL.json",)),
    ("current_non_authority_fields", ("production_authority", "live_execution_authority", "deployment_authority")),
)

CURRENT_FORBIDDEN_PATTERNS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("legacy_sse_endpoint", ("/sse",)),
    ("aimos_identity", ("AIM-OS", "AIMOS")),
    ("legacy_status_path", ("data/mcp/active_tunnel.json",)),
)


@dataclass(frozen=True)
class PatternFinding:
    name: str
    present: bool
    patterns: tuple[str, ...]


@dataclass(frozen=True)
class DonorScriptCheck:
    path: str
    exists: bool
    sha256: str | None
    reusable_patterns: tuple[PatternFinding, ...]
    forbidden_current_authority_patterns: tuple[PatternFinding, ...]


@dataclass(frozen=True)
class CurrentTunnelCheck:
    rel_path: str
    exists: bool
    required_patterns: tuple[PatternFinding, ...]
    forbidden_patterns: tuple[PatternFinding, ...]


@dataclass(frozen=True)
class LegacyTunnelReuseAudit:
    schema_id: str
    line: str
    emitted_at: str
    scanned_root: str
    root_confirmed: bool
    root_missing_files: tuple[str, ...]
    donor_scripts_found: int
    donor_reusable_pattern_count: int
    donor_forbidden_pattern_count: int
    current_required_pattern_count: int
    current_required_pattern_present_count: int
    current_forbidden_pattern_count: int
    cloudflared_found: bool
    cloudflared_path: str | None
    connector_state: str
    endpoint_path: str
    legacy_endpoint_status: str
    current_connector_url_shape: str
    accepted: bool
    production_authority: bool
    live_execution_authority: bool
    deployment_authority: bool
    mutation_performed: bool
    verdict: str
    findings: tuple[str, ...]
    donor_script_checks: tuple[DonorScriptCheck, ...] = field(default_factory=tuple)
    current_tunnel_check: CurrentTunnelCheck | None = None


def _shell_root(path: str | Path) -> Path:
    p = Path(path).expanduser().resolve()
    return p.parent if p.name == "ION" else p


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _sha256_file(path: Path) -> str | None:
    if not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _patterns_present(text: str, spec: tuple[str, tuple[str, ...]]) -> PatternFinding:
    name, patterns = spec
    return PatternFinding(
        name=name,
        present=all(pattern in text for pattern in patterns),
        patterns=patterns,
    )


def _resolve_path(shell: Path, value: str | Path) -> Path:
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (shell / path).resolve()


def _check_donor_script(path: Path) -> DonorScriptCheck:
    text = _read_text(path)
    return DonorScriptCheck(
        path=path.as_posix(),
        exists=path.is_file(),
        sha256=_sha256_file(path),
        reusable_patterns=tuple(_patterns_present(text, spec) for spec in DONOR_REUSABLE_PATTERNS),
        forbidden_current_authority_patterns=tuple(
            _patterns_present(text, spec) for spec in DONOR_FORBIDDEN_CURRENT_AUTHORITY_PATTERNS
        ),
    )


def _check_current_tunnel(shell: Path, rel_path: str | Path = CURRENT_TUNNEL_MODULE) -> CurrentTunnelCheck:
    rel = Path(rel_path)
    path = _resolve_path(shell, rel)
    text = _read_text(path)
    return CurrentTunnelCheck(
        rel_path=rel.as_posix(),
        exists=path.is_file(),
        required_patterns=tuple(_patterns_present(text, spec) for spec in CURRENT_REQUIRED_PATTERNS),
        forbidden_patterns=tuple(_patterns_present(text, spec) for spec in CURRENT_FORBIDDEN_PATTERNS),
    )


def build_legacy_tunnel_reuse_audit(
    root: str | Path,
    *,
    donor_paths: Sequence[str | Path] = DEFAULT_DONOR_SCRIPT_PATHS,
    current_tunnel_module: str | Path = CURRENT_TUNNEL_MODULE,
    cloudflared_binary: str = "cloudflared",
    emitted_at: str | None = None,
) -> LegacyTunnelReuseAudit:
    shell = _shell_root(root)
    root_required = ("pyproject.toml", "ION/REPO_AUTHORITY.md")
    root_missing = tuple(rel for rel in root_required if not (shell / rel).exists())

    donor_checks = tuple(_check_donor_script(_resolve_path(shell, path)) for path in donor_paths)
    current_check = _check_current_tunnel(shell, current_tunnel_module)

    donor_found = sum(1 for check in donor_checks if check.exists)
    donor_reusable_pattern_count = sum(
        1 for check in donor_checks for finding in check.reusable_patterns if finding.present
    )
    donor_forbidden_pattern_count = sum(
        1 for check in donor_checks for finding in check.forbidden_current_authority_patterns if finding.present
    )
    current_required_present_count = sum(1 for finding in current_check.required_patterns if finding.present)
    current_forbidden_pattern_count = sum(1 for finding in current_check.forbidden_patterns if finding.present)
    current_required_count = len(current_check.required_patterns)
    cloudflared_path = find_cloudflared(cloudflared_binary)

    findings: list[str] = []
    if root_missing:
        findings.append("shell_root_not_confirmed")
    else:
        findings.append("shell_root_confirmed")
    if donor_found:
        findings.append("legacy_cloudflare_tunnel_donor_scripts_found")
    else:
        findings.append("legacy_cloudflare_tunnel_donor_scripts_missing")
    if donor_reusable_pattern_count:
        findings.append("reusable_cloudflared_quick_tunnel_transport_found")
    else:
        findings.append("no_reusable_legacy_cloudflare_patterns_found")
    if donor_forbidden_pattern_count:
        findings.append("legacy_aimos_sse_patterns_classified_donor_only")
    if not current_check.exists:
        findings.append("current_chatgpt_cloudflare_tunnel_module_missing")
    if current_required_present_count == current_required_count:
        findings.append("current_tunnel_uses_mcp_endpoint_and_non_authority_status")
    else:
        findings.append("current_tunnel_required_patterns_missing")
    if current_forbidden_pattern_count:
        findings.append("current_tunnel_contains_legacy_forbidden_patterns")
    else:
        findings.append("current_tunnel_excludes_legacy_sse_and_aimos_authority")
    if cloudflared_path:
        findings.append("cloudflared_available_on_path")
    else:
        findings.append("cloudflared_not_found_on_path")

    contract_safe = (
        not root_missing
        and donor_found > 0
        and donor_reusable_pattern_count > 0
        and current_check.exists
        and current_required_present_count == current_required_count
        and current_forbidden_pattern_count == 0
    )
    if not contract_safe:
        verdict = BLOCKED_VERDICT
        connector_state = "LEGACY_TUNNEL_REUSE_BLOCKED"
    elif cloudflared_path:
        verdict = READY_VERDICT
        connector_state = "DONOR_TRANSPORT_READY_TO_RUN"
    else:
        verdict = SETUP_REQUIRED_VERDICT
        connector_state = "DONOR_TRANSPORT_REUSE_BLOCKED_CLOUDFLARED_NOT_INSTALLED"

    return LegacyTunnelReuseAudit(
        schema_id=SCHEMA_ID,
        line=VERSION_LINE,
        emitted_at=emitted_at or _now(),
        scanned_root=shell.as_posix(),
        root_confirmed=not root_missing,
        root_missing_files=root_missing,
        donor_scripts_found=donor_found,
        donor_reusable_pattern_count=donor_reusable_pattern_count,
        donor_forbidden_pattern_count=donor_forbidden_pattern_count,
        current_required_pattern_count=current_required_count,
        current_required_pattern_present_count=current_required_present_count,
        current_forbidden_pattern_count=current_forbidden_pattern_count,
        cloudflared_found=bool(cloudflared_path),
        cloudflared_path=cloudflared_path,
        connector_state=connector_state,
        endpoint_path="/mcp",
        legacy_endpoint_status="legacy_/sse_is_forbidden_for_current_chatgpt_connector",
        current_connector_url_shape="https://<cloudflare-host>/mcp",
        accepted=contract_safe,
        production_authority=False,
        live_execution_authority=False,
        deployment_authority=False,
        mutation_performed=False,
        verdict=verdict,
        findings=tuple(findings),
        donor_script_checks=donor_checks,
        current_tunnel_check=current_check,
    )


def audit_to_dict(audit: LegacyTunnelReuseAudit) -> dict[str, Any]:
    return asdict(audit)


def write_legacy_tunnel_reuse_audit(
    root: str | Path,
    audit: LegacyTunnelReuseAudit | None = None,
    *,
    output: str | Path | None = None,
) -> Path:
    shell = _shell_root(root)
    audit = audit or build_legacy_tunnel_reuse_audit(shell)
    out = shell / (Path(output) if output else OUTPUT_RELATIVE_PATH)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit_to_dict(audit), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit reuse of legacy Cloudflare tunnel donor scripts.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--donor-script", action="append", default=None)
    parser.add_argument("--current-tunnel-module", default=str(CURRENT_TUNNEL_MODULE))
    parser.add_argument("--cloudflared-binary", default="cloudflared")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    donor_paths = tuple(args.donor_script) if args.donor_script else DEFAULT_DONOR_SCRIPT_PATHS
    audit = build_legacy_tunnel_reuse_audit(
        args.ion_root,
        donor_paths=donor_paths,
        current_tunnel_module=args.current_tunnel_module,
        cloudflared_binary=args.cloudflared_binary,
    )
    if args.write:
        write_legacy_tunnel_reuse_audit(args.ion_root, audit, output=args.output)
    if args.json:
        print(json.dumps(audit_to_dict(audit), indent=2, sort_keys=True))
    else:
        print(audit.verdict)
        for finding in audit.findings:
            print(f"- {finding}")
    return 0 if audit.accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
