# CONTRACT-BOUND EVENT INTEGRATION PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-24  
**Authority posture:** A3 until reviewed  
**Workstream:** WS-06 continuation — contract-bound Phase 1/Phase 2 integration  
**Purpose:** Integrate V15 contract gates into the original V10 Phase 1 and Phase 2 runtime modules.

---

## 1. Integration law

```text
The evented template file graph must treat template metadata contracts as the
runtime gate for template completion events and reaction selection whenever a
contract map is provided.
```

V15 introduced tested gate helpers. V16 wires those helpers into:

```text
ION/04_packages/kernel/template_completion_events.py
ION/04_packages/kernel/template_reaction_selection.py
```

---

## 2. Backward compatibility

The integration is deliberately conservative.

```text
If no template_contracts map is provided, existing V10 behavior remains available.
If a template_contracts map is provided, contract law is enforced.
```

This lets ION transition from inference-based eventing into contract-bound eventing without breaking older witness-only tests.

---

## 3. Phase 1 behavior

When `template_contracts` is provided to `KernelTemplateCompletionWatcher.scan()` or `discover_candidates()`:

```text
completed candidate
→ resolve template_id
→ check template metadata contract
→ allow event witness only if contract validates and allows eventing
→ otherwise classify candidate as BLOCKED_OR_REFUSED
```

Blocked candidates preserve refusal reason and contract metadata.

---

## 4. Phase 2 behavior

When `template_contracts` is provided to `KernelTemplateReactionSelector.select_from_workspace()` or `select_for_event_witness()`:

```text
event witness
→ resolve template_id
→ check reaction against template metadata contract
→ select only declared allowed reactions
→ refuse forbidden / undeclared / missing-contract reactions
```

Reaction selection remains dry-run.

---

## 5. Non-loss clauses

This protocol is invalid if interpreted to allow:

1. contract-bound mode to mutate graph truth;
2. missing contracts to event successfully;
3. undeclared reactions to be selected;
4. forbidden reactions to be selected;
5. completion witness generation to mean acceptance;
6. reaction selection to mean execution;
7. backward compatibility mode to be mistaken for final automation posture.

---

## 6. Next hardening step

V16 still accepts an in-memory `template_contracts` map. The next step should add a dependency-free registry loader for `template_metadata_contract_registry.yaml` or a generated JSON projection, then make contract-bound mode the default for watched automation paths.
