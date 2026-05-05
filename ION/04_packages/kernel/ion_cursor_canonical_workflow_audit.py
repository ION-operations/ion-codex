"""Audit Cursor-side ION workflow canonicalization.

V94 checks Cursor adapter surfaces for contradictory shell-root, CLI entrypoint,
or subagent law. V116 keeps root onboarding carrier-neutral, so this audit must
not require root files to present Cursor-specific wording as universal law.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable

REQUIRED_FILES = [
    "ION/02_architecture/ION_CURSOR_CANONICAL_WORKFLOW_UNIFICATION_PROTOCOL.md",
    ".cursor/rules/ion-canonical-workflow-unification.mdc",
    ".cursor/rules/ion-carrier-mount.mdc",
    ".cursor/rules/ion-cursor-onboarding.mdc",
    ".cursor/commands/ion.md",
    ".cursor/skills/ion-autopilot/SKILL.md",
    ".cursor/agents/ion-spawn-row-slot.md",
]

OPTIONAL_COMPATIBILITY_FILES = [
    "AGENTS.md",
    "START_HERE_FOR_ANY_AGENT.md",
]

REQUIRED_PHRASES = {
    "ION/02_architecture/ION_CURSOR_CANONICAL_WORKFLOW_UNIFICATION_PROTOCOL.md": [
        "No fixed absolute or workspace-specific path is canonical",
        "ion_cursor_autopilot_packet",
        "ion_carrier_continue",
        "CURSOR_CARRIER_CONTROL_SURFACE",
        "### CONTEXT PROOF",
    ],
    ".cursor/rules/ion-carrier-mount.mdc": [
        "V94 canonical",
        "No fixed workspace path is canonical",
        "ion_cursor_autopilot_packet",
        "ion_carrier_continue",
        "### CONTEXT PROOF",
    ],
    ".cursor/rules/ion-cursor-onboarding.mdc": [
        "V94 canonical",
        "No fixed path is canonical",
        "ion_cursor_autopilot_packet",
        "Deprecated older route",
    ],
    ".cursor/commands/ion.md": [
        "Canonical ION Autopilot Command",
        "CURSOR_CARRIER_CONTROL_SURFACE",
        "ion_cursor_autopilot_packet",
        "ion_carrier_continue",
    ],
    ".cursor/skills/ion-autopilot/SKILL.md": [
        "V94 Canonical",
        "One shell root",
        "One command sequence",
        "Deprecated path",
    ],
    ".cursor/agents/ion-spawn-row-slot.md": [
        "V94 strict carrier slot",
        "SPAWN_ROW_CONTEXT_PACKAGE_MISSING",
        "### CONTEXT PROOF",
    ],
}

FORBIDDEN_ACTIVE_PHRASES = [
    "Always use:\n\n`IONcursorbuild/ION MASTER CURRENT`",
    "Default for this workspace:** `IONcursorbuild/ION MASTER CURRENT/`",
    "Run: `python3 -m kernel <workstream>",
    "Before substantive work: confirm both files exist, then run `python3 -m kernel <workstream>",
]

FORBIDDEN_ROOT_COMPATIBILITY_PHRASES = [
    "ION Cursor Carrier, V94",
    "ION Cursor Carrier Canonical Workflow, V94",
    "Run the V94 CLI spine",
    "Use `/ion` as the reset-and-run command",
]

@dataclass
class AuditResult:
    audit_id: str
    accepted: bool
    status: str
    missing_required_files: list[str]
    missing_required_phrases: list[str]
    forbidden_active_phrases: list[str]
    findings: list[str]


def _read(root: Path, rel: str) -> str:
    path = root / rel
    return path.read_text(encoding="utf-8")


def audit_cursor_canonical_workflow(root: str | Path) -> AuditResult:
    root = Path(root)
    missing_files: list[str] = []
    missing_phrases: list[str] = []
    forbidden_hits: list[str] = []
    findings: list[str] = []

    if not (root / "pyproject.toml").exists() or not (root / "ION/REPO_AUTHORITY.md").exists():
        findings.append("ROOT_NOT_CONFIRMED: pyproject.toml and ION/REPO_AUTHORITY.md are not siblings at ion_root")

    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            missing_files.append(rel)

    for rel, phrases in REQUIRED_PHRASES.items():
        path = root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in phrases:
            if phrase not in text:
                missing_phrases.append(f"{rel}: {phrase}")

    active_text = "\n".join(
        (root / rel).read_text(encoding="utf-8")
        for rel in (*REQUIRED_FILES, *OPTIONAL_COMPATIBILITY_FILES)
        if (root / rel).exists()
    )
    for phrase in FORBIDDEN_ACTIVE_PHRASES:
        if phrase in active_text:
            forbidden_hits.append(phrase)
    for rel in OPTIONAL_COMPATIBILITY_FILES:
        path = root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for phrase in FORBIDDEN_ROOT_COMPATIBILITY_PHRASES:
            if phrase in text:
                forbidden_hits.append(f"{rel}: {phrase}")

    accepted = not missing_files and not missing_phrases and not forbidden_hits and not findings
    status = "ION_CURSOR_CANONICAL_WORKFLOW_READY" if accepted else "ION_CURSOR_CANONICAL_WORKFLOW_FINDINGS"
    return AuditResult(
        audit_id="v94_cursor_canonical_workflow_unification",
        accepted=accepted,
        status=status,
        missing_required_files=missing_files,
        missing_required_phrases=missing_phrases,
        forbidden_active_phrases=forbidden_hits,
        findings=findings,
    )


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(list(argv) if argv is not None else None)
    result = audit_cursor_canonical_workflow(args.ion_root)
    if args.json:
        print(json.dumps(asdict(result), indent=2, sort_keys=True))
    else:
        print(result.status)
        if not result.accepted:
            for f in result.findings:
                print(f"finding: {f}")
            for f in result.missing_required_files:
                print(f"missing file: {f}")
            for f in result.missing_required_phrases:
                print(f"missing phrase: {f}")
            for f in result.forbidden_active_phrases:
                print(f"forbidden active phrase: {f}")
    return 0 if result.accepted else 1


if __name__ == "__main__":
    raise SystemExit(main())
