"""Audit Codex extension carrier mount surfaces for ION V106."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


OUTPUT_RELATIVE_PATH = Path("ION/05_context/current/CODEX_EXTENSION_CARRIER_AUDIT_V106.json")

REQUIRED_FILES = {
    "protocol": "ION/02_architecture/CODEX_EXTENSION_CARRIER_PROTOCOL.md",
    "profile": "ION/03_registry/codex_extension_carrier_profile.yaml",
    "execution_packet_template": "ION/07_templates/carriers/CODEX_EXTENSION_EXECUTION_PACKET.md",
    "generic_codex_profile": "ION/04_agents/carriers/CODEX_CARRIER.profile.md",
    "carrier_registry": "ION/04_agents/carriers/carrier_registry.json",
    "mount_proof_template": "ION/07_templates/carriers/CARRIER_MOUNT_PROOF.md",
    "status_module": "ION/04_packages/kernel/ion_status.py",
    "task_return_module": "ION/04_packages/kernel/ion_carrier_task_return.py",
    "context_proof_gate": "ION/04_packages/kernel/ion_context_proof_gate.py",
}

PROFILE_PHRASES = (
    "schema_id: ion.codex_extension_carrier_profile.v1",
    "carrier_id: CODEX_EXTENSION_CARRIER",
    "host_family: codex_extension",
    "default_level: L1_TOOL_ASSISTED",
    "can_spawn_host_subagents: unproven",
    "must_not_claim_ion_identity: true",
    "must_not_claim_steward_relay_persona: true",
    "context_proof_gate: kernel.ion_context_proof_gate",
    "return_intake_module: kernel.ion_carrier_task_return",
    "production_authority: false",
    "live_execution_authority: false",
)

TEMPLATE_PHRASES = (
    "### CONTEXT PROOF",
    "### TEMPLATE ACTION PROOF",
    "### RESULT",
    "production_authority: `false`",
    "live_execution_authority: `false`",
)

PROTOCOL_PHRASES = (
    "Codex extension / Codex CLI is a carrier",
    "Do not claim to be ION identity.",
    "Do not claim STEWARD/RELAY/PERSONA authority.",
    "subagent operation remains unproven",
)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _resolve_shell_root(root: str | Path | None = None) -> Path:
    candidate = Path(root or ".").expanduser().resolve()
    for path in (candidate, *candidate.parents):
        if (path / "pyproject.toml").exists() and (path / "ION/REPO_AUTHORITY.md").exists():
            return path
    raise FileNotFoundError("Could not resolve ION shell root; expected pyproject.toml and ION/REPO_AUTHORITY.md")


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def _missing_phrases(label: str, text: str, phrases: tuple[str, ...]) -> list[str]:
    return [f"{label}:missing_phrase:{phrase}" for phrase in phrases if phrase not in text]


def audit_codex_extension_carrier(root: str | Path | None = None) -> dict[str, Any]:
    shell_root = _resolve_shell_root(root)
    findings: list[str] = []

    for label, rel in REQUIRED_FILES.items():
        if not (shell_root / rel).exists():
            findings.append(f"missing_{label}:{rel}")

    profile_path = shell_root / REQUIRED_FILES["profile"]
    if profile_path.exists():
        findings.extend(_missing_phrases("profile", _read(profile_path), PROFILE_PHRASES))

    template_path = shell_root / REQUIRED_FILES["execution_packet_template"]
    if template_path.exists():
        findings.extend(_missing_phrases("execution_packet_template", _read(template_path), TEMPLATE_PHRASES))

    protocol_path = shell_root / REQUIRED_FILES["protocol"]
    if protocol_path.exists():
        findings.extend(_missing_phrases("protocol", _read(protocol_path), PROTOCOL_PHRASES))

    ready = not findings
    return {
        "schema_id": "ion.codex_extension_carrier_audit.v1",
        "generated_at": _now(),
        "verdict": "ION_CODEX_EXTENSION_CARRIER_READY" if ready else "ION_CODEX_EXTENSION_CARRIER_BLOCKED",
        "findings": findings,
        "checked_files": REQUIRED_FILES,
        "carrier_id": "CODEX_EXTENSION_CARRIER",
        "host_family": "codex_extension",
        "mount_level_ceiling": "L1_TOOL_ASSISTED_UNLESS_HOST_SPAWN_PROVEN",
        "capability_claims": {
            "filesystem_read": "PROFILE_BOUND",
            "filesystem_write": "PROFILE_BOUND",
            "shell_command_execution": "PROFILE_BOUND",
            "test_execution": "PROFILE_BOUND",
            "host_subagents": "UNPROVEN_IN_THIS_AUDIT",
        },
        "required_return_sections": ["### CONTEXT PROOF", "### TEMPLATE ACTION PROOF", "### RESULT"],
        "return_intake_module": "kernel.ion_carrier_task_return",
        "context_proof_gate": "kernel.ion_context_proof_gate",
        "forbidden_claims": [
            "ION identity",
            "STEWARD authority",
            "RELAY authority",
            "PERSONA authority",
            "production authority",
            "live host subagents without spawn proof",
        ],
        "production_authority": False,
        "live_execution_authority": False,
    }


def write_codex_extension_carrier_audit(
    root: str | Path | None = None,
    *,
    output: str | Path | None = None,
) -> dict[str, Any]:
    shell_root = _resolve_shell_root(root)
    audit = audit_codex_extension_carrier(shell_root)
    out = shell_root / (Path(output) if output else OUTPUT_RELATIVE_PATH)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return audit


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit Codex extension carrier mount surfaces.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = (
        write_codex_extension_carrier_audit(args.ion_root, output=args.output)
        if args.write
        else audit_codex_extension_carrier(args.ion_root)
    )
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["verdict"])
        for finding in result["findings"]:
            print(f"- {finding}")
    return 0 if result["verdict"] == "ION_CODEX_EXTENSION_CARRIER_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
