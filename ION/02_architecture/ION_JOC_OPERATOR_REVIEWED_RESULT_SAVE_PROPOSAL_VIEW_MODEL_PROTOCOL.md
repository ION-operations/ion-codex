# ION/JOC Operator-Reviewed Result Save Proposal View Model Protocol

## Purpose

This protocol defines the V67 cockpit surface that appears after V66 synthetic synthesis and route-result preview. The purpose is to show where a result would be routed or saved after operator review, while preserving the boundary that no memory, graph, document, artifact, or provider mutation has occurred.

## Input Chain

```text
V65 synthetic response capture
→ V66 synthetic synthesis and route-result preview
→ V67 operator-reviewed result save proposal
```

## Required Display Surfaces

- `RESULT_REVIEW_PANEL`
- `SAVE_PROPOSAL_QUEUE`
- `MEMORY_WRITE_PROPOSAL_PREVIEW`
- `DOCUMENT_DRAFT_SAVE_PREVIEW`
- `ARTIFACT_EXPORT_PREVIEW`
- `AGENT_REVIEW_PACKET_PREVIEW`
- `FOLLOWUP_MISSION_DRAFT_PREVIEW`
- `NO_WRITE_BOUNDARY_STRIP`
- `OPERATOR_DECISION_REQUIRED_STRIP`

## Verdicts

```text
RESULT_SAVE_PROPOSAL_READY
BLOCKED_SYNTHESIS_NOT_READY
BLOCKED_MISSING_RESULT_EVIDENCE
BLOCKED_LIVE_SAVE_REQUESTED
BLOCKED_MEMORY_WRITE_REQUESTED
BLOCKED_DOCUMENT_WRITE_REQUESTED
BLOCKED_ARTIFACT_EXPORT_REQUESTED
BLOCKED_CANONICAL_GRAPH_WRITE_REQUESTED
BLOCKED_SOURCE_SUMMARY_REWRITE_REQUESTED
BLOCKED_INVALID_PROPOSAL_SCOPE
BLOCKED_FORBIDDEN_COMMIT_CAPABILITY
BLOCKED_MISSING_OPERATOR_REVIEW_POLICY
```

## Canonical Boundary

The save proposal is a cockpit decision object, not a write operation. It may prepare the operator to choose whether a later branch should create memory-write, document-save, artifact-export, or graph-commit authority.
