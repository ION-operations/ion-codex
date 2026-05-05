# SELF-DOCUMENTATION EVENT PIPELINE PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-24  
**Authority posture:** A3 until reviewed  
**Purpose:** Define the evented runtime path for creating and updating self-documentation records.

---

## 1. Pipeline

```text
FILE_DISCOVERED
→ FILE_CLASSIFIED
→ FILE_RECORD_CANDIDATE
→ FILE_RECORD_VALIDATED
→ APPROVED_CONTEXT_STATUS_ASSIGNED
→ APPROVED_CONTEXT_PROJECTION_UPDATED
→ GAP_REPORT_EMITTED where needed
→ RECEIPT_EMITTED
```

---

## 2. Safety boundary

This pipeline may update approved-context projections and emit receipts. It must not silently rewrite source doctrine, promote canon, or mutate registries without governed review.

---

## 3. Allowed reactions

```text
file_record_projection_update
approved_context_index_update
metadata_gap_warning
system_card_update_proposal
domain_map_update_proposal
quarantine_warning
specialist_review_request
```

---

## 4. Forbidden reactions

```text
silent_canon_promotion
source_file_rewrite
unreviewed_registry_mutation
public_claim_update
agent_authority_widening
```
