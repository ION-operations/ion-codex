---
type: protocol
authority: A3_OPERATIONAL
template: SPEC
created: 2026-04-12T11:26:36-04:00
status: ACTIVE_CURRENT_PHASE
phase_status: CURRENT_PHASE
bridge_status: PROVISIONAL_BRIDGE
canon_status: NOT_FINAL_CANON
connections:
  - ION/01_doctrine/CANONICAL_WORKFLOW.md
  - ION/AGENT_CONTRACT.md
  - ION/02_architecture/ION_OVER_CURSOR_PROTOCOL.md
  - ION/02_architecture/CODEX_LEAD_ORCHESTRATION_PROTOCOL.md
  - ION/02_architecture/TRUE_NAME_AND_SEMANTIC_LAYER_PROTOCOL.md
  - ION/02_architecture/RANK_AND_PRECEDENCE_PROTOCOL.md
  - ION/03_registry/boots/MASON.boot.md
  - ION/03_registry/boots/VESTIGE.boot.md
  - ION/07_templates/actions/ROLE_CHASSIS_MOUNT.md
  - ION/06_intelligence/research/2026-04-12_role_chassis_mount_provenance_note.md
---

# Role / Chassis Mount Protocol

## Purpose

Define the minimum current-phase law for how a live chassis becomes a lawful carrier of
an ION role in the active root.

This bridge exists because the live branch already has:

- boots
- rank and semantic law
- Cursor / subagent chassis law
- active role topology

but did not yet have one explicit current-phase mount protocol tying those surfaces
together.

## Core law

1. Template and packet law outrank chassis preference.
2. A chassis does not become a role merely because the operator intends it.
3. A lawful mount requires explicit governing sources, a bound template set, bounded
   read/write scope, and an expected output family.
4. If a stronger semantic or registry identity exists, use it.
5. If no semantic identity record exists yet for a live role, the active boot plus
   protocol and packet assignment may carry the current-phase mount.
6. A mount packet records a carrier decision. It does not silently transfer higher
   authority than the governing law already allows.

## Required mount inputs

A lawful current-phase mount should point to all of the following:

- the target role or explicit `EXTERNAL_UNMOUNTED` state
- the chassis being mounted
- the governing boot and any semantic/rank surfaces available
- the bound template or template flow
- the bounded read set
- the bounded write set
- the governing task, role session, or handoff
- the expected output family

## Mount postures

### `MOUNTED_NOMINAL`

Use when the chassis matches the role deeply enough to carry the role under ordinary
current-phase discipline.

### `MOUNTED_DEGRADED`

Use when the role is still lawful on the chosen chassis but requires smaller diffs,
clearer packets, tighter provenance, or stronger downstream review.

### `SEQUENTIAL_MULTI_ROLE`

Use when one operator chain is explicitly switching hats in sequence and private
continuity remains per role.

### `EXTERNAL_UNMOUNTED`

Use when an external carrier may perform bounded work under packet law but has not yet
been granted a settled active role mount in the live branch.

## Current default current-phase interpretations

### Mason

Mason may be mounted on Composer 2 under current branch law because:

- `MASON.boot.md` explicitly names Composer 2 as the primary workhorse model
- `CODEX_LEAD_ORCHESTRATION_PROTOCOL.md` treats Mason as the bounded implementation role
- `ION_OVER_CURSOR_PROTOCOL.md` already allows variable chassis and bounded context packages
- `MASON__CODE.md` binds Mason to the shared `CODE` template law

### Vestige

Vestige may be mounted on Composer 2 under current branch law because:

- `VESTIGE.boot.md` explicitly names Composer 2 as the persistent low-cost excavation chassis
- `ARCHAEOLOGY_DAEMON_PROTOCOL.md` and `CODEX_LEAD_ORCHESTRATION_PROTOCOL.md` place Vestige in the archaeology lane
- broad read access plus narrow write lane are already explicit in the boot

### browser ChatGPT

browser ChatGPT remains `EXTERNAL_UNMOUNTED` by default in the current root until a
lawful mount packet plus stronger current-phase evidence says otherwise.

It may still operate as a bounded external carrier through the external-return bridge
surfaces without being silently promoted into an active named role.

## Required packet law

Any material mount or remount should be recorded through:

- one `ROLE_CHASSIS_MOUNT` packet
- one governing `TASK`, `ROLE_SESSION`, or `HANDOFF`
- one short `SIGNAL` when the mount matters operationally

## Fresh-session proof rule

A fresh session should be able to answer all of the following from file-visible sources:

- why this chassis is carrying this role
- whether the posture is nominal, degraded, sequential, or external-unmounted
- which templates govern the work
- what the read/write boundaries are
- what output family the carrier owes next

If a fresh session cannot do that, the mount is not yet lawful enough for current-phase
trust.

## Non-goals

- no final constitutional staffing law
- no forced semantic activation of deeper names
- no claim that every live role already has a full semantic identity record
- no claim that an external carrier becomes trusted merely by returning useful work
