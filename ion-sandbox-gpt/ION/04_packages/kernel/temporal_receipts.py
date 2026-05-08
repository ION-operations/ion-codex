from __future__ import annotations

"""Receipt and summary helpers for temporal evaluator outputs."""

from dataclasses import asdict
from uuid import uuid4

from .temporal_model import TemporalEvaluationReceipt, TemporalRecommendationEnvelope


def build_decision_summary(obj, heat, transitions, lease, reconciliation, confidence) -> str:
    return (
        f"Object {obj.object_id} evaluated with civil={heat.civil_heat.value}, "
        f"orchestration={heat.orchestration_heat.value}, budget={heat.budget_heat.value}. "
        f"Posture={reconciliation.reconciliation_posture.value}. "
        f"Lease role={(lease.lease_role.value if lease.lease_role else 'NONE')}. "
        f"Confidence={confidence.confidence_level}."
    )


def build_receipt(result, *, evaluated_at: str, evaluator_version: str = "temporal-evaluator-v0") -> TemporalEvaluationReceipt:
    return TemporalEvaluationReceipt(
        receipt_id=f"TEMPREC-{uuid4().hex[:12]}",
        object_id=result.object_id,
        evaluated_at=evaluated_at,
        evaluator_version=evaluator_version,
        input_summary={},
        result_summary={
            "heat": asdict(result.heat),
            "transitions": asdict(result.transitions),
            "lease": asdict(result.lease),
            "reconciliation": asdict(result.reconciliation),
            "confidence": asdict(result.confidence),
            "decision_summary": result.decision_summary,
        },
        trace_count=len(result.traces),
    )


def build_envelope(result) -> TemporalRecommendationEnvelope:
    actions = []
    if result.transitions.reconfirm_required:
        actions.append("RECONFIRM")
    if result.transitions.prepare_required:
        actions.append("PREPARE")
    if result.reconciliation.compress_required:
        actions.append("COMPRESS")
    if result.reconciliation.escalation_required:
        actions.append("ESCALATE")
    if result.lease.lease_required:
        actions.append("ASSIGN_LEASE")
    return TemporalRecommendationEnvelope(
        evaluation=result,
        recommended_actions=tuple(actions),
        receipt_required=True,
        escalation_target=("TEMPORAL_SUPERVISOR" if result.reconciliation.escalation_required else None),
    )
