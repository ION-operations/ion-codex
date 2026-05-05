# Runtime/session seam-pressure packet

## Purpose

Pressure-test the matched Lane C review set against the exact boundary failures most likely to collapse it.

Review set under pressure:
- `../14_quarantined_runtime_review/RUNTIME_SESSION_AUTHORITY_PROTOCOL.review_draft.md`
- `../14_quarantined_runtime_review/SESSION_QUEUE_AND_DISPATCH_PROTOCOL.review_draft.md`
- `../14_quarantined_runtime_review/API_RUNTIME_ENTRY_PROTOCOL.review_draft.md`

This packet does **not** install law.
It checks whether the three-surface split remains coherent when read through overlap and failure cases.

## Why this pass exists

The current review set is structurally clean in positive form.
That is not enough.
The runtime/session center is exactly the kind of area where adjacent surfaces can quietly absorb authority they should not hold.

The main failure risks are:
- scheduler law silently owning queue law
- reporting surfaces silently owning session authority
- API/service shells silently owning runtime entry authority
- queue/dispatch quietly re-answering activation questions
- continuation and settlement being misused as substitutes for runtime/session identity

## Pressure classes

### 1. Scheduler creep
A queue or dispatch decision is read as if it were just a narrowed version of top-level scheduler law.

Expected boundary:
- scheduler may stage and rank future work
- queue/dispatch governs bounded movement inside a lawful runtime/session center
- queue membership is not the whole scheduler

### 2. Reporting creep
Runtime-state witness or reporting surfaces are treated as if they define session authority merely because they can see session facts.

Expected boundary:
- reporting may witness runtime facts
- reporting does not create runtime/session authority
- seeing session state is not the same as governing session identity or persistence

### 3. API shell creep
API runtime entry is treated as the whole runtime/session center because external entry is visible and operational.

Expected boundary:
- API runtime entry binds an external carrier to the center
- it does not replace session authority
- transport presence is not the whole center

### 4. Activation bleed
Queue/dispatch or API entry is allowed to silently answer whether enactment is lawful in the broader activation sense.

Expected boundary:
- activation law remains external to this Lane C review set
- runtime/session law may prepare, bind, and stage
- it should not silently decide enactment permission

### 5. Continuation annexation
Continuation artifacts are treated as if they fully substitute for lawful runtime/session identity.

Expected boundary:
- continuation may preserve thread identity and support re-entry
- continuation does not become the whole runtime/session authority center

### 6. Settlement annexation
Settlement outcomes are treated as if they create or explain runtime/session authority rather than classifying closure of an already lawful session path.

Expected boundary:
- settlement classifies closure, deferment, escalation, or re-entry posture
- settlement does not become runtime/session authority

## Current judgment

The three-surface runtime/session split survives first adversarial reading.
It is **not** yet promotion-ready, but it is strong enough to continue as a matched review set.

The main remaining need after this pass is worked examples that show the three-surface split surviving concrete runtime flows.
