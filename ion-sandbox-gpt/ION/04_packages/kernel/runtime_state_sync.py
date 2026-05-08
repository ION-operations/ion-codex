"""Bounded runtime-state binding for the live ION kernel stack.

This module binds the C1 machine-readable state families into real runtime event edges
without claiming a broader autonomous daemon already exists. It keeps continuity prose,
route-state, and automation-state distinct while allowing governed-write and capsule
activity to persist the current operational posture.
"""

from __future__ import annotations

from dataclasses import dataclass

from .runtime_report_triggers import (
    KernelRuntimeReportTriggerManager,
    RuntimeReportTriggerReceipt,
    RuntimeReportTriggerRequest,
)
from typing import TYPE_CHECKING

from .automation_state import KernelAutomationStateManager
from .manifest_state import KernelManifestRouteStateManager, manifest_route_state_id
from .model import AutomationGate, ContextPackage, RouteBranch, WorkUnit
from .store import KernelStore
from .index import KernelIndex
from .threshold import AutomationStage, ContextMode, PromotionAction, RouteStage

if TYPE_CHECKING:
    from .automation_state import AutomationStateResult
    from .manifest_state import ManifestRouteStateResult
    from .capsule_manager import CapsuleRecord
    from .governed_write import GovernedWriteReceipt


_ROUTE_GOVERNING_REFS = (
    "ION/02_architecture/MANIFEST_AND_ROUTE_STATE_PROTOCOL.md",
    "ION/02_architecture/CONTEXT_MODE_PROTOCOL.md",
    "ION/06_intelligence/specs/T09_ManifestRouteStateSchema.spec.md",
)
_AUTOMATION_GOVERNING_REFS = (
    "ION/02_architecture/AUTOMATION_STATE_PROTOCOL.md",
    "ION/02_architecture/CONTEXT_MODE_PROTOCOL.md",
    "ION/06_intelligence/specs/T08_ConfidenceAndDriftSchema.spec.md",
    "ION/06_intelligence/specs/T10_CrossModelAuditCalibration.spec.md",
    "ION/06_intelligence/specs/T11_AutomationStateSchema.spec.md",
)


@dataclass(frozen=True)
class RuntimeStateSyncResult:
    source_kind: str
    source_ref: str
    manifest_result: ManifestRouteStateResult
    automation_result: AutomationStateResult
    notes: tuple[str, ...] = ()
    triggered_artifacts: tuple[RuntimeReportTriggerReceipt, ...] = ()

    @property
    def manifest_id(self) -> str:
        return self.manifest_result.persisted_record.manifest_id

    @property
    def automation_state_id(self) -> str:
        return self.automation_result.persisted_record.automation_state_id


class KernelRuntimeStateSync:
    """Synchronize route-state and automation-state from live kernel events."""

    def __init__(
        self,
        *,
        manifest_manager: KernelManifestRouteStateManager | None = None,
        automation_manager: KernelAutomationStateManager | None = None,
        runtime_report_trigger_manager: KernelRuntimeReportTriggerManager | None = None,
    ) -> None:
        self._manifest_manager = manifest_manager or KernelManifestRouteStateManager()
        self._automation_manager = automation_manager or KernelAutomationStateManager()
        self._runtime_report_trigger_manager = runtime_report_trigger_manager or KernelRuntimeReportTriggerManager()

    def sync_governed_write(
        self,
        store: KernelStore,
        index: KernelIndex,
        receipt: GovernedWriteReceipt,
        *,
        artifact_trigger_request: RuntimeReportTriggerRequest | None = None,
    ) -> RuntimeStateSyncResult:
        work_unit = receipt.work_unit
        commit_delta = receipt.commit_delta
        context_package = index.get("context_package", work_unit.context_package_id)
        mission = _mission_for_work_unit(work_unit, context_package)
        manifest_id = manifest_route_state_id("WORK_UNIT", work_unit.work_unit_id)

        snapshot = receipt.threshold_evaluation.snapshot
        stage_blockers = _governed_write_stage_blockers(receipt)
        automation_result = self._automation_manager.upsert_record(
            store,
            index,
            scope_type="WORK_UNIT",
            scope_ref=work_unit.work_unit_id,
            current_stage=_safe_automation_stage(snapshot.context_mode, snapshot.automation_stage),
            governing_refs=_AUTOMATION_GOVERNING_REFS,
            active_gates=_gates_from_governed_write_receipt(receipt),
            blockers=tuple(hit.condition.reason for hit in receipt.threshold_evaluation.triggered_hits) + stage_blockers,
            promotion_criteria=_governed_write_promotion_criteria(receipt),
            fallback_mode=("MANUAL" if snapshot.manual_fallback_required else _safe_automation_stage(snapshot.context_mode, snapshot.automation_stage).value),
            last_transition_reason=_governed_write_transition_reason(receipt),
            pending_actions=_governed_write_pending_actions(receipt),
            linked_manifest_id=manifest_id,
            context_mode=snapshot.context_mode,
            calibration_status=snapshot.calibration_status.value,
            notes=(
                f"governed-write::{commit_delta.delta_id}::{receipt.threshold_evaluation.recommended_action.value}"
            ),
        )

        branch_status = _branch_status_for_governed_write(receipt)
        branch_id = f"branch-{commit_delta.delta_id}"
        target_refs = tuple(
            dict.fromkeys(
                [artifact.path for artifact in commit_delta.produced_artifacts]
                + [mutation.target for mutation in commit_delta.state_mutations]
            )
        )
        evidence_refs = tuple(dict.fromkeys((commit_delta.delta_id,) + target_refs))
        blocker_refs = tuple(
            dict.fromkeys(
                tuple(hit.condition.reason for hit in receipt.threshold_evaluation.triggered_hits)
                + stage_blockers
                + tuple(receipt.request.blockers)
            )
        )
        drift_flags = tuple(dict.fromkeys(commit_delta.contradictions))
        reasons = tuple(
            dict.fromkeys(
                tuple(hit.condition.reason for hit in receipt.threshold_evaluation.triggered_hits)
                + stage_blockers
                or (_governed_write_transition_reason(receipt),)
            )
        )
        manifest_result = self._manifest_manager.upsert_record(
            store,
            index,
            owner_scope_type="WORK_UNIT",
            owner_scope_id=work_unit.work_unit_id,
            steward=work_unit.agent_personal_name,
            mission=mission,
            governing_refs=_ROUTE_GOVERNING_REFS,
            loop_position=("DELIVER" if receipt.application_result is not None else "GATE"),
            branches=(
                RouteBranch(
                    branch_id=branch_id,
                    label=f"governed-write::{work_unit.scope_ref}",
                    status=branch_status.value,
                    priority=work_unit.priority.value,
                    gate_class=("G1_BOUNDED" if receipt.passed else "G2_REVIEW"),
                    target_refs=target_refs,
                    governing_refs=_ROUTE_GOVERNING_REFS,
                    evidence_refs=evidence_refs,
                    confidence_band=_confidence_band(receipt.threshold_evaluation.snapshot.confidence),
                    started_at=commit_delta.created_at,
                    completed_at=(commit_delta.created_at if receipt.application_result is not None else None),
                    abandonment_reason=(
                        None
                        if branch_status is not RouteStage.ABANDONED
                        else _governed_write_transition_reason(receipt)
                    ),
                ),
            ),
            active_branch_id=(branch_id if branch_status is RouteStage.ACTIVE else None),
            context_mode=receipt.request.context_mode,
            automation_stage=_safe_automation_stage(receipt.request.context_mode, receipt.request.automation_stage),
            recent_evidence_refs=evidence_refs,
            unresolved_issue_refs=tuple(dict.fromkeys(commit_delta.review_reasons)),
            blocker_refs=blocker_refs,
            drift_flags=drift_flags,
            route_confidence=_confidence_band(receipt.threshold_evaluation.snapshot.confidence),
            branching_stability="STABLE",
            recommended_action=_route_recommended_action_for_governed_write(receipt),
            reasons=reasons,
            handoff_summary=_governed_write_handoff_summary(receipt),
            next_route_proposal=_governed_write_next_route(receipt),
            linked_automation_state_id=automation_result.persisted_record.automation_state_id,
            notes=(
                f"scope_ref={work_unit.scope_ref}; protocol={work_unit.protocol_id}; transition={work_unit.transition_id}"
            ),
        )
        result = RuntimeStateSyncResult(
            source_kind="governed_write",
            source_ref=commit_delta.delta_id,
            manifest_result=manifest_result,
            automation_result=automation_result,
            notes=(f"work_unit={work_unit.work_unit_id}",),
        )
        triggered = self._runtime_report_trigger_manager.emit_for_runtime_state_sync(index, result, artifact_trigger_request)
        if triggered:
            result = RuntimeStateSyncResult(
                source_kind=result.source_kind,
                source_ref=result.source_ref,
                manifest_result=result.manifest_result,
                automation_result=result.automation_result,
                notes=result.notes,
                triggered_artifacts=triggered,
            )
        return result

    def sync_capsule(
        self,
        store: KernelStore,
        index: KernelIndex,
        capsule: CapsuleRecord,
        *,
        owner_scope_type: str,
        owner_scope_id: str,
        steward: str | None = None,
        governing_refs: tuple[str, ...] = (),
        loop_position: str | None = None,
        route_targets: tuple[str, ...] = (),
        promotion_criteria: tuple[str, ...] = (),
        artifact_trigger_request: RuntimeReportTriggerRequest | None = None,
    ) -> RuntimeStateSyncResult:
        scope_type = owner_scope_type.strip().upper()
        scope_id = owner_scope_id.strip()
        if not scope_type or not scope_id:
            raise ValueError("owner_scope_type and owner_scope_id are required for capsule sync")
        manifest_id = manifest_route_state_id(scope_type, scope_id)
        context_mode = _context_mode_from_value(capsule.context_mode)
        automation_stage = _automation_stage_from_value(capsule.automation_stage)
        resolved_governing_refs = tuple(dict.fromkeys(tuple(governing_refs) + _ROUTE_GOVERNING_REFS))
        resolved_route_targets = tuple(
            dict.fromkeys(
                tuple(route_targets)
                + ((capsule.route_surface,) if capsule.route_surface else ())
                + tuple(str(item) for item in capsule.metadata.get("route_targets", ()))
            )
        )
        blockers = tuple(
            dict.fromkeys(
                ((capsule.blocker,) if capsule.blocker else ())
                + ((f"DRIFT::{capsule.drift_status}",) if capsule.drift_status and capsule.drift_status.upper() not in {"CLEAR", "STABLE", "NONE"} else ())
            )
        )
        gates = []
        if capsule.blocker:
            gates.append(
                AutomationGate(
                    gate_id="capsule-blocker",
                    gate_class="CAPSULE_BLOCKER",
                    status="BLOCKED",
                    satisfied=False,
                    detail=capsule.blocker,
                    evidence_refs=tuple(capsule.evidence),
                )
            )
        if capsule.drift_status and capsule.drift_status.upper() not in {"CLEAR", "STABLE", "NONE"}:
            gates.append(
                AutomationGate(
                    gate_id="capsule-drift",
                    gate_class="CAPSULE_DRIFT",
                    status="BLOCKED",
                    satisfied=False,
                    detail=capsule.drift_status,
                    evidence_refs=tuple(capsule.evidence),
                )
            )
        automation_result = self._automation_manager.upsert_record(
            store,
            index,
            scope_type=scope_type,
            scope_ref=scope_id,
            current_stage=automation_stage,
            governing_refs=tuple(dict.fromkeys(tuple(governing_refs) + _AUTOMATION_GOVERNING_REFS)),
            active_gates=tuple(gates),
            blockers=blockers,
            promotion_criteria=tuple(dict.fromkeys(tuple(promotion_criteria) + (capsule.next_action,))),
            fallback_mode=("MANUAL" if automation_stage is AutomationStage.MANUAL else automation_stage.value),
            last_transition_reason=f"CAPSULE_{capsule.capsule_type}_CAPTURED",
            pending_actions=(capsule.next_action,),
            linked_manifest_id=manifest_id,
            context_mode=context_mode,
            calibration_status=None,
            notes=f"capsule::{capsule.capsule_id}",
        )
        branch_status = RouteStage.ACTIVE if capsule.capsule_type == "PRE" else RouteStage.COMPLETED
        branch_id = f"capsule-{capsule.capsule_type.lower()}-{capsule.capsule_id}"
        manifest_result = self._manifest_manager.upsert_record(
            store,
            index,
            owner_scope_type=scope_type,
            owner_scope_id=scope_id,
            steward=(steward or capsule.callsign),
            mission=capsule.mission,
            governing_refs=resolved_governing_refs,
            loop_position=(loop_position or ("PLAN" if capsule.capsule_type == "PRE" else "DELIVER")),
            branches=(
                RouteBranch(
                    branch_id=branch_id,
                    label=f"capsule::{capsule.capsule_type.lower()}::{capsule.callsign}",
                    status=branch_status.value,
                    priority="P2_NORMAL",
                    gate_class="G1_BOUNDED",
                    target_refs=resolved_route_targets,
                    governing_refs=resolved_governing_refs,
                    evidence_refs=tuple(capsule.evidence),
                    confidence_band=(capsule.confidence_band or "MEDIUM"),
                    started_at=capsule.timestamp,
                    completed_at=(capsule.timestamp if branch_status is RouteStage.COMPLETED else None),
                ),
            ),
            active_branch_id=(branch_id if branch_status is RouteStage.ACTIVE else None),
            context_mode=context_mode,
            automation_stage=automation_stage,
            recent_evidence_refs=tuple(capsule.evidence),
            unresolved_issue_refs=(),
            blocker_refs=blockers,
            drift_flags=((capsule.drift_status,) if capsule.drift_status else ()),
            route_confidence=(capsule.confidence_band or "MEDIUM"),
            branching_stability="STABLE",
            recommended_action=("CONTINUE" if capsule.capsule_type == "PRE" else "HANDOFF"),
            reasons=((f"CAPSULE_{capsule.capsule_type}_CAPTURED",) if not blockers else blockers),
            handoff_summary=(capsule.handoff or None),
            next_route_proposal=capsule.next_action,
            linked_automation_state_id=automation_result.persisted_record.automation_state_id,
            notes=f"capsule::{capsule.capsule_id}",
        )
        result = RuntimeStateSyncResult(
            source_kind="capsule",
            source_ref=capsule.capsule_id,
            manifest_result=manifest_result,
            automation_result=automation_result,
            notes=(f"scope={scope_type}:{scope_id}",),
        )
        triggered = self._runtime_report_trigger_manager.emit_for_runtime_state_sync(index, result, artifact_trigger_request)
        if triggered:
            result = RuntimeStateSyncResult(
                source_kind=result.source_kind,
                source_ref=result.source_ref,
                manifest_result=result.manifest_result,
                automation_result=result.automation_result,
                notes=result.notes,
                triggered_artifacts=triggered,
            )
        return result


IonRuntimeStateSync = KernelRuntimeStateSync


def _mission_for_work_unit(work_unit: WorkUnit, context_package: object | None) -> str:
    if isinstance(context_package, ContextPackage):
        objective = context_package.tiers.tier_3_mission.objective.strip()
        if objective:
            return objective
    return f"Advance {work_unit.protocol_id}/{work_unit.transition_id} for {work_unit.scope_ref}"


def _governed_write_promotion_criteria(receipt: GovernedWriteReceipt) -> tuple[str, ...]:
    criteria = [
        "threshold pass",
        "route posture compatible",
        "bounded authority class",
    ]
    if receipt.application_result is not None:
        criteria.append("bounded write applied")
    return tuple(criteria)


def _governed_write_pending_actions(receipt: GovernedWriteReceipt) -> tuple[str, ...]:
    action = receipt.threshold_evaluation.recommended_action
    if receipt.application_result is not None:
        return ("inspect bounded workspace result",)
    if action is PromotionAction.REQUIRE_REVIEW:
        return ("request review",)
    if action is PromotionAction.HOLD:
        return ("resolve blockers before write",)
    if action is PromotionAction.ROLL_BACK:
        return ("return to manual posture",)
    return ("continue bounded execution",)


def _governed_write_transition_reason(receipt: GovernedWriteReceipt) -> str:
    if receipt.application_result is not None:
        return "WRITE_APPLIED"
    return receipt.threshold_evaluation.recommended_action.value


def _route_recommended_action_for_governed_write(receipt: GovernedWriteReceipt) -> str:
    if receipt.application_result is not None:
        return "WRITE_APPLIED"
    action = receipt.threshold_evaluation.recommended_action
    if action is PromotionAction.REQUIRE_REVIEW:
        return "REQUEST_REVIEW"
    if action is PromotionAction.HOLD:
        return "HOLD"
    if action is PromotionAction.ROLL_BACK:
        return "ROLL_BACK"
    return "CONTINUE"


def _governed_write_handoff_summary(receipt: GovernedWriteReceipt) -> str | None:
    if receipt.application_result is None:
        return None
    return (
        f"Applied {len(receipt.application_result.artifact_paths)} artifact writes and "
        f"{len(receipt.application_result.state_targets)} state mutations."
    )


def _governed_write_next_route(receipt: GovernedWriteReceipt) -> str | None:
    if receipt.application_result is not None:
        return "Deliver bounded result into the next lawful review or signal step."
    action = receipt.threshold_evaluation.recommended_action
    if action is PromotionAction.REQUIRE_REVIEW:
        return "Escalate to review before any further promotion."
    if action is PromotionAction.HOLD:
        return "Hold route until blockers are cleared."
    if action is PromotionAction.ROLL_BACK:
        return "Return to manual continuity and reassess automation posture."
    return "Continue bounded execution."


def _branch_status_for_governed_write(receipt: GovernedWriteReceipt) -> RouteStage:
    if receipt.application_result is not None:
        return RouteStage.COMPLETED
    if receipt.passed and receipt.threshold_evaluation.recommended_action is PromotionAction.ALLOW_BOUNDED_PROMOTION:
        return RouteStage.ACTIVE
    if receipt.threshold_evaluation.recommended_action is PromotionAction.ROLL_BACK:
        return RouteStage.ABANDONED
    return RouteStage.BLOCKED


def _confidence_band(confidence: float | None) -> str:
    if confidence is None:
        return "UNKNOWN"
    if confidence >= 0.9:
        return "HIGH"
    if confidence >= 0.75:
        return "MEDIUM"
    return "LOW"


def _context_mode_from_value(value: str) -> ContextMode:
    try:
        return ContextMode(value)
    except ValueError:
        return ContextMode.IDE_MANUAL


def _automation_stage_from_value(value: str) -> AutomationStage:
    try:
        return AutomationStage(value)
    except ValueError:
        return AutomationStage.MANUAL



def _governed_write_stage_blockers(receipt: GovernedWriteReceipt) -> tuple[str, ...]:
    return tuple(
        stage.stage_name
        for stage in receipt.stages
        if (not stage.passed) and stage.stage_name != "GW3_THRESHOLD"
    )


def _gates_from_governed_write_receipt(receipt: GovernedWriteReceipt) -> tuple[AutomationGate, ...]:
    threshold_gates = list(_gates_from_threshold_evaluation(receipt.threshold_evaluation))
    threshold_gate_ids = {gate.gate_id for gate in threshold_gates}
    for stage in receipt.stages:
        if stage.passed or stage.stage_name == "GW3_THRESHOLD":
            continue
        gate_id = f"gate-{stage.stage_name.lower().replace('_', '-')}"
        if gate_id in threshold_gate_ids:
            continue
        threshold_gates.append(
            AutomationGate(
                gate_id=gate_id,
                gate_class=stage.stage_name,
                status="BLOCKED",
                satisfied=False,
                detail=stage.message,
                evidence_refs=(),
                required_for_promotion=True,
            )
        )
    return tuple(threshold_gates)

def _gates_from_threshold_evaluation(evaluation) -> tuple[AutomationGate, ...]:
    return tuple(
        AutomationGate(
            gate_id=f"gate-{hit.condition.reason.lower().replace('_', '-').strip('-') or 'threshold'}",
            gate_class=hit.condition.reason,
            status=("BLOCKED" if hit.triggered else "PASS"),
            satisfied=not hit.triggered,
            detail=hit.message,
            evidence_refs=tuple(str(item) for item in evaluation.snapshot.metadata.get("review_reasons", ())),
            required_for_promotion=True,
        )
        for hit in evaluation.hits
    )


def _safe_automation_stage(context_mode: ContextMode, stage: AutomationStage) -> AutomationStage:
    if context_mode is ContextMode.IDE_MANUAL and stage is AutomationStage.RUNTIME_ACTIVE:
        return AutomationStage.SUSPENDED
    return stage
