# EXTENSION_QUEUE_PACKET_LIFECYCLE_PROTOCOL

Packet states:
- `draft`
- `candidate`
- `approved`
- `claimed`
- `running`
- `proof_accepted`
- `settled`
- `cancelled`
- `superseded`

Rules:
- Queue packets are candidate transitions, not accepted state.
- `approved|claimed|running|proof_accepted|settled` are lock states.
- Lock-state mutation requires supersession or cancellation receipt.
