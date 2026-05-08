# V29 Summary Refresh Demo Certification Gate Plan

**Date:** 2026-04-25  
**Purpose:** Add a single certification verdict over release readiness and replay doctor evidence.

## Command

```bash
PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_certification --workspace-root .
```

## Certification requirements

```text
release readiness is READY
project-root no-commit smoke passes
isolated full LAND bounded commit passes
isolated commit has >=1 commit, >=2 nodes, >=4 edges
forbidden mutation boundaries remain false
```

## Boundary

Certification means the demo is operator-demonstrable under current gates. It does not mean full product completion, global graph canon, source-summary rewrite authority, agent activation authority, or constitutional ratification.


## Verification

```text
Ran 117 tests in 31.408s
OK
```

## Project-root certification smoke

```bash
PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_certification --workspace-root .
```

The smoke run wrote a certification report under:

```text
ION/05_context/history/demo_certification_reports/
```
