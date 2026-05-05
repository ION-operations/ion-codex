---
type: public_orientation
status: DRAFT_NON_AUTHORITY
production_authority: false
live_execution_authority: false
---

# Context System

ION treats context as inherited operational state, not as a long prompt.

The goal is not to give a model everything. The goal is to give a mounted role
the bounded material needed for the current lawful act.

## Compiled Context

A context package is a compiled, bounded, ranked input to a role.

It should make explicit:

- current objective
- relevant authority files
- role and carrier boundary
- active packet references
- allowed and forbidden paths
- needed history
- expected return contract
- validation requirements

This is different from relying on a model's ambient recall.

## Inherited Context

In ION, the next context is inherited from accepted movement.

That means receipts matter not only as audit logs, but as future context
material. A receipt closes one act and improves the next act's starting point.

```text
accepted act -> receipt -> updated context -> next lawful act
```

## No Informal Memory Authority

Private model memory is not ION authority.

A model may remember something useful, but ION state must be recoverable from
packets, context packages, registries, receipts, manifests, and gates.

This is what lets different carriers continue the same work without pretending
to be the same identity.

## Context Failure Modes

Common failures:

- stale context treated as current
- historical report treated as live authority
- summary treated as proof
- carrier memory treated as accepted state
- large context pasted without selection law
- receipt omitted, so the next worker cannot inherit the delta

ION addresses these by making context explicit, bounded, and proof-linked.

## Runtime Boundary

This document is orientation. Active context authority lives in current packets,
compiled context bundles, carrier onboarding packets, role context packages,
and the context proof gate.
