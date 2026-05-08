"""Validate AI Assistant Work candidate v0.1 artifacts."""
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
DOMAINS = AIW / "domains"

REQUIRED_DOMAINS = {
    "ai_assistant_identity_embodiment",
    "chat_work_domain",
    "ide_work_domain",
    "codebase_understanding_domain",
    "planning_and_task_breakdown_domain",
    "implementation_domain",
    "ui_ux_domain",
    "documentation_writing_domain",
    "testing_quality_domain",
    "review_security_domain",
    "debugging_observability_domain",
    "devops_release_domain",
    "data_analysis_domain",
    "product_requirements_domain",
    "knowledge_context_memory_domain",
    "dependency_package_domain",
    "workflow_automation_tool_domain",
    "assistant_learning_dataset_domain",
    "cross_domain_settlement_domain",
}

REQUIRED_AGENTS = {
    "UI_ARCHITECT",
    "COMPONENT_BUILDER",
    "ACCESSIBILITY_AUDITOR",
    "DOCS_ARCHITECT",
    "TECHNICAL_WRITER",
    "API_DOCS_SCRIBE",
    "IDE_CARTOGRAPHER",
    "CODEBASE_CARTOGRAPHER",
    "TASK_PLANNER",
    "PATCH_MASON",
    "TEST_RUNNER",
    "SECURITY_NEMESIS",
    "WORK_PATTERN_ETHNOGRAPHER",
    "STATE_TAXONOMIST",
    "TEMPLATE_MINER",
    "SETTLEMENT_STEWARD",
}


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def main() -> int:
    findings = []

    domain_reg = load_yaml(REG / "AI_ASSISTANT_WORK_DOMAIN_REGISTRY_CANDIDATE_V0_1.yaml")
    agent_reg = load_yaml(REG / "AI_ASSISTANT_WORK_AGENT_REGISTRY_CANDIDATE_V0_1.yaml")
    route_reg = load_yaml(REG / "AI_ASSISTANT_WORK_ROUTE_REGISTRY_CANDIDATE_V0_1.yaml")
    state_reg = load_yaml(REG / "AI_ASSISTANT_WORK_STATE_REGISTRY_CANDIDATE_V0_1.yaml")
    template_reg = load_yaml(REG / "AI_ASSISTANT_WORK_TEMPLATE_REGISTRY_CANDIDATE_V0_1.yaml")
    protocol_reg = load_yaml(REG / "AI_ASSISTANT_WORK_PROTOCOL_REGISTRY_CANDIDATE_V0_1.yaml")
    dataset_schema = load_yaml(REG / "AI_ASSISTANT_WORK_DATASET_ENTRY_SCHEMA_V0_1.yaml")

    domain_ids = {d["domain_id"] for d in domain_reg["domains"]}
    agent_ids = {a["role_id"] for a in agent_reg["agents"]}

    missing_domains = sorted(REQUIRED_DOMAINS - domain_ids)
    missing_agents = sorted(REQUIRED_AGENTS - agent_ids)
    if missing_domains:
        findings.append({"kind": "missing_domains", "items": missing_domains})
    if missing_agents:
        findings.append({"kind": "missing_agents", "items": missing_agents})

    for domain_id in REQUIRED_DOMAINS:
        packet = DOMAINS / f"{domain_id}.domain_packet.yaml"
        if not packet.exists():
            findings.append({"kind": "missing_domain_packet", "item": domain_id})
            continue
        data = load_yaml(packet)
        if data.get("status") != "seed_candidate":
            findings.append({"kind": "bad_domain_packet_status", "item": domain_id})
        if not data.get("specialist_agents"):
            findings.append({"kind": "domain_without_agents", "item": domain_id})
        if not data.get("state_families"):
            findings.append({"kind": "domain_without_state_families", "item": domain_id})
        if not data.get("template_families"):
            findings.append({"kind": "domain_without_template_families", "item": domain_id})

    required_routes = {
        "route.assistant_identity_definition",
        "route.ide_agent_work_map",
        "route.ui_specialist_work",
        "route.documentation_specialist_work",
        "route.assistant_work_dataset_build",
        "route.cross_domain_feature_delivery",
    }
    route_ids = {r["route_id"] for r in route_reg["routes"]}
    if missing_routes := sorted(required_routes - route_ids):
        findings.append({"kind": "missing_routes", "items": missing_routes})

    for route in route_reg["routes"]:
        for domain_id in route.get("required_domains", []):
            if domain_id not in domain_ids:
                findings.append({"kind": "route_missing_domain", "route": route["route_id"], "domain": domain_id})
        for role_id in route.get("primary_agents", []):
            if role_id not in agent_ids:
                findings.append({"kind": "route_missing_agent", "route": route["route_id"], "agent": role_id})

    authority = domain_reg.get("authority_boundary", {})
    if not authority.get("candidate_only"):
        findings.append({"kind": "authority_boundary_not_candidate_only"})
    if authority.get("mutates_ION_03_registry"):
        findings.append({"kind": "authority_boundary_allows_registry_mutation"})

    if state_reg.get("state_family_count", 0) < 30:
        findings.append({"kind": "state_family_count_low", "count": state_reg.get("state_family_count")})
    if template_reg.get("template_family_count", 0) < 30:
        findings.append({"kind": "template_family_count_low", "count": template_reg.get("template_family_count")})
    if protocol_reg.get("protocol_count", 0) < 30:
        findings.append({"kind": "protocol_count_low", "count": protocol_reg.get("protocol_count")})

    required_dataset_fields = {"assistant_embodiment", "domains_involved", "state_surfaces", "templates_required", "specialist_agents_required", "settlement_path"}
    if not required_dataset_fields <= set(dataset_schema.get("required_fields", {}).keys()):
        findings.append({"kind": "dataset_schema_missing_required_fields"})

    result = {
        "schema": "ion.ai_assistant_work.validation_report.v0_1",
        "accepted": not findings,
        "status": "accepted_candidate_evidence" if not findings else "candidate_evidence_with_findings",
        "domain_count": len(domain_ids),
        "agent_count": len(agent_ids),
        "route_count": len(route_ids),
        "state_family_count": state_reg.get("state_family_count"),
        "template_family_count": template_reg.get("template_family_count"),
        "protocol_count": protocol_reg.get("protocol_count"),
        "findings": findings,
        "non_claims": [
            "Candidate validation does not accept this into ION canon.",
            "No external IDE or cloud-agent execution is claimed.",
            "No product-front-door or registry mutation is claimed."
        ],
    }
    out = AIW / "AI_ASSISTANT_WORK_VALIDATION_NOTE_20260508T143500Z.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    return 0 if result["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
