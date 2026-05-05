# RUNTIME STATE BINDING PROTOCOL

## Purpose

Bind machine-readable runtime state to real live-kernel events without claiming that continuity prose, capsule narration, or daemon autonomy are the same thing.

This protocol defines the lawful event edges for C2:
- governed-write evaluation / application
- capsule PRE capture
- capsule POST capture

## Core law

1. Continuity remains continuity.
2. Route-state remains route-state.
3. Automation-state remains automation-state.
4. Event binding may update route-state and automation-state, but it may not silently promote capsule prose into authority.
5. Invalid runtime posture must be recorded truthfully, not persisted as if valid.

## Event classes

### 1. Governed-write binding

A governed-write event may upsert:
- one `automation_state` record for the bounded scope
- one `manifest_route_state` record for the same bounded scope

The binding must reflect:
- threshold evaluation
- route compatibility
- authority compatibility
- whether the write was actually applied

If the requested posture is illegal, the persisted state must normalize to a lawful witness posture such as `SUSPENDED` rather than storing an impossible `RUNTIME_ACTIVE` claim in manual context.

### 2. Capsule PRE binding

A PRE capsule may upsert:
- route-state in planning posture
- automation-state for the declared current stage

This is a witness of intended operational posture, not proof that work was executed.

### 3. Capsule POST binding

A POST capsule may upsert:
- route-state in delivery / handoff posture
- automation-state with updated pending action / handoff posture

This is still not a global autonomous runtime claim.

## Scope rules

Bindings must remain scope-local.
Recommended first scopes:
- `WORK_UNIT`
- `LANE`
- `WORKFLOW`

Bindings must not create a hidden global singleton manifest.

## Invalid-posture handling

If an event requests a posture that violates live law, the binding layer must:
- preserve the contradiction as a blocker / gate
- downgrade the persisted posture to a lawful witness state
- keep the contradiction visible in machine-readable blockers or gates

## Minimum persisted outputs

Every binding should preserve:
- source event identity
- mission / objective anchor
- current or derived automation stage
- blockers and gates
- next route proposal or pending action
- linkage between route-state and automation-state

## Non-goals

This protocol does not establish:
- a general automation runner
- autonomous background execution
- automatic authority elevation for markdown continuity files
- a final graph-complete runtime controller

## Runtime/session clarification

Runtime-state binding may witness session-related facts and persist lawful
derived posture.
It does **not** create runtime session identity, queue ownership, or API carrier
entry permission.
Those authority surfaces now remain explicitly governed by the emitted Lane C
runtime/session trio.
