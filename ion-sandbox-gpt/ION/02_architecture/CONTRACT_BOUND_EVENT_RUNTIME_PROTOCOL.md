# CONTRACT-BOUND EVENT RUNTIME PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-24  
**Authority posture:** A3 until reviewed  
**Workstream:** WS-06 continuation — Contract-bound event runtime  
**Purpose:** Bind Phase 1/Phase 2 of the Evented Template File Graph runtime to machine-readable template metadata contracts.

---

## 1. Controlling law

```text
No template-instantiated file may become an event source unless its template
has an active or explicitly allowed provisional metadata contract.
```

This protocol hardens the V10 evented graph chain. V10 proved the safe six-phase chain. V14 added metadata contract law and a validator. V15 binds the first runtime phases to contract status.

---

## 2. Runtime boundary

V15 affects:

```text
Phase 1 — Template Completion Event witness
Phase 2 — Template Reaction Selection witness
```

V15 does not widen:

```text
graph mutation
registry mutation
schedule mutation
agent activation
source file mutation
```

---

## 3. Contract gate

Before Phase 1 emits a Template Completion Event witness, the runtime must check:

```text
contract exists
contract structure validates
contract_status is ACTIVE_CONTRACT or allowed PROVISIONAL_CONTRACT
required fields are available
completion threshold is known
receipt requirement is known
```

If the contract is missing or inactive, the runtime emits a refusal/blocked witness instead of an event-ready witness.

---

## 4. Reaction gate

Before Phase 2 selects a reaction, the runtime must check:

```text
source event references a template_id
contract exists and allows eventing
requested reaction is in downstream_effects.allowed
requested reaction is not in downstream_effects.forbidden
review requirements are preserved
```

Forbidden or undeclared reactions must be deferred/refused rather than selected.

---

## 5. Contract-bound witness classes

```text
CONTRACT_BOUND_TEMPLATE_COMPLETION_EVENT
CONTRACT_BLOCKED_TEMPLATE_COMPLETION_EVENT
CONTRACT_BOUND_REACTION_SELECTION
CONTRACT_BLOCKED_REACTION_SELECTION
```

---

## 6. Non-loss clauses

This protocol is invalid if interpreted to allow:

1. missing contracts to event by default;
2. inactive contracts to event silently;
3. prose-derived reactions to bypass `downstream_effects.allowed`;
4. forbidden reactions to be selected;
5. contract validation to equal canon ratification;
6. Phase 2 selection to equal execution;
7. graph mutation before review/commit phases.

---

## 7. Minimal test guards

```text
test_contract_bound_completion_allows_active_contract
test_contract_bound_completion_blocks_missing_contract
test_contract_bound_completion_blocks_inactive_contract
test_contract_bound_reaction_allows_declared_reaction
test_contract_bound_reaction_defers_forbidden_reaction
test_contract_bound_reaction_defers_unknown_template
```
