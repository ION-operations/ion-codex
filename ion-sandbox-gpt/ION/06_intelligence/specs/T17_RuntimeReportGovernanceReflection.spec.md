# T17 — Runtime Report Governance Reflection

## Intent

Add a bounded reflection layer for runtime-report trigger receipts so already-emitted runtime
artifacts can be surfaced into durable governance visibility without becoming kernel truth.

## Inputs

- D2 runtime report trigger receipts
- explicit workspace root
- explicit reflection request

## Outputs

- appended JSON governance ledger rows
- optional markdown operator summary packet
- enriched trigger receipts carrying governance refs

## Required invariants

1. Reflection consumes existing trigger receipts only.
2. Reflection writes only under governed relative paths.
3. Reflection never mutates kernel store/index/graph state.
4. Reflection preserves `GENERATED_STATE` / witness framing.
5. Reflection remains off unless explicitly requested.
6. Summary output must state the boundary between reflection and kernel truth.

## Default governed paths

- `ION/05_context/history/runtime_report_trigger_ledger.json`
- `ION/05_context/runtime_reports/governance/`

## Minimal row schema

```yaml
entry_type: runtime_report_trigger_reflection
event_id: string
entry_index: integer
created_at: iso8601
trigger_event: enum
artifact_kind: enum
source_ref: string
reason: string
artifact_relative_output_path: string
artifact_generated_at: iso8601
artifact_authority_class: GENERATED_STATE
runtime_refs: [string]
summary_path: string|null
```

## Receipt enrichment

Each reflected trigger receipt may carry:

- `governance_event_id`
- `governance_ledger_path`
- `operator_summary_path`

## Non-goals

- no daemon loop
- no authority promotion
- no new canonical runtime family
- no automatic doctrine mutation
