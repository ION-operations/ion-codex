# RELEASE READINESS GATE PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-24  
**Authority posture:** A3 until reviewed  
**Workstream:** Release/checkpoint validation composition  
**Purpose:** Compose current critical validation gates into one release/checkpoint readiness decision.

---

## 1. Controlling law

```text
A continuation artifact should not be treated as release/checkpoint-ready until
its key governance, contract, approved-context, and event-runtime surfaces are
present and aligned.
```

V19 created a release gate for template contract source/projection alignment. V20 composes that with the other current hardening surfaces.

---

## 2. Current V20 readiness checks

The composed gate checks:

```text
1. Template contract release gate is allowed.
2. V10 evented-template graph kernel modules exist.
3. V10 evented-template graph tests exist.
4. V11 doctrine-evolution governance receipt exists.
5. V12 approved-context seed registry exists.
6. V13 context graph ontology adapter exists.
7. V14/V17 template contract registry and projection exist.
8. V18 projection audit receipt exists.
9. V19 release-gate receipt exists.
```

---

## 3. Verdicts

```text
READY
BLOCKED
```

`READY` means current release/checkpoint evidence is present. It does **not** mean the whole ION product is complete, constitutional law is fully ratified, or every repository file is classified.

`BLOCKED` means at least one required readiness check failed.

---

## 4. Scope

The release readiness gate is suitable before:

```text
packaging a continuation zip
promoting a bounded checkpoint
running production contract-bound automation
handing the artifact to another executor
declaring a release candidate
```

---

## 5. Required receipt

Every gate evaluation may emit:

```yaml
release_readiness_receipt:
  gate_id:
  emitted_at:
  verdict:
  allowed:
  failed_checks: []
  passed_checks: []
  warnings: []
  mutation_allowed: false
```

---

## 6. Non-loss clauses

This protocol is invalid if interpreted to allow:

1. release readiness to imply full product completion;
2. readiness to bypass doctrine-evolution review;
3. readiness to mutate graph state, registries, schedules, source files, or agents;
4. readiness to ignore failed contract projection alignment;
5. readiness to treat provisional A3 surfaces as ratified A1 law;
6. readiness to replace detailed test execution.

---

## 7. Minimal tests

```text
test_release_readiness_current_project_ready
test_release_readiness_blocks_missing_contract_projection
test_release_readiness_blocks_missing_doctrine_receipt
test_release_readiness_writes_receipt
test_release_readiness_is_non_mutating
```
