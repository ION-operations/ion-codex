# T14 — Runtime State Operational Rendering Schema

## Scope

Defines the C4 rendering contract for bounded operator-facing runtime packets.

## Required Reporter

### KernelRuntimeStateReporter
Must render:
- scope status reports
- planner-manifest packets
- review packets

## RuntimeScopeStatusBundle
Required fields:
- `scope_view`
- `dispatch_posture`
- `review_pressure` (optional)
- `rendered_report`

## Status Report Minimum Contents

- scope id
- route action or explicit absence of route state
- automation stage or explicit absence of automation state
- dispatch posture
- review pressure when present
- runtime refs when present

## Planner Packet Minimum Contents

- planner manifest id and status
- parent work unit id
- source question id
- planner delta id
- child intent summary
- runtime posture summary
- route / automation surfaces when present

## Review Packet Minimum Contents

- review question id
- held delta id when available
- runtime review pressure summary
- dispatch posture summary
- route / automation surfaces when present
- linked artifacts and review reasons when present

## Constraints

- Rendering may consume existing runtime-state query objects.
- Rendering may not mutate kernel state.
- Rendering must not imply dispatch permission when `RuntimeDispatchPosture.dispatch_permitted` is false.
