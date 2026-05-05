from __future__ import annotations

"""Conservative temporal relevance evaluation helpers."""

from .temporal_model import HeatLevel, LeaseState, TemporalHeatVector, TemporalRuleTrace, TemporalTransitionFlags


def trace(rule_id: str, rule_group: str, reason: str, output_field: str, output_value: object) -> TemporalRuleTrace:
    return TemporalRuleTrace(
        rule_id=rule_id,
        rule_group=rule_group,
        reason=reason,
        output_field=output_field,
        output_value=output_value,
    )


def heat_from_score(score: int) -> HeatLevel:
    if score >= 5:
        return HeatLevel.CRITICAL
    if score >= 3:
        return HeatLevel.HIGH
    if score >= 1:
        return HeatLevel.MEDIUM
    return HeatLevel.LOW


def deadline_distance_bucket(now_utc: str, deadline_at: str | None) -> str | None:
    if not deadline_at:
        return None
    # Conservative starter: callers may pass a bucket directly in prototypes.
    if deadline_at in {"24h", "72h", ">72h"}:
        return deadline_at
    return ">72h"


def recurrence_window_open(obj, ctx) -> bool:
    return bool(obj.civil.recurrence_rule and "RECURRENCE_WINDOW_OPEN" in ctx.recent_user_events)


def reconfirmation_window_open(obj, ctx) -> bool:
    return obj.orchestration.reconfirmation_window is not None and (
        "RECONFIRM_WINDOW_OPEN" in ctx.recent_user_events or obj.civil.user_confirmation_required
    )


def blocker_change_detected(obj, ctx) -> bool:
    return bool(obj.blocked_by_ids) and bool(ctx.blocker_changes)


def cooling_condition_met(obj, ctx) -> bool:
    return obj.status in {"COMPLETED", "CANCELLED", "SUPERSEDED"}


def dormancy_condition_met(obj, ctx) -> bool:
    return obj.status in {"DEFERRED", "DORMANT"}


def evaluate_civil_heat(obj, ctx):
    traces = []
    score = 0
    bucket = deadline_distance_bucket(ctx.now_utc, obj.civil.deadline_at)
    if bucket == "24h":
        score += 3
        traces.append(trace("civil_deadline_24h", "civil_rules", "deadline within 24h", "civil_heat_score", score))
    elif bucket == "72h":
        score += 2
        traces.append(trace("civil_deadline_72h", "civil_rules", "deadline within 72h", "civil_heat_score", score))
    elif bucket == ">72h" and obj.civil.deadline_at is not None:
        score += 1
        traces.append(trace("civil_deadline_far", "civil_rules", "deadline exists but is not near", "civil_heat_score", score))

    if recurrence_window_open(obj, ctx):
        score += 2
        traces.append(trace("civil_recurrence_window", "civil_rules", "recurrence window is open", "civil_heat_score", score))

    if obj.civil.user_confirmation_required:
        score += 1
        traces.append(trace("civil_confirmation_required", "civil_rules", "user confirmation required", "civil_heat_score", score))

    return heat_from_score(score), traces


def evaluate_orchestration_heat(obj, ctx):
    traces = []
    score = 0
    if obj.orchestration.horizon_class == "NEAR":
        score += 2
        traces.append(trace("orch_near_horizon", "orchestration_rules", "near horizon object", "orch_heat_score", score))

    if obj.orchestration.dependency_pressure in {"MEDIUM", "HIGH"}:
        score += 2
        traces.append(trace("orch_dependency_pressure", "orchestration_rules", "dependency pressure present", "orch_heat_score", score))

    if blocker_change_detected(obj, ctx):
        score += 2
        traces.append(trace("orch_blocker_changed", "orchestration_rules", "blocker state changed", "orch_heat_score", score))

    if reconfirmation_window_open(obj, ctx):
        score += 2
        traces.append(trace("orch_reconfirm_window", "orchestration_rules", "reconfirmation window open", "orch_heat_score", score))

    if obj.lease and obj.lease.lease_state in {LeaseState.ACTIVE, LeaseState.WARM, LeaseState.REVIEW}:
        score += 1
        traces.append(trace("orch_active_lease", "orchestration_rules", "active or warming lease present", "orch_heat_score", score))

    return heat_from_score(score), traces


def high_burn_relative_to_posture(obj, ctx) -> bool:
    return bool(obj.budget.estimated_token_burn and obj.budget.estimated_token_burn >= 100000 and ctx.resource_posture in {"CONSTRAINED", "EMERGENCY_ONLY"})


def evaluate_budget_heat(obj, ctx):
    traces = []
    score = 0
    if ctx.resource_posture in {"CONSTRAINED", "EMERGENCY_ONLY"}:
        score += 2
        traces.append(trace("budget_resource_constrained", "budget_rules", "resource posture constrained", "budget_heat_score", score))
    if obj.budget.reserve_sensitivity in {"MEDIUM", "HIGH"}:
        score += 1
        traces.append(trace("budget_reserve_sensitive", "budget_rules", "reserve sensitivity present", "budget_heat_score", score))
    if high_burn_relative_to_posture(obj, ctx):
        score += 2
        traces.append(trace("budget_high_burn", "budget_rules", "estimated burn high relative to posture", "budget_heat_score", score))
    if obj.budget.compression_potential in {"MEDIUM", "HIGH"}:
        traces.append(trace("budget_compression_possible", "budget_rules", "compression is available", "budget_compression_signal", True))
    return heat_from_score(score), traces


def derive_heat_vector(*, civil_heat: HeatLevel, orchestration_heat: HeatLevel, budget_heat: HeatLevel) -> TemporalHeatVector:
    # Composite relevance weights civil + orchestration; budget acts as tension, not importance.
    ordering = {HeatLevel.LOW: 0, HeatLevel.MEDIUM: 1, HeatLevel.HIGH: 2, HeatLevel.CRITICAL: 3}
    composite_idx = max(ordering[civil_heat], ordering[orchestration_heat])
    composite = [HeatLevel.LOW, HeatLevel.MEDIUM, HeatLevel.HIGH, HeatLevel.CRITICAL][composite_idx]
    return TemporalHeatVector(
        civil_heat=civil_heat,
        orchestration_heat=orchestration_heat,
        budget_heat=budget_heat,
        composite_relevance=composite,
    )


def evaluate_transition_flags(obj, ctx, heat: TemporalHeatVector):
    traces = []
    wake_required = heat.orchestration_heat in {HeatLevel.HIGH, HeatLevel.CRITICAL}
    if wake_required:
        traces.append(trace("transition_wake", "transition_rules", "high orchestration heat requires wake", "wake_required", True))

    reconfirm_required = (obj.civil.user_confirmation_required and heat.civil_heat in {HeatLevel.HIGH, HeatLevel.CRITICAL}) or reconfirmation_window_open(obj, ctx)
    if reconfirm_required:
        traces.append(trace("transition_reconfirm", "transition_rules", "reconfirmation condition met", "reconfirm_required", True))

    prepare_required = obj.orchestration.preparation_window is not None and heat.orchestration_heat in {HeatLevel.MEDIUM, HeatLevel.HIGH, HeatLevel.CRITICAL}
    if prepare_required:
        traces.append(trace("transition_prepare", "transition_rules", "preparation window condition met", "prepare_required", True))

    cooling_permitted = cooling_condition_met(obj, ctx)
    if cooling_permitted:
        traces.append(trace("transition_cooling", "transition_rules", "cooling condition met", "cooling_permitted", True))

    dormant_eligible = dormancy_condition_met(obj, ctx)
    if dormant_eligible:
        traces.append(trace("transition_dormant", "transition_rules", "dormancy condition met", "dormant_eligible", True))

    return TemporalTransitionFlags(
        wake_required=wake_required,
        reconfirm_required=reconfirm_required,
        prepare_required=prepare_required,
        cooling_permitted=cooling_permitted,
        dormant_eligible=dormant_eligible,
    ), traces
