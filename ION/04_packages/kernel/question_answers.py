"""First-pass reviewer/follow-up answer ingestion and projection helpers.

This module sits one layer above open-question state. It does not claim a full reviewer
runtime or autonomous answer-resolution daemon already exists. It provides three smaller
truthful steps the current stack can support today:

1. accept one explicit bounded answer for one existing review/follow-up question,
   persist that answer as runtime state, and resolve the question through the canonical
   question-resolution path;
2. expose narrow reviewer-facing queue/projection surfaces so persisted answer records
   can be browsed by reviewer/domain/work-unit without relying only on per-question
   lookup; and
3. refresh persisted queue projections in bounded batches when later question/answer
   state makes an older projection stale.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from .graph import KernelGraph
from .index import KernelIndex
from .name_lineage import KernelNameLineageError, KernelNameLineageManager, NameIngressSurface
from .model import (
    KernelRecord,
    OpenQuestion,
    OpenQuestionPriority,
    OpenQuestionStatus,
    QuestionAnswerRecord,
    ReviewerAnswerQueueProjectionRecord,
    ReviewerQueueRefreshReceipt,
    ScopeType,
    SpawnPolicy,
    WorkPriority,
    WorkUnit,
    WorkUnitStatus,
)
from .questions import KernelQuestionRouter, QuestionResolutionResult
from .reviews import REVIEW_DOMAIN
from .signal_followups import SIGNAL_FOLLOWUP_DOMAIN
from .store import KernelStore


_SUPPORTED_DOMAINS = frozenset({REVIEW_DOMAIN, SIGNAL_FOLLOWUP_DOMAIN})
_RESOLVABLE_STATUSES = frozenset({OpenQuestionStatus.OPEN, OpenQuestionStatus.ASSIGNED})
_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")
_PRIORITY_ORDER = {
    OpenQuestionPriority.P0_BLOCKING: 0,
    OpenQuestionPriority.P1_HIGH: 1,
    OpenQuestionPriority.P2_NORMAL: 2,
    OpenQuestionPriority.P3_LOW: 3,
}


class KernelQuestionAnswerError(Exception):
    """Raised when one bounded question-answer ingestion cannot be completed lawfully."""


@dataclass(frozen=True)
class QuestionAnswerSubmission(KernelRecord):
    """Bounded explicit answer payload for one existing question."""

    question_id: str
    answered_by: str
    resolution: str
    resolution_evidence: tuple[str, ...] = ()
    answered_at: str | None = None
    notes: str | None = None


@dataclass(frozen=True)
class QuestionAnswerPreparation:
    """Validated question plus the explicit bounded answer to apply."""

    question: OpenQuestion
    work_unit: WorkUnit
    synthesized_work_unit: WorkUnit | None
    submission: QuestionAnswerSubmission
    answer_record: QuestionAnswerRecord


@dataclass(frozen=True)
class QuestionAnswerResult:
    """Result of resolving one review/follow-up question from explicit answer input."""

    preparation: QuestionAnswerPreparation
    persisted_answer: QuestionAnswerRecord
    resolution_result: QuestionResolutionResult


@dataclass(frozen=True)
class QuestionAnswerProjection:
    """Join one persisted answer record back to its question and parent work unit."""

    answer: QuestionAnswerRecord
    question: OpenQuestion
    work_unit: WorkUnit


@dataclass(frozen=True)
class ReviewerAnswerQueue:
    """Minimal reviewer-facing queue surface over pending questions and recent answers."""

    reviewer: str | None
    domains: tuple[str, ...]
    pending_questions: tuple[OpenQuestion, ...]
    recent_answers: tuple[QuestionAnswerProjection, ...]


@dataclass(frozen=True)
class ReviewerAnswerQueueProjectionResult:
    """Durable generated-state witness for one reviewer-facing queue view."""

    projection: ReviewerAnswerQueueProjectionRecord
    queue: ReviewerAnswerQueue


@dataclass(frozen=True)
class ReviewerQueueRefreshCandidate:
    """One persisted queue projection that no longer matches current runtime state."""

    projection: ReviewerAnswerQueueProjectionRecord
    reason: str


@dataclass(frozen=True)
class ReviewerQueueRefreshResult:
    """Result of refreshing one stale persisted reviewer queue projection."""

    previous_projection: ReviewerAnswerQueueProjectionRecord
    refreshed_result: ReviewerAnswerQueueProjectionResult
    reason: str


@dataclass(frozen=True)
class ReviewerQueueRefreshSweepResult:
    """Result of refreshing a bounded stale reviewer-queue batch plus one receipt."""

    receipt: ReviewerQueueRefreshReceipt
    refreshed_results: tuple[ReviewerQueueRefreshResult, ...]
    candidates: tuple[ReviewerQueueRefreshCandidate, ...]


class KernelQuestionAnswerIngestor:
    """Resolve one existing review/follow-up question from one explicit answer payload."""

    def __init__(
        self,
        *,
        question_router: KernelQuestionRouter | None = None,
        lineage_manager: KernelNameLineageManager | None = None,
    ) -> None:
        self._question_router = question_router or KernelQuestionRouter()
        self._lineage_manager = lineage_manager or KernelNameLineageManager()

    def prepare_ingestion(
        self,
        index: KernelIndex,
        submission: QuestionAnswerSubmission,
    ) -> QuestionAnswerPreparation:
        question = index.get("open_question", submission.question_id)
        if not isinstance(question, OpenQuestion):
            raise KernelQuestionAnswerError(
                f"Unknown open question: {submission.question_id}"
            )
        if question.domain not in _SUPPORTED_DOMAINS:
            raise KernelQuestionAnswerError(
                "Question domain is not supported for explicit answer ingestion: "
                f"{question.question_id} ({question.domain})"
            )
        if index.question_answers_for_question(question.question_id):
            raise KernelQuestionAnswerError(
                "Question already has a persisted answer record and cannot be ingested twice: "
                f"{question.question_id}"
            )
        if question.status not in _RESOLVABLE_STATUSES:
            raise KernelQuestionAnswerError(
                "Open question is not answerable from its current status: "
                f"{question.question_id} ({question.status})"
            )

        answered_by = submission.answered_by.strip()
        if not answered_by:
            raise KernelQuestionAnswerError("answered_by must be non-empty.")
        resolution = submission.resolution.strip()
        if not resolution:
            raise KernelQuestionAnswerError("resolution must be non-empty.")

        synthesized_work_unit: WorkUnit | None = None
        work_unit = index.get("work_unit", question.origin_work_unit)
        if not isinstance(work_unit, WorkUnit):
            if question.domain != SIGNAL_FOLLOWUP_DOMAIN:
                raise KernelQuestionAnswerError(
                    "Answer ingestion requires the origin work unit to exist: "
                    f"{question.question_id} -> {question.origin_work_unit}"
                )
            synthesized_work_unit = _build_signal_follow_up_work_unit(question)
            work_unit = synthesized_work_unit

        try:
            name_resolution = self._lineage_manager.resolve_required_name(
                answered_by,
                surface=NameIngressSurface.ANSWER_INGEST,
            )
        except KernelNameLineageError as exc:
            raise KernelQuestionAnswerError(
                "Explicit answer ingestion requires a live authority name: "
                f"{answered_by}. {exc}"
            ) from exc

        normalized_submission = QuestionAnswerSubmission(
            question_id=submission.question_id,
            answered_by=name_resolution.resolved_name or answered_by,
            resolution=resolution,
            resolution_evidence=tuple(submission.resolution_evidence),
            answered_at=submission.answered_at,
            notes=submission.notes.strip() if submission.notes is not None else None,
        )
        answer_record = QuestionAnswerRecord(
            answer_id=question_answer_id(question.question_id, normalized_submission.answered_at),
            created_at=normalized_submission.answered_at or question.created_at,
            question_id=question.question_id,
            work_unit_id=work_unit.work_unit_id,
            protocol_id=work_unit.protocol_id,
            transition_id=work_unit.transition_id,
            context_version=work_unit.context_version,
            question_domain=question.domain,
            answered_by=normalized_submission.answered_by,
            answered_by_raw=(None if name_resolution.raw_name == normalized_submission.answered_by else name_resolution.raw_name),
            answered_by_resolution_note=self._lineage_manager.render_resolution_note(name_resolution),
            resolution=normalized_submission.resolution,
            resolution_evidence=normalized_submission.resolution_evidence,
            notes=normalized_submission.notes,
        )
        if index.exists("question_answer", answer_record.answer_id):
            raise KernelQuestionAnswerError(
                "Question already has a persisted answer record for this answer timestamp: "
                f"{answer_record.answer_id}"
            )
        return QuestionAnswerPreparation(
            question=question,
            work_unit=work_unit,
            synthesized_work_unit=synthesized_work_unit,
            submission=normalized_submission,
            answer_record=answer_record,
        )

    def ingest_answer(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        submission: QuestionAnswerSubmission,
    ) -> QuestionAnswerResult:
        preparation = self.prepare_ingestion(index, submission)
        if (
            preparation.synthesized_work_unit is not None
            and not index.exists("work_unit", preparation.synthesized_work_unit.work_unit_id)
        ):
            store.create(preparation.synthesized_work_unit)
            index.record_added(preparation.synthesized_work_unit)
        store.create(preparation.answer_record)
        index.record_added(preparation.answer_record)
        resolution_result = self._question_router.resolve_question(
            store,
            index,
            graph,
            preparation.question.question_id,
            resolved_by=preparation.submission.answered_by,
            resolution=preparation.submission.resolution,
            resolution_evidence=preparation.submission.resolution_evidence,
            resolved_at=preparation.submission.answered_at,
        )
        return QuestionAnswerResult(
            preparation=preparation,
            persisted_answer=preparation.answer_record,
            resolution_result=resolution_result,
        )


class KernelQuestionAnswerProjectionBuilder:
    """Render narrow reviewer-facing queue/projection surfaces from persisted answers."""

    def projection_for_answer(self, index: KernelIndex, answer_id: str) -> QuestionAnswerProjection:
        answer = index.get("question_answer", answer_id)
        if not isinstance(answer, QuestionAnswerRecord):
            raise KernelQuestionAnswerError(f"Unknown question answer record: {answer_id}")
        return self._projection_from_answer(index, answer)

    def recent_answers(
        self,
        index: KernelIndex,
        *,
        reviewer: str | None = None,
        domains: tuple[str, ...] | None = None,
        answered_by: str | None = None,
        limit: int | None = None,
    ) -> tuple[QuestionAnswerProjection, ...]:
        allowed_domains = _normalize_domains(domains)
        projections: list[QuestionAnswerProjection] = []
        for answer in index.records_by_type("question_answer"):
            if not isinstance(answer, QuestionAnswerRecord):
                continue
            if answer.question_domain not in allowed_domains:
                continue
            if answered_by is not None and answer.answered_by != answered_by:
                continue
            projection = self._projection_from_answer(index, answer)
            if reviewer is not None and projection.question.needed_from != reviewer:
                continue
            projections.append(projection)
        projections.sort(key=lambda item: (item.answer.created_at, item.answer.answer_id), reverse=True)
        if limit is not None:
            projections = projections[:limit]
        return tuple(projections)

    def pending_questions(
        self,
        index: KernelIndex,
        *,
        reviewer: str | None = None,
        domains: tuple[str, ...] | None = None,
        limit: int | None = None,
    ) -> tuple[OpenQuestion, ...]:
        allowed_domains = _normalize_domains(domains)
        pending: list[OpenQuestion] = []
        for status in (OpenQuestionStatus.OPEN, OpenQuestionStatus.ASSIGNED):
            for question in index.open_questions_by_status(status):
                if question.domain not in allowed_domains:
                    continue
                if reviewer is not None and question.needed_from != reviewer:
                    continue
                if index.question_answers_for_question(question.question_id):
                    continue
                pending.append(question)
        pending.sort(key=lambda item: (_PRIORITY_ORDER[item.priority], item.created_at, item.question_id))
        if limit is not None:
            pending = pending[:limit]
        return tuple(pending)

    def reviewer_queue(
        self,
        index: KernelIndex,
        *,
        reviewer: str | None = None,
        domains: tuple[str, ...] | None = None,
        pending_limit: int | None = None,
        answer_limit: int | None = None,
    ) -> ReviewerAnswerQueue:
        allowed_domains = _normalize_domains(domains)
        return ReviewerAnswerQueue(
            reviewer=reviewer,
            domains=allowed_domains,
            pending_questions=self.pending_questions(
                index,
                reviewer=reviewer,
                domains=allowed_domains,
                limit=pending_limit,
            ),
            recent_answers=self.recent_answers(
                index,
                reviewer=reviewer,
                domains=allowed_domains,
                limit=answer_limit,
            ),
        )

    def build_reviewer_queue_projection(
        self,
        index: KernelIndex,
        *,
        reviewer: str | None = None,
        domains: tuple[str, ...] | None = None,
        pending_limit: int | None = None,
        answer_limit: int | None = None,
        generated_at: str | None = None,
    ) -> ReviewerAnswerQueueProjectionResult:
        allowed_domains = _normalize_domains(domains)
        queue = self.reviewer_queue(
            index,
            reviewer=reviewer,
            domains=allowed_domains,
            pending_limit=pending_limit,
            answer_limit=answer_limit,
        )
        full_pending = self.pending_questions(index, reviewer=reviewer, domains=allowed_domains, limit=None)
        full_recent = self.recent_answers(index, reviewer=reviewer, domains=allowed_domains, limit=None)
        projection = ReviewerAnswerQueueProjectionRecord(
            projection_id=reviewer_queue_projection_id(
                reviewer,
                allowed_domains,
                pending_limit=pending_limit,
                answer_limit=answer_limit,
            ),
            generated_at=generated_at or _iso_now(),
            reviewer=reviewer,
            domains=allowed_domains,
            pending_question_ids=tuple(question.question_id for question in queue.pending_questions),
            recent_answer_ids=tuple(item.answer.answer_id for item in queue.recent_answers),
            pending_total_count=len(full_pending),
            recent_answer_total_count=len(full_recent),
            pending_limit=pending_limit,
            answer_limit=answer_limit,
        )
        return ReviewerAnswerQueueProjectionResult(projection=projection, queue=queue)

    def persist_reviewer_queue_projection(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        *,
        reviewer: str | None = None,
        domains: tuple[str, ...] | None = None,
        pending_limit: int | None = None,
        answer_limit: int | None = None,
        generated_at: str | None = None,
    ) -> ReviewerAnswerQueueProjectionResult:
        result = self.build_reviewer_queue_projection(
            index,
            reviewer=reviewer,
            domains=domains,
            pending_limit=pending_limit,
            answer_limit=answer_limit,
            generated_at=generated_at,
        )
        if index.exists("reviewer_answer_queue", result.projection.projection_id):
            store.replace(result.projection)
            index.record_changed(result.projection)
        else:
            store.create(result.projection)
            index.record_added(result.projection)
        graph.build_from_index(index)
        return result

    def queue_from_projection_record(
        self,
        index: KernelIndex,
        projection_id: str,
    ) -> ReviewerAnswerQueue:
        projection = index.get("reviewer_answer_queue", projection_id)
        if not isinstance(projection, ReviewerAnswerQueueProjectionRecord):
            raise KernelQuestionAnswerError(f"Unknown reviewer queue projection: {projection_id}")
        pending_questions = tuple(
            question
            for question_id in projection.pending_question_ids
            for question in [index.get("open_question", question_id)]
            if isinstance(question, OpenQuestion)
        )
        recent_answers = tuple(self.projection_for_answer(index, answer_id) for answer_id in projection.recent_answer_ids)
        return ReviewerAnswerQueue(
            reviewer=projection.reviewer,
            domains=projection.domains,
            pending_questions=pending_questions,
            recent_answers=recent_answers,
        )

    def discover_refresh_candidates(
        self,
        index: KernelIndex,
    ) -> tuple[ReviewerQueueRefreshCandidate, ...]:
        candidates: list[ReviewerQueueRefreshCandidate] = []
        for projection in index.records_by_type("reviewer_answer_queue"):
            if not isinstance(projection, ReviewerAnswerQueueProjectionRecord):
                continue
            reason = self._refresh_reason(index, projection)
            if reason is None:
                continue
            candidates.append(ReviewerQueueRefreshCandidate(projection=projection, reason=reason))
        candidates.sort(key=lambda item: (item.projection.generated_at, item.projection.projection_id))
        return tuple(candidates)

    def refresh_projection(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        projection_id: str,
        *,
        generated_at: str | None = None,
    ) -> ReviewerQueueRefreshResult:
        projection = index.get("reviewer_answer_queue", projection_id)
        if not isinstance(projection, ReviewerAnswerQueueProjectionRecord):
            raise KernelQuestionAnswerError(f"Unknown reviewer queue projection: {projection_id}")
        reason = self._refresh_reason(index, projection) or "FORCED_REFRESH"
        refreshed = self.persist_reviewer_queue_projection(
            store,
            index,
            graph,
            reviewer=projection.reviewer,
            domains=projection.domains,
            pending_limit=projection.pending_limit,
            answer_limit=projection.answer_limit,
            generated_at=generated_at,
        )
        return ReviewerQueueRefreshResult(
            previous_projection=projection,
            refreshed_result=refreshed,
            reason=reason,
        )

    def refresh_stale_projections(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        *,
        generated_at: str | None = None,
    ) -> tuple[ReviewerQueueRefreshResult, ...]:
        results: list[ReviewerQueueRefreshResult] = []
        for candidate in self.discover_refresh_candidates(index):
            results.append(
                self.refresh_projection(
                    store,
                    index,
                    graph,
                    candidate.projection.projection_id,
                    generated_at=generated_at,
                )
            )
        return tuple(results)

    def recent_refresh_receipts(
        self,
        index: KernelIndex,
        *,
        limit: int | None = None,
        generated_by: str | None = None,
    ) -> tuple[ReviewerQueueRefreshReceipt, ...]:
        receipts = [
            record
            for record in index.records_by_type("reviewer_queue_refresh")
            if isinstance(record, ReviewerQueueRefreshReceipt)
        ]
        if generated_by is not None:
            receipts = [record for record in receipts if record.generated_by == generated_by]
        receipts.sort(key=lambda item: (item.generated_at, item.receipt_id), reverse=True)
        if limit is not None:
            receipts = receipts[:limit]
        return tuple(receipts)

    def sweep_refresh_candidates(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        *,
        generated_at: str | None = None,
        generated_by: str = "DAEMON",
    ) -> ReviewerQueueRefreshSweepResult | None:
        candidates = self.discover_refresh_candidates(index)
        if not candidates:
            return None
        refreshed_results: list[ReviewerQueueRefreshResult] = []
        for candidate in candidates:
            refreshed_results.append(
                self.refresh_projection(
                    store,
                    index,
                    graph,
                    candidate.projection.projection_id,
                    generated_at=generated_at,
                )
            )
        receipt_timestamp = generated_at or _iso_now()
        receipt = ReviewerQueueRefreshReceipt(
            receipt_id=reviewer_queue_refresh_receipt_id(receipt_timestamp),
            generated_at=receipt_timestamp,
            refreshed_projection_ids=tuple(
                item.refreshed_result.projection.projection_id for item in refreshed_results
            ),
            reasons=tuple(item.reason for item in refreshed_results),
            candidate_count=len(candidates),
            refreshed_count=len(refreshed_results),
            generated_by=generated_by.strip() or "DAEMON",
        )
        if index.exists("reviewer_queue_refresh", receipt.receipt_id):
            store.replace(receipt)
            index.record_changed(receipt)
        else:
            store.create(receipt)
            index.record_added(receipt)
        graph.build_from_index(index)
        return ReviewerQueueRefreshSweepResult(
            receipt=receipt,
            refreshed_results=tuple(refreshed_results),
            candidates=candidates,
        )

    def _refresh_reason(
        self,
        index: KernelIndex,
        projection: ReviewerAnswerQueueProjectionRecord,
    ) -> str | None:
        current = self.build_reviewer_queue_projection(
            index,
            reviewer=projection.reviewer,
            domains=projection.domains,
            pending_limit=projection.pending_limit,
            answer_limit=projection.answer_limit,
            generated_at=projection.generated_at,
        ).projection
        if current.recent_answer_ids != projection.recent_answer_ids:
            return "ANSWER_SET_CHANGED"
        if current.pending_question_ids != projection.pending_question_ids:
            return "PENDING_SET_CHANGED"
        if current.pending_total_count != projection.pending_total_count:
            return "PENDING_TOTAL_CHANGED"
        if current.recent_answer_total_count != projection.recent_answer_total_count:
            return "ANSWER_TOTAL_CHANGED"
        for question_id in projection.pending_question_ids:
            if not isinstance(index.get("open_question", question_id), OpenQuestion):
                return "BROKEN_PENDING_REFERENCE"
        for answer_id in projection.recent_answer_ids:
            if not isinstance(index.get("question_answer", answer_id), QuestionAnswerRecord):
                return "BROKEN_ANSWER_REFERENCE"
        return None

    def _projection_from_answer(
        self,
        index: KernelIndex,
        answer: QuestionAnswerRecord,
    ) -> QuestionAnswerProjection:
        question = index.get("open_question", answer.question_id)
        if not isinstance(question, OpenQuestion):
            raise KernelQuestionAnswerError(
                "Question answer record is missing its linked open question: "
                f"{answer.answer_id} -> {answer.question_id}"
            )
        work_unit = index.get("work_unit", answer.work_unit_id)
        if not isinstance(work_unit, WorkUnit):
            raise KernelQuestionAnswerError(
                "Question answer record is missing its linked work unit: "
                f"{answer.answer_id} -> {answer.work_unit_id}"
            )
        return QuestionAnswerProjection(answer=answer, question=question, work_unit=work_unit)


IonQuestionAnswerIngestor = KernelQuestionAnswerIngestor
IonQuestionAnswerProjectionBuilder = KernelQuestionAnswerProjectionBuilder


def question_answer_id(question_id: str, answered_at: str | None) -> str:
    safe_question = _SAFE_ID_RE.sub("-", question_id.lower()).strip("-") or "question"
    safe_time = _SAFE_ID_RE.sub("-", (answered_at or "explicit-answer").lower()).strip("-")
    return f"answer-{safe_question}-{safe_time}"


def reviewer_queue_projection_id(
    reviewer: str | None,
    domains: tuple[str, ...],
    *,
    pending_limit: int | None,
    answer_limit: int | None,
) -> str:
    reviewer_text = _SAFE_ID_RE.sub("-", (reviewer or "all").lower()).strip("-") or "all"
    domain_text = "-".join(_SAFE_ID_RE.sub("-", domain.lower()).strip("-") for domain in domains) or "domains"
    pending_text = str(pending_limit) if pending_limit is not None else "all"
    answer_text = str(answer_limit) if answer_limit is not None else "all"
    return f"reviewer-queue-{reviewer_text}-{domain_text}-p{pending_text}-a{answer_text}"


def reviewer_queue_refresh_receipt_id(generated_at: str) -> str:
    safe = _SAFE_ID_RE.sub("-", generated_at.lower()).strip("-") or "queue-refresh"
    return f"reviewer-queue-refresh-{safe}"


def _normalize_domains(domains: tuple[str, ...] | None) -> tuple[str, ...]:
    if domains is None:
        return tuple(sorted(_SUPPORTED_DOMAINS))
    normalized = tuple(domain for domain in domains if domain in _SUPPORTED_DOMAINS)
    if not normalized:
        raise KernelQuestionAnswerError("domains must include at least one supported reviewer/follow-up domain.")
    return normalized


def _build_signal_follow_up_work_unit(question: OpenQuestion) -> WorkUnit:
    scope_ref = (
        question.scope_ref
        or next((item for item in question.linked_artifacts if item), question.origin_work_unit)
    )
    return WorkUnit(
        work_unit_id=question.origin_work_unit,
        created_at=question.created_at,
        protocol_id="SIGNAL.follow_up",
        transition_id=question.origin_transition or "FOLLOW_UP",
        context_version=f"ctx-{question.origin_work_unit}",
        agent_personal_name=question.origin_agent or "UNKNOWN",
        agent_role="SignalFollowUpOrigin",
        agent_structural_id="T4.Runtime.SignalFollowUp",
        agent_tier=4,
        agent_domain=question.domain,
        chassis="daemon-signal-followup",
        scope_type=_scope_type_for_scope_ref(scope_ref),
        scope_ref=scope_ref,
        bound_template="RESEARCH",
        input_refs=(),
        context_package_id=f"cp-{question.origin_work_unit}",
        allowed_writes=tuple(item for item in question.linked_artifacts if item),
        allowed_next_actions=("ANSWER_QUESTION",),
        priority=_work_priority_from_question(question.priority),
        status=WorkUnitStatus.BLOCKED,
        open_questions_in_scope=(question.question_id,),
        spawn_policy=SpawnPolicy(may_spawn=False),
        expected_output_schema="QuestionAnswerRecord",
    )


def _scope_type_for_scope_ref(scope_ref: str) -> ScopeType:
    return ScopeType.FILE if Path(scope_ref).suffix else ScopeType.PROJECT


def _work_priority_from_question(priority: OpenQuestionPriority) -> WorkPriority:
    if priority is OpenQuestionPriority.P0_BLOCKING:
        return WorkPriority.P0_CRITICAL
    if priority is OpenQuestionPriority.P1_HIGH:
        return WorkPriority.P1_HIGH
    if priority is OpenQuestionPriority.P2_NORMAL:
        return WorkPriority.P2_NORMAL
    return WorkPriority.P3_LOW


def _iso_now() -> str:
    from datetime import datetime

    return datetime.now().astimezone().replace(microsecond=0).isoformat()
