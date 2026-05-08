# Session Queue and Dispatch Protocol

## Purpose

ION requires an explicit queue/dispatch surface **inside** the runtime/session center.

This protocol governs how bounded work is queued, selected, dispatched, and mutated within lawful
runtime session authority. It ensures queue/dispatch seriousness without pretending that higher
scheduler law, activation authority, or runtime-state reporting already replace this center.

This protocol is downstream of:
- `RUNTIME_SESSION_AUTHORITY_PROTOCOL.md`

And upstream of:
- `API_RUNTIME_ENTRY_PROTOCOL.md` (once promoted)

## What queue/dispatch is not

Session queue/dispatch is **not**:
- top-level orchestration scheduling,
- activation authority,
- session authority as a whole,
- or mere report output.

Scheduler surfaces may constrain queue membership. Activation surfaces may constrain enactment crossing.
Reporting surfaces may witness state. None of those surfaces define session queue ownership.

## Governing formulation

Session queue/dispatch governs:
- bounded queue membership,
- dispatch readiness and dispatch intents inside a session,
- lawful queue mutation receipts,
- dispatch transitions and the update of queue-item state,
- strict separation from scheduler ranking, activation permissioning, and reporting.

## Canonical objects

### SessionQueue
A bounded queue attached to a lawful runtime session.

### SessionQueueItem
A single queue item with explicit status and payload.

A queue item may nominate a kernel work unit by carrying a first-class `work_unit_id` field,
Payload remains available for auxiliary queue-local metadata, but core nomination must not hide inside an undifferentiated payload bag.

### SessionDispatchIntent
An explicit intention to dispatch a queue item (or a kernel work unit named by that item).

### SessionDispatchReceipt
A witness that dispatch occurred, was deferred, or was blocked, including which queue item and
which work unit were involved.

### QueueMutationReceipt
A witness proving lawful queue mutation (add/remove/status change).

## Boundary law

### Relation to scheduler law
Scheduler law ranks and stages work across horizons.
Session queue/dispatch governs bounded movement **inside** one runtime session.

Scheduler law must not claim session queue ownership, nor silently rewrite queue-item receipts.

### Relation to activation law
Queue/dispatch may prepare and nominate work.
It must not silently answer whether enactment is lawfully authorized.

Queue item DISPATCH_READY is not equivalent to activation permission.

### Relation to session authority
Queue/dispatch is owned by and subordinate to runtime session authority.
It may not create sessions, rewrite session carrier bindings, or replace session receipts.

### Relation to dispatch law
Kernel dispatch persists the `PENDING -> DISPATCHED` transition for dispatchable work units.
Session queue/dispatch binds session queue items to kernel dispatch without collapsing the boundary:
a session queue item nominates; kernel dispatch executes the lawful transition.

## Minimal compliance requirements

A compliant queue/dispatch surface must:
- persist a bounded queue per session,
- maintain explicit queue-item status transitions,
- require the parent runtime session to remain active before dispatch,
- require dispatch readiness before dispatch,
- emit receipts for queue mutations and dispatch transitions,
- prevent scheduler/reporting surfaces from masquerading as queue ownership.

## Non-goals

This protocol does **not** define:
- full runtime session identity law (see session authority protocol),
- API entry semantics,
- daemon dispatcher implementation,
- manager/orchestrator/swarm activation.

## Active emission note

This file was emitted into active architecture only after the coupled Lane C
runtime/session review chain completed promotion-candidate review, install-path
mapping, worked-example linkage, counterexample review, bounded thaw review, and
thaw closure as one set. Review-space drafts, criteria packets, mapping notes,
and thaw records remain preserved in the corpus recovery layers as support
evidence rather than as active-law replacements.
