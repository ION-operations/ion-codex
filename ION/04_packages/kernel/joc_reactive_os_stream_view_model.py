"""V57 ION/JOC reactive OS stream view-model verifier.

This module validates the runtime-facing view model that feeds the ION/JOC
cockpit Reactive OS Stream. It verifies loop coverage, event evidence, claim
lanes, visible blocked-capability boundaries, and non-authority posture.

It does not render a live UI, operate browser sessions, access credentials,
submit forms, mutate external pages, or grant production authority.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass, field, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

SCHEMA_ID = "ion.joc_reactive_os_stream_view_model.v1"
VERSION = "V57_REACTIVE_OS_STREAM_AND_AUTOMATION_VIEW_MODEL"
AUTHORITY_SCOPE = "REACTIVE_OS_STREAM_VIEW_MODEL_RECEIPT_ONLY"
DEFAULT_REPORT_DIR = "ION/05_context/history/joc_reactive_os_stream_view_model_receipts"

REQUIRED_LOOPS = (
    "VISUAL_ISSUE_CLOSURE_LOOP",
    "MISSION_DISPATCH_LOOP",
    "SESSION_HEALTH_LOOP",
    "CONTEXT_PROJECTION_LOOP",
    "CONVERSATIONAL_REPAIR_LOOP",
    "MODEL_COST_QUALITY_LOOP",
)

REQUIRED_RENDERED_SURFACES = (
    "REACTIVE_OS_STREAM",
    "CLAIM_AND_RECEIPT_RAIL",
    "VISUAL_EVIDENCE_LENS",
    "MISSION_DISPATCH_AND_MODEL_ROUTE_PANEL",
    "CONTEXT_GRAPH_COGNITIVE_EXPLORER",
    "CONVERSATIONAL_REPAIR_QUEUE",
    "BROWSER_SESSION_AUTOMATION_OVERLAY",
    "COMPUTE_AND_COST_ROUTER",
)

ALLOWED_STATUSES = ("OK", "WATCH", "BLOCKED", "REPAIR")
ALLOWED_CLAIM_LANES = ("C0", "C1", "C2", "C3", "C4", "C5")

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
class ReactiveOsStreamEvent:
    event_id: str
    occurred_at: str
    loop_id: str
    phase: str
    status: str
    claim_lane: str
    rendered_surface: str
    authority_scope: str
    evidence_refs: tuple[str, ...] = ()
    repair_required: bool = False
    blocked_capabilities: tuple[str, ...] = ()
    detail: str = ""


@dataclass(frozen=True)
class ReactiveOsStreamViewModel:
    schema_id: str
    version: str
    surface_name: str
    source_receipt_ids: tuple[str, ...]
    events: tuple[ReactiveOsStreamEvent, ...]
    forbidden_capabilities: dict[str, bool]
    dxl_constraints: dict[str, bool] = field(default_factory=dict)
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class ReactiveOsStreamViewModelReceipt:
    schema_id: str
    version: str
    receipt_id: str
    emitted_at: str
    surface_name: str
    authority_scope: str
    event_count: int
    loop_count: int
    rendered_surface_count: int
    loops_present: tuple[str, ...]
    missing_loops: tuple[str, ...]
    rendered_surfaces_present: tuple[str, ...]
    missing_rendered_surfaces: tuple[str, ...]
    event_ids_missing_evidence: tuple[str, ...]
    event_ids_with_invalid_status: tuple[str, ...]
    event_ids_with_invalid_claim_lane: tuple[str, ...]
    event_ids_with_unknown_loop: tuple[str, ...]
    event_ids_with_unknown_surface: tuple[str, ...]
    event_ids_requiring_repair: tuple[str, ...]
    blocked_capability_events: tuple[str, ...]
    forbidden_capability_violations: tuple[str, ...]
    source_receipt_ids: tuple[str, ...]
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


def build_reactive_os_stream_view_model_receipt(*, view_model: ReactiveOsStreamViewModel, emitted_at: str | None = None) -> ReactiveOsStreamViewModelReceipt:
    _validate_view_model_shape(view_model)

    loops_present = tuple(sorted({event.loop_id for event in view_model.events if event.loop_id in REQUIRED_LOOPS}))
    missing_loops = tuple(loop for loop in REQUIRED_LOOPS if loop not in loops_present)

    rendered_surfaces_present = tuple(sorted({event.rendered_surface for event in view_model.events if event.rendered_surface in REQUIRED_RENDERED_SURFACES}))
    missing_rendered_surfaces = tuple(surface for surface in REQUIRED_RENDERED_SURFACES if surface not in rendered_surfaces_present)

    event_ids_missing_evidence = tuple(
        event.event_id
        for event in view_model.events
        if not event.evidence_refs and not event.blocked_capabilities
    )
    event_ids_with_invalid_status = tuple(event.event_id for event in view_model.events if event.status not in ALLOWED_STATUSES)
    event_ids_with_invalid_claim_lane = tuple(event.event_id for event in view_model.events if event.claim_lane not in ALLOWED_CLAIM_LANES)
    event_ids_with_unknown_loop = tuple(event.event_id for event in view_model.events if event.loop_id not in REQUIRED_LOOPS)
    event_ids_with_unknown_surface = tuple(event.event_id for event in view_model.events if event.rendered_surface not in REQUIRED_RENDERED_SURFACES)
    event_ids_requiring_repair = tuple(event.event_id for event in view_model.events if event.repair_required or event.status == "REPAIR")
    blocked_capability_events = tuple(event.event_id for event in view_model.events if event.blocked_capabilities)

    forbidden_capability_violations = tuple(
        key for key, expected in FORBIDDEN_CAPABILITIES.items()
        if view_model.forbidden_capabilities.get(key) is not expected
    )
    unknown_event_capabilities = tuple(
        sorted({
            cap
            for event in view_model.events
            for cap in event.blocked_capabilities
            if cap not in FORBIDDEN_CAPABILITIES
        })
    )
    if unknown_event_capabilities:
        raise ValueError("unknown blocked capability keys: " + ", ".join(unknown_event_capabilities))

    findings: list[str] = list(view_model.notes)
    if missing_loops:
        findings.append("missing automation loop coverage: " + ", ".join(missing_loops))
    if missing_rendered_surfaces:
        findings.append("missing rendered surfaces: " + ", ".join(missing_rendered_surfaces))
    if event_ids_missing_evidence:
        findings.append("events missing evidence references: " + ", ".join(event_ids_missing_evidence))
    if event_ids_with_invalid_status:
        findings.append("events with invalid status: " + ", ".join(event_ids_with_invalid_status))
    if event_ids_with_invalid_claim_lane:
        findings.append("events with invalid claim lane: " + ", ".join(event_ids_with_invalid_claim_lane))
    if event_ids_with_unknown_loop:
        findings.append("events with unknown loop: " + ", ".join(event_ids_with_unknown_loop))
    if event_ids_with_unknown_surface:
        findings.append("events with unknown rendered surface: " + ", ".join(event_ids_with_unknown_surface))
    if event_ids_requiring_repair:
        findings.append("events requiring repair remain visible: " + ", ".join(event_ids_requiring_repair))
    if blocked_capability_events:
        findings.append("blocked capability events visible: " + ", ".join(blocked_capability_events))
    if forbidden_capability_violations:
        findings.append("forbidden capability violations: " + ", ".join(forbidden_capability_violations))
    if not view_model.source_receipt_ids:
        findings.append("no source receipt lineage attached")

    verdict = _verdict(
        missing_loops=missing_loops,
        missing_rendered_surfaces=missing_rendered_surfaces,
        missing_evidence=event_ids_missing_evidence,
        invalid_status=event_ids_with_invalid_status,
        invalid_claim_lane=event_ids_with_invalid_claim_lane,
        unknown_loop=event_ids_with_unknown_loop,
        unknown_surface=event_ids_with_unknown_surface,
        forbidden_capability_violations=forbidden_capability_violations,
        source_receipt_ids=view_model.source_receipt_ids,
    )
    emitted = emitted_at or _utc_now()
    rid = _stable_id(VERSION, view_model.surface_name, emitted, verdict)

    return ReactiveOsStreamViewModelReceipt(
        schema_id=SCHEMA_ID,
        version=VERSION,
        receipt_id=rid,
        emitted_at=emitted,
        surface_name=view_model.surface_name,
        authority_scope=AUTHORITY_SCOPE,
        event_count=len(view_model.events),
        loop_count=len(loops_present),
        rendered_surface_count=len(rendered_surfaces_present),
        loops_present=loops_present,
        missing_loops=missing_loops,
        rendered_surfaces_present=rendered_surfaces_present,
        missing_rendered_surfaces=missing_rendered_surfaces,
        event_ids_missing_evidence=event_ids_missing_evidence,
        event_ids_with_invalid_status=event_ids_with_invalid_status,
        event_ids_with_invalid_claim_lane=event_ids_with_invalid_claim_lane,
        event_ids_with_unknown_loop=event_ids_with_unknown_loop,
        event_ids_with_unknown_surface=event_ids_with_unknown_surface,
        event_ids_requiring_repair=event_ids_requiring_repair,
        blocked_capability_events=blocked_capability_events,
        forbidden_capability_violations=forbidden_capability_violations,
        source_receipt_ids=view_model.source_receipt_ids,
        findings=tuple(findings),
        verdict=verdict,
        recommended_next_actions=_actions(verdict),
        forbidden_capabilities=dict(FORBIDDEN_CAPABILITIES),
        production_authority=False,
        live_ui_claim=False,
        browser_control_authority=False,
        credential_access_authority=False,
        external_network_authority=False,
        persistent_dom_mutation_authority=False,
    )


def validate_reactive_os_stream_view_model_receipt(receipt: ReactiveOsStreamViewModelReceipt) -> tuple[str, ...]:
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
    if receipt.verdict == "VALID_REACTIVE_OS_STREAM_VIEW_MODEL" and (
        receipt.missing_loops
        or receipt.missing_rendered_surfaces
        or receipt.event_ids_missing_evidence
        or receipt.event_ids_with_invalid_status
        or receipt.event_ids_with_invalid_claim_lane
        or receipt.event_ids_with_unknown_loop
        or receipt.event_ids_with_unknown_surface
        or receipt.forbidden_capability_violations
    ):
        errors.append("valid verdict cannot include unresolved stream defects")
    return tuple(errors)


def load_view_model(workspace_root: str | Path, view_model_path: str | Path) -> ReactiveOsStreamViewModel:
    root = Path(workspace_root).resolve()
    path = _inside(root, view_model_path)
    return view_model_from_mapping(json.loads(path.read_text(encoding="utf-8")))


def view_model_from_mapping(data: Mapping[str, Any]) -> ReactiveOsStreamViewModel:
    def tup(name: str, default: Sequence[str] = ()) -> tuple[str, ...]:
        value = data.get(name, default)
        if value is None:
            return ()
        if isinstance(value, str):
            return (value,)
        return tuple(str(x) for x in value)

    events = tuple(_event_from_mapping(x) for x in data.get("events", ()))
    return ReactiveOsStreamViewModel(
        schema_id=str(data.get("schema_id") or ""),
        version=str(data.get("version") or ""),
        surface_name=str(data.get("surface_name") or ""),
        source_receipt_ids=tup("source_receipt_ids"),
        events=events,
        forbidden_capabilities={str(k): bool(v) for k, v in (data.get("forbidden_capabilities") or {}).items()},
        dxl_constraints={str(k): bool(v) for k, v in (data.get("dxl_constraints") or {}).items()},
        notes=tup("notes"),
    )


def write_reactive_os_stream_view_model_receipt(workspace_root: str | Path, receipt: ReactiveOsStreamViewModelReceipt, *, report_dir: str = DEFAULT_REPORT_DIR) -> Path:
    root = Path(workspace_root).resolve()
    out = root / report_dir
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{receipt.receipt_id}.joc_reactive_os_stream_view_model_receipt.json"
    path.write_text(json.dumps(_json(receipt), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def format_reactive_os_stream_summary(receipt: ReactiveOsStreamViewModelReceipt) -> str:
    return "\n".join([
        f"version: {receipt.version}",
        f"verdict: {receipt.verdict}",
        f"authority_scope: {receipt.authority_scope}",
        f"event_count: {receipt.event_count}",
        f"loop_count: {receipt.loop_count}",
        f"rendered_surface_count: {receipt.rendered_surface_count}",
        f"repair_visible: {len(receipt.event_ids_requiring_repair)}",
        f"blocked_capability_events: {len(receipt.blocked_capability_events)}",
        f"findings: {len(receipt.findings)}",
        f"production_authority: {receipt.production_authority}",
        f"live_ui_claim: {receipt.live_ui_claim}",
    ])


def _event_from_mapping(data: Mapping[str, Any]) -> ReactiveOsStreamEvent:
    def tup(name: str) -> tuple[str, ...]:
        value = data.get(name, ())
        if value is None:
            return ()
        if isinstance(value, str):
            return (value,)
        return tuple(str(x) for x in value)
    return ReactiveOsStreamEvent(
        event_id=str(data.get("event_id") or ""),
        occurred_at=str(data.get("occurred_at") or ""),
        loop_id=str(data.get("loop_id") or ""),
        phase=str(data.get("phase") or ""),
        status=str(data.get("status") or ""),
        claim_lane=str(data.get("claim_lane") or ""),
        rendered_surface=str(data.get("rendered_surface") or ""),
        authority_scope=str(data.get("authority_scope") or ""),
        evidence_refs=tup("evidence_refs"),
        repair_required=bool(data.get("repair_required", False)),
        blocked_capabilities=tup("blocked_capabilities"),
        detail=str(data.get("detail") or ""),
    )


def _validate_view_model_shape(view_model: ReactiveOsStreamViewModel) -> None:
    if view_model.schema_id != SCHEMA_ID:
        raise ValueError("schema_id must be " + SCHEMA_ID)
    if view_model.version != VERSION:
        raise ValueError("version must be " + VERSION)
    if not view_model.surface_name.strip():
        raise ValueError("surface_name is required")
    duplicate_events = _duplicates(event.event_id for event in view_model.events)
    if duplicate_events:
        raise ValueError("duplicate event ids: " + ", ".join(duplicate_events))
    unknown_forbidden = tuple(k for k in view_model.forbidden_capabilities if k not in FORBIDDEN_CAPABILITIES)
    if unknown_forbidden:
        raise ValueError("unknown forbidden capability keys: " + ", ".join(sorted(unknown_forbidden)))


def _verdict(*, missing_loops: Sequence[str], missing_rendered_surfaces: Sequence[str], missing_evidence: Sequence[str], invalid_status: Sequence[str], invalid_claim_lane: Sequence[str], unknown_loop: Sequence[str], unknown_surface: Sequence[str], forbidden_capability_violations: Sequence[str], source_receipt_ids: Sequence[str]) -> str:
    if forbidden_capability_violations:
        return "REACTIVE_OS_STREAM_BLOCKED_FOR_AUTHORITY_OVERREACH"
    if invalid_status or invalid_claim_lane or unknown_loop or unknown_surface:
        return "REACTIVE_OS_STREAM_VIEW_MODEL_INVALID_EVENT"
    if missing_loops or missing_rendered_surfaces:
        return "REACTIVE_OS_STREAM_VIEW_MODEL_INCOMPLETE"
    if missing_evidence:
        return "REACTIVE_OS_STREAM_VIEW_MODEL_NEEDS_EVIDENCE_REPAIR"
    if not source_receipt_ids:
        return "REACTIVE_OS_STREAM_VIEW_MODEL_NEEDS_RECEIPT_LINEAGE"
    return "VALID_REACTIVE_OS_STREAM_VIEW_MODEL"


def _actions(verdict: str) -> tuple[str, ...]:
    if verdict == "VALID_REACTIVE_OS_STREAM_VIEW_MODEL":
        return (
            "wire this view model into the cockpit shell fixture",
            "add visual screenshot validation for the rendered stream",
            "bind live receipt files instead of static fixture events",
            "keep blocked capability events visible until Steward/VZ escalation exists",
        )
    if verdict == "REACTIVE_OS_STREAM_BLOCKED_FOR_AUTHORITY_OVERREACH":
        return ("set forbidden capability flags back to false", "route escalation through Steward/VZ")
    if verdict == "REACTIVE_OS_STREAM_VIEW_MODEL_INVALID_EVENT":
        return ("repair invalid loop/status/claim-lane/rendered-surface fields before rendering",)
    if verdict == "REACTIVE_OS_STREAM_VIEW_MODEL_INCOMPLETE":
        return ("add required automation loop and rendered surface coverage",)
    if verdict == "REACTIVE_OS_STREAM_VIEW_MODEL_NEEDS_EVIDENCE_REPAIR":
        return ("attach evidence references to non-blocked automation events",)
    return ("attach V54/V55/V56 source receipt lineage",)


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


def _scenario(name: str) -> ReactiveOsStreamViewModel:
    fixture = view_model_from_mapping(json.loads(Path("ION/05_context/fixtures/ui/v57_reactive_os_stream_view_model.valid.json").read_text(encoding="utf-8")))
    if name == "valid":
        return fixture
    if name == "missing_loop":
        return replace(fixture, events=tuple(e for e in fixture.events if e.loop_id != "MODEL_COST_QUALITY_LOOP"))
    if name == "missing_evidence":
        broken = tuple(replace(e, evidence_refs=()) if e.status != "BLOCKED" else e for e in fixture.events)
        return replace(fixture, events=broken)
    if name == "overreach":
        return replace(fixture, forbidden_capabilities={**fixture.forbidden_capabilities, "credential_access": True})
    if name == "invalid_event":
        broken = tuple(replace(e, status="DONE") if e.event_id == "v57-evt-context-001" else e for e in fixture.events)
        return replace(fixture, events=broken)
    if name == "no_lineage":
        return replace(fixture, source_receipt_ids=())
    raise ValueError(f"unknown scenario: {name}")


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build V57 ION/JOC reactive OS stream view-model receipt.")
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--view-model", default=None)
    parser.add_argument("--scenario", default="valid")
    parser.add_argument("--emitted-at", default=None)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    if args.view_model:
        view_model = load_view_model(args.workspace_root, args.view_model)
    else:
        view_model = _scenario(args.scenario)
    receipt = build_reactive_os_stream_view_model_receipt(view_model=view_model, emitted_at=args.emitted_at)
    errors = validate_reactive_os_stream_view_model_receipt(receipt)
    if args.write:
        path = write_reactive_os_stream_view_model_receipt(args.workspace_root, receipt)
        print(f"receipt_path: {path}")
    print(format_reactive_os_stream_summary(receipt))
    if errors:
        print("errors:")
        for error in errors:
            print(f"- {error}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
