# V28 Summary Refresh Demo Replay Doctor Plan

**Date:** 2026-04-25  
**Purpose:** Add an operator doctor command that validates the replay demo in two safe modes.

## Command

```bash
PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_doctor --workspace-root .
```

## Two-mode validation

```text
project-root smoke:
  replay full path through review/report with --no-commit semantics

isolated full commit:
  create tiny sandbox under ION/05_context/sandboxes/demo_replay_doctor/
  copy template contract projection
  run full LAND bounded commit path
```

## Boundary

The project root is never asked to overwrite existing bounded graph-state entries. Full bounded commit is proven inside a fresh isolated workspace.


## Verification

```text
Ran 112 tests in 18.112s
OK
```

## Project-root doctor smoke

```bash
PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_doctor --workspace-root .
```

The smoke run wrote a doctor report under:

```text
ION/05_context/history/demo_replay_doctor_reports/
```
