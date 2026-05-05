# Executor Work Closure Binding Protocol

## Purpose

Define the bounded bridge from explicit executor entry into explicit return / failure / release witnesses.

This surface is subordinate to:
- activation authority,
- executor lifecycle law,
- schedule completion release law,
- and validation / commit outcomes.

It does **not** introduce mission control, swarm logic, or a new scheduler center.

## Core rule

Once a work unit has entered execution through an explicit `ENTER_EXECUTION` witness, closure must also be explicit.

Three closure actions are permitted:
- `RETURN_FOR_VALIDATION`
- `FAIL_EXECUTION`
- terminal release after `COMMITTED` / `FAILED` / `BLOCKED`

## Boundary clarifications

- Return-for-validation moves one work unit from `EXECUTING` to `VALIDATING` and emits a witness.
- Failure moves one work unit from `EXECUTING` to `FAILED` and emits a witness.
- Release remains subordinate to `M8` schedule completion/release reconciliation and may not be invented by executor closure alone.
- Closure receipts must keep the original executor/fleet/dispatch lineage visible.

## Receipt surface

Closure witnesses reuse `ExecutorWorkLifecycleBindingReceipt` with:
- `source_executor_work_lifecycle_binding_receipt_id`
- optional `source_schedule_completion_release_receipt_id`
- optional terminal commit-delta lineage
- `closure_reason` when provided
