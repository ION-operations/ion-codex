# SUMMARY REFRESH DEMO REPLAY CLI PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-25  
**Authority posture:** A3 until reviewed  
**Purpose:** Provide a single-command replay surface for the complete six-phase summary-refresh demo.

---

## 1. Command purpose

The replay command must run the complete bounded demo path from one command:

```text
front-door -> template -> event -> reaction -> projection -> proposal -> review -> bounded commit -> persona return
```

and write a replay report containing the generated artifact paths.

---

## 2. Required behavior

The command must:

```text
infer or accept workspace root
load template contract projection
run SummaryRefreshDemoRunner
write a JSON replay report
print a concise human-readable path summary
return non-zero on failure
```

---

## 3. Safety boundary

The command may create the normal demo artifacts and bounded graph-state files under:

```text
ION/05_context/
```

It may not:

```text
rewrite source summaries
mutate registries
mutate schedules
activate agents
claim global graph canon
```

---

## 4. Review behavior

By default, the replay command uses:

```text
review_verdict: LAND
run_bounded_commit: true
```

Operators may run with:

```text
--review-verdict HOLD
--review-verdict ESCALATE
--no-commit
```

to prove non-commit behavior.

---

## 5. Minimal test guards

```text
test_demo_replay_cli_module_writes_report
test_demo_replay_cli_main_prints_artifact_summary
test_demo_replay_cli_hold_review_does_not_commit
test_demo_replay_cli_report_contains_six_phase_paths
test_release_readiness_requires_demo_replay_cli_surface
```


---

## 6. Repeat replay semantics

A LAND replay may refuse to overwrite existing bounded graph-state files. This is correct.

For project-root replay demonstrations where prior bounded graph-state artifacts may already exist, use:

```bash
--no-commit
```

to replay all phases through review and return/report generation without attempting a second bounded commit over existing graph-state entries.

Fresh workspaces still exercise the complete six-phase LAND commit path.


---

## 7. Repeat front-door queue semantics

For repeated deterministic project-root smokes, use:

```bash
--no-dispatch
```

to avoid attempting to dispatch a front-door queue item that may already have been dispatched by a previous replay.
