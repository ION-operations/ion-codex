# API Runtime Entry Protocol

## Purpose

ION requires an explicit API runtime-entry surface.

This protocol governs how an external/API carrier enters the runtime/session center
lawfully without being mistaken for the whole center.

API runtime entry is **not**:
- the whole runtime/session authority center,
- queue/dispatch law,
- operator entry by another name,
- or enactment/activation authority in general.

## Governing formulation

API runtime entry governs:
- external/API carrier attachment into an existing runtime/session center,
- bounded creation of a new runtime session only when creation is explicitly allowed,
- runtime-entry constraints and refusal conditions,
- entry receipts and API carrier-boundary witnesses.

It does not define the whole session authority center and does not define queue/dispatch law.
Those surfaces remain governed by their own protocols.

## Canonical objects

### ApiRuntimeEntryIntent
An explicit request to bind an API carrier into a runtime/session path.

### ApiRuntimeEntryReceipt
A receipt that entry was accepted or refused, with explicit witness paths.

### ApiCarrierBoundary
A witness that the external/API carrier is attached to the runtime/session center
without becoming scheduler, queue, or activation authority.

### RuntimeEntryFailureDisposition
The classified reason why runtime entry was refused.

## Boundary law

### Relation to runtime/session authority
API runtime entry attaches to runtime/session authority.
It does not replace that center.

### Relation to queue/dispatch
API runtime entry may later feed queue/dispatch behavior, but it does not define
queue ownership, dispatch readiness, or queue mutation law.

### Relation to activation authority
API carrier entry does not authorize enactment crossing.
Activation law still decides whether broader executable work may begin.

## Current bounded slice

The current bounded slice supports:
- attach to an existing runtime session,
- create a new runtime session only when creation is explicitly allowed,
- bind an EXTERNAL_API carrier to that session,
- optionally bind context when both `context_version` and `context_ref` are provided,
- refuse closed sessions,
- refuse paused sessions unless explicit re-entry is requested,
- restore a paused session to active posture when explicit re-entry succeeds,
- emit explicit API runtime-entry receipts and API carrier-boundary witnesses.

This slice does **not** import a full server stack, HTTP service shell, or daemon runtime.

## Active emission note

This file was emitted into active architecture only after the coupled Lane C
runtime/session review chain completed promotion-candidate review, install-path
mapping, worked-example linkage, counterexample review, bounded thaw review, and
thaw closure as one set. Review-space drafts, criteria packets, mapping notes,
and thaw records remain preserved in the corpus recovery layers as support
evidence rather than as active-law replacements.
