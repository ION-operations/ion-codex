# V114 Deferred Spawn Visibility Lock

## Lock

V114 exposes deferred spawn/materialization state in status and cockpit projections.

After V113, zero-spawn turns can lawfully defer role candidates without writing execution bundles. Operators still need to see that distinction explicitly, so cockpit/status must not leave deferred work hidden behind a simple `0/5` spawn count.

## Current Objective

```text
V114 deferred spawn visibility: status and cockpit expose active spawn count, deferred spawn count, and execution-bundle materialization state for zero-spawn carrier turns.
```

## Required Runtime State

```yaml
kernel_status: ION_STATUS_READY
spawn_queue_count: 0
plan_spawn_count: 0
deferred_spawn_count: greater_than_zero
execution_bundle_materialized: false
production_authority: false
live_execution_authority: false
```

## Scope

This lock does not spawn deferred rows, materialize worker context packages, delete prior execution cycles, or grant production authority. It only exposes the active/deferred distinction in runtime projections and UI types.

## Exit Condition

V114 is complete when:

- `kernel.ion_status` reports deferred spawn count and execution bundle materialization state
- cockpit top bar reports active, planned, and deferred spawn counts
- the runtime status panel displays deferred count and bundle state
- full tests pass
- preservation report shows zero protected and unexpected removals
