"""V56 registry skeleton validation for API Provider Orchestration and Model Economics.

This module intentionally performs deterministic registry validation only.
It does not route calls, load credentials, call providers, or authorize production use.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

import yaml

SCHEMA_ID = "ion.model_economics_registry_skeleton_report.v1"
VERSION = "V56_MODEL_ECONOMICS_REGISTRY_SKELETONS"
AUTHORITY_SCOPE = "A3_STEWARD_MODEL_ECONOMICS_REGISTRY_SKELETON"
DEFAULT_REPORT_DIR = "ION/05_context/history/model_economics_registry_reports"
REGISTRY_PATHS = {
    "provider_registry": "ION/03_registry/provider_registry.yaml",
    "model_capability_registry": "ION/03_registry/model_capability_registry.yaml",
    "model_pricing_registry": "ION/03_registry/model_pricing_registry.yaml",
    "model_rate_limit_registry": "ION/03_registry/model_rate_limit_registry.yaml",
    "model_routing_policy": "ION/03_registry/model_routing_policy.yaml",
    "model_eval_score_registry": "ION/03_registry/model_eval_score_registry.yaml",
    "model_data_handling_registry": "ION/03_registry/model_data_handling_registry.yaml",
    "budget_policy": "ION/03_registry/budget_policy.yaml",
    "work_class_model_policy": "ION/03_registry/work_class_model_policy.yaml",
}
REQUIRED_PROVIDERS = ("openai", "anthropic", "gemini", "cerebras", "local")
REQUIRED_WORK_CLASSES = (
    "cheap_classification", "graph_indexing", "source_summary_rewrite_draft",
    "source_summary_rewrite_review", "code_patch", "code_review", "architecture_design",
    "visual_diagnosis", "claim_audit", "adversarial_review", "user_facing_answer",
    "front_stage_claim_classification", "conversation_repair", "long_context_digest",
    "batch_corpus_processing", "embedding_generation", "local_private_tagging",
)
FORBIDDEN_FLAG_PATHS = (
    ("provider_registry", ("live_provider_calls_authorized",)),
    ("provider_registry", ("provider_credentials_authorized",)),
    ("provider_registry", ("scheduler_direct_provider_calls_authorized",)),
    ("provider_registry", ("production_authority",)),
    ("model_routing_policy", ("live_routing_authorized",)),
    ("model_routing_policy", ("production_authority",)),
    ("budget_policy", ("budget_enforcement_authorized",)),
    ("budget_policy", ("production_authority",)),
)

@dataclass(frozen=True)
class RegistryValidationIssue:
    registry: str
    issue: str
    severity: str = "blocking"

@dataclass(frozen=True)
class ModelEconomicsRegistryReport:
    schema_id: str
    version: str
    report_id: str
    emitted_at: str
    workspace_root: str
    authority_scope: str
    verdict: str
    registry_count: int
    registries_loaded: tuple[str, ...]
    required_providers_present: bool
    required_work_classes_present: bool
    forbidden_authority_flags: dict[str, bool]
    live_provider_calls_authorized: bool
    provider_credentials_authorized: bool
    scheduler_direct_provider_calls_authorized: bool
    production_authority: bool
    issues: tuple[RegistryValidationIssue, ...]
    next_recommended_branch: str = "V57_MODEL_ROUTER_AND_COST_QUALITY_ROUTING"


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stable_id(*parts: str) -> str:
    return hashlib.sha256("::".join(parts).encode("utf-8")).hexdigest()[:24]


def load_yaml(path: Path) -> Mapping[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, Mapping):
        raise ValueError(f"{path} did not parse to a mapping")
    return data


def load_registries(workspace_root: str | Path) -> dict[str, Mapping[str, Any]]:
    root = Path(workspace_root)
    loaded: dict[str, Mapping[str, Any]] = {}
    for key, rel in REGISTRY_PATHS.items():
        path = root / rel
        if not path.exists():
            loaded[key] = {"__missing__": True}
        else:
            loaded[key] = load_yaml(path)
    return loaded


def _get_flag(registries: Mapping[str, Mapping[str, Any]], registry: str, key_path: Sequence[str]) -> bool:
    obj: Any = registries.get(registry, {})
    for key in key_path:
        if not isinstance(obj, Mapping):
            return False
        obj = obj.get(key)
    return bool(obj)


def validate_registries(registries: Mapping[str, Mapping[str, Any]]) -> tuple[RegistryValidationIssue, ...]:
    issues: list[RegistryValidationIssue] = []
    for name in REGISTRY_PATHS:
        reg = registries.get(name)
        if not reg or reg.get("__missing__"):
            issues.append(RegistryValidationIssue(name, "registry file missing"))
            continue
        if reg.get("production_authority") is not False:
            issues.append(RegistryValidationIssue(name, "production_authority must be false"))
        if not str(reg.get("schema_id", "")).startswith("ion."):
            issues.append(RegistryValidationIssue(name, "schema_id missing or invalid"))
    providers = registries.get("provider_registry", {}).get("providers", {})
    if not isinstance(providers, Mapping):
        issues.append(RegistryValidationIssue("provider_registry", "providers mapping missing"))
    else:
        missing = [p for p in REQUIRED_PROVIDERS if p not in providers]
        if missing:
            issues.append(RegistryValidationIssue("provider_registry", "missing required providers: " + ",".join(missing)))
        for pid, p in providers.items():
            if isinstance(p, Mapping) and (p.get("enabled_for_live_calls") or p.get("credential_source_allowed")):
                issues.append(RegistryValidationIssue("provider_registry", f"provider {pid} live/credential authority must remain false"))
    work_classes = registries.get("work_class_model_policy", {}).get("work_classes", {})
    if not isinstance(work_classes, Mapping):
        issues.append(RegistryValidationIssue("work_class_model_policy", "work_classes mapping missing"))
    else:
        missing = [w for w in REQUIRED_WORK_CLASSES if w not in work_classes]
        if missing:
            issues.append(RegistryValidationIssue("work_class_model_policy", "missing required work classes: " + ",".join(missing)))
        for wc, contract in work_classes.items():
            if not isinstance(contract, Mapping):
                issues.append(RegistryValidationIssue("work_class_model_policy", f"{wc} contract not mapping")); continue
            for field in ("minimum_quality", "default_routing_mode", "allowed_lanes", "privacy_floor", "max_default_parallelism", "required_capabilities"):
                if field not in contract:
                    issues.append(RegistryValidationIssue("work_class_model_policy", f"{wc} missing {field}"))
    for registry, key_path in FORBIDDEN_FLAG_PATHS:
        if _get_flag(registries, registry, key_path):
            issues.append(RegistryValidationIssue(registry, "forbidden authority flag true: " + ".".join(key_path)))
    return tuple(issues)


def build_model_economics_registry_report(workspace_root: str | Path, *, emitted_at: str | None = None) -> ModelEconomicsRegistryReport:
    root = Path(workspace_root).resolve()
    ts = emitted_at or _utc_now()
    registries = load_registries(root)
    issues = validate_registries(registries)
    providers = registries.get("provider_registry", {}).get("providers", {})
    work_classes = registries.get("work_class_model_policy", {}).get("work_classes", {})
    required_providers_present = isinstance(providers, Mapping) and all(p in providers for p in REQUIRED_PROVIDERS)
    required_work_classes_present = isinstance(work_classes, Mapping) and all(w in work_classes for w in REQUIRED_WORK_CLASSES)
    forbidden_flags = {f"{r}." + ".".join(k): _get_flag(registries, r, k) for r, k in FORBIDDEN_FLAG_PATHS}
    return ModelEconomicsRegistryReport(
        schema_id=SCHEMA_ID,
        version=VERSION,
        report_id=_stable_id("model-economics-registry", root.as_posix(), ts),
        emitted_at=ts,
        workspace_root=root.as_posix(),
        authority_scope=AUTHORITY_SCOPE,
        verdict="VALID_MODEL_ECONOMICS_REGISTRY_SKELETONS" if not issues else "BLOCKED_MODEL_ECONOMICS_REGISTRY_SKELETONS",
        registry_count=sum(1 for k in REGISTRY_PATHS if not registries.get(k, {}).get("__missing__")),
        registries_loaded=tuple(k for k in REGISTRY_PATHS if not registries.get(k, {}).get("__missing__")),
        required_providers_present=required_providers_present,
        required_work_classes_present=required_work_classes_present,
        forbidden_authority_flags=forbidden_flags,
        live_provider_calls_authorized=False,
        provider_credentials_authorized=False,
        scheduler_direct_provider_calls_authorized=False,
        production_authority=False,
        issues=issues,
    )


def _jsonable(obj: Any) -> Any:
    if hasattr(obj, "__dataclass_fields__"):
        return {k: _jsonable(v) for k, v in asdict(obj).items()}
    if isinstance(obj, tuple):
        return [_jsonable(x) for x in obj]
    if isinstance(obj, dict):
        return {str(k): _jsonable(v) for k, v in obj.items()}
    return obj


def write_model_economics_registry_report(workspace_root: str | Path, report: ModelEconomicsRegistryReport, *, output_dir: str | Path = DEFAULT_REPORT_DIR) -> Path:
    root = Path(workspace_root)
    out = root / output_dir
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"V56_MODEL_ECONOMICS_REGISTRY_REPORT_{report.report_id}.json"
    path.write_text(json.dumps(_jsonable(report), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Validate V56 model-economics registry skeletons.")
    p.add_argument("--workspace-root", default=".")
    p.add_argument("--write", action="store_true")
    p.add_argument("--json", action="store_true")
    return p


def main(argv: Sequence[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    report = build_model_economics_registry_report(args.workspace_root)
    if args.write:
        write_model_economics_registry_report(args.workspace_root, report)
    if args.json:
        print(json.dumps(_jsonable(report), indent=2, sort_keys=True))
    else:
        print(f"verdict: {report.verdict}")
        print(f"registry_count: {report.registry_count}")
        print(f"required_providers_present: {report.required_providers_present}")
        print(f"required_work_classes_present: {report.required_work_classes_present}")
        print(f"issues: {len(report.issues)}")
        print(f"next: {report.next_recommended_branch}")
    return 2 if report.issues else 0

if __name__ == "__main__":
    raise SystemExit(main())

