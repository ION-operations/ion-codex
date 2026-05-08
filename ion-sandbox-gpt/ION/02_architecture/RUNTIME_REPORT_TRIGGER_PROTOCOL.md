# Runtime Report Trigger Protocol

## Purpose

Define the bounded D2 rule for when runtime-state packets may be emitted automatically during an already-invoked kernel action.

## Lawful trigger shape

Runtime-report artifact emission is allowed only when all of the following are true:

1. a bounded kernel event is already being invoked,
2. the caller supplies an explicit workspace root,
3. the caller supplies an explicit trigger policy object,
4. emitted artifacts remain `GENERATED_STATE`, and
5. no store/index/graph truth is derived from the emitted artifact itself.

## Supported trigger events

- planner manifest creation
- review escalation
- governed-write runtime-state sync
- capsule runtime-state sync

## Default restraint

- planner manifest creation: enabled by explicit request
- review escalation: enabled by explicit request
- governed-write scope-status artifact: enabled by explicit request
- capsule scope-status artifact: disabled unless explicitly enabled

## Blocking posture rule

For runtime-state sync triggers, scope-status artifacts should default to emission only when the resulting posture is blocking, suspended, drifted, or otherwise non-dispatchable. Non-blocking sync may still emit only when the trigger request explicitly allows it.

## Non-goals

- no background daemon
- no hidden auto-writer
- no authority promotion
- no new persistence family
