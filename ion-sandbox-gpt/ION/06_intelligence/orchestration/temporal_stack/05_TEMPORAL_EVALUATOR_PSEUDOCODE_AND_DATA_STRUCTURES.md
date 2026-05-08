# Temporal Evaluator Pseudocode and Data Structures

## 0. Purpose

This document translates the temporal evaluator design into concrete implementation-oriented structures.

It is not yet final code. It is a near-code design artifact intended to bridge protocol law and kernel implementation.

The focus is:

* typed evaluator inputs,
* typed evaluator outputs,
* rule-group decomposition,
* deterministic evaluation order,
* receipt-oriented design,
* and a conservative override-friendly execution model.

This document assumes the prior protocol and schema drafts already exist.

---

## 1. Design posture

The first evaluator must be:

* deterministic,
* inspectable,
* bounded,
* recommendation-oriented,
* and easy to audit.

It should therefore begin as:

* a pure function over normalized temporal objects plus context,
* a rule engine with explicit traces,
* and a producer of recommendation records rather than direct world mutations.

That means the evaluator should not itself:

* send reminders,
* mutate calendar state,
* create runtime sessions,
* dispatch work,
* or enact activation crossings.

It should only evaluate and recommend.

---

## 2. Core type families

A minimal implementation likely needs the following type families.

### 2.1 Object and context types

* `TemporalObject`
* `TemporalCivilProfile`
* `TemporalOrchestrationProfile`
* `TemporalBudgetProfile`
* `TemporalLeaseProfile`
* `TemporalReconciliationProfile`
* `TemporalEvaluationContext`

### 2.2 Derived signal types

* `TemporalHeatVector`
* `TemporalTransitionFlags`
* `TemporalLeaseRecommendation`
* `TemporalReconciliationRecommendation`
* `TemporalConfidenceProfile`

### 2.3 Result and audit types

* `TemporalRuleTrace`
* `TemporalEvaluationResult`
* `TemporalEvaluationReceipt`
* `TemporalRecommendationEnvelope`

---

## 3. Candidate data structures

Below is a first-pass implementation sketch in Python-like pseudocode.

```python
from dataclasses import dataclass, field
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
```

These structures are intentionally verbose. The first implementation should optimize for clarity rather than elegance.

---

## 4. Rule decomposition

The evaluator should not be implemented as one giant function.

A better structure is a series of rule groups.

### 4.1 Rule groups

* `civil_rules`
* `orchestration_rules`
* `budget_rules`
* `transition_rules`
* `lease_rules`
* `reconciliation_rules`
* `confidence_rules`
* `summary_rules`

Each group should accept typed inputs and return outputs plus trace entries.

### 4.2 Why rule groups matter

This makes it possible to:

* test each group independently,
* audit why a result was produced,
* swap conservative rules for richer rules later,
* and keep the evaluator explainable.

---

## 5. Candidate top-level evaluator shape

A first-pass top-level evaluator may look like this.

```python
def evaluate_temporal_object(
    obj: TemporalObject,
    ctx: TemporalEvaluationContext,
) -> TemporalEvaluationResult:
    traces: list[TemporalRuleTrace] = []

    civil_heat, civil_traces = evaluate_civil_heat(obj, ctx)
    traces.extend(civil_traces)

    orchestration_heat, orchestration_traces = evaluate_orchestration_heat(obj, ctx)
    traces.extend(orchestration_traces)

    budget_heat, budget_traces = evaluate_budget_heat(obj, ctx)
    traces.extend(budget_traces)

    heat = derive_heat_vector(
        civil_heat=civil_heat,
        orchestration_heat=orchestration_heat,
        budget_heat=budget_heat,
    )
    traces.append(
        TemporalRuleTrace(
            rule_id="derive_heat_vector",
            rule_group="summary_rules",
            reason="Derived composite relevance from three heat dimensions.",
            output_field="composite_relevance",
            output_value=heat.composite_relevance,
        )
    )

    transitions, transition_traces = evaluate_transition_flags(obj, ctx, heat)
    traces.extend(transition_traces)

    lease, lease_traces = evaluate_lease_recommendation(obj, ctx, heat, transitions)
    traces.extend(lease_traces)

    reconciliation, reconciliation_traces = evaluate_reconciliation(
        obj,
        ctx,
        heat,
        transitions,
        lease,
    )
    traces.extend(reconciliation_traces)

    confidence, confidence_traces = evaluate_confidence(obj, ctx, heat, traces)
    traces.extend(confidence_traces)

    decision_summary = build_decision_summary(
        obj=obj,
        heat=heat,
        transitions=transitions,
        lease=lease,
        reconciliation=reconciliation,
        confidence=confidence,
    )

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
```

This function should remain pure and side-effect free.

---

## 6. Civil heat pseudocode

The civil heat evaluator should stay simple in v1.

```python
def evaluate_civil_heat(obj, ctx):
    traces = []
    score = 0

    if obj.civil.deadline_at is not None:
        # pseudocode: compare now to deadline
        deadline_distance = distance_to_deadline(ctx.now_utc, obj.civil.deadline_at)
        if deadline_distance <= "24h":
            score += 3
            traces.append(trace("civil_deadline_24h", "civil_rules", "deadline within 24h", "civil_heat_score", score))
        elif deadline_distance <= "72h":
            score += 2
            traces.append(trace("civil_deadline_72h", "civil_rules", "deadline within 72h", "civil_heat_score", score))
        else:
            score += 1
            traces.append(trace("civil_deadline_far", "civil_rules", "deadline exists but is not near", "civil_heat_score", score))

    if obj.civil.recurrence_rule is not None and recurrence_window_open(obj, ctx):
        score += 2
        traces.append(trace("civil_recurrence_window", "civil_rules", "recurrence window is open", "civil_heat_score", score))

    if obj.civil.user_confirmation_required:
        score += 1
        traces.append(trace("civil_confirmation_required", "civil_rules", "user confirmation required", "civil_heat_score", score))

    return heat_from_score(score), traces
```

The first version does not need perfect calendrical intelligence. It needs clear bounded behavior.

---

## 7. Orchestration heat pseudocode

```python
def evaluate_orchestration_heat(obj, ctx):
    traces = []
    score = 0

    if obj.orchestration.horizon_class == "NEAR":
        score += 2
        traces.append(trace("orch_near_horizon", "orchestration_rules", "near horizon object", "orch_heat_score", score))

    if obj.orchestration.dependency_pressure in ("MEDIUM", "HIGH"):
        score += 2
        traces.append(trace("orch_dependency_pressure", "orchestration_rules", "dependency pressure present", "orch_heat_score", score))

    if obj.blocked_by_ids and blocker_change_detected(obj, ctx):
        score += 2
        traces.append(trace("orch_blocker_changed", "orchestration_rules", "blocker state changed", "orch_heat_score", score))

    if obj.orchestration.reconfirmation_window is not None and reconfirmation_window_open(obj, ctx):
        score += 2
        traces.append(trace("orch_reconfirm_window", "orchestration_rules", "reconfirmation window open", "orch_heat_score", score))

    if obj.lease and obj.lease.lease_state in {LeaseState.ACTIVE, LeaseState.WARM, LeaseState.REVIEW}:
        score += 1
        traces.append(trace("orch_active_lease", "orchestration_rules", "active or warming lease present", "orch_heat_score", score))

    return heat_from_score(score), traces
```

This reflects that orchestration heat is about workflow force, not just dates.

---

## 8. Budget heat pseudocode

Budget heat is the most subtle dimension because high budget heat signals tension, not importance.

```python
def evaluate_budget_heat(obj, ctx):
    traces = []
    score = 0

    if ctx.resource_posture in ("CONSTRAINED", "EMERGENCY_ONLY"):
        score += 2
        traces.append(trace("budget_resource_constrained", "budget_rules", "resource posture constrained", "budget_heat_score", score))

    if obj.budget.reserve_sensitivity in ("MEDIUM", "HIGH"):
        score += 1
        traces.append(trace("budget_reserve_sensitive", "budget_rules", "reserve sensitivity present", "budget_heat_score", score))

    if obj.budget.estimated_token_burn is not None and high_burn_relative_to_posture(obj, ctx):
        score += 2
        traces.append(trace("budget_high_burn", "budget_rules", "estimated burn high relative to posture", "budget_heat_score", score))

    if obj.budget.compression_potential in ("MEDIUM", "HIGH"):
        traces.append(trace("budget_compression_possible", "budget_rules", "compression is available", "budget_compression_signal", True))

    return heat_from_score(score), traces
```

Budget heat should usually be treated as a tension indicator, not a go-signal.

---

## 9. Transition flags pseudocode

```python
def evaluate_transition_flags(obj, ctx, heat):
    traces = []

    wake_required = heat.orchestration_heat in {HeatLevel.HIGH, HeatLevel.CRITICAL}
    if wake_required:
        traces.append(trace("transition_wake", "transition_rules", "high orchestration heat requires wake", "wake_required", True))

    reconfirm_required = (
        obj.civil.user_confirmation_required
        and heat.civil_heat in {HeatLevel.HIGH, HeatLevel.CRITICAL}
    ) or reconfirmation_window_open(obj, ctx)
    if reconfirm_required:
        traces.append(trace("transition_reconfirm", "transition_rules", "reconfirmation condition met", "reconfirm_required", True))

    prepare_required = (
        obj.orchestration.preparation_window is not None
        and heat.orchestration_heat in {HeatLevel.MEDIUM, HeatLevel.HIGH, HeatLevel.CRITICAL}
    )
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
```

---

## 10. Lease recommendation pseudocode

```python
def evaluate_lease_recommendation(obj, ctx, heat, transitions):
    traces = []

    lease_required = heat.composite_relevance in {HeatLevel.MEDIUM, HeatLevel.HIGH, HeatLevel.CRITICAL}

    role = None
    state = None

    if transitions.reconfirm_required:
        role = LeaseRole.REVIEWER
        state = LeaseState.REVIEW
        traces.append(trace("lease_reviewer", "lease_rules", "reconfirmation required", "lease_role", role))
    elif transitions.prepare_required:
        role = LeaseRole.PREPARER
        state = LeaseState.ACTIVE
        traces.append(trace("lease_preparer", "lease_rules", "preparation required", "lease_role", role))
    elif transitions.wake_required:
        role = LeaseRole.WATCHER
        state = LeaseState.WARM
        traces.append(trace("lease_watcher", "lease_rules", "wake required", "lease_role", role))
    elif transitions.dormant_eligible:
        role = LeaseRole.DORMANT_STEWARD
        state = LeaseState.LATENT
        traces.append(trace("lease_dormant", "lease_rules", "dormancy eligible", "lease_role", role))

    transfer_required = False
    downgrade_required = transitions.cooling_permitted
    expiration_permitted = transitions.dormant_eligible or transitions.cooling_permitted

    return TemporalLeaseRecommendation(
        lease_required=lease_required,
        holder_type="SUBSYSTEM" if lease_required else None,
        holder_ref="TEMPORAL_RUNTIME" if lease_required else None,
        lease_role=role,
        lease_state=state,
        transfer_required=transfer_required,
        downgrade_required=downgrade_required,
        expiration_permitted=expiration_permitted,
    ), traces
```

This is intentionally simple. The first implementation should only prove the concept.

---

## 11. Reconciliation pseudocode

```python
def evaluate_reconciliation(obj, ctx, heat, transitions, lease):
    traces = []

    if heat.civil_heat in {HeatLevel.HIGH, HeatLevel.CRITICAL} and heat.orchestration_heat in {HeatLevel.HIGH, HeatLevel.CRITICAL} and heat.budget_heat in {HeatLevel.LOW, HeatLevel.MEDIUM}:
        alignment = AlignmentState.FULLY_ALIGNED
        posture = ReconciliationPosture.PREPARE_ONLY if transitions.prepare_required else ReconciliationPosture.PROCEED_NORMALLY
        traces.append(trace("reconcile_fully_aligned", "reconciliation_rules", "civil and orchestration urgency with feasible budget", "reconciliation_posture", posture))

    elif heat.civil_heat in {HeatLevel.HIGH, HeatLevel.CRITICAL} and heat.budget_heat in {HeatLevel.HIGH, HeatLevel.CRITICAL}:
        alignment = AlignmentState.BUDGET_LEADING
        posture = ReconciliationPosture.COMPRESS if compression_possible(obj) else ReconciliationPosture.ESCALATE
        traces.append(trace("reconcile_budget_tension", "reconciliation_rules", "civil urgency under budget tension", "reconciliation_posture", posture))

    elif heat.civil_heat in {HeatLevel.HIGH, HeatLevel.CRITICAL} and heat.orchestration_heat in {HeatLevel.LOW, HeatLevel.MEDIUM}:
        alignment = AlignmentState.CIVIL_LEADING
        posture = ReconciliationPosture.RECONFIRM_FIRST
        traces.append(trace("reconcile_civil_leading", "reconciliation_rules", "civil urgency exceeds orchestration readiness", "reconciliation_posture", posture))

    elif heat.orchestration_heat in {HeatLevel.HIGH, HeatLevel.CRITICAL} and heat.civil_heat in {HeatLevel.LOW, HeatLevel.MEDIUM}:
        alignment = AlignmentState.ORCHESTRATION_LEADING
        posture = ReconciliationPosture.WARM_ONLY if not transitions.prepare_required else ReconciliationPosture.PREPARE_ONLY
        traces.append(trace("reconcile_orch_leading", "reconciliation_rules", "workflow pressure exceeds civil urgency", "reconciliation_posture", posture))

    else:
        alignment = AlignmentState.TRIPLE_TENSION
        posture = ReconciliationPosture.ESCALATE
        traces.append(trace("reconcile_triple_tension", "reconciliation_rules", "no simple alignment found", "reconciliation_posture", posture))

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
```

---

## 12. Confidence pseudocode

```python
def evaluate_confidence(obj, ctx, heat, traces):
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
    elif len(missing) >= 1:
        level = "MEDIUM"
        notes.append("Some temporal inputs are incomplete.")
    else:
        level = "HIGH"

    return TemporalConfidenceProfile(
        confidence_level=level,
        missing_fields=tuple(missing),
        uncertainty_notes=tuple(notes),
    ), []
```

Confidence should remain simple and explicit at first.

---

## 13. Trace helper

A helper function keeps traces consistent.

```python
def trace(rule_id, rule_group, reason, output_field, output_value):
    return TemporalRuleTrace(
        rule_id=rule_id,
        rule_group=rule_group,
        reason=reason,
        output_field=output_field,
        output_value=output_value,
    )
```

---

## 14. Summary builder

The evaluator should always be able to produce a human-readable decision summary.

```python
def build_decision_summary(obj, heat, transitions, lease, reconciliation, confidence):
    return (
        f"Object {obj.object_id} evaluated with civil={heat.civil_heat}, "
        f"orchestration={heat.orchestration_heat}, budget={heat.budget_heat}. "
        f"Posture={reconciliation.reconciliation_posture}. "
        f"Lease role={lease.lease_role}. "
        f"Confidence={confidence.confidence_level}."
    )
```

This summary is not sufficient for full audit, but it is important for first user-facing or developer-facing explanation.

---

## 15. Recommendation envelope

The evaluator’s result should probably be wrapped in a recommendation envelope before any runtime consumes it.

```python
@dataclass(frozen=True)
class TemporalRecommendationEnvelope:
    evaluation: TemporalEvaluationResult
    recommended_actions: tuple[str, ...]
    receipt_required: bool
    escalation_target: str | None = None
```

This ensures the next layer receives explicit recommendation structure rather than raw signals only.

---

## 16. Narrow initial object-family adapters

The evaluator should probably not read arbitrary raw records directly.

Instead, it should begin with adapters.

Examples:

* `ScheduledDeliverableAdapter`
* `RecurringReviewAdapter`
* `DormantCommitmentAdapter`

Each adapter would map current object shapes into `TemporalObject`.

That makes the evaluator usable before a full temporal object migration exists.

---

## 17. Minimal tests to define early

The first implementation should be test-defined.

### 17.1 Scheduled deliverable near deadline

Expected:

* high civil heat,
* likely reconfirm or prepare recommendation,
* preparer or reviewer lease,
* no silent enactment.

### 17.2 Recurring review one day before recurrence

Expected:

* medium civil heat,
* warm orchestration heat,
* watcher or preparer lease,
* warm-only or prepare-only posture.

### 17.3 Dormant commitment with blocker removed

Expected:

* low civil heat,
* high orchestration heat,
* watcher lease,
* warm-only or prepare-only posture.

### 17.4 Budget-constrained urgent deliverable

Expected:

* high civil heat,
* high orchestration heat,
* high budget tension,
* compression or escalation posture.

These tests should exist before the evaluator is trusted.

---

## 18. Failure mode traps for implementation

The most important traps to avoid in code are:

* mutating the object inside the evaluator,
* hiding rule traces,
* flattening the three clocks into one urgency score,
* silently escalating without receipt,
* treating budget heat as importance rather than tension,
* and letting adapters leak arbitrary object semantics into core evaluator logic.

---

## 19. Strongest present conclusion

The evaluator can now be described almost as code.

The next step after this document is no longer more abstract protocol writing. It is one of two things:

1. implement the typed evaluator shell and adapters in a bounded kernel module, or
2. map these types and adapters directly onto present ION records so an implementation plan can be made without guessing.

This is the point where the temporal stack becomes buildable.
