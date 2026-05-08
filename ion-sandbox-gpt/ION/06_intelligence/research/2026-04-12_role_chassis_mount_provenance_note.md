---
type: research
from: Codex
created: 2026-04-12T11:26:36-04:00
status: COMPLETE
phase_status: CURRENT_PHASE
bridge_status: PROVISIONAL_BRIDGE
canon_status: NOT_FINAL_CANON
topic: Provenance note for the current-phase role/chassis mount bridge
connections:
  - ION/02_architecture/ROLE_CHASSIS_MOUNT_PROTOCOL.md
  - ION/07_templates/actions/ROLE_CHASSIS_MOUNT.md
  - ION/02_architecture/ION_OVER_CURSOR_PROTOCOL.md
  - ION/02_architecture/TRUE_NAME_AND_SEMANTIC_LAYER_PROTOCOL.md
  - ION/02_architecture/RANK_AND_PRECEDENCE_PROTOCOL.md
  - ION/03_registry/boots/MASON.boot.md
  - ION/03_registry/boots/VESTIGE.boot.md
  - /home/sev/ION - Production/ION-BUILD/context/13_cognitive/2026-03-30_agent_spawn_and_context_dynamics.md
---

# Role / Chassis Mount Provenance Note

## Why this exists

Phase 1 required a current-phase mount bridge triple:

1. protocol
2. template
3. provenance note

The live branch already had mount-relevant surfaces, but no single current-phase bridge
that tied them together.

## Historical and live sources searched

- `ION/02_architecture/ION_OVER_CURSOR_PROTOCOL.md`
- `ION/02_architecture/CODEX_LEAD_ORCHESTRATION_PROTOCOL.md`
- `ION/02_architecture/TRUE_NAME_AND_SEMANTIC_LAYER_PROTOCOL.md`
- `ION/02_architecture/RANK_AND_PRECEDENCE_PROTOCOL.md`
- `ION/03_registry/boots/MASON.boot.md`
- `ION/03_registry/boots/VESTIGE.boot.md`
- `ION/03_registry/semantic_identities/README.md`
- `/home/sev/ION - Production/ION-BUILD/context/13_cognitive/2026-03-30_agent_spawn_and_context_dynamics.md`

## What was found

- The live branch already states that chassis is variable and roles may be mounted on
  different hosts.
- The live branch already has true-name, semantic, and rank/precedence rules.
- Mason and Vestige already have role-specific boot law with explicit chassis guidance.
- The older ION-BUILD spawn/context note already treated agent activation as a bounded
  context-envelope problem rather than a free-form conversation.
- No exact active `ROLE_CHASSIS_MOUNT` protocol or template existed in the current root.

## What is reused directly

- variable-chassis law from `ION_OVER_CURSOR_PROTOCOL.md`
- naming/rank constraints from `TRUE_NAME_AND_SEMANTIC_LAYER_PROTOCOL.md` and
  `RANK_AND_PRECEDENCE_PROTOCOL.md`
- role-specific carrier expectations from `MASON.boot.md` and `VESTIGE.boot.md`

## What is restated for current phase

- the explicit mount postures
- the rule that current-phase mount may be carried by boot + protocol + packet when a
  semantic identity record is not yet present
- the explicit `EXTERNAL_UNMOUNTED` default for browser ChatGPT in this rollout

## Why this remains provisional

- Mason and Vestige do not yet have full semantic identity records in the live root
- the branch lacks a final constitutional staffing law
- the current bridge is meant to stop drift now, not to close the total ontology

## Non-claims

- This note does not claim final naming ratification.
- This note does not claim every chassis-role pairing is now lawful by default.
- This note does not claim browser ChatGPT has a settled active role mount.
