# APPROVED CONTEXT INDEX PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-24  
**Authority posture:** A3 until reviewed  
**Purpose:** Define how ION distinguishes approved context from raw files, witnesses, drafts, stale surfaces, and historical lineage.

---

## 1. Approved context is a verdict

A file is not approved context by presence. It requires a context verdict.

A context verdict answers:

```text
Can this file be loaded?
For what scope?
Under what authority posture?
With what caveats?
For which agent/graph region?
Until when?
```

---

## 2. Approved context entry schema

```yaml
approved_context_entry:
  entry_id:
  file_path:
  graph_node_id:
  context_scope: []
  approved_for: []
  approved_context_status:
  authority_status:
  operational_status:
  epistemic_status:
  retrieval_zone:
  owner_agent_family:
  reviewer_agent_family:
  approval_basis:
  approval_receipt:
  stale_after:
  contradictions: []
  notes: []
```

---

## 3. Approved-for classes

```text
doctrine_read
runtime_boot
template_execution
role_context
donor_lineage
recovery
public_explanation
implementation_mapping
test_guard
product_mvp
```

---

## 4. Loading rule

```text
A context package may include only files whose approved_context_status,
retrieval_zone, and approved_for scope are compatible with the current task,
authority class, agent role, and graph region.
```

If the file is historical, stale, witness, or provisional, the context package must preserve that posture.

---

## 5. Projection rule

The approved context index is a projection. It is not source truth and not the whole graph.

It must be rebuildable from:

```text
ion_file_records
registries
receipts
authority surfaces
runtime status
review verdicts
```

---

## 6. Evented update rule

A completed `ION_FILE_RECORD`, `APPROVED_CONTEXT_ENTRY`, or `SELF_DOCUMENTATION_GAP_REPORT` may trigger:

```text
approved_context_projection_update
metadata_gap_warning
specialist_review_request
domain_map_update_proposal
system_card_update_proposal
quarantine_warning
```

Every outcome must emit a receipt.
