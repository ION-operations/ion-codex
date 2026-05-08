"""ION V103 temporal/context enforcement reconciliation audit.

The audit exists to prevent a specific false diagnosis: claiming ION lacks
advanced temporal/context systems when the real defect is missing wiring or
enforcement across those systems.

It performs no mutation.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

TEMPORAL_PROTOCOLS = (
    "ION/02_architecture/ORCHESTRATION_TEMPORAL_RELEVANCE_PROTOCOL.md",
    "ION/02_architecture/TEMPORAL_CONTEXT_LEASE_PROTOCOL.md",
    "ION/02_architecture/RUNTIME_REPORT_TEMPORAL_PROVENANCE_PROTOCOL.md",
    "ION/02_architecture/RUNTIME_REPORT_BIDIRECTIONAL_TEMPORAL_PROTOCOL.md",
    "ION/02_architecture/SCHEDULE_LINEAGE_AND_SUPERSESSION_ARCHIVAL_PROTOCOL.md",
    "ION/02_architecture/SCHEDULE_LINEAGE_REPLAY_AND_ACTIVE_CYCLE_RECONSTRUCTION_PROTOCOL.md",
    "ION/02_architecture/SCHEDULE_RESUME_BUNDLE_MATERIALIZATION_PROTOCOL.md",
    "ION/02_architecture/CONTEXT_PERFECT_CONTINUATION_PROTOCOL.md",
    "ION/02_architecture/ION_AGENT_CONTEXT_DYNAMICS_AND_CONTEXT_WINDOW_PROTOCOL.md",
    "ION/02_architecture/ION_COMPILED_ROLE_CONTEXT_BUNDLE_INVARIANT_PROTOCOL.md",
    "ION/02_architecture/ION_AGENT_CONTEXT_CONTINUITY_TIMELINE_AND_ROUTE_MAP_PROTOCOL.md",
    "ION/02_architecture/ION_CONTEXT_METABOLISM_AND_LIFECYCLE_PROTOCOL.md",
    "ION/02_architecture/ION_TEMPORAL_CONTEXT_ENFORCEMENT_RECONCILIATION_PROTOCOL.md",
)

TEMPORAL_KERNEL_SURFACES = (
    "ION/04_packages/kernel/temporal_evaluator.py",
    "ION/04_packages/kernel/temporal_leases.py",
    "ION/04_packages/kernel/temporal_model.py",
    "ION/04_packages/kernel/temporal_object_adapters.py",
    "ION/04_packages/kernel/temporal_receipts.py",
    "ION/04_packages/kernel/temporal_reconciliation.py",
    "ION/04_packages/kernel/temporal_relevance.py",
    "ION/04_packages/kernel/schedule_lineage.py",
    "ION/04_packages/kernel/schedule_lineage_replay.py",
    "ION/04_packages/kernel/schedule_resume_bundle.py",
    "ION/04_packages/kernel/schedule_resume_projection.py",
    "ION/04_packages/kernel/context_compiler.py",
    "ION/04_packages/kernel/ion_agent_context_dynamics.py",
    "ION/04_packages/kernel/ion_compiled_role_context_bundle_audit.py",
    "ION/04_packages/kernel/ion_context_lifecycle.py",
    "ION/04_packages/kernel/ion_autonomous_loop.py",
)

REPORT_REL = Path("ION/05_context/current/TEMPORAL_CONTEXT_ENFORCEMENT_AUDIT_V103.json")
SIGNAL_REL = Path("ION/05_context/signals/v103_temporal_context_enforcement_reconciliation_receipt_20260502.txt")

LIFECYCLE_PACKAGING_GATE_SURFACES = (
    "ION/04_packages/kernel/ion_lifecycle_packager.py",
    "ION/03_registry/ion_lifecycle_package_manifest.schema.json",
    "ION/tests/test_kernel_ion_lifecycle_packager.py",
)


@dataclass(frozen=True)
class SurfaceCheck:
    rel_path: str
    exists: bool
    category: str


@dataclass(frozen=True)
class TemporalContextEnforcementAudit:
    schema_id: str
    line: str
    emitted_at: str
    scanned_root: str
    protocol_surface_count: int
    protocol_surface_present_count: int
    kernel_surface_count: int
    kernel_surface_present_count: int
    autonomous_loop_binds_context_lifecycle: bool
    autonomous_loop_writes_context_lifecycle_report: bool
    lifecycle_policy_present: bool
    lifecycle_report_present: bool
    temporal_tests_present_count: int
    context_lifecycle_tests_present: bool
    packaging_gate_present: bool
    mutation_performed: bool
    verdict: str
    findings: tuple[str, ...]
    surfaces: tuple[SurfaceCheck, ...] = field(default_factory=tuple)


def _shell_root(path: str | Path) -> Path:
    p = Path(path).expanduser().resolve()
    return p.parent if p.name == "ION" else p


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _lifecycle_packaging_gate_present(shell: Path) -> bool:
    """Detect the current V106 lifecycle-aware package gate by contract, not name alone."""
    gate_path = shell / "ION/04_packages/kernel/ion_lifecycle_packager.py"
    gate_text = _text(gate_path)
    gate_contract_tokens = (
        "build_context_lifecycle_report",
        "excluded_forensic_context",
        "COMPACT_RUNTIME",
        "FORENSIC_ARCHIVE",
        "audit_zip_root",
    )
    if gate_path.is_file() and all(token in gate_text for token in gate_contract_tokens):
        return True

    # Backward-compatible detection for older candidate release packagers.
    for rel in (
        "ION/04_packages/kernel/release_candidate_builder.py",
        "ION/04_packages/kernel/ion_release_packager.py",
        "ION/04_packages/kernel/ion_carrier_package_builder.py",
    ):
        path = shell / rel
        if path.exists() and "context_lifecycle" in _text(path).lower():
            return True
    return False


def build_temporal_context_enforcement_audit(root: str | Path, *, emitted_at: str | None = None) -> TemporalContextEnforcementAudit:
    shell = _shell_root(root)
    surfaces: list[SurfaceCheck] = []
    for rel in TEMPORAL_PROTOCOLS:
        surfaces.append(SurfaceCheck(rel_path=rel, exists=(shell / rel).is_file(), category="protocol"))
    for rel in TEMPORAL_KERNEL_SURFACES:
        surfaces.append(SurfaceCheck(rel_path=rel, exists=(shell / rel).is_file(), category="kernel"))
    for rel in LIFECYCLE_PACKAGING_GATE_SURFACES:
        surfaces.append(SurfaceCheck(rel_path=rel, exists=(shell / rel).is_file(), category="lifecycle_packaging_gate"))

    protocol_present = sum(1 for item in surfaces if item.category == "protocol" and item.exists)
    kernel_present = sum(1 for item in surfaces if item.category == "kernel" and item.exists)

    loop_text = _text(shell / "ION/04_packages/kernel/ion_autonomous_loop.py")
    autonomous_loop_binds_context_lifecycle = "build_context_lifecycle_report" in loop_text and "context_lifecycle_report_to_dict" in loop_text
    autonomous_loop_writes_context_lifecycle_report = "write_context_lifecycle_report" in loop_text

    tests_root = shell / "ION/tests"
    temporal_tests_present = 0
    context_lifecycle_tests_present = False
    if tests_root.exists():
        for item in tests_root.glob("test_kernel_*.py"):
            name = item.name.lower()
            if "temporal" in name or "schedule" in name:
                temporal_tests_present += 1
            if "context_lifecycle" in name:
                context_lifecycle_tests_present = True

    lifecycle_policy_present = (shell / "ION/03_registry/context_lifecycle_policy.yaml").is_file()
    lifecycle_report_present = (shell / "ION/05_context/current/CONTEXT_LIFECYCLE_AUDIT_V102.json").is_file()

    # V106 promoted lifecycle packaging from a planned release-packager idea into
    # a current compact-runtime/forensic-archive package boundary.
    packaging_gate_present = _lifecycle_packaging_gate_present(shell)

    findings: list[str] = []
    if protocol_present < len(TEMPORAL_PROTOCOLS) - 1:
        findings.append("temporal_context_protocol_surfaces_missing")
    else:
        findings.append("temporal_context_protocol_surfaces_present")
    if kernel_present < len(TEMPORAL_KERNEL_SURFACES):
        findings.append("temporal_context_kernel_surfaces_missing")
    else:
        findings.append("temporal_context_kernel_surfaces_present")
    if autonomous_loop_binds_context_lifecycle and autonomous_loop_writes_context_lifecycle_report:
        findings.append("autonomous_loop_bound_to_context_lifecycle_audit")
    else:
        findings.append("autonomous_loop_not_bound_to_context_lifecycle_audit")
    if temporal_tests_present == 0:
        findings.append("temporal_kernel_specific_tests_absent_in_current_compact_branch")
    if not packaging_gate_present:
        findings.append("carrier_release_packaging_gate_not_yet_bound_to_context_lifecycle")
    else:
        findings.append("carrier_release_packaging_gate_bound_to_context_lifecycle")
    if lifecycle_policy_present and context_lifecycle_tests_present:
        findings.append("context_lifecycle_policy_and_tests_present")

    if "autonomous_loop_not_bound_to_context_lifecycle_audit" in findings:
        verdict = "SYSTEM_PRESENT_BUT_NOT_ENFORCED"
    elif not packaging_gate_present or temporal_tests_present == 0:
        verdict = "SYSTEM_PRESENT_AND_PARTIALLY_ENFORCED"
    else:
        verdict = "SYSTEM_PRESENT_AND_ENFORCED"

    return TemporalContextEnforcementAudit(
        schema_id="ion.temporal_context_enforcement_audit.v1",
        line="V103_TEMPORAL_CONTEXT_ENFORCEMENT_RECONCILIATION",
        emitted_at=emitted_at or _now(),
        scanned_root=shell.as_posix(),
        protocol_surface_count=len(TEMPORAL_PROTOCOLS),
        protocol_surface_present_count=protocol_present,
        kernel_surface_count=len(TEMPORAL_KERNEL_SURFACES),
        kernel_surface_present_count=kernel_present,
        autonomous_loop_binds_context_lifecycle=autonomous_loop_binds_context_lifecycle,
        autonomous_loop_writes_context_lifecycle_report=autonomous_loop_writes_context_lifecycle_report,
        lifecycle_policy_present=lifecycle_policy_present,
        lifecycle_report_present=lifecycle_report_present,
        temporal_tests_present_count=temporal_tests_present,
        context_lifecycle_tests_present=context_lifecycle_tests_present,
        packaging_gate_present=packaging_gate_present,
        mutation_performed=False,
        verdict=verdict,
        findings=tuple(findings),
        surfaces=tuple(surfaces),
    )


def audit_to_dict(audit: TemporalContextEnforcementAudit) -> dict[str, Any]:
    return asdict(audit)


def write_temporal_context_enforcement_audit(root: str | Path, audit: TemporalContextEnforcementAudit | None = None) -> Path:
    shell = _shell_root(root)
    audit = audit or build_temporal_context_enforcement_audit(shell)
    out = shell / REPORT_REL
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit_to_dict(audit), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    signal = shell / SIGNAL_REL
    signal.parent.mkdir(parents=True, exist_ok=True)
    signal.write_text(
        "V103 temporal context enforcement reconciliation receipt\n"
        f"verdict: {audit.verdict}\n"
        f"protocol_surface_present_count: {audit.protocol_surface_present_count}/{audit.protocol_surface_count}\n"
        f"kernel_surface_present_count: {audit.kernel_surface_present_count}/{audit.kernel_surface_count}\n"
        f"autonomous_loop_binds_context_lifecycle: {audit.autonomous_loop_binds_context_lifecycle}\n"
        f"packaging_gate_present: {audit.packaging_gate_present}\n"
        "mutation_performed: false\n",
        encoding="utf-8",
    )
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Audit ION temporal/context enforcement wiring.")
    parser.add_argument("--ion-root", default=".")
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    audit = build_temporal_context_enforcement_audit(args.ion_root)
    if args.write_report:
        write_temporal_context_enforcement_audit(args.ion_root, audit)
    if args.json:
        print(json.dumps(audit_to_dict(audit), indent=2, sort_keys=True))
    else:
        print(f"ION_TEMPORAL_CONTEXT_ENFORCEMENT_{audit.verdict}")
        for finding in audit.findings:
            print(f"- {finding}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
