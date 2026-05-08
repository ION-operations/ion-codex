"""Minimal Carrier Mount helper for ION.

This helper does not replace the scheduler, packet law, or Meta Carrier protocol.
It only performs read-only carrier-root discovery and renders a mount proof skeleton.

Usage:
    python ION/04_packages/kernel/carrier_mount.py status
    python ION/04_packages/kernel/carrier_mount.py mount-proof --host Cursor --profile CURSOR_CARRIER

The helper is deliberately dependency-free and safe for L0/L1 use.
"""

import argparse
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


REQUIRED_RELATIVE_PATHS = {
    "repo_authority": "ION/REPO_AUTHORITY.md",
    "carrier_boot": "ION/04_agents/carriers/CARRIER_AGENT.boot.md",
    "meta_carrier_protocol": "ION/04_agents/carriers/META_CARRIER_EVOLUTION_PROTOCOL.md",
    "carrier_registry": "ION/04_agents/carriers/carrier_registry.json",
    "capability_registry": "ION/03_registry/capabilities/capability_registry.json",
    "capability_survey_template": "ION/07_templates/carriers/CARRIER_CAPABILITY_SURVEY.md",
    "mount_proof_template": "ION/07_templates/carriers/CARRIER_MOUNT_PROOF.md",
}


@dataclass(frozen=True)
class CarrierMountStatus:
    shell_root: str
    shell_root_found: bool
    pyproject_present: bool
    repo_authority_present: bool
    required_files: dict[str, bool]
    missing_files: list[str]
    default_start_level: str | None
    default_return_agent: str | None
    status: str


def find_shell_root(start: str | Path | None = None) -> Path:
    """Find a root where pyproject.toml and ION/REPO_AUTHORITY.md exist together."""
    current = Path(start or ".").resolve()
    candidates = [current, *current.parents]
    for candidate in candidates:
        if (candidate / "pyproject.toml").exists() and (candidate / "ION/REPO_AUTHORITY.md").exists():
            return candidate
    return current


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return value if isinstance(value, dict) else {}


def inspect_mount(root: str | Path | None = None) -> CarrierMountStatus:
    shell_root = find_shell_root(root)
    required = {key: (shell_root / rel).exists() for key, rel in REQUIRED_RELATIVE_PATHS.items()}
    missing = [rel for key, rel in REQUIRED_RELATIVE_PATHS.items() if not required[key]]
    registry = _load_json(shell_root / REQUIRED_RELATIVE_PATHS["carrier_registry"])
    status = "ready_for_l0_mount" if not missing else "blocked_missing_required_files"
    return CarrierMountStatus(
        shell_root=str(shell_root),
        shell_root_found=(shell_root / "pyproject.toml").exists() and (shell_root / "ION/REPO_AUTHORITY.md").exists(),
        pyproject_present=(shell_root / "pyproject.toml").exists(),
        repo_authority_present=(shell_root / "ION/REPO_AUTHORITY.md").exists(),
        required_files=required,
        missing_files=missing,
        default_start_level=registry.get("default_start_level"),
        default_return_agent=registry.get("default_return_agent"),
        status=status,
    )


def render_mount_proof(status: CarrierMountStatus, *, host: str, profile: str) -> str:
    now = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    lines = [
        "# Carrier Mount Proof",
        "",
        f"## Mount Proof ID",
        f"CMP-{now}",
        "",
        "## Host",
        host,
        "",
        "## Selected Carrier Profile",
        profile,
        "",
        "## Starting Level",
        status.default_start_level or "L0",
        "",
        "## Shell Root Proof",
        f"- shell_root: `{status.shell_root}`",
        f"- pyproject.toml: {'yes' if status.pyproject_present else 'no'}",
        f"- ION/REPO_AUTHORITY.md: {'yes' if status.repo_authority_present else 'no'}",
        "",
        "## Required Files Read / Present",
    ]
    for key, present in status.required_files.items():
        rel = REQUIRED_RELATIVE_PATHS[key]
        lines.append(f"- [{'x' if present else ' '}] {rel}")
    lines.extend([
        "",
        "## Missing Files",
    ])
    if status.missing_files:
        lines.extend(f"- {item}" for item in status.missing_files)
    else:
        lines.append("- none")
    lines.extend([
        "",
        "## Default Return Agent",
        status.default_return_agent or "CURRENT_CARRIER",
        "",
        "## Mount Verdict",
        "MOUNTED_AS_L0" if status.status == "ready_for_l0_mount" else "BLOCKED",
        "",
        "## Notes",
        "This proof is read-only. It does not approve carrier upgrade.",
        "",
    ])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="ION Carrier Mount helper")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    proof = sub.add_parser("mount-proof")
    proof.add_argument("--host", default="Unknown")
    proof.add_argument("--profile", default="MANUAL_CARRIER")
    args = parser.parse_args(argv)

    status = inspect_mount(Path("."))
    if args.command == "status":
        print(json.dumps(asdict(status), indent=2, sort_keys=True))
        return 0 if status.status == "ready_for_l0_mount" else 2
    if args.command == "mount-proof":
        print(render_mount_proof(status, host=args.host, profile=args.profile))
        return 0 if status.status == "ready_for_l0_mount" else 2
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
