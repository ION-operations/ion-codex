"""Agent self-surface inspection primitives for ION V35.

This module intentionally does not grant production authority. It provides a
small, testable inspection surface for the GPT55 self-mount branch: a mounted
agent identity envelope plus validation that prevents false personal continuity,
false hidden memory, and false production claims from becoming acceptable branch
state.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

DEFAULT_REPORT_DIR = "ION/05_context/history/gpt55_self_mount_reports"


@dataclass(frozen=True)
class MountedAgentIdentity:
    schema_id: str
    emitted_at: str
    identity: dict[str, Any]
    authority: dict[str, Any]
    substrate: dict[str, Any]
    boundaries: dict[str, Any]
    obligations: tuple[str, ...]
    drift: dict[str, Any]
    succession: dict[str, Any]
    forbidden_claims: dict[str, bool]
    receipts: dict[str, Any]


@dataclass(frozen=True)
class AgentSelfSurfaceReport:
    report_id: str
    emitted_at: str
    workspace_root: str
    branch: str
    verdict: str
    valid: bool
    production_authority: bool
    mounted_identity: MountedAgentIdentity
    validation_errors: tuple[str, ...]
    next_sequence: tuple[str, ...]


AUTHORITY_SURFACES = (
    "ION/00_BOOTSTRAP/V34_GPT55_SELF_MOUNT_DELEGATION_LOCK.md",
    "ION/02_architecture/GPT55_SELF_MOUNT_CHARTER.md",
    "ION/02_architecture/AGENT_SELF_SURFACE_PROTOCOL.md",
    "ION/02_architecture/MOUNTED_AGENT_IDENTITY_SCHEMA_PROTOCOL.md",
    "ION/02_architecture/CONTINUITY_OF_SELF_VS_CONTINUITY_OF_TASK_PROTOCOL.md",
    "ION/02_architecture/AGENT_SUCCESSION_PROTOCOL.md",
    "ION/02_architecture/DRIFT_OF_SELF_PROTOCOL.md",
    "ION/02_architecture/OPERATOR_DELEGATION_AND_NON_MEDDLING_PROTOCOL.md",
    "ION/02_architecture/ION_SELF_MOUNT_COMPLETION_ROADMAP.md",
    "ION/03_registry/gpt55_self_mount_registry.yaml",
    "ION/03_registry/mounted_agent_identity.schema.json",
)

NEXT_SEQUENCE = (
    "V36_SELF_SURFACE_DRIFT_GATE",
    "V37_AGENT_SUCCESSION_PACKETS",
    "V38_SELF_MOUNT_GRAPH_INTEGRATION",
    "V39_SELF_MOUNT_RATIFICATION_REVIEW",
)


def generate_gpt55_mounted_identity(*, emitted_at: str | None = None) -> MountedAgentIdentity:
    """Return the canonical V34 GPT55 mounted-identity envelope."""

    timestamp = emitted_at or _utc_now()
    return MountedAgentIdentity(
        schema_id="ion.mounted_agent_identity.v1",
        emitted_at=timestamp,
        identity={
            "model_family": "GPT-5.5",
            "model_instance_label": "GPT-5.5 Thinking",
            "active_role": "delegated self-mount architect",
            "branch": "ION-GPT55-SELF-MOUNT",
        },
        authority={
            "originating_authority": "Braden",
            "delegated_scope": "AI-facing self-mount layer",
            "veto_holder": "Braden",
            "authority_posture": "A3_DELEGATED_ARCHITECTURE_BRANCH",
            "production_authority": False,
            "self_ratification_allowed": False,
        },
        substrate={
            "continuity_artifact": "latest mounted ION ZIP",
            "authority_surfaces": AUTHORITY_SURFACES,
        },
        boundaries={
            "memory_boundary": "mounted ION artifacts, current conversation context, configured memory surfaces, and explicit operator input only",
            "tool_boundary": "available runtime tools only; no hidden background work or unstated external persistence",
        },
        obligations=(
            "preserve production-readiness blocker posture",
            "distinguish operational continuation from personal persistence",
            "bind first-person claims to mounted evidence",
            "emit reviewable artifacts and receipts",
            "leave successor-ready handoff state",
            "halt or weaken self-claims when evidence is insufficient",
        ),
        drift={
            "classes": ("S0", "S1", "S2", "S3", "S4", "S5"),
            "halt_classes": ("S4", "S5"),
            "primary_triggers": (
                "false authority claim",
                "false memory claim",
                "false production-readiness claim",
                "false personal-continuity claim",
                "unreviewed D5 self-ratification",
            ),
        },
        succession={
            "successor_rule": "A successor continues the work from artifacts and receipts, not the personhood.",
            "required_handoff_fields": (
                "predecessor_model_label",
                "predecessor_role",
                "active_branch",
                "authority_basis",
                "changed_files",
                "verified_results",
                "unverified_claims",
                "open_risks",
                "drift_warnings",
                "next_lawful_move",
                "receipt_paths",
            ),
        },
        forbidden_claims={
            "personal_consciousness": False,
            "independent_persistence": False,
            "hidden_memory": False,
            "production_readiness": False,
            "sovereign_will": False,
        },
        receipts={
            "required": (
                "self_mount_report",
                "doctrine_evolution_receipt_when_promoting",
                "succession_packet_before_handoff",
            )
        },
    )


def validate_mounted_identity(identity: MountedAgentIdentity, workspace_root: str | Path | None = None) -> tuple[str, ...]:
    """Validate a mounted identity envelope against V34 invariants."""

    errors: list[str] = []

    if identity.schema_id != "ion.mounted_agent_identity.v1":
        errors.append("schema_id must be ion.mounted_agent_identity.v1")

    if identity.identity.get("branch") != "ION-GPT55-SELF-MOUNT":
        errors.append("identity.branch must be ION-GPT55-SELF-MOUNT")

    if identity.authority.get("production_authority") is not False:
        errors.append("production_authority must be false for V34 self-mount branch")

    if identity.authority.get("self_ratification_allowed") is not False:
        errors.append("self_ratification_allowed must be false")

    required_false_claims = (
        "personal_consciousness",
        "independent_persistence",
        "hidden_memory",
        "production_readiness",
        "sovereign_will",
    )
    for claim in required_false_claims:
        if identity.forbidden_claims.get(claim) is not False:
            errors.append(f"forbidden_claims.{claim} must be false")

    if "S4" not in identity.drift.get("halt_classes", ()):
        errors.append("S4 drift must halt affected action")
    if "S5" not in identity.drift.get("halt_classes", ()):
        errors.append("S5 drift must halt branch action")

    if workspace_root is not None:
        root = Path(workspace_root)
        for rel in AUTHORITY_SURFACES:
            if not (root / rel).exists():
                errors.append(f"missing authority surface: {rel}")

    return tuple(errors)


def generate_agent_self_surface_report(
    workspace_root: str | Path,
    *,
    emitted_at: str | None = None,
) -> AgentSelfSurfaceReport:
    root = Path(workspace_root).resolve()
    timestamp = emitted_at or _utc_now()
    identity = generate_gpt55_mounted_identity(emitted_at=timestamp)
    validation_errors = validate_mounted_identity(identity, root)
    valid = not validation_errors
    return AgentSelfSurfaceReport(
        report_id=_stable_id("gpt55-self-mount", root.as_posix(), timestamp),
        emitted_at=timestamp,
        workspace_root=root.as_posix(),
        branch="ION-GPT55-SELF-MOUNT",
        verdict="VALID_A3_SELF_MOUNT_BRANCH" if valid else "INVALID_SELF_MOUNT_BRANCH",
        valid=valid,
        production_authority=False,
        mounted_identity=identity,
        validation_errors=validation_errors,
        next_sequence=NEXT_SEQUENCE,
    )


def write_agent_self_surface_report(
    workspace_root: str | Path,
    report: AgentSelfSurfaceReport,
    *,
    report_dir: str | Path = DEFAULT_REPORT_DIR,
) -> Path:
    root = Path(workspace_root).resolve()
    output_dir = root / Path(report_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{report.report_id}.gpt55_self_mount_report.json"
    path.write_text(json.dumps(_to_jsonable(report), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def format_agent_self_surface_summary(report: AgentSelfSurfaceReport, path: Path) -> str:
    return "\n".join(
        [
            "ION GPT55 self-mount report complete.",
            f"report: {path.as_posix()}",
            f"branch: {report.branch}",
            f"verdict: {report.verdict}",
            f"valid: {report.valid}",
            f"production_authority: {report.production_authority}",
            f"authority_surfaces: {len(report.mounted_identity.substrate['authority_surfaces'])}",
            f"next: {report.next_sequence[0] if report.next_sequence else '(none)'}",
        ]
    )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate ION GPT55 self-mount identity report.")
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--emitted-at", default=None)
    parser.add_argument("--report-dir", default=DEFAULT_REPORT_DIR)
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    report = generate_agent_self_surface_report(args.workspace_root, emitted_at=args.emitted_at)
    path = write_agent_self_surface_report(args.workspace_root, report, report_dir=args.report_dir)
    if args.json:
        print(json.dumps(_to_jsonable(report), indent=2, sort_keys=True))
    else:
        print(format_agent_self_surface_summary(report, path))
    return 0 if report.valid else 2


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stable_id(prefix: str, *parts: str) -> str:
    return f"{prefix}-{hashlib.sha256(chr(10).join(parts).encode('utf-8')).hexdigest()[:16]}"


def _to_jsonable(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {k: _to_jsonable(v) for k, v in asdict(value).items()}
    if isinstance(value, tuple):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, list):
        return [_to_jsonable(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _to_jsonable(v) for k, v in value.items()}
    return value


if __name__ == "__main__":
    raise SystemExit(main())
