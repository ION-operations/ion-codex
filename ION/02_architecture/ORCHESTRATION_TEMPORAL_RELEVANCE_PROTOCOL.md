# ORCHESTRATION_TEMPORAL_RELEVANCE_PROTOCOL Draft

## 0. Status

Draft protocol for ION temporal development.

This is a proposed first unifying protocol. Its purpose is not to replace scheduler law, horizon law, route-state law, automation law, or civil calendar logic. Its purpose is to give those systems a common lawful language for temporal relevance.

---

## 1. Purpose

ION requires a protocol that defines when any object is temporally alive enough to influence the present.

The present protocol governs:

* when an object is considered temporally relevant,
* how that relevance is derived,
* how relevance transitions occur,
* how temporal relevance differs from civil schedule and budget feasibility,
* and how existing ION subsystems contribute to a unified temporal field.

This protocol is necessary because ION already has meaningful temporal machinery distributed across horizon, scheduler, route-state, automation posture, continuation, lifecycle, and readiness surfaces. What is missing is a common law that says how these pieces combine into current relevance.

---

## 2. Non-goals

This protocol does **not** define:

* civil calendar semantics,
* alarms or reminder delivery,
* exact deadline management,
* budget allocation policy,
* token accounting,
* project finance,
* full activation authority,
* or full scheduler implementation.

Those surfaces may influence temporal relevance, but they are not replaced by this protocol.

This protocol also does not attempt to define the whole triple-time bridge at once. It defines the orchestration-time center first.

---

## 3. Core thesis

Temporal relevance is not the same thing as:

* having a date,
* having a deadline,
* being present in the scheduler,
* existing in memory,
* being in a plan,
* or being semantically important.

An object is temporally relevant when it lawfully exerts enough force on present orchestration to justify occupying active attention, influencing context compilation, or triggering preparatory or enactment behavior.

Temporal relevance is therefore a derived lawful state.

---

## 4. Governing formulation

For any temporal-bearing object, ION should compute an orchestration temporal profile that expresses:

* whether the object is alive enough to matter now,
* how intensely it matters,
* whether it should warm, stay active, cool, or become dormant,
* whether reconfirmation or preparation is required,
* and whether it is entitled to hold context or lease attention.

This profile should be computed from lawful inputs rather than by arbitrary intuition.

---

## 5. Canonical concepts

### 5.1 Temporal-bearing object

A temporal-bearing object is any object whose relevance unfolds over time.

Examples include:

* future commitments
* reports
* routines
* reviews
* pending branch work
* unresolved dependency clusters
* recurring checkups
* deferred missions
* future activations
* dormant but not archived obligations

### 5.2 Orchestration temporal profile

The orchestration temporal profile is the object’s internal relevance state within ION.

It is distinct from:

* civil time profile
* budget or endurance profile

### 5.3 Relevance heat

Relevance heat is a derived signal expressing how strongly an object currently exerts pressure on present orchestration.

### 5.4 Wake condition

A wake condition is any lawful condition under which an object moves from cooler or dormant posture into warmer active posture.

### 5.5 Cooling condition

A cooling condition is any lawful condition under which an object reduces relevance or leaves active attention.

### 5.6 Dormancy

Dormancy is a lawful state in which an object is neither dead nor active. It remains expected to reawaken under valid conditions.

### 5.7 Reconfirmation window

A reconfirmation window is a temporal stage in which the system must verify whether an object should continue toward enactment or remain active.

### 5.8 Preparation window

A preparation window is the temporal stage in which the system gathers context, dependencies, or materials before enactment.

### 5.9 Temporal lease

A temporal lease is the lawful assignment of present attention responsibility for a temporal-bearing object to an agent, branch, subsystem, or user-facing runtime.

---

## 6. Temporal relevance is not activation authority

A key boundary must be enforced.

An object may be highly relevant without being enactable.

Temporal relevance may justify:

* entering active context,
* warming a future branch,
* beginning preparation,
* requiring reconfirmation,
* assigning a temporal lease,
* or triggering context preload.

Temporal relevance does **not** by itself authorize enactment crossing.

Activation authority remains a separate protocol surface.

---

## 7. Inputs to temporal relevance

Temporal relevance should be computed from a bounded set of lawful inputs.

### 7.1 Horizon inputs

* near / mid / far horizon classification
* horizon tightening or widening
* relation to already active horizon work

### 7.2 Scheduler inputs

* commitment gradient
* schedule state
* future candidate or deferred posture
* blocked or stale posture

### 7.3 Route-state inputs

* branch activation conditions
* branch readiness
* route occupancy or route inheritance
* supersession and archival relations

### 7.4 Dependency inputs

* dependency count
* dependency criticality
* whether other objects are waiting on this object
* whether a blocker changed

### 7.5 Open-question inputs

* unresolved question count
* unresolved question severity
* contradiction pressure
* uncertainty that threatens enactment

### 7.6 Civil-time inputs

* deadline proximity
* recurrence imminence
* scheduled civil event proximity
* reconfirmation due against real-world commitments

### 7.7 Budget inputs

* current resource posture
* available budget envelope
* current throughput posture
* whether the object is feasible, compressible, or likely to be deferred

### 7.8 User and history inputs

* user reaffirmation or change
* historical slippage risk
* historical failure rate for similar objects
* archival lineage and prior attempts

### 7.9 Lease inputs

* whether the object is already under active lease
* whether a lease has lapsed
* whether a holder transfer is pending

---

## 8. Outputs of temporal relevance computation

A first-pass relevance computation may yield:

* `civil_heat`
* `orchestration_heat`
* `budget_heat`
* `composite_relevance`
* `wake_required`
* `reconfirm_required`
* `prepare_required`
* `cooling_permitted`
* `dormant_eligible`
* `lease_recommended`

This protocol is primarily concerned with orchestration heat and composite relevance, but it should remain capable of interacting with the other two heat dimensions.

---

## 9. Relevance states

A useful generalized progression is:

* FROZEN
* DORMANT
* COOL
* WARM
* HOT
* CRITICAL
* COOLING
* ARCHIVED

### 9.1 FROZEN

Known to the system but not currently entitled to active influence.

### 9.2 DORMANT

Expected to matter again but not yet warm.

### 9.3 COOL

Relevant enough to remain lawful memory, but not active enough to shape present compilation strongly.

### 9.4 WARM

Should begin influencing attention, preload, or lease assignment.

### 9.5 HOT

Actively shaping current context and requiring present orchestration awareness.

### 9.6 CRITICAL

High-pressure present relevance requiring near-immediate attention, reconfirmation, preparation, or escalation.

### 9.7 COOLING

No longer hot, but still transitioning out of active posture.

### 9.8 ARCHIVED

Preserved for history and lineage, no longer expected to reawaken under current assumptions.

---

## 10. Heat derivation

Heat must be derived, not declared arbitrarily.

### 10.1 Possible derivation factors

* deadline distance
* schedule commitment strength
* dependency fan-in or fan-out
* blocker severity
* recurrence proximity
* open-question pressure
* user commitment strength
* prior failure/slippage tendency
* budget feasibility posture
* whether the object already failed reconfirmation
* whether another hot object depends on it

### 10.2 Heat vector model

The protocol should prefer a multi-axis model over a single scalar.

At minimum:

* civil heat
* orchestration heat
* budget heat

The protocol may still expose a composite field for convenience, but the underlying vector should remain recoverable.

---

## 11. Temporal state transitions

Transitions should be receipted and auditable.

### 11.1 Canonical transitions

* FROZEN → DORMANT
* DORMANT → COOL
* COOL → WARM
* WARM → HOT
* HOT → CRITICAL
* CRITICAL → COOLING
* COOLING → DORMANT
* COOLING → ARCHIVED

### 11.2 Example wake transitions

A dormant object may move to warm if:

* a civil deadline enters a threshold window,
* a blocked dependency clears,
* a recurrence window opens,
* a user reaffirms the object,
* or another object that depends on it becomes critical.

### 11.3 Example cooling transitions

An object may cool if:

* the work is completed,
* the object is superseded,
* the civil commitment is cancelled,
* reconfirmation fails,
* or budget posture temporarily makes enactment impossible and the object must return to dormant monitoring.

---

## 12. Reconfirmation and preparation hooks

Temporal relevance should explicitly call for reconfirmation or preparation when needed.

### 12.1 Reconfirmation required

Reconfirmation should become true when:

* a previously declared future commitment is approaching enactment,
* circumstances may have changed,
* a civil event is near but alignment is uncertain,
* or an object has stayed warm/hot for too long without fresh validation.

### 12.2 Preparation required

Preparation should become true when:

* enactment is near,
* context preload is needed,
* dependencies should be checked,
* budget should be reconfirmed,
* or preparatory materials should be assembled.

These outputs should not enact work automatically. They should open the next lawful protocol stage.

---

## 13. Temporal leases

This protocol should interact closely with lease logic.

### 13.1 Relevance and lease relationship

An object that is warm or hot may justify lease assignment.

An object that is cooling may justify lease downgrading.

An object that becomes dormant may justify lease expiration or fallback stewardship.

### 13.2 Lease recommendation

The relevance engine should be able to recommend:

* whether a lease is needed,
* which holder type is appropriate,
* whether the lease should be owner/reviewer/watcher/fallback,
* and when a lease should expire or transfer.

---

## 14. Relation to civil time

Civil time is not replaced by this protocol.

Civil time contributes lawful inputs such as:

* deadlines,
* schedule windows,
* recurrence,
* timezone-aware event timing,
* and real-world commitments.

But civil time alone does not define orchestration temporal relevance.

A civil event may exist on the calendar while still being cool or dormant in orchestration time.
A civilly distant object may become hot in orchestration time because a dependency or blocker shifted.

This protocol therefore consumes civil inputs without becoming equivalent to the civil calendar.

---

## 15. Relation to budget time

Budget or endurance posture also does not replace temporal relevance.

Budget posture may:

* suppress false criticality,
* force compression or deferment,
* increase risk pressure,
* or change whether preparation is lawful right now.

But budget scarcity does not erase civil commitments or orchestration history.

This protocol therefore consumes budget inputs without becoming a pure resource allocator.

---

## 16. Relation to existing ION systems

This protocol must bind to, not replace, the following existing centers:

* scheduler law
* horizon law
* route-state logic
* automation progression
* continuation and replay
* activation authority
* runtime/session systems
* signals and receipt systems

This protocol should be a unifying law over those surfaces, not a competing controller.

---

## 17. Minimal compliance requirements

A compliant implementation of this protocol must:

* compute temporal relevance from explicit lawful inputs,
* preserve distinction from civil time and budget time,
* expose heat states and state transitions,
* produce receiptable transitions or transition-ready events,
* support wake/reconfirmation/preparation/cooling outputs,
* remain compatible with temporal leases,
* and avoid silently authorizing enactment.

---

## 18. Failure modes

### 18.1 Magical heat

Heat becomes aesthetic and untrustworthy if not derived from lawful fields.

### 18.2 Scheduler duplication

If this protocol begins to schedule work directly, it duplicates scheduler law.

### 18.3 Calendar duplication

If civil deadlines become the only determinant of relevance, civil time swallows orchestration time.

### 18.4 Budget domination

If resource posture alone suppresses relevance, the system becomes opportunistic and loses duty.

### 18.5 No cooling

Without cooling, all objects accumulate as semi-hot forever.

### 18.6 No receipts

Without receipts or auditable state transitions, temporal relevance becomes opaque and untrustworthy.

---

## 19. Candidate data model

A first-pass orchestration temporal record might include:

* `object_id`
* `object_type`
* `orchestration_heat`
* `civil_heat`
* `budget_heat`
* `composite_relevance`
* `last_transition`
* `wake_required`
* `reconfirm_required`
* `prepare_required`
* `cooling_permitted`
* `dormant_eligible`
* `lease_recommended`
* `input_summary`
* `receipt_ref`

This is only a sketch and must be aligned with broader object law later.

---

## 20. Minimal first algorithm

A conservative initial algorithm should:

1. ingest lawful input signals,
2. compute heat dimensions independently,
3. derive a composite relevance class,
4. determine whether a transition is required,
5. determine whether reconfirmation or preparation hooks should fire,
6. determine whether lease recommendation should be emitted,
7. emit receipts or transition events.

This should begin as a transparent rule-based pass before any deeper learned weighting is trusted.

---

## 21. Recommended implementation path

### Phase 1

Introduce orchestration temporal profile fields and a conservative rule-based evaluator.

### Phase 2

Bind the evaluator to scheduler, route-state, and automation surfaces.

### Phase 3

Add receipts for heat transitions and reconfirmation triggers.

### Phase 4

Introduce lease recommendations and preparation hooks.

### Phase 5

Bridge to civil and budget time through the triple-time reconciliation layer.

---

## 22. Strongest present conclusion

The first correct temporal protocol for ION is not a calendar protocol and not a budget protocol.

It is the protocol that defines what it means for anything to be temporally alive enough to matter now.

That is the purpose of `ORCHESTRATION_TEMPORAL_RELEVANCE_PROTOCOL`.

It should become the common lawful language through which existing horizon, scheduler, route-state, automation, civil, and budget surfaces begin to converge without being collapsed into one another.
