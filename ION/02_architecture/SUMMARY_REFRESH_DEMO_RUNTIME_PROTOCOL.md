# SUMMARY REFRESH DEMO RUNTIME PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-25  
**Authority posture:** A3 until reviewed  
**Purpose:** Define the first narrow release-demo path proving ION as an evented living context graph behind a front-door assistant interaction.

---

## 1. Demo spine

```text
User
  -> Persona Interface ingress
  -> Relay semantic-boundary packet
  -> Steward routing envelope / WorkUnit / dispatch
  -> summary-refresh template file
  -> template completion event witness
  -> contract-bound reaction selection
  -> Relay return package
  -> Persona response package
  -> User
```

---

## 2. Boundary

The demo path is proof of runtime continuity and lawful routing. It is not a full autonomous summarizer yet.

It may:

```text
materialize front-door boundary artifacts
create a bounded summary-refresh request template file
emit a Phase 1 completion witness
emit a Phase 2 dry-run reaction selection witness
emit receipts
prepare a controlled return package
```

It may not:

```text
rewrite source summaries
mutate the source graph directly
promote new doctrine
activate agents
claim final product completion
```

---

## 3. Contract requirement

The summary-refresh template type is:

```text
demo.summary_refresh_request
```

It must have a template metadata contract in both:

```text
ION/03_registry/template_metadata_contract_registry.yaml
ION/03_registry/template_metadata_contract_registry.projection.json
```

The projection audit/release gate must remain aligned.

---

## 4. Minimal test guards

```text
test_summary_refresh_demo_runs_front_door_to_evented_path
test_summary_refresh_demo_is_contract_bound
test_summary_refresh_demo_emits_persona_return
test_summary_refresh_contract_projection_is_aligned
test_release_readiness_requires_summary_refresh_demo_surface
```
