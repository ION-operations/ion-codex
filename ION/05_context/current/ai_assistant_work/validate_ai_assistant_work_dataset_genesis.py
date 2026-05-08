"""Validate AI Assistant Work dataset genesis candidate.

This is current-context candidate validation only. It proves internal consistency of
dataset-genesis artifacts; it does not accept them into ION canon.
"""
from __future__ import annotations

import glob
import json
from collections import Counter
from datetime import datetime, UTC
from pathlib import Path
import sys

for _p in [
    str(Path.home() / ".local" / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"),
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
SIM_LATEST = AIW / "simulations/AI_ASSISTANT_WORK_DATASET_ROUTE_SIMULATION_REPORT_LATEST.json"
OUT_DIR = AIW / "validation"
REQUIRED_EMBODIMENTS = {"chat", "ide", "cli", "cloud_agent", "pr_agent", "background_agent", "hybrid"}


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def latest_summary_path() -> Path:
    candidates = sorted((AIW / "dataset").glob("AI_ASSISTANT_WORK_DATASET_GENESIS_SUMMARY_*.json"))
    if not candidates:
        raise FileNotFoundError("missing dataset genesis summary")
    return candidates[-1]


def load_dataset():
    return [json.loads(line) for line in DATASET.read_text(encoding="utf-8").splitlines() if line.strip()]


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    findings = []

    domain_ids = {d["domain_id"] for d in load_yaml(REG / "AI_ASSISTANT_WORK_DOMAIN_REGISTRY_CANDIDATE_V0_1.yaml")["domains"]}
    agent_ids = {a["role_id"] for a in load_yaml(REG / "AI_ASSISTANT_WORK_AGENT_REGISTRY_CANDIDATE_V0_1.yaml")["agents"]}
    failure_reg = load_yaml(REG / "AI_ASSISTANT_WORK_FAILURE_MODE_REGISTRY_CANDIDATE_V0_1.yaml")
    skill_map = load_yaml(REG / "AI_ASSISTANT_WORK_SKILL_TO_AGENT_BINDING_MAP_V0_1.yaml")
    gap_analysis = load_yaml(AIW / "gaps/AI_ASSISTANT_WORK_DATASET_GAP_ANALYSIS_V0_1.yaml")
    simulation = load_json(SIM_LATEST)
    summary = load_json(latest_summary_path())

    entries = load_dataset()
    embodiment_counts = Counter(item["assistant_embodiment"] for item in entries)
    domain_coverage = {d for item in entries for d in item["domains_involved"]}
    agent_coverage = {a for item in entries for a in item["specialist_agents_required"]}

    if len(entries) < 25:
        findings.append({"kind": "entry_count_below_minimum", "count": len(entries)})
    missing_embodiments = sorted(REQUIRED_EMBODIMENTS - set(embodiment_counts))
    if missing_embodiments:
        findings.append({"kind": "missing_embodiments", "items": missing_embodiments})
    if missing_domains := sorted(domain_ids - domain_coverage):
        findings.append({"kind": "missing_domain_coverage", "items": missing_domains})
    if missing_agents := sorted(agent_ids - agent_coverage):
        findings.append({"kind": "missing_agent_coverage", "items": missing_agents})
    if failure_reg.get("failure_mode_count", 0) < 10:
        findings.append({"kind": "failure_mode_count_low", "count": failure_reg.get("failure_mode_count")})
    if skill_map.get("binding_count", 0) < 10:
        findings.append({"kind": "skill_binding_count_low", "count": skill_map.get("binding_count")})
    if gap_analysis.get("template_gap_count", 0) < 10:
        findings.append({"kind": "template_gap_count_low", "count": gap_analysis.get("template_gap_count")})
    if gap_analysis.get("agent_domain_gap_count", 0) < 10:
        findings.append({"kind": "agent_domain_gap_count_low", "count": gap_analysis.get("agent_domain_gap_count")})
    if not simulation.get("accepted"):
        findings.append({"kind": "route_simulation_not_accepted", "status": simulation.get("status")})
    if simulation.get("case_count") != len(entries):
        findings.append({"kind": "route_simulation_case_count_mismatch", "simulation": simulation.get("case_count"), "entries": len(entries)})
    for artifact_name, artifact in [
        ("failure_registry", failure_reg),
        ("skill_map", skill_map),
        ("gap_analysis", gap_analysis),
    ]:
        status = artifact.get("status", "")
        if "candidate" not in status:
            findings.append({"kind": "artifact_not_candidate_status", "artifact": artifact_name, "status": status})
        auth = artifact.get("authority_boundary", {})
        if auth and auth.get("mutates_ION_03_registry"):
            findings.append({"kind": "artifact_claims_registry_mutation", "artifact": artifact_name})

    report = {
        "schema": "ion.ai_assistant_work.dataset_genesis_validation_report.v0_1",
        "accepted": not findings,
        "status": "accepted_candidate_evidence" if not findings else "candidate_evidence_with_findings",
        "created_at": datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "dataset_entry_count": len(entries),
        "embodiment_counts": dict(sorted(embodiment_counts.items())),
        "domain_coverage_count": len(domain_coverage),
        "agent_coverage_count": len(agent_coverage),
        "failure_mode_count": failure_reg.get("failure_mode_count"),
        "skill_binding_count": skill_map.get("binding_count"),
        "template_gap_count": gap_analysis.get("template_gap_count"),
        "agent_domain_gap_count": gap_analysis.get("agent_domain_gap_count"),
        "route_simulation": {
            "accepted": simulation.get("accepted"),
            "case_count": simulation.get("case_count"),
            "cases_accepted": simulation.get("cases_accepted"),
        },
        "summary_path": str(latest_summary_path().relative_to(ROOT)),
        "findings": findings,
        "non_claims": [
            "Dataset validation is candidate evidence only.",
            "It does not promote observations into accepted ION canon.",
            "It does not mutate ION/03_registry, product-front-door law, IDE state, GitHub, MCP, Codex, or any external system."
        ],
    }

    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    stamped = OUT_DIR / f"AI_ASSISTANT_WORK_DATASET_GENESIS_VALIDATION_NOTE_{stamp}.json"
    latest = OUT_DIR / "AI_ASSISTANT_WORK_DATASET_GENESIS_VALIDATION_NOTE_LATEST.json"
    for path in [stamped, latest]:
        path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
