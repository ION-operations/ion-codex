# RUNTIME REPORT BIDIRECTIONAL FAMILY SUMMARY PROTOCOL

## Purpose

Define a bounded, read-only structural synopsis over one lawful profile↔digest bridge family.

This protocol sits **downstream** from:
- I1 profile-to-digest traces
- I2 digest reverse traces
- I3 bidirectional traces
- I4 bidirectional-trace comparisons
- I5 bidirectional temporal bridge-history traces

It does not create a new authority surface.

## Scope

A bidirectional family summary collapses one lawful I5 bridge-history family into:
- first / last generation span
- per-aspect presence coverage
- stable / transient / emergent / vanished values
- family-level unions for trigger events, artifact kinds, source families, runtime refs, and asymmetries

## Inputs

A lawful summary request resolves exactly one bridge family through an existing `RuntimeReportBidirectionalTemporalSelector`.

Allowed selector modes:
- `PROFILE_NAME`
- `PROFILE_PATH`
- `BROWSER_ENTRY`

## Outputs

Governed packet root:
- `ION/05_context/runtime_reports/governance/digest_profiles/bidirectional_traces/families/`

Packet kinds:
- markdown family-summary packet
- JSON family-summary packet

Output classification:
- `summary_kind: RUNTIME_REPORT_BIDIRECTIONAL_FAMILY_SUMMARY`
- `authority_class: GENERATED_STATE`
- `interface_mode: READ_ONLY`

## Structural Guarantees

The family summary must preserve:
- profile identity
- generation count
- first / last digest generation markers
- per-aspect structural summaries derived from the real I5 temporal trace

The family summary must not:
- mutate kernel truth
- become route authority
- become runtime authority
- become digest authority
- become profile authority
- become bridge-history authority
- become summary authority

## Aspect Semantics

Each aspect summary reports:
- presence count
- ever / always present flags
- max value count
- stable values
- transient values
- emergent values
- vanished values
- first / last present generation labels

## Boundary

This protocol defines a **read-only compression layer** over lawful bridge-history witness material.
It exists for operator understanding and traversal only.
