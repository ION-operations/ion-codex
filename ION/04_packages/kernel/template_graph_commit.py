"""Bounded graph commit handling for LANDed template graph writeback proposals.

This module implements Phase 6 of the Evented Template File Graph pipeline. It
reads Phase 5 LAND review verdicts and commits the accepted proposed nodes and
edges into a dedicated template-event graph-state surface.

It intentionally does not mutate source files, registries, schedules, or agent
activation state. The only graph truth it writes is the bounded evented-template
file graph state under ``ION/05_context/graph/template_event_graph_state``.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any


class KernelTemplateGraphCommitError(Exception):
    """Raised when a LANDed graph writeback proposal cannot be committed lawfully."""


@dataclass(frozen=True)
class CommittedTemplateGraphNode:
    """A bounded committed node in the evented-template file graph state."""

    node_id: str
    node_type: str
    committed_at: str
    committed_from_proposal: str
    committed_from_review: str
    source_path: str
    event_id: str
    selection_id: str
    requested_effect: str
    reaction_family: str
    authority_status: str
    graph_state_status: str


@dataclass(frozen=True)
class CommittedTemplateGraphEdge:
    """A bounded committed edge in the evented-template file graph state."""

    edge_id: str
    edge_type: str
    committed_at: str
    committed_from_proposal: str
    committed_from_review: str
    from_node: str
    to_node: str
    source_path: str
    graph_state_status: str


@dataclass(frozen=True)
class TemplateGraphCommitRecord:
    """Commit record for one LANDed Phase 5 review."""

    commit_id: str
    commit_type: str
    emitted_at: str
    phase: str
    review_id: str
    proposal_id: str
    proposal_path: str
    reviewer: str
    verdict: str
    committed_node_ids: tuple[str, ...]
    committed_edge_ids: tuple[str, ...]
    skipped_existing_node_ids: tuple[str, ...] = field(default_factory=tuple)
    skipped_existing_edge_ids: tuple[str, ...] = field(default_factory=tuple)
    source_file_mutation_blocked: bool = True
    registry_mutation_blocked: bool = True
    schedule_mutation_blocked: bool = True
    agent_activation_blocked: bool = True
    notes: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class TemplateGraphCommitReceipt:
    """Aggregate receipt for one Phase 6 bounded graph commit pass."""

    receipt_id: str
    emitted_at: str
    scanned_root: str
    eligible_land_review_count: int
    committed_review_count: int
    committed_node_count: int
    committed_edge_count: int
    skipped_review_count: int
    commit_paths: tuple[str, ...]
    graph_state_root: str
    bounded_graph_commit: bool
    source_file_mutation_blocked: bool
    registry_mutation_blocked: bool
    schedule_mutation_blocked: bool
    agent_activation_blocked: bool


class KernelTemplateGraphCommitter:
    """Commit LANDed graph-writeback proposals into bounded graph-state files."""

    def commit_landed_from_workspace(
        self,
        workspace_root: Path,
        *,
        emitted_at: str | None = None,
        only_uncommitted: bool = True,
    ) -> TemplateGraphCommitReceipt:
        root = Path(workspace_root)
        if not root.exists():
            raise KernelTemplateGraphCommitError(f"workspace root does not exist: {root}")
        timestamp = emitted_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        review_paths = self._land_review_paths(root)
        if not review_paths:
            raise KernelTemplateGraphCommitError("no LANDed template graph writeback reviews found")

        commit_paths: list[str] = []
        committed_node_count = 0
        committed_edge_count = 0
        skipped_review_count = 0

        for review_path in review_paths:
            review = self._load_review(review_path)
            if only_uncommitted and self._review_has_commit(root, str(review.get("review_id", ""))):
                skipped_review_count += 1
                continue
            commit = self.build_commit(root, review_path, emitted_at=timestamp)
            node_count, edge_count = self.write_committed_graph_state(root, commit, review_path)
            committed_node_count += node_count
            committed_edge_count += edge_count
            commit_path = self.write_commit_record(root, commit)
            commit_paths.append(commit_path.relative_to(root).as_posix())

        receipt = TemplateGraphCommitReceipt(
            receipt_id=self._stable_id("template-graph-commit", timestamp, *commit_paths),
            emitted_at=timestamp,
            scanned_root=root.as_posix(),
            eligible_land_review_count=len(review_paths),
            committed_review_count=len(commit_paths),
            committed_node_count=committed_node_count,
            committed_edge_count=committed_edge_count,
            skipped_review_count=skipped_review_count,
            commit_paths=tuple(commit_paths),
            graph_state_root="ION/05_context/graph/template_event_graph_state",
            bounded_graph_commit=True,
            source_file_mutation_blocked=True,
            registry_mutation_blocked=True,
            schedule_mutation_blocked=True,
            agent_activation_blocked=True,
        )
        self.write_commit_receipt(root, receipt)
        return receipt

    def build_commit(self, workspace_root: Path, review_path: Path, *, emitted_at: str) -> TemplateGraphCommitRecord:
        root = Path(workspace_root)
        review = self._load_review(review_path)
        if review.get("review_type") != "TEMPLATE_GRAPH_WRITEBACK_REVIEW_VERDICT":
            raise KernelTemplateGraphCommitError(f"not a template graph writeback review: {review_path}")
        if review.get("verdict") != "LAND" or review.get("accepted_for_later_graph_commit") is not True:
            raise KernelTemplateGraphCommitError("only LAND reviews accepted for later graph commit can be committed")
        if review.get("source_graph_mutation_blocked") is not True:
            raise KernelTemplateGraphCommitError("Phase 5 review must preserve source_graph_mutation_blocked=true")

        proposal_path = root / str(review.get("proposal_path", ""))
        proposal = self._load_proposal(root, proposal_path)
        if proposal.get("proposal_id") != review.get("proposal_id"):
            raise KernelTemplateGraphCommitError("review proposal_id does not match proposal file")
        proposed_nodes = proposal.get("proposed_nodes", [])
        proposed_edges = proposal.get("proposed_edges", [])
        if not proposed_nodes and not proposed_edges:
            raise KernelTemplateGraphCommitError("cannot commit an empty graph proposal")

        committed_node_ids = tuple(str(item.get("node_id", "")) for item in proposed_nodes)
        committed_edge_ids = tuple(str(item.get("edge_id", "")) for item in proposed_edges)
        commit_id = self._stable_id(
            "template-graph-commit",
            str(review.get("review_id", "")),
            str(proposal.get("proposal_id", "")),
            emitted_at,
        )
        return TemplateGraphCommitRecord(
            commit_id=commit_id,
            commit_type="TEMPLATE_GRAPH_BOUNDED_COMMIT",
            emitted_at=emitted_at,
            phase="PHASE_6_BOUNDED_GRAPH_COMMIT",
            review_id=str(review.get("review_id", "")),
            proposal_id=str(proposal.get("proposal_id", "")),
            proposal_path=str(review.get("proposal_path", "")),
            reviewer=str(review.get("reviewer", "")),
            verdict=str(review.get("verdict", "")),
            committed_node_ids=committed_node_ids,
            committed_edge_ids=committed_edge_ids,
            notes=(
                "Bounded commit of LANDed template graph writeback proposal.",
                "Writes only the evented-template graph-state surface, not source files or registries.",
                "This is the first phase where accepted proposals become bounded graph truth.",
            ),
        )

    def write_committed_graph_state(self, workspace_root: Path, commit: TemplateGraphCommitRecord, review_path: Path) -> tuple[int, int]:
        root = Path(workspace_root)
        review = self._load_review(review_path)
        proposal = self._load_proposal(root, root / str(review.get("proposal_path", "")))
        node_dir = root / "ION/05_context/graph/template_event_graph_state/nodes"
        edge_dir = root / "ION/05_context/graph/template_event_graph_state/edges"
        node_dir.mkdir(parents=True, exist_ok=True)
        edge_dir.mkdir(parents=True, exist_ok=True)

        written_nodes = 0
        written_edges = 0
        for item in proposal.get("proposed_nodes", []):
            node = CommittedTemplateGraphNode(
                node_id=str(item.get("node_id", "")),
                node_type=str(item.get("node_type", "")),
                committed_at=commit.emitted_at,
                committed_from_proposal=commit.proposal_id,
                committed_from_review=commit.review_id,
                source_path=str(item.get("source_path", "")),
                event_id=str(item.get("event_id", "")),
                selection_id=str(item.get("selection_id", "")),
                requested_effect=str(item.get("requested_effect", "")),
                reaction_family=str(item.get("reaction_family", "")),
                authority_status="LANDED_BY_REVIEW",
                graph_state_status="COMMITTED",
            )
            path = node_dir / f"{node.node_id}.template_graph_node.json"
            if self._write_once_or_same(path, _to_jsonable(node)):
                written_nodes += 1
        for item in proposal.get("proposed_edges", []):
            edge = CommittedTemplateGraphEdge(
                edge_id=str(item.get("edge_id", "")),
                edge_type=str(item.get("edge_type", "")),
                committed_at=commit.emitted_at,
                committed_from_proposal=commit.proposal_id,
                committed_from_review=commit.review_id,
                from_node=str(item.get("from_node", "")),
                to_node=str(item.get("to_node", "")),
                source_path=str(item.get("source_path", "")),
                graph_state_status="COMMITTED",
            )
            path = edge_dir / f"{edge.edge_id}.template_graph_edge.json"
            if self._write_once_or_same(path, _to_jsonable(edge)):
                written_edges += 1
        return written_nodes, written_edges

    def write_commit_record(self, workspace_root: Path, commit: TemplateGraphCommitRecord) -> Path:
        output_dir = Path(workspace_root) / "ION/05_context/history/template_graph_commits"
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"{commit.commit_id}.template_graph_commit.json"
        self._write_once_or_same(path, _to_jsonable(commit))
        return path

    def write_commit_receipt(self, workspace_root: Path, receipt: TemplateGraphCommitReceipt) -> Path:
        output_dir = Path(workspace_root) / "ION/05_context/history/template_graph_commit_receipts"
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"{receipt.receipt_id}.template_graph_commit_receipt.json"
        self._write_once_or_same(path, _to_jsonable(receipt))
        return path

    def _land_review_paths(self, root: Path) -> tuple[Path, ...]:
        review_dir = root / "ION/05_context/history/template_graph_writeback_reviews"
        paths: list[Path] = []
        for path in sorted(review_dir.glob("*.template_graph_writeback_review.json")):
            try:
                data = self._load_review(path)
            except KernelTemplateGraphCommitError:
                continue
            if data.get("verdict") == "LAND" and data.get("accepted_for_later_graph_commit") is True:
                paths.append(path)
        return tuple(paths)

    def _review_has_commit(self, root: Path, review_id: str) -> bool:
        commit_dir = root / "ION/05_context/history/template_graph_commits"
        if not commit_dir.exists():
            return False
        for path in commit_dir.glob("*.template_graph_commit.json"):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            if data.get("review_id") == review_id:
                return True
        return False

    def _load_review(self, review_path: Path) -> dict[str, Any]:
        path = Path(review_path)
        if not path.exists():
            raise KernelTemplateGraphCommitError(f"review path does not exist: {path}")
        review = json.loads(path.read_text(encoding="utf-8"))
        if review.get("review_type") != "TEMPLATE_GRAPH_WRITEBACK_REVIEW_VERDICT":
            raise KernelTemplateGraphCommitError(f"not a template graph writeback review: {path}")
        return review

    def _load_proposal(self, root: Path, proposal_path: Path) -> dict[str, Any]:
        path = Path(proposal_path)
        if not path.exists():
            raise KernelTemplateGraphCommitError(f"proposal path does not exist: {path}")
        proposal = json.loads(path.read_text(encoding="utf-8"))
        if proposal.get("proposal_type") != "TEMPLATE_GRAPH_WRITEBACK_PROPOSAL":
            raise KernelTemplateGraphCommitError(f"not a template graph writeback proposal: {path}")
        if proposal.get("proposal_only") is not True:
            raise KernelTemplateGraphCommitError("proposal must be proposal_only=true before Phase 6 commit")
        return proposal

    def _write_once_or_same(self, path: Path, payload: dict[str, Any]) -> bool:
        text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        if path.exists():
            if path.read_text(encoding="utf-8") != text:
                raise KernelTemplateGraphCommitError(f"refusing to overwrite different graph state: {path}")
            return False
        path.write_text(text, encoding="utf-8")
        return True

    @staticmethod
    def _stable_id(prefix: str, *parts: str) -> str:
        digest = hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()[:16]
        return f"{prefix}-{digest}"


IonTemplateGraphCommitter = KernelTemplateGraphCommitter
IonTemplateGraphCommitError = KernelTemplateGraphCommitError


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
