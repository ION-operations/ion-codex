---
type: protocol
authority: A3_OPERATIONAL
template: SPEC
created: 2026-04-23T18:32:00-04:00
status: ACTIVE_CURRENT_PHASE
connections:
  - ION/02_architecture/NAME_LINEAGE_REGISTRY_PROTOCOL.md
  - ION/03_registry/name_lineage_registry.yaml
  - ION/04_packages/kernel/name_lineage.py
---

# INGRESS AUTHORITY RESOLUTION PROTOCOL

## Purpose

Define how live names entering the runtime become lawful execution identity.

## Law

1. A raw incoming name may be preserved for provenance.
2. Live execution must run on current resolved authority truth, not on stale free-form input.
3. If a historical name has no lawful automatic route, the ingress should refuse silent execution.
4. Historical replay may preserve older names without forcing active normalization.

## First-pass live ingress surfaces

- bootstrap packet creation defaults
- open-question routing
- explicit answer ingestion
- operator CLI resolution commands

## Resolution outcomes

### `ALLOW_AS_AUTHORITY`

The incoming name is already the current true name.

### `NORMALIZE_TO_CURRENT_TRUE_NAME`

The incoming name is preserved as lineage but the active execution name is the current
true name.

### `REQUIRES_EXPLICIT_TRUE_NAME`

The incoming name is stale, ambiguous, retired, or carrier-only.
The system must not silently decide which current authority the caller meant.

### `UNREGISTERED_NAME`

The current lineage registry does not yet govern this token.
The system may carry it with warning until wider lineage coverage exists.

## Witness rule

When normalization occurs, the runtime should preserve the raw incoming token in a
visible witness field or receipt rather than flattening the historical token away.
