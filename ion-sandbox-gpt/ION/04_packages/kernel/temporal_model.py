from __future__ import annotations

"""Typed temporal evaluator structures.

These structures are intentionally verbose. The first landing should optimize
for clarity and auditability rather than compactness.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Any


class HeatLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class OrchestrationHeatState(str, Enum):
    FROZEN = "FROZEN"
    DORMANT = "DORMANT"
    COOL = "COOL"
    WARM = "WARM"
    HOT = "HOT"
    CRITICAL = "CRITICAL"
    COOLING = "COOLING"
    ARCHIVED = "ARCHIVED"


class LeaseRole(str, Enum):
    OWNER = "OWNER"
    WATCHER = "WATCHER"
    REVIEWER = "REVIEWER"
    PREPARER = "PREPARER"
    FALLBACK = "FALLBACK"
    DORMANT_STEWARD = "DORMANT_STEWARD"


class LeaseState(str, Enum):
    LATENT = "LATENT"
    WARM = "WARM"
    ACTIVE = "ACTIVE"
    REVIEW = "REVIEW"
    COOLING = "COOLING"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"
    TRANSFERRED = "TRANSFERRED"
    ARCHIVED = "ARCHIVED"


class AlignmentState(str, Enum):
    FULLY_ALIGNED = "FULLY_ALIGNED"
    CIVIL_LEADING = "CIVIL_LEADING"
    ORCHESTRATION_LEADING = "ORCHESTRATION_LEADING"
    BUDGET_LEADING = "BUDGET_LEADING"
    TRIPLE_TENSION = "TRIPLE_TENSION"


class ReconciliationPosture(str, Enum):
    PROCEED_NORMALLY = "PROCEED_NORMALLY"
    WARM_ONLY = "WARM_ONLY"
    RECONFIRM_FIRST = "RECONFIRM_FIRST"
    PREPARE_ONLY = "PREPARE_ONLY"
    COMPRESS = "COMPRESS"
    DEFER_WITH_CONTINUITY = "DEFER_WITH_CONTINUITY"
    ESCALATE = "ESCALATE"


@dataclass(frozen=True)
class TemporalCivilProfile:
    scheduled_at: str | None = None
    deadline_at: str | None = None
    timezone: str | None = None
    recurrence_rule: str | None = None
    alarm_windows: tuple[str, ...] = ()
    calendar_visibility: str | None = None
    real_world_commitment_strength: str | None = None
    user_confirmation_required: bool = False


@dataclass(frozen=True)
class TemporalOrchestrationProfile:
    horizon_class: str | None = None
    heat_state: OrchestrationHeatState = OrchestrationHeatState.COOL
    wake_conditions: tuple[str, ...] = ()
    cooldown_conditions: tuple[str, ...] = ()
    dormancy_conditions: tuple[str, ...] = ()
    activation_readiness: str | None = None
    dependency_pressure: str | None = None
    open_question_pressure: str | None = None
    reconfirmation_window: str | None = None
    preparation_window: str | None = None


@dataclass(frozen=True)
class TemporalBudgetProfile:
    estimated_token_burn: int | None = None
    estimated_slice_count: int | None = None
    effort_class: str | None = None
    confidence_band: str | None = None
    context_pressure: str | None = None
    throughput_requirement: str | None = None
    expected_tpm_band: str | None = None
    project_budget_ref: str | None = None
    compression_potential: str | None = None
    minimum_viable_slice: str | None = None
    reserve_sensitivity: str | None = None


@dataclass(frozen=True)
class TemporalLeaseProfile:
    lease_id: str | None = None
    holder_type: str | None = None
    holder_ref: str | None = None
    lease_role: LeaseRole | None = None
    lease_state: LeaseState | None = None
    fallback_holder_ref: str | None = None


@dataclass(frozen=True)
class TemporalObject:
    object_id: str
    object_type: str
    title: str
    status: str
    created_at: str
    updated_at: str
    civil: TemporalCivilProfile
    orchestration: TemporalOrchestrationProfile
    budget: TemporalBudgetProfile
    lease: TemporalLeaseProfile | None = None
    related_object_ids: tuple[str, ...] = ()
    dependency_ids: tuple[str, ...] = ()
    blocked_by_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class TemporalEvaluationContext:
    now_utc: str
    user_timezone: str
    resource_posture: str
    reserve_posture: str
    competing_hot_object_ids: tuple[str, ...] = ()
    recent_user_events: tuple[str, ...] = ()
    blocker_changes: tuple[str, ...] = ()
    prior_estimate_accuracy: str | None = None
    recurrence_history_summary: str | None = None


@dataclass(frozen=True)
class TemporalHeatVector:
    civil_heat: HeatLevel
    orchestration_heat: HeatLevel
    budget_heat: HeatLevel
    composite_relevance: HeatLevel


@dataclass(frozen=True)
class TemporalTransitionFlags:
    wake_required: bool
    reconfirm_required: bool
    prepare_required: bool
    cooling_permitted: bool
    dormant_eligible: bool


@dataclass(frozen=True)
class TemporalLeaseRecommendation:
    lease_required: bool
    holder_type: str | None
    holder_ref: str | None
    lease_role: LeaseRole | None
    lease_state: LeaseState | None
    transfer_required: bool
    downgrade_required: bool
    expiration_permitted: bool


@dataclass(frozen=True)
class TemporalReconciliationRecommendation:
    alignment_state: AlignmentState
    reconciliation_posture: ReconciliationPosture
    compress_required: bool
    defer_permitted: bool
    escalation_required: bool
    civil_manifestation_required: bool
    lease_adjustment_required: bool
    budget_warning_required: bool


@dataclass(frozen=True)
class TemporalConfidenceProfile:
    confidence_level: str
    missing_fields: tuple[str, ...] = ()
    uncertainty_notes: tuple[str, ...] = ()


@dataclass(frozen=True)
class TemporalRuleTrace:
    rule_id: str
    rule_group: str
    reason: str
    output_field: str
    output_value: Any


@dataclass(frozen=True)
class TemporalEvaluationResult:
    object_id: str
    heat: TemporalHeatVector
    transitions: TemporalTransitionFlags
    lease: TemporalLeaseRecommendation
    reconciliation: TemporalReconciliationRecommendation
    confidence: TemporalConfidenceProfile
    traces: tuple[TemporalRuleTrace, ...]
    decision_summary: str


@dataclass(frozen=True)
class TemporalEvaluationReceipt:
    receipt_id: str
    object_id: str
    evaluated_at: str
    evaluator_version: str
    input_summary: dict[str, Any]
    result_summary: dict[str, Any]
    trace_count: int


@dataclass(frozen=True)
class TemporalRecommendationEnvelope:
    evaluation: TemporalEvaluationResult
    recommended_actions: tuple[str, ...]
    receipt_required: bool
    escalation_target: str | None = None
