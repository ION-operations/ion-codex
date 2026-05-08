---
type: protocol_review_draft
authority: A0_UNRATIFIED_REVIEW
status: REVIEW_ONLY
future_target: ION/02_architecture/API_RUNTIME_ENTRY_PROTOCOL.md
review_layer: ION/06_intelligence/orchestration/corpus_recovery/14_quarantined_runtime_review/
---

# API Runtime Entry Protocol — Review Draft

## Short thesis

ION needs an explicit API runtime-entry surface.

This surface should govern how an external or API carrier enters the runtime/session center lawfully without being mistaken for the whole authority center.

## Why this surface exists

The strongest historical runtime line preserved explicit API entry behavior in `ION-BUILD`.
The current line therefore needs a distinct API runtime-entry surface rather than relying on shell convenience, operator-entry analogy, or transport availability alone.

## API runtime entry is not

API runtime entry is **not**:
- the whole runtime/session authority center,
- queue/dispatch law,
- operator entry by another name,
- or enactment authority in general.

## Governing formulation

API runtime entry governs:
- external/API carrier binding into the runtime/session center,
- runtime-entry constraints,
- entry receipts,
- and lawful failure or refusal of API entry.

## Candidate objects

### ApiRuntimeEntryIntent
An explicit request to bind an API carrier into a lawful runtime/session path.

### ApiRuntimeEntryReceipt
A witness that entry succeeded, was deferred, escalated, or refused.

### ApiCarrierBoundary
The explicit boundary between external/API carrier behavior and the internal runtime/session center.

### RuntimeEntryFailureDisposition
The classified reason why a runtime entry failed or was denied.

## Boundary law

### Relation to operator entry
API entry may resemble operator invocation structurally, but it should not collapse into operator-entry law.

### Relation to runtime/session authority
API entry attaches to the runtime/session center. It does not replace that center.

### Relation to queue/dispatch
API entry may precede or feed queue/dispatch behavior, but it does not define queue/dispatch itself.

### Relation to activation law
API carrier entry should not be mistaken for enactment permission in the broader activation sense.

## Non-goals

This draft does **not** define:
- the whole session authority center,
- full queue/dispatch law,
- or the still-open activation lane.
