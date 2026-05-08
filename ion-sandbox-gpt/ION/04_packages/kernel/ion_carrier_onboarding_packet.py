"""ION-native carrier onboarding packet builder.

This module builds the actual carrier onboarding path from ION-native surfaces:
root proof, current operating packet, carrier profile, mount contract, active
packets, role/context surfaces, compiled bundles, execution templates, and proof
flow. It does not use root-level START_HERE/AGENTS markdown as authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .ion_carrier_onboard import resolve_shell_root_from_ion_root

SCHEMA_ID = "ion.carrier_onboarding_packet.v1"
VERSION_LINE = "V1_1_GPT_SANDBOX_CARRIER_ONBOARDING_WIRED"
OUTPUT_RELATIVE_PATH = Path("ION/05_context/current/ACTIVE_CARRIER_ONBOARDING_PACKET.json")
CURRENT_OPERATING_PACKET = Path("ION/docs/setup/ION_CURRENT_OPERATING_PACKET_V119.md")
MOUNT_CONTRACT = Path("ION/02_architecture/ION_MOUNT_CONTRACT.md")

CARRIER_PROFILE_BY_ALIAS = {
    # Self-contained uploaded-zip / GPT sandbox carrier lane.
    # This is distinct from the ChatGPT-browser MCP connector lane below.
    "gpt_sandbox": "ION/03_registry/gpt_sandbox_carrier_profile.yaml",
    "gpt_sandbox_carrier": "ION/03_registry/gpt_sandbox_carrier_profile.yaml",
    "gpt_sandbox_runtime": "ION/03_registry/gpt_sandbox_carrier_profile.yaml",
    "gpt_uploaded_zip": "ION/03_registry/gpt_sandbox_carrier_profile.yaml",
    "gpt_full_ion_package": "ION/03_registry/gpt_sandbox_carrier_profile.yaml",
    "ion_gpt": "ION/03_registry/gpt_sandbox_carrier_profile.yaml",
    "ion_gpt_sandbox": "ION/03_registry/gpt_sandbox_carrier_profile.yaml",
    "single_carrier_sandbox": "ION/03_registry/gpt_sandbox_carrier_profile.yaml",
    "self_contained_sandbox": "ION/03_registry/gpt_sandbox_carrier_profile.yaml",
    "gpt-5.5 thinking": "ION/03_registry/gpt_sandbox_carrier_profile.yaml",
    "gpt-5.5": "ION/03_registry/gpt_sandbox_carrier_profile.yaml",
    # Browser/MCP connector carrier lane.
    "chatgpt": "ION/03_registry/chatgpt_browser_carrier_profile.yaml",
    "chatgpt_browser": "ION/03_registry/chatgpt_browser_carrier_profile.yaml",
    "full_carrier_mcp_parity": "ION/03_registry/chatgpt_browser_carrier_profile.yaml",
    "chatgpt_browser_full_carrier": "ION/03_registry/chatgpt_browser_carrier_profile.yaml",
    "gpt55": "ION/03_registry/chatgpt_browser_carrier_profile.yaml",
    "sev": "ION/03_registry/chatgpt_browser_carrier_profile.yaml",
    "codex": "ION/03_registry/codex_cli_carrier_profile.yaml",
    "codex_cli": "ION/03_registry/codex_cli_carrier_profile.yaml",
    "codex_extension": "ION/03_registry/codex_extension_carrier_profile.yaml",
    "cursor": "ION/03_registry/codex_extension_carrier_profile.yaml",
}

ACTIVE_PACKET_PATHS = (
    "ION/05_context/current/ACTIVE_WORK_PACKET.json",
    "ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json",
    "ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json",
    "ION/05_context/current/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json",
    "ION/05_context/current/ACTIVE_STEWARD_INTEGRATION_QUEUE.json",
    "ION/05_context/current/ACTIVE_OPERATOR_MESSAGE_QUEUE.json",
    "ION/05_context/current/ACTIVE_HUMAN_GATE_QUEUE.json",
    "ION/05_context/current/ACTIVE_AGENT_CONTEXT_WINDOW_PLAN.json",
    "ION/05_context/current/ACTIVE_FRONT_DOOR_TEAM_PLAN.json",
    "ION/05_context/current/ACTIVE_COCKPIT_VIEW_MODEL.json",
)

ROLE_BOOT_PATHS = (
    "ION/03_registry/boots/RELAY.boot.md",
    "ION/03_registry/boots/STEWARD.boot.md",
    "ION/03_registry/boots/PERSONA_INTERFACE.boot.md",
    "ION/03_registry/boots/MASON.boot.md",
    "ION/03_registry/boots/NEMESIS.boot.md",
)

ROLE_CONTEXT_PATHS = (
    "ION/05_context/current/agent_context_systems/RELAY.context_system.md",
    "ION/05_context/current/agent_context_systems/STEWARD.context_system.md",
    "ION/05_context/current/agent_context_systems/PERSONA_INTERFACE.context_system.md",
    "ION/05_context/current/agent_context_systems/MASON.context_system.md",
    "ION/05_context/current/agent_context_systems/NEMESIS.context_system.md",
)

EXECUTION_TEMPLATE_PATHS = (
    "ION/07_templates/carriers/CARRIER_MOUNT_PROOF.md",
    "ION/07_templates/carriers/CARRIER_CAPABILITY_SURVEY.md",
    "ION/07_templates/carriers/CARRIER_SESSION_PACKET.md",
    "ION/07_templates/carriers/GPT_SANDBOX_CARRIER_SESSION_PACKET.md",
    "ION/07_templates/carriers/CHATGPT_BROWSER_CONNECTOR_SESSION_PACKET.md",
    "ION/07_templates/carriers/CODEX_CLI_EXECUTION_PACKET.md",
    "ION/07_templates/carriers/CODEX_EXTENSION_EXECUTION_PACKET.md",
    "ION/07_templates/carriers/FULL_CARRIER_MOUNT_PROOF.md",
    "ION/07_templates/actions/FULL_CARRIER_ACTION_RECEIPT.md",
)

PROOF_FLOW = (
    {
        "step": "context_proof",
        "surface": "kernel.ion_context_proof_gate",
        "required_section": "### CONTEXT PROOF",
    },
    {
        "step": "template_action_proof",
        "surface": "kernel.ion_template_action_gate",
        "required_section": "### TEMPLATE ACTION PROOF",
    },
    {
        "step": "task_return_intake",
        "surface": "kernel.ion_carrier_task_return",
        "required_section": "### RESULT",
    },
    {
        "step": "receipt_flow",
        "surface": "ION/05_context/current/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json",
        "required_section": "receipt_or_return_record",
    },
)


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


def _surface(root: Path, rel: str | Path, *, include_excerpt: bool = False) -> dict[str, Any]:
    rel_path = Path(rel)
    path = root / rel_path
    text = _read_text(path)
    result: dict[str, Any] = {
        "path": rel_path.as_posix(),
        "exists": path.exists(),
        "is_file": path.is_file(),
        "sha256": _sha256_file(path),
    }
    if include_excerpt and text:
        result["excerpt"] = text[:1200]
    return result


def _latest_compiled_bundle_surfaces(root: Path, *, limit: int = 8) -> list[dict[str, Any]]:
    cycles_root = root / "ION/05_context/current/execution_cycles"
    if not cycles_root.exists():
        return []
    bundles = sorted(
        cycles_root.glob("*/**/*COMPILED*CONTEXT_BUNDLE.md"),
        key=lambda path: path.as_posix(),
        reverse=True,
    )
    return [_surface(root, path.relative_to(root)) for path in bundles[:limit]]


def _carrier_profile_path(carrier_id: str, explicit_profile: str | None = None) -> str:
    if explicit_profile:
        return explicit_profile
    normalized = carrier_id.lower().strip()
    return CARRIER_PROFILE_BY_ALIAS.get(normalized, "ION/03_registry/chatgpt_browser_carrier_profile.yaml")


def _safe_carrier_slug(carrier_id: str) -> str:
    text = carrier_id.lower().strip()
    return "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in text).strip("_") or "unknown"


def _profile_scalar(text: str, key: str) -> str | None:
    prefix = f"{key}:"
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(prefix):
            value = stripped[len(prefix):].strip().strip("\"'")
            return value or None
    return None


def _carrier_profile_metadata(root: Path, rel: str | Path) -> dict[str, Any]:
    text = _read_text(root / rel)
    return {
        "carrier_id": _profile_scalar(text, "carrier_id"),
        "project_facing_callsign": _profile_scalar(text, "project_facing_callsign"),
        "callsign_authority": _profile_scalar(text, "callsign_authority"),
        "callsign_decision_receipt": _profile_scalar(text, "callsign_decision_receipt"),
        "production_authority": False,
        "live_execution_authority": False,
    }


def carrier_onboarding_packet_output_path(carrier_id: str) -> Path:
    """Return the carrier-specific active onboarding packet path."""

    slug = _safe_carrier_slug(carrier_id)
    return OUTPUT_RELATIVE_PATH.with_name(f"ACTIVE_CARRIER_ONBOARDING_PACKET.{slug}.json")


def build_carrier_onboarding_packet(
    root: str | Path | None,
    *,
    carrier_id: str = "chatgpt_browser",
    carrier_profile_path: str | None = None,
    include_excerpts: bool = False,
) -> dict[str, Any]:
    shell_root = resolve_shell_root_from_ion_root(root)
    root_proof = {
        "shell_root": shell_root.as_posix(),
        "pyproject_toml": _surface(shell_root, "pyproject.toml"),
        "repo_authority": _surface(shell_root, "ION/REPO_AUTHORITY.md", include_excerpt=include_excerpts),
    }
    root_confirmed = bool(root_proof["pyproject_toml"]["exists"] and root_proof["repo_authority"]["exists"])
    profile_rel = _carrier_profile_path(carrier_id, carrier_profile_path)
    root_markdown = {
        "AGENTS.md": {
            "path": "AGENTS.md",
            "exists": (shell_root / "AGENTS.md").exists(),
            "authority": False,
        },
        "START_HERE_FOR_ANY_AGENT.md": {
            "path": "START_HERE_FOR_ANY_AGENT.md",
            "exists": (shell_root / "START_HERE_FOR_ANY_AGENT.md").exists(),
            "authority": False,
        },
    }
    findings: list[str] = []
    if root_confirmed:
        findings.append("shell_root_confirmed")
    else:
        findings.append("shell_root_not_confirmed")
    if any(value["exists"] for value in root_markdown.values()):
        findings.append("root_markdown_present_but_not_onboarding_authority")
    else:
        findings.append("root_markdown_absent_from_hot_onboarding")

    current_packet = _surface(shell_root, CURRENT_OPERATING_PACKET, include_excerpt=include_excerpts)
    profile = _surface(shell_root, profile_rel, include_excerpt=include_excerpts)
    profile_metadata = _carrier_profile_metadata(shell_root, profile_rel)
    mount_contract = _surface(shell_root, MOUNT_CONTRACT, include_excerpt=include_excerpts)
    if current_packet["exists"]:
        findings.append("current_operating_packet_loaded")
    if profile["exists"]:
        findings.append("carrier_profile_loaded")
    if mount_contract["exists"]:
        findings.append("mount_contract_loaded")

    active_packets = [_surface(shell_root, rel) for rel in ACTIVE_PACKET_PATHS]
    role_boots = [_surface(shell_root, rel) for rel in ROLE_BOOT_PATHS]
    role_contexts = [_surface(shell_root, rel) for rel in ROLE_CONTEXT_PATHS]
    execution_templates = [_surface(shell_root, rel) for rel in EXECUTION_TEMPLATE_PATHS]
    compiled_bundles = _latest_compiled_bundle_surfaces(shell_root)
    required_present = (
        root_confirmed
        and current_packet["exists"]
        and profile["exists"]
        and mount_contract["exists"]
        and any(packet["exists"] for packet in active_packets)
        and any(template["exists"] for template in execution_templates)
    )
    if required_present:
        findings.append("ion_native_carrier_onboarding_ready")
    else:
        findings.append("ion_native_carrier_onboarding_incomplete")

    return {
        "schema_id": SCHEMA_ID,
        "version_line": VERSION_LINE,
        "generated_at": _now(),
        "carrier_id": carrier_id,
        "root_confirmed": root_confirmed,
        "onboarding_verdict": "ION_CARRIER_ONBOARDING_PACKET_READY" if required_present else "ION_CARRIER_ONBOARDING_PACKET_INCOMPLETE",
        "correct_onboarding_order": [
            "confirm_shell_root",
            "read_current_operating_packet",
            "resolve_carrier_identity_from_profile",
            "load_mount_contract",
            "load_active_packets",
            "load_role_context_surfaces_and_compiled_bundles",
            "load_execution_packet_templates",
            "execute_context_proof_template_action_proof_task_return_receipt_flow",
        ],
        "root_proof": root_proof,
        "current_operating_packet": current_packet,
        "carrier_profile": profile,
        "carrier_profile_metadata": profile_metadata,
        "mount_contract": mount_contract,
        "active_packets": active_packets,
        "role_boot_surfaces": role_boots,
        "role_context_surfaces": role_contexts,
        "compiled_context_bundles": compiled_bundles,
        "execution_packet_templates": execution_templates,
        "proof_flow": list(PROOF_FLOW),
        "root_markdown_status": root_markdown,
        "root_markdown_onboarding_authority": False,
        "next_lawful_action": "Use this packet as carrier onboarding input, then execute only through proof-gated task return and receipt flow.",
        "findings": findings,
        "production_authority": False,
        "live_execution_authority": False,
        "deployment_authority": False,
    }


def write_carrier_onboarding_packet(
    root: str | Path | None,
    *,
    carrier_id: str = "chatgpt_browser",
    carrier_profile_path: str | None = None,
    output: str | Path | None = None,
) -> dict[str, Any]:
    shell_root = resolve_shell_root_from_ion_root(root)
    packet = build_carrier_onboarding_packet(
        shell_root,
        carrier_id=carrier_id,
        carrier_profile_path=carrier_profile_path,
    )
    out = shell_root / (Path(output) if output else OUTPUT_RELATIVE_PATH)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return packet


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build the ION-native carrier onboarding packet.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--carrier", default="chatgpt_browser")
    parser.add_argument("--carrier-profile", default=None)
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--output", default=None)
    parser.add_argument("--include-excerpts", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.write:
        result = write_carrier_onboarding_packet(
            args.ion_root,
            carrier_id=args.carrier,
            carrier_profile_path=args.carrier_profile,
            output=args.output,
        )
    else:
        result = build_carrier_onboarding_packet(
            args.ion_root,
            carrier_id=args.carrier,
            carrier_profile_path=args.carrier_profile,
            include_excerpts=args.include_excerpts,
        )
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["onboarding_verdict"])
        for finding in result["findings"]:
            print(f"- {finding}")
    return 0 if result["root_confirmed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
