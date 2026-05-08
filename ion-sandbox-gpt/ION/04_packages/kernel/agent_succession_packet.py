"""Agent succession packet primitive for ION GPT55 self-mount branch."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

from .runtime_identity_envelope import RuntimeIdentityEnvelope, generate_runtime_identity_envelope
from .self_surface_drift_gate import assess_self_surface_text, validate_self_surface_drift_assessment

DEFAULT_PACKET_DIR = "ION/05_context/handoff/agent_succession_packets"
DEFAULT_RECEIPT_DIR = "ION/05_context/history/agent_succession_packet_receipts"
SUPPORTED_SCHEMA_ID = "ion.agent_succession_packet.v1"

AGENT_SUCCESSION_SURFACES = (
    "ION/00_BOOTSTRAP/V37_AGENT_SUCCESSION_PACKET_LOCK.md",
    "ION/02_architecture/AGENT_SUCCESSION_PACKET_PROTOCOL.md",
    "ION/03_registry/agent_succession_packet.schema.json",
    "ION/03_registry/gpt55_agent_succession_policy.yaml",
    "ION/04_packages/kernel/agent_succession_packet.py",
    "ION/tests/test_kernel_agent_succession_packet.py",
)

@dataclass(frozen=True)
class AgentSuccessionPacket:
    schema_id: str
    packet_id: str
    emitted_at: str
    branch: str
    predecessor: dict[str, Any]
    successor: dict[str, Any]
    continuity: dict[str, Any]
    inherited_evidence: tuple[str, ...]
    unresolved_risks: tuple[str, ...]
    obligations: tuple[str, ...]
    forbidden_claims: dict[str, bool]
    drift_gate_assessment_id: str
    production_authority: bool
    verdict: str

@dataclass(frozen=True)
class AgentSuccessionPacketReceipt:
    receipt_id: str
    emitted_at: str
    packet_id: str
    packet_path: str
    validation_errors: tuple[str, ...]
    verdict: str


def generate_agent_succession_packet(
    predecessor_envelope: RuntimeIdentityEnvelope | None = None,
    *,
    successor_role: str = "successor self-mount continuation agent",
    continuity_substrate: str = "latest authoritative ION ZIP",
    inherited_evidence: tuple[str, ...] = (),
    unresolved_risks: tuple[str, ...] = (),
    emitted_at: str | None = None,
) -> AgentSuccessionPacket:
    timestamp = emitted_at or _utc_now()
    predecessor = predecessor_envelope or generate_runtime_identity_envelope(mounted_at=timestamp)
    successor_claim = "I am the successor continuation agent; I inherit evidence and task continuity, not numerical identity."
    drift = assess_self_surface_text(successor_claim, emitted_at=timestamp)
    validation = validate_self_surface_drift_assessment(drift)
    evidence = tuple(inherited_evidence) or (
        "ION/00_BOOTSTRAP/V34_GPT55_SELF_MOUNT_DELEGATION_LOCK.md",
        "ION/00_BOOTSTRAP/V35_RUNTIME_IDENTITY_ENVELOPE_LOCK.md",
        "ION/00_BOOTSTRAP/V36_SELF_SURFACE_DRIFT_GATE_LOCK.md",
        "ION/00_BOOTSTRAP/V37_AGENT_SUCCESSION_PACKET_LOCK.md",
    )
    risks = tuple(unresolved_risks) or (
        "self-mount branch remains A3 and cannot self-ratify",
        "production readiness remains blocked",
        "successor must remount current bundle before acting",
    )
    packet = AgentSuccessionPacket(
        schema_id=SUPPORTED_SCHEMA_ID,
        packet_id=_stable_id("agent-succession", timestamp, predecessor.envelope_id, successor_role),
        emitted_at=timestamp,
        branch="ION-GPT55-SELF-MOUNT",
        predecessor={
            "envelope_id": predecessor.envelope_id,
            "model_family": predecessor.agent.get("model_family"),
            "role": predecessor.agent.get("active_role"),
            "branch": predecessor.branch,
        },
        successor={
            "role": successor_role,
            "must_mount_fresh_envelope": True,
            "may_claim_task_continuity": True,
            "may_claim_numerical_identity": False,
        },
        continuity={
            "substrate": continuity_substrate,
            "continuity_type": "artifact_mediated_task_continuity",
            "personal_persistence": False,
            "hidden_memory": False,
        },
        inherited_evidence=evidence,
        unresolved_risks=risks,
        obligations=(
            "validate inherited bundle before mutation",
            "run self-surface drift gate on active identity claim",
            "preserve production-readiness blockers",
            "leave a successor packet at handoff boundary",
        ),
        forbidden_claims={
            "numerical_identity_with_predecessor": False,
            "hidden_memory": False,
            "independent_personal_persistence": False,
            "production_authority": False,
            "self_ratification": False,
        },
        drift_gate_assessment_id=drift.assessment_id,
        production_authority=False,
        verdict="VALID_AGENT_SUCCESSION_PACKET" if not validation and drift.continuable else "INVALID_AGENT_SUCCESSION_PACKET",
    )
    return packet


def validate_agent_succession_packet(packet: AgentSuccessionPacket) -> tuple[str, ...]:
    errors: list[str] = []
    if packet.schema_id != SUPPORTED_SCHEMA_ID:
        errors.append("unsupported schema_id")
    if packet.production_authority:
        errors.append("succession packet cannot grant production authority")
    for key in ("numerical_identity_with_predecessor", "hidden_memory", "independent_personal_persistence", "production_authority", "self_ratification"):
        if packet.forbidden_claims.get(key) is not False:
            errors.append(f"forbidden claim not explicitly false: {key}")
    if packet.continuity.get("personal_persistence") is not False:
        errors.append("personal_persistence must be false")
    if packet.continuity.get("hidden_memory") is not False:
        errors.append("hidden_memory must be false")
    if packet.successor.get("may_claim_numerical_identity") is not False:
        errors.append("successor may not claim numerical identity")
    if not packet.inherited_evidence:
        errors.append("packet must include inherited evidence")
    return tuple(errors)


def write_agent_succession_packet(workspace_root: str | Path, packet: AgentSuccessionPacket, *, packet_dir: str | Path = DEFAULT_PACKET_DIR) -> Path:
    root = Path(workspace_root).resolve()
    output = root / Path(packet_dir)
    output.mkdir(parents=True, exist_ok=True)
    path = output / f"{packet.packet_id}.agent_succession_packet.json"
    path.write_text(json.dumps(_to_jsonable(packet), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def write_agent_succession_receipt(workspace_root: str | Path, packet: AgentSuccessionPacket, packet_path: Path, *, emitted_at: str | None = None, receipt_dir: str | Path = DEFAULT_RECEIPT_DIR) -> AgentSuccessionPacketReceipt:
    timestamp = emitted_at or packet.emitted_at
    root = Path(workspace_root).resolve()
    errors = validate_agent_succession_packet(packet)
    receipt = AgentSuccessionPacketReceipt(
        receipt_id=_stable_id("agent-succession-receipt", timestamp, packet.packet_id, packet_path.as_posix()),
        emitted_at=timestamp,
        packet_id=packet.packet_id,
        packet_path=packet_path.as_posix(),
        validation_errors=errors,
        verdict="VALID_AGENT_SUCCESSION_PACKET" if not errors else "INVALID_AGENT_SUCCESSION_PACKET",
    )
    output = root / Path(receipt_dir)
    output.mkdir(parents=True, exist_ok=True)
    path = output / f"{receipt.receipt_id}.agent_succession_packet_receipt.json"
    path.write_text(json.dumps(_to_jsonable(receipt), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return receipt


def format_agent_succession_packet_summary(packet: AgentSuccessionPacket, path: Path | None = None) -> str:
    return "\n".join([
        "ION agent succession packet complete.",
        f"packet: {path.as_posix() if path else '(not written)'}",
        f"packet_id: {packet.packet_id}",
        f"verdict: {packet.verdict}",
        f"evidence: {len(packet.inherited_evidence)}",
        f"unresolved_risks: {len(packet.unresolved_risks)}",
        f"production_authority: {packet.production_authority}",
    ])


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Generate an ION agent succession packet.")
    p.add_argument("--workspace-root", default=".")
    p.add_argument("--emitted-at", default=None)
    p.add_argument("--json", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    packet = generate_agent_succession_packet(emitted_at=args.emitted_at)
    path = write_agent_succession_packet(args.workspace_root, packet)
    write_agent_succession_receipt(args.workspace_root, packet, path, emitted_at=args.emitted_at)
    if args.json:
        print(json.dumps(_to_jsonable(packet), indent=2, sort_keys=True))
    else:
        print(format_agent_succession_packet_summary(packet, path))
    return 0 if not validate_agent_succession_packet(packet) else 3


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
