# Single-Carrier Sequence Receipt Template

template_id: ion.template.single_carrier_sequence_receipt.v1
status: ACCEPTED_SANDBOX_LINE_TEMPLATE
production_authority: false
live_execution_authority: false

## Purpose

Records one single-carrier sequential runtime packet and, when available, the
carrier's completed role-phase return.

## Required receipt fields

```yaml
schema_id: ion.single_carrier_sequence_receipt.v1
sequence_id: <id>
carrier: <carrier>
objective: <objective>
phase_order: <ordered phases>
packet_path: <packet path>
completed_output_path: <optional>
context_proof_required: true
template_action_proof_required: true
phase_section_validation: <ready|accepted|blocked>
steward_review_required: true
production_authority: false
live_execution_authority: false
```

A receipt candidate is not accepted state until reviewed through Steward/human
authority.
