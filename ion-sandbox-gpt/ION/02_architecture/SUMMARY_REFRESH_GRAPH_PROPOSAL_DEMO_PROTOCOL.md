# SUMMARY REFRESH GRAPH PROPOSAL DEMO PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-25  
**Authority posture:** A3 until reviewed  
**Purpose:** Extend the summary-refresh release demo from projection-only Phase 3 into Phase 4 proposal-only graph writeback.

---

## 1. Demo spine

```text
User
  -> Persona Interface ingress
  -> Relay semantic-boundary packet
  -> Steward routing envelope / WorkUnit / dispatch
  -> demo.summary_refresh_request template file
  -> Phase 1 contract-bound completion event witness
  -> Phase 2 contract-bound dry-run reaction selection
  -> Phase 3 projection-only index surface
  -> Phase 4 proposal-only graph writeback surface
  -> Relay return package
  -> Persona response package
  -> User
```

---

## 2. Proposal boundary

Phase 4 may create proposed graph nodes and edges as reviewable proposal records.

It may not:

```text
commit graph state
mutate source graph truth
rewrite project summaries
mutate registries
mutate schedules
activate agents
claim final summary synthesis
```

---

## 3. Product-demo meaning

This proves that the front-door assistant can create a template-governed request and carry it through the first four evented-template graph phases.

It remains a proposal-only demo path. Later phases must handle review and bounded commit separately.

---

## 4. Minimal test guards

```text
test_summary_refresh_demo_runs_graph_proposal_phase
test_summary_refresh_demo_graph_proposal_is_non_mutating
test_summary_refresh_demo_receipt_records_proposal
test_summary_refresh_demo_return_mentions_proposal
test_release_readiness_requires_graph_proposal_demo_surface
```
