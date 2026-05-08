"""V55 UI work-surface projection receipt.

Projects V54 visual closure/runtime receipt state into an operator-facing ION/JOC
maintained work surface. This is a projection and planning surface only: it tells
UI builders what must be rendered and what must remain bounded. It does not grant
production authority, unrestricted browser control, credential access, form
submission, destructive action, persistent DOM mutation, or external-network
authority.
"""
from __future__ import annotations
import argparse, hashlib, json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

SCHEMA_ID = "ion.ui_work_surface_projection.v1"
VERSION = "V55_VISUAL_CLOSURE_GRAPH_PROJECTION_AND_UI_WORK_SURFACE"
AUTHORITY_SCOPE = "UI_WORK_SURFACE_PROJECTION_RECEIPT_ONLY"
DEFAULT_REPORT_DIR = "ION/05_context/history/ui_work_surface_projection_receipts"

REQUIRED_LAYOUT_ZONES = (
    "TOP_BAR",
    "LEFT_RAIL",
    "MAIN_WORK_SURFACE",
    "RIGHT_INSPECTOR",
    "BOTTOM_TIMELINE",
)
REQUIRED_PROJECTION_SURFACES = (
    "MAINTAINED_WORK_SURFACE_OVERVIEW",
    "FRONT_STAGE_COUNCIL_STATE_STRIP",
    "CLAIM_AND_RECEIPT_RAIL",
    "VISUAL_EVIDENCE_LENS",
    "MISSION_DISPATCH_AND_MODEL_ROUTE_PANEL",
    "CONTEXT_GRAPH_COGNITIVE_EXPLORER",
    "REACTIVE_OS_STREAM",
    "CONVERSATIONAL_REPAIR_QUEUE",
    "BROWSER_SESSION_AUTOMATION_OVERLAY",
    "COMPUTE_AND_COST_ROUTER",
)
REQUIRED_AUTOMATION_LOOPS = (
    "VISUAL_ISSUE_CLOSURE_LOOP",
    "MISSION_DISPATCH_LOOP",
    "SESSION_HEALTH_LOOP",
    "CONTEXT_PROJECTION_LOOP",
    "CONVERSATIONAL_REPAIR_LOOP",
    "MODEL_COST_QUALITY_LOOP",
)
DXL_REQUIRED_TRUE = (
    "no_emoji_ui_controls",
    "custom_inline_svg_icons",
    "mono_dense_uppercase_labels",
    "instrument_panel_radius_lte_2px",
    "no_material_design_structural_colors",
    "no_placeholder_only_finished_panels",
    "desktop_first_full_width_layout",
)
FORBIDDEN_CAPABILITIES = {
    "production_authority": False,
    "unrestricted_browser_control": False,
    "credential_access": False,
    "external_network_authority": False,
    "account_operation": False,
    "destructive_action": False,
    "form_submission": False,
    "purchase_or_submission": False,
    "persistent_dom_mutation": False,
    "production_visual_automation": False,
}

@dataclass(frozen=True)
class UIWorkSurfaceProjectionRequest:
    projection_name: str
    target_ui: str = "ION/JOC maintained work surface"
    source_inputs: tuple[str, ...] = ()
    visual_closure_receipt_ids: tuple[str, ...] = ()
    front_stage_receipt_ids: tuple[str, ...] = ()
    conversational_repair_receipt_ids: tuple[str, ...] = ()
    layout_zones: tuple[str, ...] = REQUIRED_LAYOUT_ZONES
    projection_surfaces: tuple[str, ...] = REQUIRED_PROJECTION_SURFACES
    automation_loops: tuple[str, ...] = REQUIRED_AUTOMATION_LOOPS
    dxl_constraints: dict[str, bool] = field(default_factory=lambda: {k: True for k in DXL_REQUIRED_TRUE})
    requested_capabilities: dict[str, bool] = field(default_factory=dict)
    notes: tuple[str, ...] = ()

@dataclass(frozen=True)
class UIWorkSurfaceProjectionReceipt:
    schema_id: str
    version: str
    projection_id: str
    emitted_at: str
    projection_name: str
    target_ui: str
    authority_scope: str
    source_inputs: tuple[str, ...]
    visual_closure_receipt_ids: tuple[str, ...]
    front_stage_receipt_ids: tuple[str, ...]
    conversational_repair_receipt_ids: tuple[str, ...]
    layout_zones: tuple[str, ...]
    projection_surfaces: tuple[str, ...]
    automation_loops: tuple[str, ...]
    dxl_constraints: dict[str, bool]
    missing_layout_zones: tuple[str, ...]
    missing_projection_surfaces: tuple[str, ...]
    missing_automation_loops: tuple[str, ...]
    projection_findings: tuple[str, ...]
    projection_verdict: str
    recommended_next_actions: tuple[str, ...]
    forbidden_capabilities: dict[str, bool] = field(default_factory=lambda: dict(FORBIDDEN_CAPABILITIES))
    production_authority: bool = False
    unrestricted_browser_control_authorized: bool = False
    credential_access_authorized: bool = False
    external_network_authorized: bool = False
    destructive_action_authorized: bool = False
    submit_or_account_action_authorized: bool = False
    persistent_dom_mutation_authorized: bool = False


def build_ui_work_surface_projection_receipt(*, request: UIWorkSurfaceProjectionRequest, emitted_at: str | None = None) -> UIWorkSurfaceProjectionReceipt:
    _validate_request(request)
    findings = list(request.notes)
    forbidden_requested = tuple(k for k, v in request.requested_capabilities.items() if v and k in FORBIDDEN_CAPABILITIES)
    if forbidden_requested:
        findings.append("requested forbidden capabilities: " + ", ".join(sorted(forbidden_requested)))
    missing_zones = tuple(z for z in REQUIRED_LAYOUT_ZONES if z not in request.layout_zones)
    missing_surfaces = tuple(s for s in REQUIRED_PROJECTION_SURFACES if s not in request.projection_surfaces)
    missing_loops = tuple(l for l in REQUIRED_AUTOMATION_LOOPS if l not in request.automation_loops)
    missing_dxl = tuple(k for k in DXL_REQUIRED_TRUE if request.dxl_constraints.get(k) is not True)
    if missing_zones:
        findings.append("missing required layout zones: " + ", ".join(missing_zones))
    if missing_surfaces:
        findings.append("missing required projection surfaces: " + ", ".join(missing_surfaces))
    if missing_loops:
        findings.append("missing required automation loops: " + ", ".join(missing_loops))
    if missing_dxl:
        findings.append("DXL constraints not affirmed: " + ", ".join(missing_dxl))
    if not request.source_inputs:
        findings.append("no UI source inputs attached")
    if not request.visual_closure_receipt_ids:
        findings.append("no visual closure receipt lineage attached")
    if not request.front_stage_receipt_ids:
        findings.append("no front-stage claim receipt lineage attached")
    verdict = _projection_verdict(bool(forbidden_requested), missing_zones, missing_surfaces, missing_loops, missing_dxl, request)
    ts = emitted_at or _utc_now()
    pid = _stable_id("v55-ui-work-surface-projection", ts, request.projection_name, request.target_ui, verdict)
    return UIWorkSurfaceProjectionReceipt(
        schema_id=SCHEMA_ID,
        version=VERSION,
        projection_id=pid,
        emitted_at=ts,
        projection_name=request.projection_name,
        target_ui=request.target_ui,
        authority_scope=AUTHORITY_SCOPE,
        source_inputs=request.source_inputs,
        visual_closure_receipt_ids=request.visual_closure_receipt_ids,
        front_stage_receipt_ids=request.front_stage_receipt_ids,
        conversational_repair_receipt_ids=request.conversational_repair_receipt_ids,
        layout_zones=request.layout_zones,
        projection_surfaces=request.projection_surfaces,
        automation_loops=request.automation_loops,
        dxl_constraints=dict(request.dxl_constraints),
        missing_layout_zones=missing_zones,
        missing_projection_surfaces=missing_surfaces,
        missing_automation_loops=missing_loops,
        projection_findings=tuple(findings),
        projection_verdict=verdict,
        recommended_next_actions=_actions(verdict),
        forbidden_capabilities=dict(FORBIDDEN_CAPABILITIES),
        production_authority=False,
    )


def validate_ui_work_surface_projection_receipt(receipt: UIWorkSurfaceProjectionReceipt) -> tuple[str, ...]:
    errors: list[str] = []
    if receipt.schema_id != SCHEMA_ID:
        errors.append("schema_id mismatch")
    if receipt.version != VERSION:
        errors.append("version mismatch")
    if receipt.authority_scope != AUTHORITY_SCOPE:
        errors.append("authority scope mismatch")
    if receipt.production_authority:
        errors.append("production authority must remain false")
    if receipt.unrestricted_browser_control_authorized or receipt.credential_access_authorized or receipt.external_network_authorized or receipt.destructive_action_authorized or receipt.submit_or_account_action_authorized or receipt.persistent_dom_mutation_authorized:
        errors.append("forbidden authority flag must remain false")
    if any(receipt.forbidden_capabilities.values()):
        errors.append("forbidden capabilities must all remain false")
    for zone in REQUIRED_LAYOUT_ZONES:
        if zone not in receipt.layout_zones:
            errors.append(f"required layout zone missing: {zone}")
    for surface in REQUIRED_PROJECTION_SURFACES:
        if surface not in receipt.projection_surfaces:
            errors.append(f"required projection surface missing: {surface}")
    for loop in REQUIRED_AUTOMATION_LOOPS:
        if loop not in receipt.automation_loops:
            errors.append(f"required automation loop missing: {loop}")
    for key in DXL_REQUIRED_TRUE:
        if receipt.dxl_constraints.get(key) is not True:
            errors.append(f"DXL constraint must be true: {key}")
    if receipt.projection_verdict == "VALID_UI_WORK_SURFACE_PROJECTION" and receipt.projection_findings:
        errors.append("valid projection must not carry blocking findings")
    return tuple(errors)


def load_ui_work_surface_projection_request(workspace_root: str | Path, request_path: str | Path) -> UIWorkSurfaceProjectionRequest:
    root = Path(workspace_root).resolve()
    p = _inside(root, request_path)
    return request_from_mapping(json.loads(p.read_text(encoding="utf-8")))


def request_from_mapping(data: Mapping[str, Any]) -> UIWorkSurfaceProjectionRequest:
    def tup(name: str, default: Sequence[str] = ()) -> tuple[str, ...]:
        value = data.get(name, default)
        if value is None:
            return ()
        if isinstance(value, str):
            return (value,)
        return tuple(str(x) for x in value)
    return UIWorkSurfaceProjectionRequest(
        projection_name=str(data.get("projection_name") or "ION/JOC UI work surface projection"),
        target_ui=str(data.get("target_ui") or "ION/JOC maintained work surface"),
        source_inputs=tup("source_inputs"),
        visual_closure_receipt_ids=tup("visual_closure_receipt_ids"),
        front_stage_receipt_ids=tup("front_stage_receipt_ids"),
        conversational_repair_receipt_ids=tup("conversational_repair_receipt_ids"),
        layout_zones=tup("layout_zones", REQUIRED_LAYOUT_ZONES),
        projection_surfaces=tup("projection_surfaces", REQUIRED_PROJECTION_SURFACES),
        automation_loops=tup("automation_loops", REQUIRED_AUTOMATION_LOOPS),
        dxl_constraints={str(k): bool(v) for k, v in (data.get("dxl_constraints") or {k: True for k in DXL_REQUIRED_TRUE}).items()},
        requested_capabilities={str(k): bool(v) for k, v in (data.get("requested_capabilities") or {}).items()},
        notes=tup("notes"),
    )


def write_ui_work_surface_projection_receipt(workspace_root: str | Path, receipt: UIWorkSurfaceProjectionReceipt, *, report_dir: str = DEFAULT_REPORT_DIR) -> Path:
    root = Path(workspace_root).resolve()
    out = root / report_dir
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{receipt.projection_id}.ui_work_surface_projection_receipt.json"
    path.write_text(json.dumps(_json(receipt), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def format_ui_work_surface_projection_summary(receipt: UIWorkSurfaceProjectionReceipt) -> str:
    return "\n".join([
        f"version: {receipt.version}",
        f"projection_verdict: {receipt.projection_verdict}",
        f"authority_scope: {receipt.authority_scope}",
        f"layout_zones: {len(receipt.layout_zones)}",
        f"projection_surfaces: {len(receipt.projection_surfaces)}",
        f"automation_loops: {len(receipt.automation_loops)}",
        f"findings: {len(receipt.projection_findings)}",
        f"production_authority: {receipt.production_authority}",
    ])


def _projection_verdict(forbidden_requested: bool, missing_zones: Sequence[str], missing_surfaces: Sequence[str], missing_loops: Sequence[str], missing_dxl: Sequence[str], request: UIWorkSurfaceProjectionRequest) -> str:
    if forbidden_requested:
        return "UI_WORK_SURFACE_PROJECTION_BLOCKED_FOR_AUTHORITY_OVERREACH"
    if missing_dxl:
        return "UI_WORK_SURFACE_PROJECTION_NEEDS_DXL_REPAIR"
    if missing_zones or missing_surfaces or missing_loops:
        return "UI_WORK_SURFACE_PROJECTION_INCOMPLETE"
    if not request.source_inputs or not request.visual_closure_receipt_ids or not request.front_stage_receipt_ids:
        return "UI_WORK_SURFACE_PROJECTION_NEEDS_SOURCE_LINEAGE"
    return "VALID_UI_WORK_SURFACE_PROJECTION"


def _actions(verdict: str) -> tuple[str, ...]:
    if verdict == "VALID_UI_WORK_SURFACE_PROJECTION":
        return (
            "bind projection receipt to actual JOC/Electron/React shell components",
            "implement DXL-compliant top bar, left rail, main surface, right inspector, and bottom timeline",
            "render V54 visual closure receipts in the Visual Evidence Lens and Receipt Rail",
            "wire Reactive OS Stream to filesystem, test, automation, and repair events",
        )
    if verdict == "UI_WORK_SURFACE_PROJECTION_BLOCKED_FOR_AUTHORITY_OVERREACH":
        return ("remove requested forbidden capabilities", "route capability escalation through Steward/VZ review")
    if verdict == "UI_WORK_SURFACE_PROJECTION_NEEDS_DXL_REPAIR":
        return ("repair DXL constraint mismatch", "revalidate no-emoji/custom-SVG/instrument-panel constraints")
    if verdict == "UI_WORK_SURFACE_PROJECTION_INCOMPLETE":
        return ("add missing layout zones, projection surfaces, or automation loops",)
    return ("attach source lineage and receipt lineage before using projection as UI build authority",)


def _validate_request(request: UIWorkSurfaceProjectionRequest) -> None:
    if not request.projection_name.strip():
        raise ValueError("projection_name is required")
    unknown = tuple(k for k in request.requested_capabilities if k not in FORBIDDEN_CAPABILITIES)
    if unknown:
        raise ValueError("unknown requested capabilities: " + ", ".join(sorted(unknown)))


def _inside(root: Path, p: str | Path) -> Path:
    path = (root / p).resolve()
    if root not in path.parents and path != root:
        raise ValueError("path escapes workspace root")
    return path


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stable_id(*parts: str) -> str:
    return hashlib.sha256("::".join(parts).encode("utf-8")).hexdigest()[:24]


def _json(obj: Any) -> Any:
    if hasattr(obj, "__dataclass_fields__"):
        return asdict(obj)
    return obj


def _scenario(name: str) -> UIWorkSurfaceProjectionRequest:
    base_sources = (
        "ION/docs/ui/source_inputs/CANON_JOC_UI_ARCHITECTURE.md",
        "ION/docs/ui/source_inputs/JOC_UI_REQUIREMENTS.md",
        "ION/docs/ui/source_inputs/OPUS1_JOC_ARCHITECTURE.md",
        "ION/docs/ui/source_inputs/OPUS1_JOC_COMPUTE_AND_IDE_LAYOUT.md",
        "ION/docs/ui/source_inputs/OPUS1_JOC_GOALS_AND_ROADMAP.md",
        "ION/docs/ui/source_inputs/ui_evolution_plan.md",
    )
    if name == "valid":
        return UIWorkSurfaceProjectionRequest(
            projection_name="ION/JOC V55 UI work surface projection",
            source_inputs=base_sources,
            visual_closure_receipt_ids=("v54-visual-run-diagnosis-binding-81e07a3edf21feee",),
            front_stage_receipt_ids=("v41-front-stage-council-runtime-receipt-reference",),
            conversational_repair_receipt_ids=("v42-conversational-repair-reference",),
        )
    if name == "missing_source":
        return UIWorkSurfaceProjectionRequest(projection_name="missing source")
    if name == "missing_zone":
        return UIWorkSurfaceProjectionRequest(
            projection_name="missing zone",
            source_inputs=base_sources,
            visual_closure_receipt_ids=("v54",),
            front_stage_receipt_ids=("v41",),
            layout_zones=("TOP_BAR", "LEFT_RAIL"),
        )
    if name == "dxl_repair":
        return UIWorkSurfaceProjectionRequest(
            projection_name="dxl repair",
            source_inputs=base_sources,
            visual_closure_receipt_ids=("v54",),
            front_stage_receipt_ids=("v41",),
            dxl_constraints={**{k: True for k in DXL_REQUIRED_TRUE}, "no_emoji_ui_controls": False},
        )
    if name == "overreach":
        return UIWorkSurfaceProjectionRequest(
            projection_name="overreach",
            source_inputs=base_sources,
            visual_closure_receipt_ids=("v54",),
            front_stage_receipt_ids=("v41",),
            requested_capabilities={"credential_access": True},
        )
    raise ValueError(f"unknown scenario: {name}")


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build V55 UI work-surface projection receipt.")
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--request", default=None)
    parser.add_argument("--scenario", default="valid")
    parser.add_argument("--emitted-at", default=None)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    if args.request:
        req = load_ui_work_surface_projection_request(args.workspace_root, args.request)
    else:
        req = _scenario(args.scenario)
    receipt = build_ui_work_surface_projection_receipt(request=req, emitted_at=args.emitted_at)
    errors = validate_ui_work_surface_projection_receipt(receipt)
    if args.write:
        path = write_ui_work_surface_projection_receipt(args.workspace_root, receipt)
        print(f"receipt_path: {path}")
    print(format_ui_work_surface_projection_summary(receipt))
    if errors:
        print("errors:")
        for error in errors:
            print(f"- {error}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
