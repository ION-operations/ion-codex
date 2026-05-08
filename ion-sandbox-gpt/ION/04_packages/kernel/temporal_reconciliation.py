from __future__ import annotations

"""Triple-time reconciliation recommendation logic."""

from .temporal_model import AlignmentState, HeatLevel, ReconciliationPosture, TemporalReconciliationRecommendation
from .temporal_relevance import trace


def compression_possible(obj) -> bool:
    return obj.budget.compression_potential in {"MEDIUM", "HIGH"}


def evaluate_reconciliation(obj, ctx, heat, transitions, lease):
    traces = []
    if heat.civil_heat in {HeatLevel.HIGH, HeatLevel.CRITICAL} and heat.orchestration_heat in {HeatLevel.HIGH, HeatLevel.CRITICAL} and heat.budget_heat in {HeatLevel.LOW, HeatLevel.MEDIUM}:
        alignment = AlignmentState.FULLY_ALIGNED
        posture = ReconciliationPosture.PREPARE_ONLY if transitions.prepare_required else ReconciliationPosture.PROCEED_NORMALLY
        traces.append(trace("reconcile_fully_aligned", "reconciliation_rules", "civil and orchestration urgency with feasible budget", "reconciliation_posture", posture.value))
    elif heat.civil_heat in {HeatLevel.HIGH, HeatLevel.CRITICAL} and heat.budget_heat in {HeatLevel.HIGH, HeatLevel.CRITICAL}:
        alignment = AlignmentState.BUDGET_LEADING
        posture = ReconciliationPosture.COMPRESS if compression_possible(obj) else ReconciliationPosture.ESCALATE
        traces.append(trace("reconcile_budget_tension", "reconciliation_rules", "civil urgency under budget tension", "reconciliation_posture", posture.value))
    elif heat.civil_heat in {HeatLevel.HIGH, HeatLevel.CRITICAL} and heat.orchestration_heat in {HeatLevel.LOW, HeatLevel.MEDIUM}:
        alignment = AlignmentState.CIVIL_LEADING
        posture = ReconciliationPosture.RECONFIRM_FIRST
        traces.append(trace("reconcile_civil_leading", "reconciliation_rules", "civil urgency exceeds orchestration readiness", "reconciliation_posture", posture.value))
    elif heat.orchestration_heat in {HeatLevel.HIGH, HeatLevel.CRITICAL} and heat.civil_heat in {HeatLevel.LOW, HeatLevel.MEDIUM}:
        alignment = AlignmentState.ORCHESTRATION_LEADING
        posture = ReconciliationPosture.PREPARE_ONLY if transitions.prepare_required else ReconciliationPosture.WARM_ONLY
        traces.append(trace("reconcile_orch_leading", "reconciliation_rules", "workflow pressure exceeds civil urgency", "reconciliation_posture", posture.value))
    else:
        alignment = AlignmentState.TRIPLE_TENSION
        posture = ReconciliationPosture.ESCALATE
        traces.append(trace("reconcile_triple_tension", "reconciliation_rules", "no simple alignment found", "reconciliation_posture", posture.value))

    return TemporalReconciliationRecommendation(
        alignment_state=alignment,
        reconciliation_posture=posture,
        compress_required=(posture == ReconciliationPosture.COMPRESS),
        defer_permitted=(posture == ReconciliationPosture.DEFER_WITH_CONTINUITY),
        escalation_required=(posture == ReconciliationPosture.ESCALATE),
        civil_manifestation_required=heat.civil_heat in {HeatLevel.HIGH, HeatLevel.CRITICAL},
        lease_adjustment_required=lease.lease_required,
        budget_warning_required=heat.budget_heat in {HeatLevel.HIGH, HeatLevel.CRITICAL},
    ), traces
