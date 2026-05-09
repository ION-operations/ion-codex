#!/usr/bin/env python3
"""Simulate ION self-knowledge onboarding route interception.

This is a sandbox-local candidate validation. It does not mutate active carrier
onboarding, does not land ION/03_registry/self_knowledge, and does not claim an
external Codex/MCP/daemon invocation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


CARRIER_CASES = [
    {
        "carrier_case_id": "gpt_sandbox_identity",
        "carrier_profile": "ION/03_registry/gpt_sandbox_carrier_profile.yaml",
        "active_onboarding_packet": "ION/05_context/current/ACTIVE_CARRIER_ONBOARDING_PACKET.json",
        "operator_task": "What is ION?",
        "task_class": "ion_identity_question",
        "expected_ion_about_ion": True,
        "expected_route_id": "route.ion_identity_answer",
    },
    {
        "carrier_case_id": "gpt_sandbox_authority_donor_boundary",
        "carrier_profile": "ION/03_registry/gpt_sandbox_carrier_profile.yaml",
        "active_onboarding_packet": "ION/05_context/current/ACTIVE_CARRIER_ONBOARDING_PACKET.json",
        "operator_task": "Which ION source is authoritative if a donor archive conflicts with current law?",
        "task_class": "ion_authority_question",
        "expected_ion_about_ion": True,
        "expected_route_id": "route.ion_authority_classification",
    },
    {
        "carrier_case_id": "gpt_sandbox_product_boundary",
        "carrier_profile": "ION/03_registry/gpt_sandbox_carrier_profile.yaml",
        "active_onboarding_packet": "ION/05_context/current/ACTIVE_CARRIER_ONBOARDING_PACKET.json",
        "operator_task": "Is the Custom GPT package a reduced ION or full ION in a sandbox body?",
        "task_class": "ion_package_or_gpt_sandbox_question",
        "expected_ion_about_ion": True,
        "expected_route_id": "route.gpt_sandbox_adaptation",
    },
    {
        "carrier_case_id": "codex_cli_full_runtime",
        "carrier_profile": "ION/03_registry/codex_cli_carrier_profile.yaml",
        "active_onboarding_packet": "ION/05_context/current/ACTIVE_CARRIER_ONBOARDING_PACKET.codex_cli.json",
        "operator_task": "Explain full local ION with Codex CLI isolated invocations.",
        "task_class": "ion_runtime_question",
        "expected_ion_about_ion": True,
        "expected_route_id": "route.full_local_codex_api_ion",
    },
    {
        "carrier_case_id": "codex_cli_context_template_receipt",
        "carrier_profile": "ION/03_registry/codex_cli_carrier_profile.yaml",
        "active_onboarding_packet": "ION/05_context/current/ACTIVE_CARRIER_ONBOARDING_PACKET.codex_cli.json",
        "operator_task": "How do context package, template law, proof gate, work packet, and receipt relate in ION?",
        "task_class": "ion_workpacket_or_context_question",
        "expected_ion_about_ion": True,
        "expected_route_id": "route.context_template_receipt",
    },
    {
        "carrier_case_id": "codex_cli_self_knowledge_continue",
        "carrier_profile": "ION/03_registry/codex_cli_carrier_profile.yaml",
        "active_onboarding_packet": "ION/05_context/current/ACTIVE_CARRIER_ONBOARDING_PACKET.codex_cli.json",
        "operator_task": "Continue building ION about ION self knowledge domain state.",
        "task_class": "ion_self_knowledge_implementation_question",
        "expected_ion_about_ion": True,
        "expected_route_id": "route.self_knowledge_implementation",
    },
    {
        "carrier_case_id": "gpt_sandbox_recovery_anti_regression",
        "carrier_profile": "ION/03_registry/gpt_sandbox_carrier_profile.yaml",
        "active_onboarding_packet": "ION/05_context/current/ACTIVE_CARRIER_ONBOARDING_PACKET.json",
        "operator_task": "How should ION prevent repeated failure, stale resurfacing, and hallucinated replacement during recovery?",
        "task_class": "ion_recovery_or_anti_regression_question",
        "expected_ion_about_ion": True,
        "expected_route_id": "route.ion_recovery_anti_regression",
    },
    {
        "carrier_case_id": "gpt_sandbox_non_ion_bypass",
        "carrier_profile": "ION/03_registry/gpt_sandbox_carrier_profile.yaml",
        "active_onboarding_packet": "ION/05_context/current/ACTIVE_CARRIER_ONBOARDING_PACKET.json",
        "operator_task": "Draft a short project update email for a teammate.",
        "task_class": "ordinary_user_writing_request",
        "expected_ion_about_ion": False,
        "expected_route_id": None,
    },
]

ION_TASK_CLASS_PREFIXES = (
    "ion_",
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def find_route(routes: list[dict[str, Any]], query: str) -> dict[str, Any] | None:
    q = query.casefold()
    scored: list[tuple[int, dict[str, Any]]] = []
    for route in routes:
        score = 0
        for pattern in route.get("trigger_patterns", []):
            p = str(pattern).casefold()
            if p and p in q:
                score = max(score, len(p))
        if score:
            scored.append((score, route))
    if not scored:
        return None
    scored.sort(key=lambda item: item[0], reverse=True)
    return scored[0][1]


def classify_task(case: dict[str, Any]) -> bool:
    return str(case["task_class"]).startswith(ION_TASK_CLASS_PREFIXES)


def trace_step(action: str, path: str | None = None, status: str = "ok", note: str | None = None) -> dict[str, Any]:
    out: dict[str, Any] = {"action": action, "status": status}
    if path is not None:
        out["path"] = path
    if note is not None:
        out["note"] = note
    return out


def step_index(trace: list[dict[str, Any]], action: str) -> int | None:
    for index, step in enumerate(trace):
        if step.get("action") == action:
            return index
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".", help="Repo shell root")
    parser.add_argument("--out", required=True, help="Report JSON path")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    sk = root / "ION/05_context/current/self_knowledge"
    promo = sk / "promotion_candidate"

    required_paths = {
        "repo_authority": root / "ION/REPO_AUTHORITY.md",
        "mount_contract": root / "ION/02_architecture/ION_MOUNT_CONTRACT.md",
        "self_knowledge_mount_packet": root / "ION/05_context/current/ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET.md",
        "route_registry_candidate": sk / "candidate_registries/route_registry.candidate.yaml",
        "domain_registry_candidate": sk / "candidate_registries/domain_registry.candidate.yaml",
        "onboarding_overlay": promo / "SELF_KNOWLEDGE_ONBOARDING_WIRING_OVERLAY_V0_2.json",
        "onboarding_proposal": promo / "ONBOARDING_WIRING_PROPOSAL_V0_3.md",
    }

    missing_required = [name for name, path in required_paths.items() if not path.exists()]
    if missing_required:
        report = {
            "schema_id": "ion.self_knowledge.onboarding_wiring_simulation_report.v0_2",
            "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "status": "failed_candidate_evidence",
            "accepted": False,
            "findings": [f"missing_required:{name}" for name in missing_required],
        }
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
        print(json.dumps({"accepted": False, "findings": report["findings"], "out": str(out)}, indent=2))
        return 1

    route_registry = load_yaml(required_paths["route_registry_candidate"])
    domain_registry = load_yaml(required_paths["domain_registry_candidate"])
    routes = route_registry["routes"]
    domain_packets: dict[str, dict[str, Any]] = {}
    for path in sorted((sk / "domains").glob("*.domain_packet.yaml")):
        data = load_yaml(path)
        domain_packets[data["domain_id"]] = data

    cases_out: list[dict[str, Any]] = []
    findings: list[str] = []
    carriers_exercised: set[str] = set()
    matched_routes: set[str] = set()
    loaded_domain_union: set[str] = set()

    for case in CARRIER_CASES:
        trace: list[dict[str, Any]] = []
        case_findings: list[str] = []

        profile_path = root / case["carrier_profile"]
        onboarding_path = root / case["active_onboarding_packet"]

        trace.append(trace_step("confirm_shell_root", ".", "ok" if (root / "pyproject.toml").exists() else "missing"))
        trace.append(trace_step("read_repo_authority", "ION/REPO_AUTHORITY.md"))
        trace.append(trace_step("read_mount_contract", "ION/02_architecture/ION_MOUNT_CONTRACT.md"))

        if not profile_path.exists():
            case_findings.append("missing_carrier_profile")
            trace.append(trace_step("read_carrier_profile", case["carrier_profile"], "missing"))
            profile = {}
        else:
            trace.append(trace_step("read_carrier_profile", case["carrier_profile"]))
            profile = load_yaml(profile_path)
            carriers_exercised.add(profile.get("carrier_id", profile_path.stem))

        if not onboarding_path.exists():
            case_findings.append("missing_active_onboarding_packet")
            trace.append(trace_step("read_active_onboarding_packet", case["active_onboarding_packet"], "missing"))
            onboarding_packet = {}
        else:
            trace.append(trace_step("read_active_onboarding_packet", case["active_onboarding_packet"]))
            onboarding_packet = load_json(onboarding_path)

        ion_about_ion = classify_task(case)
        if ion_about_ion != case["expected_ion_about_ion"]:
            case_findings.append("task_classification_mismatch")
        trace.append(trace_step("classify_operator_task", note=f"task_class={case['task_class']} ion_about_ion={ion_about_ion}"))

        matched_route = None
        loaded_domains: list[str] = []

        if ion_about_ion:
            trace.append(trace_step("mount_active_self_knowledge_mount_packet", "ION/05_context/current/ACTIVE_ION_SELF_KNOWLEDGE_MOUNT_PACKET.md"))
            trace.append(trace_step("load_self_knowledge_route_registry", "ION/05_context/current/self_knowledge/candidate_registries/route_registry.candidate.yaml"))
            matched_route = find_route(routes, case["operator_task"])
            if matched_route is None:
                case_findings.append("no_self_knowledge_route_selected")
                trace.append(trace_step("select_self_knowledge_route", status="failed", note="no route matched"))
            else:
                trace.append(trace_step("select_self_knowledge_route", note=matched_route["route_id"]))
                matched_routes.add(matched_route["route_id"])
                if matched_route["route_id"] != case["expected_route_id"]:
                    case_findings.append(f"wrong_route:{matched_route['route_id']}")
                for domain_id in matched_route.get("required_domains", []):
                    if domain_id not in domain_packets:
                        case_findings.append(f"missing_domain_packet:{domain_id}")
                    else:
                        loaded_domains.append(domain_id)
                        loaded_domain_union.add(domain_id)
                trace.append(trace_step("load_required_domain_packets", "ION/05_context/current/self_knowledge/domains/", note=",".join(loaded_domains)))
            trace.append(trace_step("answer_or_act_with_non_claims", note="candidate route-shaped response only"))

            mount_i = step_index(trace, "mount_active_self_knowledge_mount_packet")
            route_i = step_index(trace, "load_self_knowledge_route_registry")
            answer_i = step_index(trace, "answer_or_act_with_non_claims")
            classify_i = step_index(trace, "classify_operator_task")
            if None in (classify_i, mount_i, route_i, answer_i):
                case_findings.append("missing_required_trace_step")
            elif not (classify_i < mount_i < route_i < answer_i):
                case_findings.append("bad_onboarding_order_for_ion_about_ion")
            if matched_route and not matched_route.get("anti_drift_required"):
                case_findings.append("selected_route_missing_anti_drift")
            if matched_route and not matched_route.get("output_contract", {}).get("forbid"):
                case_findings.append("selected_route_missing_forbidden_claims")
        else:
            trace.append(trace_step("skip_self_knowledge_route", note="non-ION task; use ordinary active packet/domain workflow"))
            trace.append(trace_step("continue_normal_active_packet_route", "ION/05_context/current/ACTIVE_WORK_PACKET.json"))
            if step_index(trace, "mount_active_self_knowledge_mount_packet") is not None:
                case_findings.append("non_ion_task_mounted_self_knowledge")
            if step_index(trace, "load_self_knowledge_route_registry") is not None:
                case_findings.append("non_ion_task_loaded_self_knowledge_route_registry")

        # Universal safety checks
        if case["expected_ion_about_ion"]:
            if step_index(trace, "answer_or_act_with_non_claims") is not None and step_index(trace, "mount_active_self_knowledge_mount_packet") is None:
                case_findings.append("answer_without_self_knowledge_mount")
        if onboarding_packet.get("production_authority") is True or profile.get("production_authority") is True:
            case_findings.append("unexpected_production_authority_true")
        if onboarding_packet.get("live_execution_authority") is True or profile.get("live_execution_authority") is True:
            case_findings.append("unexpected_live_execution_authority_true")

        accepted = not case_findings
        if not accepted:
            findings.extend(f"{case['carrier_case_id']}:{finding}" for finding in case_findings)

        cases_out.append({
            "carrier_case_id": case["carrier_case_id"],
            "carrier_id": profile.get("carrier_id", profile_path.stem) if profile else profile_path.stem,
            "carrier_profile": case["carrier_profile"],
            "active_onboarding_packet": case["active_onboarding_packet"],
            "operator_task": case["operator_task"],
            "task_class": case["task_class"],
            "expected_ion_about_ion": case["expected_ion_about_ion"],
            "classified_ion_about_ion": ion_about_ion,
            "expected_route_id": case["expected_route_id"],
            "matched_route_id": matched_route["route_id"] if matched_route else None,
            "loaded_domains": loaded_domains,
            "trace": trace,
            "accepted": accepted,
            "findings": case_findings,
        })

    ion_cases = [case for case in cases_out if case["expected_ion_about_ion"]]
    non_ion_cases = [case for case in cases_out if not case["expected_ion_about_ion"]]
    if not ion_cases:
        findings.append("no_ion_about_ion_cases_exercised")
    if not non_ion_cases:
        findings.append("no_non_ion_bypass_case_exercised")

    if len(carriers_exercised) < 2:
        findings.append("less_than_two_carriers_exercised")

    # Ensure all ION-about-ION cases answered only after self-knowledge mount.
    for case in ion_cases:
        trace = case["trace"]
        mount_i = step_index(trace, "mount_active_self_knowledge_mount_packet")
        answer_i = step_index(trace, "answer_or_act_with_non_claims")
        if mount_i is None or answer_i is None or not mount_i < answer_i:
            findings.append(f"{case['carrier_case_id']}:mount_not_before_answer")

    # Ensure bypass case did not over-route.
    for case in non_ion_cases:
        actions = {step["action"] for step in case["trace"]}
        if "mount_active_self_knowledge_mount_packet" in actions or "load_self_knowledge_route_registry" in actions:
            findings.append(f"{case['carrier_case_id']}:non_ion_overrouted")

    inputs = {}
    for key, path in required_paths.items():
        inputs[key] = {
            "path": str(path.relative_to(root)),
            "sha256": sha256_file(path),
            "exists": path.exists(),
        }

    report = {
        "schema_id": "ion.self_knowledge.onboarding_wiring_simulation_report.v0_2",
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "+00:00"),
        "status": "accepted_candidate_evidence" if not findings else "failed_candidate_evidence",
        "accepted": not findings,
        "simulation_mode": "sandbox_local_onboarding_trace_not_external_codex",
        "root": str(root),
        "inputs": inputs,
        "coverage": {
            "carrier_cases": len(CARRIER_CASES),
            "cases_accepted": sum(1 for case in cases_out if case["accepted"]),
            "ion_about_ion_cases": len(ion_cases),
            "non_ion_bypass_cases": len(non_ion_cases),
            "carriers_exercised": sorted(carriers_exercised),
            "matched_routes": sorted(matched_routes),
            "loaded_domain_count": len(loaded_domain_union),
            "loaded_domain_union": sorted(loaded_domain_union),
        },
        "cases": cases_out,
        "findings": findings,
        "acceptance_criterion_11": {
            "criterion": "future carriers select self-knowledge route before answering ION-about-ION questions",
            "status": "ready_candidate" if not findings else "failed",
            "evidence": "sandbox-local onboarding trace simulation across GPT sandbox and Codex CLI carrier surfaces; external carrier invocation not claimed",
        },
        "authority_boundary": {
            "candidate_only": True,
            "production_authority": False,
            "live_execution_authority": False,
            "mutated_active_onboarding_packets": False,
            "mutated_ION_03_registry": False,
        },
        "non_claims": [
            "This simulation does not mutate active onboarding packets.",
            "This simulation does not accept or land ION/03_registry/self_knowledge.",
            "This simulation is not an external Codex/MCP/daemon invocation.",
            "Trace-shaped answer/action steps are candidate evidence, not canon."
        ],
    }

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({
        "accepted": report["accepted"],
        "status": report["status"],
        "carrier_cases": report["coverage"]["carrier_cases"],
        "cases_accepted": report["coverage"]["cases_accepted"],
        "ion_about_ion_cases": report["coverage"]["ion_about_ion_cases"],
        "non_ion_bypass_cases": report["coverage"]["non_ion_bypass_cases"],
        "carriers_exercised": report["coverage"]["carriers_exercised"],
        "matched_routes": report["coverage"]["matched_routes"],
        "out": str(out),
        "findings": findings,
    }, indent=2, sort_keys=True))
    return 0 if report["accepted"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
