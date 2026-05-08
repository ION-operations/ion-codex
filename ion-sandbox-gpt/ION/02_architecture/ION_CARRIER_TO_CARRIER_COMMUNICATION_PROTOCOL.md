---
type: protocol
authority: A3_PROPOSED
status: DRAFT_NON_PRODUCTION
production_authority: false
live_execution_authority: false
---

> Operational mount order is governed by `ION/02_architecture/ION_MOUNT_CONTRACT.md`.

# ION Carrier-To-Carrier Communication Protocol

## Purpose

Carrier-to-carrier communication lets mounted carriers exchange bounded
messages through ION-managed queues without treating any carrier as ION identity
or creating a second messaging authority.

## Existing Owners Reused

- Operator messages remain in `ION/05_context/current/ACTIVE_OPERATOR_MESSAGE_QUEUE.json`.
- Steward decisions and integration records remain in `ION/05_context/current/ACTIVE_STEWARD_INTEGRATION_QUEUE.json`.
- Task returns remain in `ION/05_context/current/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json` and connector task-return packets.
- Carrier messages use the same active-context queue pattern at `ION/05_context/current/ACTIVE_CARRIER_MESSAGE_QUEUE.json`.
- MCP browser packets and receipts remain under `ION/05_context/current/chatgpt_connector/`.

## Distinctions

```text
operator_message = human/operator instruction or continuation signal
carrier_message = carrier-to-carrier coordination note with sender/recipient evidence
steward_decision = integration or route authority record
task_return = proof-bearing work output proposed for intake
receipt = custody, validation, decision, or lifecycle evidence
```

## Required Message Fields

- `message_id`
- `sender_carrier_id`
- `recipient`
- `channel`
- `message_type`
- `body`
- `context_refs`
- `receipt_refs`
- `status`
- `acked_by`
- `production_authority: false`
- `live_execution_authority: false`

## MCP Tool Surface

```text
ion_carrier_message_send
ion_carrier_message_poll
ion_carrier_message_ack
```

`send` and `ack` require `ION_BOUNDED_WRITE_CONFIRMED`. `poll` is a bounded
read. None of these tools can act as Steward, Relay, Persona, shell, git, or
production authority.

## Routing Law

Carrier messages may coordinate work, cite context, and point to receipts. They
must not directly promote truth. Steward integration or the appropriate packet
gate remains required for current-state authority changes.

## Failure Classification

If carrier communication fails, classify the issue before changing core law:

```text
CARRIER_ADAPTER_FAILURE
TRANSPORT_FAILURE
AUTH_OR_CONFIRMATION_FAILURE
CAPABILITY_NOT_YET_IMPLEMENTED
ION_CORE_FAILURE
POLICY_BLOCK_WORKING_AS_DESIGNED
```
