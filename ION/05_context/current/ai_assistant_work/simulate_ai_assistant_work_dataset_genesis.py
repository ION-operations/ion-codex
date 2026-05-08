"""Simulate route usage across AI Assistant Work dataset genesis entries.

Sandbox-local candidate evidence only. This does not execute an IDE, CLI,
cloud agent, PR agent, daemon, or product-front-door mutation.
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from datetime import datetime, UTC
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
DATASET = AIW / "dataset/AI_ASSISTANT_WORK_DATASET_GENESIS_V0_1.jsonl"
OUT_DIR = AIW / "simulations"

REQUIRED_FIELDS = {
    "entry_id",
    "observed_at",
    "source_class",
    "assistant_embodiment",
    "user_intent",
    "work_pattern",
    "domains_involved",
    "state_surfaces",
    "tools_or_actions",
    "protocols_required",
    "templates_required",
    "specialist_agents_required",
    "proof_required",
    "failure_modes_observed",
    "settlement_path",
    "candidate_improvements",
    "authority_notes",
    "candidate_route",
}

REQUIRED_EMBODIMENTS = {
    "chat",
    "ide",
    "cli",
    "cloud_agent",
    "pr_agent",
    "background_agent",
    "hybrid",
}


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_dataset():
    entries = []
    with DATASET.open(encoding="utf-8") as fh:
        for line_no, line in enumerate(fh, start=1):
            if line.strip():
                item = json.loads(line)
                item["_line_no"] = line_no
                entries.append(item)
    return entries


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    domain_ids = {d["domain_id"] for d in load_yaml(REG / "AI_ASSISTANT_WORK_DOMAIN_REGISTRY_CANDIDATE_V0_1.yaml")["domains"]}
    agent_ids = {a["role_id"] for a in load_yaml(REG / "AI_ASSISTANT_WORK_AGENT_REGISTRY_CANDIDATE_V0_1.yaml")["agents"]}
    state_ids = {s["state_family_id"] for s in load_yaml(REG / "AI_ASSISTANT_WORK_STATE_REGISTRY_CANDIDATE_V0_1.yaml")["state_families"]}
    template_ids = {t["template_family_id"] for t in load_yaml(REG / "AI_ASSISTANT_WORK_TEMPLATE_REGISTRY_CANDIDATE_V0_1.yaml")["template_families"]}
    protocol_ids = {p["protocol_id"] for p in load_yaml(REG / "AI_ASSISTANT_WORK_PROTOCOL_REGISTRY_CANDIDATE_V0_1.yaml")["protocols"]}
    route_ids = {r["route_id"] for r in load_yaml(REG / "AI_ASSISTANT_WORK_ROUTE_REGISTRY_CANDIDATE_V0_1.yaml")["routes"]}
    failure_ids = {f["failure_mode_id"] for f in load_yaml(REG / "AI_ASSISTANT_WORK_FAILURE_MODE_REGISTRY_CANDIDATE_V0_1.yaml")["failure_modes"]}

    entries = load_dataset()
    findings = []
    cases = []

    for item in entries:
        entry_findings = []
        missing_fields = sorted(REQUIRED_FIELDS - set(item))
        if missing_fields:
            entry_findings.append({"kind": "missing_fields", "items": missing_fields})

        for key, valid in [
            ("domains_involved", domain_ids),
            ("state_surfaces", state_ids),
            ("protocols_required", protocol_ids),
            ("templates_required", template_ids),
            ("specialist_agents_required", agent_ids),
            ("failure_modes_observed", failure_ids),
        ]:
            missing = sorted(set(item.get(key, [])) - valid)
            if missing:
                entry_findings.append({"kind": f"unknown_{key}", "items": missing})

        route = item.get("candidate_route")
        if route not in route_ids:
            entry_findings.append({"kind": "unknown_candidate_route", "item": route})

        if not item.get("proof_required"):
            entry_findings.append({"kind": "missing_proof_required"})
        if item.get("settlement_path") not in {"none", "single_domain_receipt", "cross_domain_settlement", "human_gate", "external_approval"}:
            entry_findings.append({"kind": "bad_settlement_path", "item": item.get("settlement_path")})

        cases.append({
            "entry_id": item.get("entry_id"),
            "candidate_route": route,
            "accepted": not entry_findings,
            "findings": entry_findings,
        })
        findings.extend({"entry_id": item.get("entry_id"), **finding} for finding in entry_findings)

    embodiment_counts = Counter(item.get("assistant_embodiment") for item in entries)
    domain_coverage = sorted({d for item in entries for d in item.get("domains_involved", [])})
    agent_coverage = sorted({a for item in entries for a in item.get("specialist_agents_required", [])})
    template_coverage = sorted({t for item in entries for t in item.get("templates_required", [])})
    protocol_coverage = sorted({p for item in entries for p in item.get("protocols_required", [])})
    state_coverage = sorted({s for item in entries for s in item.get("state_surfaces", [])})

    if len(entries) < 25:
        findings.append({"kind": "entry_count_below_minimum", "count": len(entries)})
    missing_embeddings = sorted(REQUIRED_EMBODIMENTS - set(embodiment_counts))
    if missing_embeddings:
        findings.append({"kind": "missing_required_embodiments", "items": missing_embeddings})
    if set(domain_coverage) != domain_ids:
        findings.append({"kind": "domain_coverage_incomplete", "items": sorted(domain_ids - set(domain_coverage))})
    if set(agent_coverage) != agent_ids:
        findings.append({"kind": "agent_coverage_incomplete", "items": sorted(agent_ids - set(agent_coverage))})

    report = {
        "schema": "ion.ai_assistant_work.dataset_route_simulation_report.v0_1",
        "status": "accepted_candidate_evidence" if not findings else "candidate_evidence_with_findings",
        "accepted": not findings,
        "created_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "simulation_mode": "sandbox_local_dataset_route_usage_not_external_ide_cli_cloud_pr_or_daemon_execution",
        "dataset_path": "ION/05_context/current/ai_assistant_work/dataset/AI_ASSISTANT_WORK_DATASET_GENESIS_V0_1.jsonl",
        "case_count": len(cases),
        "cases_accepted": sum(1 for c in cases if c["accepted"]),
        "route_counts": dict(sorted(Counter(c["candidate_route"] for c in cases).items())),
        "embodiment_counts": dict(sorted(embodiment_counts.items())),
        "domain_coverage_count": len(domain_coverage),
        "agent_coverage_count": len(agent_coverage),
        "state_surface_coverage_count": len(state_coverage),
        "template_coverage_count": len(template_coverage),
        "protocol_coverage_count": len(protocol_coverage),
        "cases": cases,
        "findings": findings,
        "non_claims": [
            "No external IDE execution occurred.",
            "No external CLI, cloud-agent, PR-agent, daemon, GitHub, or MCP execution occurred.",
            "Dataset route simulation does not accept candidate entries into ION canon.",
            "No product-front-door or ION/03_registry mutation is claimed."
        ],
    }

    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    stamped = OUT_DIR / f"AI_ASSISTANT_WORK_DATASET_ROUTE_SIMULATION_REPORT_{stamp}.json"
    latest = OUT_DIR / "AI_ASSISTANT_WORK_DATASET_ROUTE_SIMULATION_REPORT_LATEST.json"
    for path in [stamped, latest]:
        path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
