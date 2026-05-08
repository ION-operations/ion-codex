# SUMMARY REFRESH DEMO CERTIFICATION GATE PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-25  
**Authority posture:** A3 until reviewed  
**Purpose:** Certify the complete summary-refresh release demo from readiness and doctor evidence.

---

## 1. Certification law

```text
A demo is certifiable only when readiness is READY and the doctor proves both
project-root replay safety and isolated full bounded-commit execution.
```

V28 made the demo repeatably testable. V29 makes that evidence consumable as a single certification verdict.

---

## 2. Required evidence

Certification requires:

```text
release readiness: READY / allowed
project-root doctor smoke: passed with 0 bounded commits
isolated doctor full commit: passed with >=1 bounded commit
isolated committed nodes: >=2
isolated committed edges: >=4
mutation boundaries: source/registry/schedule/agent mutation false
```

---

## 3. Verdicts

```text
CERTIFIED
BLOCKED
```

`CERTIFIED` means the bounded demo path is operator-demonstrable under current gates.

It does **not** mean:

```text
full product completion
global graph canon
source-summary rewrite authority
agent activation authority
constitutional ratification of provisional A3 surfaces
```

---

## 4. Command

```bash
PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_certification --workspace-root .
```

---

## 5. Report

The command writes:

```text
ION/05_context/history/demo_certification_reports/
```

---

## 6. Minimal test guards

```text
test_demo_certification_current_project_certified
test_demo_certification_cli_prints_summary
test_demo_certification_report_contains_doctor_evidence
test_demo_certification_blocks_when_doctor_skips_isolated_commit
test_release_readiness_requires_demo_certification_surface
```
