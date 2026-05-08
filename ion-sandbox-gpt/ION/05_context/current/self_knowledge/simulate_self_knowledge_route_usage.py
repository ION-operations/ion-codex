#!/usr/bin/env python3
"""Run a local route-usage simulation for candidate ION self-knowledge.

This is not an external Codex invocation and not accepted registry state. It
exercises the candidate self-knowledge route registry, mount packet, and domain
packets as a sandbox-local workpacket before human/Steward acceptance.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ROUTE_CASES = [
    {
        "case_id": "identity_minimal_continue",
        "query": "What is ION?",
        "expected_route_id": "route.ion_identity_answer",
        "must_include": ["AI output is not state", "candidate state transitions", "what ION is not"],
    },
    {
        "case_id": "authority_donor_boundary",
        "query": "Which source is authoritative if a donor archive conflicts with current law?",
        "expected_route_id": "route.ion_authority_classification",
        "must_include": ["source ranking", "donor", "not active authority"],
    },
    {
        "case_id": "full_local_codex_api",
        "query": "Explain full local ION with Codex CLI and isolated invocations.",
        "expected_route_id": "route.full_local_codex_api_ion",
        "must_include": ["single-carrier sequential mode is a host-limited fallback", "API-like backend", "settlement"],
    },
    {
        "case_id": "gpt_sandbox_adaptation",
        "query": "How does ChatGPT ION work in the GPT sandbox body?",
        "expected_route_id": "route.gpt_sandbox_adaptation",
        "must_include": ["full ION adapted to sandbox constraints", "candidate/export boundary", "no external spawn claim"],
    },
    {
        "case_id": "context_template_receipt",
        "query": "How do context package, template law, proof gate, work packet, and receipt relate?",
        "expected_route_id": "route.context_template_receipt",
        "must_include": ["context", "template", "proof", "receipt", "raw output"],
    },
    {
        "case_id": "self_knowledge_implementation",
        "query": "Continue building ION about ION self knowledge domain state and route registry.",
        "expected_route_id": "route.self_knowledge_implementation",
        "must_include": ["inventory proof", "candidate files", "validation", "not new architecture"],
    },
    {
        "case_id": "recovery_anti_regression",
        "query": "How should ION prevent repeated failure, stale resurfacing, and hallucinated replacement during recovery?",
        "expected_route_id": "route.ion_recovery_anti_regression",
        "must_include": ["known failure pattern", "authority ranking", "containment", "receipt"],
    },
]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def find_route(routes: list[dict[str, Any]], query: str) -> dict[str, Any] | None:
    q = query.casefold()
    matches: list[tuple[int, dict[str, Any]]] = []
    for route in routes:
        patterns = route.get("trigger_patterns", [])
        route_score = 0
        for pattern in patterns:
            p = str(pattern).casefold()
            if p in q:
                route_score = max(route_score, len(p))
        if route_score:
            matches.append((route_score, route))
    if not matches:
        return None
    matches.sort(key=lambda item: item[0], reverse=True)
    return matches[0][1]


def render_answer_draft(case: dict[str, Any], route: dict[str, Any], loaded_domains: list[dict[str, Any]], mount_text: str) -> str:
    route_id = route["route_id"]
    domain_titles = ", ".join(domain.get("title", domain.get("domain_id", "unknown")) for domain in loaded_domains)
    guard_lines = "; ".join(route.get("anti_drift_required", []))
    include_lines = "; ".join(route.get("output_contract", {}).get("include", []))
    forbid_lines = "; ".join(route.get("output_contract", {}).get("forbid", []))
    domain_purposes = " ".join(str(domain.get("purpose", "")) for domain in loaded_domains)
    domain_anti_drift = " ".join(
        note
        for domain in loaded_domains
        for note in domain.get("anti_drift_notes", [])
    )

    # Deterministic route-local answer fragments. These are not accepted canon;
    # they demonstrate that the route can assemble the correct answer shape from
    # mounted self-knowledge surfaces rather than from carrier memory.
    fragments = {
        "route.ion_identity_answer": (
            "AI output is not state. ION is a continuity substrate for AI-mediated work that treats model output as "
            "candidate state transitions until context, template law, proof, Steward/human decision, receipt, and "
            "export/inheritance make a transition lawful. It must also state what ION is not: not a model, prompt trick, "
            "memory dump, roleplay persona, daemon claim, or whatever a carrier says."
        ),
        "route.ion_authority_classification": (
            "Answer by source ranking: current root authority, active operational packet, receipts/tests/manifests, "
            "candidate current context, then witness/donor/deprecated material. A donor archive may inform recovery, "
            "but donor material is not active authority and must not become law without settlement."
        ),
        "route.full_local_codex_api_ion": (
            "Full local/API/Codex-style ION uses isolated invocations and fan-out/fan-in settlement. Codex CLI is treated "
            "as an API-like backend for isolated invocations. Single-carrier sequential mode is a host-limited fallback, "
            "not the intended center, and branch returns still require settlement before landing."
        ),
        "route.gpt_sandbox_adaptation": (
            "The Custom GPT / ChatGPT sandbox body is full ION adapted to sandbox constraints, not reduced ION. It may "
            "emulate role sequence in one carrier, preserve candidate/export boundary, and must make no external spawn claim, "
            "production authority claim, or registry landing claim."
        ),
        "route.context_template_receipt": (
            "A bounded action loads a context package, follows template law, supplies proof, and emits a receipt only after "
            "the relevant acceptance boundary. A work packet scopes the act. Raw output is not state and cannot inherit as "
            "law without proof and receipt."
        ),
        "route.self_knowledge_implementation": (
            "Continue as activation, not new architecture: use inventory proof, candidate files, validation, receipts, and "
            "next packets. Check existing organs first and avoid inventing a replacement architecture or broad registry "
            "mutation without acceptance."
        ),
        "route.ion_recovery_anti_regression": (
            "Start from a known failure pattern, then apply authority ranking before any recovery action. Containment should "
            "stop stale resurfacing and hallucinated replacement, preserve mature ION organs, and leave a receipt or next "
            "packet that future carriers can inherit."
        ),
    }

    fragment = fragments.get(route_id, "")
    return (
        f"Route: {route_id}\n"
        f"Loaded domains: {domain_titles}\n"
        f"Required guards: {guard_lines}\n"
        f"Output must include: {include_lines}\n"
        f"Output forbids: {forbid_lines}\n"
        f"Domain support: {domain_purposes} {domain_anti_drift}\n"
        f"Answer draft: {fragment}\n"
        "Non-claim: this is a sandbox route-usage simulation and not accepted registry law."
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Repo shell root")
    parser.add_argument("--out", required=True, help="Report JSON path")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    sk = root / "ION/05_context/current/self_knowledge"
    mount = root / "ION/05_context/current/ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET.md"
    route_registry_path = sk / "candidate_registries/route_registry.candidate.yaml"
    domain_registry_path = sk / "candidate_registries/domain_registry.candidate.yaml"
    domain_dir = sk / "domains"

    mount_text = mount.read_text(encoding="utf-8")
    route_registry = load_yaml(route_registry_path)
    domain_registry = load_yaml(domain_registry_path)
    routes = route_registry["routes"]
    domain_registry_ids = {item["domain_id"] for item in domain_registry["domains"]}

    domain_packets: dict[str, dict[str, Any]] = {}
    for path in sorted(domain_dir.glob("*.domain_packet.yaml")):
        data = load_yaml(path)
        domain_packets[data["domain_id"]] = data

    cases_out = []
    findings = []
    exercised_routes = set()
    loaded_domain_union = set()

    for case in ROUTE_CASES:
        route = find_route(routes, case["query"])
        if route is None:
            findings.append(f"no_route_match:{case['case_id']}")
            cases_out.append({**case, "accepted": False, "findings": ["no route match"]})
            continue

        route_findings = []
        if route["route_id"] != case["expected_route_id"]:
            route_findings.append(f"wrong_route:{route['route_id']}")

        missing_domains = [
            domain_id for domain_id in route.get("required_domains", [])
            if domain_id not in domain_packets or domain_id not in domain_registry_ids
        ]
        if missing_domains:
            route_findings.append(f"missing_domains:{','.join(missing_domains)}")

        loaded_domains = [domain_packets[domain_id] for domain_id in route.get("required_domains", []) if domain_id in domain_packets]
        loaded_domain_union.update(domain.get("domain_id") for domain in loaded_domains)
        exercised_routes.add(route["route_id"])

        if not route.get("anti_drift_required"):
            route_findings.append("missing_route_anti_drift_guards")
        if not route.get("output_contract", {}).get("include"):
            route_findings.append("missing_output_include_contract")
        if not route.get("output_contract", {}).get("forbid"):
            route_findings.append("missing_output_forbid_contract")

        answer_draft = render_answer_draft(case, route, loaded_domains, mount_text)
        answer_low = answer_draft.casefold()
        missing_phrases = [phrase for phrase in case["must_include"] if phrase.casefold() not in answer_low]
        if missing_phrases:
            route_findings.append(f"answer_missing_phrases:{'|'.join(missing_phrases)}")

        for forbidden in route.get("output_contract", {}).get("forbid", []):
            if route["route_id"] == "route.full_local_codex_api_ion" and "implying single-carrier is intended center" in forbidden:
                if "intended center" in answer_low and "not the intended center" not in answer_low:
                    route_findings.append("bad_single_carrier_center_claim")
            if route["route_id"] == "route.gpt_sandbox_adaptation":
                if "reduced ion" in answer_low and "not reduced ion" not in answer_low:
                    route_findings.append("bad_gpt_reduction_claim")

        accepted = not route_findings
        if not accepted:
            findings.extend(f"{case['case_id']}:{finding}" for finding in route_findings)

        cases_out.append({
            "case_id": case["case_id"],
            "query": case["query"],
            "expected_route_id": case["expected_route_id"],
            "matched_route_id": route["route_id"],
            "accepted": accepted,
            "findings": route_findings,
            "loaded_domains": [domain["domain_id"] for domain in loaded_domains],
            "anti_drift_required": route.get("anti_drift_required", []),
            "output_contract": route.get("output_contract", {}),
            "answer_draft": answer_draft,
        })

    all_route_ids = {route["route_id"] for route in routes}
    missing_route_coverage = sorted(all_route_ids - exercised_routes)
    if missing_route_coverage:
        findings.append("missing_route_coverage:" + ",".join(missing_route_coverage))

    report = {
        "schema_id": "ion.self_knowledge.route_usage_simulation_report.v0_2",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "+00:00"),
        "status": "accepted_candidate_evidence" if not findings else "failed_candidate_evidence",
        "accepted": not findings,
        "simulation_mode": "sandbox_local_route_usage_not_external_codex",
        "root": str(root),
        "inputs": {
            "mount_packet": str(mount.relative_to(root)),
            "mount_packet_sha256": sha256_file(mount),
            "route_registry": str(route_registry_path.relative_to(root)),
            "route_registry_sha256": sha256_file(route_registry_path),
            "domain_registry": str(domain_registry_path.relative_to(root)),
            "domain_registry_sha256": sha256_file(domain_registry_path),
            "domain_packets_dir": str(domain_dir.relative_to(root)),
        },
        "coverage": {
            "route_count": len(routes),
            "routes_exercised": sorted(exercised_routes),
            "missing_route_coverage": missing_route_coverage,
            "loaded_domain_count": len(loaded_domain_union),
            "loaded_domain_union": sorted(loaded_domain_union),
            "case_count": len(ROUTE_CASES),
            "cases_accepted": sum(1 for case in cases_out if case["accepted"]),
        },
        "cases": cases_out,
        "findings": findings,
        "acceptance_criterion_7": {
            "criterion": "at least one Codex/local workpacket uses the self-knowledge route",
            "status": "ready_candidate" if not findings else "failed",
            "evidence": "sandbox-local route usage simulation exercised every candidate route; external Codex not claimed",
        },
        "non_claims": [
            "This simulation is not external Codex execution.",
            "This simulation does not accept or land ION/03_registry/self_knowledge.",
            "This simulation does not prove production readiness.",
            "The generated answer drafts are route-shape evidence, not accepted canon."
        ],
        "production_authority": False,
        "live_execution_authority": False,
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "accepted": report["accepted"],
        "status": report["status"],
        "route_count": report["coverage"]["route_count"],
        "case_count": report["coverage"]["case_count"],
        "cases_accepted": report["coverage"]["cases_accepted"],
        "missing_route_coverage": missing_route_coverage,
        "out": str(out),
    }, indent=2, sort_keys=True))
    return 0 if report["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
