# TEMPLATE METADATA CONTRACT PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-24  
**Authority posture:** A3 until reviewed  
**Workstream:** WS-06 — Template Metadata Contract Hardening  
**Purpose:** Define the machine-readable contract required before a template may participate in evented-template-file automation.

---

## 1. Controlling principle

```text
Automation-capable templates must declare their graph behavior explicitly.
```

A template is not automation-capable merely because it has headings or prose. It becomes automation-capable only when it declares:

```text
identity
file class
graph node type
graph region
authority class
allowed statuses
required fields
completion threshold
allowed reactions
forbidden reactions
receipt requirements
review requirements
scheduler / index / agent hooks where applicable
```

This prevents the evented-file graph from guessing behavior from free prose.

---

## 2. Contract status classes

```text
NO_CONTRACT
DRAFT_CONTRACT
PROVISIONAL_CONTRACT
ACTIVE_CONTRACT
RETIRED_CONTRACT
QUARANTINED_CONTRACT
```

Only `ACTIVE_CONTRACT` and explicitly allowed `PROVISIONAL_CONTRACT` templates may become event sources.

---

## 3. Minimum metadata contract

```yaml
template_metadata_contract:
  template_id:
  canonical_name:
  version:
  contract_status:
  file_class:
  graph_node_type:
  graph_region:
  authority_class:
  lifecycle:
    allowed_statuses: []
    draft_statuses: []
    complete_statuses: []
    terminal_statuses: []
  required_fields: []
  optional_fields: []
  completion_threshold:
    mode:
    required_fields: []
    additional_checks: []
  graph_mapping:
    node_id_strategy:
    node_id_field:
    edge_fields: []
    dependency_fields: []
    affected_region_fields: []
  downstream_effects:
    allowed: []
    forbidden: []
  reaction_hooks:
    index_update_hooks: []
    scheduler_hooks: []
    agent_activation_hooks: []
    registry_update_hooks: []
    graph_writeback_hooks: []
  review:
    required_reviewers: []
    review_depth:
    approval_required:
  receipts:
    receipt_required:
    receipt_classes: []
  safety:
    forbidden_reactions: []
    escalation_behavior:
    stale_behavior:
    contradiction_behavior:
```

---

## 4. Completion threshold law

Completion is template-specific.

A file reaches completion only when:

```text
template contract exists
contract status permits eventing
required fields are present
status is in complete_statuses
authority class is present
graph region is present
completion threshold passes
receipt path is available
```

Completion does not equal acceptance or graph truth.

---

## 5. Reaction law

A completed file may request only reactions declared in `downstream_effects.allowed`.

If a reaction is not declared allowed, it must be refused or escalated.

If a reaction appears in `forbidden`, it must be refused even if the file requests it.

---

## 6. Integration with V10 evented graph chain

The V10 chain should use metadata contracts in this order:

```text
Phase 1 Template Completion Event:
  use contract to classify and validate candidate completion

Phase 2 Reaction Selection:
  use contract allowed/forbidden downstream effects

Phase 3 Index Projection:
  use contract index hooks

Phase 4 Writeback Proposal:
  use contract graph mapping and graph_writeback_hooks

Phase 5 Review:
  use contract review requirements

Phase 6 Commit:
  commit only reviewed proposals from templates whose contract allowed graph writeback
```

---

## 7. Non-loss clauses

This protocol is invalid if interpreted to allow:

1. prose-only templates to trigger automation;
2. incomplete contracts to become active silently;
3. completion to mean acceptance;
4. allowed reactions to be inferred from file wording;
5. agent activation without an explicit hook;
6. registry update without an explicit hook and review;
7. graph writeback without contract mapping and review;
8. template contract edits without doctrine/template evolution governance.

---

## 8. Minimal test guards

```text
test_template_metadata_contract_protocol_exists
test_template_metadata_contract_registry_exists
test_contract_schema_required_fields
test_contract_validator_accepts_complete_contract
test_contract_validator_rejects_missing_required_fields
test_contract_validator_rejects_inactive_contract_for_eventing
test_known_v10_templates_have_seed_contracts
```
