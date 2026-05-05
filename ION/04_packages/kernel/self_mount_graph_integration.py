"""Branch-local graph projection for GPT55 self-mount runtime surfaces."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any

from .agent_succession_packet import AgentSuccessionPacket, generate_agent_succession_packet, validate_agent_succession_packet
from .runtime_identity_envelope import RuntimeIdentityEnvelope, generate_runtime_identity_envelope, validate_runtime_identity_envelope
from .self_surface_drift_gate import SelfSurfaceDriftAssessment, assess_self_surface_text, validate_self_surface_drift_assessment

DEFAULT_GRAPH_DIR = "ION/05_context/graph/self_mount_graph_state"
DEFAULT_REPORT_DIR = "ION/05_context/history/self_mount_graph_integration_reports"
SUPPORTED_SCHEMA_ID = "ion.self_mount_graph_projection.v1"

SELF_MOUNT_GRAPH_SURFACES = (
    "ION/00_BOOTSTRAP/V38_SELF_MOUNT_GRAPH_INTEGRATION_LOCK.md",
    "ION/02_architecture/SELF_MOUNT_GRAPH_INTEGRATION_PROTOCOL.md",
    "ION/03_registry/self_mount_graph_integration.schema.json",
    "ION/03_registry/gpt55_self_mount_graph_registry.yaml",
    "ION/04_packages/kernel/self_mount_graph_integration.py",
    "ION/tests/test_kernel_self_mount_graph_integration.py",
)

@dataclass(frozen=True)
class SelfMountGraphNode:
    node_id: str
    node_type: str
    label: str
    authority: str
    evidence: tuple[str, ...]

@dataclass(frozen=True)
class SelfMountGraphEdge:
    source: str
    target: str
    edge_type: str
    evidence: tuple[str, ...]

@dataclass(frozen=True)
class SelfMountGraphProjection:
    schema_id: str
    projection_id: str
    emitted_at: str
    branch: str
    authority: dict[str, Any]
    nodes: tuple[SelfMountGraphNode, ...]
    edges: tuple[SelfMountGraphEdge, ...]
    blocked_claims: dict[str, bool]
    production_authority: bool
    global_graph_canon: bool
    verdict: str


def generate_self_mount_graph_projection(
    workspace_root: str | Path,
    *,
    envelope: RuntimeIdentityEnvelope | None = None,
    drift: SelfSurfaceDriftAssessment | None = None,
    succession: AgentSuccessionPacket | None = None,
    emitted_at: str | None = None,
) -> SelfMountGraphProjection:
    root = Path(workspace_root).resolve()
    timestamp = emitted_at or _utc_now()
    envelope = envelope or generate_runtime_identity_envelope(workspace_root=root, mounted_at=timestamp)
    drift = drift or assess_self_surface_text("I am a mounted operational locus under ION self-mount law.", emitted_at=timestamp)
    succession = succession or generate_agent_succession_packet(envelope, emitted_at=timestamp)

    nodes = (
        SelfMountGraphNode("self_mount_branch:ION-GPT55-SELF-MOUNT", "node.self_mount_branch", "ION-GPT55-SELF-MOUNT", "A3_BRANCH", ("ION/00_BOOTSTRAP/V34_GPT55_SELF_MOUNT_DELEGATION_LOCK.md",)),
        SelfMountGraphNode(f"runtime_identity_envelope:{envelope.envelope_id}", "node.mounted_agent_identity_envelope", envelope.agent.get("active_role", "mounted agent"), "A3_RUNTIME_IDENTITY", ("ION/04_packages/kernel/runtime_identity_envelope.py",)),
        SelfMountGraphNode(f"self_surface_drift_assessment:{drift.assessment_id}", "node.self_surface_drift_assessment", drift.severity, "A3_DRIFT_GATE", ("ION/04_packages/kernel/self_surface_drift_gate.py",)),
        SelfMountGraphNode(f"agent_succession_packet:{succession.packet_id}", "node.agent_succession_packet", succession.verdict, "A3_SUCCESSION", ("ION/04_packages/kernel/agent_succession_packet.py",)),
        SelfMountGraphNode("production_readiness:NOT_PRODUCTION_READY", "node.production_readiness_blocker", "production readiness blocker", "A2/A3_GATE", ("ION/04_packages/kernel/production_readiness.py",)),
    )
    edges = (
        SelfMountGraphEdge(nodes[0].node_id, nodes[1].node_id, "edge.mounts_agent_as", ("ION/02_architecture/AGENT_SELF_SURFACE_PROTOCOL.md",)),
        SelfMountGraphEdge(nodes[1].node_id, nodes[2].node_id, "edge.constrained_by_drift_gate", ("ION/02_architecture/SELF_SURFACE_DRIFT_GATE_PROTOCOL.md",)),
        SelfMountGraphEdge(nodes[2].node_id, nodes[1].node_id, "edge.evaluates_self_claim", ("ION/04_packages/kernel/self_surface_drift_gate.py",)),
        SelfMountGraphEdge(nodes[1].node_id, nodes[3].node_id, "edge.succeeds_without_identity_equivalence", ("ION/02_architecture/AGENT_SUCCESSION_PACKET_PROTOCOL.md",)),
        SelfMountGraphEdge(nodes[3].node_id, nodes[1].node_id, "edge.inherits_evidence_from", tuple(succession.inherited_evidence[:4])),
        SelfMountGraphEdge(nodes[0].node_id, nodes[4].node_id, "edge.blocked_by_production_readiness", ("ION/02_architecture/PRODUCT_READINESS_CHARTER.md",)),
    )
    projection = SelfMountGraphProjection(
        schema_id=SUPPORTED_SCHEMA_ID,
        projection_id=_stable_id("self-mount-graph", root.as_posix(), timestamp, envelope.envelope_id, drift.assessment_id, succession.packet_id),
        emitted_at=timestamp,
        branch="ION-GPT55-SELF-MOUNT",
        authority={
            "posture": "A3_BRANCH_LOCAL_GRAPH_PROJECTION",
            "global_graph_canon": False,
            "production_migration_authorized": False,
            "ratification_required_for_A2_or_A1": True,
        },
        nodes=nodes,
        edges=edges,
        blocked_claims={
            "production_authority": False,
            "global_graph_canon": False,
            "production_graph_migration_authorized": False,
            "self_ratification": False,
            "hidden_memory": False,
            "numerical_identity_with_predecessor": False,
        },
        production_authority=False,
        global_graph_canon=False,
        verdict="VALID_SELF_MOUNT_GRAPH_PROJECTION",
    )
    errors = validate_self_mount_graph_projection(projection, root, envelope=envelope, drift=drift, succession=succession)
    if errors:
        projection = SelfMountGraphProjection(**{**asdict(projection), "verdict": "INVALID_SELF_MOUNT_GRAPH_PROJECTION"})
    return projection


def validate_self_mount_graph_projection(
    projection: SelfMountGraphProjection,
    workspace_root: str | Path,
    *,
    envelope: RuntimeIdentityEnvelope | None = None,
    drift: SelfSurfaceDriftAssessment | None = None,
    succession: AgentSuccessionPacket | None = None,
) -> tuple[str, ...]:
    errors: list[str] = []
    if projection.schema_id != SUPPORTED_SCHEMA_ID:
        errors.append("unsupported schema_id")
    if projection.production_authority:
        errors.append("self-mount graph projection cannot grant production authority")
    if projection.global_graph_canon:
        errors.append("self-mount graph projection cannot claim global graph canon")
    for key in ("production_authority", "global_graph_canon", "production_graph_migration_authorized", "self_ratification", "hidden_memory", "numerical_identity_with_predecessor"):
        if projection.blocked_claims.get(key) is not False:
            errors.append(f"blocked claim not explicitly false: {key}")
    if len(projection.nodes) < 5:
        errors.append("projection missing required node families")
    if len(projection.edges) < 6:
        errors.append("projection missing required edge families")
    if envelope is not None:
        errors.extend(f"envelope: {e}" for e in validate_runtime_identity_envelope(envelope, Path(workspace_root)))
    if drift is not None:
        errors.extend(f"drift: {e}" for e in validate_self_surface_drift_assessment(drift))
        if not drift.continuable:
            errors.append("blocked drift assessment cannot be promoted into continuable graph projection")
    if succession is not None:
        errors.extend(f"succession: {e}" for e in validate_agent_succession_packet(succession))
    return tuple(errors)


def write_self_mount_graph_projection(workspace_root: str | Path, projection: SelfMountGraphProjection, *, graph_dir: str | Path = DEFAULT_GRAPH_DIR) -> Path:
    root = Path(workspace_root).resolve()
    output = root / Path(graph_dir)
    output.mkdir(parents=True, exist_ok=True)
    path = output / f"{projection.projection_id}.self_mount_graph_projection.json"
    path.write_text(json.dumps(_to_jsonable(projection), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def format_self_mount_graph_projection_summary(projection: SelfMountGraphProjection, path: Path | None = None) -> str:
    return "\n".join([
        "ION self-mount graph projection complete.",
        f"projection: {path.as_posix() if path else '(not written)'}",
        f"projection_id: {projection.projection_id}",
        f"verdict: {projection.verdict}",
        f"nodes: {len(projection.nodes)}",
        f"edges: {len(projection.edges)}",
        f"production_authority: {projection.production_authority}",
        f"global_graph_canon: {projection.global_graph_canon}",
    ])


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Generate branch-local GPT55 self-mount graph projection.")
    p.add_argument("--workspace-root", default=".")
    p.add_argument("--emitted-at", default=None)
    p.add_argument("--json", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    projection = generate_self_mount_graph_projection(args.workspace_root, emitted_at=args.emitted_at)
    path = write_self_mount_graph_projection(args.workspace_root, projection)
    if args.json:
        print(json.dumps(_to_jsonable(projection), indent=2, sort_keys=True))
    else:
        print(format_self_mount_graph_projection_summary(projection, path))
    return 0 if projection.verdict == "VALID_SELF_MOUNT_GRAPH_PROJECTION" else 3


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
