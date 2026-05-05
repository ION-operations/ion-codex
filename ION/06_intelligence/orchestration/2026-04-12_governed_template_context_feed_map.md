---
type: orchestration_map
authority: A3_OPERATIONAL
created: 2026-04-12T22:24:00-04:00
status: ACTIVE
purpose: >-
  Map which governed templates currently feed bounded context formation in the
  active branch, how they are classified, and where current-phase bridge status
  still applies.
connections:
  - ION/02_architecture/TEMPLATE_BINDING_PROTOCOL.md
  - ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md
  - ION/03_registry/current_phase_template_surface_registry.yaml
  - ION/05_context/comms/kernel_router_runs/2026-04-12_phase1_mount_proof_and_context_feed/06_context_bank_feed_proof.md
  - ION/07_templates/_MASTER.md
  - ION/06_intelligence/orchestration/2026-04-13_startup_template_feed_and_task_routing_defaults.md
---

# Governed Template Context-Feed Map

## Core thesis

ION is a governed-template system.

Templates are governed.
Governed templates feed bounded context formation.
Bounded context formation drives packetized lawful work.
Receipts, signals, handoffs, and review then reveal template sufficiency, drift,
or required bridging.

This file names the currently active template surfaces in that loop.

## Active startup-critical templates

These template classes are currently startup-critical for the active branch.

### 1. Task packetization
- `ION/07_templates/actions/TASK.md`
- status: `ACTIVE`
- function: bounded work packetization

### 2. Role-bounded execution pass
- `ION/07_templates/actions/ROLE_SESSION.md`
- status: `ACTIVE`
- function: one bounded role pass under packet law

### 3. Bounded transfer / handoff
- `ION/07_templates/actions/HANDOFF.md`
- status: `ACTIVE`
- origin: `RECOVERED_FROM_ESTATE`
- function: bounded transfer between carriers

### 4. IDE-targeted handoff
- `ION/07_templates/actions/CURSOR_HANDOFF.md`
- status: `ACTIVE`
- origin: `RECOVERED_FROM_ESTATE`
- function: IDE-specific bounded transfer

### 5. Patch/package return
- `ION/07_templates/actions/PATCH_PACKAGE.md`
- status: `ACTIVE`
- function: bounded external or cross-lane patch return

### 6. Signal pointer
- `ION/07_templates/actions/SIGNAL.md`
- status: `ACTIVE`
- function: state-change pointer and event surfacing

### 7. Auxiliary activation
- `ION/07_templates/actions/AGENT_SPAWN.md`
- status: `ACTIVE`
- origin: `RECOVERED_FROM_ESTATE`
- function: bounded auxiliary activation

## Current-phase bridge templates

These templates are active now but explicitly remain current-phase provisional bridges.

### 8. Role/chassis mount
- `ION/07_templates/actions/ROLE_CHASSIS_MOUNT.md`
- status: `ACTIVE_CURRENT_PHASE`
- canon posture: `PROVISIONAL_BRIDGE_NOT_FINAL_CANON`
- function: lawful role mount under current branch law
- paired protocol: `ION/02_architecture/ROLE_CHASSIS_MOUNT_PROTOCOL.md`
- provenance: `ION/06_intelligence/research/2026-04-12_role_chassis_mount_provenance_note.md`

### 9. Disagreement escalation
- `ION/07_templates/actions/DISAGREEMENT_ESCALATION.md`
- status: `ACTIVE_CURRENT_PHASE`
- canon posture: `PROVISIONAL_BRIDGE_NOT_FINAL_CANON`
- function: contradiction-preserving escalation routing
- paired protocol: `ION/02_architecture/DISAGREEMENT_ESCALATION_PROTOCOL.md`
- provenance: `ION/06_intelligence/research/2026-04-12_disagreement_escalation_provenance_note.md`

### 10. External return
- `ION/07_templates/actions/EXTERNAL_RETURN.md`
- status: `ACTIVE_CURRENT_PHASE`
- canon posture: `PROVISIONAL_BRIDGE_NOT_FINAL_CANON`
- function: browser/zip-class bounded external return
- paired protocol: `ION/02_architecture/EXTERNAL_ZIP_RETURN_BRIDGE_PROTOCOL.md`
- provenance: `ION/06_intelligence/research/2026-04-12_external_zip_return_bridge_provenance_note.md`

## Active report templates feeding the same loop

These report templates do not replace packet law, but they are active in the current branch because disagreement and research outputs must land in governed form.

- `ION/07_templates/reports/AUDIT.md`
- `ION/07_templates/reports/RESEARCH.md`
- `ION/07_templates/reports/PROPOSAL.md`

These are especially relevant when disagreement or evidence workloads are active.

## How the feed currently works

The current branch has already produced one explicit proof that governed templates feed bounded context formation.
That proof lives at:

- `ION/05_context/comms/kernel_router_runs/2026-04-12_phase1_mount_proof_and_context_feed/06_context_bank_feed_proof.md`

The practical feed chain is:

1. active doctrine and packet law define the workflow floor
2. active templates bind task, role session, handoff, and return surfaces
3. current-phase bridge templates carry mount, disagreement, and external return where needed
4. those governed surfaces feed bounded context materialization for a real packet
5. the packet is executed, returned, landed, and witnessed
6. receipts/signals/proofs reveal whether any template surface is stale, missing, or still provisional

## Status classes in this map

Use the registry language already adopted by the current branch:

- `ACTIVE` = current startup-critical governed surface
- `ACTIVE_SUPPORTING` = active support, but not center
- `ACTIVE_CURRENT_PHASE` = active current-phase bridge or bridge companion
- `STALE_FOR_STARTUP` = not current startup center even if historically important
- `RECOVERED_FROM_ESTATE` = restored from earlier lineage rather than invented fresh
- `PROVISIONAL_BRIDGE_NOT_FINAL_CANON` = lawful enough for current phase, not final constitutional closure

## Current decision rule

A template should be treated as startup-critical now only if it directly feeds one of these:

- packetization,
- bounded role pass,
- handoff,
- disagreement preservation,
- external return,
- or current-phase lawful mounting.

Templates outside that floor may still matter, but they do not automatically belong in startup center.


## Startup routing note

Use `ION/06_intelligence/orchestration/2026-04-13_startup_template_feed_and_task_routing_defaults.md` for the current sender/routing defaults that sit downstream of this template-feed floor.
