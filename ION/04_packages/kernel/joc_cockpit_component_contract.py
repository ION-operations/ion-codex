"""V56 ION/JOC cockpit component contract verifier.

This module validates whether a proposed ION/JOC cockpit shell exposes the
required V55 maintained-work-surface projection zones, components, automation
loops, DXL constraints, and non-authority boundaries.

It is a UI contract verifier only. It does not render a live React app, control a
browser, access credentials, submit forms, mutate external pages, or grant
production authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass, field, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

SCHEMA_ID = "ion.joc_cockpit_component_contract.v1"
VERSION = "V56_ION_JOC_COCKPIT_SHELL_COMPONENT_CONTRACTS"
AUTHORITY_SCOPE = "JOC_COCKPIT_COMPONENT_CONTRACT_RECEIPT_ONLY"
DEFAULT_REPORT_DIR = "ION/05_context/history/joc_cockpit_component_contract_receipts"

REQUIRED_LAYOUT_ZONES = (
    "TOP_BAR",
    "LEFT_RAIL",
    "MAIN_WORK_SURFACE",
    "RIGHT_INSPECTOR",
    "BOTTOM_TIMELINE",
)

REQUIRED_COMPONENTS = (
    "IonTopBar",
    "IonLeftRail",
    "IonMainWorkSurface",
    "IonRightInspector",
    "IonBottomTimeline",
    "ReceiptRail",
    "VisualEvidenceLens",
    "ReactiveOsStream",
    "MissionRoutePanel",
    "ContextGraphExplorer",
    "ConversationalRepairQueue",
    "BrowserAutomationOverlay",
    "ComputeCostRouter",
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

REQUIRED_DXL_CONSTRAINTS = (
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
class CockpitComponentContract:
    name: str
    layout_zone: str
    projection_surfaces: tuple[str, ...] = ()
    automation_loops: tuple[str, ...] = ()
    claim_lanes: tuple[str, ...] = ()
    evidence_lanes: tuple[str, ...] = ()
    receipts_rendered: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class CockpitComponentManifest:
    schema_id: str
    version: str
    component_set_name: str
    target_ui: str
    components: tuple[CockpitComponentContract, ...]
    layout_zones: tuple[str, ...]
    projection_surfaces: tuple[str, ...]
    automation_loops: tuple[str, ...]
    dxl_constraints: dict[str, bool]
    forbidden_capabilities: dict[str, bool]
    source_projection_receipt_ids: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class CockpitComponentContractReceipt:
    schema_id: str
    version: str
    receipt_id: str
    emitted_at: str
    component_set_name: str
    target_ui: str
    authority_scope: str
    component_count: int
    layout_zones: tuple[str, ...]
    projection_surfaces: tuple[str, ...]
    automation_loops: tuple[str, ...]
    source_projection_receipt_ids: tuple[str, ...]
    missing_layout_zones: tuple[str, ...]
    missing_components: tuple[str, ...]
    missing_projection_surfaces: tuple[str, ...]
    missing_automation_loops: tuple[str, ...]
    missing_dxl_constraints: tuple[str, ...]
    forbidden_capability_violations: tuple[str, ...]
    unbound_components: tuple[str, ...]
    findings: tuple[str, ...]
    verdict: str
    recommended_next_actions: tuple[str, ...]
    forbidden_capabilities: dict[str, bool] = field(default_factory=lambda: dict(FORBIDDEN_CAPABILITIES))
    production_authority: bool = False
    live_ui_claim: bool = False
    browser_control_authority: bool = False
    credential_access_authority: bool = False
    external_network_authority: bool = False
    persistent_dom_mutation_authority: bool = False


def build_cockpit_component_contract_receipt(*, manifest: CockpitComponentManifest, emitted_at: str | None = None) -> CockpitComponentContractReceipt:
    _validate_manifest_shape(manifest)

    component_names = tuple(c.name for c in manifest.components)
    missing_layout_zones = tuple(z for z in REQUIRED_LAYOUT_ZONES if z not in manifest.layout_zones)
    missing_components = tuple(c for c in REQUIRED_COMPONENTS if c not in component_names)
    missing_projection_surfaces = tuple(s for s in REQUIRED_PROJECTION_SURFACES if s not in manifest.projection_surfaces)
    missing_automation_loops = tuple(l for l in REQUIRED_AUTOMATION_LOOPS if l not in manifest.automation_loops)
    missing_dxl_constraints = tuple(k for k in REQUIRED_DXL_CONSTRAINTS if manifest.dxl_constraints.get(k) is not True)
    forbidden_capability_violations = tuple(k for k, expected in FORBIDDEN_CAPABILITIES.items() if manifest.forbidden_capabilities.get(k) is not expected)

    unbound_components = tuple(
        c.name
        for c in manifest.components
        if not c.projection_surfaces or not c.automation_loops or not c.claim_lanes or not c.evidence_lanes
    )

    findings: list[str] = list(manifest.notes)
    if missing_layout_zones:
        findings.append("missing layout zones: " + ", ".join(missing_layout_zones))
    if missing_components:
        findings.append("missing required components: " + ", ".join(missing_components))
    if missing_projection_surfaces:
        findings.append("missing projection surfaces: " + ", ".join(missing_projection_surfaces))
    if missing_automation_loops:
        findings.append("missing automation loops: " + ", ".join(missing_automation_loops))
    if missing_dxl_constraints:
        findings.append("DXL constraints not affirmed: " + ", ".join(missing_dxl_constraints))
    if forbidden_capability_violations:
        findings.append("forbidden capability violations: " + ", ".join(forbidden_capability_violations))
    if unbound_components:
        findings.append("components missing projection/loop/claim/evidence bindings: " + ", ".join(unbound_components))
    if not manifest.source_projection_receipt_ids:
        findings.append("no V55 projection receipt lineage attached")

    verdict = _verdict(
        missing_layout_zones=missing_layout_zones,
        missing_components=missing_components,
        missing_projection_surfaces=missing_projection_surfaces,
        missing_automation_loops=missing_automation_loops,
        missing_dxl_constraints=missing_dxl_constraints,
        forbidden_capability_violations=forbidden_capability_violations,
        unbound_components=unbound_components,
        source_projection_receipt_ids=manifest.source_projection_receipt_ids,
    )
    emitted = emitted_at or _utc_now()
    rid = _stable_id(VERSION, manifest.component_set_name, emitted, verdict)

    return CockpitComponentContractReceipt(
        schema_id=SCHEMA_ID,
        version=VERSION,
        receipt_id=rid,
        emitted_at=emitted,
        component_set_name=manifest.component_set_name,
        target_ui=manifest.target_ui,
        authority_scope=AUTHORITY_SCOPE,
        component_count=len(manifest.components),
        layout_zones=manifest.layout_zones,
        projection_surfaces=manifest.projection_surfaces,
        automation_loops=manifest.automation_loops,
        source_projection_receipt_ids=manifest.source_projection_receipt_ids,
        missing_layout_zones=missing_layout_zones,
        missing_components=missing_components,
        missing_projection_surfaces=missing_projection_surfaces,
        missing_automation_loops=missing_automation_loops,
        missing_dxl_constraints=missing_dxl_constraints,
        forbidden_capability_violations=forbidden_capability_violations,
        unbound_components=unbound_components,
        findings=tuple(findings),
        verdict=verdict,
        recommended_next_actions=_actions(verdict),
        forbidden_capabilities=dict(FORBIDDEN_CAPABILITIES),
        production_authority=False,
        live_ui_claim=False,
    )


def validate_cockpit_component_contract_receipt(receipt: CockpitComponentContractReceipt) -> tuple[str, ...]:
    errors: list[str] = []
    if receipt.schema_id != SCHEMA_ID:
        errors.append("schema_id mismatch")
    if receipt.version != VERSION:
        errors.append("version mismatch")
    if receipt.authority_scope != AUTHORITY_SCOPE:
        errors.append("authority_scope mismatch")
    if receipt.production_authority or receipt.live_ui_claim or receipt.browser_control_authority or receipt.credential_access_authority or receipt.external_network_authority or receipt.persistent_dom_mutation_authority:
        errors.append("authority flags must remain false")
    if any(receipt.forbidden_capabilities.values()):
        errors.append("forbidden capabilities must remain false")
    for zone in REQUIRED_LAYOUT_ZONES:
        if zone not in receipt.layout_zones:
            errors.append(f"required layout zone missing: {zone}")
    for surface in REQUIRED_PROJECTION_SURFACES:
        if surface not in receipt.projection_surfaces:
            errors.append(f"required projection surface missing: {surface}")
    for loop in REQUIRED_AUTOMATION_LOOPS:
        if loop not in receipt.automation_loops:
            errors.append(f"required automation loop missing: {loop}")
    if receipt.verdict == "VALID_JOC_COCKPIT_COMPONENT_CONTRACT" and (
        receipt.missing_layout_zones
        or receipt.missing_components
        or receipt.missing_projection_surfaces
        or receipt.missing_automation_loops
        or receipt.missing_dxl_constraints
        or receipt.forbidden_capability_violations
        or receipt.unbound_components
    ):
        errors.append("valid verdict cannot include missing/broken contract fields")
    return tuple(errors)


def load_manifest(workspace_root: str | Path, manifest_path: str | Path) -> CockpitComponentManifest:
    root = Path(workspace_root).resolve()
    path = _inside(root, manifest_path)
    return manifest_from_mapping(json.loads(path.read_text(encoding="utf-8")))


def manifest_from_mapping(data: Mapping[str, Any]) -> CockpitComponentManifest:
    def tup(name: str, default: Sequence[str] = ()) -> tuple[str, ...]:
        value = data.get(name, default)
        if value is None:
            return ()
        if isinstance(value, str):
            return (value,)
        return tuple(str(x) for x in value)

    components = tuple(_component_from_mapping(x) for x in data.get("components", ()))
    return CockpitComponentManifest(
        schema_id=str(data.get("schema_id") or ""),
        version=str(data.get("version") or ""),
        component_set_name=str(data.get("component_set_name") or ""),
        target_ui=str(data.get("target_ui") or ""),
        components=components,
        layout_zones=tup("layout_zones"),
        projection_surfaces=tup("projection_surfaces"),
        automation_loops=tup("automation_loops"),
        dxl_constraints={str(k): bool(v) for k, v in (data.get("dxl_constraints") or {}).items()},
        forbidden_capabilities={str(k): bool(v) for k, v in (data.get("forbidden_capabilities") or {}).items()},
        source_projection_receipt_ids=tup("source_projection_receipt_ids"),
        notes=tup("notes"),
    )


def write_cockpit_component_contract_receipt(workspace_root: str | Path, receipt: CockpitComponentContractReceipt, *, report_dir: str = DEFAULT_REPORT_DIR) -> Path:
    root = Path(workspace_root).resolve()
    out = root / report_dir
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{receipt.receipt_id}.joc_cockpit_component_contract_receipt.json"
    path.write_text(json.dumps(_json(receipt), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def format_cockpit_component_contract_summary(receipt: CockpitComponentContractReceipt) -> str:
    return "\n".join([
        f"version: {receipt.version}",
        f"verdict: {receipt.verdict}",
        f"authority_scope: {receipt.authority_scope}",
        f"component_count: {receipt.component_count}",
        f"layout_zones: {len(receipt.layout_zones)}",
        f"projection_surfaces: {len(receipt.projection_surfaces)}",
        f"automation_loops: {len(receipt.automation_loops)}",
        f"findings: {len(receipt.findings)}",
        f"production_authority: {receipt.production_authority}",
        f"live_ui_claim: {receipt.live_ui_claim}",
    ])


def _component_from_mapping(data: Mapping[str, Any]) -> CockpitComponentContract:
    def tup(name: str) -> tuple[str, ...]:
        value = data.get(name, ())
        if value is None:
            return ()
        if isinstance(value, str):
            return (value,)
        return tuple(str(x) for x in value)
    return CockpitComponentContract(
        name=str(data.get("name") or ""),
        layout_zone=str(data.get("layout_zone") or ""),
        projection_surfaces=tup("projection_surfaces"),
        automation_loops=tup("automation_loops"),
        claim_lanes=tup("claim_lanes"),
        evidence_lanes=tup("evidence_lanes"),
        receipts_rendered=tup("receipts_rendered"),
        notes=tup("notes"),
    )


def _validate_manifest_shape(manifest: CockpitComponentManifest) -> None:
    if manifest.schema_id != SCHEMA_ID:
        raise ValueError("schema_id must be " + SCHEMA_ID)
    if manifest.version != VERSION:
        raise ValueError("version must be " + VERSION)
    if not manifest.component_set_name.strip():
        raise ValueError("component_set_name is required")
    if not manifest.target_ui.strip():
        raise ValueError("target_ui is required")
    duplicate_components = _duplicates(c.name for c in manifest.components)
    if duplicate_components:
        raise ValueError("duplicate components: " + ", ".join(duplicate_components))
    unknown_forbidden = tuple(k for k in manifest.forbidden_capabilities if k not in FORBIDDEN_CAPABILITIES)
    if unknown_forbidden:
        raise ValueError("unknown forbidden capability keys: " + ", ".join(sorted(unknown_forbidden)))


def _verdict(*, missing_layout_zones: Sequence[str], missing_components: Sequence[str], missing_projection_surfaces: Sequence[str], missing_automation_loops: Sequence[str], missing_dxl_constraints: Sequence[str], forbidden_capability_violations: Sequence[str], unbound_components: Sequence[str], source_projection_receipt_ids: Sequence[str]) -> str:
    if forbidden_capability_violations:
        return "JOC_COCKPIT_COMPONENT_CONTRACT_BLOCKED_FOR_AUTHORITY_OVERREACH"
    if missing_dxl_constraints:
        return "JOC_COCKPIT_COMPONENT_CONTRACT_NEEDS_DXL_REPAIR"
    if missing_layout_zones or missing_components or missing_projection_surfaces or missing_automation_loops:
        return "JOC_COCKPIT_COMPONENT_CONTRACT_INCOMPLETE"
    if unbound_components:
        return "JOC_COCKPIT_COMPONENT_CONTRACT_NEEDS_BINDING_REPAIR"
    if not source_projection_receipt_ids:
        return "JOC_COCKPIT_COMPONENT_CONTRACT_NEEDS_V55_LINEAGE"
    return "VALID_JOC_COCKPIT_COMPONENT_CONTRACT"


def _actions(verdict: str) -> tuple[str, ...]:
    if verdict == "VALID_JOC_COCKPIT_COMPONENT_CONTRACT":
        return (
            "mount the cockpit shell scaffold into a React/Electron package",
            "bind live V55 projection receipts into UI state",
            "capture visual screenshots and emit V56 visual validation receipts",
            "wire the receipt rail, visual lens, and reactive OS stream before enabling browser controls",
        )
    if verdict == "JOC_COCKPIT_COMPONENT_CONTRACT_BLOCKED_FOR_AUTHORITY_OVERREACH":
        return ("set all forbidden capability flags to false", "route any escalation through Steward/VZ review")
    if verdict == "JOC_COCKPIT_COMPONENT_CONTRACT_NEEDS_DXL_REPAIR":
        return ("repair DXL constraints before rendering shell as ION-native",)
    if verdict == "JOC_COCKPIT_COMPONENT_CONTRACT_INCOMPLETE":
        return ("add missing layout zones, required components, projection surfaces, or automation loops",)
    if verdict == "JOC_COCKPIT_COMPONENT_CONTRACT_NEEDS_BINDING_REPAIR":
        return ("attach projection, automation, claim, and evidence bindings to every required component",)
    return ("attach V55 projection receipt lineage before using this as build authority",)


def _duplicates(values: Sequence[str] | Any) -> tuple[str, ...]:
    seen: set[str] = set()
    dupes: set[str] = set()
    for value in values:
        if value in seen:
            dupes.add(value)
        seen.add(value)
    return tuple(sorted(dupes))


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


def _scenario(name: str) -> CockpitComponentManifest:
    fixture = manifest_from_mapping(json.loads(Path("ION/05_context/fixtures/ui/v56_joc_cockpit_component_manifest.valid.json").read_text(encoding="utf-8")))
    if name == "valid":
        return fixture
    if name == "missing_component":
        return replace(fixture, components=fixture.components[:-1])
    if name == "dxl_repair":
        return replace(fixture, dxl_constraints={**fixture.dxl_constraints, "no_emoji_ui_controls": False})
    if name == "overreach":
        return replace(fixture, forbidden_capabilities={**fixture.forbidden_capabilities, "credential_access": True})
    if name == "unbound":
        broken = tuple(replace(c, automation_loops=()) if c.name == "ReceiptRail" else c for c in fixture.components)
        return replace(fixture, components=broken)
    if name == "no_lineage":
        return replace(fixture, source_projection_receipt_ids=())
    raise ValueError(f"unknown scenario: {name}")


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build V56 ION/JOC cockpit component contract receipt.")
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--manifest", default=None)
    parser.add_argument("--scenario", default="valid")
    parser.add_argument("--emitted-at", default=None)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    if args.manifest:
        manifest = load_manifest(args.workspace_root, args.manifest)
    else:
        manifest = _scenario(args.scenario)
    receipt = build_cockpit_component_contract_receipt(manifest=manifest, emitted_at=args.emitted_at)
    errors = validate_cockpit_component_contract_receipt(receipt)
    if args.write:
        path = write_cockpit_component_contract_receipt(args.workspace_root, receipt)
        print(f"receipt_path: {path}")
    print(format_cockpit_component_contract_summary(receipt))
    if errors:
        print("errors:")
        for error in errors:
            print(f"- {error}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
