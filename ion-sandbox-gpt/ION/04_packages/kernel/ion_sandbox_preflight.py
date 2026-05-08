"GPT sandbox preflight and capability reconciliation for ION."

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

from .ion_carrier_onboard import (
    ACTIVE_PACKET_RELATIVE_PATH,
    PROFILE_BY_CARRIER_ALIAS,
    resolve_shell_root_from_ion_root,
    _read_simple_yaml,
)

SANDBOX_ENVIRONMENT_CONTRACT_RELATIVE_PATH = Path("ION/02_architecture/ION_GPT_SANDBOX_ENVIRONMENT_CONTRACT.md")
ACTIVE_SANDBOX_PREFLIGHT_RELATIVE_PATH = Path("ION/05_context/current/ACTIVE_GPT_SANDBOX_PREFLIGHT.json")

CAPABILITY_KEYS = (
    "can_read_files",
    "can_edit_files",
    "can_run_tests",
    "can_spawn_carrier_slots",
    "can_use_mcp",
    "production_authority",
    "live_execution_authority",
)

HOST_OBSERVED_GPT_SANDBOX_CAPABILITIES: dict[str, bool] = {
    "can_read_files": True,
    "can_edit_files": True,
    "can_run_tests": True,
    "can_spawn_carrier_slots": False,
    "can_use_mcp": False,
    "can_edit_sandbox_copy": True,
    "can_export_candidate_zip": True,
    "can_run_python_validation_in_sandbox": True,
    "can_patch_live_repo": False,
    "can_push_git": False,
    "production_authority": False,
    "live_execution_authority": False,
}


def _iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _profile_path_for_carrier(carrier: str) -> Path:
    return PROFILE_BY_CARRIER_ALIAS.get(
        (carrier or "").lower().strip(),
        Path("ION/03_registry/gpt_sandbox_carrier_profile.yaml"),
    )


def _capability_subset(source: Mapping[str, Any] | None) -> dict[str, Any]:
    if not isinstance(source, Mapping):
        return {}
    return {key: source[key] for key in CAPABILITY_KEYS if key in source}


def _active_packet_capabilities(active_packet: Mapping[str, Any] | None) -> dict[str, Any]:
    if not isinstance(active_packet, Mapping):
        return {}
    caps = active_packet.get("carrier_capabilities")
    return _capability_subset(caps if isinstance(caps, Mapping) else {})


def _compare_capabilities(
    *,
    profile_caps: Mapping[str, Any],
    packet_caps: Mapping[str, Any],
    host_caps: Mapping[str, Any],
) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for key in CAPABILITY_KEYS:
        values = {
            "profile": profile_caps.get(key, "UNDECLARED"),
            "active_packet": packet_caps.get(key, "UNDECLARED"),
            "host_observed": host_caps.get(key, "UNDECLARED"),
        }
        declared_values = [value for value in values.values() if value != "UNDECLARED"]
        if len(set(map(str, declared_values))) > 1:
            findings.append({
                "kind": "capability_mismatch",
                "capability": key,
                "values": values,
                "severity": "review" if key not in {"production_authority", "live_execution_authority"} else "block",
            })

    for key in ("production_authority", "live_execution_authority"):
        if profile_caps.get(key) is not False or packet_caps.get(key) is not False or host_caps.get(key) is not False:
            findings.append({
                "kind": "authority_not_false",
                "capability": key,
                "severity": "block",
                "values": {
                    "profile": profile_caps.get(key, "UNDECLARED"),
                    "active_packet": packet_caps.get(key, "UNDECLARED"),
                    "host_observed": host_caps.get(key, "UNDECLARED"),
                },
            })

    if host_caps.get("can_use_mcp") is False and (profile_caps.get("can_use_mcp") is True or packet_caps.get("can_use_mcp") is True):
        findings.append({"kind": "mcp_declared_but_not_host_observed", "severity": "review", "capability": "can_use_mcp"})
    if host_caps.get("can_spawn_carrier_slots") is False and (profile_caps.get("can_spawn_carrier_slots") is True or packet_caps.get("can_spawn_carrier_slots") is True):
        findings.append({"kind": "carrier_spawn_declared_but_not_host_observed", "severity": "review", "capability": "can_spawn_carrier_slots"})
    return findings


def build_gpt_sandbox_preflight(
    root: str | Path | None = None,
    *,
    carrier: str = "GPT_SANDBOX_CARRIER",
    host_observed_capabilities: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    shell_root = resolve_shell_root_from_ion_root(root)
    profile_rel = _profile_path_for_carrier(carrier)
    profile_path = shell_root / profile_rel
    active_packet_path = shell_root / ACTIVE_PACKET_RELATIVE_PATH
    contract_path = shell_root / SANDBOX_ENVIRONMENT_CONTRACT_RELATIVE_PATH

    profile = _read_simple_yaml(profile_path)
    active_packet = _read_json(active_packet_path) or {}
    host_caps = dict(HOST_OBSERVED_GPT_SANDBOX_CAPABILITIES)
    host_caps.update(dict(host_observed_capabilities or {}))

    profile_caps = _capability_subset(profile)
    packet_caps = _active_packet_capabilities(active_packet)
    findings = _compare_capabilities(profile_caps=profile_caps, packet_caps=packet_caps, host_caps=host_caps)
    blocking = [finding for finding in findings if finding.get("severity") == "block"]

    allowed_paths = active_packet.get("allowed_paths", []) if isinstance(active_packet, Mapping) else []
    if not isinstance(allowed_paths, list):
        allowed_paths = []

    return {
        "schema_id": "ion.gpt_sandbox_preflight.v1",
        "created_at": _iso_now(),
        "carrier": carrier,
        "preflight_verdict": "ION_GPT_SANDBOX_PREFLIGHT_READY" if not blocking else "ION_GPT_SANDBOX_PREFLIGHT_BLOCKED",
        "shell_root_confirmed": (shell_root / "ION/REPO_AUTHORITY.md").exists(),
        "shell_root": str(shell_root),
        "ion_root": str(shell_root / "ION"),
        "contract_path": str(SANDBOX_ENVIRONMENT_CONTRACT_RELATIVE_PATH),
        "contract_exists": contract_path.exists(),
        "carrier_profile_path": str(profile_rel),
        "carrier_profile_exists": profile_path.exists(),
        "active_work_packet_path": str(ACTIVE_PACKET_RELATIVE_PATH),
        "active_work_packet_exists": active_packet_path.exists(),
        "profile_capabilities": profile_caps,
        "active_packet_capabilities": packet_caps,
        "host_observed_capabilities": host_caps,
        "capability_findings": findings,
        "allowed_paths": allowed_paths,
        "test_tiers": [
            "ion_status",
            "focused_gpt_sandbox_readiness_tests",
            "changed_surface_kernel_tests",
            "segmented_pytest_slices",
            "monolithic_pytest_only_when_host_allows",
        ],
        "sandbox_boundary": {
            "can_edit_sandbox_copy": bool(host_caps.get("can_edit_sandbox_copy")),
            "can_export_candidate_zip": bool(host_caps.get("can_export_candidate_zip")),
            "can_patch_live_repo": False,
            "can_push_git": False,
            "production_authority": False,
            "live_execution_authority": False,
        },
        "next_lawful_action": (
            "Proceed with bounded sandbox work and receipt export"
            if not blocking
            else "Stop and resolve blocking authority mismatch before role execution"
        ),
    }


def write_gpt_sandbox_preflight(
    root: str | Path | None = None,
    *,
    carrier: str = "GPT_SANDBOX_CARRIER",
    host_observed_capabilities: Mapping[str, Any] | None = None,
    output_relative_path: str | Path = ACTIVE_SANDBOX_PREFLIGHT_RELATIVE_PATH,
) -> dict[str, Any]:
    shell_root = resolve_shell_root_from_ion_root(root)
    report = build_gpt_sandbox_preflight(shell_root, carrier=carrier, host_observed_capabilities=host_observed_capabilities)
    output_path = shell_root / Path(output_relative_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    report["preflight_report_path"] = str(Path(output_relative_path))
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build/write the ION GPT sandbox preflight report.")
    parser.add_argument("--ion-root", default=None)
    parser.add_argument("--carrier", default="GPT_SANDBOX_CARRIER")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    report = write_gpt_sandbox_preflight(args.ion_root, carrier=args.carrier) if args.write else build_gpt_sandbox_preflight(args.ion_root, carrier=args.carrier)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(report["preflight_verdict"])
    return 0 if report["preflight_verdict"] == "ION_GPT_SANDBOX_PREFLIGHT_READY" else 1


if __name__ == "__main__":
    raise SystemExit(main())
