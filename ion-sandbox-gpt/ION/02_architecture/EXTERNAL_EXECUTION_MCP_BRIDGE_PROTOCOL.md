# EXTERNAL EXECUTION MCP BRIDGE PROTOCOL

## Purpose

Define the truthful supervised bridge between the active ION kernel and external execution surfaces such as MCP-hosted tools or IDE task chassis.

## Core law

1. External execution is subordinate to kernel truth, automation policy, and operator control.
2. Exported execution packets are generated witness/service artifacts, not doctrine and not kernel truth.
3. External actors may only return bounded execution payloads; they do not gain direct write authority over kernel truth.
4. Returned execution payloads must re-enter the existing execution path as proposed commit deltas.
5. Governed write and validation remain separate downstream gates.
6. The bridge must make approval and refusal conditions explicit for external action classes.
7. No uncontrolled external write path or hidden MCP autonomy may be implied.

## Required action classes

The supervised automation policy must recognize at least:
- `EXPORT_EXTERNAL_EXECUTION_PACKET`
- `ACCEPT_EXTERNAL_EXECUTION_RETURN`

Both are supervised external boundary actions.

## Required behaviors

### 1. External export packet

A lawful export must:
- select one dispatchable work unit,
- materialize the normal dispatch/context payload,
- write an external execution packet under a governed service path,
- expose explicit MCP-facing metadata,
- mark the work unit as dispatched only through the normal dispatch path.

### 2. MCP-facing automation surface

The exported packet must expose a machine-readable MCP-facing surface including:
- resource kind/name,
- transport,
- tool name,
- request schema,
- response schema.

### 3. Returned execution acceptance

A lawful external return must:
- require an explicit returned `ExecutionSubmission`,
- re-enter through the normal execution path,
- create only a proposed commit delta,
- advance the work unit only to the next lawful execution-return state,
- persist bridge receipts and ledger rows.

### 4. Approval and refusal conditions

The bridge must refuse or require approval when:
- operator stop is active,
- operator hold/drain is active,
- automation policy blocks or holds the action,
- explicit approval is required by context, calibration, route stage, or review pressure.

### 5. Non-goals

- no direct external governed-write application,
- no direct external store/index mutation beyond the normal execution path,
- no hidden autonomous MCP loop,
- no authority collapse between service artifacts and kernel truth.

## Runtime/session clarification

An external execution bridge may export or accept bounded execution returns that
touch a runtime session.
It does **not** create session identity, own session-local queue mutation, or
replace API runtime-entry authority.
Those surfaces now remain explicitly governed by the emitted Lane C
runtime/session trio.
