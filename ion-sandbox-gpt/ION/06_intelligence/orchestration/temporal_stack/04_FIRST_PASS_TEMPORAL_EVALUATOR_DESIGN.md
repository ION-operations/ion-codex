# First Pass Temporal Evaluator Design

## 0. Purpose

This document defines a first-pass evaluator for the emerging temporal stack.

The goal is not full autonomy and not a universal engine for every ION object. The goal is a narrow, conservative, rule-based evaluator that can operate over a small initial family of temporal-bearing objects and produce auditable recommendations.

The evaluator should combine:

* orchestration temporal relevance,
* temporal lease recommendation,
* and triple-time reconciliation posture,

without collapsing them into one opaque score.

---

## 1. Scope of the first evaluator

The evaluator should only operate over a limited initial object family.

### 1.1 Initial supported object classes

The first supported classes should likely be:

* scheduled deliverables
* recurring reviews
* dormant future commitments

These classes are strong starting points because they are:

* clearly future-bearing,
* rich in civil/orchestration/budget interaction,
* user-meaningful,
* and likely to reveal contradictions quickly.

### 1.2 Explicitly out of scope for v1

The evaluator should not initially handle:

* all memory atoms,
* all runtime/session records,
* all branch objects,
* all activation candidates,
* or every budget checkpoint in the system.

It should remain narrow until its receipts and recommendations are trustworthy.

---

## 2. Evaluator goals

The evaluator should answer three distinct questions for each object.

### 2.1 Relevance question

How alive is this object in orchestration time right now?

### 2.2 Stewardship question

Who, if anyone, should currently hold bounded responsibility for this object?

### 2.3 Reconciliation question

Given civil time, orchestration time, and budget time, what is the lawful present posture?

These questions should remain distinguishable in the output.

---

## 3. Evaluator philosophy

The first evaluator should be:

* conservative,
* rule-based,
* transparent,
* receiptable,
* bounded,
* and easy to override.

It should prefer:

* recommendation over silent control,
* receipts over invisible state mutation,
* and the smallest lawful next move over large autonomous leaps.

The evaluator is not yet the operating intelligence itself. It is the first lawful temporal interpreter.

---

## 4. Required inputs

The evaluator operates over one temporal object plus contextual signals.

### 4.1 Object input

A temporal object conforming, at least conceptually, to the `TEMPORAL_OBJECT_SCHEMA`.

It should expose at minimum:

* identity
* civil profile
* orchestration profile
* budget profile
* status
* lineage references

### 4.2 Global contextual inputs

The evaluator may also consume:

* current time in user timezone
* current resource posture
* current reserve posture
* active competing hot objects
* recurrence history
* prior estimate receipts
* current blocker changes
* recent user reconfirmations or changes

### 4.3 Optional environmental signals

For later phases, it may also use:

* calendar changes
* branch readiness changes
* route-state updates
* automation posture changes
* tool availability changes

The first evaluator should keep these optional so it does not overbind too early.

---

## 5. Core outputs

The evaluator should return a structured result rather than one scalar judgment.

### 5.1 Relevance outputs

* `civil_heat`
* `orchestration_heat`
* `budget_heat`
* `composite_relevance`
* `wake_required`
* `reconfirm_required`
* `prepare_required`
* `cooling_permitted`
* `dormant_eligible`

### 5.2 Lease outputs

* `lease_required`
* `lease_role`
* `holder_type`
* `holder_ref`
* `lease_state`
* `transfer_required`
* `downgrade_required`
* `expiration_permitted`

### 5.3 Reconciliation outputs

* `alignment_state`
* `reconciliation_posture`
* `compress_required`
* `defer_permitted`
* `escalation_required`
* `civil_manifestation_required`
* `lease_adjustment_required`
* `budget_warning_required`

### 5.4 Audit outputs

* `input_summary`
* `decision_summary`
* `triggered_rules`
* `confidence_level`
* `receipt_required`

These are needed so the evaluator remains inspectable.

---

## 6. Minimal heat model

The first evaluator should use a simple, explicit, bounded heat model.

### 6.1 Civil heat

Derived from:

* deadline distance
* scheduled time proximity
* recurrence imminence
* alarm windows

Example rough categories:

* LOW
* MEDIUM
* HIGH
* CRITICAL

### 6.2 Orchestration heat

Derived from:

* dependency pressure
* blocker changes
* horizon class
* reconfirmation need
* preparation need
* whether the object is already under lease
* whether related objects are hot

### 6.3 Budget heat

Derived from:

* expected burn vs available reserve
* throughput sufficiency
* compression potential
* current resource posture
* forecast confidence

Budget heat should be interpreted carefully.
A high budget heat means resource tension, not importance.

### 6.4 Composite relevance

Composite relevance should be derived, not dominant.

It should summarize the relationship, but never erase the three underlying heats.

---

## 7. Rule families

The evaluator should probably be built from explicit rule families.

### 7.1 Civil rules

Examples:

* If deadline is within 24 hours, civil heat cannot remain LOW.
* If recurrence window is open, wake_required becomes eligible.
* If scheduled time is near and user confirmation is required, reconfirm_required becomes likely.

### 7.2 Orchestration rules

Examples:

* If a blocker clears and dependencies are waiting, orchestration heat rises.
* If the object was dormant and a wake condition fires, dormancy ends.
* If preparation window opens, prepare_required becomes true.

### 7.3 Budget rules

Examples:

* If reserve is constrained and expected burn is high, budget_warning_required becomes true.
* If compression potential is high and civil heat is high, compression becomes eligible.
* If resource posture is emergency_only, escalation or deferment becomes more likely.

### 7.4 Lease rules

Examples:

* If composite relevance rises above threshold, a lease may be required.
* If reconfirm_required is true, reviewer or reconfirmation steward lease is preferred.
* If prepare_required is true, preparer lease becomes a candidate.
* If object cools, downgrade or expiry becomes eligible.

### 7.5 Reconciliation rules

Examples:

* High civil heat + high orchestration heat + sufficient budget → `PROCEED_NORMALLY` or `PREPARE_ONLY`
* High civil heat + high orchestration heat + constrained budget → `COMPRESS` or `ESCALATE`
* Low civil heat + high orchestration heat + moderate budget → `WARM_ONLY` or bounded preparation
* High civil heat + low orchestration heat → `RECONFIRM_FIRST`

---

## 8. Initial object-class policies

The first evaluator should not treat all supported object classes identically.

### 8.1 Scheduled deliverables

These are likely to be strongly civil-driven.

Default tendencies:

* civil deadlines should matter strongly,
* reconfirmation should occur before enactment when appropriate,
* compression may be valid under budget constraint,
* cooling should follow fulfillment or postponement.

### 8.2 Recurring reviews

These are likely to emphasize recurrence, reseeding, and chronic slippage patterns.

Default tendencies:

* should warm in cycles,
* should cool and reseed lawfully,
* repeated skips should raise orchestration pressure or reconfirmation need,
* a dormant steward lease may hold them between active windows.

### 8.3 Dormant future commitments

These are likely to be more orchestration-sensitive than civilly urgent.

Default tendencies:

* wake conditions matter strongly,
* dependency changes may dominate,
* civil time may be distant,
* watcher or dormant steward leases may be the default posture.

---

## 9. Candidate evaluator pipeline

A minimal first-pass evaluation pipeline could be:

### Step 1 — Normalize object

Read the temporal object and coerce required fields into a normalized in-memory form.

### Step 2 — Compute heat vector

Compute:

* civil heat
* orchestration heat
* budget heat

### Step 3 — Compute transitions

Determine:

* wake_required
* reconfirm_required
* prepare_required
* cooling_permitted
* dormant_eligible

### Step 4 — Compute lease recommendation

Choose whether a lease is needed and what role/state it should likely have.

### Step 5 — Compute reconciliation posture

Determine whether to:

* proceed normally,
* warm only,
* reconfirm first,
* prepare only,
* compress,
* defer with continuity,
* or escalate.

### Step 6 — Build audit record

Produce:

* a rule trace,
* a human-readable decision summary,
* and receipt-ready transition notes.

---

## 10. Recommendation, not action

The first evaluator should output recommendations, not immediately mutate the world.

Examples of recommendation outputs:

* recommend warm transition
* recommend reconfirmation message
* recommend preparer lease
* recommend compression posture
* recommend escalation
* recommend civil manifestation

Other layers may consume those recommendations and decide whether to act.

This is important for trust and auditability.

---

## 11. Receipt strategy

The evaluator should probably emit two kinds of record.

### 11.1 Evaluation receipt

This states:

* the object evaluated,
* the input summary,
* the heat vector,
* the selected posture,
* the triggered rules,
* and the confidence level.

### 11.2 Transition recommendation receipt

This states:

* whether wake/reconfirm/prepare/cool/lease/reconcile actions were recommended,
* and why.

This allows later comparison between recommendations and actual enacted transitions.

---

## 12. Confidence and uncertainty

The evaluator should expose uncertainty explicitly.

### 12.1 Confidence sources

Confidence may depend on:

* completeness of object fields,
* quality of recurrence history,
* quality of estimate receipts,
* certainty of budget posture,
* certainty of civil profile,
* certainty of dependency state.

### 12.2 Low-confidence behavior

When confidence is low, the evaluator should prefer:

* reconfirmation,
* conservative warmup,
* smaller preparation moves,
* and escalation over overcommitment.

---

## 13. Example outputs by class

### 13.1 Scheduled deliverable near deadline

Possible output:

* civil_heat: HIGH
* orchestration_heat: MEDIUM_HIGH
* budget_heat: MEDIUM
* composite_relevance: HIGH
* reconfirm_required: true
* prepare_required: true
* lease_required: true
* lease_role: PREPARER
* reconciliation_posture: RECONFIRM_FIRST

### 13.2 Recurring review one day before recurrence

Possible output:

* civil_heat: MEDIUM
* orchestration_heat: WARM
* budget_heat: LOW
* wake_required: true
* lease_required: true
* lease_role: WATCHER or PREPARER
* reconciliation_posture: WARM_ONLY

### 13.3 Dormant future commitment with blocker just cleared

Possible output:

* civil_heat: LOW
* orchestration_heat: HIGH
* budget_heat: MEDIUM
* wake_required: true
* lease_required: true
* lease_role: WATCHER
* prepare_required: maybe
* reconciliation_posture: WARM_ONLY or PREPARE_ONLY

---

## 14. Minimal data structures

A first implementation likely needs at least:

* `TemporalEvaluationInput`
* `TemporalHeatVector`
* `TemporalLeaseRecommendation`
* `TemporalReconciliationRecommendation`
* `TemporalEvaluationResult`
* `TemporalEvaluationReceipt`

This keeps the engine structured and auditable.

---

## 15. Failure modes

### 15.1 Score collapse

The evaluator reduces everything to one urgency number and loses the three-clock distinction.

### 15.2 Hidden action

The evaluator mutates world state directly instead of making recommendation and receipt outputs.

### 15.3 Overreach

The evaluator tries to govern every object family immediately.

### 15.4 Under-specification

The evaluator does not explain why a recommendation occurred.

### 15.5 No override path

The evaluator behaves as though its recommendation is unquestionable.

---

## 16. Recommended implementation order

### Phase 1

Implement a paper design and example records only.

### Phase 2

Implement a rule-based evaluator over one object class.

### Phase 3

Add receipts and recommendation logging.

### Phase 4

Expand to the other two initial object classes.

### Phase 5

Bind recommendations to a runtime or orchestration surface that may choose to act.

---

## 17. Strongest present conclusion

The first-pass evaluator should not be ambitious in scope.
It should be ambitious in clarity.

Its first job is to prove that the temporal stack can produce:

* interpretable heat,
* bounded stewardship recommendations,
* and lawful reconciliation posture,

for a narrow class of future-bearing objects.

If that works, the temporal stack can begin moving from protocol theory into executable architecture.
