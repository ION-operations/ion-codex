# Runtime/session negative-case counterexample review packet

## Question class
Counterexample review for the Lane C runtime/session/API promotion candidate.

## Primary candidate under stress
- `../16_promotion_candidate_review/runtime_session_joint_promotion_candidate_packet.md`
- `../16_promotion_candidate_review/runtime_session_joint_thaw_readiness_criteria.md`
- `../18_worked_examples/runtime_session_receipt_linkage_worked_examples_packet.md`
- `../19_install_path_mapping/runtime_session_install_path_mapping_packet.md`
- `../14_quarantined_runtime_review/RUNTIME_SESSION_AUTHORITY_PROTOCOL.review_draft.md`
- `../14_quarantined_runtime_review/SESSION_QUEUE_AND_DISPATCH_PROTOCOL.review_draft.md`
- `../14_quarantined_runtime_review/API_RUNTIME_ENTRY_PROTOCOL.review_draft.md`

## Purpose
Test whether the runtime/session trio survives explicit negative and refusal
cases without letting runtime/session authority, queue/dispatch, API entry, or
adjacent continuation/settlement surfaces collapse into one another.

This packet does **not** thaw the candidate.
This packet does **not** install active law.
This packet does **not** claim that pause/re-entry/closure handling is already
complete.

## Why this review is necessary
The current Lane C slice is already legible in positive form and now survives
receipt-linkage review.

That is still not enough for thaw readiness.

The remaining risk is that the set only behaves coherently when everything goes
right, while refusal, blocked movement, stale carrier/context state, or
re-entry pressure quietly reintroduce authority confusion.

## Counterexample classes

### 1. Invalid runtime session identity
A session identifier attempts path escape or hidden authority mutation.

Expected outcome:
- invalid session identity is rejected at the runtime/session authority layer
- no hidden session root is created
- refusal happens before queue or carrier meaning can be inferred

### 2. Blocked queue prerequisites
A queue item is missing lawful dispatch prerequisites or is already cancelled.

Expected outcome:
- queue ownership remains inside the session center
- dispatch only occurs from `DISPATCH_READY`
- cancelled or underspecified queue items are blocked rather than silently
  coerced into dispatch

### 3. API refusal and malformed entry
API entry attempts to attach to a missing session, create a session without
root authority, supply partial context, or pass an invalid carrier reference.

Expected outcome:
- API entry may refuse cleanly without becoming the center
- refusal provenance remains explicit
- malformed entry does not mint hidden session authority

### 4. Carrier/context conflict under re-attachment pressure
An entry attempt collides with an already-bound carrier or context.

Expected outcome:
- existing carrier/context bindings remain authoritative until lawfully changed
- conflict is emitted as refusal, not silently overwritten
- API entry remains attachment law, not rebinding sovereignty

### 5. Queue-local cancellation versus dispatch convenience
A queue item that has already been cancelled is treated as if it were still
dispatchable.

Expected outcome:
- queue-local cancellation remains a real blocking status
- dispatch convenience does not overwrite queue truth

### 6. Runtime pause, lawful re-entry, and closure pressure
A runtime path pauses, resumes, or re-enters after prior bounded history.

Expected outcome:
- pause and re-entry remain governed by runtime/session authority plus
  continuity law
- continuation or settlement may cite prior runtime receipts but do not replace
  session identity or queue ownership
- any resumed attachment rules remain explicit rather than implied

## Current review judgment
Current judgment: **first bounded negative-case slice demonstrated — still not
thaw-ready**

What this pass establishes:
- invalid session identity is bounded at the session-authority layer
- blocked queue prerequisites are explicit at the queue/dispatch layer
- API refusal modes are explicit for missing session, missing root authority,
  malformed context, invalid carrier ref, and binding conflict
- queue-local cancellation already blocks dispatch under current kernel law

What still remains after this pass:
- explicit runtime pause handling
- lawful re-entry pressure across prior carrier/context state
- closure posture that cites runtime/session history without letting settlement
  annex the center

## Landing boundary
Counterexample review only.
No thaw authorization.
No active-law installation.
