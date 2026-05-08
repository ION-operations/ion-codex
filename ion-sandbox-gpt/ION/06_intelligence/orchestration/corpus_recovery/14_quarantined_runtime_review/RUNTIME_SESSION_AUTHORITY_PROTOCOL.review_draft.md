---
type: protocol_review_draft
authority: A0_UNRATIFIED_REVIEW
status: REVIEW_ONLY
future_target: ION/02_architecture/RUNTIME_SESSION_AUTHORITY_PROTOCOL.md
review_layer: ION/06_intelligence/orchestration/corpus_recovery/14_quarantined_runtime_review/
---

# Runtime Session Authority Protocol — Review Draft

## Short thesis

ION needs an explicit runtime/session authority center.

This center should govern the lawful identity, continuity, and bounded authority of runtime sessions.
It should define what a runtime session is, what state and context it may bind, and how carriers lawfully attach to it.

It is therefore neither:
- scheduler law,
- runtime-state witness/reporting,
- nor daemon/API shell convenience.

## Why this surface exists

The strongest historical runtime/session center survived in `ION-BUILD`, while the current branch preserved stronger startup, packet, reporting, and routing surfaces.
The current line therefore needs a first-class runtime/session authority center if it is going to reintegrate the historical runtime organism honestly.

## Runtime/session authority is not

Runtime/session authority is **not**:
- top-level orchestration scheduling,
- activation authority,
- runtime reporting,
- packet legality,
- or continuation law itself.

Those surfaces may constrain runtime sessions, but they do not replace them.

## Governing formulation

Runtime/session authority is the bounded surface that governs:
- runtime session identity,
- runtime context binding,
- carrier attachment,
- lawful session persistence,
- and the relation between session state and downstream queue/dispatch behavior.

## Canonical objects

### RuntimeSessionIdentity
A durable identity for the session being governed.

### RuntimeSessionAuthority
The lawful authority surface under which a session exists and persists.

### RuntimeSessionCarrierBinding
The explicit binding between a session and a carrier or transport posture.

### RuntimeSessionContextBinding
The session-bound context or state required for lawful continuation.

### RuntimeSessionReceipt
A witness proving that session creation, binding, re-entry, or release occurred.

## Relation map

### Relation to scheduler law
Scheduler law may nominate work or govern future-work horizon decisions.
Runtime/session authority governs the lawful session substrate beneath bounded dispatch and execution surfaces.

### Relation to runtime-state witness/reporting
State/query/reporting surfaces may witness runtime facts.
They do not, by themselves, define session authority or lawful persistence.

### Relation to continuation law
Continuation may preserve thread identity and allow lawful re-entry.
But continuation is not the whole runtime/session center.

### Relation to settlement law
Settlement may classify how a session path closes or reopens.
It does not create session authority.

## Non-goals

This draft does **not** define:
- the full queue/dispatch law,
- API carrier entry semantics,
- or the still-open activation lane.
