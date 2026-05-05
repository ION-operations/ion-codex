# 2026-04-10 daemon bootstrap bridge — next packet

## Current truth

The supervised daemon has now been proven non-idle in the current working branch.

What made that possible was not hidden chat context or a pretend always-on carrier.
It was one lawful machine-readable pressure artifact:

- `ION/05_context/signals/archive/ION_TASK_FAILED_bootstrap_non_idle_daemon_20260410T1835.signal.json`

The daemon consumed that signal and created durable `signal_followup` pressure in the kernel store.

## Problem statement

The current bootstrap path still requires manual signal authoring.
That is acceptable for proof, but not as the long-term native self-use posture.

## Next bounded objective

Land one lawful bootstrap bridge that can seed first daemon pressure from a visible repo-native input.

## Preferred bridge order

1. **Inbox/bootstrap packet -> canonical signal**
   - keep the current daemon law unchanged
   - only automate the seed-pressure creation step
   - easiest short-path candidate

2. **Inbox/bootstrap packet -> open question**
   - bypasses signal semantics
   - simpler in some ways but loses the current canonical signal pressure lane

3. **Inbox/bootstrap packet -> work unit + context package**
   - strongest long-term path
   - larger design surface and likely not the next smallest lawful packet

## Recommendation

Choose option 1 first.

The smallest truthful next packet is:

- define one bootstrap packet shape
- write one parser/bridge that renders a canonical `TASK_FAILED` or `BLOCKED` daemon signal
- archive the bootstrap input after successful bridge emission
- keep the daemon unchanged
- add one end-to-end test covering bootstrap input -> signal -> daemon action -> durable follow-up pressure

## Why this order is correct

This preserves the current constitutional layers:

- bootstrap input is only seed pressure
- signal remains the canonical daemon pressure bus
- daemon continues to interpret existing lawful signal types
- follow-up remains routed through current `signal_followups.py` law

## Exit condition

A fresh extracted root should be able to reach the first non-idle daemon action without manual signal authoring and without inventing any hidden runtime state.
