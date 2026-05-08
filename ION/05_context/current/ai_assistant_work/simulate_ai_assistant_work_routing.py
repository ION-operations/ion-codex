"""Sandbox-local route simulation for AI Assistant Work candidate v0.1.

This script validates route/domain/agent coverage. It does not claim external
IDE, Codex, GitHub, MCP, or production execution.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys

for _p in [
    "/opt/pyvenv/lib/python3.13/site-packages",
    "/opt/pyvenv/lib/python3.13/dist-packages",
    "/usr/local/lib/python3.13/dist-packages",
]:
    if _p not in sys.path:
        sys.path.insert(0, _p)

import yaml

ROOT = Path(__file__).resolve().parents[4]
AIW = ROOT / "ION/05_context/current/ai_assistant_work"
REG = AIW / "registries"


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> int:
    domain_reg = load_yaml(REG / "AI_ASSISTANT_WORK_DOMAIN_REGISTRY_CANDIDATE_V0_1.yaml")
    route_reg = load_yaml(REG / "AI_ASSISTANT_WORK_ROUTE_REGISTRY_CANDIDATE_V0_1.yaml")
    agent_reg = load_yaml(REG / "AI_ASSISTANT_WORK_AGENT_REGISTRY_CANDIDATE_V0_1.yaml")

    domain_ids = {d["domain_id"] for d in domain_reg["domains"]}
    agent_ids = {a["role_id"] for a in agent_reg["agents"]}
    cases = [
        {
            "case_id": "define_ai_assistant",
            "input": "What is an AI assistant in chat and IDE?",
            "expected_route": "route.assistant_identity_definition",
        },
        {
            "case_id": "map_ide_agent_work",
            "input": "Define the space of IDE agent work.",
            "expected_route": "route.ide_agent_work_map",
        },
        {
            "case_id": "make_ui",
            "input": "Make a UI for this feature.",
            "expected_route": "route.ui_specialist_work",
        },
        {
            "case_id": "write_docs",
            "input": "Write the docs for this API.",
            "expected_route": "route.documentation_specialist_work",
        },
        {
            "case_id": "build_dataset",
            "input": "Build the massive dataset of assistant work states and domains.",
            "expected_route": "route.assistant_work_dataset_build",
        },
        {
            "case_id": "ship_feature",
            "input": "Build and ship a full stack feature.",
            "expected_route": "route.cross_domain_feature_delivery",
        },
    ]

    route_by_id = {r["route_id"]: r for r in route_reg["routes"]}
    loaded_domains = set()
    used_agents = set()
    findings = []
    case_results = []
    for case in cases:
        route = route_by_id.get(case["expected_route"])
        if not route:
            findings.append(f"missing route {case['expected_route']}")
            accepted = False
            domains = []
            agents = []
        else:
            domains = route["required_domains"]
            agents = route["primary_agents"]
            missing_domains = [d for d in domains if d not in domain_ids]
            missing_agents = [a for a in agents if a not in agent_ids]
            accepted = not missing_domains and not missing_agents
            if missing_domains:
                findings.append(f"{case['case_id']} missing domains: {missing_domains}")
            if missing_agents:
                findings.append(f"{case['case_id']} missing agents: {missing_agents}")
            loaded_domains.update(domains)
            used_agents.update(agents)
        case_results.append({
            "case_id": case["case_id"],
            "input": case["input"],
            "selected_route": case["expected_route"],
            "required_domains": domains,
            "primary_agents": agents,
            "accepted": accepted,
        })

    report = {
        "schema": "ion.ai_assistant_work.route_simulation_report.v0_1",
        "status": "accepted_candidate_evidence" if not findings else "candidate_evidence_with_findings",
        "accepted": not findings,
        "simulation_mode": "sandbox_local_route_usage_not_external_ide_or_codex",
        "case_count": len(cases),
        "cases_accepted": sum(1 for c in case_results if c["accepted"]),
        "route_count": len(route_by_id),
        "domain_count": len(domain_ids),
        "agent_count": len(agent_ids),
        "loaded_domain_count": len(loaded_domains),
        "used_agent_count": len(used_agents),
        "missing_route_coverage": sorted(set(route_by_id) - {c["expected_route"] for c in cases}),
        "case_results": case_results,
        "findings": findings,
        "non_claims": [
            "No external IDE execution occurred.",
            "No accepted canon was modified.",
            "This simulation validates candidate route coverage only."
        ],
    }
    out = AIW / "simulations" / "AI_ASSISTANT_WORK_ROUTE_SIMULATION_REPORT_20260508T143500Z.json"
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if report["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
