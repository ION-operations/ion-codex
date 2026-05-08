"""V60 branch consolidation verifier for ION/JOC UI and model-governor lanes."""
from __future__ import annotations

import argparse, hashlib, json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

SCHEMA_ID = "ion.branch_consolidation_ui_model_governor_binding.v1"
VERSION = "V60_BRANCH_CONSOLIDATION_UI_MODEL_GOVERNOR_BINDING"
AUTHORITY_SCOPE = "BRANCH_CONSOLIDATION_AND_UI_MODEL_GOVERNOR_BINDING_RECEIPT_ONLY"
DEFAULT_REPORT_DIR = "ION/05_context/history/branch_consolidation_receipts"

REQUIRED_BUDGET_SURFACES = (
    "ION/00_BOOTSTRAP/V56_MODEL_ECONOMICS_REGISTRY_SKELETONS_LOCK.md",
    "ION/00_BOOTSTRAP/V57_MODEL_ROUTER_AND_COST_QUALITY_ROUTING_LOCK.md",
    "ION/00_BOOTSTRAP/V58_BUDGET_AND_API_RATE_GOVERNORS_LOCK.md",
    "ION/02_architecture/MODEL_ROUTER_AND_COST_QUALITY_ROUTING_PROTOCOL.md",
    "ION/02_architecture/BUDGET_AND_API_RATE_GOVERNORS_PROTOCOL.md",
    "ION/03_registry/model_route_decision.schema.json",
    "ION/03_registry/budget_governor_decision.schema.json",
    "ION/03_registry/api_rate_governor_decision.schema.json",
    "ION/04_packages/kernel/model_router.py",
    "ION/04_packages/kernel/cost_quality_router.py",
    "ION/04_packages/kernel/budget_governor.py",
    "ION/04_packages/kernel/api_rate_governor.py",
    "ION/tests/test_kernel_model_router.py",
    "ION/tests/test_kernel_budget_governor.py",
    "ION/tests/test_kernel_api_rate_governor.py",
)
REQUIRED_UI_SURFACES = (
    "ION/00_BOOTSTRAP/V55_VISUAL_CLOSURE_GRAPH_PROJECTION_AND_UI_WORK_SURFACE_LOCK.md",
    "ION/00_BOOTSTRAP/V56_ION_JOC_COCKPIT_SHELL_COMPONENT_CONTRACTS_LOCK.md",
    "ION/00_BOOTSTRAP/V57_REACTIVE_OS_STREAM_AND_AUTOMATION_VIEW_MODEL_LOCK.md",
    "ION/00_BOOTSTRAP/V58_COGNITIVE_EXPLORER_AND_CONTEXT_ROUTE_VIEW_MODEL_LOCK.md",
    "ION/00_BOOTSTRAP/V59_MISSION_DISPATCH_AND_MODEL_ROUTE_VIEW_MODEL_LOCK.md",
    "ION/04_packages/kernel/ui_work_surface_projection.py",
    "ION/04_packages/kernel/joc_cockpit_component_contract.py",
    "ION/04_packages/kernel/joc_reactive_os_stream_view_model.py",
    "ION/04_packages/kernel/joc_cognitive_explorer_route_view_model.py",
    "ION/04_packages/kernel/joc_mission_dispatch_route_view_model.py",
    "ION/08_ui/joc_cockpit_shell/JocCockpitShell.tsx",
    "ION/08_ui/joc_cockpit_shell/MissionDispatchRouterPanel.tsx",
    "ION/08_ui/joc_cockpit_shell/ModelRouteMatrixPanel.tsx",
    "ION/tests/test_kernel_joc_mission_dispatch_route_view_model.py",
)
REQUIRED_BINDINGS = (
    "cognitive_route_to_dispatch_preview",
    "dispatch_preview_to_model_router",
    "model_router_to_budget_governor",
    "model_router_to_api_rate_governor",
    "governor_chain_to_future_dry_run_call_receipt",
)
FORBIDDEN_CAPABILITIES = {
    "live_external_model_dispatch": False,
    "provider_credentials": False,
    "browser_session_mutation": False,
    "scheduler_direct_provider_calls": False,
    "paid_cloud_launch": False,
    "source_summary_rewrite": False,
    "canonical_graph_write": False,
    "unrestricted_agent_activation": False,
    "production_authority": False,
}

@dataclass(frozen=True)
class BranchBinding:
    binding_id: str
    from_surface: str
    to_surface: str
    required_before_live_dispatch: bool
    rationale: str = "required V60 consolidation binding"

@dataclass(frozen=True)
class BranchConsolidationCandidate:
    consolidation_id: str
    economics_lane: tuple[str, ...]
    ui_lane: tuple[str, ...]
    bindings: tuple[BranchBinding, ...]
    blocked_capabilities: Mapping[str, bool] = field(default_factory=lambda: FORBIDDEN_CAPABILITIES.copy())

@dataclass(frozen=True)
class BranchConsolidationReceipt:
    version: str
    schema_id: str
    receipt_id: str
    generated_at: str
    authority_scope: str
    consolidation_id: str
    consolidation_verdict: str
    budget_branch_present: bool
    ui_branch_present: bool
    budget_surface_count: int
    ui_surface_count: int
    binding_count: int
    economics_lane: tuple[str, ...]
    ui_lane: tuple[str, ...]
    bindings: tuple[Mapping[str, Any], ...]
    findings: tuple[str, ...]
    blocked_capabilities: Mapping[str, bool]
    production_authority: bool = False
    live_dispatch_claim: bool = False
    next_recommended_branch: str = "V61_DRY_RUN_MODEL_CALL_RECEIPTS_AND_GOVERNED_DISPATCH_PREVIEW"
    def to_dict(self) -> dict[str, Any]: return asdict(self)

def _utc_now() -> str: return datetime.now(timezone.utc).replace(microsecond=0).isoformat()
def _stable_id(*parts: str) -> str: return hashlib.sha256("::".join(parts).encode()).hexdigest()[:24]
def _missing(root: Path, surfaces: Sequence[str]) -> tuple[str, ...]: return tuple(s for s in surfaces if not (root / s).exists())

def default_consolidation_candidate() -> BranchConsolidationCandidate:
    return BranchConsolidationCandidate(
        "v60-ui-model-governor-branch-consolidation",
        ("V56_MODEL_ECONOMICS_REGISTRY_SKELETONS", "V57_MODEL_ROUTER_AND_COST_QUALITY_ROUTING", "V58_BUDGET_AND_API_RATE_GOVERNORS"),
        ("V55_VISUAL_CLOSURE_GRAPH_PROJECTION_AND_UI_WORK_SURFACE", "V56_ION_JOC_COCKPIT_SHELL_COMPONENT_CONTRACTS", "V57_REACTIVE_OS_STREAM_AND_AUTOMATION_VIEW_MODEL", "V58_COGNITIVE_EXPLORER_AND_CONTEXT_ROUTE_VIEW_MODEL", "V59_MISSION_DISPATCH_AND_MODEL_ROUTE_VIEW_MODEL"),
        tuple(BranchBinding(bid, src, dst, req) for bid, src, dst, req in (
            ("cognitive_route_to_dispatch_preview", "V58_COGNITIVE_EXPLORER_AND_CONTEXT_ROUTE_VIEW_MODEL", "V59_MISSION_DISPATCH_AND_MODEL_ROUTE_VIEW_MODEL", False),
            ("dispatch_preview_to_model_router", "V59_MISSION_DISPATCH_AND_MODEL_ROUTE_VIEW_MODEL", "V57_MODEL_ROUTER_AND_COST_QUALITY_ROUTING", True),
            ("model_router_to_budget_governor", "V57_MODEL_ROUTER_AND_COST_QUALITY_ROUTING", "V58_BUDGET_AND_API_RATE_GOVERNORS", True),
            ("model_router_to_api_rate_governor", "V57_MODEL_ROUTER_AND_COST_QUALITY_ROUTING", "V58_BUDGET_AND_API_RATE_GOVERNORS", True),
            ("governor_chain_to_future_dry_run_call_receipt", "V58_BUDGET_AND_API_RATE_GOVERNORS", "V61_DRY_RUN_MODEL_CALL_RECEIPTS_AND_GOVERNED_DISPATCH_PREVIEW", True),
        )),
    )

def candidate_from_mapping(data: Mapping[str, Any]) -> BranchConsolidationCandidate:
    return BranchConsolidationCandidate(
        str(data.get("consolidation_id", "v60-fixture")),
        tuple(str(x) for x in data.get("economics_lane", ())),
        tuple(str(x) for x in data.get("ui_lane", ())),
        tuple(BranchBinding(str(x.get("binding_id","")), str(x.get("from_surface","")), str(x.get("to_surface","")), bool(x.get("required_before_live_dispatch", False))) for x in data.get("bindings", ()) if isinstance(x, Mapping)),
        dict(data.get("blocked_capabilities", FORBIDDEN_CAPABILITIES)),
    )

def load_candidate(path: str | Path) -> BranchConsolidationCandidate:
    return candidate_from_mapping(json.loads(Path(path).read_text(encoding="utf-8")))

def validate_branch_consolidation(workspace_root: str | Path, candidate: BranchConsolidationCandidate | None = None, *, generated_at: str | None = None) -> BranchConsolidationReceipt:
    root = Path(workspace_root); candidate = candidate or default_consolidation_candidate(); findings=[]; verdict="CONSOLIDATED_BINDING_READY"
    mb=_missing(root, REQUIRED_BUDGET_SURFACES); mu=_missing(root, REQUIRED_UI_SURFACES)
    if mb: findings.append("missing budget branch surfaces: "+", ".join(mb)); verdict="BLOCKED_MISSING_BUDGET_BRANCH_SURFACES"
    if mu: findings.append("missing UI branch surfaces: "+", ".join(mu)); verdict="BLOCKED_MISSING_UI_BRANCH_SURFACES"
    ids={b.binding_id for b in candidate.bindings}; miss=[x for x in REQUIRED_BINDINGS if x not in ids]
    if miss: findings.append("missing required bindings: "+", ".join(miss)); verdict="BLOCKED_MISSING_BINDINGS"
    for k, exp in FORBIDDEN_CAPABILITIES.items():
        if candidate.blocked_capabilities.get(k) is not exp: findings.append(f"forbidden capability {k!r} expected {exp!r} got {candidate.blocked_capabilities.get(k)!r}"); verdict="BLOCKED_FORBIDDEN_CAPABILITY"
    for k,v in candidate.blocked_capabilities.items():
        if v is not False: findings.append(f"capability {k!r} is not blocked"); verdict="BLOCKED_FORBIDDEN_CAPABILITY"
    ts=generated_at or _utc_now(); payload=json.dumps({"id":candidate.consolidation_id,"verdict":verdict,"ts":ts},sort_keys=True)
    return BranchConsolidationReceipt(VERSION, SCHEMA_ID, _stable_id("v60", payload), ts, AUTHORITY_SCOPE, candidate.consolidation_id, verdict, not mb, not mu, len(REQUIRED_BUDGET_SURFACES)-len(mb), len(REQUIRED_UI_SURFACES)-len(mu), len(candidate.bindings), candidate.economics_lane, candidate.ui_lane, tuple(asdict(b) for b in candidate.bindings), tuple(findings), dict(candidate.blocked_capabilities), False, False)

def _jsonable(x: Any) -> Any:
    if hasattr(x, "__dataclass_fields__"): return {k:_jsonable(v) for k,v in asdict(x).items()}
    if isinstance(x, tuple): return [_jsonable(v) for v in x]
    if isinstance(x, dict): return {str(k):_jsonable(v) for k,v in x.items()}
    return x

def write_branch_consolidation_receipt(workspace_root: str | Path, receipt: BranchConsolidationReceipt, *, output_dir: str | Path = DEFAULT_REPORT_DIR) -> Path:
    out=Path(workspace_root)/output_dir; out.mkdir(parents=True, exist_ok=True)
    path=out/f"{receipt.receipt_id}.branch_consolidation_ui_model_governor_binding_receipt.json"
    path.write_text(json.dumps(_jsonable(receipt), indent=2, sort_keys=True)+"\n", encoding="utf-8")
    return path

def _main(argv: Sequence[str] | None = None) -> int:
    p=argparse.ArgumentParser(); p.add_argument("--workspace-root", default="."); p.add_argument("--fixture"); p.add_argument("--write", action="store_true"); p.add_argument("--generated-at")
    a=p.parse_args(argv); cand=load_candidate(a.fixture) if a.fixture else None; r=validate_branch_consolidation(a.workspace_root, cand, generated_at=a.generated_at)
    if a.write: print(write_branch_consolidation_receipt(a.workspace_root, r).as_posix())
    print(json.dumps(_jsonable(r), indent=2, sort_keys=True)); return 0 if r.consolidation_verdict=="CONSOLIDATED_BINDING_READY" else 2
if __name__ == "__main__": raise SystemExit(_main())
