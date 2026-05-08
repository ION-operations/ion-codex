---
type: template
template_name: ROLE_CHASSIS_MOUNT
created: 2026-04-12T11:26:36-04:00
status: ACTIVE_CURRENT_PHASE
phase_status: CURRENT_PHASE
bridge_status: PROVISIONAL_BRIDGE
canon_status: NOT_FINAL_CANON
---

# TEMPLATE — ROLE CHASSIS MOUNT

Use this when mounting, remounting, or explicitly holding an external carrier in an
unmounted state for one bounded lane of work.

## Required frontmatter

```yaml
---
type: role_chassis_mount
template: ROLE_CHASSIS_MOUNT
created: <ISO timestamp>
status: <ACTIVE|COMPLETE|SUPERSEDED>
target_role: <role name or EXTERNAL_UNMOUNTED>
chassis: <carrier or host>
mount_posture: <MOUNTED_NOMINAL|MOUNTED_DEGRADED|SEQUENTIAL_MULTI_ROLE|EXTERNAL_UNMOUNTED>
governing_packet: <task, role session, or handoff path>
---
```

## Required body sections

```markdown
# Role / Chassis Mount: <title>

## Purpose

## Carrier / Chassis

## Requested Role or External State

## Governing Sources

## Bound Template Set

## Read Set

## Write Set

## Mount Posture and Constraints

## Expected Output / Review Trigger
```

## Invariants

1. The mount must point to explicit governing sources.
2. The bound template set must be named.
3. Read and write scope must be explicit.
4. If the carrier is external and not yet mounted into a named role, say so plainly.
5. If a semantic identity record is missing, the packet should say which current-phase
   surfaces are carrying the mount instead.
6. A mount packet records carriage; it does not silently expand authority.
