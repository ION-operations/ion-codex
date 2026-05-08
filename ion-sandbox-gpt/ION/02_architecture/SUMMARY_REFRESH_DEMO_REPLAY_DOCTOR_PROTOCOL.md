# SUMMARY REFRESH DEMO REPLAY DOCTOR PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-25  
**Authority posture:** A3 until reviewed  
**Purpose:** Provide a repeatable operator-facing doctor command for validating the complete summary-refresh demo replay path.

---

## 1. Problem

V27 added a replay CLI, but a repeated LAND replay against the live project root may correctly refuse to overwrite existing bounded graph-state files.

The doctor command resolves this by separating two checks:

```text
project-root smoke: run replay with no bounded commit
isolated full commit: run replay in a tiny fresh sandbox with bounded commit enabled
```

---

## 2. Required behavior

The doctor must:

```text
evaluate release readiness for the project root
run project-root no-commit replay
create an isolated fresh replay workspace
copy only the template contract projection into that workspace
run full LAND bounded-commit replay in the isolated workspace
write a doctor report
print a concise summary
```

---

## 3. Sandbox boundary

The isolated workspace lives under:

```text
ION/05_context/sandboxes/demo_replay_doctor/
```

It is intentionally small and contains only enough registry projection data to run the bounded demo path.

---

## 4. Safety boundary

The doctor may write:

```text
demo replay reports
summary-refresh demo artifacts
bounded graph-state files in isolated sandbox
doctor report
```

It may not:

```text
rewrite source summaries
mutate registries
mutate schedules
activate agents
claim global graph canon
overwrite existing bounded graph-state entries
```

---

## 5. Minimal test guards

```text
test_demo_replay_doctor_runs_project_smoke_and_isolated_full_commit
test_demo_replay_doctor_cli_prints_summary
test_demo_replay_doctor_report_has_two_modes
test_demo_replay_doctor_isolated_commit_does_not_touch_project_graph_state
test_release_readiness_requires_demo_replay_doctor_surface
```


---

## 6. Project-root smoke dispatch rule

The project-root smoke is non-dispatching. It may materialize replay evidence, but it must not attempt to re-dispatch an existing front-door queue item from a previous deterministic replay.
