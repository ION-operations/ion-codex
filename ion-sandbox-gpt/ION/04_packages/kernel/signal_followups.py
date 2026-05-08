"""First-pass signal-triggered follow-up helper for the active ION kernel stack.

This module sits one layer above canonical signal interpretation/consumption. It
does not claim a full replanner, recovery daemon, or reviewer runtime already
exists. It provides the smaller truthful path the current stack can support
today: when a consumed signal already implies one lawful bounded next step,
materialize that next step as durable kernel state, and when a later completion
signal lawfully supersedes earlier review/follow-up pressure, resolve that
pressure into durable question state instead of leaving it open indefinitely.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from .graph import KernelGraph
from .index import KernelIndex
from .model import (
    CommitDelta,
    CommitDeltaStatus,
    OpenQuestion,
    OpenQuestionPriority,
    OpenQuestionStatus,
    ScopeType,
    SpawnPolicy,
    StrEnum,
    WorkPriority,
    WorkUnit,
    WorkUnitStatus,
)
from .questions import KernelQuestionRouter, QuestionResolutionResult
from .reviews import REVIEW_DOMAIN, KernelReviewEscalator, ReviewEscalationResult, has_review_escalation
from .signals import SignalInterpretationResult, SignalRecommendedAction
from .store import KernelStore
from .runtime_state_views import KernelRuntimeStateView, RuntimeStateScopeView


SIGNAL_FOLLOWUP_DOMAIN = "signal_followup"
DEFAULT_SIGNAL_FOLLOW_UP_NEEDED_FROM = "Steward"
_SAFE_ID_RE = re.compile(r"[^0-9a-z]+")


class SignalFollowUpDisposition(StrEnum):
    NO_FOLLOW_UP_REQUIRED = "NO_FOLLOW_UP_REQUIRED"
    CREATED_OPEN_QUESTION = "CREATED_OPEN_QUESTION"
    ESCALATED_REVIEW = "ESCALATED_REVIEW"
    RESOLVED_EXISTING_QUESTIONS = "RESOLVED_EXISTING_QUESTIONS"
    FOLLOW_UP_ALREADY_PRESENT = "FOLLOW_UP_ALREADY_PRESENT"


class KernelSignalFollowUpError(Exception):
    """Raised when one signal-triggered follow-up cannot be completed lawfully."""


@dataclass(frozen=True)
class SignalFollowUpPreparation:
    interpretation_result: SignalInterpretationResult
    disposition: SignalFollowUpDisposition
    follow_up_question: OpenQuestion | None = None
    synthesized_work_unit: WorkUnit | None = None
    questions_to_resolve: tuple[OpenQuestion, ...] = ()


@dataclass(frozen=True)
class SignalFollowUpResult:
    preparation: SignalFollowUpPreparation
    disposition: SignalFollowUpDisposition
    created_question: OpenQuestion | None = None
    review_escalation_result: ReviewEscalationResult | None = None
    resolved_questions: tuple[QuestionResolutionResult, ...] = ()


class KernelSignalFollowUpHandler:
    """Materialize one bounded follow-up from one consumed canonical signal."""

    def __init__(
        self,
        *,
        review_escalator: KernelReviewEscalator | None = None,
        question_router: KernelQuestionRouter | None = None,
        runtime_state_view: KernelRuntimeStateView | None = None,
    ) -> None:
        self._review_escalator = review_escalator or KernelReviewEscalator()
        self._question_router = question_router or KernelQuestionRouter()
        self._runtime_state_view = runtime_state_view or KernelRuntimeStateView()

    def prepare_follow_up(
        self,
        index: KernelIndex,
        interpretation_result: SignalInterpretationResult,
        *,
        followed_up_at: str,
    ) -> SignalFollowUpPreparation:
        interpretation = interpretation_result.interpretation

        if interpretation.recommended_action is SignalRecommendedAction.ACKNOWLEDGE_AND_ARCHIVE:
            questions_to_resolve = _resolvable_questions_for_completion(index, interpretation_result)
            if questions_to_resolve:
                return SignalFollowUpPreparation(
                    interpretation_result=interpretation_result,
                    disposition=SignalFollowUpDisposition.RESOLVED_EXISTING_QUESTIONS,
                    questions_to_resolve=questions_to_resolve,
                )
            return SignalFollowUpPreparation(
                interpretation_result=interpretation_result,
                disposition=SignalFollowUpDisposition.NO_FOLLOW_UP_REQUIRED,
            )

        if interpretation.recommended_action is SignalRecommendedAction.ESCALATE_REQUIRED_ROLE:
            if _can_escalate_review(index, interpretation.work_unit_id, interpretation.delta_id):
                if has_review_escalation(index, interpretation.delta_id):
                    return SignalFollowUpPreparation(
                        interpretation_result=interpretation_result,
                        disposition=SignalFollowUpDisposition.FOLLOW_UP_ALREADY_PRESENT,
                    )
                return SignalFollowUpPreparation(
                    interpretation_result=interpretation_result,
                    disposition=SignalFollowUpDisposition.ESCALATED_REVIEW,
                )

        if has_signal_follow_up(index, interpretation.signal_id):
            return SignalFollowUpPreparation(
                interpretation_result=interpretation_result,
                disposition=SignalFollowUpDisposition.FOLLOW_UP_ALREADY_PRESENT,
            )

        scope_view = self._runtime_state_view.work_unit_view(index, interpretation.work_unit_id)
        question = _build_follow_up_question(
            interpretation_result,
            created_at=followed_up_at,
            scope_view=scope_view,
        )
        synthesized_work_unit = None
        if not isinstance(index.get("work_unit", interpretation.work_unit_id), WorkUnit):
            synthesized_work_unit = _build_follow_up_work_unit(question)
        return SignalFollowUpPreparation(
            interpretation_result=interpretation_result,
            disposition=SignalFollowUpDisposition.CREATED_OPEN_QUESTION,
            follow_up_question=question,
            synthesized_work_unit=synthesized_work_unit,
        )

    def apply_follow_up(
        self,
        store: KernelStore,
        index: KernelIndex,
        graph: KernelGraph,
        interpretation_result: SignalInterpretationResult,
        *,
        followed_up_at: str,
    ) -> SignalFollowUpResult:
        preparation = self.prepare_follow_up(
            index,
            interpretation_result,
            followed_up_at=followed_up_at,
        )

        if preparation.disposition in (
            SignalFollowUpDisposition.NO_FOLLOW_UP_REQUIRED,
            SignalFollowUpDisposition.FOLLOW_UP_ALREADY_PRESENT,
        ):
            return SignalFollowUpResult(
                preparation=preparation,
                disposition=preparation.disposition,
            )

        if preparation.disposition is SignalFollowUpDisposition.RESOLVED_EXISTING_QUESTIONS:
            interpretation = interpretation_result.interpretation
            resolved_questions = tuple(
                self._question_router.resolve_question(
                    store,
                    index,
                    graph,
                    question.question_id,
                    resolved_by="DAEMON",
                    resolution=_resolution_text(question, interpretation),
                    resolution_evidence=_resolution_evidence(interpretation),
                    resolved_at=followed_up_at,
                )
                for question in preparation.questions_to_resolve
            )
            return SignalFollowUpResult(
                preparation=preparation,
                disposition=SignalFollowUpDisposition.RESOLVED_EXISTING_QUESTIONS,
                resolved_questions=resolved_questions,
            )

        if preparation.disposition is SignalFollowUpDisposition.ESCALATED_REVIEW:
            interpretation = interpretation_result.interpretation
            escalation_result = self._review_escalator.escalate_review(
                store,
                index,
                graph,
                interpretation.work_unit_id,
                interpretation.delta_id,
                escalated_at=followed_up_at,
            )
            return SignalFollowUpResult(
                preparation=preparation,
                disposition=SignalFollowUpDisposition.ESCALATED_REVIEW,
                created_question=escalation_result.created_question,
                review_escalation_result=escalation_result,
            )

        question = preparation.follow_up_question
        if question is None:
            raise KernelSignalFollowUpError("CREATED_OPEN_QUESTION requires a prepared question.")
        if (
            preparation.synthesized_work_unit is not None
            and not index.exists("work_unit", preparation.synthesized_work_unit.work_unit_id)
        ):
            store.create(preparation.synthesized_work_unit)
            index.record_added(preparation.synthesized_work_unit)
        store.create(question)
        index.record_added(question)
        graph.build_from_index(index)
        return SignalFollowUpResult(
            preparation=preparation,
            disposition=SignalFollowUpDisposition.CREATED_OPEN_QUESTION,
            created_question=question,
        )


IonSignalFollowUpHandler = KernelSignalFollowUpHandler


def signal_follow_up_question_id(signal_id: str) -> str:
    safe = _SAFE_ID_RE.sub("-", signal_id.lower()).strip("-") or "signal"
    return f"signal-followup-{safe}"


def has_signal_follow_up(index: KernelIndex, signal_id: str) -> bool:
    record = index.get("open_question", signal_follow_up_question_id(signal_id))
    if not isinstance(record, OpenQuestion):
        return False
    return record.domain == SIGNAL_FOLLOWUP_DOMAIN and record.status is not OpenQuestionStatus.CANCELLED


def _can_escalate_review(index: KernelIndex, work_unit_id: str, delta_id: str) -> bool:
    work_unit = index.get("work_unit", work_unit_id)
    delta = index.get("commit_delta", delta_id)
    return (
        isinstance(work_unit, WorkUnit)
        and isinstance(delta, CommitDelta)
        and delta.status is CommitDeltaStatus.REQUIRES_REVIEW
        and delta.work_unit_id == work_unit.work_unit_id
    )


def _build_follow_up_question(
    interpretation_result: SignalInterpretationResult,
    *,
    created_at: str,
    scope_view: RuntimeStateScopeView | None = None,
) -> OpenQuestion:
    signal = interpretation_result.signal
    interpretation = interpretation_result.interpretation
    needed_from = interpretation.needed_from or DEFAULT_SIGNAL_FOLLOW_UP_NEEDED_FROM
    scope_ref = interpretation.output_path or interpretation.receipt_path
    linked_artifacts = tuple(
        artifact
        for artifact in (
            interpretation.receipt_path,
            interpretation.output_path,
        )
        if artifact
    )
    runtime_summary = None
    if scope_view is not None and scope_view.has_runtime_state:
        runtime_summary = scope_view.compact_summary()
    return OpenQuestion(
        question_id=signal_follow_up_question_id(interpretation.signal_id),
        created_at=created_at,
        origin_work_unit=interpretation.work_unit_id,
        origin_agent=signal.source_agent,
        origin_transition=signal.signal_type.value,
        domain=SIGNAL_FOLLOWUP_DOMAIN,
        scope_ref=scope_ref,
        question_text=_question_text(interpretation, runtime_summary=runtime_summary),
        needed_from=needed_from,
        priority=_priority_from_signal(signal.priority),
        status=OpenQuestionStatus.OPEN,
        context=_context_text(interpretation, scope_view=scope_view),
        blocking=(interpretation.delta_id,),
        linked_artifacts=linked_artifacts,
    )


def _resolvable_questions_for_completion(
    index: KernelIndex,
    interpretation_result: SignalInterpretationResult,
) -> tuple[OpenQuestion, ...]:
    interpretation = interpretation_result.interpretation
    if interpretation.recommended_action is not SignalRecommendedAction.ACKNOWLEDGE_AND_ARCHIVE:
        return ()

    resolvable: list[OpenQuestion] = []
    for record in index.records_for_work_unit(interpretation.work_unit_id):
        if not isinstance(record, OpenQuestion):
            continue
        if record.status not in (OpenQuestionStatus.OPEN, OpenQuestionStatus.ASSIGNED):
            continue
        if record.domain not in (SIGNAL_FOLLOWUP_DOMAIN, REVIEW_DOMAIN):
            continue
        if interpretation.delta_id in record.blocking:
            continue
        if record.created_at > interpretation_result.signal.created_at:
            continue
        resolvable.append(record)

    return tuple(sorted(resolvable, key=lambda item: (item.created_at, item.question_id)))


def _resolution_text(question: OpenQuestion, interpretation) -> str:
    if question.domain == REVIEW_DOMAIN:
        return (
            f"Completion signal {interpretation.signal_id} for {interpretation.work_unit_id} "
            "materialized bounded completion evidence after earlier validation-review pressure."
        )
    return (
        f"Completion signal {interpretation.signal_id} for {interpretation.work_unit_id} "
        "superseded earlier signal-follow-up pressure."
    )


def _resolution_evidence(interpretation) -> tuple[str, ...]:
    return tuple(
        artifact
        for artifact in (interpretation.receipt_path, interpretation.output_path)
        if artifact
    )


def _build_follow_up_work_unit(question: OpenQuestion) -> WorkUnit:
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


def _question_text(interpretation, *, runtime_summary: str | None = None) -> str:
    if interpretation.recommended_action is SignalRecommendedAction.REPLAN_OR_RETRY:
        text = (
            f"Failure recorded for {interpretation.work_unit_id}; determine the lawful "
            "replan or retry path."
        )
        return f"{text} Runtime posture: {runtime_summary}." if runtime_summary else text
    text = (
        f"Signal follow-up required for {interpretation.work_unit_id}; escalate to "
        f"{interpretation.needed_from or DEFAULT_SIGNAL_FOLLOW_UP_NEEDED_FROM}."
    )
    return f"{text} Runtime posture: {runtime_summary}." if runtime_summary else text


def _context_text(interpretation, *, scope_view: RuntimeStateScopeView | None = None) -> str:
    parts = [
        f"signal_id={interpretation.signal_id}",
        f"recommended_action={interpretation.recommended_action.value}",
        f"receipt_path={interpretation.receipt_path}",
    ]
    if interpretation.needed_from:
        parts.append(f"needed_from={interpretation.needed_from}")
    if interpretation.recoverable is not None:
        parts.append(f"recoverable={interpretation.recoverable}")
    if interpretation.output_path:
        parts.append(f"output_path={interpretation.output_path}")
    if scope_view is not None and scope_view.has_runtime_state:
        if scope_view.manifest is not None:
            parts.append(f"manifest_id={scope_view.manifest.manifest_id}")
        if scope_view.automation is not None:
            parts.append(f"automation_state_id={scope_view.automation.automation_state_id}")
    return ";".join(parts)


def _priority_from_signal(priority: WorkPriority) -> OpenQuestionPriority:
    mapping = {
        WorkPriority.P0_CRITICAL: OpenQuestionPriority.P0_BLOCKING,
        WorkPriority.P1_HIGH: OpenQuestionPriority.P1_HIGH,
        WorkPriority.P2_NORMAL: OpenQuestionPriority.P2_NORMAL,
        WorkPriority.P3_LOW: OpenQuestionPriority.P3_LOW,
    }
    return mapping[priority]


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
