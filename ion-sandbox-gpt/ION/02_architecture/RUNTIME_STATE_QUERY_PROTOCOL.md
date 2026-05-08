# RUNTIME STATE QUERY PROTOCOL

## Purpose

C3 promotes persisted `manifest_route_state` and `automation_state` from passive storage into bounded query surfaces that daemon, review, and signal-follow-up services can consume directly.

## Lawful Boundaries

- Query helpers may read runtime state and derive bounded posture summaries.
- Query helpers may not invent autonomous actions not already supported by the live kernel.
- Runtime query consumption must preserve continuity law: prose continuity remains distinct from machine-readable route and automation state.

## Required C3 Consumption Surfaces

1. Graph traversal must surface runtime-state nodes and edges.
2. Daemon arbitration must be able to suppress dispatch when runtime posture is explicitly blocked.
3. Review escalation must be able to include runtime-state witness references in durable review pressure.
4. Signal follow-up creation must be able to bind follow-up pressure to runtime-state witness references.

## Canonical Query Objects

- `RuntimeStateScopeView`
- `RuntimeReviewPressure`
- `RuntimeDispatchPosture`

## First-pass Graph Rules

- `work_unit -> manifest_route_state` when the manifest owner scope is `WORK_UNIT`
- `work_unit -> automation_state` when the automation scope is `WORK_UNIT`
- `manifest_route_state -> automation_state` when the records are linked

## Non-goals

- no daemon autonomy claim
- no hidden singleton manifest
- no collapsing markdown continuity into kernel state

## Runtime/session clarification

Runtime-state query may summarize posture derived from runtime/session facts.
It does **not** create session authority, own session-local queues, or decide
API entry legality.
Those authority surfaces now remain explicitly governed by the emitted Lane C
runtime/session trio.
