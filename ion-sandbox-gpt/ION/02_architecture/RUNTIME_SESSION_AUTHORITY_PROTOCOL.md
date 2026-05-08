# Runtime Session Authority Protocol

## Purpose

ION requires an explicit runtime/session authority center.

This protocol defines what a **runtime session** is, what it may lawfully bind, and how
carriers may attach to it. It is the durable substrate beneath bounded queue/dispatch
and supervised runtime assistance.

Runtime session authority is **not**:
- scheduler law,
- activation authority,
- runtime-state witness/reporting,
- packet legality,
- continuation law itself,
- or daemon/API shell convenience.

Those surfaces may constrain a runtime session, but they do not replace it.

## Governing formulation

Runtime session authority governs:
- runtime session identity,
- session persistence and re-entry,
- bounded pause and closure posture,
- carrier attachment,
- context/state bindings required for lawful continuation,
- the existence and integrity of a bounded session queue.

This protocol does not define the full queue/dispatch law or API entry semantics.
Those surfaces have their own protocols and are promoted only after this center exists.

## Canonical objects

### RuntimeSessionIdentity
A durable identity for the session being governed.

### RuntimeSessionAuthority
The lawful authority surface under which a session exists and persists.
It must reference the controlling root authority surface (e.g., repo authority).

### RuntimeSessionCarrierBinding
The explicit binding between a session and a carrier or transport posture.

### RuntimeSessionContextBinding
The session-bound context or state required for lawful continuation.

### RuntimeSessionReceipt
A witness proving that session creation, binding, pause, re-entry, queue mutation, or closure occurred.

## Boundary clarifications

### Relation to scheduler law
Scheduler law nominates work and governs horizon decisions.
Runtime session authority governs the session substrate beneath bounded dispatch.

Scheduler surfaces **must not** claim session identity, session persistence, or queue ownership.

### Relation to activation authority
Activation authority governs enactment crossing.
Runtime session authority governs session existence and bounded session state.

A session may exist without being activated. Activation never retroactively creates session authority.

### Relation to runtime-state witness/reporting
State/query/reporting surfaces may witness runtime facts.
They do not, by themselves, define session identity, carrier attachment, or lawful persistence.

### Relation to continuation law
Continuation may preserve thread identity and allow lawful re-entry.
Continuation does not replace session persistence, carrier binding, or session queue ownership.

### Relation to settlement law
Settlement classifies how a path closes or reopens.
It does not create session authority, nor does it substitute for session receipts.

## Minimal compliance requirements

A compliant runtime session center must:
- persist session identity and authority,
- persist explicit lifecycle posture for active, paused, or closed session state,
- persist carrier and context bindings when present,
- persist a bounded session queue,
- emit receipts for creation, binding, pause, re-entry, and closure operations,
- sanitize identifiers to prevent path escape or hidden authority mutation,
- remain subordinate to repo authority and kernel law.

## Non-goals

This protocol does **not** define:
- full queue/dispatch reconciliation semantics,
- API carrier entry semantics,
- daemon orchestration loops,
- or manager/orchestrator/swarm activation.

## Active emission note

This file was emitted into active architecture only after the coupled Lane C
runtime/session review chain completed promotion-candidate review, install-path
mapping, worked-example linkage, counterexample review, bounded thaw review, and
thaw closure as one set. Review-space drafts, criteria packets, mapping notes,
and thaw records remain preserved in the corpus recovery layers as support
evidence rather than as active-law replacements.
