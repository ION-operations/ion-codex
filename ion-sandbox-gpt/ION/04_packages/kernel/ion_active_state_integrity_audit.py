"""Audit active runtime state for test/temp contamination.

This catches a concrete failure mode observed in V106: tests writing
``/tmp/pytest-*`` context-package paths into active runtime JSON.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .ion_carrier_onboard import resolve_shell_root_from_ion_root

SCHEMA_ID = "ion.active_state_integrity_audit.v1"
CURRENT = Path("ION/05_context/current")
OUTPUT = CURRENT / "ACTIVE_STATE_INTEGRITY_AUDIT.json"
FORBIDDEN_TEMP_MARKERS = ("/tmp/pytest", "\\pytest-", "/private/var/folders/")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _json_path(parent: str, key: str | int) -> str:
    if isinstance(key, int):
        return f"{parent}[{key}]"
    if not parent:
        return key
    return f"{parent}.{key}"


def _scan_strings(value: Any, *, json_path: str = "") -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    if isinstance(value, str):
        if any(marker in value for marker in FORBIDDEN_TEMP_MARKERS):
            findings.append((json_path or "$", value))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            findings.extend(_scan_strings(item, json_path=_json_path(json_path, index)))
    elif isinstance(value, dict):
        for key, item in value.items():
            findings.extend(_scan_strings(item, json_path=_json_path(json_path, str(key))))
    return findings


def audit_active_state_integrity(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = resolve_shell_root_from_ion_root(root)
    current = shell_root / CURRENT
    checked_files: list[str] = []
    findings: list[dict[str, str]] = []

    if not current.exists():
        return {
            "schema_id": SCHEMA_ID,
            "generated_at": utc_now(),
            "checked_files": [],
            "finding_count": 1,
            "findings": [{"path": CURRENT.as_posix(), "json_path": "$", "value": "missing_current_directory"}],
            "verdict": "ION_ACTIVE_STATE_INTEGRITY_BLOCKED",
            "accepted": False,
            "production_authority": False,
            "live_execution_authority": False,
        }

    for path in sorted(current.glob("ACTIVE_*.json")):
        if path.name == OUTPUT.name:
            continue
        rel = path.relative_to(shell_root).as_posix()
        checked_files.append(rel)
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            findings.append({"path": rel, "json_path": "$", "value": f"json_read_error:{exc}"})
            continue
        for json_path, value in _scan_strings(payload):
            findings.append({"path": rel, "json_path": json_path, "value": value})

    return {
        "schema_id": SCHEMA_ID,
        "generated_at": utc_now(),
        "checked_files": checked_files,
        "self_audit_path": OUTPUT.as_posix(),
        "finding_count": len(findings),
        "findings": findings,
        "verdict": "ION_ACTIVE_STATE_INTEGRITY_READY" if not findings else "ION_ACTIVE_STATE_INTEGRITY_BLOCKED",
        "accepted": not findings,
        "production_authority": False,
        "live_execution_authority": False,
    }


def write_active_state_integrity_audit(
    root: str | Path | None = None,
    *,
    output: str | Path | None = None,
) -> dict[str, Any]:
    shell_root = resolve_shell_root_from_ion_root(root)
    audit = audit_active_state_integrity(shell_root)
    out = shell_root / (Path(output) if output else OUTPUT)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return audit


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit ION active runtime state for test/temp contamination.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    audit = (
        write_active_state_integrity_audit(args.ion_root, output=args.output)
        if args.write
        else audit_active_state_integrity(args.ion_root)
    )
    if args.json:
        print(json.dumps(audit, indent=2, sort_keys=True))
    else:
        print(audit["verdict"])
        for finding in audit["findings"]:
            print(f"- {finding['path']} {finding['json_path']}: {finding['value']}")
    return 0 if audit["accepted"] else 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
