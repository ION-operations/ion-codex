# Temporal Stack Mapping Into Current ION

## 0. Purpose

This document maps the emerging temporal stack back into current ION so the work remains evolutionary rather than duplicative.

The goal is to answer:

* where each draft protocol belongs,
* which current ION surfaces it overlaps with,
* which surfaces it should extend rather than replace,
* which parts of the temporal stack appear to have no current home,
* and what the minimal lawful insertion path would be.

This is not yet implementation code. It is architectural landing guidance.

---

## 1. The temporal stack being mapped

The drafts currently on the table are:

* `ORCHESTRATION_TEMPORAL_RELEVANCE_PROTOCOL`
* `TEMPORAL_CONTEXT_LEASE_PROTOCOL`
* `TRIPLE_TIME_RECONCILIATION_PROTOCOL`
* `TEMPORAL_OBJECT_SCHEMA`
* the broader temporal framework paper
* and the worked-scenarios document

These drafts should now be mapped onto existing ION centers.

---

## 2. Mapping principles

### 2.1 Do not create false centers

A new temporal layer must not silently become a second scheduler, second route-state system, second automation system, or second calendar.

### 2.2 Prefer overlay before replacement

If a current ION surface already holds a meaningful temporal concern, the correct move is probably to extend it or bind it into a shared temporal vocabulary rather than replace it.

### 2.3 Separate vocabulary from implementation

The temporal stack should first land as a shared vocabulary and protocol layer before forcing a full migration of current records.

### 2.4 Receipts before autonomy

Any new temporal evaluator should become auditable before it becomes deeply autonomous.

---

## 3. High-level landing map

A high-level first map looks like this.

### 3.1 Existing current ION centers most relevant to the temporal stack

The temporal stack most naturally lands across these current centers:

* horizon and orchestration planning
* scheduler law and schedule state
* branch / route-state / activation conditions
* automation state and fallback posture
* runtime/session recovery and activation lifecycle
* signal and receipt / history surfaces
* user-facing runtime / calendar / reminder expression layers
* budget, bounded work, and forecast-related planning surfaces

### 3.2 Likely architectural posture

The temporal stack should function as a **cross-cutting protocol layer** that binds these surfaces together.

It should not initially be one monolithic engine replacing them all.

---

## 4. Mapping: Orchestration Temporal Relevance

### 4.1 Current ION surfaces it most overlaps with

This protocol most directly overlaps with:

* horizon logic
* scheduler commitment gradients
* branch / route-state activation conditions
* automation posture and promotion logic
* readiness / blocked / deferred states
* cooling / archival / dormant-like status semantics already scattered in the system

### 4.2 What it should extend

It should extend these systems by giving them a shared language for:

* relevance heat
* wake conditions
* reconfirmation requirements
* preparation requirements
* cooling and dormancy transitions
* composite relevance across object types

### 4.3 What it should not replace

It should not replace:

* the scheduler itself,
* route-state logic,
* activation authority,
* or the civil schedule layer.

### 4.4 Best insertion path

The cleanest first landing is probably:

* introduce orchestration temporal profile fields as optional overlays on selected objects,
* write a conservative evaluator that consumes existing scheduler / route / automation state,
* emit recommendation receipts rather than hard decisions,
* then gradually bind outputs into preparation and review behaviors.

### 4.5 Current likely home

Conceptually, this belongs nearest to the orchestration and doctrine layer rather than purely runtime or purely UI surfaces.

This feels like a cross between current scheduler doctrine, route-state, and orchestration planning.

---

## 5. Mapping: Temporal Context Lease

### 5.1 Current ION surfaces it most overlaps with

This protocol most directly overlaps with:

* executor roles
* route / branch ownership
* workflow stewardship
* fallback and dormant responsibility postures
* runtime/session holder concepts
* preparation and review ownership

### 5.2 What it should extend

It should extend those systems by defining:

* bounded temporal stewardship,
* holder roles,
* holder transitions,
* dormant stewardship,
* and explicit transfer lineage.

### 5.3 What it should not replace

It should not replace:

* role identity,
* activation authority,
* scheduler lane assignment,
* or broad organizational structure.

A lease is not the same thing as permanent role ownership.

### 5.4 Best insertion path

The likely right insertion order is:

* begin with lease recommendations driven by temporal relevance,
* attach lease records to a limited set of future-bearing objects,
* support creation, transfer, downgrade, and expiry receipts,
* and only later bind those lease outputs into richer runtime behavior.

### 5.5 Current likely home

This belongs partly in orchestration doctrine and partly in runtime/session stewardship, because leases are the bridge between relevance and live holders.

---

## 6. Mapping: Triple Time Reconciliation

### 6.1 Current ION surfaces it most overlaps with

This protocol overlaps with:

* future/horizon planning
* scheduler posture
* civil schedule / reminder / calendar surfaces
* budget and bounded-work planning
* runtime feasibility and automation posture
* escalation and review logic

### 6.2 What it should extend

It should extend these by providing:

* alignment states,
* reconciliation postures,
* compression / deferment / escalation logic,
* and lease-adjustment recommendations.

### 6.3 What it should not replace

It should not replace:

* civil calendar semantics,
* budget accounting,
* scheduler logic,
* or activation authority.

It is a bridge law, not a sovereign controller.

### 6.4 Best insertion path

This should probably land later than temporal relevance and leases.

The likely path is:

1. get orchestration temporal relevance working,
2. get leases working,
3. then introduce triple-time reconciliation as a recommendation layer,
4. then allow it to influence user-facing runtime and escalation behavior.

### 6.5 Current likely home

This is the most cross-cutting of the new protocols. It likely lives at the orchestration/kernel boundary, with strong influence on user-facing runtime messaging and planning behavior.

---

## 7. Mapping: Temporal Object Schema

### 7.1 Current ION surfaces it most overlaps with

The schema overlaps with almost all current future-bearing objects:

* schedule entries
* route-state records
* branch records
* automation state records
* runtime/session records
* reminders / calendar objects
* forecast or planning objects
* historical receipts / signal objects

### 7.2 What it should extend

It should provide a common vocabulary for:

* identity
* lineage
* civil profile
* orchestration profile
* budget profile
* lease profile
* reconciliation profile
* and receipt/profile references

### 7.3 What it should not do immediately

It should not force every existing object into one giant new storage format on day one.

That would be a migration mistake.

### 7.4 Best insertion path

The schema should first be treated as:

* canonical vocabulary,
* optional overlay fields,
* and mapping guidance.

Only later should it become a persistent first-class record family if needed.

### 7.5 Current likely home

This belongs across doctrine, schema, and storage planning rather than in one isolated subsystem.

---

## 8. Mapping into existing ION object classes

The temporal stack should likely first attach to a narrow initial set of object classes rather than all of them.

### 8.1 Strong candidate first object classes

The best initial candidates appear to be:

* future commitments
* recurring reviews or routines
* deferred or dormant branch activations
* scheduled deliverables
* preparation/reconfirmation checkpoints
* project budget checkpoints

These are temporally rich and likely to expose the architecture quickly.

### 8.2 Object classes to delay

Some object classes probably should not be migrated first:

* fully archived historical artifacts
* low-significance ephemeral notes
* every generic memory atom
* purely structural records with no future-bearing behavior

This keeps the first landing disciplined.

---

## 9. Mapping into user-facing behavior

A major issue is when these protocols become visible to the user.

### 9.1 What should remain mostly internal at first

The following should remain mostly kernel/orchestration internal early on:

* full heat vectors
* raw lease states
* budget heat details
* alignment-state internals
* full reconciliation posture logic

### 9.2 What may surface to the user naturally

These outputs can surface as dialogue:

* reconfirmation questions
* preparation reminders
* budget-aware compression suggestions
* escalation suggestions
* soft warmup notices
* civil schedule confirmations
* post-completion cooling / recurrence language

Thus, the user interacts with the outputs, not the whole internal theory.

---

## 10. Mapping into receipts and audit

The temporal stack should land with strong receipt support.

### 10.1 New receipt families likely needed

Potential receipt families include:

* temporal heat transition receipts
* lease creation / transfer / expiry receipts
* reconfirmation receipts
* preparation start / finish receipts
* budget forecast receipts
* budget actual receipts
* reconciliation posture receipts
* recurrence reseed receipts

### 10.2 Why this matters

Without receipts, the temporal stack will feel magical.
With receipts, it becomes auditable and calibratable.

---

## 11. Minimal lawful insertion order

The temporal stack should probably be inserted in this order.

### Step 1

Adopt `TEMPORAL_OBJECT_SCHEMA` as canonical vocabulary only.

### Step 2

Draft and lightly bind `ORCHESTRATION_TEMPORAL_RELEVANCE_PROTOCOL` to existing scheduler / route / automation / horizon surfaces.

### Step 3

Introduce `TEMPORAL_CONTEXT_LEASE_PROTOCOL` as recommendation and receipt logic for a small set of future-bearing objects.

### Step 4

Introduce a conservative `TRIPLE_TIME_RECONCILIATION_PROTOCOL` recommendation layer for a small number of user-facing commitments.

### Step 5

Bind the results into runtime/calendar/reminder expression surfaces.

### Step 6

Only later, deepen autonomy and automation.

This order minimizes duplication risk.

---

## 12. Strongest insertion candidates by current subsystem

### 12.1 Scheduler / horizon

Best place to contribute:

* heat inputs
* wake conditions
* future candidate relevance
* preparation windows

### 12.2 Route-state / activation conditions

Best place to contribute:

* branch warmth
* activation readiness influence
* dormant-to-warm transitions

### 12.3 Automation state

n
Best place to contribute:

* whether budget posture or relevance supports automation promotion,
* whether cooling or dormancy should demote automation posture,
* whether fallback stewardship is needed.

### 12.4 Runtime/session layer

Best place to contribute:

* active holders of user-facing commitments,
* runtime preparation ownership,
* civil/orchestration/budget reconciliation outputs,
* and later reminder / calendar handling.

### 12.5 Receipt layer

Best place to contribute:

* auditable transitions,
* lineage preservation,
* estimate calibration,
* historical actual-versus-forecast intelligence.

---

## 13. What still appears to have no current home

Several parts of the temporal stack still look like they lack a strong current home and may require genuine new centers.

These include:

* lease lineage as a first-class concept
* unified temporal object profile overlays
* explicit heat vector records
* explicit budget-time forecast / actual reconciliation as temporal object fields
* generalized recurrence reseeding with lineage preservation
* explicit alignment-state and reconciliation posture records

These are likely the true “new centers,” as opposed to the more obviously evolutionary pieces.

---

## 14. Main contradiction risks

The temporal stack could still go wrong in several ways.

### 14.1 Scheduler overreach

If scheduler law is made to carry all temporal relevance and lease logic, it will become bloated and fragile.

### 14.2 Calendar overreach

If civil-time objects are treated as the main temporal objects, orchestration time will be reduced to reminder logic.

### 14.3 Runtime overreach

If runtime/session becomes the holder of all temporal responsibility too early, it may become another false center.

### 14.4 Protocol drift

If the new protocols are not anchored to receipts and current object classes, they may remain elegant but floating abstractions.

---

## 15. Strongest present conclusion

The temporal stack is attachable to current ION.

It is not obviously duplicative if inserted carefully.

The safest landing path is:

* schema vocabulary first,
* temporal relevance overlay second,
* lease logic third,
* reconciliation bridge fourth,
* user-facing runtime expression later.

This means the drafts are no longer merely theoretical. They now have a plausible evolutionary insertion path into the present organism.

---

## 16. Immediate next move

The strongest next move after this mapping is to design a **first-pass evaluator** that works over a narrow subset of temporal-bearing objects.

That evaluator should probably combine:

* relevance computation,
* lease recommendation,
* and reconciliation posture,

in a conservative rule-based way for a small initial object family such as:

* scheduled deliverables,
* recurring reviews,
* and dormant future commitments.

That would be the first point where the temporal stack becomes operational rather than purely documentary.
