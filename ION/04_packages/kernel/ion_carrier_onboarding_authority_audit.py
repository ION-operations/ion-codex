"""ION carrier onboarding authority audit.

This audit guards against stale host-specific onboarding being presented as
root-level ION law. The enforceable carrier onboarding substrate is registry
profiles, role boot files, and carrier execution templates; shell-root
markdown must not become a procedural onboarding substrate.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPORT_REL = Path("ION/05_context/current/CARRIER_ONBOARDING_AUTHORITY_AUDIT_V123.json")

OPTIONAL_ROOT_ONBOARDING_FILES = (
    "AGENTS.md",
    "START_HERE_FOR_ANY_AGENT.md",
)

REQUIRED_AUTHORITY_SURFACES = (
    "ION/02_architecture/ION_CARRIER_ONBOARDING_AUTHORITY_PROTOCOL.md",
    "ION/02_architecture/ION_DEFAULT_CARRIER_ONBOARDING_PROTOCOL.md",
    "ION/02_architecture/ION_CARRIER_RUNTIME_FOUNDATION_PROTOCOL.md",
    "ION/02_architecture/CODEX_EXTENSION_CARRIER_PROTOCOL.md",
    "ION/03_registry/codex_extension_carrier_profile.yaml",
    "ION/03_registry/gpt55_runtime_identity_mount_registry.yaml",
    "ION/03_registry/boots/STEWARD.boot.md",
    "ION/03_registry/boots/RELAY.boot.md",
    "ION/03_registry/boots/MASON.boot.md",
    "ION/03_registry/boots/NEMESIS.boot.md",
    "ION/07_templates/carriers/CARRIER_MOUNT_PROOF.md",
    "ION/07_templates/carriers/CARRIER_SESSION_PACKET.md",
    "ION/07_templates/carriers/CARRIER_CAPABILITY_SURVEY.md",
    "ION/07_templates/carriers/CODEX_EXTENSION_EXECUTION_PACKET.md",
)

FORBIDDEN_ROOT_PATTERNS = (
    "ION Cursor Carrier, V94",
    "ION Cursor Carrier Canonical Workflow, V94",
    "Run the V94 CLI spine",
    "You start as `CURSOR_CARRIER_CONTROL_SURFACE`",
    "ion_cursor_autopilot_packet --ion-root . --operator-message \"<message>\" --write --json",
    "Use `/ion` as the reset-and-run command",
    "/ion is the primary reset-and-run command",
)

FORBIDDEN_ROOT_PROCEDURAL_PATTERNS = (
    "Current Operating Packet",
    "Confirm Shell Root",
    "Read Current Runtime Truth",
    "Carrier Continue",
    "Current Protocol Anchors",
    "Authority Anchors",
    "Mandatory reads",
    "kernel.ion_carrier_continue",
    "kernel.ion_status",
    "PYTHONDONTWRITEBYTECODE",
    "ACTIVE_WORK_PACKET",
    "ACTIVE_CARRIER_TURN_PACKET",
    "ACTIVE_ROLE_SPAWN_PLAN",
)

ACTIVE_SURFACES_TO_SCAN = (
    "ION/REPO_AUTHORITY.md",
    "ION/05_context/current/OPERATOR_VISIBLE_LAST_RUN.md",
    "ION/05_context/current/_tmp_onboard.json",
    ".cursor/hooks/ion_session_start_persona_mount.py",
)

FORBIDDEN_ACTIVE_ROOT_READ_PATTERNS = (
    "Read **AGENTS.md**",
    "AGENTS.md at workspace root",
    "`AGENTS.md`",
    "`START_HERE_FOR_ANY_AGENT.md`",
    "START_HERE_FOR_ANY_AGENT.md",
    "Root authority bundle: `ION/05_context/exports/2026-04-17_root_authority_bundle/START_HERE.md`",
    "preferred first surface is now",
    "Use that bundle before either `STATUS.md`",
    "Read the bundle first",
)


@dataclass(frozen=True)
class RootOnboardingFileCheck:
    rel_path: str
    exists: bool
    forbidden_patterns_present: tuple[str, ...]
    forbidden_procedural_patterns_present: tuple[str, ...]


@dataclass(frozen=True)
class ActiveSurfaceCheck:
    rel_path: str
    exists: bool
    forbidden_root_read_patterns_present: tuple[str, ...]


@dataclass(frozen=True)
class CarrierOnboardingAuthorityAudit:
    schema_id: str
    line: str
    emitted_at: str
    scanned_root: str
    root_confirmed: bool
    root_missing_files: tuple[str, ...]
    authority_surface_count: int
    authority_surface_present_count: int
    missing_authority_surfaces: tuple[str, ...]
    optional_root_onboarding_files_present: int
    stale_cursor_root_patterns_present: int
    procedural_root_patterns_present: int
    forbidden_active_root_read_patterns_present: int
    accepted: bool
    production_authority: bool
    live_execution_authority: bool
    mutation_performed: bool
    verdict: str
    findings: tuple[str, ...]
    file_checks: tuple[RootOnboardingFileCheck, ...] = field(default_factory=tuple)
    active_surface_checks: tuple[ActiveSurfaceCheck, ...] = field(default_factory=tuple)


def _shell_root(path: str | Path) -> Path:
    p = Path(path).expanduser().resolve()
    return p.parent if p.name == "ION" else p


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def build_carrier_onboarding_authority_audit(
    root: str | Path,
    *,
    emitted_at: str | None = None,
) -> CarrierOnboardingAuthorityAudit:
    shell = _shell_root(root)
    root_required = ("pyproject.toml", "ION/REPO_AUTHORITY.md")
    root_missing = tuple(rel for rel in root_required if not (shell / rel).exists())
    file_checks: list[RootOnboardingFileCheck] = []
    active_surface_checks: list[ActiveSurfaceCheck] = []

    stale_count = 0
    procedural_count = 0
    present_count = 0
    for rel in OPTIONAL_ROOT_ONBOARDING_FILES:
        path = shell / rel
        text = _text(path)
        exists = path.is_file()
        if exists:
            present_count += 1
        forbidden_present = tuple(pattern for pattern in FORBIDDEN_ROOT_PATTERNS if pattern in text)
        procedural_present = tuple(pattern for pattern in FORBIDDEN_ROOT_PROCEDURAL_PATTERNS if pattern in text)
        stale_count += len(forbidden_present)
        procedural_count += len(procedural_present)
        file_checks.append(
            RootOnboardingFileCheck(
                rel_path=rel,
                exists=exists,
                forbidden_patterns_present=forbidden_present,
                forbidden_procedural_patterns_present=procedural_present,
            )
        )

    active_root_read_count = 0
    for rel in ACTIVE_SURFACES_TO_SCAN:
        path = shell / rel
        text = _text(path)
        exists = path.is_file()
        forbidden_present = tuple(pattern for pattern in FORBIDDEN_ACTIVE_ROOT_READ_PATTERNS if pattern in text)
        active_root_read_count += len(forbidden_present)
        active_surface_checks.append(
            ActiveSurfaceCheck(
                rel_path=rel,
                exists=exists,
                forbidden_root_read_patterns_present=forbidden_present,
            )
        )

    missing_authority = tuple(rel for rel in REQUIRED_AUTHORITY_SURFACES if not (shell / rel).is_file())
    authority_present_count = len(REQUIRED_AUTHORITY_SURFACES) - len(missing_authority)
    findings: list[str] = []
    if root_missing:
        findings.append("shell_root_not_confirmed")
    else:
        findings.append("shell_root_confirmed")
    if missing_authority:
        findings.append("carrier_registry_template_onboarding_surfaces_missing")
    else:
        findings.append("carrier_registry_template_onboarding_surfaces_present")
    if present_count:
        findings.append("optional_root_onboarding_shims_present_in_hot_root")
    else:
        findings.append("optional_root_onboarding_shims_retired_from_hot_root")
    if stale_count:
        findings.append("stale_cursor_root_onboarding_patterns_present")
    if procedural_count:
        findings.append("procedural_root_onboarding_patterns_present")
    if active_root_read_count:
        findings.append("active_surface_requires_retired_root_onboarding")
    if not stale_count and not procedural_count and not active_root_read_count:
        findings.append("root_onboarding_shims_not_authority_and_not_stale")

    accepted = (
        not root_missing
        and not missing_authority
        and present_count == 0
        and stale_count == 0
        and procedural_count == 0
        and active_root_read_count == 0
    )
    verdict = "ION_CARRIER_ONBOARDING_AUTHORITY_READY" if accepted else "ION_CARRIER_ONBOARDING_AUTHORITY_BLOCKED"

    return CarrierOnboardingAuthorityAudit(
        schema_id="ion.carrier_onboarding_authority_audit.v1",
        line="V123_ROOT_ONBOARDING_SHIM_RETIREMENT",
        emitted_at=emitted_at or _now(),
        scanned_root=shell.as_posix(),
        root_confirmed=not root_missing,
        root_missing_files=root_missing,
        authority_surface_count=len(REQUIRED_AUTHORITY_SURFACES),
        authority_surface_present_count=authority_present_count,
        missing_authority_surfaces=missing_authority,
        optional_root_onboarding_files_present=present_count,
        stale_cursor_root_patterns_present=stale_count,
        procedural_root_patterns_present=procedural_count,
        forbidden_active_root_read_patterns_present=active_root_read_count,
        accepted=accepted,
        production_authority=False,
        live_execution_authority=False,
        mutation_performed=False,
        verdict=verdict,
        findings=tuple(findings),
        file_checks=tuple(file_checks),
        active_surface_checks=tuple(active_surface_checks),
    )


def audit_to_dict(audit: CarrierOnboardingAuthorityAudit) -> dict[str, Any]:
    return asdict(audit)


def write_carrier_onboarding_authority_audit(
    root: str | Path,
    audit: CarrierOnboardingAuthorityAudit | None = None,
) -> Path:
    shell = _shell_root(root)
    audit = audit or build_carrier_onboarding_authority_audit(shell)
    out = shell / REPORT_REL
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit_to_dict(audit), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit root carrier onboarding authority.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    audit = build_carrier_onboarding_authority_audit(args.ion_root)
    if args.write_report:
        write_carrier_onboarding_authority_audit(args.ion_root, audit)
    if args.json:
        print(json.dumps(audit_to_dict(audit), indent=2, sort_keys=True))
    else:
        print(audit.verdict)
        for finding in audit.findings:
            print(f"- {finding}")
    return 0 if audit.accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
