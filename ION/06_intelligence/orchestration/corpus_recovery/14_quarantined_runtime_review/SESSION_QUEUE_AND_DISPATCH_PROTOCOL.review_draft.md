---
type: protocol_review_draft
authority: A0_UNRATIFIED_REVIEW
status: REVIEW_ONLY
future_target: ION/02_architecture/SESSION_QUEUE_AND_DISPATCH_PROTOCOL.md
review_layer: ION/06_intelligence/orchestration/corpus_recovery/14_quarantined_runtime_review/
---

# Session Queue and Dispatch Protocol — Review Draft

## Short thesis

ION needs an explicit queue/dispatch surface inside the runtime/session center.

This surface should govern how bounded work is queued, selected, dispatched, and mutated within lawful session authority.

It is therefore not identical to higher scheduler law and not reducible to runtime-state witness artifacts.

## Why this surface exists

The historical runtime/session line preserved explicit queue and scheduler/session interaction evidence in `ION-BUILD`.
The current branch needs a current-line surface that can carry queue/dispatch seriousness without pretending the scheduler already solved it all.

## Queue/dispatch is not

Queue/dispatch is **not**:
- top-level orchestration scheduling,
- activation authority,
- session authority as a whole,
- or mere report output.

## Governing formulation

Session queue and dispatch governs:
- bounded queue membership,
- dispatch intents,
- queue mutation receipts,
- dispatch readiness,
- and relation to the owning runtime/session center.

## Candidate objects

### SessionQueue
The bounded queue surface attached to a lawful runtime/session center.

### SessionDispatchIntent
The explicit intention to dispatch bounded work from a session queue.

### SessionDispatchReceipt
A witness showing that dispatch occurred, was deferred, or was blocked.

### QueueMutationWitness
A witness for lawful queue mutation events.

## Boundary law

### Relation to scheduler law
Scheduler law may rank or stage future work across a broader horizon.
Session queue/dispatch governs bounded movement inside the runtime/session center.

### Relation to activation law
Queue/dispatch may prepare or nominate work.
It should not silently answer whether enactment is lawfully authorized.

### Relation to session authority
Queue/dispatch is owned by and downstream of the runtime/session center, not its replacement.

## Non-goals

This draft does **not** define:
- API entry semantics,
- full runtime/session identity law,
- or broad activation authority.
