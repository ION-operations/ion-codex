"""Bounded threshold evaluation helpers for the live ION kernel stack.

This module does not claim the historical fully autonomous governance layer already exists.
It provides the smaller truthful bridge the current repository can support today:
normalize confidence / drift / route / automation state into a bounded snapshot,
evaluate explicit threshold conditions, and recommend whether bounded promotion should
hold, escalate, or proceed.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterable

from .model import CommitDelta, CommitDeltaStatus, StrEnum


class KernelThresholdError(Exception):
    """Raised when one threshold evaluation request cannot be interpreted lawfully."""


class ThresholdOperator(StrEnum):
    LT = "lt"
    LTE = "lte"
    GT = "gt"
    GTE = "gte"
    EQ = "eq"
    NEQ = "neq"
    IN = "in"
    NOT_IN = "not_in"


class PromotionAction(StrEnum):
    HOLD = "HOLD"
    ALLOW_BOUNDED_PROMOTION = "ALLOW_BOUNDED_PROMOTION"
    REQUIRE_REVIEW = "REQUIRE_REVIEW"
    ROLL_BACK = "ROLL_BACK"


class ContextMode(StrEnum):
    IDE_MANUAL = "IDE_MANUAL"
    COMPILED_RUNTIME = "COMPILED_RUNTIME"


class AutomationStage(StrEnum):
    MANUAL = "MANUAL"
    ASSISTED = "ASSISTED"
    GATED_AUTOMATION = "GATED_AUTOMATION"
    RUNTIME_ACTIVE = "RUNTIME_ACTIVE"
    SUSPENDED = "SUSPENDED"
    DISABLED = "DISABLED"


class RouteStage(StrEnum):
    FUTURE = "FUTURE"
    ACTIVE = "ACTIVE"
    BLOCKED = "BLOCKED"
    COMPLETED = "COMPLETED"
    ABANDONED = "ABANDONED"


class CalibrationStatus(StrEnum):
    CALIBRATED = "CALIBRATED"
    UNTESTED = "UNTESTED"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
    UNDERCALIBRATED = "UNDERCALIBRATED"
    OVERCALIBRATED = "OVERCALIBRATED"


@dataclass(frozen=True)
class ThresholdCondition:
    """One explicit threshold rule over a named snapshot field."""

    field: str
    operator: ThresholdOperator
    value: Any
    reason: str
    on_trigger: PromotionAction = PromotionAction.REQUIRE_REVIEW


@dataclass(frozen=True)
class ThresholdSnapshot:
    """Normalized runtime posture for one bounded threshold decision."""

    subject_ref: str
    confidence: float | None = None
    drift_score: float | None = None
    blocker_count: int = 0
    contradiction_count: int = 0
    concern_count: int = 0
    review_required: bool = False
    manual_fallback_required: bool = False
    context_mode: ContextMode = ContextMode.IDE_MANUAL
    automation_stage: AutomationStage = AutomationStage.MANUAL
    route_stage: RouteStage = RouteStage.ACTIVE
    calibration_status: CalibrationStatus = CalibrationStatus.INSUFFICIENT_DATA
    metadata: dict[str, Any] = field(default_factory=dict)

    def value_for_field(self, field_name: str) -> Any:
        if hasattr(self, field_name):
            return getattr(self, field_name)
        if field_name in self.metadata:
            return self.metadata[field_name]
        raise KernelThresholdError(f"Unknown threshold field: {field_name}")


@dataclass(frozen=True)
class ThresholdHit:
    """Outcome for one threshold condition."""

    condition: ThresholdCondition
    triggered: bool
    actual_value: Any
    message: str


@dataclass(frozen=True)
class ThresholdEvaluation:
    """Aggregate result for one bounded threshold pass."""

    snapshot: ThresholdSnapshot
    hits: tuple[ThresholdHit, ...]
    recommended_action: PromotionAction

    @property
    def triggered_hits(self) -> tuple[ThresholdHit, ...]:
        return tuple(hit for hit in self.hits if hit.triggered)

    @property
    def passed(self) -> bool:
        return not self.triggered_hits

    def summary(self) -> str:
        if self.passed:
            return (
                f"ThresholdEvaluation({self.snapshot.subject_ref}): PASS — "
                f"{len(self.hits)} checks, action={self.recommended_action}"
            )
        reasons = ", ".join(hit.condition.reason for hit in self.triggered_hits)
        return (
            f"ThresholdEvaluation({self.snapshot.subject_ref}): FAIL — "
            f"{len(self.triggered_hits)}/{len(self.hits)} triggered, "
            f"action={self.recommended_action}, reasons={reasons}"
        )


class KernelThresholdEvaluator:
    """Evaluate bounded promotion / automation thresholds."""

    def default_promotion_conditions(self) -> tuple[ThresholdCondition, ...]:
        """Conservative first-pass gate aligned to the active bridge protocols."""

        return (
            ThresholdCondition(
                field="confidence",
                operator=ThresholdOperator.LT,
                value=0.85,
                reason="CONFIDENCE_BELOW_PROMOTION_FLOOR",
                on_trigger=PromotionAction.REQUIRE_REVIEW,
            ),
            ThresholdCondition(
                field="drift_score",
                operator=ThresholdOperator.GT,
                value=0.15,
                reason="DRIFT_ABOVE_PROMOTION_CEILING",
                on_trigger=PromotionAction.HOLD,
            ),
            ThresholdCondition(
                field="blocker_count",
                operator=ThresholdOperator.GT,
                value=0,
                reason="BLOCKERS_PRESENT",
                on_trigger=PromotionAction.HOLD,
            ),
            ThresholdCondition(
                field="review_required",
                operator=ThresholdOperator.EQ,
                value=True,
                reason="REVIEW_ALREADY_REQUIRED",
                on_trigger=PromotionAction.REQUIRE_REVIEW,
            ),
            ThresholdCondition(
                field="manual_fallback_required",
                operator=ThresholdOperator.EQ,
                value=True,
                reason="MANUAL_FALLBACK_REQUIRED",
                on_trigger=PromotionAction.HOLD,
            ),
            ThresholdCondition(
                field="route_stage",
                operator=ThresholdOperator.NOT_IN,
                value=(RouteStage.ACTIVE.value, RouteStage.COMPLETED.value),
                reason="ROUTE_NOT_WRITEABLE",
                on_trigger=PromotionAction.HOLD,
            ),
            ThresholdCondition(
                field="automation_stage",
                operator=ThresholdOperator.IN,
                value=(AutomationStage.SUSPENDED.value, AutomationStage.DISABLED.value),
                reason="AUTOMATION_STAGE_BLOCKED",
                on_trigger=PromotionAction.ROLL_BACK,
            ),
            ThresholdCondition(
                field="calibration_status",
                operator=ThresholdOperator.IN,
                value=(
                    CalibrationStatus.UNDERCALIBRATED.value,
                    CalibrationStatus.OVERCALIBRATED.value,
                ),
                reason="CALIBRATION_UNSAFE_FOR_PROMOTION",
                on_trigger=PromotionAction.REQUIRE_REVIEW,
            ),
        )

    def snapshot_for_commit_delta(
        self,
        commit_delta: CommitDelta,
        *,
        blockers: Iterable[str] = (),
        context_mode: ContextMode = ContextMode.IDE_MANUAL,
        automation_stage: AutomationStage = AutomationStage.MANUAL,
        route_stage: RouteStage = RouteStage.ACTIVE,
        calibration_status: CalibrationStatus = CalibrationStatus.INSUFFICIENT_DATA,
        manual_fallback_required: bool = False,
        drift_score: float | None = None,
    ) -> ThresholdSnapshot:
        """Normalize one commit delta into a threshold-ready posture snapshot."""

        blocker_items = tuple(item for item in blockers if item)
        concern_count = len(commit_delta.review_reasons) + len(commit_delta.contradictions)
        if drift_score is None:
            drift_score = min(
                1.0,
                len(commit_delta.review_reasons) * 0.1 + len(commit_delta.contradictions) * 0.25,
            )
        review_required = commit_delta.status in {
            CommitDeltaStatus.REQUIRES_REVIEW,
            CommitDeltaStatus.REQUIRES_RECONCILIATION,
        } or bool(commit_delta.review_reasons or commit_delta.contradictions)
        return ThresholdSnapshot(
            subject_ref=commit_delta.delta_id,
            confidence=commit_delta.confidence,
            drift_score=drift_score,
            blocker_count=len(blocker_items),
            contradiction_count=len(commit_delta.contradictions),
            concern_count=concern_count,
            review_required=review_required,
            manual_fallback_required=manual_fallback_required,
            context_mode=context_mode,
            automation_stage=automation_stage,
            route_stage=route_stage,
            calibration_status=calibration_status,
            metadata={
                "work_unit_id": commit_delta.work_unit_id,
                "status": commit_delta.status.value,
                "review_reasons": tuple(commit_delta.review_reasons),
                "contradictions": tuple(commit_delta.contradictions),
                "blockers": blocker_items,
            },
        )

    def evaluate(
        self,
        snapshot: ThresholdSnapshot,
        *,
        conditions: Iterable[ThresholdCondition] | None = None,
    ) -> ThresholdEvaluation:
        active_conditions = tuple(conditions or self.default_promotion_conditions())
        hits: list[ThresholdHit] = []
        recommended_action = PromotionAction.ALLOW_BOUNDED_PROMOTION
        for condition in active_conditions:
            actual_value = snapshot.value_for_field(condition.field)
            triggered = _compare(actual_value, condition.operator, condition.value)
            hits.append(
                ThresholdHit(
                    condition=condition,
                    triggered=triggered,
                    actual_value=actual_value,
                    message=f"{condition.field}={actual_value!r} {condition.operator.value} {condition.value!r}",
                )
            )
            if triggered:
                recommended_action = _max_action(recommended_action, condition.on_trigger)
        return ThresholdEvaluation(
            snapshot=snapshot,
            hits=tuple(hits),
            recommended_action=recommended_action,
        )


IonThresholdEvaluator = KernelThresholdEvaluator


def _compare(actual_value: Any, operator: ThresholdOperator, expected_value: Any) -> bool:
    if operator is ThresholdOperator.LT:
        return _coerce_float(actual_value) < _coerce_float(expected_value)
    if operator is ThresholdOperator.LTE:
        return _coerce_float(actual_value) <= _coerce_float(expected_value)
    if operator is ThresholdOperator.GT:
        return _coerce_float(actual_value) > _coerce_float(expected_value)
    if operator is ThresholdOperator.GTE:
        return _coerce_float(actual_value) >= _coerce_float(expected_value)
    if operator is ThresholdOperator.EQ:
        return _normalize(actual_value) == _normalize(expected_value)
    if operator is ThresholdOperator.NEQ:
        return _normalize(actual_value) != _normalize(expected_value)
    if operator is ThresholdOperator.IN:
        return _normalize(actual_value) in _normalize_iterable(expected_value)
    if operator is ThresholdOperator.NOT_IN:
        return _normalize(actual_value) not in _normalize_iterable(expected_value)
    raise KernelThresholdError(f"Unsupported threshold operator: {operator}")


def _normalize(value: Any) -> Any:
    if isinstance(value, StrEnum):
        return value.value
    return value


def _normalize_iterable(value: Any) -> tuple[Any, ...]:
    if isinstance(value, (str, bytes)):
        return (_normalize(value),)
    try:
        return tuple(_normalize(item) for item in value)
    except TypeError as exc:
        raise KernelThresholdError(f"Threshold expected an iterable value, found: {value!r}") from exc


def _coerce_float(value: Any) -> float:
    normalized = _normalize(value)
    try:
        return float(normalized)
    except (TypeError, ValueError) as exc:
        raise KernelThresholdError(f"Threshold value is not numeric: {value!r}") from exc


def _max_action(left: PromotionAction, right: PromotionAction) -> PromotionAction:
    order = {
        PromotionAction.ALLOW_BOUNDED_PROMOTION: 0,
        PromotionAction.HOLD: 1,
        PromotionAction.REQUIRE_REVIEW: 2,
        PromotionAction.ROLL_BACK: 3,
    }
    return left if order[left] >= order[right] else right
