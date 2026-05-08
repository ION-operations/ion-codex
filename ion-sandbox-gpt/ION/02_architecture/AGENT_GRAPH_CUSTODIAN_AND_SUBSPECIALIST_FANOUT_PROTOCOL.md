---
type: architecture_protocol
authority: A3_OPERATIONAL_CANDIDATE
status: PROPOSED_RESTORATION_NOT_YET_RATIFIED
created: 2026-04-24
protocol_id: agent_graph_custodian_and_subspecialist_fanout_protocol
related:
  - ION/02_architecture/CONTEXT_GRAPH_SUBSTRATE_PROTOCOL.md
  - ION/02_architecture/BOUNDED_MULTI_AGENT_ALLOCATOR_PROTOCOL.md
  - ION/02_architecture/FAN_IN_MERGE_REVIEW_SETTLEMENT_PROTOCOL.md
  - ION/03_registry/agent_roster_registry.yaml
---

# Agent Graph Custodian and Subspecialist Fan-Out Protocol

## Purpose

Define how current ION agents operate as managers and custodians over graph regions, and how they lawfully fan out to sub-specialists without inflating the top-level roster.

## Core rule

A top-level agent is not expected to contain all relevant context. It must know how to request, assemble, delegate, and settle context packages from graph-region specialists.

## Fan-out law

A manager may fan out when the task crosses graph regions, the parent context burden exceeds safe bounded context, distinct evidence standards apply, concurrent read/analysis lanes reduce drift, or specialized graph custody is required.

Fan-out must declare parent manager, requested sub-specialists, graph regions assigned, context package IDs, allowed read/write scope, expected settlement outputs, and fan-in target.

## Fan-in law

Sub-specialist outputs return as proposals. They are not parent truth until settled by the manager and, where required, audited or approved by higher authority.

## Current roster reading

The current ION 3 roster is a manager/support lattice, not a small fixed team.

- Steward: current-phase routing and approval manager.
- Vizier: architecture and cross-region synthesis manager.
- Vice: contradiction-pressure manager.
- Nemesis: independent audit manager.
- Mason: implementation-region manager.
- Scribe: legibility/archive/projection manager.
- Vestige: donor-lineage and drift-watch manager.
- Relay: intent/packet/signal boundary manager.
- Thoth: research/evidence extraction manager.
- Atlas: topology/comparative mapping manager.
- Weaver: reserved presentation/projection manager, not live until instantiated.
