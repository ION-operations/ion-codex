# QUEUE_EVENT_LEDGER_PROTOCOL

Every queue mutation emits an append-only event:
- event_id
- queue_type
- packet_id
- event_type
- actor
- before_state
- after_state
- diff
- created_at

Ledger is immutable except supersession references.
