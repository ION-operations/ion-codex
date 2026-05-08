"""Governed writeback proposals for Evented Template File Graph projections.

This module implements Phase 4 of the Evented Template File Graph law. It reads
Phase 3 template event index projections and materializes proposal-only graph
writeback records: proposed nodes, proposed edges, blocked/deferred reactions,
and receipts.

It intentionally does not mutate source graph state, registries, schedules,
source files, or agent activation state. The output is a proposal surface that
must pass later governed write / landing before becoming source graph truth.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any


class KernelTemplateGraphWritebackProposalError(Exception):
    """Raised when template graph writeback proposal generation cannot proceed."""


@dataclass(frozen=True)
class ProposedTemplateGraphNode:
    """A proposal for one source graph node derived from an event projection entry."""

    node_id: str
    node_type: str
    source_path: str
    event_id: str
    selection_id: str
    requested_effect: str
    reaction_family: str
    authority_status: str
    proposal_status: str


@dataclass(frozen=True)
class ProposedTemplateGraphEdge:
    """A proposal for one source graph edge derived from an event projection entry."""

    edge_id: str
    edge_type: str
    from_node: str
    to_node: str
    source_path: str
    proposal_status: str


@dataclass(frozen=True)
class DeferredTemplateGraphReaction:
    """A non-writeback reaction preserved as blocked/deferred evidence."""

    event_id: str
    selection_id: str
    source_path: str
    requested_effect: str
    reaction_family: str
    reaction_class: str
    deferral_reason: str
    proposal_status: str


@dataclass(frozen=True)
class TemplateGraphWritebackProposal:
    """Proposal-only graph writeback surface.

    This record is deliberately not source graph truth. It is the inspectable
    artifact that a later governed write/landing pass can accept, hold, or
    escalate.
    """

    proposal_id: str
    proposal_type: str
    emitted_at: str
    phase: str
    proposal_only: bool
    source_graph_mutation_blocked: bool
    registry_mutation_blocked: bool
    schedule_mutation_blocked: bool
    agent_activation_blocked: bool
    source_projection_paths: tuple[str, ...]
    proposed_nodes: tuple[ProposedTemplateGraphNode, ...]
    proposed_edges: tuple[ProposedTemplateGraphEdge, ...]
    deferred_reactions: tuple[DeferredTemplateGraphReaction, ...]
    notes: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class TemplateGraphWritebackProposalReceipt:
    """Receipt for one Phase 4 graph-writeback proposal pass."""

    receipt_id: str
    emitted_at: str
    scanned_root: str
    projection_count: int
    proposed_node_count: int
    proposed_edge_count: int
    deferred_reaction_count: int
    proposal_path: str
    proposal_only: bool


class KernelTemplateGraphWritebackProposer:
    """Build proposal-only graph writeback records from Phase 3 projections.

    Phase 4 contract:
    - May read Phase 3 projection-only index surfaces.
    - May materialize proposed graph nodes/edges as proposal records.
    - Must preserve deferred reactions as blocked/deferred evidence.
    - Must not mutate source graph, registries, schedules, source files, or
      agent activation state.
    """

    def propose_from_workspace(
        self,
        workspace_root: Path,
        *,
        emitted_at: str | None = None,
        write_proposal: bool = True,
    ) -> TemplateGraphWritebackProposalReceipt:
        root = Path(workspace_root)
        if not root.exists():
            raise KernelTemplateGraphWritebackProposalError(f"workspace root does not exist: {root}")
        timestamp = emitted_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        projection_paths = tuple(
            sorted((root / "ION/05_context/projections/template_event_index_projection").glob("*.json"))
        )
        proposal = self.build_writeback_proposal(root, projection_paths, emitted_at=timestamp)
        proposal_path = ""
        receipt = TemplateGraphWritebackProposalReceipt(
            receipt_id=self._stable_id("template-graph-writeback-proposal", proposal.proposal_id, timestamp),
            emitted_at=timestamp,
            scanned_root=root.as_posix(),
            projection_count=len(projection_paths),
            proposed_node_count=len(proposal.proposed_nodes),
            proposed_edge_count=len(proposal.proposed_edges),
            deferred_reaction_count=len(proposal.deferred_reactions),
            proposal_path=proposal_path,
            proposal_only=True,
        )
        if write_proposal:
            path = self.write_writeback_proposal(root, proposal)
            proposal_path = path.relative_to(root).as_posix()
            receipt = TemplateGraphWritebackProposalReceipt(
                receipt_id=receipt.receipt_id,
                emitted_at=receipt.emitted_at,
                scanned_root=receipt.scanned_root,
                projection_count=receipt.projection_count,
                proposed_node_count=receipt.proposed_node_count,
                proposed_edge_count=receipt.proposed_edge_count,
                deferred_reaction_count=receipt.deferred_reaction_count,
                proposal_path=proposal_path,
                proposal_only=True,
            )
            self.write_writeback_proposal_receipt(root, receipt)
        return receipt

    def build_writeback_proposal(
        self,
        workspace_root: Path,
        projection_paths: tuple[Path, ...],
        *,
        emitted_at: str,
    ) -> TemplateGraphWritebackProposal:
        root = Path(workspace_root)
        proposed_nodes: list[ProposedTemplateGraphNode] = []
        proposed_edges: list[ProposedTemplateGraphEdge] = []
        deferred: list[DeferredTemplateGraphReaction] = []
        source_projection_paths: list[str] = []

        for path in projection_paths:
            projection = json.loads(Path(path).read_text(encoding="utf-8"))
            if projection.get("projection_type") != "TEMPLATE_EVENT_INDEX_PROJECTION":
                raise KernelTemplateGraphWritebackProposalError(
                    f"not a template event index projection: {path}"
                )
            rel = path.relative_to(root).as_posix() if path.is_relative_to(root) else path.as_posix()
            source_projection_paths.append(rel)

            for entry in projection.get("entries", []):
                node_id = self._stable_id(
                    "ctx-template-event-node",
                    str(entry.get("event_id", "")),
                    str(entry.get("source_path", "")),
                    str(entry.get("requested_effect", "")),
                )
                file_node_id = self._stable_id("ctx-template-file", str(entry.get("source_path", "")))
                selection_node_id = self._stable_id(
                    "ctx-template-selection",
                    str(entry.get("selection_id", "")),
                    str(entry.get("requested_effect", "")),
                )
                proposed_nodes.append(
                    ProposedTemplateGraphNode(
                        node_id=node_id,
                        node_type="TEMPLATE_COMPLETION_EVENT_REACTION_NODE",
                        source_path=str(entry.get("source_path", "")),
                        event_id=str(entry.get("event_id", "")),
                        selection_id=str(entry.get("selection_id", "")),
                        requested_effect=str(entry.get("requested_effect", "")),
                        reaction_family=str(entry.get("reaction_family", "")),
                        authority_status="PROPOSAL_REQUIRES_LANDING",
                        proposal_status="PROPOSED_NOT_MUTATED",
                    )
                )
                proposed_edges.append(
                    ProposedTemplateGraphEdge(
                        edge_id=self._stable_id("ctx-template-edge", file_node_id, node_id, "EMITS_TEMPLATE_EVENT"),
                        edge_type="EMITS_TEMPLATE_EVENT",
                        from_node=file_node_id,
                        to_node=node_id,
                        source_path=str(entry.get("source_path", "")),
                        proposal_status="PROPOSED_NOT_MUTATED",
                    )
                )
                proposed_edges.append(
                    ProposedTemplateGraphEdge(
                        edge_id=self._stable_id(
                            "ctx-template-edge", selection_node_id, node_id, "PROJECTS_REACTION_TO_GRAPH_NODE"
                        ),
                        edge_type="PROJECTS_REACTION_TO_GRAPH_NODE",
                        from_node=selection_node_id,
                        to_node=node_id,
                        source_path=str(entry.get("source_path", "")),
                        proposal_status="PROPOSED_NOT_MUTATED",
                    )
                )

            for item in projection.get("deferred_reactions", []):
                deferred.append(
                    DeferredTemplateGraphReaction(
                        event_id=str(item.get("event_id", "")),
                        selection_id=str(item.get("selection_id", "")),
                        source_path=str(item.get("source_path", "")),
                        requested_effect=str(item.get("requested_effect", "")),
                        reaction_family=str(item.get("reaction_family", "")),
                        reaction_class=str(item.get("reaction_class", "")),
                        deferral_reason=str(item.get("deferral_reason", "DEFERRED_BY_PHASE_3")),
                        proposal_status="DEFERRED_NOT_MUTATED",
                    )
                )

        proposal_id = self._stable_id(
            "template-graph-writeback-proposal",
            emitted_at,
            *[node.node_id for node in proposed_nodes],
            *[edge.edge_id for edge in proposed_edges],
            *[item.event_id + item.requested_effect + item.deferral_reason for item in deferred],
        )
        return TemplateGraphWritebackProposal(
            proposal_id=proposal_id,
            proposal_type="TEMPLATE_GRAPH_WRITEBACK_PROPOSAL",
            emitted_at=emitted_at,
            phase="PHASE_4_GOVERNED_WRITEBACK_PROPOSAL",
            proposal_only=True,
            source_graph_mutation_blocked=True,
            registry_mutation_blocked=True,
            schedule_mutation_blocked=True,
            agent_activation_blocked=True,
            source_projection_paths=tuple(source_projection_paths),
            proposed_nodes=tuple(proposed_nodes),
            proposed_edges=tuple(proposed_edges),
            deferred_reactions=tuple(deferred),
            notes=(
                "Proposal-only graph writeback: not source graph truth.",
                "A later governed write/landing pass must accept, hold, or escalate this proposal.",
                "Deferred schedule, registry, graph, and agent activation reactions remain non-mutating.",
            ),
        )

    def write_writeback_proposal(self, workspace_root: Path, proposal: TemplateGraphWritebackProposal) -> Path:
        output_dir = Path(workspace_root) / "ION/05_context/history/template_graph_writeback_proposals"
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"{proposal.proposal_id}.template_graph_writeback_proposal.json"
        if path.exists():
            return path
        path.write_text(json.dumps(_to_jsonable(proposal), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def write_writeback_proposal_receipt(
        self, workspace_root: Path, receipt: TemplateGraphWritebackProposalReceipt
    ) -> Path:
        output_dir = Path(workspace_root) / "ION/05_context/history/template_graph_writeback_proposal_receipts"
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"{receipt.receipt_id}.template_graph_writeback_proposal_receipt.json"
        if path.exists():
            return path
        path.write_text(json.dumps(_to_jsonable(receipt), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path

    @staticmethod
    def _stable_id(prefix: str, *parts: str) -> str:
        digest = hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()[:16]
        return f"{prefix}-{digest}"


IonTemplateGraphWritebackProposer = KernelTemplateGraphWritebackProposer
IonTemplateGraphWritebackProposalError = KernelTemplateGraphWritebackProposalError


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
