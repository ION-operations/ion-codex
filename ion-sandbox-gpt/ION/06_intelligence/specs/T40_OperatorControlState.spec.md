# T40 — Operator Control State

## Intent

Provide machine-readable operator hold / resume / stop control for supervised automation.

## Required Behaviors

1. Persist service mode as one of `ENABLED`, `STOPPED`, or `DRAINING`.
2. Persist scope-local holds with reason and timestamps.
3. Preserve an append-only ledger of control mutations.
4. Allow scope hold and scope resume operations.
5. Allow service-mode mutation operations.

## Non-Goals

- mutation of kernel truth
- hidden overrides of threshold or review law
