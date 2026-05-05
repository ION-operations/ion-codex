# ION Carrier Task-Return Intake Protocol

## Purpose

This protocol defines how a carrier parent chat receives, validates, records, and forwards Cursor Task worker returns.

The carrier parent chat is not a role worker. It is the control lane that executes ION's active spawn queue and records evidence.

## Law

A spawned Task return is not an ION return until it is recorded in the active Task-return ledger.

A Task return is not eligible for Steward integration until `kernel.ion_carrier_task_return` accepts its `### CONTEXT PROOF` against the row's `context_load_receipt_path`.

Generic acknowledgments such as "I read the context file" are not acceptable evidence.

## Active files

- `ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json`
- `ION/05_context/current/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json`
- `ION/05_context/current/ACTIVE_STEWARD_INTEGRATION_QUEUE.json`

## Carrier procedure

1. Run `kernel.ion_carrier_continue` at the start of a continuation turn.
2. Read `ACTIVE_CARRIER_TURN_PACKET.json`.
3. Spawn only rows listed in `spawn_queue`.
4. Give each worker the generated `context_package_path`.
5. Capture the full Task worker output.
6. Run `kernel.ion_carrier_task_return` with the row role/index and captured output.
7. If accepted, leave the result in `ACTIVE_STEWARD_INTEGRATION_QUEUE.json` for Steward integration.
8. If rejected, rerun that role with the same context package and the rejection findings.

## Forbidden behavior

- The parent chat must not integrate raw Task output directly.
- The parent chat must not summarize a rejected return as if it were accepted.
- The parent chat must not ask the operator what agents to spawn while a valid spawn plan exists.
- The parent chat must not treat MINI/CAPSULE or boot-file acknowledgment as a context proof.

## Authority

This protocol is file-backed carrier law for Cursor-hosted ION. It does not grant production authority, live external execution authority, secrets access, or arbitrary shell authority.
