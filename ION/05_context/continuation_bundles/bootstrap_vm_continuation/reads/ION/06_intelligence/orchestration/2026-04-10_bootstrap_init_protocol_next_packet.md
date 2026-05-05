---
type: orchestration
authority: A2_EXECUTOR
created: 2026-04-10T18:50:00-04:00
status: ACTIVE
---

# Bootstrap-init protocol — next packet

## Current truth

The branch now supports the following lawful early-runtime chain:

1. visible bootstrap `task` packet in `ION/05_context/inbox/bootstrap/`
2. `python -m kernel bootstrap emit ...`
3. canonical daemon signal in `ION/05_context/signals/`
4. supervised daemon consumption
5. durable `signal_followup` or review pressure in kernel state

## What remains missing

A fresh root still relies on an operator or current executor to author the first bootstrap packet by hand.

That is acceptable for the present branch.
It is not yet the native end-state.

## Next bounded objective

Define one lawful **bootstrap-init** surface that can mint the first bootstrap packet without bypassing packet law.

## Preferred order

1. **operator bootstrap-init command -> bootstrap task packet**
   - smallest next step
   - keeps packet law explicit
   - composes cleanly with the landed bootstrap bridge

2. **visible initialization manifest -> bootstrap task packet**
   - more declarative
   - slightly wider design surface

3. **direct init manifest -> canonical signal**
   - should not be the next move
   - skips the now-useful bootstrap packet lane

## Recommendation

Choose option 1 first.

The next packet should land:

- one explicit bootstrap-init CLI command
- one canonical task-packet writer into `ION/05_context/inbox/bootstrap/`
- one focused test proving init -> bootstrap packet -> bootstrap bridge -> daemon action

## Anti-drift rule

Do not widen daemon law while landing bootstrap-init.
The bootstrap path should remain:

- init writes packet
- bridge writes signal
- daemon consumes signal

That preserves the now-explicit constitutional layering.
