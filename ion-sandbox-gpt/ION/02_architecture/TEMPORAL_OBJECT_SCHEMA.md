# TEMPORAL_OBJECT_SCHEMA Draft

## 0. Status

Draft schema for ION temporal development.

This schema is intended to provide a shared backbone for:

* `ORCHESTRATION_TEMPORAL_RELEVANCE_PROTOCOL`
* `TEMPORAL_CONTEXT_LEASE_PROTOCOL`
* `TRIPLE_TIME_RECONCILIATION_PROTOCOL`

It is not yet a final storage format. It is a canonical object vocabulary draft.

---

## 1. Purpose

ION requires a common temporal object schema so that future-bearing entities can be reasoned about across:

* civil time,
* orchestration time,
* budget time,
* lease ownership,
* receipts,
* and reconciliation.

Without a shared schema, each protocol risks inventing its own incompatible object model.

This schema therefore exists to ensure that temporal relevance, temporal leases, and triple-time reconciliation all operate over the same conceptual substrate.

---

## 2. Non-goals

This schema does **not** yet define:

* a final database layout,
* a single file format,
* a UI representation,
* a specific runtime API surface,
* or a final storage backend.

This document defines canonical object fields and relations, not the final implementation substrate.

---

## 3. Core thesis

A temporal object is any object whose relevance unfolds across time and whose present significance depends on the interaction of:

* past history,
* current workflow state,
* future commitments,
* and capability posture.

Temporal objects should therefore not be represented as flat reminders or bare tasks. They should be represented as lawful entities with multiple temporal projections and explicit lineage.

---

## 4. Canonical temporal object categories

A temporal object may belong to one or more categories.

### 4.1 Commitment objects

Examples:

* reports
* obligations
* deliverables
* deadlines
* appointments
* promises

### 4.2 Workflow objects

Examples:

* branch activations
* deferred missions
* preparation windows
* review checkpoints
* escalation points

### 4.3 Recurring objects

Examples:

* weekly review
* recurring maintenance
* periodic check-in
* recurring research cadence

### 4.4 Dormant objects

Examples:

* paused obligations
* latent future plans
* future candidates
* deferred but still alive commitments

### 4.5 Budget and capacity objects

Examples:

* project budget envelope
* reserve warning checkpoint
* re-estimation event
* forecast recalibration checkpoint

---

## 5. Object identity layer

Every temporal object requires stable identity.

### 5.1 Core identity fields

* `object_id`
* `object_type`
* `title`
* `description`
* `created_at`
* `updated_at`
* `created_by`
* `origin_surface`
* `status`

### 5.2 Lineage fields

* `parent_object_id`
* `supersedes`
* `superseded_by`
* `derived_from`
* `recurs_from`
* `recurs_to`
* `historical_lineage_ref`

### 5.3 Relation fields

* `related_object_ids`
* `dependency_ids`
* `blocked_by_ids`
* `supports_ids`
* `conflicts_with_ids`

This layer answers the question: what object is this, where did it come from, and what is it related to?

---

## 6. Civil profile

The civil profile describes how the object exists in the user/world time reality.

### 6.1 Civil fields

* `scheduled_at`
* `deadline_at`
* `timezone`
* `recurrence_rule`
* `alarm_windows`
* `calendar_visibility`
* `real_world_commitment_strength`
* `user_confirmation_required`
* `civil_priority`

### 6.2 Civil semantics

These fields answer questions like:

* When is this due in real-world time?
* Is it recurring?
* Should it appear on the civil calendar?
* Does the user expect reminders or confirmation?

The civil profile does not define orchestration heat or budget feasibility.

---

## 7. Orchestration profile

The orchestration profile describes the object’s internal relevance in the ION workflow field.

### 7.1 Orchestration fields

* `horizon_class`
* `orchestration_heat`
* `composite_relevance`
* `wake_conditions`
* `cooldown_conditions`
* `dormancy_conditions`
* `activation_readiness`
* `dependency_pressure`
* `open_question_pressure`
* `reconfirmation_window`
* `preparation_window`
* `cooling_window`
* `dormancy_eligible`

### 7.2 Orchestration semantics

These fields answer questions like:

* Is this object alive enough to influence present attention?
* Is it warming, hot, cooling, or dormant?
* Does it require reconfirmation or preparation?
* Is it exerting pressure because other futures depend on it?

The orchestration profile does not decide civil manifestation or budget availability on its own.

---

## 8. Budget profile

The budget profile describes capability feasibility.

### 8.1 Budget fields

* `estimated_token_burn`
* `estimated_slice_count`
* `effort_class`
* `confidence_band`
* `context_pressure`
* `throughput_requirement`
* `expected_TPM_band`
* `project_budget_ref`
* `compression_potential`
* `re_estimation_trigger`
* `minimum_viable_slice`
* `reserve_sensitivity`
* `budget_heat`

### 8.2 Budget semantics

These fields answer questions like:

* What does this object likely cost?
* Is it feasible now?
* Does it require a lot of context or tool burn?
* Can it be compressed into a smaller lawful slice?
* Does it threaten reserves or require escalation?

The budget profile should be calibrated by receipts and actuals over time.

---

## 9. Lease profile

The lease profile describes current stewardship.

### 9.1 Lease fields

* `lease_id`
* `holder_type`
* `holder_ref`
* `lease_role`
* `lease_state`
* `lease_start`
* `lease_end`
* `renewal_conditions`
* `transfer_conditions`
* `revocation_conditions`
* `visibility_scope`
* `fallback_holder_ref`
* `prior_holder_ref`
* `successor_holder_ref`

### 9.2 Lease semantics

These fields answer questions like:

* Who is lawfully holding this object now?
* In what role?
* When does that stewardship begin and end?
* Who takes over if the current holder cools, fails, or transfers?

---

## 10. Reconciliation profile

The reconciliation profile describes how the three clocks are currently being reconciled.

### 10.1 Reconciliation fields

* `alignment_state`
* `reconciliation_posture`
* `wake_required`
* `reconfirm_required`
* `prepare_required`
* `compress_required`
* `defer_permitted`
* `escalation_required`
* `civil_manifestation_required`
* `lease_adjustment_required`
* `budget_warning_required`

### 10.2 Reconciliation semantics

These fields answer questions like:

* Are civil, orchestration, and budget time aligned?
* Is the object in normal flow, preparation, compression, deferment, or escalation?
* Does the system need to adjust lease posture or warn about budget tension?

---

## 11. Receipt profile

Temporal objects should carry or reference their own temporal receipts.

### 11.1 Receipt fields

* `prediction_receipts`
* `actual_execution_receipts`
* `heat_transition_receipts`
* `reconfirmation_receipts`
* `cooldown_receipts`
* `lease_transition_receipts`
* `budget_reconciliation_receipts`
* `escalation_receipts`

### 11.2 Receipt semantics

Receipts ensure the object’s temporal life is auditable.

The system should be able to answer:

* Why did this object become hot?
* Why did it cool?
* When was it reconfirmed?
* When did the holder change?
* Why did it get compressed or deferred?
* How wrong was the forecast?

---

## 12. Object relations

Temporal objects should not exist in isolation.

### 12.1 Relation types

Possible temporal relation types include:

* `DEPENDS_ON`
* `BLOCKED_BY`
* `SUPPORTS`
* `WARMS`
* `COOLS`
* `RESEEDS`
* `RECONFIRMS`
* `ESCALATES_TO`
* `COMPETES_WITH`
* `SHARES_BUDGET_WITH`
* `INHERITS_LEASE_FROM`

These relation types can later support graph reasoning over the temporal field.

---

## 13. Minimal canonical states

A minimal state vocabulary should be kept small at first.

### 13.1 Object lifecycle states

* `ACTIVE`
* `DEFERRED`
* `DORMANT`
* `COOLING`
* `ARCHIVED`
* `SUPERSEDED`
* `CANCELLED`

### 13.2 Heat states

* `FROZEN`
* `DORMANT`
* `COOL`
* `WARM`
* `HOT`
* `CRITICAL`
* `COOLING`
* `ARCHIVED`

### 13.3 Lease states

* `LATENT`
* `WARM`
* `ACTIVE`
* `REVIEW`
* `COOLING`
* `EXPIRED`
* `REVOKED`
* `TRANSFERRED`
* `ARCHIVED`

### 13.4 Reconciliation postures

* `PROCEED_NORMALLY`
* `WARM_ONLY`
* `RECONFIRM_FIRST`
* `PREPARE_ONLY`
* `COMPRESS`
* `DEFER_WITH_CONTINUITY`
* `ESCALATE`

---

## 14. Candidate minimal record skeleton

A first-pass canonical temporal object skeleton might look like:

```yaml
object_id: TOBJ_001
object_type: PLANNED_REPORT
title: Climate research report
description: Draft and submit climate report.
created_at: 2026-04-15T10:00:00Z
updated_at: 2026-04-15T12:00:00Z
origin_surface: USER_DIALOGUE
status: ACTIVE

civil:
  scheduled_at: 2026-05-12T10:00:00-04:00
  deadline_at: 2026-05-12T14:00:00-04:00
  timezone: America/Toronto
  recurrence_rule: null
  alarm_windows: [P1D, PT2H]
  calendar_visibility: visible
  real_world_commitment_strength: HIGH
  user_confirmation_required: true

orchestration:
  horizon_class: NEAR
  orchestration_heat: WARM
  composite_relevance: MEDIUM_HIGH
  wake_conditions: [DEADLINE_WINDOW_OPEN]
  cooldown_conditions: [COMPLETED, CANCELLED]
  dormancy_conditions: [DEFERRED_WITH_CONTINUITY]
  activation_readiness: LOW
  dependency_pressure: MEDIUM
  open_question_pressure: LOW
  reconfirmation_window: P1D
  preparation_window: PT3H
  cooling_window: P1D
  dormancy_eligible: true

budget:
  estimated_token_burn: 150000
  estimated_slice_count: 3
  effort_class: MEDIUM
  confidence_band: LOW_MEDIUM
  context_pressure: MEDIUM
  throughput_requirement: MODERATE
  expected_TPM_band: MEDIUM
  project_budget_ref: PROJ_ABC
  compression_potential: HIGH
  re_estimation_trigger: AFTER_INITIAL_RESEARCH
  minimum_viable_slice: OUTLINE_PLUS_KEY_FINDINGS
  reserve_sensitivity: MEDIUM
  budget_heat: LOW

lease:
  lease_id: LEASE_001
  holder_type: SUBSYSTEM
  holder_ref: PREPARATION_RUNTIME
  lease_role: PREPARER
  lease_state: WARM
  lease_start: 2026-05-11T10:00:00-04:00
  lease_end: 2026-05-12T14:00:00-04:00
  renewal_conditions: [RECONFIRMED]
  transfer_conditions: [ENACTMENT_READY]
  revocation_conditions: [CANCELLED]
  visibility_scope: LOCAL_PLUS_FALLBACK

reconciliation:
  alignment_state: CIVIL_LEADING
  reconciliation_posture: RECONFIRM_FIRST
  wake_required: true
  reconfirm_required: true
  prepare_required: false
  compress_required: false
  defer_permitted: true
  escalation_required: false
  civil_manifestation_required: true
  lease_adjustment_required: false
  budget_warning_required: false

receipts:
  prediction_receipts: []
  actual_execution_receipts: []
  heat_transition_receipts: []
  reconfirmation_receipts: []
  cooldown_receipts: []
  lease_transition_receipts: []
  budget_reconciliation_receipts: []
  escalation_receipts: []
```

This is only illustrative, but it provides a concrete shared structure.

---

## 15. Schema constraints

A lawful implementation should enforce several constraints.

### 15.1 Distinct profiles

Civil, orchestration, budget, lease, and reconciliation data must remain distinguishable.

### 15.2 No implicit collapsing

One profile must not silently overwrite another.

For example:

* a civil deadline must not become equivalent to orchestration heat,
* budget scarcity must not silently nullify commitment,
* lease ownership must not silently grant activation authority.

### 15.3 Lineage preservation

Recurring, superseding, cooling, or transferred objects must preserve lineage rather than appearing as unrelated duplicates.

### 15.4 Receiptable transitions

Heat changes, lease changes, reconciliation shifts, and recurrence reseeding should all be receipt-compatible.

---

## 16. Schema implementation strategy

### Phase 1

Adopt the schema as canonical vocabulary only.

### Phase 2

Map existing ION objects and records onto the schema without forcing total migration.

### Phase 3

Introduce dedicated temporal object records for future-facing commitments and workflows.

### Phase 4

Bind schema fields into protocol evaluators for temporal relevance, leases, and reconciliation.

### Phase 5

Use receipts and actuals to calibrate budget profile and recurrence behavior over time.

---

## 17. Failure modes

### 17.1 Flat task schema

If the temporal object is reduced to a normal task object with a due date, the whole temporal architecture collapses.

### 17.2 Overloaded schema

If too many concerns are fused too early, the schema becomes unreadable and ungovernable.

### 17.3 Hidden collapsing of profiles

If civil, orchestration, and budget fields are not explicitly separated, downstream logic will drift.

### 17.4 No lineage

Without lineage, recurrence, supersession, transfer, and cooling become lossy and ambiguous.

### 17.5 No receipts

Without receipt-compatible fields, the schema becomes stateful but not auditable.

---

## 18. Strongest present conclusion

The temporal protocol stack requires a shared object language.

`TEMPORAL_OBJECT_SCHEMA` is that shared language.

Its purpose is to ensure that:

* temporal relevance,
* temporal leases,
* and triple-time reconciliation

all reason over the same lawful object rather than three disconnected abstractions.

This schema should therefore be treated as the backbone of the temporal development effort, even before final implementation details are chosen.
