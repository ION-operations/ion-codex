# ION/JOC Synthetic Synthesis and Route-Result Preview Protocol

## Purpose

V66 defines the non-executing cockpit layer after synthetic response capture. The cockpit may render a synthesis preview, disagreement placeholder, follow-up draft, and route-result preview rail. It may not write memory, commit graph state, update source summaries, call providers, mutate browser sessions, or claim consensus.

## Required inputs

- V65 synthetic capture reference
- V65 extraction receipt preview id
- synthetic extracted text
- extraction quality flags
- synthesis flags
- evidence references
- budget/API governor snapshots
- allowed route preview actions
- follow-up prompt preview

## Required visible surfaces

```text
SYNTHETIC_SYNTHESIS_PREVIEW_PANEL
ROUTE_RESULT_PREVIEW_RAIL
EXTRACTION_RECEIPT_LINK
NO_CONSENSUS_TRUTH_STRIP
NO_MEMORY_WRITE_STRIP
NO_GRAPH_COMMIT_STRIP
FOLLOWUP_DRAFT_PREVIEW
OPERATOR_REVIEW_NEXT_ACTION
```

## Verdicts

```text
SYNTHETIC_SYNTHESIS_PREVIEW_READY
BLOCKED_CAPTURE_NOT_READY
BLOCKED_MISSING_SYNTHESIS_EVIDENCE
BLOCKED_FORBIDDEN_ROUTE_CAPABILITY
BLOCKED_LIVE_SYNTHESIS_REQUESTED
BLOCKED_ROUTE_RESULT_MUTATION_REQUESTED
BLOCKED_INVALID_SYNTHETIC_RECEIPT
```

## Non-authority rule

V66 is a view-model branch. It may render post-capture result shape. It does not execute result routing.
