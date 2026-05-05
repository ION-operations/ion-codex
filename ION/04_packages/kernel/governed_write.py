"""Bounded governed-write wrapper for the live ION kernel stack.

This module does not resurrect the older full write pipeline. It composes the current
commit applier with the newly landed threshold and automation bridge surfaces so one
accepted commit delta can be checked against route posture before any filesystem write
is materialized.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from pathlib import Path
from typing import Iterable

from .commit import CommitApplicationResult, KernelCommitApplier, KernelCommitError
from .index import KernelIndex
from .model import AuthorityClass, CommitDelta, WorkUnit
from .store import KernelStore
from .runtime_state_sync import KernelRuntimeStateSync, RuntimeStateSyncResult
from .runtime_report_triggers import RuntimeReportTriggerRequest
from .threshold import (
    AutomationStage,
    CalibrationStatus,
    ContextMode,
    KernelThresholdEvaluator,
    PromotionAction,
    RouteStage,
    ThresholdCondition,
    ThresholdEvaluation,
    ThresholdSnapshot,
)


class KernelGovernedWriteError(Exception):
    """Raised when a governed write cannot be completed lawfully."""


@dataclass(frozen=True)
class GovernedWriteStageResult:
    stage_name: str
    passed: bool
    message: str


@dataclass(frozen=True)
class GovernedWriteRequest:
    work_unit_id: str
    delta_id: str
    workspace_root: str | Path
    context_mode: ContextMode = ContextMode.IDE_MANUAL
    automation_stage: AutomationStage = AutomationStage.MANUAL
    route_stage: RouteStage = RouteStage.ACTIVE
    calibration_status: CalibrationStatus = CalibrationStatus.INSUFFICIENT_DATA
    blockers: tuple[str, ...] = ()
    manual_fallback_required: bool = False
    threshold_conditions: tuple[ThresholdCondition, ...] = ()
    threshold_snapshot: ThresholdSnapshot | None = None
    artifact_trigger_request: RuntimeReportTriggerRequest | None = None


@dataclass(frozen=True)
class GovernedWriteReceipt:
    request: GovernedWriteRequest
    work_unit: WorkUnit
    commit_delta: CommitDelta
    stages: tuple[GovernedWriteStageResult, ...]
    threshold_evaluation: ThresholdEvaluation
    application_result: CommitApplicationResult | None = None
    runtime_state_sync: RuntimeStateSyncResult | None = None

    @property
    def passed(self) -> bool:
        return all(stage.passed for stage in self.stages)


class KernelGovernedWriter:
    """Apply one accepted commit delta only after explicit route and threshold gates pass."""

    _FORBIDDEN_AUTHORITIES = frozenset(
        {
            AuthorityClass.STALE_COMPETITOR,
            AuthorityClass.ARCHIVE_REFERENCE,
        }
    )

    def __init__(
        self,
        *,
        commit_applier: KernelCommitApplier | None = None,
        threshold_evaluator: KernelThresholdEvaluator | None = None,
        runtime_state_sync: KernelRuntimeStateSync | None = None,
    ) -> None:
        self._commit_applier = commit_applier or KernelCommitApplier()
        self._threshold_evaluator = threshold_evaluator or KernelThresholdEvaluator()
        self._runtime_state_sync = runtime_state_sync or KernelRuntimeStateSync()

    def evaluate(
        self,
        index: KernelIndex,
        request: GovernedWriteRequest,
    ) -> GovernedWriteReceipt:
        work_unit = index.get("work_unit", request.work_unit_id)
        if not isinstance(work_unit, WorkUnit):
            raise KernelGovernedWriteError(f"Unknown work unit: {request.work_unit_id}")
        commit_delta = index.get("commit_delta", request.delta_id)
        if not isinstance(commit_delta, CommitDelta):
            raise KernelGovernedWriteError(f"Unknown commit delta: {request.delta_id}")

        stages: list[GovernedWriteStageResult] = []

        try:
            self._commit_applier.prepare_application(
                index,
                request.work_unit_id,
                request.delta_id,
                request.workspace_root,
            )
            stages.append(
                GovernedWriteStageResult(
                    stage_name="GW1_BINDING",
                    passed=True,
                    message="Commit delta binds cleanly to the committed work unit and bounded workspace.",
                )
            )
        except KernelCommitError as exc:
            stages.append(GovernedWriteStageResult("GW1_BINDING", False, str(exc)))
            return GovernedWriteReceipt(
                request=request,
                work_unit=work_unit,
                commit_delta=commit_delta,
                stages=tuple(stages),
                threshold_evaluation=self._threshold_evaluator.evaluate(
                    request.threshold_snapshot
                    or self._threshold_evaluator.snapshot_for_commit_delta(commit_delta)
                ),
                application_result=None,
            )

        route_ok, route_message = _validate_route_state(request)
        stages.append(GovernedWriteStageResult("GW2_ROUTE", route_ok, route_message))
        snapshot = request.threshold_snapshot or self._threshold_evaluator.snapshot_for_commit_delta(
            commit_delta,
            blockers=request.blockers,
            context_mode=request.context_mode,
            automation_stage=request.automation_stage,
            route_stage=request.route_stage,
            calibration_status=request.calibration_status,
            manual_fallback_required=request.manual_fallback_required,
        )
        threshold_evaluation = self._threshold_evaluator.evaluate(
            snapshot,
            conditions=request.threshold_conditions or None,
        )
        stages.append(
            GovernedWriteStageResult(
                "GW3_THRESHOLD",
                threshold_evaluation.passed,
                threshold_evaluation.summary(),
            )
        )

        authority_ok, authority_message = _validate_authorities(commit_delta, self._FORBIDDEN_AUTHORITIES)
        stages.append(GovernedWriteStageResult("GW4_AUTHORITY", authority_ok, authority_message))

        return GovernedWriteReceipt(
            request=request,
            work_unit=work_unit,
            commit_delta=commit_delta,
            stages=tuple(stages),
            threshold_evaluation=threshold_evaluation,
            application_result=None,
        )

    def apply(
        self,
        store: KernelStore,
        index: KernelIndex,
        request: GovernedWriteRequest,
    ) -> GovernedWriteReceipt:
        receipt = self.evaluate(index, request)
        if not receipt.passed:
            sync_result = self._runtime_state_sync.sync_governed_write(
                store,
                index,
                receipt,
                artifact_trigger_request=receipt.request.artifact_trigger_request,
            )
            return replace(receipt, runtime_state_sync=sync_result)
        if receipt.threshold_evaluation.recommended_action is not PromotionAction.ALLOW_BOUNDED_PROMOTION:
            sync_result = self._runtime_state_sync.sync_governed_write(
                store,
                index,
                receipt,
                artifact_trigger_request=receipt.request.artifact_trigger_request,
            )
            return replace(receipt, runtime_state_sync=sync_result)

        application_result = self._commit_applier.apply_commit_delta(
            index,
            request.work_unit_id,
            request.delta_id,
            request.workspace_root,
        )
        stages = receipt.stages + (
            GovernedWriteStageResult(
                stage_name="GW5_WRITE",
                passed=True,
                message=(
                    f"Applied {len(application_result.artifact_paths)} artifact writes and "
                    f"{len(application_result.state_targets)} state mutations."
                ),
            ),
        )
        receipt = GovernedWriteReceipt(
            request=receipt.request,
            work_unit=receipt.work_unit,
            commit_delta=receipt.commit_delta,
            stages=stages,
            threshold_evaluation=receipt.threshold_evaluation,
            application_result=application_result,
        )
        sync_result = self._runtime_state_sync.sync_governed_write(
            store,
            index,
            receipt,
            artifact_trigger_request=receipt.request.artifact_trigger_request,
        )
        return replace(receipt, runtime_state_sync=sync_result)


IonGovernedWriter = KernelGovernedWriter


def _validate_route_state(request: GovernedWriteRequest) -> tuple[bool, str]:
    if request.route_stage in {RouteStage.FUTURE, RouteStage.BLOCKED, RouteStage.ABANDONED}:
        return False, f"Route stage is not writeable: {request.route_stage.value}"
    if request.automation_stage in {AutomationStage.SUSPENDED, AutomationStage.DISABLED}:
        return False, f"Automation stage blocks write application: {request.automation_stage.value}"
    if (
        request.context_mode is ContextMode.IDE_MANUAL
        and request.automation_stage is AutomationStage.RUNTIME_ACTIVE
    ):
        return False, "RUNTIME_ACTIVE posture requires COMPILED_RUNTIME context mode."
    return True, "Context mode, route stage, and automation posture are compatible with bounded writes."


def _validate_authorities(
    commit_delta: CommitDelta,
    forbidden_authorities: Iterable[AuthorityClass],
) -> tuple[bool, str]:
    forbidden_set = set(forbidden_authorities)
    forbidden = {authority for authority in commit_delta.authorities_touched() if authority in forbidden_set}
    if forbidden:
        joined = ", ".join(sorted(authority.value for authority in forbidden))
        return False, f"Commit delta touches non-writeable authority classes: {joined}"
    return True, "Produced artifacts stay inside writeable authority classes."
