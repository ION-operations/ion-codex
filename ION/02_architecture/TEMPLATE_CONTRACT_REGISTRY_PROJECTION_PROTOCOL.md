# TEMPLATE CONTRACT REGISTRY PROJECTION PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-24  
**Authority posture:** A3 until reviewed  
**Workstream:** WS-06 continuation — Template contract registry projection  
**Purpose:** Provide a dependency-free runtime projection for template metadata contracts and bind automation-capable event paths to it by default when available.

---

## 1. Problem

`template_metadata_contract_registry.yaml` is human-legible, but the safe `python -S` runtime path must not rely on external YAML packages.

Therefore ION needs a runtime projection:

```text
ION/03_registry/template_metadata_contract_registry.projection.json
```

The JSON projection is a derived runtime-readable surface, not an independent canon source.

---

## 2. Source/projection relation

```text
template_metadata_contract_registry.yaml
  = human/governance registry source

template_metadata_contract_registry.projection.json
  = dependency-free runtime projection
```

If the projection diverges from the source, Nemesis must flag the mismatch.

---

## 3. Loader behavior

The runtime loader must:

```text
read JSON projection if present
validate shape enough for runtime
return contracts keyed by template_id
avoid external dependencies
avoid registry mutation
fail closed if malformed in strict mode
return empty mapping if absent in non-strict mode
```

---

## 4. Default event behavior

Phase 1 and Phase 2 runtime modules should behave as follows:

```text
if explicit template_contracts is supplied:
    use it
elif projection exists in workspace:
    load projection and enforce contract-bound mode
else:
    preserve backward-compatible witness-only behavior
```

This means the real ION root becomes contract-aware by default, while isolated tests and legacy temp workspaces do not break.

---

## 5. Safety boundary

The loader may read registry projections only.

It may not:

```text
mutate YAML registry
mutate JSON projection
promote contracts
generate contracts silently
activate agents
commit graph state
```

---

## 6. Non-loss clauses

This protocol is invalid if interpreted to allow:

1. JSON projection to supersede governance registry source;
2. malformed projections to be ignored in strict production mode;
3. missing contracts to event successfully once projection mode is active;
4. stale projection to be treated as canon;
5. external YAML dependency to become required for kernel-safe tests;
6. contract projection loading to widen graph mutation authority.

---

## 7. Minimal tests

```text
test_contract_projection_loader_reads_json
test_contract_projection_loader_missing_non_strict_returns_empty
test_contract_projection_loader_malformed_strict_raises
test_phase1_auto_contracts_from_projection
test_phase1_auto_contract_projection_blocks_missing_contract
test_phase2_auto_contracts_from_projection
```
