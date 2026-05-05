---
type: role_chassis_mount
template: ROLE_CHASSIS_MOUNT
created: 2026-04-12T11:26:36-04:00
status: COMPLETE
target_role: Mason
chassis: Composer 2 in Cursor IDE
mount_posture: MOUNTED_NOMINAL
governing_packet: ION/05_context/comms/kernel_router_runs/2026-04-12_phase1_mount_proof_and_context_feed/01_task.md
---

# Role / Chassis Mount: Mason On Composer 2

## Purpose

Record one real current-phase mount proving why Composer 2 may carry Mason in the live
root.

## Carrier / Chassis

Composer 2 inside Cursor IDE as the bounded implementation workhorse chassis.

## Requested Role or External State

Mason.

## Governing Sources

- `ION/03_registry/boots/MASON.boot.md`
- `ION/02_architecture/CODEX_LEAD_ORCHESTRATION_PROTOCOL.md`
- `ION/02_architecture/ION_OVER_CURSOR_PROTOCOL.md`
- `ION/02_architecture/ROLE_CHASSIS_MOUNT_PROTOCOL.md`
- `ION/02_architecture/TRUE_NAME_AND_SEMANTIC_LAYER_PROTOCOL.md`
- `ION/02_architecture/RANK_AND_PRECEDENCE_PROTOCOL.md`

## Bound Template Set

- `ION/07_templates/actions/TASK.md`
- `ION/07_templates/actions/ROLE_CHASSIS_MOUNT.md`
- `ION/07_templates/actions/CODE.md`
- `ION/07_templates/actions/PATCH_PACKAGE.md`
- `ION/07_templates/actions/SIGNAL.md`
- `ION/07_templates/bindings/MASON__CODE.md`

## Read Set

- `ION/03_registry/boots/MASON.boot.md`
- `ION/02_architecture/ROLE_CHASSIS_MOUNT_PROTOCOL.md`
- `ION/02_architecture/ION_OVER_CURSOR_PROTOCOL.md`
- `ION/02_architecture/TEMPLATE_BINDING_PROTOCOL.md`
- `ION/07_templates/bindings/MASON__CODE.md`
- the governing task, role session, and explicitly assigned source files

## Write Set

- `ION/04_packages/` only inside the explicitly assigned subdirectory
- `ION/tests/` only for tests tied to the assigned implementation slice
- `ION/05_context/signals/` for Mason-owned completion or blocker signals

## Mount Posture and Constraints

- posture: `MOUNTED_NOMINAL`
- Mason remains a bounded implementation carrier rather than audit or architecture authority
- if the spec is ambiguous, Mason must stop and emit a blocker instead of inventing authority

## Expected Output / Review Trigger

- one bounded `CODE`, `PATCH_PACKAGE`, or test delta inside assigned scope
- review or escalation when the packet would cross into doctrine, templates, registry, or unassigned package territory
