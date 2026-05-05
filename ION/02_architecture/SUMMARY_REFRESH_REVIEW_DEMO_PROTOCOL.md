# SUMMARY REFRESH REVIEW DEMO PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-25  
**Authority posture:** A3 until reviewed  
**Purpose:** Extend the summary-refresh release demo from Phase 4 proposal-only graph writeback into Phase 5 governed review.

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
  -> Phase 5 governed review verdict surface
  -> Relay return package
  -> Persona response package
  -> User
```

---

## 2. Review boundary

Phase 5 may review the Phase 4 proposal and emit a LAND/HOLD/ESCALATE review verdict.

In the V25 demo path, the default review verdict is:

```text
LAND
```

but LAND means:

```text
accepted_for_later_graph_commit = true
```

It does **not** mean graph truth was committed.

---

## 3. Forbidden behavior

The V25 demo may not:

```text
commit graph state
mutate source graph truth
rewrite project summaries
mutate registries
mutate schedules
activate agents
claim final autonomous summary synthesis
```

---

## 4. Product-demo meaning

This proves that the front-door assistant can create a template-governed request and carry it through the first five evented-template graph phases.

The next logical phase would be a bounded Phase 6 commit into the demo graph-state surface, but that should be treated separately because it crosses from review into commit semantics.

---

## 5. Minimal test guards

```text
test_summary_refresh_demo_runs_review_phase
test_summary_refresh_demo_review_is_non_mutating
test_summary_refresh_demo_receipt_records_review
test_summary_refresh_demo_return_mentions_review
test_release_readiness_requires_review_demo_surface
```
