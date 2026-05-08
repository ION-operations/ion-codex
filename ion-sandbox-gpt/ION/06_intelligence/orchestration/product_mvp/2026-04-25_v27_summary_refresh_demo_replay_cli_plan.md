# V27 Summary Refresh Demo Replay CLI Plan

**Date:** 2026-04-25  
**Purpose:** Add a one-command replay surface for the complete six-phase summary-refresh demo.

## Command

```bash
PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_replay --workspace-root .
```

## Path

```text
CLI
→ contract projection load
→ SummaryRefreshDemoRunner
→ front-door ingress
→ template request
→ completion witness
→ reaction selection
→ projection-only index surface
→ proposal-only graph writeback surface
→ governed review verdict surface
→ bounded graph-state commit
→ persona return
→ replay report
```

## Boundary

The command writes normal demo artifacts and a replay report. It does not rewrite source summaries, mutate registries, mutate schedules, activate agents, or claim global graph canon.


## Verification

```text
Ran 107 tests in 8.780s
OK
```

## Project-root replay smoke

```bash
PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_replay --workspace-root .
```

The smoke run produced a replay report under:

```text
ION/05_context/history/demo_replay_reports/
```


## Repeat project-root smoke

If the project root already contains bounded graph-state entries from earlier demo runs, replay with:

```bash
PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_replay --workspace-root . --no-commit
```

The full LAND bounded commit path is still tested in fresh temporary workspaces.
