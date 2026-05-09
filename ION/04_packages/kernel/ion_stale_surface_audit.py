"""Executable stale-surface audit for GPT sandbox package lines."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .ion_carrier_onboard import resolve_shell_root_from_ion_root

ACTIVE_PACKET_RELATIVE_PATH = Path("ION/05_context/current/ACTIVE_WORK_PACKET.json")
ACTIVE_AUDIT_OUTPUT_RELATIVE_PATH = Path("ION/05_context/current/ACTIVE_STALE_SURFACE_AUDIT.json")
CURSOR_RELAY_RULE_RELATIVE_PATH = Path(".cursor/rules/ion-carrier-relay-mediation.mdc")

LEGACY_CONTEXT_PATTERNS = [
    re.compile(r"primary[^.\n]{0,80}\b(MINI|CAPSULE|Mini|Capsule)\b"),
    re.compile(r"\b(MINI|CAPSULE|Mini|Capsule)\b[^.\n]{0,80}primary context"),
    re.compile(r"mount[^.\n]{0,80}\b(MINI|CAPSULE|Mini|Capsule)\b[^.\n]{0,80}alone"),
]

ALLOWED_LEGACY_CONTEXT_MARKERS = (
    "legacy", "historical", "witness", "supersedes", "superseded",
    "not primary", "not sufficient", "not live", "stale", "donor",
    "release artifact", "source-input", "source input", "must not",
    "cannot", "forbidden", "nonconformant", "may remain", "do not",
    "not used", "no active", "not be", "must use a current contextpackage",
)

SCAN_RELATIVE_PREFIXES = (
    "ION/01_doctrine/", "ION/02_architecture/", "ION/03_registry/",
    "ION/04_packages/kernel/", "ION/05_context/current/", "ION/07_templates/",
    ".cursor/rules/", "product/custom_gpt_adapter/", "product/package_guides/",
)

TEXT_SUFFIXES = {".md", ".mdc", ".py", ".json", ".yaml", ".yml", ".txt"}


def _iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _iter_scanned_files(shell_root: Path):
    for prefix in SCAN_RELATIVE_PREFIXES:
        base = shell_root / prefix
        if not base.exists():
            continue
        candidates = [base] if base.is_file() else [p for p in base.rglob("*") if p.is_file()]
        for path in candidates:
            if path.relative_to(shell_root) == ACTIVE_AUDIT_OUTPUT_RELATIVE_PATH:
                continue
            if path.suffix.lower() in TEXT_SUFFIXES:
                yield path


def build_stale_surface_audit(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = resolve_shell_root_from_ion_root(root)
    findings: list[dict[str, Any]] = []

    active_packet = _read_json(shell_root / ACTIVE_PACKET_RELATIVE_PATH) or {}
    carrier = active_packet.get("carrier")
    active_template = active_packet.get("active_template")
    phase_sequence = active_packet.get("role_phase_sequence") or []

    if carrier == "GPT_SANDBOX_CARRIER" and isinstance(active_template, str) and "ION/docs/cursor/" in active_template:
        findings.append({"kind": "gpt_sandbox_cursor_template_default", "severity": "block", "path": str(ACTIVE_PACKET_RELATIVE_PATH), "detail": active_template})

    if carrier == "GPT_SANDBOX_CARRIER":
        if not phase_sequence or phase_sequence[0] != "PERSONA_INTERFACE_INGRESS":
            findings.append({"kind": "missing_persona_ingress_phase", "severity": "block", "path": str(ACTIVE_PACKET_RELATIVE_PATH), "detail": phase_sequence})
        if not phase_sequence or phase_sequence[-1] != "PERSONA_INTERFACE_RESPONSE":
            findings.append({"kind": "missing_persona_response_phase", "severity": "block", "path": str(ACTIVE_PACKET_RELATIVE_PATH), "detail": phase_sequence})

    cursor_rule_path = shell_root / CURSOR_RELAY_RULE_RELATIVE_PATH
    if cursor_rule_path.exists():
        text = cursor_rule_path.read_text(encoding="utf-8", errors="replace")
        if re.search(r"run\s+or\s+manually\s+apply", text, flags=re.IGNORECASE):
            findings.append({"kind": "manual_gate_fallback_phrase", "severity": "block", "path": str(CURSOR_RELAY_RULE_RELATIVE_PATH), "detail": "run or manually apply"})

    legacy_references: list[dict[str, Any]] = []
    for path in _iter_scanned_files(shell_root):
        rel = path.relative_to(shell_root).as_posix()
        try:
            lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for idx, line in enumerate(lines, start=1):
            if not re.search(r"\b(MINI|CAPSULE|Mini|Capsule)\b", line):
                continue
            lower = line.lower()
            allowed = any(marker in lower for marker in ALLOWED_LEGACY_CONTEXT_MARKERS)
            legacy_references.append({"path": rel, "line": idx, "allowed_classified_reference": allowed, "excerpt": line.strip()[:240]})
            for pattern in LEGACY_CONTEXT_PATTERNS:
                if pattern.search(line) and not allowed:
                    findings.append({"kind": "legacy_mini_capsule_primary_context_reference", "severity": "block", "path": rel, "line": idx, "detail": line.strip()[:240]})

    blocking = [item for item in findings if item.get("severity") == "block"]
    return {
        "schema_id": "ion.stale_surface_audit.v1",
        "created_at": _iso_now(),
        "verdict": "ION_STALE_SURFACE_AUDIT_READY" if not blocking else "ION_STALE_SURFACE_AUDIT_BLOCKED",
        "active_packet_path": str(ACTIVE_PACKET_RELATIVE_PATH),
        "active_template": active_template,
        "carrier": carrier,
        "phase_sequence": phase_sequence,
        "findings": findings,
        "legacy_reference_count": len(legacy_references),
        "legacy_references_sample": legacy_references[:30],
        "non_claims": [
            "Historical/source/forensic references are allowed when classified.",
            "Cursor adapter support is not removed.",
            "Mini/Capsule material may be mined into ContextPackages but is not primary live context.",
        ],
    }


def write_stale_surface_audit(root: str | Path | None = None, output_relative_path: str | Path = ACTIVE_AUDIT_OUTPUT_RELATIVE_PATH) -> dict[str, Any]:
    shell_root = resolve_shell_root_from_ion_root(root)
    report = build_stale_surface_audit(shell_root)
    output_path = shell_root / Path(output_relative_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report["output_path"] = str(Path(output_relative_path))
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit GPT sandbox package for stale active surfaces.")
    parser.add_argument("--ion-root", default=None)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    report = write_stale_surface_audit(args.ion_root) if args.write else build_stale_surface_audit(args.ion_root)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["verdict"])
    return 0 if report["verdict"] == "ION_STALE_SURFACE_AUDIT_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
