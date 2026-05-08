# ION Cursor Cockpit Extension Protocol

## Status

Version: V90  
Authority class: runtime projection and host UI protocol  
Production authority: false  
Live execution authority: false

## Purpose

This protocol binds the existing ION/JOC cockpit shell to the post-V88 Cursor carrier-control runtime. The cockpit is a projection and control surface over kernel-governed packets. It must not become an independent authority layer.

## Core law

The Cursor cockpit renders kernel-emitted runtime state. It may invoke kernel commands. It must not directly accept worker returns, resolve human gates, integrate state, or mutate active packets outside kernel entrypoints.

## Required data path

```text
ION active runtime packets
  -> kernel.ion_cockpit_view_model
  -> ION/05_context/current/ACTIVE_COCKPIT_VIEW_MODEL.json
  -> Cursor extension status tree / JOC webview
  -> operator command
  -> kernel command
  -> refreshed active packets
```

## Required packets

The cockpit view model must read, when available:

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

## Required UI authority classes

The cockpit must preserve authority status for displayed objects:

```text
ACTIVE_RUNTIME_AUTHORITY
ACCEPTED_TASK_RETURN
PENDING_TASK_RETURN
REJECTED_TASK_RETURN
HUMAN_GATE_REQUIRED
LEGACY_CONTEXT_WITNESS
DONOR_REFERENCE
FORBIDDEN_CAPABILITY
```

## Extension commands

The extension may expose:

```text
ION: Continue
ION: Status
ION: Audit Carrier Workflow
ION: Refresh Cockpit View Model
ION: Open Active Carrier Turn Packet
ION: Open Task Return Ledger
ION: Open Steward Integration Queue
ION: Open Human Gate Queue
ION: Open JOC Cockpit
```

Each command must call a kernel module or open a file. The extension must not replace ION kernel authority.

## JOC shell binding

`ION/08_ui/joc_cockpit_shell/JocCockpitShell.tsx` must continue to support the historical fixture-backed projection while also accepting `runtimeProjection?: IonCockpitViewModel`. The live runtime cockpit is a successor projection, not a deletion of older UI law.

## Acceptance criteria

A V90-conformant cockpit implementation:

1. Builds `ACTIVE_COCKPIT_VIEW_MODEL.json` from active runtime packets.
2. Provides a Cursor/VS Code extension scaffold.
3. Provides a status tree and live webview shell.
4. Preserves JOC layout zones.
5. Makes carrier-control distinct from STEWARD integration authority.
6. Displays human gates, spawn rows, Task returns, Steward queue, receipts, and timeline state.
7. Does not bypass proof-gated Task-return intake or Steward integration queue.
