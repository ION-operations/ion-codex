# TEMPLATE CONTRACT PROJECTION ALIGNMENT AUDIT PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-24  
**Authority posture:** A3 until reviewed  
**Workstream:** WS-06 continuation — Template contract projection alignment audit  
**Purpose:** Ensure the runtime JSON projection of template metadata contracts does not silently drift from the human-governance YAML registry source.

---

## 1. Controlling law

```text
A runtime projection must remain auditable against its governance source.
```

V17 made Phase 1/Phase 2 automatically contract-aware when the JSON projection exists. That is correct only if ION can detect divergence between:

```text
ION/03_registry/template_metadata_contract_registry.yaml
ION/03_registry/template_metadata_contract_registry.projection.json
```

---

## 2. Source/projection relation

```text
YAML registry = governance source.
JSON projection = runtime-readable derivative.
Audit = Nemesis visibility over drift between the two.
```

The projection may be consumed by runtime. It must not become unreviewed canon.

---

## 3. Audit scope

The first audit must compare:

```text
template_id set
canonical_name
version
contract_status
projection source_registry pointer
duplicate template IDs
missing projection
malformed projection
malformed/minimally unreadable source
```

This is intentionally conservative and dependency-free. It does not require external YAML packages.

---

## 4. Verdicts

```text
ALIGNED
MISMATCH
SOURCE_MISSING
PROJECTION_MISSING
SOURCE_UNREADABLE
PROJECTION_UNREADABLE
```

---

## 5. Required receipt

Every audit run should be able to emit a receipt with:

```text
audit_id
source_registry_path
projection_path
verdict
source_contract_count
projection_contract_count
missing_in_projection
extra_in_projection
field_mismatches
duplicate_source_template_ids
duplicate_projection_template_ids
mutation_allowed: false
```

---

## 6. Non-loss clauses

This protocol is invalid if interpreted to allow:

1. JSON projection to supersede YAML source;
2. mismatched projection to be used silently in production;
3. projection generation without receipt;
4. runtime eventing to ignore known projection drift;
5. source/projection mismatch to mutate either file directly;
6. external YAML dependency to become required for safe kernel tests.

---

## 7. Minimal tests

```text
test_projection_audit_aligned_project_seed
test_projection_audit_detects_missing_contract_in_projection
test_projection_audit_detects_extra_contract_in_projection
test_projection_audit_detects_status_mismatch
test_projection_audit_missing_projection
test_projection_audit_writes_receipt_without_mutation
```
