# T37 — Runtime Report Bidirectional Family Summary

## Intent

Provide a bounded structural synopsis over one lawful profile↔digest bridge family.

## Depends On

- T32 `RuntimeReportProfileDigestTrace`
- T33 `RuntimeReportDigestReverseTrace`
- T34 `RuntimeReportBidirectionalTrace`
- T35 `RuntimeReportBidirectionalTraceComparison`
- T36 `RuntimeReportBidirectionalTemporalTrace`

## Required Behaviors

1. Resolve exactly one lawful bridge family through an existing temporal selector.
2. Delegate family realization to the existing I5 temporal bridge-history surface.
3. Emit first / last generation span markers.
4. Emit family-level unions for:
   - forward source kinds
   - reverse source kinds
   - reverse profile-resolution modes
   - trigger events
   - artifact kinds
   - source families
   - runtime refs
   - asymmetries
5. Emit per-aspect summaries with:
   - presence count
   - ever / always present flags
   - max value count
   - stable values
   - transient values
   - emergent values
   - vanished values
   - first / last present generation labels
6. Support governed markdown + JSON packet write-out.
7. Preserve read-only downstream witness semantics.

## Governed Output Root

- `ION/05_context/runtime_reports/governance/digest_profiles/bidirectional_traces/families/`

## Non-Goals

- ranking bridge families
- mutating any upstream surface
- inventing a new identity scheme for bridge generations
- promoting summaries into kernel or runtime authority
