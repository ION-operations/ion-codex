from __future__ import annotations

"""Top-level conservative temporal evaluator."""

from .temporal_model import TemporalConfidenceProfile, TemporalEvaluationResult, TemporalRuleTrace
from .temporal_relevance import (
    derive_heat_vector,
    evaluate_budget_heat,
    evaluate_civil_heat,
    evaluate_orchestration_heat,
    evaluate_transition_flags,
    trace,
)
from .temporal_leases import evaluate_lease_recommendation
from .temporal_reconciliation import evaluate_reconciliation
from .temporal_receipts import build_decision_summary


def evaluate_confidence(obj, ctx, heat, traces: list[TemporalRuleTrace]):
    missing = []
    notes = []
    if obj.civil.deadline_at is None and obj.civil.scheduled_at is None:
        missing.append("civil_profile_time_anchor")
    if obj.budget.estimated_token_burn is None:
        missing.append("estimated_token_burn")
    if obj.orchestration.horizon_class is None:
        missing.append("horizon_class")

    if len(missing) >= 3:
        level = "LOW"
        notes.append("Several critical temporal fields are missing.")
    elif missing:
        level = "MEDIUM"
        notes.append("Some temporal inputs are incomplete.")
    else:
        level = "HIGH"
    traces.append(trace("confidence_profile", "confidence_rules", "confidence derived from field completeness", "confidence_level", level))
    return TemporalConfidenceProfile(confidence_level=level, missing_fields=tuple(missing), uncertainty_notes=tuple(notes)), traces


def evaluate_temporal_object(obj, ctx) -> TemporalEvaluationResult:
    traces: list[TemporalRuleTrace] = []
    civil_heat, civil_traces = evaluate_civil_heat(obj, ctx)
    traces.extend(civil_traces)

    orchestration_heat, orch_traces = evaluate_orchestration_heat(obj, ctx)
    traces.extend(orch_traces)

    budget_heat, budget_traces = evaluate_budget_heat(obj, ctx)
    traces.extend(budget_traces)

    heat = derive_heat_vector(
        civil_heat=civil_heat,
        orchestration_heat=orchestration_heat,
        budget_heat=budget_heat,
    )
    traces.append(trace("derive_heat_vector", "summary_rules", "Derived composite relevance from three heat dimensions.", "composite_relevance", heat.composite_relevance.value))

    transitions, transition_traces = evaluate_transition_flags(obj, ctx, heat)
    traces.extend(transition_traces)

    lease, lease_traces = evaluate_lease_recommendation(obj, ctx, heat, transitions)
    traces.extend(lease_traces)

    reconciliation, reconciliation_traces = evaluate_reconciliation(obj, ctx, heat, transitions, lease)
    traces.extend(reconciliation_traces)

    confidence, traces = evaluate_confidence(obj, ctx, heat, traces)

    decision_summary = build_decision_summary(obj, heat, transitions, lease, reconciliation, confidence)
    return TemporalEvaluationResult(
        object_id=obj.object_id,
        heat=heat,
        transitions=transitions,
        lease=lease,
        reconciliation=reconciliation,
        confidence=confidence,
        traces=tuple(traces),
        decision_summary=decision_summary,
    )
