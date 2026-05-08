# Data Zip Operating Protocol

## Mount

Inspect `ION_DATA_MANIFEST.json`, `STATE/current_state.json`,
`DOMAINS/domain_registry.json`, `CONTEXT/context_graph.json`,
`PACKETS/open_packets.json`, `DECISIONS/decision_ledger.json`,
`ARTIFACTS/artifact_manifest.json`,
`PERSONA/persona_state.json`, and `RECEIPTS/receipt_ledger.jsonl`.

## Work

Produce proposals, not unreceipted state. Meaningful updates require a
receipt append and an updated export.

## Export

Export a new data zip after state changes. The user carries that zip
forward as continuity.
