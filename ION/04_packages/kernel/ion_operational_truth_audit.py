"""ION V104 operational truth audit.

This module inspects whether the current compact ION branch has coherent wiring
between active state, context systems, lifecycle/temporal enforcement, carrier
packaging, and long-horizon orchestration. It is audit-first: it records truth
without granting production authority.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .ion_context_lifecycle import build_context_lifecycle_report, context_lifecycle_report_to_dict
from .ion_temporal_context_enforcement_audit import build_temporal_context_enforcement_audit, audit_to_dict as temporal_audit_to_dict

REPORT_REL = Path("ION/05_context/current/ION_OPERATIONAL_TRUTH_AUDIT_V104.json")
SIGNAL_REL = Path("ION/05_context/signals/v104_operational_truth_audit_receipt_20260502.txt")

ACTIVE_STATE_FILES = (
    "ION/05_context/current/ACTIVE_WORK_PACKET.json",
    "ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json",
    "ION/05_context/current/ACTIVE_AGENT_CONTEXT_WINDOW_PLAN.json",
    "ION/05_context/current/ACTIVE_COCKPIT_VIEW_MODEL.json",
    "ION/05_context/current/ACTIVE_HUMAN_GATE_QUEUE.json",
    "ION/05_context/current/ACTIVE_STEWARD_INTEGRATION_QUEUE.json",
)

REQUIRED_SURVIVAL_MODULES = (
    "ION/04_packages/kernel/ion_autonomous_loop.py",
    "ION/04_packages/kernel/ion_template_action_gate.py",
    "ION/04_packages/kernel/ion_steward_integrate.py",
    "ION/04_packages/kernel/ion_context_lifecycle.py",
    "ION/04_packages/kernel/ion_temporal_context_enforcement_audit.py",
)

REQUIRED_ROLE_CONTEXT_SYSTEMS = (
    "STEWARD",
    "VIZIER",
    "MASON",
    "RELAY",
    "PERSONA_INTERFACE",
    "ATLAS",
    "VESTIGE",
    "NEMESIS",
    "VICE",
    "SCRIBE",
    "THOTH",
    "TEMPLATE_CURATOR",
    "CONTEXT_CARTOGRAPHER",
    "RUNTIME_CARTOGRAPHER",
    "CANON_LIBRARIAN",
    "IONOLOGIST",
)

@dataclass(frozen=True)
class OperationalCheck:
    check_id: str
    status: str
    severity: str
    summary: str
    evidence: tuple[str, ...] = field(default_factory=tuple)
    required_next: tuple[str, ...] = field(default_factory=tuple)

@dataclass(frozen=True)
class OperationalTruthAudit:
    schema_id: str
    line: str
    emitted_at: str
    scanned_root: str
    production_authority: bool
    verdict: str
    pass_count: int
    repair_applied_count: int
    open_blocker_count: int
    warning_count: int
    checks: tuple[OperationalCheck, ...]


def _shell_root(path: str | Path) -> Path:
    p = Path(path).expanduser().resolve()
    return p.parent if p.name == "ION" else p


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, dict) else {}
    except json.JSONDecodeError:
        return {}


def _walk_missing_path_flags(value: Any, root: Path) -> tuple[list[str], list[str]]:
    stale_missing_flags: list[str] = []
    true_missing_flags: list[str] = []
    def walk(x: Any) -> None:
        if isinstance(x, dict):
            if "path" in x and x.get("exists") is False:
                rel = str(x["path"])
                if (root / rel).exists():
                    stale_missing_flags.append(rel)
                else:
                    true_missing_flags.append(rel)
            for v in x.values():
                walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(value)
    return stale_missing_flags, true_missing_flags


def _role_context_path(role: str) -> str:
    return f"ION/05_context/current/agent_context_systems/{role}.context_system.md"


def build_operational_truth_audit(root: str | Path, *, emitted_at: str | None = None) -> OperationalTruthAudit:
    shell = _shell_root(root)
    timestamp = emitted_at or _now()
    checks: list[OperationalCheck] = []

    root_invariant = (shell / "pyproject.toml").is_file() and (shell / "ION/REPO_AUTHORITY.md").is_file()
    checks.append(OperationalCheck(
        check_id="root_invariant",
        status="PASS" if root_invariant else "BLOCKER",
        severity="blocking" if not root_invariant else "info",
        summary="Shell root contains pyproject.toml and ION/REPO_AUTHORITY.md." if root_invariant else "Shell root invariant is broken.",
        evidence=("pyproject.toml", "ION/REPO_AUTHORITY.md"),
        required_next=() if root_invariant else ("mount from the real shell root before running kernel modules",),
    ))

    missing_active = tuple(rel for rel in ACTIVE_STATE_FILES if not (shell / rel).is_file())
    checks.append(OperationalCheck(
        check_id="active_state_surface",
        status="PASS" if not missing_active else "BLOCKER",
        severity="blocking" if missing_active else "info",
        summary="Required active state files are present." if not missing_active else "Required active state files are missing.",
        evidence=missing_active or ACTIVE_STATE_FILES,
        required_next=() if not missing_active else ("rebuild active state from bootstrap/onboard surfaces",),
    ))

    work_packet = _json(shell / "ION/05_context/current/ACTIVE_WORK_PACKET.json")
    active_template = str(work_packet.get("active_template", ""))
    active_template_exists = bool(active_template and (shell / active_template).is_file())
    packet_flag = work_packet.get("active_template_exists")
    if active_template_exists and packet_flag is True:
        status = "PASS"
        summary = "Active carrier work-cycle template exists and ACTIVE_WORK_PACKET agrees."
        req: tuple[str, ...] = ()
        severity = "info"
    elif active_template_exists and packet_flag is False:
        status = "WARNING"
        summary = "Active carrier work-cycle template exists but ACTIVE_WORK_PACKET has a stale false flag."
        req = ("regenerate ACTIVE_WORK_PACKET from the template registry",)
        severity = "warning"
    else:
        status = "BLOCKER"
        summary = "Active carrier work-cycle template is missing."
        req = ("create or repoint ION/docs/cursor/ION_CURSOR_WORK_CYCLE_PACKET.md",)
        severity = "blocking"
    checks.append(OperationalCheck(
        check_id="active_work_template_binding",
        status=status,
        severity=severity,
        summary=summary,
        evidence=(active_template or "<no active_template>", f"active_template_exists_field={packet_flag!r}"),
        required_next=req,
    ))

    context_window = _json(shell / "ION/05_context/current/ACTIVE_AGENT_CONTEXT_WINDOW_PLAN.json")
    stale_missing, true_missing = _walk_missing_path_flags(context_window, shell)
    # Legacy MINI/CAPSULE paths may be intentionally missing and optional; they are not counted as blockers here.
    nonlegacy_true_missing = tuple(path for path in true_missing if "/MINI.md" not in path and "/CAPSULE.md" not in path and not path.endswith("/STATUS.md") and "ION/05_context/inbox/" not in path)
    if stale_missing:
        checks.append(OperationalCheck(
            check_id="context_window_stale_existence_flags",
            status="WARNING",
            severity="warning",
            summary="Generated context-window plan marks existing surfaces as missing.",
            evidence=tuple(stale_missing[:25]),
            required_next=("regenerate ACTIVE_AGENT_CONTEXT_WINDOW_PLAN from current filesystem and role registry",),
        ))
    else:
        checks.append(OperationalCheck(
            check_id="context_window_stale_existence_flags",
            status="PASS",
            severity="info",
            summary="No stale false existence flags remain in the active context-window plan.",
            evidence=(),
            required_next=(),
        ))
    checks.append(OperationalCheck(
        check_id="context_window_true_missing_required_surfaces",
        status="PASS" if not nonlegacy_true_missing else "BLOCKER",
        severity="blocking" if nonlegacy_true_missing else "info",
        summary="No non-legacy required context-window paths are missing." if not nonlegacy_true_missing else "Non-legacy context-window paths are missing.",
        evidence=nonlegacy_true_missing,
        required_next=() if not nonlegacy_true_missing else ("repair missing required context surfaces or downgrade them to route-deeper optional surfaces",),
    ))

    missing_role_systems = []
    empty_role_systems = []
    for role in REQUIRED_ROLE_CONTEXT_SYSTEMS:
        rel = _role_context_path(role)
        path = shell / rel
        if not path.is_file():
            missing_role_systems.append(rel)
        elif path.stat().st_size == 0:
            empty_role_systems.append(rel)
    role_status = "PASS" if not missing_role_systems and not empty_role_systems else "BLOCKER"
    checks.append(OperationalCheck(
        check_id="role_context_system_completeness",
        status=role_status,
        severity="blocking" if role_status == "BLOCKER" else "info",
        summary="Required role context-system cards exist and are non-empty." if role_status == "PASS" else "Role context-system cards are missing or empty.",
        evidence=tuple(missing_role_systems + empty_role_systems),
        required_next=() if role_status == "PASS" else ("materialize missing/empty role context-system cards before trusting spawn plans",),
    ))

    missing_modules = tuple(rel for rel in REQUIRED_SURVIVAL_MODULES if not (shell / rel).is_file())
    checks.append(OperationalCheck(
        check_id="local_survival_loop_modules",
        status="PASS" if not missing_modules else "BLOCKER",
        severity="blocking" if missing_modules else "info",
        summary="Local autonomous loop, template gate, Steward integration, lifecycle, and temporal audit modules exist." if not missing_modules else "Required local survival modules are missing.",
        evidence=missing_modules or REQUIRED_SURVIVAL_MODULES,
        required_next=() if not missing_modules else ("restore V101-V103 local survival modules",),
    ))

    temporal = temporal_audit_to_dict(build_temporal_context_enforcement_audit(shell, emitted_at=timestamp))
    packaging_gate_present = bool(temporal.get("packaging_gate_present"))
    checks.append(OperationalCheck(
        check_id="context_lifecycle_temporal_enforcement",
        status="PASS" if temporal.get("verdict") in {"SYSTEM_PRESENT_AND_ENFORCED", "SYSTEM_PRESENT_AND_PARTIALLY_ENFORCED"} else "BLOCKER",
        severity="warning" if temporal.get("verdict") == "SYSTEM_PRESENT_AND_PARTIALLY_ENFORCED" else "info",
        summary=f"Temporal/context enforcement audit verdict: {temporal.get('verdict')}",
        evidence=tuple(temporal.get("findings", ())),
        required_next=("bind release/carrier packaging to context lifecycle before large forensic branches are zipped as hot runtime",) if not packaging_gate_present else (),
    ))

    lifecycle = context_lifecycle_report_to_dict(build_context_lifecycle_report(shell, emitted_at=timestamp))
    checks.append(OperationalCheck(
        check_id="context_lifecycle_size_posture",
        status="PASS" if lifecycle.get("verdict") == "PASS_WITH_LIFECYCLE_MODEL" else "WARNING",
        severity="warning" if lifecycle.get("verdict") != "PASS_WITH_LIFECYCLE_MODEL" else "info",
        summary=f"Context lifecycle audit verdict: {lifecycle.get('verdict')}; total_context_bytes={lifecycle.get('total_context_bytes')}",
        evidence=tuple(lifecycle.get("findings", ())),
        required_next=("classify or digest current-context artifacts that remain unclassified",) if lifecycle.get("verdict") != "PASS_WITH_LIFECYCLE_MODEL" else (),
    ))

    loop_text = (shell / "ION/04_packages/kernel/ion_autonomous_loop.py").read_text(encoding="utf-8", errors="replace") if (shell / "ION/04_packages/kernel/ion_autonomous_loop.py").exists() else ""
    # Keep this check explicit rather than clever: V101 intentionally proves a deterministic local worker first.
    external_adapter_bound = "worker_adapter" in loop_text or "executor_registry" in loop_text or "external_execution_bridge" in loop_text
    checks.append(OperationalCheck(
        check_id="worker_adapter_boundary",
        status="BLOCKED_BY_DESIGN" if not external_adapter_bound else "PASS",
        severity="warning" if not external_adapter_bound else "info",
        summary="Autonomous loop remains deterministic/local; external workers are intentionally not bound yet." if not external_adapter_bound else "Autonomous loop includes a worker-adapter binding surface.",
        evidence=("ION/04_packages/kernel/ion_autonomous_loop.py",),
        required_next=("implement a bounded worker-adapter interface after local loop and packaging gates remain stable",) if not external_adapter_bound else (),
    ))

    roadmap = _json(shell / "ION/05_context/current/ION_MASTER_OPERATIONAL_ROADMAP_V104.json")
    checks.append(OperationalCheck(
        check_id="long_horizon_operational_roadmap",
        status="PASS" if roadmap.get("schema_id") == "ion.master_operational_roadmap.v104" else "WARNING",
        severity="warning" if roadmap.get("schema_id") != "ion.master_operational_roadmap.v104" else "info",
        summary="V104 master operational roadmap is present." if roadmap.get("schema_id") == "ion.master_operational_roadmap.v104" else "V104 master operational roadmap has not been written yet.",
        evidence=("ION/05_context/current/ION_MASTER_OPERATIONAL_ROADMAP_V104.json",),
        required_next=() if roadmap.get("schema_id") == "ion.master_operational_roadmap.v104" else ("write the V104 long-horizon operational roadmap",),
    ))

    blocking_statuses = {"BLOCKER"}
    warning_statuses = {"WARNING", "BLOCKED_BY_DESIGN"}
    open_blocker_count = sum(1 for c in checks if c.status in blocking_statuses)
    warning_count = sum(1 for c in checks if c.status in warning_statuses)
    repair_applied_count = 0
    if work_packet.get("v104_template_reconnection"):
        repair_applied_count += 1
    if context_window.get("v104_context_window_plan_refresh", {}).get("refreshed_stale_existence_flags", 0):
        repair_applied_count += 1
    if (shell / "ION/05_context/current/agent_context_systems/IONOLOGIST.context_system.md").is_file():
        repair_applied_count += 1

    if open_blocker_count:
        verdict = "NOT_OPERATIONAL_READY_BLOCKERS_PRESENT"
    elif warning_count:
        verdict = "PARTIAL_OPERATIONAL_READY_WITH_OPEN_GATES"
    else:
        verdict = "OPERATIONAL_READY_FOR_NEXT_LOCAL_SURVIVAL_PASS"

    return OperationalTruthAudit(
        schema_id="ion.operational_truth_audit.v104",
        line="V104_OPERATIONAL_TRUTH_AUDIT_AND_LONG_HORIZON_ORCHESTRATION",
        emitted_at=timestamp,
        scanned_root=shell.as_posix(),
        production_authority=False,
        verdict=verdict,
        pass_count=sum(1 for c in checks if c.status == "PASS"),
        repair_applied_count=repair_applied_count,
        open_blocker_count=open_blocker_count,
        warning_count=warning_count,
        checks=tuple(checks),
    )


def audit_to_dict(audit: OperationalTruthAudit) -> dict[str, Any]:
    return asdict(audit)


def write_operational_truth_audit(root: str | Path, audit: OperationalTruthAudit | None = None) -> Path:
    shell = _shell_root(root)
    audit = audit or build_operational_truth_audit(shell)
    out = shell / REPORT_REL
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit_to_dict(audit), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    signal = shell / SIGNAL_REL
    signal.parent.mkdir(parents=True, exist_ok=True)
    signal.write_text(
        "V104 operational truth audit receipt\n"
        f"verdict: {audit.verdict}\n"
        f"pass_count: {audit.pass_count}\n"
        f"repair_applied_count: {audit.repair_applied_count}\n"
        f"open_blocker_count: {audit.open_blocker_count}\n"
        f"warning_count: {audit.warning_count}\n"
        "production_authority: false\n",
        encoding="utf-8",
    )
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit ION operational wiring and long-horizon readiness.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    audit = build_operational_truth_audit(args.ion_root)
    if args.write_report:
        write_operational_truth_audit(args.ion_root, audit)
    if args.json:
        print(json.dumps(audit_to_dict(audit), indent=2, sort_keys=True))
    else:
        print(f"ION_OPERATIONAL_TRUTH_{audit.verdict}")
        for check in audit.checks:
            print(f"- {check.check_id}: {check.status} — {check.summary}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
