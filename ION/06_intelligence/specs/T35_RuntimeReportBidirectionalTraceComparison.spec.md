# T35 — Runtime Report Bidirectional Trace Comparison

## Intent

Add a bounded read-only packet that compares two or more lawful profile↔digest bidirectional traces side by side.

## Requirements

1. Require at least two comparison inputs.
2. Accept each input as exactly one of:
   - a live lawful `RuntimeReportBidirectionalTraceSelector`
   - an existing bidirectional-trace JSON packet path
3. Preserve and surface per-trace consistency markers:
   - profile name match
   - digest json path match
   - digest markdown path match
4. Preserve and surface per-trace asymmetry rows.
5. Provide structural unions/intersections for:
   - trigger events
   - artifact kinds
   - source families
   - runtime refs
6. Preserve read-only downstream witness semantics.

## Governed output root

`ION/05_context/runtime_reports/governance/digest_profiles/bidirectional_traces/comparisons/`

## Non-goals

- No ranking surface
- No new digest authority
- No new profile authority
- No daemon or scheduler
- No mutation of kernel truth
