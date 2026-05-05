# ION/JOC Operator-Reviewed Export Handoff Manifest Preview Protocol

V68 defines the non-executing view-model boundary between V67 result-save proposal cards and any future materialized handoff/export package.

## Flow

```text
V67 result-save proposal preview
→ operator-reviewed handoff manifest preview
→ manifest section rail
→ evidence reference table
→ governor snapshot strip
→ future authority requirements
```

## Non-authority rule

The manifest is a preview. It is not a file write, artifact export, memory write, external transfer, release package, graph commit, or source-summary mutation.

## Required manifest sections

```text
MISSION_SUMMARY
SYNTHETIC_RESULT_BOUNDARY
SAVE_PROPOSAL_CARDS
EVIDENCE_REFS
GOVERNOR_SNAPSHOT_REFS
BLOCKED_CAPABILITIES
FUTURE_AUTHORITY_REQUIREMENTS
OPERATOR_DECISION_LANE
```

## Verdicts

```text
HANDOFF_MANIFEST_PREVIEW_READY
BLOCKED_SAVE_PROPOSAL_NOT_READY
BLOCKED_MISSING_HANDOFF_EVIDENCE
BLOCKED_INVALID_MANIFEST_SECTION
BLOCKED_INVALID_HANDOFF_INTENT
BLOCKED_LIVE_EXPORT_REQUESTED
BLOCKED_FILE_WRITE_REQUESTED
BLOCKED_ZIP_CREATION_REQUESTED
BLOCKED_EXTERNAL_TRANSFER_REQUESTED
BLOCKED_MEMORY_WRITE_REQUESTED
BLOCKED_DOCUMENT_WRITE_REQUESTED
BLOCKED_ARTIFACT_EXPORT_REQUESTED
BLOCKED_CANONICAL_GRAPH_WRITE_REQUESTED
BLOCKED_SOURCE_SUMMARY_REWRITE_REQUESTED
BLOCKED_FORBIDDEN_EXPORT_CAPABILITY
BLOCKED_MISSING_OPERATOR_REVIEW_POLICY
```
