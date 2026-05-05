---
type: protocol
authority: A2_EXECUTOR
created: 2026-04-08T20:15:00-04:00
status: ACTIVE
---

# Horizon Orchestration Protocol

## Purpose

ION must not only decide the next bounded step. It must also maintain a lawful **orchestration horizon** that becomes more precise as execution approaches.

## Horizon layers

### 1. Immediate horizon
The immediate horizon contains the next bounded steps that are precise enough to execute now.

Properties:
- exact route or executor request
- bounded context package or manual-equivalent packet
- explicit allowed writes / expected outputs
- blocking review or operator pressure attached

### 2. Near horizon
The near horizon contains sequenced likely-next work that is shaped but not yet fully packetized.

Properties:
- ordered work candidates
- unresolved dependencies called out
- probable executor families
- packetization pending latest truth updates

### 3. Far horizon
The far horizon contains looser orchestration intent.

Properties:
- thematic chains or campaign direction
- unresolved research / architecture / dependency surfaces
- no pretense of final ordering where truth is insufficient

## Law of progressive tightening

As the system approaches a horizon item, the kernel or current executor must refine it:

- far horizon becomes near horizon,
- near horizon becomes immediate horizon,
- immediate horizon becomes a bounded executable packet.

The closer the work is to execution, the stricter the required detail.

## Carrier symmetry

This law applies identically whether the carrier is:
- a chat/manual executor,
- an IDE executor,
- the supervised daemon runtime,
- an external/API worker,
- or a future swarm child.

The difference is not the workflow. The difference is who carries the next transition.

## What is forbidden

- pretending a far-horizon idea is an immediate executable packet
- leaving immediate work under-specified
- hiding the shift from loose orchestration to bounded execution
- allowing automation mode to create a separate horizon law
