#!/usr/bin/env python3
"""Validate candidate ION self-knowledge domain-state artifacts.

This is a current-state candidate validation helper, not an accepted kernel test.
It checks parseability and minimum anti-drift/route coverage for the generated
self-knowledge candidate namespace under ION/05_context/current/self_knowledge.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    import yaml
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"PyYAML unavailable: {exc}")

ROOT = Path(__file__).resolve().parents[4]
SK = ROOT / "ION/05_context/current/self_knowledge"
INV = ROOT / "ION/05_context/current/SELF_KNOWLEDGE_ORGAN_INVENTORY_V0_2.json"
MOUNT = ROOT / "ION/05_context/current/ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET.md"

REQUIRED_ANTI_DRIFT = [
    "Do not treat single-carrier mode as ION's intended center.",
    "Do not call the GPT package",
    "Do not let historical donor material become active authority.",
    "Do not turn broad synthesis into state without Steward/human acceptance and receipt.",
]

REQUIRED_DOMAINS = {
    "ion_identity",
    "ion_canon_authority",
    "ion_architecture",
    "ion_agent_role",
    "ion_full_multi_agent_runtime",
    "ion_carrier_embodiment",
    "ion_context_system",
    "ion_template_law",
    "ion_state_steward_receipt",
    "ion_product_package",
    "ion_workpacket",
    "ion_stale_donor_historical",
    "ion_recovery_anti_regression",
    "ion_operations_build",
}

def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))

def main() -> int:
    findings = []
    parsed = []

    for path in [INV, SK / "SELF_KNOWLEDGE_DOMAIN_STATE_INDEX_V0_2.json"]:
        if not path.exists():
            findings.append(f"missing_json:{path}")
            continue
        load_json(path)
        parsed.append(str(path.relative_to(ROOT)))

    for path in sorted((SK / "candidate_registries").glob("*.yaml")) + sorted((SK / "domains").glob("*.yaml")):
        data = load_yaml(path)
        if not isinstance(data, dict):
            findings.append(f"yaml_not_mapping:{path}")
        parsed.append(str(path.relative_to(ROOT)))

    registry = load_yaml(SK / "candidate_registries/domain_registry.candidate.yaml")
    route_registry = load_yaml(SK / "candidate_registries/route_registry.candidate.yaml")
    domains = {d.get("domain_id") for d in registry.get("domains", []) if isinstance(d, dict)}
    missing_domains = sorted(REQUIRED_DOMAINS - domains)
    if missing_domains:
        findings.append(f"missing_domains:{','.join(missing_domains)}")

    routes = route_registry.get("routes", [])
    if len(routes) < 5:
        findings.append("too_few_routes")
    if not any("single_carrier_is_fallback_not_base" in r.get("anti_drift_required", []) for r in routes if isinstance(r, dict)):
        findings.append("missing_single_carrier_reduction_route_guard")
    if not any("do_not_call_gpt_reduced_ion" in r.get("anti_drift_required", []) for r in routes if isinstance(r, dict)):
        findings.append("missing_gpt_reduced_ion_route_guard")
    if not any("no_donor_as_active_authority" in r.get("anti_drift_required", []) for r in routes if isinstance(r, dict)):
        findings.append("missing_donor_authority_route_guard")

    mount_text = MOUNT.read_text(encoding="utf-8")
    for phrase in REQUIRED_ANTI_DRIFT:
        if phrase not in mount_text:
            findings.append(f"missing_mount_anti_drift:{phrase}")

    result = {
        "schema_id": "ion.self_knowledge_candidate_validation.v0_2",
        "accepted": not findings,
        "findings": findings,
        "parsed_files_count": len(parsed),
        "domain_count": len(domains),
        "route_count": len(routes),
        "production_authority": False,
        "live_execution_authority": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not findings else 1

if __name__ == "__main__":
    raise SystemExit(main())
