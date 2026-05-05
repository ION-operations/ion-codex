---
type: protocol
authority: A3_OPERATIONAL
created: 2026-04-15T02:10:00Z
status: ACTIVE
purpose: Define the bounded bridge that turns a lawful dispatch witness plus active fleet/capability truth into an explicit executor-entry receipt for one work unit
connections:
  - ION/02_architecture/ACTIVATION_AUTHORITY_PROTOCOL.md
  - ION/02_architecture/EXECUTOR_LIFECYCLE_PROTOCOL.md
  - ION/02_architecture/FLEET_EXECUTOR_CAPABILITY_BINDING_PROTOCOL.md
  - ION/02_architecture/LAWFUL_ORCHESTRATION_SCHEDULER_PROTOCOL.md
  - ION/02_architecture/SESSION_QUEUE_AND_DISPATCH_PROTOCOL.md
---

# Executor Work Lifecycle Binding Protocol

## Short thesis

ION needs one explicit bridge between:
- a lawful dispatch witness,
- an active fleet member that has already been materialized into executor capability truth,
- and the executor lifecycle transition that actually enters work into enactment.

This bridge exists so `DISPATCHED` work does not drift directly into shell-specific execution without one explicit executor-entry receipt.

## What this surface does

This surface binds:
- one `fleet_id`,
- one active `member_id`,
- one matching `executor_id` / `capability_id`,
- and one dispatched `work_unit_id`

into a single lifecycle action: `ENTER_EXECUTION`.

The result is one explicit receipt proving that executor identity, fleet membership, capability posture, and dispatch witness all lined up when the work crossed from `DISPATCHED` to `EXECUTING`.

## What this surface is not

It is not:
- activation authority,
- scheduler law,
- runtime-session authority,
- mission control,
- swarm logic,
- or commit/validation/settlement.

It is only the bounded entry bridge into actual executor work.

## Minimum checks

An executor-work entry should require:
- a real fleet member,
- member state `ACTIVE`,
- a matching executor capability record,
- active capability availability,
- a real `schedule_dispatch_reconciliation_receipt`,
- and a target work unit currently in `DISPATCHED`.

## Output

The bridge emits one `ExecutorWorkLifecycleBindingReceipt` and advances the work unit into `EXECUTING`.

## Boundary rule

This bridge does not create or infer activation. It assumes activation/dispatch already happened and only proves executor-entry alignment at the exact crossing into work enactment.
