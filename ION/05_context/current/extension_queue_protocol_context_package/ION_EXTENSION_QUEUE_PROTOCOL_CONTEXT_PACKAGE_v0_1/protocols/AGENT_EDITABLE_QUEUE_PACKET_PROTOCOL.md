# AGENT_EDITABLE_QUEUE_PACKET_PROTOCOL

Agent edits:
- Allowed only for `draft` and `candidate` packets.
- Must be represented as diff-bearing `queue_event` entries.

Forbidden:
- Direct overwrite without event ledger.
- Editing locked states except through explicit supersession/cancellation flow.
