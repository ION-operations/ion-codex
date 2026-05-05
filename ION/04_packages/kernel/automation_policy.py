"""Supervised automation policy gate for the live ION kernel stack.

This module does not create autonomy. It provides the first bounded decision matrix
for deciding whether a supervised automation action is allowed, blocked, held, or
requires explicit approval.
"""

from __future__ import annotations

from dataclasses import dataclass

from .model import StrEnum
from .threshold import AutomationStage, CalibrationStatus, ContextMode, PromotionAction, RouteStage


class KernelAutomationPolicyError(Exception):
    """Raised when one automation-policy request is not lawful."""


class AutomationActionClass(StrEnum):
    START_DAEMON_SERVICE = "START_DAEMON_SERVICE"
    RUN_DAEMON_STEP = "RUN_DAEMON_STEP"
    ISSUE_CHILD_WORK = "ISSUE_CHILD_WORK"
    APPLY_GOVERNED_WRITE = "APPLY_GOVERNED_WRITE"
    ESCALATE_REVIEW = "ESCALATE_REVIEW"
    EMIT_RUNTIME_REPORT = "EMIT_RUNTIME_REPORT"
    EXPORT_EXTERNAL_EXECUTION_PACKET = "EXPORT_EXTERNAL_EXECUTION_PACKET"
    ACCEPT_EXTERNAL_EXECUTION_RETURN = "ACCEPT_EXTERNAL_EXECUTION_RETURN"


class AutomationPolicyDecision(StrEnum):
    ALLOW = "ALLOW"
    REQUIRE_APPROVAL = "REQUIRE_APPROVAL"
    HOLD = "HOLD"
    BLOCK = "BLOCK"


_SENSITIVE_ACTIONS = frozenset(
    {
        AutomationActionClass.START_DAEMON_SERVICE,
        AutomationActionClass.RUN_DAEMON_STEP,
        AutomationActionClass.ISSUE_CHILD_WORK,
        AutomationActionClass.APPLY_GOVERNED_WRITE,
        AutomationActionClass.EXPORT_EXTERNAL_EXECUTION_PACKET,
        AutomationActionClass.ACCEPT_EXTERNAL_EXECUTION_RETURN,
    }
)

_EXTERNAL_BOUNDARY_ACTIONS = frozenset(
    {
        AutomationActionClass.EXPORT_EXTERNAL_EXECUTION_PACKET,
        AutomationActionClass.ACCEPT_EXTERNAL_EXECUTION_RETURN,
    }
)

_REVIEW_SENSITIVE_ACTIONS = frozenset(
    {
        AutomationActionClass.START_DAEMON_SERVICE,
        AutomationActionClass.ISSUE_CHILD_WORK,
        AutomationActionClass.APPLY_GOVERNED_WRITE,
        AutomationActionClass.EXPORT_EXTERNAL_EXECUTION_PACKET,
        AutomationActionClass.ACCEPT_EXTERNAL_EXECUTION_RETURN,
    }
)


@dataclass(frozen=True)
class AutomationPolicyRequest:
    action_class: AutomationActionClass
    context_mode: ContextMode
    automation_stage: AutomationStage
    route_stage: RouteStage = RouteStage.ACTIVE
    calibration_status: CalibrationStatus = CalibrationStatus.INSUFFICIENT_DATA
    threshold_action: PromotionAction | None = None
    review_required: bool = False
    manual_fallback_required: bool = False
    operator_stop: bool = False
    operator_hold: bool = False
    supervisor_present: bool = False
    explicit_approval: bool = False
    notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class AutomationPolicyEvaluation:
    request: AutomationPolicyRequest
    decision: AutomationPolicyDecision
    reasons: tuple[str, ...] = ()
    required_controls: tuple[str, ...] = ()

    @property
    def permitted(self) -> bool:
        return self.decision is AutomationPolicyDecision.ALLOW


class KernelAutomationPolicy:
    """Evaluate whether one bounded automation action is lawful right now."""

    def evaluate(self, request: AutomationPolicyRequest) -> AutomationPolicyEvaluation:
        if request.operator_stop:
            return self._evaluation(
                request,
                decision=AutomationPolicyDecision.BLOCK,
                reasons=("OPERATOR_SERVICE_STOP_ACTIVE",),
            )

        if request.operator_hold:
            return self._evaluation(
                request,
                decision=AutomationPolicyDecision.HOLD,
                reasons=("OPERATOR_SCOPE_HOLD_ACTIVE",),
            )

        if request.automation_stage is AutomationStage.DISABLED:
            return self._evaluation(
                request,
                decision=AutomationPolicyDecision.BLOCK,
                reasons=("AUTOMATION_STAGE_DISABLED",),
            )

        if request.automation_stage is AutomationStage.SUSPENDED:
            return self._evaluation(
                request,
                decision=AutomationPolicyDecision.HOLD,
                reasons=("AUTOMATION_STAGE_SUSPENDED",),
            )

        if request.action_class in _SENSITIVE_ACTIONS and not request.supervisor_present:
            return self._evaluation(
                request,
                decision=AutomationPolicyDecision.BLOCK,
                reasons=("SUPERVISOR_REQUIRED",),
            )

        if request.threshold_action in {PromotionAction.HOLD, PromotionAction.ROLL_BACK}:
            return self._evaluation(
                request,
                decision=AutomationPolicyDecision.HOLD,
                reasons=(f"THRESHOLD_{request.threshold_action.value}",),
            )

        if request.manual_fallback_required and request.action_class in _SENSITIVE_ACTIONS:
            return self._evaluation(
                request,
                decision=AutomationPolicyDecision.HOLD,
                reasons=("MANUAL_FALLBACK_REQUIRED",),
            )

        approval_reasons: list[str] = []
        if request.threshold_action is PromotionAction.REQUIRE_REVIEW:
            approval_reasons.append("THRESHOLD_REQUIRES_REVIEW")
        if request.review_required and request.action_class in _REVIEW_SENSITIVE_ACTIONS:
            approval_reasons.append("REVIEW_REQUIRED")
        if (
            request.context_mode is ContextMode.IDE_MANUAL
            and request.action_class in _SENSITIVE_ACTIONS
            and request.automation_stage in {AutomationStage.MANUAL, AutomationStage.GATED_AUTOMATION, AutomationStage.RUNTIME_ACTIVE}
        ):
            approval_reasons.append("IDE_MANUAL_REQUIRES_EXPLICIT_APPROVAL")
        if request.context_mode is ContextMode.IDE_MANUAL and request.action_class in _EXTERNAL_BOUNDARY_ACTIONS:
            approval_reasons.append("EXTERNAL_BOUNDARY_REQUIRES_EXPLICIT_APPROVAL")
        if request.calibration_status in {
            CalibrationStatus.UNDERCALIBRATED,
            CalibrationStatus.OVERCALIBRATED,
        } and request.action_class in _SENSITIVE_ACTIONS:
            approval_reasons.append("CALIBRATION_REQUIRES_APPROVAL")
        if request.route_stage in {RouteStage.BLOCKED, RouteStage.ABANDONED} and request.action_class in _SENSITIVE_ACTIONS:
            approval_reasons.append(f"ROUTE_STAGE_{request.route_stage.value}")

        if approval_reasons:
            if request.explicit_approval:
                return self._evaluation(
                    request,
                    decision=AutomationPolicyDecision.ALLOW,
                    reasons=tuple(dict.fromkeys(tuple(approval_reasons) + ("EXPLICIT_APPROVAL_SUPPLIED",))),
                    required_controls=("explicit_approval",),
                )
            return self._evaluation(
                request,
                decision=AutomationPolicyDecision.REQUIRE_APPROVAL,
                reasons=tuple(dict.fromkeys(approval_reasons)),
                required_controls=("explicit_approval",),
            )

        return self._evaluation(
            request,
            decision=AutomationPolicyDecision.ALLOW,
            reasons=("POLICY_ALLOW",),
        )

    def _evaluation(
        self,
        request: AutomationPolicyRequest,
        *,
        decision: AutomationPolicyDecision,
        reasons: tuple[str, ...],
        required_controls: tuple[str, ...] = (),
    ) -> AutomationPolicyEvaluation:
        return AutomationPolicyEvaluation(
            request=request,
            decision=decision,
            reasons=reasons,
            required_controls=required_controls,
        )


IonAutomationPolicy = KernelAutomationPolicy
