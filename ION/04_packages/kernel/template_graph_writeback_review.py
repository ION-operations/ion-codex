"""LAND/HOLD/ESCALATE review for template graph writeback proposals.

This module implements Phase 5 of the Evented Template File Graph pipeline. It
reviews Phase 4 TEMPLATE_GRAPH_WRITEBACK_PROPOSAL records and emits durable
verdict witnesses plus receipts.

It intentionally does not mutate source graph state. A LAND verdict means the
proposal is accepted as eligible for a later governed graph-commit phase; it is
not itself graph truth.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


class KernelTemplateGraphWritebackReviewError(Exception):
    """Raised when a graph writeback proposal review cannot proceed lawfully."""


_ALLOWED_VERDICTS = {"LAND", "HOLD", "ESCALATE"}


@dataclass(frozen=True)
class TemplateGraphWritebackReviewVerdict:
    """A durable review verdict over one Phase 4 graph writeback proposal.

    This is a review/landing witness, not source graph mutation. LAND authorizes
    later bounded graph writeback work to use the proposal as an accepted input.
    HOLD and ESCALATE preserve the proposal and its blocker/defect reason.
    """

    review_id: str
    review_type: str
    emitted_at: str
    phase: str
    proposal_id: str
    proposal_path: str
    reviewer: str
    verdict: str
    reason: str
    accepted_for_later_graph_commit: bool
    source_graph_mutation_blocked: bool
    proposed_node_count: int
    proposed_edge_count: int
    deferred_reaction_count: int
    proposed_node_ids: tuple[str, ...]
    proposed_edge_ids: tuple[str, ...]
    deferred_reaction_keys: tuple[str, ...]
    notes: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True)
class TemplateGraphWritebackReviewReceipt:
    """Receipt emitted for one Phase 5 proposal review pass."""

    receipt_id: str
    emitted_at: str
    scanned_root: str
    reviewed_proposal_count: int
    land_count: int
    hold_count: int
    escalate_count: int
    review_paths: tuple[str, ...]
    source_graph_mutation_blocked: bool


class KernelTemplateGraphWritebackReviewer:
    """Review Phase 4 graph writeback proposals with LAND/HOLD/ESCALATE verdicts."""

    def review_from_workspace(
        self,
        workspace_root: Path,
        *,
        verdict: str,
        reviewer: str = "Steward",
        reason: str = "Phase 5 governed graph writeback review.",
        emitted_at: str | None = None,
        only_unreviewed: bool = True,
    ) -> TemplateGraphWritebackReviewReceipt:
        """Review all proposal files in the workspace with one explicit verdict.

        This helper is intentionally simple and bounded for Phase 5. It applies
        one operator/agent verdict to every unreviewed Phase 4 proposal in the
        proposal directory and emits one aggregate receipt. Later phases may add
        per-proposal mixed verdicts through a richer review packet.
        """

        root = Path(workspace_root)
        if not root.exists():
            raise KernelTemplateGraphWritebackReviewError(f"workspace root does not exist: {root}")
        timestamp = emitted_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        proposal_dir = root / "ION/05_context/history/template_graph_writeback_proposals"
        proposal_paths = tuple(sorted(proposal_dir.glob("*.template_graph_writeback_proposal.json")))
        if not proposal_paths:
            raise KernelTemplateGraphWritebackReviewError("no template graph writeback proposals found")

        review_paths: list[str] = []
        land_count = hold_count = escalate_count = 0
        for proposal_path in proposal_paths:
            proposal = self._load_proposal(root, proposal_path)
            if only_unreviewed and self._proposal_has_review(root, proposal["proposal_id"]):
                continue
            review = self.build_review_verdict(
                root,
                proposal_path,
                verdict=verdict,
                reviewer=reviewer,
                reason=reason,
                emitted_at=timestamp,
            )
            written = self.write_review(root, review)
            review_paths.append(written.relative_to(root).as_posix())
            if review.verdict == "LAND":
                land_count += 1
            elif review.verdict == "HOLD":
                hold_count += 1
            elif review.verdict == "ESCALATE":
                escalate_count += 1

        receipt = TemplateGraphWritebackReviewReceipt(
            receipt_id=self._stable_id("template-graph-writeback-review", timestamp, *review_paths),
            emitted_at=timestamp,
            scanned_root=root.as_posix(),
            reviewed_proposal_count=len(review_paths),
            land_count=land_count,
            hold_count=hold_count,
            escalate_count=escalate_count,
            review_paths=tuple(review_paths),
            source_graph_mutation_blocked=True,
        )
        self.write_review_receipt(root, receipt)
        return receipt

    def build_review_verdict(
        self,
        workspace_root: Path,
        proposal_path: Path,
        *,
        verdict: str,
        reviewer: str,
        reason: str,
        emitted_at: str,
    ) -> TemplateGraphWritebackReviewVerdict:
        root = Path(workspace_root)
        normalized_verdict = verdict.strip().upper()
        if normalized_verdict not in _ALLOWED_VERDICTS:
            raise KernelTemplateGraphWritebackReviewError(
                f"invalid graph writeback review verdict: {verdict!r}; expected LAND, HOLD, or ESCALATE"
            )
        if not reviewer.strip():
            raise KernelTemplateGraphWritebackReviewError("reviewer is required")
        if not reason.strip():
            raise KernelTemplateGraphWritebackReviewError("reason is required")

        proposal = self._load_proposal(root, proposal_path)
        proposed_nodes = proposal.get("proposed_nodes", [])
        proposed_edges = proposal.get("proposed_edges", [])
        deferred_reactions = proposal.get("deferred_reactions", [])
        if normalized_verdict == "LAND" and not proposed_nodes and not proposed_edges:
            raise KernelTemplateGraphWritebackReviewError("cannot LAND an empty graph writeback proposal")

        rel = Path(proposal_path).relative_to(root).as_posix() if Path(proposal_path).is_relative_to(root) else Path(proposal_path).as_posix()
        node_ids = tuple(str(item.get("node_id", "")) for item in proposed_nodes)
        edge_ids = tuple(str(item.get("edge_id", "")) for item in proposed_edges)
        deferred_keys = tuple(
            self._stable_id(
                "deferred-reaction",
                str(item.get("event_id", "")),
                str(item.get("selection_id", "")),
                str(item.get("requested_effect", "")),
                str(item.get("deferral_reason", "")),
            )
            for item in deferred_reactions
        )
        review_id = self._stable_id(
            "template-graph-writeback-review",
            str(proposal.get("proposal_id", "")),
            normalized_verdict,
            reviewer,
            reason,
            emitted_at,
        )
        return TemplateGraphWritebackReviewVerdict(
            review_id=review_id,
            review_type="TEMPLATE_GRAPH_WRITEBACK_REVIEW_VERDICT",
            emitted_at=emitted_at,
            phase="PHASE_5_LAND_HOLD_ESCALATE_REVIEW",
            proposal_id=str(proposal.get("proposal_id", "")),
            proposal_path=rel,
            reviewer=reviewer,
            verdict=normalized_verdict,
            reason=reason,
            accepted_for_later_graph_commit=normalized_verdict == "LAND",
            source_graph_mutation_blocked=True,
            proposed_node_count=len(proposed_nodes),
            proposed_edge_count=len(proposed_edges),
            deferred_reaction_count=len(deferred_reactions),
            proposed_node_ids=node_ids,
            proposed_edge_ids=edge_ids,
            deferred_reaction_keys=deferred_keys,
            notes=(
                "Phase 5 review verdict over proposal-only graph writeback surface.",
                "LAND authorizes later graph-commit proposal handling but does not mutate source graph truth.",
                "HOLD and ESCALATE preserve reasons as review evidence without deleting the proposal.",
            ),
        )

    def write_review(self, workspace_root: Path, review: TemplateGraphWritebackReviewVerdict) -> Path:
        output_dir = Path(workspace_root) / "ION/05_context/history/template_graph_writeback_reviews"
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"{review.review_id}.template_graph_writeback_review.json"
        if path.exists():
            return path
        path.write_text(json.dumps(_to_jsonable(review), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def write_review_receipt(self, workspace_root: Path, receipt: TemplateGraphWritebackReviewReceipt) -> Path:
        output_dir = Path(workspace_root) / "ION/05_context/history/template_graph_writeback_review_receipts"
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"{receipt.receipt_id}.template_graph_writeback_review_receipt.json"
        if path.exists():
            return path
        path.write_text(json.dumps(_to_jsonable(receipt), indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def _load_proposal(self, root: Path, proposal_path: Path) -> dict[str, Any]:
        path = Path(proposal_path)
        if not path.exists():
            raise KernelTemplateGraphWritebackReviewError(f"proposal path does not exist: {path}")
        proposal = json.loads(path.read_text(encoding="utf-8"))
        if proposal.get("proposal_type") != "TEMPLATE_GRAPH_WRITEBACK_PROPOSAL":
            raise KernelTemplateGraphWritebackReviewError(f"not a template graph writeback proposal: {path}")
        if proposal.get("proposal_only") is not True:
            raise KernelTemplateGraphWritebackReviewError("proposal must be proposal_only=true")
        if proposal.get("source_graph_mutation_blocked") is not True:
            raise KernelTemplateGraphWritebackReviewError("proposal must preserve source_graph_mutation_blocked=true")
        return proposal

    def _proposal_has_review(self, root: Path, proposal_id: str) -> bool:
        review_dir = root / "ION/05_context/history/template_graph_writeback_reviews"
        if not review_dir.exists():
            return False
        for path in review_dir.glob("*.template_graph_writeback_review.json"):
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            if data.get("proposal_id") == proposal_id:
                return True
        return False

    @staticmethod
    def _stable_id(prefix: str, *parts: str) -> str:
        digest = hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()[:16]
        return f"{prefix}-{digest}"


IonTemplateGraphWritebackReviewer = KernelTemplateGraphWritebackReviewer
IonTemplateGraphWritebackReviewError = KernelTemplateGraphWritebackReviewError


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
