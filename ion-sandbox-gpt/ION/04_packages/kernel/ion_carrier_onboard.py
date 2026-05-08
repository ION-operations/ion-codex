"""Default carrier onboarding front door for ION.

This module binds the existing sequential/manual kernel route substrate into one
carrier-readable active work packet. It does not grant production authority, live
execution authority, arbitrary shell authority, or a new carrier ontology.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .sequential_kernel import SequentialKernelRouter, Workstream, default_repo_root

ACTIVE_PACKET_RELATIVE_PATH = Path("ION/05_context/current/ACTIVE_WORK_PACKET.json")
DEFAULT_TEMPLATE_PATH = "ION/docs/cursor/ION_CURSOR_WORK_CYCLE_PACKET.md"
DEFAULT_MODE = "MANUAL_TEMPLATE_BOUND_WORKFLOW"
PROFILE_BY_CARRIER_ALIAS = {
    # Self-contained uploaded-zip / GPT sandbox carrier lane.
    # Keep this in parity with ion_carrier_onboarding_packet.CARRIER_PROFILE_BY_ALIAS.
    "gpt_sandbox": Path("ION/03_registry/gpt_sandbox_carrier_profile.yaml"),
    "gpt_sandbox_carrier": Path("ION/03_registry/gpt_sandbox_carrier_profile.yaml"),
    "gpt_sandbox_runtime": Path("ION/03_registry/gpt_sandbox_carrier_profile.yaml"),
    "gpt_uploaded_zip": Path("ION/03_registry/gpt_sandbox_carrier_profile.yaml"),
    "gpt_full_ion_package": Path("ION/03_registry/gpt_sandbox_carrier_profile.yaml"),
    "ion_gpt": Path("ION/03_registry/gpt_sandbox_carrier_profile.yaml"),
    "ion_gpt_sandbox": Path("ION/03_registry/gpt_sandbox_carrier_profile.yaml"),
    "single_carrier_sandbox": Path("ION/03_registry/gpt_sandbox_carrier_profile.yaml"),
    "self_contained_sandbox": Path("ION/03_registry/gpt_sandbox_carrier_profile.yaml"),
    "gpt-5.5 thinking": Path("ION/03_registry/gpt_sandbox_carrier_profile.yaml"),
    "gpt-5.5": Path("ION/03_registry/gpt_sandbox_carrier_profile.yaml"),
    "codex": Path("ION/03_registry/codex_extension_carrier_profile.yaml"),
    "codex_extension": Path("ION/03_registry/codex_extension_carrier_profile.yaml"),
    "cursor": Path("ION/03_registry/codex_extension_carrier_profile.yaml"),
    "chatgpt": Path("ION/03_registry/chatgpt_browser_carrier_profile.yaml"),
    "chatgpt_browser": Path("ION/03_registry/chatgpt_browser_carrier_profile.yaml"),
}
EDIT_TEST_CAPABLE_CARRIERS = {"cursor", "codex", "codex_extension", "ide", "terminal"}
CARRIER_CAPABILITY_KEYS = {
    "can_read_files",
    "can_edit_files",
    "can_run_tests",
    "can_spawn_carrier_slots",
    "can_use_mcp",
}


class CarrierOnboardError(RuntimeError):
    """Raised when shell root cannot be resolved for the given path."""

    def __init__(self, *args: object, code: str | None = None) -> None:
        super().__init__(*args)
        self.code = code or "CARRIER_ONBOARD_ERROR"


def resolve_shell_root_from_ion_root(root: str | Path | None) -> Path:
    """Resolve shell (repo) root from a path to `ION/` or to a directory that contains `ION/`."""
    try:
        return _resolve_shell_root(root)
    except FileNotFoundError as exc:
        raise CarrierOnboardError(
            str(exc),
            code="REPO_ROOT_NOT_CONFIRMED",
        ) from exc


def _iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _resolve_shell_root(root: str | Path | None) -> Path:
    if root is None:
        return default_repo_root()
    candidate = Path(root).expanduser().resolve()
    if (candidate / "ION" / "04_packages" / "kernel").is_dir():
        return candidate
    if candidate.name == "ION" and (candidate / "04_packages" / "kernel").is_dir():
        return candidate.parent
    return default_repo_root(candidate)


def _workstream_from_objective(objective: str | None) -> Workstream:
    text = (objective or "").lower()
    if any(word in text for word in ("research", "evidence", "survey")):
        return Workstream.RESEARCH
    if any(word in text for word in ("archaeolog", "recover", "provenance", "lineage")):
        return Workstream.ARCHAEOLOGY
    if any(word in text for word in ("relay", "report", "handoff", "communicat")):
        return Workstream.RELAY
    if any(word in text for word in ("governance", "protocol", "law", "policy")):
        return Workstream.GOVERNANCE
    return Workstream.IMPLEMENTATION


def _role_phase_sequence(trace_roles: list[str]) -> list[str]:
    sequence: list[str] = ["RELAY"]
    for role in trace_roles:
        role_upper = role.upper()
        if role_upper not in sequence:
            sequence.append(role_upper)
    if "STEWARD" not in sequence:
        sequence.insert(1, "STEWARD")
    if sequence[-1] != "STEWARD":
        sequence.append("STEWARD")
    sequence.append("RELAY")
    return sequence


def _path_exists(shell_root: Path, relative_path: str) -> bool:
    return (shell_root / relative_path).exists()


def _parse_yaml_scalar(value: str) -> Any:
    cleaned = value.strip().strip("\"'")
    lowered = cleaned.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "none", "~"}:
        return None
    return cleaned


def _read_simple_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    values: dict[str, Any] = {}
    for raw_line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if raw_line[:1].isspace() or ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        key = key.strip()
        if key and value.strip():
            values[key] = _parse_yaml_scalar(value)
    return values


def _registry_capabilities(shell_root: Path, carrier: str) -> dict[str, Any]:
    profile_rel = PROFILE_BY_CARRIER_ALIAS.get(carrier.lower().strip())
    if profile_rel is None:
        return {}
    profile = _read_simple_yaml(shell_root / profile_rel)
    return {
        key: profile[key]
        for key in CARRIER_CAPABILITY_KEYS
        if key in profile
    }


def _trace_projection(shell_root: Path, objective: str) -> dict[str, Any]:
    router = SequentialKernelRouter.default(shell_root)
    workstream = _workstream_from_objective(objective)
    trace = router.build_trace(workstream, objective=objective)
    missing = trace.missing_required(shell_root)
    sessions: list[dict[str, Any]] = []
    for role_pass, session in zip(trace.passes, trace.sessions):
        sessions.append({
            "role": role_pass.role_name.upper(),
            "purpose": role_pass.purpose,
            "required": role_pass.required,
            "load_targets": [
                {
                    "label": target.label,
                    "path": target.path,
                    "kind": target.kind,
                    "required": target.required,
                    "exists": target.exists(shell_root),
                    "note": target.note,
                }
                for target in session.load_targets
            ],
        })
    return {
        "workstream": workstream.value,
        "required_surfaces_ok": not bool(missing),
        "missing_required_surfaces": {
            role.upper(): [target.path for target in targets]
            for role, targets in missing.items()
        },
        "trace_roles": [role.role_name for role in trace.passes],
        "sessions": sessions,
    }


def _capability_profile(carrier: str, capabilities: Mapping[str, Any] | None = None) -> dict[str, Any]:
    supplied = dict(capabilities or {})
    normalized_carrier = carrier.lower().strip()
    defaults: dict[str, Any] = {
        "carrier": carrier,
        "can_read_files": True,
        "can_edit_files": normalized_carrier in EDIT_TEST_CAPABLE_CARRIERS,
        "can_run_tests": normalized_carrier in EDIT_TEST_CAPABLE_CARRIERS,
        "can_spawn_carrier_slots": normalized_carrier == "cursor",
        "can_use_mcp": True,
        "live_execution_authority": False,
        "production_authority": False,
    }
    defaults.update(supplied)
    defaults["live_execution_authority"] = False
    defaults["production_authority"] = False
    return defaults


def build_active_work_packet(
    shell_root: Path,
    *,
    carrier: str,
    objective: str,
    capabilities: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    trace = _trace_projection(shell_root, objective)
    role_sequence = _role_phase_sequence(list(trace["trace_roles"]))
    template_exists = _path_exists(shell_root, DEFAULT_TEMPLATE_PATH)
    return {
        "packet_type": "ION_ACTIVE_WORK_PACKET",
        "schema_version": "1.0",
        "created_at": _iso_now(),
        "carrier": carrier,
        "carrier_capabilities": _capability_profile(carrier, capabilities),
        "objective": objective,
        "mode": DEFAULT_MODE,
        "active_packet_path": str(ACTIVE_PACKET_RELATIVE_PATH),
        "role_phase_sequence": role_sequence,
        "route_source": {
            "kind": "kernel.sequential_kernel",
            "workstream": trace["workstream"],
            "required_surfaces_ok": trace["required_surfaces_ok"],
            "missing_required_surfaces": trace["missing_required_surfaces"],
        },
        "active_template": DEFAULT_TEMPLATE_PATH,
        "active_template_exists": template_exists,
        "template_status": "present" if template_exists else "missing_template",
        "context_package": {
            "kind": "active_work_packet",
            "source": str(ACTIVE_PACKET_RELATIVE_PATH),
            "route_sessions": trace["sessions"],
        },
        "next_lawful_action": "Execute this active work packet within allowed paths and return evidence through the declared return contract.",
        "allowed_paths": [
            "ION/05_context/current/",
            "ION/04_packages/kernel/",
            "ION/tests/",
            "ION/docs/consolidation/",
            "ION/05_context/signals/",
            "ION/02_architecture/",
        ],
        "forbidden_paths": [
            ".env",
            ".env.*",
            "secrets/",
            "vault/",
            "credentials/",
            "archive roots as authority",
            "sibling roots as authority",
        ],
        "validation_commands": [
            "PYTHONPATH=ION/04_packages pytest -q ION/tests/test_kernel_ion_carrier_onboard.py",
            "PYTHONPATH=ION/04_packages pytest -q ION/tests",
        ],
        "return_contract": [
            "files_changed",
            "sample_onboarding_json",
            "focused_test_result",
            "full_suite_result",
            "commit_hash",
            "remaining_gaps",
        ],
        "integration_target": "STEWARD",
        "visible_report_target": "RELAY",
        "production_authority": False,
        "live_execution_authority": False,
    }


def validate_active_work_packet(packet: Mapping[str, Any]) -> tuple[bool, list[str]]:
    required = (
        "packet_type", "carrier", "objective", "mode", "role_phase_sequence",
        "active_template", "next_lawful_action", "allowed_paths", "forbidden_paths",
        "validation_commands", "return_contract", "integration_target",
        "visible_report_target", "production_authority", "live_execution_authority",
    )
    findings: list[str] = []
    for field in required:
        if field not in packet:
            findings.append(f"missing:{field}")
    if packet.get("packet_type") != "ION_ACTIVE_WORK_PACKET":
        findings.append("invalid:packet_type")
    role_sequence = packet.get("role_phase_sequence")
    if not isinstance(role_sequence, list) or not role_sequence:
        findings.append("invalid:role_phase_sequence")
    else:
        if "RELAY" not in role_sequence:
            findings.append("missing_role:RELAY")
        if "STEWARD" not in role_sequence:
            findings.append("missing_role:STEWARD")
    for field in ("allowed_paths", "forbidden_paths", "validation_commands", "return_contract"):
        value = packet.get(field)
        if not isinstance(value, list) or not value:
            findings.append(f"invalid:{field}")
    if packet.get("production_authority") is not False:
        findings.append("authority:production_not_false")
    if packet.get("live_execution_authority") is not False:
        findings.append("authority:live_execution_not_false")
    return (not findings, findings)


def onboard_carrier(
    root: str | Path | None = None,
    *,
    carrier: str,
    objective: str | None = None,
    capabilities: Mapping[str, Any] | None = None,
    force: bool = False,
) -> dict[str, Any]:
    shell_root = _resolve_shell_root(root)
    objective = objective or "continue the current ION work cycle through the active carrier packet"
    packet_path = shell_root / ACTIVE_PACKET_RELATIVE_PATH
    packet_path.parent.mkdir(parents=True, exist_ok=True)

    created = False
    if packet_path.exists() and not force:
        packet = json.loads(packet_path.read_text(encoding="utf-8"))
    else:
        if capabilities is None:
            capabilities = _registry_capabilities(shell_root, carrier)
        packet = build_active_work_packet(shell_root, carrier=carrier, objective=objective, capabilities=capabilities)
        packet_path.write_text(json.dumps(packet, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        created = True

    valid, findings = validate_active_work_packet(packet)
    return {
        "onboarding_verdict": "ION_DEFAULT_CARRIER_ONBOARDING_READY" if valid else "ION_DEFAULT_CARRIER_ONBOARDING_BLOCKED",
        "created_active_packet": created,
        "active_packet_path": str(ACTIVE_PACKET_RELATIVE_PATH),
        "active_packet_absolute_path": str(packet_path),
        "valid": valid,
        "findings": findings,
        "packet": packet,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Create or load the default ION carrier onboarding packet.")
    parser.add_argument("--ion-root", default=None, help="Path to ION root or shell root containing ION/.")
    parser.add_argument("--carrier", required=True, help="Carrier identifier, e.g. cursor, codex, chatgpt, terminal.")
    parser.add_argument("--objective", default=None, help="Bounded objective used when creating the packet.")
    parser.add_argument("--force", action="store_true", help="Recreate ACTIVE_WORK_PACKET.json even if it exists.")
    parser.add_argument("--write-current", action="store_true", help="Alias for --force; refresh ACTIVE_WORK_PACKET.json for this objective.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text summary.")
    args = parser.parse_args(argv)

    result = onboard_carrier(args.ion_root, carrier=args.carrier, objective=args.objective, force=(args.force or args.write_current))
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["onboarding_verdict"])
        print(f"active_packet_path: {result['active_packet_path']}")
        print(f"created_active_packet: {result['created_active_packet']}")
        if result["findings"]:
            print("findings:")
            for finding in result["findings"]:
                print(f"- {finding}")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
