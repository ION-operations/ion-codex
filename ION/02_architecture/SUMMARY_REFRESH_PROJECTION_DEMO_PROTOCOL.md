# SUMMARY REFRESH PROJECTION DEMO PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-25  
**Authority posture:** A3 until reviewed  
**Purpose:** Extend the V22 summary-refresh demo from Phase 1/Phase 2 witnesses into Phase 3 projection-only index output.

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
  -> Relay return package
  -> Persona response package
  -> User
```

---

## 2. Projection boundary

Phase 3 may materialize a separate projection-only index surface for projection-safe reactions.

It may not:

```text
mutate source graph truth
rewrite project summaries
mutate registries
mutate schedules
activate agents
claim a final summary was produced
```

---

## 3. Product-demo meaning

This proves that the front-door assistant can create a template-governed request and carry it through the first three evented-template graph phases.

It does not yet prove full source-summary synthesis. That belongs to a later governed write / projection-consumption phase.

---

## 4. Minimal test guards

```text
test_summary_refresh_demo_runs_projection_phase
test_summary_refresh_demo_projection_is_non_mutating
test_summary_refresh_demo_return_mentions_projection
test_release_readiness_requires_projection_demo_surface
```
