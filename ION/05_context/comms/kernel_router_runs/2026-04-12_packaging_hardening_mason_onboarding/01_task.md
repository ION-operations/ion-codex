---
type: task
agent: Mason
template: TASK
priority: P0
created: 2026-04-12T15:15:04-04:00
from: Codex
target: ION/05_context/comms/kernel_router_runs/2026-04-12_packaging_hardening_mason_onboarding/
status: ACTIVE
---

# Mission: Land Outsider-Grade Packaging Hardening

## Goal

Implement the minimum packaging/import/CLI surface needed so the active branch no longer
depends on mandatory manual `PYTHONPATH=ION/04_packages` wiring for basic use.

## Source / Context

- `ION/06_intelligence/orchestration/2026-04-12_current_generation_ratification_assessment.md`
- `ION/06_intelligence/research/2026-04-12_outsider_grade_packaging_hardening_next_workload_plan.md`
- `ION/06_intelligence/orchestration/2026-04-12_ion_acceptance_evidence_bundle_current_state.md`
- `ION/03_registry/boots/MASON.boot.md`
- `ION/07_templates/bindings/MASON__CODE.md`

## Requirements

- target packaging/import/CLI entry only
- keep kernel behavior unchanged
- add or adjust only the minimum metadata/import/test surfaces required
- leave a reproducible verification trail

## Deliverables

- bounded code/test implementation for packaging hardening
- one completion or blocker signal from Mason

## Constraints

- no doctrine, template, registry, or architecture edits
- no packet-law widening
- no bridge packet canon / validator widening
- no repacking of sibling roots outside this working branch

## Completion Signal

Emit one Mason signal naming the landed packaging surfaces and the exact verification
performed.
