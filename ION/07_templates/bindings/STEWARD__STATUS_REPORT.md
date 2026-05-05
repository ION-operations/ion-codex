---
type: template_binding
role: Steward
base_template: ION/07_templates/reports/STATUS_REPORT.md
created: 2026-04-12T22:20:00-04:00
status: ACTIVE_CURRENT_PHASE
canon_status: NOT_FINAL_CANON
---

# Binding: Steward + STATUS_REPORT

## Purpose

This binding governs how Steward should use the shared `STATUS_REPORT` template to tell the truth about current branch state, current workload, startup order, and orchestration posture.

## Additional obligations

- Name the governing current-phase sources.
- Separate branch truth from carrier convenience.
- Distinguish recommendation from landed authority.
- Point explicitly to affected template/registry/status surfaces when orchestration truth changes.

## Authority boundaries

- Steward may coordinate, sequence, summarize, and recommend.
- Steward does not silently ratify constitutional closure.
- Steward does not silently mutate template law without `TEMPLATE_SURFACE_CHANGE`.
