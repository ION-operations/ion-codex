---
type: role_chassis_mount
template: ROLE_CHASSIS_MOUNT
created: 2026-04-12T11:26:36-04:00
status: COMPLETE
target_role: EXTERNAL_UNMOUNTED
chassis: browser ChatGPT with uploaded zip or VM snapshot
mount_posture: EXTERNAL_UNMOUNTED
governing_packet: ION/05_context/comms/kernel_router_runs/2026-04-12_phase1_mount_proof_and_context_feed/01_task.md
---

# Role / Chassis Mount: browser ChatGPT As External Unmounted Carrier

## Purpose

Record one real current-phase packet proving that browser ChatGPT is external and
unmounted by default in the live root.

## Carrier / Chassis

browser ChatGPT operating on an uploaded workspace zip or VM snapshot outside the live
branch.

## Requested Role or External State

`EXTERNAL_UNMOUNTED`.

## Governing Sources

- `ION/02_architecture/ROLE_CHASSIS_MOUNT_PROTOCOL.md`
- `ION/02_architecture/EXTERNAL_ZIP_RETURN_BRIDGE_PROTOCOL.md`
- `ION/02_architecture/EXTERNAL_EXECUTION_MCP_BRIDGE_PROTOCOL.md`
- `ION/AGENT_CONTRACT.md`
- `ION/01_doctrine/CANONICAL_WORKFLOW.md`

## Bound Template Set

- `ION/07_templates/actions/TASK.md`
- `ION/07_templates/actions/ROLE_CHASSIS_MOUNT.md`
- `ION/07_templates/actions/EXTERNAL_RETURN.md`
- `ION/07_templates/actions/PATCH_PACKAGE.md`
- `ION/07_templates/actions/HANDOFF.md`
- `ION/07_templates/actions/SIGNAL.md`

## Read Set

- the governing task, role session, or handoff packet
- the uploaded workspace snapshot or zip
- exact bounded source surfaces named by the governing packet

## Write Set

- external snapshot only
- returned packet artifacts only
- no direct write to the live branch

## Mount Posture and Constraints

- posture: `EXTERNAL_UNMOUNTED`
- the carrier may perform bounded work under packet law but does not gain active named-role status by default
- returned work remains witness until compared and landed by the live branch owner

## Expected Output / Review Trigger

- one bounded `EXTERNAL_RETURN` packet and any companion `PATCH_PACKAGE`, `HANDOFF`, or `SIGNAL`
- escalation if the requested work would require silent live-branch mutation, hidden merge, or authority beyond the governing packet
