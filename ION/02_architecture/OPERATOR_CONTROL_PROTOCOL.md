# OPERATOR CONTROL PROTOCOL

## Purpose

Define the first machine-readable operator control state for supervised automation.
The operator must be able to hold, resume, stop, or drain automation explicitly.

## Core law

1. Operator control is authoritative over supervised service entry.
2. Control state must be persisted as machine-readable witness state.
3. Control state must be scope-aware.
4. Resume clears a hold; it does not erase historical control events.
5. Stop / drain state must remain explicit until changed.

## First control surfaces

### Service mode

- `ENABLED`
- `STOPPED`
- `DRAINING`

### Scope hold

A scope hold binds:
- `scope_type`
- `scope_ref`
- reason
- created time
- optional actor

## Required outputs

- operator control state JSON
- operator control ledger JSON

## Non-goals

- no kernel-truth promotion
- no hidden override of review or threshold law
- no unattended control mutation
