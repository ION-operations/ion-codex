---
type: role_chassis_mount
template: ROLE_CHASSIS_MOUNT
created: 2026-04-12T22:31:00-04:00
status: COMPLETE
target_role: STEWARD
chassis: Codex IDE in Cursor
mount_posture: MOUNTED_NOMINAL
governing_packet: ION/05_context/comms/kernel_router_runs/2026-04-12_steward_truename_and_template_alignment/00_trace.md
---

# Role / Chassis Mount: Steward over Codex carrier

## Purpose
Record that current-phase orchestration truth is Steward while the common active chassis remains Codex IDE in Cursor.

## Carrier / Chassis
Codex IDE in Cursor

## Requested Role or External State
Steward

## Governing Sources
- `ION/03_registry/boots/STEWARD.boot.md`
- `ION/03_registry/semantic_identities/STEWARD.semantic.yaml`
- `ION/03_registry/semantic_identities/CODEX.semantic.yaml`
- `ION/02_architecture/ROLE_CHASSIS_MOUNT_PROTOCOL.md`

## Bound Template Set
- `STEWARD__TASK`
- `STEWARD__STATUS_REPORT`
- `STEWARD__PROPOSAL`

## Read Set
- current startup and orchestration surfaces

## Write Set
- orchestration/status maps

## Mount Posture and Constraints
Mounted nominally for current-phase orchestration only. This does not erase Codex as carrier alias or historical construction lane.

## Expected Output / Review Trigger
Updated startup/orchestration truth surfaces reflecting Steward role truth and Codex carrier posture.
