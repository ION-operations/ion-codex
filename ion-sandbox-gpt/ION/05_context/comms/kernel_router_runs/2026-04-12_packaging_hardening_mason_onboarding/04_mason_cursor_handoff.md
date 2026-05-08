---
type: cursor_handoff
template: CURSOR_HANDOFF
created: 2026-04-12T15:15:04-04:00
status: ACTIVE
target_surface: Composer 2 chat mounted as Mason
objective: Implement outsider-grade packaging hardening without changing kernel behavior
---

# Cursor Handoff: Mason Packaging Hardening

## Role / chassis target

Composer 2 chat mounted as Mason using the existing current-phase Mason posture.

## Load order

1. `ION/03_registry/boots/MASON.boot.md`
2. `ION/07_templates/bindings/MASON__CODE.md`
3. `ION/05_context/comms/kernel_router_runs/2026-04-12_packaging_hardening_mason_onboarding/03_mason_role_chassis_mount.md`
4. `ION/06_intelligence/orchestration/2026-04-12_current_generation_ratification_assessment.md`
5. `ION/06_intelligence/research/2026-04-12_outsider_grade_packaging_hardening_next_workload_plan.md`

## Exact files to read first

- `ION/06_intelligence/orchestration/2026-04-12_current_generation_ratification_assessment.md`
- `ION/06_intelligence/research/2026-04-12_outsider_grade_packaging_hardening_next_workload_plan.md`
- `ION/04_packages/kernel/operator_cli.py`
- `ION/04_packages/kernel/__init__.py`

## Task to perform

- scope: outsider-grade packaging hardening for the active working branch
- bounded step: implement the minimum packaging/import/CLI surface needed so the branch
  no longer depends on mandatory manual `PYTHONPATH=ION/04_packages` wiring for basic
  use, while keeping kernel behavior unchanged

## Boundaries

- no doctrine, architecture, registry, or template edits
- no bridge packet canon / validator widening
- no behavior redesign
- keep the write set bounded to packaging metadata, minimal import/entry adjustments,
  and directly related tests

## Expected output artifact

- one bounded Mason implementation pass plus one Mason completion or blocker signal
