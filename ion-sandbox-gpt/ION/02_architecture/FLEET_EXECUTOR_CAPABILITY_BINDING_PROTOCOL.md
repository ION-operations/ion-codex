---
type: protocol
authority: A2_ARCHITECTURE
created: 2026-04-15T00:00:00+00:00
status: ACTIVE
purpose: Bind factual fleet membership witness into explicit executor capability records without importing swarm or hidden heuristics
connections:
  - ION/02_architecture/EXECUTOR_FLEET_LIFECYCLE_PROTOCOL.md
  - ION/02_architecture/EXECUTOR_CAPABILITY_REGISTRY_PROTOCOL.md
  - ION/02_architecture/LAWFUL_ORCHESTRATION_SCHEDULER_PROTOCOL.md
---

# Fleet → Executor Capability Binding Protocol

## Purpose

ION requires an explicit bridge between:

1) **Fleet membership witness** (which members exist and their lifecycle state), and  
2) **Executor capability registry** (which executors are selectable and under what constraints).

This bridge exists so scheduler surfaces can select executors based on explicit capability records
rather than hidden heuristics or log inference.

## Boundary law

- Fleet lifecycle does **not** define capability truth.
- Capability registry does **not** invent fleet membership.
- This binding surface materializes capability records from factual fleet membership state.

This protocol explicitly rejects “autonomous swarm” creep: it is a mapping bridge, not an orchestrator.

## Canonical mapping (minimal)

A minimal binding MAY map fleet member state to executor availability as:

- `BOOTING` → `DEGRADED`
- `ACTIVE` → `AVAILABLE`
- `SUSPENDED` → `DRAINED`
- `TERMINATED` → `UNAVAILABLE`

The binding may use stable identifiers:

- `executor_id := member_id`
- `capability_id := "cap-" + member_id`

These are implementation conventions, but they preserve true-name discipline and ensure repeatability.

## Receipts

Binding must emit receipts that state:
- which fleet was bound,
- how many members were observed,
- which capability IDs were created or updated,
- and any warnings (e.g., empty fleet).

## Non-goals

This protocol does **not** define:
- mission control,
- swarm cycles,
- pubsub/event busses,
- or activation authority.

It is strictly a witness-to-registry bridge.
