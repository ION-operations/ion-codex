"""Summary-refresh demo runtime.

V22 proves the first narrow release-demo path:

    user text
    -> Persona Interface / Relay / Steward front door
    -> bounded summary-refresh template file
    -> contract-bound Phase 1 completion event
    -> contract-bound Phase 2 reaction selection
    -> Phase 3 projection-only index surface
    -> Phase 4 proposal-only graph writeback surface
    -> Phase 5 governed review verdict surface
    -> Phase 6 bounded graph-state commit
    -> Relay return package
    -> Persona response package

The module is intentionally conservative. It does not rewrite source summaries,
mutate graph truth, activate agents, or claim autonomous completion.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from .front_door_chat_orchestration import (
    FrontDoorChatOrchestrationAdapter,
    FrontDoorChatReturnResult,
    FrontDoorChatTurnResult,
)
from .template_completion_events import (
    KernelTemplateCompletionWatcher,
    TemplateCompletionScanReceipt,
    TemplateCompletionWatchRule,
)
from .template_reaction_selection import (
    KernelTemplateReactionSelector,
    TemplateReactionSelectionScanReceipt,
)
from .template_index_projection import (
    KernelTemplateIndexProjector,
    TemplateIndexProjectionReceipt,
)
from .template_graph_writeback_proposals import (
    KernelTemplateGraphWritebackProposer,
    TemplateGraphWritebackProposalReceipt,
)
from .template_graph_writeback_review import (
    KernelTemplateGraphWritebackReviewer,
    TemplateGraphWritebackReviewReceipt,
)
from .template_graph_commit import (
    KernelTemplateGraphCommitter,
    TemplateGraphCommitReceipt,
)


SUMMARY_REFRESH_TEMPLATE_ID = "demo.summary_refresh_request"
SUMMARY_REFRESH_INBOX_RELATIVE = Path("ION/05_context/inbox/product_mvp")
SUMMARY_REFRESH_HISTORY_RELATIVE = Path("ION/05_context/history/summary_refresh_demo_receipts")


@dataclass(frozen=True)
class SummaryRefreshDemoResult:
    demo_id: str
    emitted_at: str
    request_path: str
    front_door_turn: FrontDoorChatTurnResult
    completion_receipt: TemplateCompletionScanReceipt
    reaction_receipt: TemplateReactionSelectionScanReceipt
    projection_receipt: TemplateIndexProjectionReceipt
    proposal_receipt: TemplateGraphWritebackProposalReceipt
    review_receipt: TemplateGraphWritebackReviewReceipt
    commit_receipt: TemplateGraphCommitReceipt | None
    return_result: FrontDoorChatReturnResult
    mutation_allowed: bool = False


class SummaryRefreshDemoRunner:
    """Run the bounded summary-refresh demo path."""

    def __init__(
        self,
        *,
        front_door_adapter: FrontDoorChatOrchestrationAdapter | None = None,
        completion_watcher: KernelTemplateCompletionWatcher | None = None,
        reaction_selector: KernelTemplateReactionSelector | None = None,
        index_projector: KernelTemplateIndexProjector | None = None,
        graph_proposer: KernelTemplateGraphWritebackProposer | None = None,
        graph_reviewer: KernelTemplateGraphWritebackReviewer | None = None,
        graph_committer: KernelTemplateGraphCommitter | None = None,
    ) -> None:
        self._front_door = front_door_adapter or FrontDoorChatOrchestrationAdapter()
        self._completion_watcher = completion_watcher or KernelTemplateCompletionWatcher()
        self._reaction_selector = reaction_selector or KernelTemplateReactionSelector()
        self._index_projector = index_projector or KernelTemplateIndexProjector()
        self._graph_proposer = graph_proposer or KernelTemplateGraphWritebackProposer()
        self._graph_reviewer = graph_reviewer or KernelTemplateGraphWritebackReviewer()
        self._graph_committer = graph_committer or KernelTemplateGraphCommitter()

    def run(
        self,
        *,
        workspace_root: str | Path,
        raw_user_text: str = "Please refresh the current ION project summary.",
        session_id: str = "summary-refresh-demo-session",
        user_ref: str = "user.sovereign",
        summary_target: str = "ION current project",
        visible_persona_name: str | None = None,
        created_at: str | None = None,
        dispatch: bool = True,
        template_contracts: Mapping[str, Mapping[str, Any]] | None = None,
        review_verdict: str = "LAND",
        reviewer: str = "Steward",
        review_reason: str = "V25 summary-refresh demo review accepts proposal as eligible for later bounded commit.",
        run_bounded_commit: bool = True,
    ) -> SummaryRefreshDemoResult:
        root = Path(workspace_root).resolve()
        emitted = created_at or _utc_now()
        demo_id = _stable_id("summary-refresh-demo", session_id, raw_user_text, emitted)

        front_door_turn = self._front_door.submit_user_turn(
            workspace_root=root,
            raw_user_text=raw_user_text,
            session_id=session_id,
            user_ref=user_ref,
            visible_persona_name=visible_persona_name,
            relation_context_refs=(
                "ION/02_architecture/SUMMARY_REFRESH_DEMO_RUNTIME_PROTOCOL.md",
                "ION/07_templates/product_mvp/SUMMARY_REFRESH_REQUEST.md",
            ),
            carrier_ref="api://summary-refresh-demo",
            root_authority_ref="ION/00_BOOTSTRAP/ROOT_AUTHORITY_BUNDLE.md",
            created_at=emitted,
            dispatch=dispatch,
        )

        request_path = self.write_summary_refresh_request(
            root=root,
            demo_id=demo_id,
            emitted_at=emitted,
            raw_user_text=raw_user_text,
            summary_target=summary_target,
            session_id=session_id,
            front_door_turn=front_door_turn,
        )

        rule = TemplateCompletionWatchRule(
            rule_id="watch.product_mvp.summary_refresh_requests",
            path_glob="ION/05_context/inbox/product_mvp/*.task.md",
            required_fields=("type", "status", "summary_target", "downstream_effects"),
            active_statuses=("READY",),
            template_class=SUMMARY_REFRESH_TEMPLATE_ID,
        )
        completion = self._completion_watcher.scan(
            root,
            rules=(rule,),
            emitted_at=emitted,
            template_contracts=template_contracts,
        )
        reaction = self._reaction_selector.select_from_workspace(
            root,
            emitted_at=emitted,
            template_contracts=template_contracts,
        )
        projection = self._index_projector.project_from_workspace(
            root,
            emitted_at=emitted,
        )
        proposal = self._graph_proposer.propose_from_workspace(
            root,
            emitted_at=emitted,
        )
        review = self._graph_reviewer.review_from_workspace(
            root,
            verdict=review_verdict,
            reviewer=reviewer,
            reason=review_reason,
            emitted_at=emitted,
        )
        commit = None
        if run_bounded_commit and review.land_count > 0:
            commit = self._graph_committer.commit_landed_from_workspace(
                root,
                emitted_at=emitted,
            )

        commit_summary = "0 bounded commit(s)"
        if commit is not None:
            commit_summary = (
                f"{commit.committed_review_count} bounded commit(s), "
                f"{commit.committed_node_count} committed bounded node(s), "
                f"{commit.committed_edge_count} committed bounded edge(s)"
            )

        controlled_output = (
            "Summary-refresh demo path completed as a bounded projection witness, bounded graph-proposal witness, governed review witness, and bounded graph-state commit witness: "
            f"{completion.completed_count} completion event(s), "
            f"{reaction.selected_reaction_count} selected dry-run reaction(s), "
            f"{reaction.refused_reaction_count} refused reaction(s), "
            f"{projection.projected_entry_count} projection entrie(s), "
            f"{projection.deferred_reaction_count} deferred reaction(s), "
            f"{proposal.proposed_node_count} proposed graph node(s), "
            f"{proposal.proposed_edge_count} proposed graph edge(s), "
            f"{proposal.deferred_reaction_count} proposal deferral(s), "
            f"{review.reviewed_proposal_count} reviewed proposal(s), "
            f"{review.land_count} LAND review(s), "
            f"{review.hold_count} HOLD review(s), "
            f"{review.escalate_count} ESCALATE review(s), "
            f"{commit_summary}. "
            "No source summary or graph truth was mutated; No source summary or source graph truth was mutated."
        )
        return_result = self._front_door.prepare_system_return(
            workspace_root=root,
            controlled_system_output=controlled_output,
            session_id=session_id,
            user_ref=user_ref,
            source_system_ref=demo_id,
            visible_persona_name=visible_persona_name,
            style_notes=("bounded release demo", "preserve Persona / Relay / Steward role split"),
            created_at=emitted,
        )

        result = SummaryRefreshDemoResult(
            demo_id=demo_id,
            emitted_at=emitted,
            request_path=request_path.relative_to(root).as_posix(),
            front_door_turn=front_door_turn,
            completion_receipt=completion,
            reaction_receipt=reaction,
            projection_receipt=projection,
            proposal_receipt=proposal,
            review_receipt=review,
            commit_receipt=commit,
            return_result=return_result,
        )
        self.write_demo_receipt(root, result)
        return result

    def write_summary_refresh_request(
        self,
        *,
        root: Path,
        demo_id: str,
        emitted_at: str,
        raw_user_text: str,
        summary_target: str,
        session_id: str,
        front_door_turn: FrontDoorChatTurnResult,
    ) -> Path:
        output_dir = root / SUMMARY_REFRESH_INBOX_RELATIVE
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"{demo_id}.task.md"
        if path.exists():
            return path

        downstream_effects = ("update_index", "refresh_context_package_source")
        content = (
            "---\n"
            f"type: {SUMMARY_REFRESH_TEMPLATE_ID}\n"
            "status: READY\n"
            f"summary_target: {summary_target}\n"
            f"session_id: {session_id}\n"
            f"demo_id: {demo_id}\n"
            f"front_door_work_unit_id: {front_door_turn.steward_work_unit.work_unit_id}\n"
            f"relay_packet_id: {front_door_turn.ingress.relay_packet.packet_id}\n"
            f"steward_envelope_id: {front_door_turn.ingress.steward_envelope.envelope_id}\n"
            "downstream_effects:\n"
            + "".join(f"  - {effect}\n" for effect in downstream_effects)
            + "---\n\n"
            "# Summary Refresh Request\n\n"
            "This is a bounded V22 release-demo task file.\n\n"
            "## User request\n\n"
            f"{raw_user_text}\n\n"
            "## Boundary\n\n"
            "This task may trigger completion/reaction witnesses only. It does not authorize source rewrite.\n"
        )
        path.write_text(content, encoding="utf-8")
        return path

    def write_demo_receipt(self, root: Path, result: SummaryRefreshDemoResult) -> Path:
        output_dir = root / SUMMARY_REFRESH_HISTORY_RELATIVE
        output_dir.mkdir(parents=True, exist_ok=True)
        path = output_dir / f"{result.demo_id}.summary_refresh_demo_receipt.json"
        if path.exists():
            return path
        payload = {
            "demo_id": result.demo_id,
            "emitted_at": result.emitted_at,
            "request_path": result.request_path,
            "completion_receipt_id": result.completion_receipt.receipt_id,
            "completion_count": result.completion_receipt.completed_count,
            "completion_witness_paths": list(result.completion_receipt.witness_paths),
            "reaction_receipt_id": result.reaction_receipt.receipt_id,
            "selected_reaction_count": result.reaction_receipt.selected_reaction_count,
            "refused_reaction_count": result.reaction_receipt.refused_reaction_count,
            "projection_receipt_id": result.projection_receipt.receipt_id,
            "projection_path": result.projection_receipt.projection_path,
            "projected_entry_count": result.projection_receipt.projected_entry_count,
            "projection_deferred_reaction_count": result.projection_receipt.deferred_reaction_count,
            "projection_only": result.projection_receipt.projection_only,
            "proposal_receipt_id": result.proposal_receipt.receipt_id,
            "proposal_path": result.proposal_receipt.proposal_path,
            "proposed_node_count": result.proposal_receipt.proposed_node_count,
            "proposed_edge_count": result.proposal_receipt.proposed_edge_count,
            "proposal_deferred_reaction_count": result.proposal_receipt.deferred_reaction_count,
            "proposal_only": result.proposal_receipt.proposal_only,
            "review_receipt_id": result.review_receipt.receipt_id,
            "review_paths": list(result.review_receipt.review_paths),
            "reviewed_proposal_count": result.review_receipt.reviewed_proposal_count,
            "land_count": result.review_receipt.land_count,
            "hold_count": result.review_receipt.hold_count,
            "escalate_count": result.review_receipt.escalate_count,
            "review_source_graph_mutation_blocked": result.review_receipt.source_graph_mutation_blocked,
            "commit_receipt_id": result.commit_receipt.receipt_id if result.commit_receipt is not None else "",
            "commit_paths": list(result.commit_receipt.commit_paths) if result.commit_receipt is not None else [],
            "committed_review_count": result.commit_receipt.committed_review_count if result.commit_receipt is not None else 0,
            "committed_node_count": result.commit_receipt.committed_node_count if result.commit_receipt is not None else 0,
            "committed_edge_count": result.commit_receipt.committed_edge_count if result.commit_receipt is not None else 0,
            "bounded_graph_commit": result.commit_receipt.bounded_graph_commit if result.commit_receipt is not None else False,
            "commit_source_file_mutation_blocked": result.commit_receipt.source_file_mutation_blocked if result.commit_receipt is not None else True,
            "commit_registry_mutation_blocked": result.commit_receipt.registry_mutation_blocked if result.commit_receipt is not None else True,
            "commit_schedule_mutation_blocked": result.commit_receipt.schedule_mutation_blocked if result.commit_receipt is not None else True,
            "commit_agent_activation_blocked": result.commit_receipt.agent_activation_blocked if result.commit_receipt is not None else True,
            "persona_response_id": result.return_result.return_result.persona_response.response_id,
            "mutation_allowed": False,
        }
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path


def _utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("\n".join(part for part in parts if part).encode("utf-8")).hexdigest()[:16]
    return f"{prefix}-{digest}"


IonSummaryRefreshDemoRunner = SummaryRefreshDemoRunner
