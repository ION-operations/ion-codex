# SUPERVISED DAEMON SERVICE PROTOCOL

## Purpose

Define a truthful service harness over the existing bounded daemon loop.
This protocol turns the daemon loop into an operator-invoked supervised service surface without claiming unattended autonomy.

## Service law

1. Service execution requires explicit workspace context.
2. Service execution must consult operator control state.
3. Service execution must consult automation policy before action.
4. Service execution may run only bounded loop steps.
5. Every service invocation must emit a receipt.
6. Service receipts are witness / generated-state outputs, not kernel truth.

## Minimum request fields

- workspace root
- max steps
- context mode
- automation stage
- supervising operator presence
- explicit approval flag
- optional scope binding

## Minimum receipt fields

- service status
- control posture
- policy decision
- run timestamp
- optional daemon-loop receipt linkage
- service receipt path
- service ledger path

## Status classes

- `EXECUTED`
- `DRY_RUN`
- `CONTROL_BLOCKED`
- `POLICY_BLOCKED`
- `APPROVAL_REQUIRED`

## Non-goals

- no unattended service restart loop
- no background scheduler
- no external execution bridge

## Runtime/session clarification

A supervised daemon service may invoke bounded work inside an existing
runtime/session center.
It does **not** mint session identity, own the session queue, or replace API
runtime-entry law.
Those authority surfaces now remain explicitly governed by the emitted Lane C
runtime/session trio.
