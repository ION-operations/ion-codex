---
type: role_chassis_mount
template: ROLE_CHASSIS_MOUNT
created: 2026-04-12T15:15:04-04:00
status: COMPLETE
target_role: Mason
chassis: Composer 2 in Cursor IDE
mount_posture: MOUNTED_NOMINAL
governing_packet: ION/05_context/comms/kernel_router_runs/2026-04-12_packaging_hardening_mason_onboarding/01_task.md
---

# Role / Chassis Mount: Mason On Composer 2 For Packaging Hardening

## Purpose

Record one bounded implementation mount for Mason on the next selected stabilization
slice.

## Carrier / Chassis

Composer 2 inside Cursor IDE as the primary bounded implementation workhorse.

## Requested Role or External State

Mason.

## Governing Sources

- `ION/03_registry/boots/MASON.boot.md`
- `ION/07_templates/bindings/MASON__CODE.md`
- `ION/02_architecture/CODEX_LEAD_ORCHESTRATION_PROTOCOL.md`
- `ION/02_architecture/ROLE_CHASSIS_MOUNT_PROTOCOL.md`

## Bound Template Set

- `ION/07_templates/actions/TASK.md`
- `ION/07_templates/actions/ROLE_CHASSIS_MOUNT.md`
- `ION/07_templates/actions/CURSOR_HANDOFF.md`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/actions/SIGNAL.md`
- `ION/07_templates/bindings/MASON__CODE.md`

## Read Set

- `ION/03_registry/boots/MASON.boot.md`
- `ION/07_templates/bindings/MASON__CODE.md`
- `ION/06_intelligence/orchestration/2026-04-12_current_generation_ratification_assessment.md`
- `ION/06_intelligence/research/2026-04-12_outsider_grade_packaging_hardening_next_workload_plan.md`
- `ION/04_packages/kernel/operator_cli.py`
- `ION/04_packages/kernel/__init__.py`

## Write Set

- branch-root packaging metadata if required by the slice
- `ION/04_packages/kernel/` only for packaging/import entry adjustments required by the slice
- `ION/tests/` only for packaging/import/CLI entry verification tied to the slice
- `ION/agents/mason/`
- `ION/05_context/signals/`

## Mount Posture and Constraints

- posture: `MOUNTED_NOMINAL`
- Mason owns bounded implementation execution only
- Mason must not drift into doctrine, template, registry, or architecture edits
- Mason must not widen packet canon or validator law while doing this slice

## Expected Output / Review Trigger

- one bounded packaging hardening patch with reproducible verification
- or one blocker signal if packaging cannot be improved without architecture or law changes
