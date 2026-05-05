# SUMMARY REFRESH BOUNDED COMMIT DEMO PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-25  
**Authority posture:** A3 until reviewed  
**Purpose:** Extend the summary-refresh release demo from Phase 5 governed review into Phase 6 bounded graph-state commit.

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
  -> Phase 6 bounded graph-state commit
  -> Relay return package
  -> Persona response package
  -> User
```

---

## 2. Commit boundary

Phase 6 may commit LANDed review proposals into the bounded evented-template graph state:

```text
ION/05_context/graph/template_event_graph_state/
```

It may not:

```text
mutate source files
rewrite project summaries
mutate registries
mutate schedules
activate agents
claim final autonomous summary synthesis
```

---

## 3. LAND-only rule

Phase 6 may run only when a Phase 5 review verdict is:

```text
LAND
accepted_for_later_graph_commit: true
```

HOLD and ESCALATE must not commit. They remain review evidence.

---

## 4. Product-demo meaning

This proves the first complete six-phase evented-template chain behind the front door.

It is a bounded graph-state commit, not global graph canon and not source-summary mutation.

---

## 5. Minimal test guards

```text
test_summary_refresh_demo_runs_bounded_commit_phase
test_summary_refresh_demo_commit_writes_bounded_graph_state_only
test_summary_refresh_demo_hold_review_does_not_commit
test_summary_refresh_demo_receipt_records_commit
test_summary_refresh_demo_return_mentions_bounded_commit
test_release_readiness_requires_bounded_commit_demo_surface
```
