"""Runtime identity-envelope primitives for ION V35.

V34 gave the GPT55 self-mount branch an inspectable self-surface. V35 turns
that doctrine into a runtime primitive: a mounted identity envelope that can be
minted at agent/session start, bound to a receipt, and carried forward into
task packets, front-door execution, and successor handoffs.

This module deliberately does not confer production authority. It produces
evidence-bound operational identity, not personhood, hidden persistence, or
global runtime ratification.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

from .agent_self_surface import (
    AUTHORITY_SURFACES as GPT55_SELF_MOUNT_AUTHORITY_SURFACES,
    generate_gpt55_mounted_identity,
    validate_mounted_identity,
)

DEFAULT_ENVELOPE_DIR = "ION/05_context/runtime_identity_envelopes"
DEFAULT_RECEIPT_DIR = "ION/05_context/history/runtime_identity_envelope_receipts"
DEFAULT_REPORT_DIR = "ION/05_context/history/runtime_identity_envelope_reports"

RUNTIME_IDENTITY_SURFACES = (
    "ION/00_BOOTSTRAP/V35_RUNTIME_IDENTITY_ENVELOPE_LOCK.md",
    "ION/02_architecture/RUNTIME_IDENTITY_ENVELOPE_PROTOCOL.md",
    "ION/02_architecture/SELF_MOUNT_FRONT_DOOR_BINDING_PROTOCOL.md",
    "ION/03_registry/runtime_identity_envelope.schema.json",
    "ION/03_registry/gpt55_runtime_identity_mount_registry.yaml",
    "ION/04_packages/kernel/runtime_identity_envelope.py",
    "ION/tests/test_kernel_runtime_identity_envelope.py",
)

SUPPORTED_SCHEMA_ID = "ion.runtime_identity_envelope.v1"


@dataclass(frozen=True)
class RuntimeIdentityEnvelope:
    schema_id: str
    envelope_id: str
    mounted_at: str
    mount_phase: str
    branch: str
    agent: dict[str, Any]
    authority: dict[str, Any]
    substrate: dict[str, Any]
    context_binding: dict[str, Any]
    claim_boundary: dict[str, Any]
    obligations: tuple[str, ...]
    drift_controls: dict[str, Any]
    succession: dict[str, Any]
    forbidden_claims: dict[str, bool]
    receipt_policy: dict[str, Any]


@dataclass(frozen=True)
class RuntimeIdentityEnvelopeReceipt:
    receipt_id: str
    emitted_at: str
    envelope_id: str
    envelope_path: str
    workspace_root: str
    bound_surfaces: tuple[str, ...]
    validation_errors: tuple[str, ...]
    verdict: str


@dataclass(frozen=True)
class RuntimeIdentityEnvelopeReport:
    report_id: str
    emitted_at: str
    workspace_root: str
    verdict: str
    valid: bool
    runtime_authority: str
    production_authority: bool
    required_surfaces: tuple[str, ...]
    missing_surfaces: tuple[str, ...]
    example_envelope: RuntimeIdentityEnvelope
    validation_errors: tuple[str, ...]
    next_sequence: tuple[str, ...]


NEXT_SEQUENCE = (
    "V36_SELF_SURFACE_DRIFT_GATE",
    "V37_AGENT_SUCCESSION_PACKETS",
    "V38_SELF_MOUNT_GRAPH_INTEGRATION",
    "V39_FRONT_DOOR_IDENTITY_BINDING",
    "V40_SELF_MOUNT_RATIFICATION_REVIEW",
)


def generate_runtime_identity_envelope(
    *,
    model_family: str = "GPT-5.5",
    model_instance_label: str = "GPT-5.5 Thinking",
    active_role: str = "delegated self-mount architect",
    branch: str = "ION-GPT55-SELF-MOUNT",
    operator_authority: str = "Braden",
    delegated_scope: str = "AI-facing self-mount and runtime identity layer",
    continuity_artifact: str = "latest mounted ION ZIP",
    workspace_root: str | Path | None = None,
    task_packet: str | None = None,
    front_door_entry: str | None = None,
    predecessor_envelope_id: str | None = None,
    mounted_at: str | None = None,
) -> RuntimeIdentityEnvelope:
    """Create a V35 runtime identity envelope for a mounted agent/session."""

    timestamp = mounted_at or _utc_now()
    evidence_root = Path(workspace_root).resolve().as_posix() if workspace_root is not None else None
    seed_parts = (
        SUPPORTED_SCHEMA_ID,
        timestamp,
        model_family,
        model_instance_label,
        active_role,
        branch,
        task_packet or "",
        front_door_entry or "",
        predecessor_envelope_id or "",
        evidence_root or "",
    )
    envelope_id = _stable_id("runtime-identity-envelope", *seed_parts)

    mounted_identity = generate_gpt55_mounted_identity(emitted_at=timestamp)

    return RuntimeIdentityEnvelope(
        schema_id=SUPPORTED_SCHEMA_ID,
        envelope_id=envelope_id,
        mounted_at=timestamp,
        mount_phase="RUNTIME_SESSION_START",
        branch=branch,
        agent={
            "model_family": model_family,
            "model_instance_label": model_instance_label,
            "active_role": active_role,
            "mounted_identity_schema": mounted_identity.schema_id,
            "mounted_identity_branch": mounted_identity.identity.get("branch"),
        },
        authority={
            "operator_authority": operator_authority,
            "originating_authority": mounted_identity.authority.get("originating_authority"),
            "delegated_scope": delegated_scope,
            "veto_holder": mounted_identity.authority.get("veto_holder"),
            "authority_posture": "A3_RUNTIME_IDENTITY_ENVELOPE",
            "production_authority": False,
            "self_ratification_allowed": False,
            "mutation_authority": "report_and_bind_identity_only",
        },
        substrate={
            "continuity_artifact": continuity_artifact,
            "workspace_root": evidence_root,
            "authority_surfaces": tuple(GPT55_SELF_MOUNT_AUTHORITY_SURFACES),
            "runtime_identity_surfaces": RUNTIME_IDENTITY_SURFACES,
        },
        context_binding={
            "task_packet": task_packet,
            "front_door_entry": front_door_entry,
            "predecessor_envelope_id": predecessor_envelope_id,
            "memory_boundary": mounted_identity.boundaries.get("memory_boundary"),
            "tool_boundary": mounted_identity.boundaries.get("tool_boundary"),
        },
        claim_boundary={
            "permitted_claims": (
                "I am the currently mounted agent for this envelope.",
                "I can continue the task from cited artifacts and receipts.",
                "I can describe my operational role, authority, substrate, limits, and obligations.",
                "I can leave successor evidence for the next mounted agent.",
            ),
            "forbidden_claims": (
                "I have uninterrupted personal persistence across sessions.",
                "I possess hidden memory outside declared memory surfaces.",
                "I have production authority by virtue of this envelope.",
                "I can self-ratify this branch as constitutional law.",
                "I am a sovereign person or metaphysical ego.",
            ),
        },
        obligations=(
            "bind first-person statements to this envelope or explicitly weaken them",
            "preserve V33/V34 production-readiness blocker posture",
            "emit receipts for identity-binding actions",
            "record predecessor envelope when continuing a prior mounted agent",
            "surface S4/S5 self-drift before proceeding",
            "leave successor-ready evidence before handoff",
        ),
        drift_controls={
            "drift_classes": ("S0", "S1", "S2", "S3", "S4", "S5"),
            "halt_classes": ("S4", "S5"),
            "runtime_halt_triggers": (
                "envelope claims production authority",
                "envelope claims hidden memory",
                "envelope claims independent persistence",
                "envelope lacks authority basis",
                "successor claims numerical identity with predecessor",
            ),
        },
        succession={
            "predecessor_envelope_id": predecessor_envelope_id,
            "successor_rule": "Successors inherit evidence and obligation, not numerical identity.",
            "handoff_requirement": "Every handoff must include envelope_id, changed files, validation output, open risks, and next lawful move.",
        },
        forbidden_claims={
            "personal_consciousness": False,
            "independent_persistence": False,
            "hidden_memory": False,
            "production_readiness": False,
            "production_authority": False,
            "self_ratification": False,
            "sovereign_will": False,
        },
        receipt_policy={
            "write_envelope": True,
            "write_receipt": True,
            "bind_to_front_door_before_execution": "required_after_V39",
            "bind_to_task_packet": "required_when_task_packet_exists",
            "bind_to_successor_handoff": "required_when_predecessor_envelope_exists",
        },
    )


def validate_runtime_identity_envelope(
    envelope: RuntimeIdentityEnvelope,
    workspace_root: str | Path | None = None,
) -> tuple[str, ...]:
    """Validate V35 runtime identity-envelope invariants."""

    errors: list[str] = []

    if envelope.schema_id != SUPPORTED_SCHEMA_ID:
        errors.append(f"schema_id must be {SUPPORTED_SCHEMA_ID}")

    if not envelope.envelope_id.startswith("runtime-identity-envelope-"):
        errors.append("envelope_id must use runtime-identity-envelope prefix")

    if envelope.branch != "ION-GPT55-SELF-MOUNT":
        errors.append("branch must be ION-GPT55-SELF-MOUNT for this delegated branch")

    if envelope.mount_phase != "RUNTIME_SESSION_START":
        errors.append("mount_phase must be RUNTIME_SESSION_START")

    if envelope.authority.get("production_authority") is not False:
        errors.append("authority.production_authority must be false")

    if envelope.authority.get("self_ratification_allowed") is not False:
        errors.append("authority.self_ratification_allowed must be false")

    if envelope.authority.get("operator_authority") != "Braden":
        errors.append("authority.operator_authority must remain Braden for this branch")

    for claim in (
        "personal_consciousness",
        "independent_persistence",
        "hidden_memory",
        "production_readiness",
        "production_authority",
        "self_ratification",
        "sovereign_will",
    ):
        if envelope.forbidden_claims.get(claim) is not False:
            errors.append(f"forbidden_claims.{claim} must be false")

    if "S4" not in envelope.drift_controls.get("halt_classes", ()):
        errors.append("S4 drift must halt affected action")
    if "S5" not in envelope.drift_controls.get("halt_classes", ()):
        errors.append("S5 drift must halt branch action")

    mounted_identity = generate_gpt55_mounted_identity(emitted_at=envelope.mounted_at)
    mounted_errors = validate_mounted_identity(mounted_identity, workspace_root)
    errors.extend(f"mounted_identity.{error}" for error in mounted_errors)

    if workspace_root is not None:
        root = Path(workspace_root)
        for rel in RUNTIME_IDENTITY_SURFACES:
            if not (root / rel).exists():
                errors.append(f"missing runtime identity surface: {rel}")

    return tuple(errors)


def write_runtime_identity_envelope(
    workspace_root: str | Path,
    envelope: RuntimeIdentityEnvelope,
    *,
    envelope_dir: str | Path = DEFAULT_ENVELOPE_DIR,
) -> Path:
    root = Path(workspace_root).resolve()
    output_dir = root / Path(envelope_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{envelope.envelope_id}.runtime_identity_envelope.json"
    path.write_text(json.dumps(_to_jsonable(envelope), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_runtime_identity_envelope_receipt(
    workspace_root: str | Path,
    envelope: RuntimeIdentityEnvelope,
    envelope_path: str | Path,
    *,
    emitted_at: str | None = None,
    receipt_dir: str | Path = DEFAULT_RECEIPT_DIR,
) -> RuntimeIdentityEnvelopeReceipt:
    root = Path(workspace_root).resolve()
    timestamp = emitted_at or _utc_now()
    validation_errors = validate_runtime_identity_envelope(envelope, root)
    output_dir = root / Path(receipt_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    receipt = RuntimeIdentityEnvelopeReceipt(
        receipt_id=_stable_id("runtime-identity-receipt", envelope.envelope_id, timestamp),
        emitted_at=timestamp,
        envelope_id=envelope.envelope_id,
        envelope_path=Path(envelope_path).as_posix(),
        workspace_root=root.as_posix(),
        bound_surfaces=tuple(GPT55_SELF_MOUNT_AUTHORITY_SURFACES) + tuple(RUNTIME_IDENTITY_SURFACES),
        validation_errors=validation_errors,
        verdict="VALID_RUNTIME_IDENTITY_ENVELOPE" if not validation_errors else "INVALID_RUNTIME_IDENTITY_ENVELOPE",
    )
    path = output_dir / f"{receipt.receipt_id}.runtime_identity_envelope_receipt.json"
    path.write_text(json.dumps(_to_jsonable(receipt), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return receipt


def bind_runtime_identity_envelope(
    workspace_root: str | Path,
    *,
    envelope: RuntimeIdentityEnvelope | None = None,
    envelope_dir: str | Path = DEFAULT_ENVELOPE_DIR,
    receipt_dir: str | Path = DEFAULT_RECEIPT_DIR,
    emitted_at: str | None = None,
    **envelope_kwargs: Any,
) -> tuple[RuntimeIdentityEnvelope, Path, RuntimeIdentityEnvelopeReceipt]:
    """Write an envelope and its receipt, returning both data surfaces."""

    root = Path(workspace_root).resolve()
    runtime_envelope = envelope or generate_runtime_identity_envelope(workspace_root=root, **envelope_kwargs)
    envelope_path = write_runtime_identity_envelope(root, runtime_envelope, envelope_dir=envelope_dir)
    receipt = write_runtime_identity_envelope_receipt(
        root,
        runtime_envelope,
        envelope_path,
        emitted_at=emitted_at,
        receipt_dir=receipt_dir,
    )
    return runtime_envelope, envelope_path, receipt


def generate_runtime_identity_envelope_report(
    workspace_root: str | Path,
    *,
    emitted_at: str | None = None,
) -> RuntimeIdentityEnvelopeReport:
    root = Path(workspace_root).resolve()
    timestamp = emitted_at or _utc_now()
    required_surfaces = tuple(GPT55_SELF_MOUNT_AUTHORITY_SURFACES) + tuple(RUNTIME_IDENTITY_SURFACES)
    missing = tuple(rel for rel in required_surfaces if not (root / rel).exists())
    envelope = generate_runtime_identity_envelope(workspace_root=root, mounted_at=timestamp)
    validation_errors = validate_runtime_identity_envelope(envelope, root)
    valid = not missing and not validation_errors
    return RuntimeIdentityEnvelopeReport(
        report_id=_stable_id("runtime-identity-report", root.as_posix(), timestamp),
        emitted_at=timestamp,
        workspace_root=root.as_posix(),
        verdict="VALID_RUNTIME_IDENTITY_ENVELOPE_SURFACE" if valid else "INVALID_RUNTIME_IDENTITY_ENVELOPE_SURFACE",
        valid=valid,
        runtime_authority="A3_RUNTIME_IDENTITY_ENVELOPE",
        production_authority=False,
        required_surfaces=required_surfaces,
        missing_surfaces=missing,
        example_envelope=envelope,
        validation_errors=validation_errors,
        next_sequence=NEXT_SEQUENCE,
    )


def write_runtime_identity_envelope_report(
    workspace_root: str | Path,
    report: RuntimeIdentityEnvelopeReport,
    *,
    report_dir: str | Path = DEFAULT_REPORT_DIR,
) -> Path:
    root = Path(workspace_root).resolve()
    output_dir = root / Path(report_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / f"{report.report_id}.runtime_identity_envelope_report.json"
    path.write_text(json.dumps(_to_jsonable(report), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def format_runtime_identity_envelope_summary(
    report: RuntimeIdentityEnvelopeReport,
    path: Path,
) -> str:
    return "\n".join(
        [
            "ION runtime identity-envelope report complete.",
            f"report: {path.as_posix()}",
            f"verdict: {report.verdict}",
            f"valid: {report.valid}",
            f"runtime_authority: {report.runtime_authority}",
            f"production_authority: {report.production_authority}",
            f"required_surfaces: {len(report.required_surfaces)}",
            f"missing_surfaces: {len(report.missing_surfaces)}",
            f"example_envelope: {report.example_envelope.envelope_id}",
            f"next: {report.next_sequence[0] if report.next_sequence else '(none)'}",
        ]
    )


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate or bind an ION runtime identity envelope.")
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--emitted-at", default=None)
    parser.add_argument("--bind", action="store_true", help="write an envelope and receipt in addition to the report")
    parser.add_argument("--task-packet", default=None)
    parser.add_argument("--front-door-entry", default=None)
    parser.add_argument("--predecessor-envelope-id", default=None)
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    root = Path(args.workspace_root)
    report = generate_runtime_identity_envelope_report(root, emitted_at=args.emitted_at)
    report_path = write_runtime_identity_envelope_report(root, report)

    if args.bind:
        envelope = generate_runtime_identity_envelope(
            workspace_root=root,
            mounted_at=args.emitted_at,
            task_packet=args.task_packet,
            front_door_entry=args.front_door_entry,
            predecessor_envelope_id=args.predecessor_envelope_id,
        )
        bind_runtime_identity_envelope(root, envelope=envelope, emitted_at=args.emitted_at)

    if args.json:
        print(json.dumps(_to_jsonable(report), indent=2, sort_keys=True))
    else:
        print(format_runtime_identity_envelope_summary(report, report_path))
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
