# ION V90 Live JOC Cockpit Webview Binding Report

## Summary

V90 promotes ION's existing JOC cockpit shell toward a live Cursor-visible cockpit by adding a kernel cockpit view-model builder, Cursor/VS Code extension scaffold, status tree provider, live webview provider, and React runtime panels for the post-V88 carrier-control packet layer.

## Main addition

The key new runtime projection is:

```text
ION/04_packages/kernel/ion_cockpit_view_model.py
```

It emits:

```text
ION/05_context/current/ACTIVE_COCKPIT_VIEW_MODEL.json
```

The view model reads active runtime packets instead of chat memory:

```text
ACTIVE_CURSOR_HOOK_STATE.json
ACTIVE_WORK_PACKET.json
ACTIVE_ROLE_SPAWN_PLAN.json
ACTIVE_CARRIER_TURN_PACKET.json
ACTIVE_CARRIER_TASK_RETURN_LEDGER.json
ACTIVE_STEWARD_INTEGRATION_QUEUE.json
ACTIVE_OPERATOR_MESSAGE_QUEUE.json
ACTIVE_HUMAN_GATE_QUEUE.json
```

## UI binding

V90 updates the existing JOC shell so it can render either:

```text
legacy fixture projection
```

or:

```text
live IonCockpitViewModel runtime projection
```

New runtime panels include:

```text
RuntimeStatusPanel
CarrierTurnPanel
SpawnQueuePanel
TaskReturnLedgerPanel
StewardIntegrationQueuePanel
HumanGateQueuePanel
OperatorMessageQueuePanel
CursorHookStatePanel
ContextPackageInspectorPanel
```

## Cursor extension scaffold

V90 adds:

```text
ION/09_integrations/cursor_extension/
```

The extension scaffold detects the ION root, runs kernel commands, watches `ION/05_context/current/*.json`, exposes a status tree, and opens a JOC cockpit webview from `ACTIVE_COCKPIT_VIEW_MODEL.json`.

## Authority boundary

The extension and cockpit are not ION authority. They render and invoke kernel state only. STEWARD remains integration authority and only accepts proof-gated Task returns through the Steward integration queue.

## Validation

Direct validation performed in the handoff environment:

```text
py_compile: ion_cockpit_view_model.py passed
build_cockpit_view_model fixture: emitted ion.cockpit_view_model.v1
write_cockpit_view_model fixture: wrote ACTIVE_COCKPIT_VIEW_MODEL.json
overlay zip integrity: passed
```

Full TypeScript compilation was not run in the handoff environment because the extension scaffold requires local npm dependency installation. The extension is intentionally delivered as a scaffold with TypeScript source and package metadata.

## Next recommended version

V91 should install a small webview bundling path and connect the extension scaffold to the existing React JOC shell, either by a local build step or by preserving the current no-bundle HTML renderer until the dependency strategy is fixed.
