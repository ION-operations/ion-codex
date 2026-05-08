# Temporal Worked Scenarios for ION

## 0. Purpose

This document pressure-tests the emerging temporal stack against realistic scenarios.

The goal is not merely to illustrate the protocols. The goal is to expose hidden contradictions, redundancies, missing receipts, weak boundaries, and any places where the theory fails under actual use.

These scenarios are written against the emerging stack:

* `ORCHESTRATION_TEMPORAL_RELEVANCE_PROTOCOL`
* `TEMPORAL_CONTEXT_LEASE_PROTOCOL`
* `TRIPLE_TIME_RECONCILIATION_PROTOCOL`
* `TEMPORAL_OBJECT_SCHEMA`

Each scenario should show how civil time, orchestration time, and budget time interact without collapsing into one another.

---

## 1. Scenario method

Each scenario is written through the same skeleton:

1. object introduced
2. civil profile assigned
3. orchestration profile assigned
4. budget profile assigned
5. initial heat computation
6. lease assignment
7. wake/reconfirmation/preparation behavior
8. enactment or non-enactment decision
9. cooling / dormancy / recurrence outcome
10. receipts and lessons

This keeps the scenarios comparable.

---

## 2. Scenario A — scientific report due tomorrow

### 2.1 Introduction

The user told ION three weeks ago:

> On May 12 at 10:00 AM I need to do the scientific report.

The user is now in dialogue with the AI on May 11.

The report still exists as a temporal object.

### 2.2 Civil profile

* scheduled_at: May 12, 10:00 AM
* timezone: America/Toronto
* alarm windows: T-24h, T-2h
* calendar visibility: visible
* commitment strength: high

Civilly, the object is now near urgent.

### 2.3 Orchestration profile

* horizon_class: near
* orchestration heat: warm moving toward hot
* reconfirmation window: now open
* preparation window: T-3h to T-1h
* dependency pressure: medium
* open question pressure: medium
* wake required: yes

The object is not yet in full enactment posture, but it is clearly alive enough to influence the present.

### 2.4 Budget profile

* estimated slice count: 2–3
* budget heat: moderate
* compression potential: high
* re-estimation trigger: after checking whether source materials already exist
* reserve sensitivity: medium

The object is feasible, but only if the system does not assume a deep research campaign from scratch.

### 2.5 Initial heat computation

* civil heat: high
* orchestration heat: medium-high
* budget heat: moderate
* composite relevance: high

The object is not yet critical, but it is fully alive in present attention.

### 2.6 Lease assignment

A preparer or reviewer lease should be assigned now.

For example:

* holder_type: user-facing runtime
* lease_role: reconfirmation steward
* lease_state: active
* fallback holder: preparation runtime

This means the object is now lawfully owned for present-time stewardship.

### 2.7 Reconfirmation behavior

ION should not jump directly to “let’s do the report now.”

It should ask something like:

* Is the report still happening tomorrow?
* Has the scope changed?
* Do you already have the source materials?
* Do you want a compressed version or full version?

This is a lawful reconfirmation stage, not hesitation.

### 2.8 Preparation behavior

If reconfirmed, the system should then:

* check whether relevant files and research notes already exist,
* preload context,
* estimate budget posture more accurately,
* determine whether a compressed or full slice is realistic.

### 2.9 Enactment decision

If the user confirms alignment and the budget profile remains feasible, the system can move toward enactment preparation.

If the budget is tighter than expected, it may offer compression:

* executive summary version first,
* full version later.

### 2.10 Cooling outcome

After completion, the object cools.

Possible states:

* resolved_hot immediately after completion,
* cooling within hours,
* archived the next day,
* or recurring_seed if this is a weekly or monthly report.

### 2.11 Receipts and lessons

Receipts should exist for:

* warm transition,
* reconfirmation,
* preparation start,
* enacted or compressed fulfillment,
* cooling transition,
* actual budget burn versus forecast.

The key lesson of this scenario is that the object should not behave like a dumb reminder. It should behave like a living future commitment entering lawful present stewardship.

---

## 3. Scenario B — recurring weekly review

### 3.1 Introduction

The user has a weekly review every Friday at 4:00 PM.

This is not a one-off object. It is recurring and reseeded.

### 3.2 Civil profile

* recurrence_rule: weekly, Friday 4:00 PM
* timezone: America/Toronto
* alarm windows: T-24h, T-1h
* visibility: visible

### 3.3 Orchestration profile

The current cycle of the weekly review is dormant for most of the week, warming on Thursday, hot on Friday, then cooling and reseeding.

### 3.4 Budget profile

* expected slice count: 1
* budget heat: low to moderate
* compression potential: medium
* reserve sensitivity: low

This should normally be feasible, but may still need compression under scarcity.

### 3.5 Heat progression

* Saturday to Wednesday: dormant
* Thursday: warm
* Friday morning: hot
* Friday afternoon: critical
* post-review: cooling
* then: recurring_seed

### 3.6 Lease assignment

A dormant steward may hold it during the week.
A preparer or owner lease may activate on Thursday/Friday.

### 3.7 Reconfirmation

Some recurring objects may not require full reconfirmation every cycle.

But the system may still check:

* Is the weekly review still happening this week?
* Are there any unusual agenda items?

### 3.8 Enactment and completion

After the review happens, this cycle cools and archives.
A new seed object is created for next week, linked by lineage.

### 3.9 Lessons

Recurrence must not be modeled as one immortal task that never cools.
Each cycle needs lawful reseeding with preserved lineage.

---

## 4. Scenario C — timezone shift without identity corruption

### 4.1 Introduction

The user has a meeting on May 20 at 2:00 PM Toronto time.
Before the meeting, the user travels to Vancouver.

### 4.2 Civil profile

The civil manifestation changes because the timezone context changes.

The object may now need to show:

* original meeting time in Toronto
* equivalent current local time in Vancouver

### 4.3 Orchestration profile

The object’s orchestration identity should not be destroyed merely because timezone interpretation changes.

Its warming, reconfirmation, preparation, and meeting-support logic remain the same object.

### 4.4 Budget profile

Likely low to moderate.
This scenario is not mainly budget-sensitive.

### 4.5 Key reconciliation issue

Civil time changes representation.
Orchestration time should preserve identity.

The bridge must therefore update civil manifestation without turning this into a new unrelated object.

### 4.6 Lease effect

Any active lease remains attached to the same object.
It may receive updated civil timing context, but it is not reset from scratch.

### 4.7 Lessons

Timezone shifts are a good test of whether civil time and orchestration time have been wrongly collapsed.

If the object loses identity or gets duplicated, the architecture is wrong.

---

## 5. Scenario D — civil urgency with severe budget constraint

### 5.1 Introduction

The user has a deliverable due tonight.
But the current AI budget is heavily constrained.

### 5.2 Civil profile

* deadline: tonight
* civil heat: critical

### 5.3 Orchestration profile

The object is also hot or critical because it is near enactment and not yet done.

### 5.4 Budget profile

* very low remaining reserve
* low sustained throughput
* compression potential: high
* escalation threshold: near

### 5.5 Reconciliation posture

This is likely a **budget-leading tension** or even **triple tension** state.

The correct answer is not:

* pretend the full work can still be done,
* or ignore the deadline.

The correct answer is likely:

* compress,
* reconfirm expectations if necessary,
* or escalate.

### 5.6 Lease effect

The object should stay actively leased, but the role may shift toward:

* compression steward,
* escalation steward,
* or fallback owner.

### 5.7 Lawful output

A lawful system might say:

* the full version is not feasible under current budget,
* but a smaller valid slice can be produced now,
* and a deeper version can follow later if still needed.

### 5.8 Lessons

Budget scarcity must not silently erase duty.
It must force explicit compression or escalation.

---

## 6. Scenario E — orchestration-hot, civilly distant

### 6.1 Introduction

A branch of work is not due for another month.
But suddenly a dependency is cleared, and several near-future branches now depend on it.

### 6.2 Civil profile

Civil heat is still low.
No immediate deadline.

### 6.3 Orchestration profile

Orchestration heat becomes high because dependency pressure changed.

### 6.4 Budget profile

Moderate feasibility.
This work could be usefully advanced now.

### 6.5 Reconciliation posture

This is an **orchestration-leading** case.

The correct system behavior is not to ignore it just because the civil deadline is far away.
It should likely:

* warm the object,
* assign a watcher or preparer lease,
* and potentially begin bounded preparatory work.

### 6.6 Lessons

This proves why orchestration time must remain distinct from civil calendar logic.

---

## 7. Scenario F — dormant commitment awakened by blocker change

### 7.1 Introduction

A future commitment was dormant because a blocker made it impossible.
Now the blocker clears.

### 7.2 Civil profile

The object may still be far from deadline.
Civil heat remains low or moderate.

### 7.3 Orchestration profile

The blocker clearance acts as a wake condition.
The object should move from dormant to warm or hot depending on downstream pressure.

### 7.4 Budget profile

If feasible, preparation or partial activation may begin.

### 7.5 Lease effect

A dormant steward lease may expire and transfer to a watcher or preparer lease.

### 7.6 Lessons

This scenario shows why wake conditions must include more than clock-time triggers.
Dependency change itself can wake a future object.

---

## 8. Scenario G — budget surge and reserve drawdown

### 8.1 Introduction

Several high-priority commitments converge within a short civil window.
The system must enter surge mode.

### 8.2 Civil profile

Multiple objects are civilly hot.

### 8.3 Orchestration profile

The orchestration field becomes crowded and high-pressure.

### 8.4 Budget profile

The system may choose or be authorized to draw from reserve and temporarily tolerate higher burn.

### 8.5 Reconciliation posture

This is not ordinary execution.
This is a surge condition.

Possible lawful outputs:

* limited reserve drawdown,
* reduced exploratory branching,
* aggressive compression on lower-priority objects,
* explicit escalation receipts.

### 8.6 Lessons

Resource posture needs its own doctrine because it materially changes what behavior is lawful.

---

## 9. Scenario H — user changes commitment after warming began

### 9.1 Introduction

A report was warming and already under preparation lease.
The user then says the report is postponed by two weeks.

### 9.2 Civil profile

The deadline shifts.
Civil heat drops.

### 9.3 Orchestration profile

Preparation may now be premature.
The object should likely cool from warm/hot toward cool or dormant.

### 9.4 Budget profile

Resources previously allocated may be released or reassigned.

### 9.5 Lease effect

A preparer lease may cool or transfer to dormant stewardship.

### 9.6 Lessons

This scenario tests whether the system can cool gracefully without losing lineage or continuity.

---

## 10. Scenario I — recurring object under chronic noncompletion

### 10.1 Introduction

A weekly review has been skipped three weeks in a row.

### 10.2 Civil profile

The civil recurrence continues.

### 10.3 Orchestration profile

The recurrence may now carry slippage pressure or unresolved pattern pressure.

### 10.4 Budget profile

The cost per cycle may be small, but the pattern of noncompletion is meaningful.

### 10.5 Reconciliation effect

The system may need to stop treating the object as normal recurrence and instead escalate:

* Is the recurrence still valid?
* Is the timing wrong?
* Does the user want a different cadence?

### 10.6 Lessons

Repeated recurrence failure should become part of the object’s temporal intelligence.

---

## 11. Scenario J — low-civil, low-budget, but identity-critical object

### 11.1 Introduction

A constitutional or architectural correction is not civilly urgent and may not be immediately feasible, but it is identity-critical for the system.

### 11.2 Civil profile

Low or absent.

### 11.3 Orchestration profile

Potentially warm because of strategic importance.

### 11.4 Budget profile

Possibly low-feasibility right now.

### 11.5 Reconciliation posture

The object may justify continued watcher or fallback lease even if no active work occurs.

### 11.6 Lessons

Not all important future objects are user-calendar objects. Some are deeply internal and still require lawful temporal stewardship.

---

## 12. Cross-scenario observations

These scenarios reveal several recurring truths.

### 12.1 Civil time is necessary but insufficient

Many important future objects would be mismanaged if they were treated as calendar events alone.

### 12.2 Orchestration wake conditions are broader than deadlines

Dependency changes, blocker removal, slippage history, and recurrence failure all matter.

### 12.3 Budget posture changes lawful behavior, not object existence

Scarcity may justify compression, deferment, or escalation.
It should not erase object identity or commitment lineage.

### 12.4 Lease logic is indispensable

Without leases, the system cannot manage who is responsible for warming, preparation, reconfirmation, or dormant stewardship.

### 12.5 Cooling and recurrence must preserve lineage

The object should remain historically coherent across cycles, postponements, or compression events.

---

## 13. What these scenarios suggest is still missing

The scenario set reinforces that the strongest remaining implementation needs are likely:

* a concrete temporal relevance evaluator,
* a lease evaluator,
* a triple-time reconciliation engine,
* receipt structures for heat, lease, and forecast transitions,
* and a first lawful runtime that can hold these objects without collapsing them into a mere task or reminder list.

---

## 14. Next scenario expansions

The next scenarios to add should likely include:

* multi-project reserve competition
* user override against system recommendation
* human review as a budget-time bottleneck
* asynchronous agent handoff across long future intervals
* civil cancellation with lingering orchestration pressure
* low-confidence forecast bundles and re-estimation behavior

These would pressure-test the stack further.
