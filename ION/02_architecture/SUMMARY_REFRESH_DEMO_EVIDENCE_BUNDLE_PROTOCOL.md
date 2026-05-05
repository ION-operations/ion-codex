# SUMMARY REFRESH DEMO EVIDENCE BUNDLE PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-25  
**Authority posture:** A3 until reviewed  
**Purpose:** Assemble a compact operator/shareable evidence bundle for the certified summary-refresh release demo.

A V30 evidence bundle packages certification, doctor, and replay evidence into:

```text
ION/05_context/history/demo_evidence_bundles/<bundle_id>/
```

It may copy reports and write a manifest/README. It may not rewrite source summaries, mutate registries, mutate schedules, activate agents, claim global graph canon, or ratify provisional A3 surfaces.

Command:

```bash
PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_evidence_bundle --workspace-root .
```
