"""ION V105 deep operational cartography audit.

This audit is deliberately broader than the V104 operational-truth pass. It maps
core ION systems as living operational surfaces: whether doctrine exists,
whether kernel/runtime code exists, whether tests exist, whether active-state
artifacts exist, and whether the system is actually wired into the next-run
surface. It does not grant production authority and it does not move evidence.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

REPORT_REL = Path("ION/05_context/current/ION_DEEP_OPERATIONAL_CARTOGRAPHY_AUDIT_V105.json")
PLAN_REL = Path("ION/05_context/current/ION_LONG_HORIZON_ORCHESTRATION_PLAN_V105.json")
TELEMETRY_REL = Path("ION/05_context/current/ION_CORE_SYSTEM_TELEMETRY_REQUIREMENTS_V105.json")
CARRIER_PLAN_REL = Path("ION/05_context/current/CARRIER_AGENT_SYSTEM_BUILD_PLAN_V105.json")
SIGNAL_REL = Path("ION/05_context/signals/v105_deep_operational_cartography_receipt_20260502.txt")

@dataclass(frozen=True)
class RequiredSurface:
    rel_path: str
    role: str = "required"

@dataclass(frozen=True)
class SystemFinding:
    system_id: str
    verdict: str
    severity: str
    summary: str
    present: tuple[str, ...] = field(default_factory=tuple)
    missing: tuple[str, ...] = field(default_factory=tuple)
    disconnected: tuple[str, ...] = field(default_factory=tuple)
    next_required: tuple[str, ...] = field(default_factory=tuple)

@dataclass(frozen=True)
class DeepOperationalCartographyAudit:
    schema_id: str
    line: str
    emitted_at: str
    scanned_root: str
    production_authority: bool
    verdict: str
    ready_count: int
    partial_count: int
    missing_count: int
    blocked_count: int
    systems: tuple[SystemFinding, ...]


def _shell_root(path: str | Path) -> Path:
    p = Path(path).expanduser().resolve()
    return p.parent if p.name == "ION" else p


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _exists(root: Path, rel: str) -> bool:
    return (root / rel).exists()


def _json(root: Path, rel: str) -> dict[str, Any]:
    path = root / rel
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except Exception:
        return {}


def _split(root: Path, surfaces: Iterable[str]) -> tuple[tuple[str, ...], tuple[str, ...]]:
    present: list[str] = []
    missing: list[str] = []
    for rel in surfaces:
        (present if _exists(root, rel) else missing).append(rel)
    return tuple(present), tuple(missing)


def _finding(system_id: str, root: Path, required: Iterable[str], *, summary_ready: str, summary_partial: str, severity: str = "warning", disconnected: Iterable[str] = (), next_required: Iterable[str] = ()) -> SystemFinding:
    present, missing = _split(root, required)
    dis = tuple(disconnected)
    nxt = tuple(next_required)
    if not missing and not dis:
        verdict = "READY_SURFACE_PRESENT"
        sev = "info"
        summary = summary_ready
    elif len(present) == 0:
        verdict = "MISSING_SURFACE"
        sev = "blocking"
        summary = f"{summary_partial} No required surfaces were found."
    else:
        verdict = "PARTIAL_OR_DISCONNECTED"
        sev = severity
        summary = summary_partial
    return SystemFinding(system_id=system_id, verdict=verdict, severity=sev, summary=summary, present=present, missing=missing, disconnected=dis, next_required=nxt)


def _cursor_subagent_files(root: Path) -> list[str]:
    base = root / ".cursor/agents"
    if not base.exists():
        return []
    return sorted(str(p.relative_to(root)) for p in base.glob("ion-*.md"))


def _current_files(root: Path) -> set[str]:
    base = root / "ION/05_context/current"
    if not base.exists():
        return set()
    return {str(p.relative_to(root)) for p in base.rglob("*") if p.is_file()}


def build_deep_operational_cartography(root: str | Path, *, emitted_at: str | None = None) -> DeepOperationalCartographyAudit:
    shell = _shell_root(root)
    timestamp = emitted_at or _now()
    systems: list[SystemFinding] = []
    current_files = _current_files(shell)

    systems.append(_finding(
        "root_authority_and_mount_invariant",
        shell,
        (
            "pyproject.toml",
            "ION/REPO_AUTHORITY.md",
            "ION/02_architecture/ION_MOUNT_CONTRACT.md",
            "ION/02_architecture/ION_CARRIER_ONBOARDING_AUTHORITY_PROTOCOL.md",
            "ION/03_registry/codex_extension_carrier_profile.yaml",
            "ION/07_templates/carriers/CARRIER_MOUNT_PROOF.md",
            "ION/07_templates/carriers/CARRIER_SESSION_PACKET.md",
        ),
        summary_ready="Shell root, mount contract, and registry/template carrier onboarding authority are physically present.",
        summary_partial="Root/mount authority is incomplete.",
        next_required=("every carrier must prove pyproject.toml + ION/REPO_AUTHORITY.md and mount through registry/profile/template surfaces before running kernel modules",),
    ))

    systems.append(_finding(
        "temporal_context_stack",
        shell,
        (
            "ION/02_architecture/TEMPORAL_CONTEXT_LEASE_PROTOCOL.md",
            "ION/02_architecture/TRIPLE_TIME_RECONCILIATION_PROTOCOL.md",
            "ION/02_architecture/ORCHESTRATION_TEMPORAL_RELEVANCE_PROTOCOL.md",
            "ION/04_packages/kernel/temporal_model.py",
            "ION/04_packages/kernel/temporal_leases.py",
            "ION/04_packages/kernel/temporal_relevance.py",
            "ION/04_packages/kernel/temporal_reconciliation.py",
            "ION/04_packages/kernel/ion_temporal_context_enforcement_audit.py",
            "ION/tests/test_kernel_ion_temporal_context_enforcement_audit.py",
        ),
        summary_ready="Temporal/context doctrine, kernel adapters, enforcement audit, and focused test are present.",
        summary_partial="Temporal/context stack exists but is not completely surfaced.",
        next_required=("promote temporal checks from audit/report into packaging, front-door, and worker-adapter gates",),
    ))

    systems.append(_finding(
        "context_lifecycle_and_metabolism",
        shell,
        (
            "ION/02_architecture/ION_CONTEXT_METABOLISM_AND_LIFECYCLE_PROTOCOL.md",
            "ION/03_registry/context_lifecycle_policy.yaml",
            "ION/04_packages/kernel/ion_context_lifecycle.py",
            "ION/tests/test_kernel_ion_context_lifecycle.py",
            "ION/05_context/current/CONTEXT_LIFECYCLE_AUDIT_V102.json",
        ),
        summary_ready="Context lifecycle audit and policy surfaces are present.",
        summary_partial="Context lifecycle/metabolism is incomplete.",
        disconnected=("release/carrier packaging still needs hard lifecycle binding",),
        next_required=("build compact runtime package + forensic archive package from lifecycle classifications",),
    ))

    systems.append(_finding(
        "local_autonomous_loop_survival_path",
        shell,
        (
            "ION/02_architecture/ION_LOCAL_AUTONOMOUS_LOOP_SURVIVAL_PROTOCOL.md",
            "ION/04_packages/kernel/ion_autonomous_loop.py",
            "ION/04_packages/kernel/ion_template_action_gate.py",
            "ION/04_packages/kernel/ion_steward_integrate.py",
            "ION/tests/test_kernel_ion_autonomous_loop.py",
            "ION/tests/test_kernel_ion_template_action_gate.py",
            "ION/tests/test_kernel_ion_steward_integrate.py",
        ),
        summary_ready="Local deterministic autonomous-loop survival path exists with proof gates and tests.",
        summary_partial="Local autonomous-loop survival path is incomplete.",
        disconnected=("external workers intentionally remain blocked until bounded adapter gate exists",),
        next_required=("keep deterministic local loop as floor; attach workers only through proof-gated adapter",),
    ))

    systems.append(_finding(
        "active_agent_context_systems",
        shell,
        (
            "ION/02_architecture/ION_AGENT_CONTEXT_SYSTEMS_PROTOCOL.md",
            "ION/02_architecture/ION_AGENT_CONTEXT_DYNAMICS_AND_CONTEXT_WINDOW_PROTOCOL.md",
            "ION/04_packages/kernel/ion_agent_context_systems.py",
            "ION/04_packages/kernel/ion_agent_context_dynamics.py",
            "ION/05_context/current/ACTIVE_AGENT_CONTEXT_WINDOW_PLAN.json",
            "ION/05_context/current/agent_context_systems/STEWARD.context_system.md",
            "ION/05_context/current/agent_context_systems/CONTEXT_CARTOGRAPHER.context_system.md",
            "ION/05_context/current/agent_context_systems/RUNTIME_CARTOGRAPHER.context_system.md",
        ),
        summary_ready="Agent context-system and rolling context-window surfaces are present.",
        summary_partial="Agent context-system wiring is incomplete.",
        next_required=("regenerate role context packages from registry + filesystem before every serious carrier run",),
    ))

    systems.append(_finding(
        "front_door_persona_relay_steward_runtime",
        shell,
        (
            "ION/02_architecture/FRONT_DOOR_PERSONA_RELAY_STEWARD_BOUNDARY_PROTOCOL.md",
            "ION/02_architecture/FRONT_DOOR_RUNTIME_ENTRY_PROTOCOL.md",
            "ION/02_architecture/ION_FRONT_DOOR_AUTONOMOUS_TEAM_WORKFLOW_PROTOCOL.md",
            "ION/04_packages/kernel/front_door_chat_orchestration.py",
            "ION/04_packages/kernel/front_door_runtime_entry.py",
            "ION/04_packages/kernel/ion_front_door_proof_trace.py",
            "ION/03_registry/ion_front_door_proof_trace.schema.json",
            "ION/08_ui/joc_cockpit_shell/FrontDoorProofTracePanel.tsx",
            "ION/tests/test_kernel_ion_front_door_proof_trace.py",
            "ION/05_context/current/ACTIVE_FRONT_DOOR_PROOF_TRACE.json",
            "ION/05_context/current/ACTIVE_FRONT_DOOR_TEAM_PLAN.json",
        ),
        summary_ready="Front-door Persona/Relay/Steward runtime proof trace surfaces are present.",
        summary_partial="Front-door deterministic proof trace exists; live host binding remains incomplete.",
        disconnected=("deterministic proof trace exists; live front-door host/SSE/DB binding remains unproven",),
        next_required=("bind a real operator host message through the same proof trace and UI hydration path",),
    ))

    receipt_required = (
        "ION/02_architecture/FRONT_STAGE_COUNCIL_RUNTIME_RECEIPT_PROTOCOL.md",
        "ION/02_architecture/CONVERSATIONAL_RECEIPT_AND_LIVE_REPAIR_PROTOCOL.md",
        "ION/04_packages/kernel/front_stage_council_receipt.py",
        "ION/04_packages/kernel/conversational_receipt.py",
        "ION/04_packages/kernel/ion_receipt_hydration_mapper.py",
        "ION/03_registry/ion_receipt_hydration_view_model.schema.json",
        "ION/08_ui/joc_cockpit_shell/ReceiptHydrationPanel.tsx",
        "ION/tests/test_kernel_ion_receipt_hydration_mapper.py",
    )
    receipt_disconnected = []
    if not _exists(shell, "ION/04_packages/kernel/ion_receipt_hydration_mapper.py"):
        receipt_disconnected.append("no verified assistant-bubble hydration mapper for mixed utterance_id/atom_id cases")
    if not _exists(shell, "ION/tests/test_kernel_ion_receipt_hydration_mapper.py"):
        receipt_disconnected.append("no mixed utterance_id/atom_id hydration tests")
    if not receipt_disconnected:
        receipt_disconnected.append("receipt hydration mapper is fixture/JSON-adapter ready; live DB query binding remains unproven")
    systems.append(_finding(
        "receipt_repair_and_hydration_mapping",
        shell,
        receipt_required,
        summary_ready="Receipt and conversational repair hydration surfaces are present.",
        summary_partial="Receipt/repair hydration exists but live DB binding is not proven.",
        disconnected=tuple(receipt_disconnected),
        next_required=(
            "bind receipt hydration mapper to the real DB/SSE adapter when that surface is present",
            "keep conflict/unresolved receipt warnings visible in UI instead of attaching by recency",
        ),
    ))

    ui_required = (
        "ION/08_ui/joc_cockpit_shell/ionRuntimeCockpitTypes.ts",
        "ION/08_ui/joc_cockpit_shell/RuntimeStatusPanel.tsx",
        "ION/08_ui/joc_cockpit_shell/LaneTimelinePanel.tsx",
        "ION/08_ui/joc_cockpit_shell/ReceiptHydrationPanel.tsx",
        "ION/08_ui/joc_cockpit_shell/RuntimeDebugOverlayPanel.tsx",
        "ION/09_integrations/cursor_extension/src/webviews/cockpit/CockpitWebviewProvider.ts",
        "ION/04_packages/kernel/ion_cockpit_view_model.py",
        "ION/04_packages/kernel/ion_lane_timeline_view_model.py",
        "ION/04_packages/kernel/ion_receipt_hydration_mapper.py",
        "ION/04_packages/kernel/ion_runtime_debug_overlay.py",
        "ION/tests/test_kernel_ion_cockpit_view_model.py",
        "ION/tests/test_kernel_ion_lane_timeline_view_model.py",
        "ION/tests/test_kernel_ion_receipt_hydration_mapper.py",
        "ION/tests/test_kernel_ion_runtime_debug_overlay.py",
    )
    ui_disconnected = []
    if not _exists(shell, "ION/08_ui/joc_cockpit_shell/LaneTimelinePanel.tsx"):
        ui_disconnected.append("lane timeline widget missing: requested/effective lane changes and lane/organ events per message")
    if not _exists(shell, "ION/08_ui/joc_cockpit_shell/ReceiptHydrationPanel.tsx"):
        ui_disconnected.append("receipt hydration widget missing: receipt/repair mapping per assistant bubble")
    if not _exists(shell, "ION/08_ui/joc_cockpit_shell/RuntimeDebugOverlayPanel.tsx"):
        ui_disconnected.append("debug overlay missing: SSE throughput, render timings, DB hydration time")
    if not _exists(shell, "ION/04_packages/kernel/ion_runtime_debug_overlay.py"):
        ui_disconnected.append("kernel telemetry projection missing: throughput/render/hydration metrics schema")
    if not ui_disconnected:
        ui_disconnected.append("lane timeline, receipt hydration, and debug overlay surfaces are present; live SSE/DB adapters remain projected/not-connected until host integration proves them")
    systems.append(_finding(
        "joc_cockpit_ui_and_core_telemetry",
        shell,
        ui_required,
        summary_ready="JOC/cockpit view model and basic UI surfaces are present.",
        summary_partial="JOC/cockpit telemetry overlays exist but live host adapters are not fully proven.",
        disconnected=tuple(ui_disconnected),
        next_required=(
            "bind LaneTimelinePanel to live front-door lane events beyond active-packet projection",
            "bind receipt hydration integrity view to the real assistant-bubble DB adapter",
            "bind RuntimeDebugOverlay to live SSE/render/DB hydration timings",
        ),
    ))

    cursor_subagents = _cursor_subagent_files(shell)
    cursor_disconnected = []
    if not cursor_subagents:
        cursor_disconnected.append("Cursor subagent carrier slot files missing")
    if not _exists(shell, "ION/09_integrations/cursor_extension/src/ionCommands.ts"):
        cursor_disconnected.append("Cursor extension command surface missing")
    if not _exists(shell, "ION/04_packages/kernel/ion_codex_extension_carrier_audit.py"):
        cursor_disconnected.append("Codex extension carrier audit missing")
    else:
        codex_audit = _json(shell, "ION/05_context/current/CODEX_EXTENSION_CARRIER_AUDIT_V106.json")
        if codex_audit.get("verdict") != "ION_CODEX_EXTENSION_CARRIER_READY":
            cursor_disconnected.append("Codex extension carrier audit not ready")
        else:
            cursor_disconnected.append("Codex extension carrier is mounted as tool-assisted; host-native subagents remain unproven")
    systems.append(_finding(
        "cursor_carrier_and_codex_extension_surface",
        shell,
        (
            "ION/04_agents/carriers/CURSOR_CARRIER.profile.md",
            "ION/04_agents/carriers/CODEX_CARRIER.profile.md",
            "ION/02_architecture/CODEX_EXTENSION_CARRIER_PROTOCOL.md",
            "ION/02_architecture/ION_OVER_CURSOR_PROTOCOL.md",
            "ION/02_architecture/CODEX_LEAD_ORCHESTRATION_PROTOCOL.md",
            "ION/03_registry/codex_extension_carrier_profile.yaml",
            ".cursor/commands/ion.md",
            ".cursor/agents/ion-spawn-row-slot.md",
            "ION/09_integrations/cursor_extension/package.json",
            "ION/07_templates/carriers/CODEX_EXTENSION_EXECUTION_PACKET.md",
            "ION/04_packages/kernel/ion_codex_extension_carrier_audit.py",
            "ION/tests/test_kernel_ion_codex_extension_carrier_audit.py",
            "ION/05_context/current/CODEX_EXTENSION_CARRIER_AUDIT_V106.json",
        ),
        summary_ready="Cursor/Codex carrier doctrine, commands, subagent carrier slots, and extension scaffold are present.",
        summary_partial="Cursor/Codex carrier surfaces exist but host-native spawn proof remains bounded.",
        disconnected=tuple(cursor_disconnected),
        next_required=("validate Codex returns through carrier task return intake and keep host-native subagents gated by spawn proof",),
    ))

    mcp_donor_audit = _json(shell, "ION/05_context/current/V108_V72_MCP_DONOR_RECONCILIATION_AUDIT.json")
    mcp_donor_disconnected = []
    if mcp_donor_audit.get("reconciliation_verdict") != "V72_MCP_DONOR_RECONCILIATION_PASS":
        mcp_donor_disconnected.append("V72 MCP donor reconciliation audit is missing or not passing")
    if mcp_donor_audit.get("forbidden_runtime_file_count", 0):
        mcp_donor_disconnected.append("old V72 runtime receipts were restored into hot runtime state")
    if not mcp_donor_disconnected:
        mcp_donor_disconnected.append("V72 MCP substrate is restored and current Cursor MCP bridge is preserved; live MCP execution authority remains bounded and unclaimed")
    systems.append(_finding(
        "v72_mcp_donor_reconciliation_and_current_bridge",
        shell,
        (
            "ION/00_BOOTSTRAP/V108_V72_MCP_DONOR_RECONCILIATION_LOCK.md",
            "ION/02_architecture/ION_V72_MCP_DONOR_RECONCILIATION_PROTOCOL.md",
            "ION/03_registry/ion_v72_mcp_donor_reconciliation_audit.schema.json",
            "ION/04_packages/kernel/ion_v72_mcp_donor_reconciliation_audit.py",
            "ION/tests/test_kernel_ion_v72_mcp_donor_reconciliation_audit.py",
            "ION/05_context/current/V108_V72_MCP_DONOR_RECONCILIATION_AUDIT.json",
            "ION/04_packages/kernel/ion_mcp_local_bridge.py",
            "ION/04_packages/kernel/ion_mcp_client_certification.py",
            "ION/04_packages/kernel/ion_mcp_transport_preview.py",
            "ION/04_packages/kernel/ion_mcp_bridge_audit.py",
            "ION/09_integrations/mcp/ion_mcp_server.py",
        ),
        summary_ready="V72 MCP donor substrate and current Cursor MCP bridge reconciliation surfaces are present.",
        summary_partial="V72 MCP donor reconciliation exists but requires review.",
        disconnected=tuple(mcp_donor_disconnected),
        next_required=(
            "keep V72 donor runtime receipts out of hot trunk unless explicitly promoted through archive/donor manifests",
            "bind restored MCP substrate to live MCP operation only through mount-session, budget, and receipt gates",
        ),
    ))

    systems.append(_finding(
        "chatgpt_browser_carrier_surface",
        shell,
        (
            "ION/04_agents/carriers/CHATGPT_CARRIER.profile.md",
            "ION/04_agents/carriers/MANUAL_CARRIER.profile.md",
            "ION/04_agents/carriers/carrier_registry.json",
            "ION/07_templates/carriers/CARRIER_CAPABILITY_SURVEY.md",
            "ION/07_templates/carriers/CARRIER_MOUNT_PROOF.md",
        ),
        summary_ready="ChatGPT browser carrier starts from explicit Manual/L1 profile and survey law.",
        summary_partial="ChatGPT carrier profile is incomplete.",
        disconnected=("normal ChatGPT browser cannot claim real subagents; needs an active-session mount proof and one-artifact/full-zip discipline",),
        next_required=("create ChatGPT Browser Carrier operating packet for this project line",),
    ))

    systems.append(_finding(
        "template_graph_evolution_and_writeback_metabolism",
        shell,
        (
            "ION/02_architecture/EVENTED_TEMPLATE_FILE_GRAPH_PROTOCOL.md",
            "ION/02_architecture/TEMPLATE_EVENT_REACTION_PIPELINE_PROTOCOL.md",
            "ION/04_packages/kernel/template_graph_writeback_proposals.py",
            "ION/04_packages/kernel/template_graph_writeback_review.py",
            "ION/04_packages/kernel/template_graph_commit.py",
            "ION/04_packages/kernel/template_contract_registry.py",
        ),
        summary_ready="Template graph proposal/review/commit surfaces are present.",
        summary_partial="Template graph evolution surfaces are incomplete.",
        disconnected=("writeback proposals need diff/residue lifecycle so full graph snapshots do not become hot context",),
        next_required=("add proposal corpus synthesis + accepted diff residue generation",),
    ))

    release_disconnected = []
    if not _exists(shell, "ION/04_packages/kernel/ion_lifecycle_packager.py"):
        release_disconnected.append("no lifecycle-aware full-project/compact-runtime/forensic-archive packager is yet hard-bound")
    else:
        compact_manifest = _json(shell, "ION/05_context/current/LIFECYCLE_PACKAGE_MANIFEST_COMPACT_RUNTIME_V106.json")
        if compact_manifest.get("zip_creation_performed") and (compact_manifest.get("zip_root_audit") or {}).get("verdict") == "ZIP_ROOT_CONFIRMED":
            release_disconnected.append("compact runtime zip materialization is proven; full-project and forensic archive package approvals remain bounded")
        else:
            release_disconnected.append("lifecycle package root-integrity gate is present; package materialization has not been proven")

    systems.append(_finding(
        "release_packaging_and_productized_runtime_boundary",
        shell,
        (
            "ION/02_architecture/ION_PRODUCTIZED_RUNTIME_BOUNDARY_PROTOCOL.md",
            "ION/02_architecture/ION_LIFECYCLE_AWARE_PACKAGE_ROOT_INTEGRITY_PROTOCOL.md",
            "ION/03_registry/ion_lifecycle_package_manifest.schema.json",
            "ION/05_context/current/ION_RUNTIME_SEPARATION_PLAN_V99.json",
            "ION/05_context/current/PRODUCTIZED_RUNTIME_MANIFEST_V104.json",
            "ION/04_packages/kernel/ion_lifecycle_packager.py",
            "ION/06_artifacts/packages",
            "ION/04_packages/kernel/release_readiness.py",
            "ION/04_packages/kernel/summary_refresh_demo_release_candidate_verify.py",
            "ION/tests/test_kernel_ion_lifecycle_packager.py",
        ),
        summary_ready="Runtime/productization boundary surfaces are present.",
        summary_partial="Release/productized runtime boundary is incomplete.",
        disconnected=tuple(release_disconnected),
        next_required=("extend lifecycle package materialization into operator-approved full-project and forensic archive receipts",),
    ))

    systems.append(_finding(
        "model_router_budget_and_provider_economics",
        shell,
        (
            "ION/02_architecture/MODEL_ROUTER_AND_COST_QUALITY_ROUTING_PROTOCOL.md",
            "ION/02_architecture/BUDGET_AND_API_RATE_GOVERNORS_PROTOCOL.md",
            "ION/04_packages/kernel/model_router.py",
            "ION/04_packages/kernel/cost_quality_router.py",
            "ION/04_packages/kernel/budget_governor.py",
            "ION/04_packages/kernel/api_rate_governor.py",
        ),
        summary_ready="Model routing, cost-quality, budget, and rate-governor surfaces are present.",
        summary_partial="Model routing/economics stack is incomplete.",
        disconnected=("provider adapters remain planning/view-model surfaces until real API call receipts exist",),
        next_required=("bind provider selection to call receipts and budget/rate governors before external API operation",),
    ))

    systems.append(_finding(
        "visual_browser_and_computer_use_lane",
        shell,
        (
            "ION/02_architecture/VISUAL_PERCEPTION_AND_INTERACTION_AGENT_PROTOCOL.md",
            "ION/02_architecture/VISUAL_CLOSURE_GRAPH_PROJECTION_AND_UI_WORK_SURFACE_PROTOCOL.md",
            "ION/04_packages/kernel/local_browser_capture_adapter.py",
            "ION/04_packages/kernel/local_browser_execution_harness.py",
            "ION/04_packages/kernel/local_visual_harness.py",
            "ION/04_packages/kernel/visual_before_after_verification.py",
        ),
        summary_ready="Visual/browser harness and verification surfaces are present.",
        summary_partial="Visual/browser lane is incomplete.",
        disconnected=("visual/computer-use authority remains bounded; no unrestricted action lane is production-ratified",),
        next_required=("wire visual receipts into cockpit timeline and front-stage claim receipts",),
    ))

    ready_count = sum(1 for s in systems if s.verdict == "READY_SURFACE_PRESENT")
    partial_count = sum(1 for s in systems if s.verdict == "PARTIAL_OR_DISCONNECTED")
    missing_count = sum(1 for s in systems if s.verdict == "MISSING_SURFACE")
    blocked_count = sum(1 for s in systems if s.severity == "blocking")
    verdict = "DEEP_CARTOGRAPHY_PREPARED_WITH_DISCONNECTED_SYSTEMS" if partial_count or missing_count else "DEEP_CARTOGRAPHY_READY_SURFACES_PRESENT"

    return DeepOperationalCartographyAudit(
        schema_id="ion.deep_operational_cartography.v105",
        line="V105_DEEP_OPERATIONAL_CARTOGRAPHY_AND_CORE_SYSTEM_TELEMETRY",
        emitted_at=timestamp,
        scanned_root=str(shell),
        production_authority=False,
        verdict=verdict,
        ready_count=ready_count,
        partial_count=partial_count,
        missing_count=missing_count,
        blocked_count=blocked_count,
        systems=tuple(systems),
    )


def audit_to_dict(audit: DeepOperationalCartographyAudit) -> dict[str, Any]:
    return asdict(audit)


def build_long_horizon_plan(audit: DeepOperationalCartographyAudit) -> dict[str, Any]:
    return {
        "schema_id": "ion.long_horizon_orchestration_plan.v105",
        "line": audit.line,
        "created_at": audit.emitted_at,
        "production_authority": False,
        "true_north": "Make ION operational by proving every core system as wired runtime, not merely doctrine or isolated modules.",
        "current_verdict": audit.verdict,
        "phase_order": [
            {
                "phase": "P0_system_cartography_floor",
                "status": "active",
                "exit_condition": "deep operational cartography audit runs and names disconnected systems without false production claims",
            },
            {
                "phase": "P1_lifecycle_aware_packaging",
                "status": "next",
                "exit_condition": "full project, compact runtime, and forensic archive packages are emitted with lifecycle receipts and exclusions made explicit",
            },
            {
                "phase": "P2_front_door_receipt_hydration_and_lane_telemetry",
                "status": "next",
                "exit_condition": "operator messages have lane/organ timelines, requested/effective lane transitions, receipt hydration mapping, and debug timing overlays",
            },
            {
                "phase": "P3_carrier_mounts_chatgpt_cursor_codex",
                "status": "next",
                "exit_condition": "ChatGPT browser, Cursor, and Codex extension each have mount proof, capability survey, return intake, and stop conditions",
            },
            {
                "phase": "P4_bounded_worker_adapter",
                "status": "blocked_until_P1_P3",
                "exit_condition": "external/local workers cannot return without context proof, template action proof, lifecycle check, and Steward integration",
            },
            {
                "phase": "P5_template_graph_and_context_metabolism",
                "status": "planned",
                "exit_condition": "template graph writebacks and execution cycles produce compact residues and archive raw evidence without deleting proof",
            },
            {
                "phase": "P6_release_candidate_and_production_namespace",
                "status": "planned",
                "exit_condition": "production gates are separate from branch versions and release verifier can explain all blocks",
            },
        ],
        "open_work": [
            {
                "id": "V105-OW-001",
                "priority": "P0",
                "title": "Keep deep operational cartography as living status object",
                "owner_role": "RUNTIME_CARTOGRAPHER+NEMESIS",
                "exit_condition": "audit is regenerated before major branches and blocks false latest-state claims",
            },
            {
                "id": "V105-OW-002",
                "priority": "P0",
                "title": "Implement UI telemetry triad",
                "owner_role": "MASON+PERSONA_INTERFACE",
                "exit_condition": "lane timeline, receipt hydration mapper, and runtime debug overlay are visible/tested",
            },
            {
                "id": "V105-OW-003",
                "priority": "P0",
                "title": "Lifecycle-aware packaging",
                "owner_role": "MASON+ATLAS",
                "exit_condition": "package generator distinguishes hot runtime from forensic history by policy",
            },
            {
                "id": "V105-OW-004",
                "priority": "P0",
                "title": "Carrier setup for ChatGPT browser, Cursor, and Codex extension",
                "owner_role": "RUNTIME_CARTOGRAPHER+STEWARD",
                "exit_condition": "each carrier has profile, mount proof, survey, command path, return intake, and no-theatre constraints",
            },
            {
                "id": "V105-OW-005",
                "priority": "P1",
                "title": "Front-door runtime proof",
                "owner_role": "RELAY+STEWARD+PERSONA_INTERFACE",
                "exit_condition": "one operator message routes to Relay packet, Steward verdict, Persona output, and receipts",
            },
            {
                "id": "V105-OW-006",
                "priority": "P1",
                "title": "Template graph writeback metabolism",
                "owner_role": "TEMPLATE_CURATOR+ATLAS",
                "exit_condition": "writeback proposals are summarized into accepted diffs/residues rather than full hot snapshots",
            },
        ],
    }


def build_core_telemetry_requirements(emitted_at: str) -> dict[str, Any]:
    return {
        "schema_id": "ion.core_system_telemetry_requirements.v105",
        "created_at": emitted_at,
        "production_authority": False,
        "origin_operator_request": "Implement lane timeline, receipt/repair hydration, and debug performance overlays; generalize that instrumentation discipline across all core ION systems.",
        "requirements": [
            {
                "id": "TEL-001",
                "name": "lane_timeline_widget",
                "status": "required_not_implemented",
                "must_show": [
                    "message_id",
                    "requested_lane",
                    "effective_lane",
                    "lane_change_reason",
                    "organ_events",
                    "authority_verdict",
                    "repair_obligations",
                ],
                "applies_to": ["front_door", "persona", "relay", "steward", "visual", "worker_adapter"],
            },
            {
                "id": "TEL-002",
                "name": "receipt_repair_hydration_mapper",
                "status": "required_not_implemented",
                "must_prove": [
                    "latest DB/source receipts map to the correct assistant bubble",
                    "mixed utterance_id and atom_id cases are deterministic",
                    "repair receipts supersede stale claim receipts without orphaning history",
                ],
                "applies_to": ["front_stage_council_receipts", "conversational_repair", "joc_cockpit", "persona_output"],
            },
            {
                "id": "TEL-003",
                "name": "runtime_debug_overlay",
                "status": "required_not_implemented",
                "must_show": ["SSE event throughput", "render timings", "DB hydration time", "kernel projection time", "file watcher refresh time"],
                "applies_to": ["joc_cockpit", "cursor_extension", "front_door", "future_browser_chat_surface"],
            },
            {
                "id": "TEL-004",
                "name": "core_system_health_overlay",
                "status": "planned",
                "must_show": ["system verdict", "wired vs doctrine-only", "latest receipt", "next gate", "latency/cost/size where measurable"],
                "applies_to": ["all core systems in ion.deep_operational_cartography.v105"],
            },
        ],
    }


def build_carrier_agent_system_plan(emitted_at: str) -> dict[str, Any]:
    return {
        "schema_id": "ion.carrier_agent_system_build_plan.v105",
        "created_at": emitted_at,
        "production_authority": False,
        "principle": "Carrier powers scale only with proof. ChatGPT browser, Cursor, Codex, and MCP are transport hosts, not ION identity.",
        "carriers": [
            {
                "carrier": "CHATGPT_BROWSER",
                "current_floor": "L1 in this session only if file inspection and zip creation are proven; no real subagents claimed",
                "needed_next": [
                    "active-session mount proof",
                    "one-artifact full project zip return rule",
                    "lead-dev context control surface update after each pass",
                    "explicit no-real-subagent claim unless host exposes and proves them",
                ],
            },
            {
                "carrier": "CURSOR_IDE",
                "current_floor": "L1/L2 candidate: command/rules/subagent slot surfaces exist but require live host proof",
                "needed_next": [
                    "run /ion health/audit from actual Cursor root",
                    "capture spawn row transcript or subagent result packet",
                    "return intake through kernel.ion_carrier_task_return",
                    "JOC cockpit refresh proof",
                ],
            },
            {
                "carrier": "CODEX_EXTENSION_IN_CURSOR",
                "current_floor": "L1/L2 candidate: Codex profile exists; extension-specific mount proof not yet complete",
                "needed_next": [
                    "Codex extension command path inventory",
                    "Codex bounded execution packet template",
                    "Codex return-to-current-carrier receipt",
                    "test/diff proof capture",
                ],
            },
            {
                "carrier": "MCP_RUNTIME",
                "current_floor": "L4 candidate only when callable ION MCP tools prove operation schemas and receipts",
                "needed_next": ["tool schema proof", "call proof", "journal/receipt path", "manual fallback template"],
            },
        ],
    }


def write_outputs(root: str | Path, audit: DeepOperationalCartographyAudit) -> None:
    shell = _shell_root(root)
    data = audit_to_dict(audit)
    for rel, value in (
        (REPORT_REL, data),
        (PLAN_REL, build_long_horizon_plan(audit)),
        (TELEMETRY_REL, build_core_telemetry_requirements(audit.emitted_at)),
        (CARRIER_PLAN_REL, build_carrier_agent_system_plan(audit.emitted_at)),
    ):
        path = shell / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    signal = shell / SIGNAL_REL
    signal.parent.mkdir(parents=True, exist_ok=True)
    signal.write_text(
        "V105 deep operational cartography emitted. Production authority: false. "
        f"Verdict: {audit.verdict}. Ready={audit.ready_count}; partial={audit.partial_count}; missing={audit.missing_count}; blocked={audit.blocked_count}.\n",
        encoding="utf-8",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build ION V105 deep operational cartography audit.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    audit = build_deep_operational_cartography(args.ion_root)
    if args.write:
        write_outputs(args.ion_root, audit)
    if args.json:
        print(json.dumps(audit_to_dict(audit), indent=2, sort_keys=True))
    else:
        print(f"ION_DEEP_OPERATIONAL_CARTOGRAPHY_{audit.verdict}")
    return 0 if audit.blocked_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
