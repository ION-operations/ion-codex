# TEMPORAL_CONTEXT_LEASE_PROTOCOL Draft

## 0. Status

Draft protocol for ION temporal development.

This protocol is intended as a companion to `ORCHESTRATION_TEMPORAL_RELEVANCE_PROTOCOL`.

Its purpose is to define who lawfully holds future-bearing objects, when that holding begins, under what conditions it expires, and how responsibility transfers without losing continuity.

---

## 1. Purpose

ION requires a lawful mechanism for assigning temporal responsibility.

A future-bearing object should not merely be “remembered by the system.” It should, when appropriate, be held under a governed temporal lease.

This protocol governs:

* who may hold present attention responsibility over a future-bearing object,
* when that responsibility becomes active,
* how long it remains active,
* how it cools or lapses,
* how it transfers,
* and how temporal responsibility remains bounded rather than ambient.

The protocol exists to prevent two opposite failures:

* no one owns the future object, so it drifts,
* everyone holds the future object, so context bloats and relevance becomes noisy.

---

## 2. Non-goals

This protocol does **not** define:

* civil calendar semantics,
* alarm delivery,
* scheduler ranking,
* activation authority,
* budget allocation,
* or the entire temporal relevance computation.

Those systems may influence lease behavior, but they are not replaced by this protocol.

This protocol also does not grant enactment authority. A holder of a lease is not thereby entitled to execute work without satisfying other lawful gates.

---

## 3. Core thesis

A future-bearing object should enter present attention lawfully, not ambiently.

A temporal lease is the bounded right and duty of a holder to maintain awareness, stewardship, review, reconfirmation, preparation, or fallback responsibility for a temporal-bearing object.

This means:

* temporal objects are not globally hot by default,
* context should not be permanently retained everywhere,
* responsibility should be explicit,
* and future-bearing work should have lawful stewardship.

The lease model is therefore the mechanism by which ION turns temporal relevance into bounded attention and responsibility.

---

## 4. Governing formulation

Whenever a temporal-bearing object reaches a relevant enough orchestration posture, the system may create, modify, transfer, downgrade, or expire a temporal lease.

A lease is not identical to object existence.
A lease is not identical to activation.
A lease is not identical to ownership in a broad organizational sense.

A lease is specifically the bounded present-time stewardship posture by which an object is kept alive in lawful attention.

---

## 5. Canonical concepts

### 5.1 Temporal-bearing object

Any object whose relevance unfolds across time and may therefore need bounded stewardship.

Examples include:

* future commitments
* deadlines
* reports
* recurring reviews
* dormant obligations
* future branch activations
* preparation windows
* follow-ups
* reconfirmation obligations
* budget review checkpoints

### 5.2 Lease holder

The entity holding the lease.

Possible holder classes include:

* agent
* branch
* subsystem
* workflow
* user-facing runtime
* dormant fallback steward

### 5.3 Lease role

The type of stewardship being exercised.

Possible roles include:

* owner
* watcher
* reviewer
* fallback
* preparer
* reconfirmation steward
* dormant steward

### 5.4 Lease state

The current posture of the lease itself.

Possible states include:

* latent
* warm
* active
* review
* cooling
* expired
* revoked
* transferred
* archived

### 5.5 Lease scope

The visibility and responsibility boundary of the lease.

For example:

* local to one branch,
* visible to one runtime surface,
* shared between one primary owner and one fallback steward,
* or only visible during a preparation window.

### 5.6 Lease lineage

The history of prior holders, transfers, renewals, revocations, and expirations.

---

## 6. Why leases are necessary

Without lease logic, ION risks two pathologies.

### 6.1 No-holder drift

A future object exists in memory or schedule but is not actively stewarded by any lawful holder.
This leads to forgotten future commitments, poor reconfirmation behavior, and false dormancy.

### 6.2 Ambient omniscience

Every subsystem behaves as though it must hold all relevant future objects all the time.
This leads to context bloat, attention noise, poor prioritization, and unstable reasoning.

A lease solves both by making stewardship explicit and bounded.

---

## 7. Lease inputs

Lease behavior should be influenced by lawful inputs, not intuition alone.

### 7.1 Temporal relevance inputs

* orchestration heat
* wake requirement
* reconfirmation requirement
* preparation requirement
* cooling permission
* dormancy eligibility

These should usually arrive from the orchestration temporal relevance layer.

### 7.2 Object-class inputs

Different object types may justify different lease defaults.

For example:

* a future report may need a preparer and a reconfirmation steward,
* a recurring checkup may need a dormant steward until it warms,
* a future branch activation may belong primarily to a branch rather than a user-facing runtime.

### 7.3 Dependency inputs

If many future objects depend on one object, that object may justify a stronger or longer-lived lease.

### 7.4 User inputs

The user may directly assign, confirm, withdraw, or modify temporal responsibility.

### 7.5 Budget inputs

A lease may be recommended, shortened, downgraded, or moved into fallback posture depending on budget and endurance conditions.

### 7.6 Civil-time inputs

Approaching real-world deadlines or scheduled events may intensify or shift lease posture.

---

## 8. Lease outputs

A lease engine may produce:

* `lease_required`
* `lease_role`
* `holder_type`
* `holder_ref`
* `lease_start`
* `lease_end`
* `renewal_required`
* `transfer_required`
* `downgrade_required`
* `fallback_required`
* `expiration_permitted`
* `revocation_permitted`

The lease layer may also emit receipts or transfer instructions.

---

## 9. Lease roles in detail

### 9.1 Owner

Primary steward of the object’s present temporal responsibility.

The owner is not necessarily the enactor. The owner is the entity responsible for ensuring that the object remains lawfully attended, reconfirmed, prepared, or escalated as needed.

### 9.2 Watcher

Maintains low-burn awareness without primary stewardship.
Useful for objects that are warming but not yet hot.

### 9.3 Reviewer

Responsible for checkpoints, reconfirmation, or validation before enactment.

### 9.4 Preparer

Responsible for preflight gathering, context preload, dependency readiness, or readiness staging.

### 9.5 Fallback

Holds the object if the primary holder cools, expires, fails, or transfers responsibility.

### 9.6 Dormant steward

Maintains lawful low-intensity linkage while the object remains dormant.

---

## 10. Lease states in detail

### 10.1 Latent

No active present-time stewardship yet, but a future lease may be created if relevance rises.

### 10.2 Warm

Lease is becoming active but stewardship is still low-burn.

### 10.3 Active

The holder is currently responsible for present-time stewardship.

### 10.4 Review

The lease is active specifically for validation, reconfirmation, or decision review.

### 10.5 Cooling

The lease is being reduced or wound down but not yet fully expired.

### 10.6 Expired

The lease ended lawfully without transfer.

### 10.7 Revoked

The lease ended because its basis no longer held or because a higher-order change invalidated it.

### 10.8 Transferred

The lease is no longer held by the current holder, but continuity was passed onward.

### 10.9 Archived

The lease and its lineage are preserved for history, but no present stewardship remains.

---

## 11. Lease lifecycle

A plausible lifecycle might be:

* no lease
* latent lease recommendation
* warm lease
* active lease
* review or preparation substate
* cooling lease
* transferred or expired lease
* archived lease lineage

This lifecycle should be receipted.

---

## 12. Lease creation

### 12.1 Conditions for creation

A lease may be created when:

* an object becomes warm or hot enough,
* a reconfirmation window opens,
* a preparation window opens,
* a dormant obligation requires stewardship,
* a civil deadline is approaching,
* or the system needs bounded present attention rather than ambient memory.

### 12.2 Creation constraints

A lease should not be created merely because an object exists.

Lease creation should be justified by:

* current relevance,
* lawful stewardship need,
* and a bounded holder assignment.

---

## 13. Lease renewal, downgrade, and expiry

### 13.1 Renewal

A lease may renew when:

* relevance remains high,
* reconfirmation succeeds,
* preparation is still in progress,
* or a recurrence window is reopening.

### 13.2 Downgrade

A lease may downgrade when:

* heat drops,
* the object finishes preparation and returns to waiting posture,
* budget posture requires a lighter steward,
* or the object leaves present focus but remains dormant.

### 13.3 Expiry

A lease may expire when:

* the object cools lawfully,
* the object is completed,
* the obligation is cancelled,
* the object returns to lawful dormancy,
* or a transfer made the old lease unnecessary.

### 13.4 Revocation

A lease may be revoked when:

* the basis of the commitment collapses,
* the object is superseded,
* the holder loses legitimacy,
* or a higher-order route change invalidates the lease.

---

## 14. Lease transfer

Transfer is one of the most important features.

### 14.1 Why transfer matters

Without transfer, continuity breaks whenever future stewardship changes hands.

### 14.2 Conditions for transfer

A lease may transfer when:

* a warmer object becomes the responsibility of a different subsystem,
* a dormant object becomes active and moves from fallback steward to owner,
* a user-facing runtime hands a future obligation to a branch worker,
* budget posture requires a different holder class,
* or a scheduled future object moves from watcher to preparer.

### 14.3 Transfer requirements

Transfer should preserve:

* object identity,
* temporal lineage,
* holder transition receipts,
* and any active obligations still attached to the object.

Transfer must not look like object death followed by object recreation.

---

## 15. Lease and activation boundary

A lease does not equal activation authority.

A holder may lawfully steward an object for:

* reconfirmation,
* preparation,
* review,
* or monitoring,

without yet being permitted to enact work.

This boundary must remain explicit.

Activation law may consume lease state as input, but a lease itself does not authorize enactment.

---

## 16. Lease and scheduler boundary

A scheduler may nominate work, but it does not automatically become the owner of temporal responsibility.

Scheduler state may justify a lease recommendation, but scheduler law must not silently swallow lease law.

This is important because future obligations are more than scheduled items. They are governed stewardship objects.

---

## 17. Lease and civil-time boundary

Civil deadlines or appointments may intensify lease posture, but the lease layer is not just a calendar subscriber.

For example:

* a future report may be on the calendar,
* but only a few days before it warms enough for a preparer or reviewer lease,
* and only near enactment does the owner lease intensify.

So civil time influences lease behavior without defining it entirely.

---

## 18. Lease and budget-time boundary

Budget posture may affect:

* whether a lease is active or merely latent,
* whether the holder is full owner or fallback steward,
* whether a hot object can maintain a high-burn preparer lease,
* whether downgrade or delayed activation is required.

But budget scarcity should not silently erase commitments.
It should alter stewardship posture lawfully.

---

## 19. Minimal compliance requirements

A compliant lease implementation must:

* assign holders explicitly,
* distinguish role and state,
* support renewal, downgrade, transfer, expiry, and revocation,
* keep continuity through lineage rather than object recreation,
* remain distinct from activation authority,
* remain distinct from scheduler ownership,
* and emit auditable receipts.

---

## 20. Failure modes

### 20.1 Ambient holding

If the protocol is ignored, every subsystem may behave as though it owns all future obligations.

### 20.2 False ownership

If a scheduler or activation surface implicitly becomes the owner of temporal responsibility, lease law is bypassed.

### 20.3 No fallback

Without fallback stewardship, cooling or holder failure may produce dropped future obligations.

### 20.4 Transfer breakage

Without transfer lineage, continuity is lost whenever responsibility changes hands.

### 20.5 Lease inflation

If leases are created too eagerly, the system becomes noisy and over-attentive.

### 20.6 Lease starvation

If leases are created too late, the system underprepares and misses lawful warmup or reconfirmation behavior.

---

## 21. Candidate data model

A first-pass lease record might include:

* `lease_id`
* `object_id`
* `object_type`
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
* `parent_lease`
* `prior_holder_ref`
* `successor_holder_ref`
* `receipt_ref`

---

## 22. Minimal first algorithm

A conservative initial lease evaluator should:

1. consume temporal relevance outputs,
2. determine whether stewardship is required,
3. choose a holder class,
4. assign a lease role,
5. determine lease state,
6. emit renewal / downgrade / transfer / expiry recommendations,
7. emit receipts or lease transition events.

This evaluator should begin as a rule-based and auditable system.

---

## 23. Recommended implementation path

### Phase 1

Introduce lease vocabulary and record structure.

### Phase 2

Bind lease recommendations to orchestration temporal relevance outputs.

### Phase 3

Add receipts for lease creation, renewal, downgrade, transfer, expiry, and revocation.

### Phase 4

Bind lease logic to preparation, reconfirmation, and dormant stewardship flows.

### Phase 5

Integrate with civil and budget bridge layers.

---

## 24. Strongest present conclusion

The future should not be globally remembered and globally hot.

It should be lawfully stewarded.

`TEMPORAL_CONTEXT_LEASE_PROTOCOL` is the protocol that turns temporal relevance into bounded responsibility.

It ensures that future obligations are neither ownerless nor omnipresent, but held under explicit, auditable, and transferable stewardship within ION.
