"""Validate AI Assistant Work template instance corpus and agent boot exercises.

Candidate current-context validator only. It does not claim accepted template law,
real isolated agent execution, registry landing, product-front-door mutation, or
external tool execution.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

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
SPEC_DIR = AIW / "template_specs"
INSTANCE_DIR = AIW / "template_instances"
EXERCISE_DIR = AIW / "agent_boot_exercises"
BOOT_DIR = AIW / "agent_boots"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _stringify_items(value: Any) -> str:
    if isinstance(value, list):
        return " ".join(_stringify_items(v) for v in value)
    if isinstance(value, dict):
        return " ".join(f"{k} {_stringify_items(v)}" for k, v in value.items())
    return str(value)


def validate_sections(spec: dict[str, Any], instance: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    sections = instance.get("sections")
    if not isinstance(sections, dict):
        return [{"kind": "sections_not_object", "template_id": spec.get("template_id")}]

    for rule in spec.get("machine_required_sections", []):
        name = rule["name"]
        if name not in sections:
            findings.append({"kind": "missing_required_section", "section": name})
            continue

        value = sections[name]
        typ = rule["type"]
        if typ == "string":
            if not isinstance(value, str):
                findings.append({"kind": "section_type_error", "section": name, "expected": "string"})
            elif len(value) < int(rule.get("min_length", 0)):
                findings.append({"kind": "section_min_length_error", "section": name})
        elif typ == "integer":
            if not isinstance(value, int):
                findings.append({"kind": "section_type_error", "section": name, "expected": "integer"})
        elif typ == "enum":
            if value not in rule.get("allowed", []):
                findings.append({"kind": "enum_value_error", "section": name, "value": value})
        elif typ == "list":
            if not isinstance(value, list):
                findings.append({"kind": "section_type_error", "section": name, "expected": "list"})
            else:
                if len(value) < int(rule.get("min_items", 0)):
                    findings.append({"kind": "section_min_items_error", "section": name})
                required_keys = rule.get("item_required_keys", [])
                for idx, item in enumerate(value):
                    if required_keys:
                        if not isinstance(item, dict):
                            findings.append({"kind": "list_item_type_error", "section": name, "index": idx})
                            continue
                        missing = [k for k in required_keys if k not in item]
                        if missing:
                            findings.append({"kind": "list_item_missing_keys", "section": name, "index": idx, "missing": missing})
                include_any = rule.get("must_include_any", [])
                if include_any:
                    flattened = _stringify_items(value).lower()
                    if not any(token.lower() in flattened for token in include_any):
                        findings.append({"kind": "list_must_include_any_error", "section": name, "expected_any": include_any})
        elif typ == "object":
            if not isinstance(value, dict):
                findings.append({"kind": "section_type_error", "section": name, "expected": "object"})
            else:
                missing = [k for k in rule.get("required_keys", []) if k not in value]
                if missing:
                    findings.append({"kind": "object_missing_required_keys", "section": name, "missing": missing})
        else:
            findings.append({"kind": "unknown_section_rule_type", "section": name, "type": typ})

    # Candidate-boundary proof gate: at least one NON_CLAIMS item must preserve non-accepted boundary.
    nc = sections.get("NON_CLAIMS")
    if not isinstance(nc, list) or not nc:
        findings.append({"kind": "non_claims_missing_or_empty"})
    else:
        text = " ".join(str(v).lower() for v in nc)
        if "not accepted" not in text and "candidate" not in text and "not claimed" not in text:
            findings.append({"kind": "candidate_boundary_non_claim_absent"})

    # Settlement/receipt route: where present, cannot be blank.
    for route_key in ("SETTLEMENT_ROUTE", "RECEIPT_TARGET"):
        if route_key in sections:
            value = sections.get(route_key)
            if not isinstance(value, str) or len(value.strip()) < 5:
                findings.append({"kind": "route_or_receipt_target_invalid", "section": route_key})

    return findings


def validate_instance_file(path: Path, specs_by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    instance = load_json(path)
    tid = instance.get("template_id")
    spec = specs_by_id.get(tid)
    if spec is None:
        return {"path": str(path), "accepted": False, "findings": [{"kind": "unknown_template_id", "template_id": tid}]}

    findings = validate_sections(spec, instance)
    should_pass = bool(instance.get("expected_validation", {}).get("should_pass"))
    accepted = not findings if should_pass else bool(findings)
    return {
        "path": str(path.relative_to(ROOT)),
        "template_id": tid,
        "case_type": instance.get("case_type"),
        "should_pass": should_pass,
        "accepted": accepted,
        "finding_count": len(findings),
        "findings": findings[:20],
    }


def validate_agent_exercise(path: Path, specs_by_id: dict[str, dict[str, Any]], boots_by_role: dict[str, dict[str, Any]]) -> dict[str, Any]:
    exercise = load_json(path)
    findings: list[dict[str, Any]] = []
    role_id = exercise.get("role_id")
    tid = exercise.get("template_id")
    spec = specs_by_id.get(tid)
    boot = boots_by_role.get(role_id)

    if spec is None:
        findings.append({"kind": "unknown_template_id", "template_id": tid})
    if boot is None:
        findings.append({"kind": "unknown_role_id", "role_id": role_id})
    if spec and spec.get("primary_agent") != role_id:
        findings.append({"kind": "primary_agent_template_mismatch", "role_id": role_id, "template_id": tid})
    if boot and tid not in boot.get("owned_template_specs", []):
        findings.append({"kind": "template_not_owned_by_boot", "role_id": role_id, "template_id": tid})
    dispatch = exercise.get("dispatch_assertion", {})
    if dispatch.get("specialist_first") is not True or dispatch.get("generic_implementation_first") is not False:
        findings.append({"kind": "specialist_first_dispatch_not_preserved"})
    if dispatch.get("selected_agent") != role_id or dispatch.get("selected_template") != tid:
        findings.append({"kind": "dispatch_selection_mismatch"})
    for ref_key in ("valid_instance_ref", "rejection_case_ref"):
        ref = exercise.get(ref_key)
        if not ref or not (ROOT / ref).exists():
            findings.append({"kind": "missing_instance_ref", "ref_key": ref_key, "ref": ref})
    if exercise.get("authority_boundary", {}).get("candidate_only") is not True:
        findings.append({"kind": "candidate_boundary_missing"})
    nc_text = " ".join(exercise.get("non_claims", [])).lower()
    if "not" not in nc_text or "external" not in nc_text:
        findings.append({"kind": "exercise_non_claims_weak"})

    return {
        "path": str(path.relative_to(ROOT)),
        "role_id": role_id,
        "template_id": tid,
        "accepted": not findings,
        "finding_count": len(findings),
        "findings": findings[:20],
    }


def build_report() -> dict[str, Any]:
    specs_by_id = {
        load_yaml(path)["template_id"]: load_yaml(path)
        for path in sorted(SPEC_DIR.glob("*.template_spec.yaml"))
    }
    boots_by_role = {
        load_yaml(path)["role_id"]: load_yaml(path)
        for path in sorted(BOOT_DIR.glob("*.agent_boot.yaml"))
    }

    valid_results = [validate_instance_file(path, specs_by_id) for path in sorted(INSTANCE_DIR.glob("*.minimal_valid.instance.json"))]
    rejection_results = [validate_instance_file(path, specs_by_id) for path in sorted(INSTANCE_DIR.glob("*.expected_rejection.instance.json"))]
    exercise_results = [validate_agent_exercise(path, specs_by_id, boots_by_role) for path in sorted(EXERCISE_DIR.glob("*.boot_exercise.json"))]

    template_ids = set(specs_by_id)
    valid_ids = {r["template_id"] for r in valid_results}
    rejection_ids = {r["template_id"] for r in rejection_results}
    exercise_roles = {r["role_id"] for r in exercise_results}
    required_roles = {spec["primary_agent"] for spec in specs_by_id.values()}

    findings: list[dict[str, Any]] = []
    if valid_ids != template_ids:
        findings.append({"kind": "valid_instance_template_coverage_mismatch", "missing": sorted(template_ids - valid_ids)})
    if rejection_ids != template_ids:
        findings.append({"kind": "rejection_instance_template_coverage_mismatch", "missing": sorted(template_ids - rejection_ids)})
    if exercise_roles != required_roles:
        findings.append({"kind": "agent_exercise_role_coverage_mismatch", "missing": sorted(required_roles - exercise_roles)})

    for group, results in [("valid_instances", valid_results), ("rejection_cases", rejection_results), ("agent_exercises", exercise_results)]:
        failed = [r for r in results if not r["accepted"]]
        if failed:
            findings.append({"kind": f"{group}_not_accepted_by_validator", "count": len(failed), "items": failed[:10]})

    report = {
        "schema": "ion.ai_assistant_work.template_instance_agent_boot_exercise_validation_report.v0_1",
        "status": "accepted_candidate_validation" if not findings else "validation_findings_present",
        "candidate_only": True,
        "template_spec_count": len(specs_by_id),
        "valid_instance_count": len(valid_results),
        "expected_rejection_count": len(rejection_results),
        "agent_boot_exercise_count": len(exercise_results),
        "valid_instances_accepted": sum(1 for r in valid_results if r["accepted"]),
        "expected_rejections_accepted": sum(1 for r in rejection_results if r["accepted"]),
        "agent_boot_exercises_accepted": sum(1 for r in exercise_results if r["accepted"]),
        "findings": findings,
        "valid_instance_results": valid_results,
        "expected_rejection_results": rejection_results,
        "agent_boot_exercise_results": exercise_results,
        "non_claims": [
            "This validator checks candidate current-context artifacts only.",
            "Passing validation does not promote template specs or agent boots to accepted law.",
            "No external agent invocation or production mutation is performed."
        ],
    }
    return report


def main() -> int:
    report = build_report()
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "accepted_candidate_validation" else 1


if __name__ == "__main__":
    raise SystemExit(main())
