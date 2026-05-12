"""Read-only local port routing truth for ION connector surfaces."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_ID = "ion.local_port_routing_truth.v1"
READY_VERDICT = "ION_LOCAL_PORT_ROUTING_TRUTH_PROJECTED"
REGISTRY_RELATIVE_PATH = Path("ION/03_registry/ion_local_port_routing_registry.json")

EXPECTED_CANONICAL_PORTS = {
    "ion_chatops_bridge": 8767,
    "ion_mcp_preview": 8765,
    "ion_action_gateway": 8777,
    "ion_local_cockpit": 8788,
    "daimon_gemini_bridge": 8795,
}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def load_local_port_routing_registry(ion_root: str | Path = ".") -> dict[str, Any]:
    root = Path(ion_root).resolve()
    path = root / REGISTRY_RELATIVE_PATH
    if not path.exists():
        return {
            "schema_id": "ion.local_port_routing_registry.missing.v1",
            "registry_present": False,
            "registry_path": REGISTRY_RELATIVE_PATH.as_posix(),
            "assignments": [],
        }
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["registry_present"] = True
    payload["registry_path"] = REGISTRY_RELATIVE_PATH.as_posix()
    return payload


def build_local_port_routing_truth(ion_root: str | Path = ".") -> dict[str, Any]:
    registry = load_local_port_routing_registry(ion_root)
    assignments = list(registry.get("assignments") or [])
    by_service = {str(row.get("service_id")): row for row in assignments if row.get("service_id")}
    by_port: dict[int, list[str]] = defaultdict(list)
    findings: list[str] = []

    for row in assignments:
        port = row.get("local_port")
        service_id = row.get("service_id")
        if isinstance(port, int) and service_id:
            by_port[port].append(str(service_id))

    for service_id, expected_port in EXPECTED_CANONICAL_PORTS.items():
        row = by_service.get(service_id)
        if row is None:
            findings.append(f"missing_assignment:{service_id}")
            continue
        if row.get("local_port") != expected_port:
            findings.append(f"wrong_port:{service_id}:expected_{expected_port}:actual_{row.get('local_port')}")

    for port, services in sorted(by_port.items()):
        if len(services) > 1:
            findings.append(f"duplicate_port_assignment:{port}:{','.join(sorted(services))}")

    return {
        "schema_id": SCHEMA_ID,
        "generated_at": utc_now(),
        "verdict": READY_VERDICT,
        "status": "ready" if not findings and registry.get("registry_present") else "degraded",
        "registry_present": bool(registry.get("registry_present")),
        "registry_path": registry.get("registry_path", REGISTRY_RELATIVE_PATH.as_posix()),
        "active_packet": registry.get("active_packet"),
        "canonical_ports": {
            service_id: by_service.get(service_id, {}).get("local_port") for service_id in sorted(EXPECTED_CANONICAL_PORTS)
        },
        "assignments": assignments,
        "known_collision": registry.get("known_collision"),
        "migration_plan": registry.get("migration_plan"),
        "findings": findings,
        "production_authority": False,
        "deployment_authority": False,
        "live_execution_authority": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Project read-only local port routing truth.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    result = build_local_port_routing_truth(args.ion_root)
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(result["status"])
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
