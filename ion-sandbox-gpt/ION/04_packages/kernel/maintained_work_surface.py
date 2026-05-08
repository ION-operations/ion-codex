"""V40 Maintained Work Surface and Persona-System canon inspection.

This module records the doctrine/runtime-planning surfaces introduced by V40:
maintained workflow canon, representational integrity, front-stage council,
Persona context budgeting, expressive telemetry, live provisional speech, and
visual perception/interaction agent planning.

It is an inspection/report surface only. It does not grant production authority.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

SCHEMA_ID = "ion.maintained_work_surface.v1"
VERSION = "V40_MAINTAINED_WORK_SURFACE_AND_PERSONA_SYSTEM_CANON"
DEFAULT_REPORT_DIR = "ION/05_context/history/maintained_work_surface_reports"

REQUIRED_SURFACES: tuple[str, ...] = (
    "ION/00_BOOTSTRAP/V40_MAINTAINED_WORK_SURFACE_AND_PERSONA_SYSTEM_LOCK.md",
    "ION/01_doctrine/MAINTAINED_WORK_SURFACE_CANON.md",
    "ION/02_architecture/REPRESENTATIONAL_INTEGRITY_PROTOCOL.md",
    "ION/02_architecture/FRONT_STAGE_COUNCIL_PROTOCOL.md",
    "ION/02_architecture/PERSONA_CONTEXT_BUDGET_AND_HORIZON_PROTOCOL.md",
    "ION/02_architecture/EXPRESSIVE_TELEMETRY_AND_AFFECT_INTEGRITY_PROTOCOL.md",
    "ION/02_architecture/LIVE_PERSONA_LATENCY_AND_PROVISIONAL_UTTERANCE_PROTOCOL.md",
    "ION/02_architecture/VISUAL_PERCEPTION_AND_INTERACTION_AGENT_PROTOCOL.md",
    "ION/03_registry/maintained_work_surface.schema.json",
    "ION/03_registry/maintained_work_surface_canon.yaml",
    "ION/03_registry/front_stage_council_policy.yaml",
    "ION/03_registry/expressive_telemetry_policy.yaml",
    "ION/03_registry/live_persona_latency_policy.yaml",
    "ION/03_registry/visual_perception_agent_policy.yaml",
    "ION/04_packages/kernel/maintained_work_surface.py",
    "ION/tests/test_kernel_maintained_work_surface.py",
)

COMPONENTS: tuple[str, ...] = (
    "maintained_work_surface_canon",
    "representational_integrity",
    "front_stage_council",
    "persona_context_budget_and_horizon",
    "expressive_telemetry_and_affect_integrity",
    "live_persona_latency_and_provisional_utterance",
    "visual_perception_and_interaction_agent",
)

FORBIDDEN_CLAIMS: dict[str, bool] = {
    "persona_is_total_ion": False,
    "persona_may_emit_high_impact_claim_alone": False,
    "affect_is_lived_human_emotion": False,
    "provisional_speech_is_ratified_truth": False,
    "visual_agent_unrestricted_computer_control": False,
    "v40_grants_production_authority": False,
}

@dataclass(frozen=True)
class MaintainedWorkSurfaceReport:
    schema_id: str
    version: str
    emitted_at: str
    workspace_root: str
    verdict: str
    production_authority: bool
    components: tuple[str, ...]
    required_surfaces: tuple[str, ...]
    missing_surfaces: tuple[str, ...]
    universal_workflow_grammar: tuple[str, ...]
    front_stage_council_roles: dict[str, str]
    live_persona_lanes: dict[str, str]
    visual_agent_modes: tuple[str, ...]
    forbidden_claims: dict[str, bool]


def generate_maintained_work_surface_report(workspace_root: str | Path, *, emitted_at: str | None = None) -> MaintainedWorkSurfaceReport:
    root = Path(workspace_root).resolve()
    timestamp = emitted_at or _utc_now()
    missing = tuple(rel for rel in REQUIRED_SURFACES if not (root / rel).exists())
    verdict = "VALID_V40_MAINTAINED_WORK_SURFACE_CANON" if not missing else "INCOMPLETE_V40_MAINTAINED_WORK_SURFACE_CANON"
    return MaintainedWorkSurfaceReport(
        schema_id=SCHEMA_ID,
        version=VERSION,
        emitted_at=timestamp,
        workspace_root=root.as_posix(),
        verdict=verdict,
        production_authority=False,
        components=COMPONENTS,
        required_surfaces=REQUIRED_SURFACES,
        missing_surfaces=missing,
        universal_workflow_grammar=("pressure", "synthesis", "evidence", "recognition", "formalization", "receipt", "continuation"),
        front_stage_council_roles={
            "persona": "relationship_horizon_expression",
            "relay": "context_transport_provenance_freshness",
            "steward_vz": "authority_risk_claim_class_work_legitimacy",
        },
        live_persona_lanes={
            "L0": "backchannel",
            "L1": "conversational_provisional",
            "L2": "checked_response",
            "L3": "ratified_answer",
            "L4": "formal_artifact",
        },
        visual_agent_modes=("OBSERVE", "DIAGNOSE", "COMPARE", "NAVIGATE", "TEST", "EXPLAIN", "PATCH_REQUEST", "VERIFY"),
        forbidden_claims=dict(FORBIDDEN_CLAIMS),
    )


def validate_maintained_work_surface_report(report: MaintainedWorkSurfaceReport, workspace_root: str | Path | None = None) -> tuple[str, ...]:
    errors: list[str] = []
    if report.schema_id != SCHEMA_ID:
        errors.append("schema_id mismatch")
    if report.production_authority:
        errors.append("V40 must not grant production authority")
    for claim, allowed in report.forbidden_claims.items():
        if allowed is not False:
            errors.append(f"forbidden claim {claim!r} must be false")
    if "persona" not in report.front_stage_council_roles or "steward_vz" not in report.front_stage_council_roles:
        errors.append("front-stage council must include Persona and Steward/VZ roles")
    if "OBSERVE" not in report.visual_agent_modes or "VERIFY" not in report.visual_agent_modes:
        errors.append("visual agent modes must include OBSERVE and VERIFY")
    if report.missing_surfaces:
        errors.append("missing required surfaces: " + ", ".join(report.missing_surfaces))
    if workspace_root is not None:
        root = Path(workspace_root).resolve()
        for rel in report.required_surfaces:
            if not (root / rel).exists():
                errors.append(f"required surface absent from workspace: {rel}")
    return tuple(errors)


def write_maintained_work_surface_report(workspace_root: str | Path, report: MaintainedWorkSurfaceReport) -> Path:
    root = Path(workspace_root).resolve()
    out_dir = root / DEFAULT_REPORT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{_stable_id('maintained-work-surface', report.version, report.emitted_at)}.json"
    path.write_text(json.dumps(asdict(report), indent=2, sort_keys=True), encoding="utf-8")
    return path


def format_maintained_work_surface_summary(report: MaintainedWorkSurfaceReport) -> str:
    return "\n".join([
        f"version: {report.version}",
        f"verdict: {report.verdict}",
        f"production_authority: {report.production_authority}",
        f"components: {len(report.components)}",
        f"required_surfaces: {len(report.required_surfaces)}",
        f"missing_surfaces: {len(report.missing_surfaces)}",
        "front_stage_council: Persona + Relay + Steward/VZ",
        "persona_total_ion_claim: forbidden",
        "next: V41_FRONT_STAGE_COUNCIL_RUNTIME_RECEIPTS",
    ])


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stable_id(*parts: str) -> str:
    return hashlib.sha256("::".join(parts).encode("utf-8")).hexdigest()[:24]


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inspect V40 maintained work surface canon.")
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--emitted-at", default=None)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    report = generate_maintained_work_surface_report(args.workspace_root, emitted_at=args.emitted_at)
    errors = validate_maintained_work_surface_report(report, args.workspace_root)
    if args.write:
        path = write_maintained_work_surface_report(args.workspace_root, report)
        print(f"report_path: {path}")
    print(format_maintained_work_surface_summary(report))
    if errors:
        print("errors:")
        for error in errors:
            print(f"- {error}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
