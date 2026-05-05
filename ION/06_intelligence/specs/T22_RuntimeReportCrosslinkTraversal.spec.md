# T22 — Runtime Report Crosslink Traversal

## Objective

Specify a bounded read-only traversal layer that resolves related downstream runtime-report witness surfaces for browser and packet navigation.

## Inputs

- runtime-report navigation result
- workspace root
- optional generated-at timestamp

## Required outputs

- crosslink view
- per-entry target list
- target existence witness
- optional markdown crosslink packet
- optional json crosslink packet

## Required target kinds

- `ARTIFACT_REPORT`
- `PACKET_INDEX`
- `OPERATOR_DASHBOARD`
- `GOVERNANCE_LEDGER`
- `GOVERNANCE_SUMMARY`
- `SYSTEM_LEDGER`
- `OPERATOR_ROLLUP`

Targets may be omitted only when the source entry does not carry the relevant path.

## Constraints

- read-only only
- relative workspace-governed paths only
- no absolute path escape
- no target mutation during traversal
- no promotion into kernel truth or runtime authority

## Browser integration

An F2 browser may render F3 crosslinks inline so long as the browser remains explicitly read-only and downstream.

## Non-goals

- no daemon
- no mutable UI control plane
- no link target hydration into kernel store/index/graph
- no authority promotion
