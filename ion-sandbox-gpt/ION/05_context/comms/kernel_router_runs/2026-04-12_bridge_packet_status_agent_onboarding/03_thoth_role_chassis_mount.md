---
type: role_chassis_mount
template: ROLE_CHASSIS_MOUNT
created: 2026-04-12T12:55:19-04:00
status: COMPLETE
target_role: Thoth
chassis: Composer 2 in Cursor IDE
mount_posture: MOUNTED_DEGRADED
governing_packet: ION/05_context/comms/kernel_router_runs/2026-04-12_bridge_packet_status_agent_onboarding/01_task.md
---

# Role / Chassis Mount: Thoth On Composer 2

## Purpose

Record one current-phase mount for Thoth as the bounded evidence and research carrier
for the bridge packet family status workload.

## Carrier / Chassis

Composer 2 inside Cursor IDE as a cheap, high-throughput read-heavy support chassis.

## Requested Role or External State

Thoth.

## Governing Sources

- `ION/03_registry/boots/THOTH.boot.md`
- `ION/02_architecture/CODEX_LEAD_ORCHESTRATION_PROTOCOL.md`
- `ION/02_architecture/ION_OVER_CURSOR_PROTOCOL.md`
- `ION/02_architecture/ROLE_CHASSIS_MOUNT_PROTOCOL.md`
- `ION/02_architecture/TRUE_NAME_AND_SEMANTIC_LAYER_PROTOCOL.md`
- `ION/02_architecture/RANK_AND_PRECEDENCE_PROTOCOL.md`

## Bound Template Set

- `ION/07_templates/actions/TASK.md`
- `ION/07_templates/actions/ROLE_CHASSIS_MOUNT.md`
- `ION/07_templates/reports/RESEARCH.md`
- `ION/07_templates/reports/EVIDENCE.md`
- `ION/07_templates/actions/SIGNAL.md`
- `ION/07_templates/bindings/THOTH__RESEARCH.md`

## Read Set

- `ION/03_registry/boots/THOTH.boot.md`
- `ION/02_architecture/ROLE_CHASSIS_MOUNT_PROTOCOL.md`
- `ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md`
- `ION/04_packages/kernel/packet_validation.py`
- `ION/tests/test_kernel_packet_validation.py`
- the governing task, role session, and explicitly assigned bridge-packet surfaces

## Write Set

- `ION/06_intelligence/evidence/` for extracted evidence notes
- `ION/06_intelligence/research/` for bounded synthesis
- `ION/05_context/signals/` for Thoth-owned completion or blocker signals

## Mount Posture and Constraints

- posture: `MOUNTED_DEGRADED`
- Thoth is lawful on Composer 2 for this workload, but citations, extraction discipline,
  and downstream review must stay tighter than ordinary drafting work
- Thoth must not silently drift into architecture ownership or code mutation

## Expected Output / Review Trigger

- one bounded research or evidence artifact on bridge-packet status and validator
  coverage
- review or escalation if the packet-law question cannot be answered from the assigned
  surfaces and older estate evidence
