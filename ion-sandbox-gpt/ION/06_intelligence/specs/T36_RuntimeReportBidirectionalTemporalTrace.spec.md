# T36 — Runtime Report Bidirectional Temporal Trace

## Summary

Introduce a bounded temporal packet over successive generations of one lawful profile↔digest bridge family.

## Inputs

`RuntimeReportBidirectionalTemporalSelector`
- `profile_name`
- `profile_path`
- `browser_query` + `browser_entry_index`
- `limit`

## Outputs

`RuntimeReportBidirectionalTemporalTrace`
- generation metadata
- per-generation bridge consistency fields
- aspect-by-aspect temporal transitions
- governed markdown/json packet outputs

## Governed Output Root

`ION/05_context/runtime_reports/governance/digest_profiles/bidirectional_traces/temporal/`

## Invariants

- at least two digest generations are required
- only one profile selection mode may be active
- digest generations must reverse-resolve to the selected profile
- the packet remains read-only and downstream

## Non-Goals

- no daemon or background reconciliation
- no authority promotion
- no mutation of kernel truth surfaces
