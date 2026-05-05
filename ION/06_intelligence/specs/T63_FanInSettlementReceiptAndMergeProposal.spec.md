---
type: spec
authority: A2_EXECUTOR
created: 2026-04-09T23:56:00-04:00
status: ACTIVE
---

# T63 — Fan-In settlement receipt and merge proposal family

## Goal
Make M2 settlement outcomes durable and queryable.

## Required
- `branch_merge_proposal`
- `branch_settlement_receipt`
- parent-scope indexing
- outcome indexing
- release of active claims on non-deferred settlement

## Proof
- settlement tests cover accept, merge-required, review escalation, and persistence.
