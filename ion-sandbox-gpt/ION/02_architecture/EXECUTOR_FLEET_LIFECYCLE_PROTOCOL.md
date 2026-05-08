---
type: protocol
authority: A2_ARCHITECTURE
created: 2026-04-15T00:00:00+00:00
status: ACTIVE
purpose: Define the minimal fleet-lifecycle witness center (spawn/suspend/terminate/heartbeat/stale discipline) without importing swarm mythology or server shells
connections:
  - ION/02_architecture/ACTIVATION_AUTHORITY_PROTOCOL.md
  - ION/02_architecture/EXECUTOR_LIFECYCLE_PROTOCOL.md
  - ION/02_architecture/EXECUTOR_CAPABILITY_REGISTRY_PROTOCOL.md
  - ION/02_architecture/RUNTIME_STATE_REPORTING_PROTOCOL.md
---

# Executor Fleet Lifecycle Protocol

## Short thesis

ION needs a **fleet lifecycle** witness surface.

This surface tracks the existence and basic lifecycle of *executor members* (spawn, heartbeat, suspend, terminate, stale detection)
as a bounded operational substrate. It provides receipts so “fleet state” is not inferred from logs or mythology.

Fleet lifecycle is **not**:
- activation authority,
- executor-work lifecycle (claim/readiness/entry/return/release),
- runtime session ontology,
- or autonomous swarm orchestration.

It is the smallest disciplined layer that says: *which executor members exist, what state they are in, and what receipts prove it.*

## Why this surface exists

Older lines (Victus/Gemini) preserved a concrete `active_fleet` witness with:
- member spawn,
- member suspend,
- member terminate,
- heartbeat/last-ping,
- stale detection and automatic suspension.

The current branch preserved activation authority and executor-work lifecycle law, but did not yet preserve
a compact fleet membership witness that can support capability truth, receipt discipline, and later bounded multi-executor work.

This protocol reincorporates that witness **without** importing old server stacks, pubsub systems, or role mythology.

## Canonical objects

### FleetIdentity
A durable identity for the fleet being tracked.

### FleetMemberIdentity
A durable identity for one fleet member with:
- callsign,
- branch,
- optional authority class descriptor,
- lifecycle state,
- heartbeat witness,
- and suspension/termination reasons when relevant.

### FleetMemberState
The minimal member lifecycle vocabulary:
- `BOOTING`
- `ACTIVE`
- `SUSPENDED`
- `TERMINATED`

### FleetReceipt
A receipt proving that a fleet or member lifecycle event occurred.

## Boundary clarifications

### Relation to activation authority
Fleet membership does not authorize enactment.
Activation authority still decides whether bounded work may cross into execution.

### Relation to executor lifecycle
Fleet membership is not executor-work binding.
Executor lifecycle still governs claim/readiness/entry/suspend/resume/return/release/retire **for a work target**.
Fleet lifecycle only witnesses member existence and member state.

### Relation to capability registry
Fleet lifecycle can inform whether a member exists and appears healthy,
but capability truth remains a separate registry surface.

### Relation to runtime/session
Runtime sessions may attach to executors later, but fleet lifecycle is not session ontology.

### Anti-theater rule
Fleet lifecycle must remain factual: members, states, receipts.
It must not smuggle in “autonomous swarm” narratives or unbounded role hierarchies.

## Minimal compliance requirements

A compliant fleet lifecycle surface must:
- persist fleet identity,
- persist member identities,
- persist heartbeat evidence,
- enforce explicit suspend/terminate transitions,
- support stale detection with explicit suspension receipts,
- sanitize identifiers and prevent path-escape mutation,
- remain receiptable and auditable.

## Non-goals

This protocol does **not** define:
- multi-agent task decomposition,
- orchestrator mission control,
- pubsub/event-bus infrastructure,
- or autonomous swarm cycles.

Those remain later surfaces, and only after bounded fleet witness and receipt discipline are stable.
