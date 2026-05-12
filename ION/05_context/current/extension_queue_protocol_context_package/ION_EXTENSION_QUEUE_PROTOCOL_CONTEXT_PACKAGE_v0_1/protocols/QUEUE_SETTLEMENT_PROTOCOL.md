# QUEUE_SETTLEMENT_PROTOCOL

Settlement transitions:
- proof_accepted -> settled
- cancelled -> settled
- superseded -> settled

Required settlement evidence:
- result_capture_ref
- receipt_refs
- settlement_reason
- settlement_actor
