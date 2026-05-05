# TEMPLATE CONTRACT RELEASE GATE PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-24  
**Authority posture:** A3 until reviewed  
**Workstream:** WS-06 continuation — release/checkpoint validation gate  
**Purpose:** Make the template contract source/projection alignment audit actionable during release, checkpoint, and production automation readiness checks.

---

## 1. Controlling law

```text
Production contract-bound automation must not proceed unless the template
metadata contract source and runtime projection are aligned.
```

V18 gave Nemesis visibility. V19 converts that visibility into a gate.

---

## 2. Gate relation

```text
template_metadata_contract_registry.yaml
  -> source governance registry

template_metadata_contract_registry.projection.json
  -> runtime-readable projection

template_contract_projection_audit.py
  -> detects drift

template_contract_release_gate.py
  -> blocks release/checkpoint readiness unless audit is ALIGNED
```

---

## 3. Gate verdicts

```text
ALLOW
BLOCK
```

Allowed only when:

```text
audit verdict == ALIGNED
```

Blocked when:

```text
SOURCE_MISSING
PROJECTION_MISSING
SOURCE_UNREADABLE
PROJECTION_UNREADABLE
MISMATCH
AUDIT_ERROR
```

---

## 4. Gate use

This gate should be called before:

```text
production contract-bound event scanning
checkpoint bundle release
runtime handoff packaging
default automation path widening
template contract projection regeneration acceptance
```

---

## 5. Receipt

Every gate evaluation may emit a receipt:

```yaml
template_contract_release_gate_receipt:
  gate_id:
  emitted_at:
  gate_name:
  audit_id:
  audit_verdict:
  allowed:
  blocked_reason:
  source_contract_count:
  projection_contract_count:
  mutation_allowed: false
```

---

## 6. Non-loss clauses

This protocol is invalid if interpreted to allow:

1. release/checkpoint readiness while contract projection audit is mismatched;
2. a JSON projection to supersede YAML source;
3. an audit error to be ignored;
4. gate success to imply constitutional ratification;
5. gate success to widen graph mutation authority;
6. gate failure to mutate either source or projection automatically.

---

## 7. Minimal tests

```text
test_release_gate_allows_aligned_projection
test_release_gate_blocks_missing_projection
test_release_gate_blocks_mismatch
test_release_gate_writes_receipt
test_project_release_gate_allows_current_seed
```
