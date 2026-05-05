# RUNTIME REPORT GOVERNANCE PROTOCOL

## Purpose

Define how runtime-report trigger receipts may be reflected into durable witness surfaces
without promoting those reflections into kernel truth.

This protocol sits **after** D2 trigger emission.
It governs the optional E1 layer that turns already-emitted runtime report artifacts into:

- a bounded governance ledger
- an operator-facing summary packet

## Core law

1. Triggered runtime artifacts remain the primary generated outputs.
2. Governance reflections are **witness over generated state**, not runtime authority.
3. Reflection may occur only from already-emitted trigger receipts.
4. Reflection requires an explicit workspace root supplied by the caller.
5. Reflection must write only under governed relative paths.
6. Reflection must not mutate kernel store, kernel index, or graph truth.
7. Reflection must preserve the artifact/source/event relationship explicitly.

## Reflection surfaces

### Governance ledger

Default path:

`ION/05_context/history/runtime_report_trigger_ledger.json`

Each row must include at minimum:

- event id
- created at
- trigger event
- artifact kind
- source ref
- reason
- artifact relative output path
- artifact authority class
- runtime refs when present
- summary path when present

### Operator summary

Default directory:

`ION/05_context/runtime_reports/governance/`

The summary is a generated markdown witness packet that groups one trigger batch and states
clearly that the batch is reflective, not governing.

## Boundaries

This layer does **not**:

- create a new kernel persistence family
- create an autonomous reporter or daemon
- upgrade generated witness into doctrine or runtime authority
- reinterpret continuity prose as machine state

## Expected call shape

The caller may request reflection during trigger handling by explicitly opting in through the
runtime report trigger request. Reflection should remain optional and off by default.

## Relationship to adjacent packets

- D1 created durable runtime artifacts.
- D2 created explicit trigger policy for emitting those artifacts.
- E1 reflects those trigger receipts into governance visibility.
- A later packet may decide how, or whether, selected governance rows should feed broader system ledgers.
