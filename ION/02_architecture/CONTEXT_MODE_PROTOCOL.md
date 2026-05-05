---
type: protocol
authority: A3_OPERATIONAL
template: SPEC
created: 2026-04-07T23:05:00-04:00
status: ACTIVE_FIRST_PASS
connections:
  - ION/02_architecture/CONTINUITY_ARCHITECTURE.md
  - ION/02_architecture/CONTEXT_PLANES.md
  - ION/02_architecture/AGENT_REASONING_PROTOCOL.md
  - ION/02_architecture/MANIFEST_AND_ROUTE_STATE_PROTOCOL.md
  - ION/02_architecture/AUTOMATION_STATE_PROTOCOL.md
  - ION/06_intelligence/specs/T03_ContextPackageSchema.spec.md
  - ION/06_intelligence/specs/T04_ReasoningWindowSchema.spec.md
  - ION/05_context/comms/migration_ledgers/domain_semantic_runtime_migration.md
lineage:
  - SOS/02_architecture/CONTEXT_PROTOCOL.md
  - SOS-OPUS/02_architecture/CONTEXT_PROTOCOL.md
---

# CONTEXT MODE PROTOCOL

## Status

This protocol formalizes the live distinction between manual continuity mode and compiled context mode.
It is an operational bridge surface for the current root.
It does not claim that full daemon mode already exists in the live repository.

## 1. Why this layer exists

`CONTINUITY_ARCHITECTURE.md` already established the most important law:
private continuity is source, while root surfaces are curated projection.
What the live root still lacked was an explicit mode protocol saying how the organism behaves
when work is being carried manually versus when it is being carried by compiled runtime support.

That distinction matters because the same files do not mean the same thing in every operating mode.
Without an explicit mode layer, continuity state, route state, and automation state blur together.

## 2. Core law

### Law 1 — Context mode must be explicit

Every serious work cycle should be interpretable as operating in one declared context mode.
Silently mixing manual assumptions with daemon assumptions is drift.

### Law 2 — Manual continuity is not an inferior form of automation

Manual mode is a real governed operating mode.
It is not merely "automation absent."
It has its own lawful state surfaces, its own burdens, and its own constraints.

### Law 3 — Compiled context does not replace constitutional authority

When compiled context exists, it narrows visibility and packages state for execution.
It does not outrank doctrine, protocols, or registry truth.

### Law 4 — Switching modes does not widen authority on its own

A change in context mode may change transport, state handling, or compilation method.
It does not itself authorize broader writes, silent branch activation, or automation promotion.

### Law 5 — Projection surfaces must stay projection surfaces

Root projections such as `ION/MINI.md`, `ION/CAPSULE.md`, and `ION/STATUS.md`
remain witness/projection surfaces in manual mode.
They must not be quietly reinterpreted as daemon route-state files.

## 3. Active context modes

### Mode A — IDE / Manual Continuity Mode

This is the current default live mode.

Primary traits:
- source continuity lives in private role lanes
- root trio are curated witness surfaces
- inbox + signals coordinate handoff
- reasoning journals and CSR surfaces carry bounded reflection / confidence state
- the operator or a role steward performs integration explicitly

Primary state surfaces:
- `ION/agents/{role}/MINI.md`
- `ION/agents/{role}/CAPSULE.md`
- `ION/MINI.md`
- `ION/CAPSULE.md`
- `ION/STATUS.md`
- `ION/05_context/inbox/`
- `ION/05_context/signals/`

### Mode B — Compiled Context / Runtime-Assisted Mode

This is a target mode, not yet the default live operating reality.

Primary traits:
- a bounded context package is compiled for one step or work unit
- reasoning is carried through an explicit reasoning window or equivalent governed chamber
- route-state is tracked through manifest/branch state rather than through prose alone
- automation-stage visibility becomes explicit rather than inferred

Primary target surfaces:
- `ION/06_intelligence/specs/T03_ContextPackageSchema.spec.md`
- `ION/06_intelligence/specs/T04_ReasoningWindowSchema.spec.md`
- `ION/02_architecture/MANIFEST_AND_ROUTE_STATE_PROTOCOL.md`
- `ION/02_architecture/AUTOMATION_STATE_PROTOCOL.md`

## 4. Distinction map

| Surface | What it answers | What it is not |
|---|---|---|
| Private continuity | what this role knows about its own ongoing work | system-wide route-state |
| Root projection | what the organism is presenting as current witness | source continuity |
| Context package | what one execution step may see | long-lived continuity |
| Reasoning window / journal | how one bounded step is reasoned through | automation-stage record |
| Manifest / route-state | where the system is in governed traversal | private continuity narrative |
| Automation state | how much execution is manual, assisted, gated, or runtime-driven | route-state itself |

## 5. Manual mode obligations

When operating in IDE/manual continuity mode:

1. read and write private continuity in role-native lanes
2. treat root projections as witness, not source
3. keep the active template explicit when the step is non-trivial
4. use reasoning journals / CSR surfaces when drift, confidence, or escalation pressure is real
5. do not fabricate compiled route-state if the runtime layer is not actually active

## 6. Runtime-assisted mode obligations

When operating in compiled context mode:

1. the context package must define what is visible for the step
2. route-state must be machine-legible or equivalently structured
3. automation-state must be explicit and reviewable
4. any fallback to manual intervention must be recorded rather than hidden
5. private continuity and route-state must remain distinct even when both are updated in the same cycle

## 7. Mode transition rule

A transition between modes should be witnessed by at least one of the following:
- an explicit routing or handoff note
- a manifest / automation-state update
- a role MINI update that names the operating mode change
- a bounded report or reasoning journal that declares the mode assumptions

The important law is visibility, not ceremony.
A hidden mode switch is architectural drift.

## 8. Current live default

The live April 5 integrated root remains primarily in **IDE / Manual Continuity Mode**.
This protocol exists so future runtime support can be added without flattening the current law.

## 9. Non-claims

This protocol does **not** yet claim:
- a fully implemented daemon context compiler in the live root
- a final runtime manifest file path
- that every task requires a formal mode transition artifact
- that manual mode should disappear once runtime support grows
