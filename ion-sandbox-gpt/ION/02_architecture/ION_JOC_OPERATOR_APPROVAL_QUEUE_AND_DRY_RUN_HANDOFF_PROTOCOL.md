# ION/JOC Operator Approval Queue and Dry-Run Dispatch Handoff Protocol

## Version

`V62_OPERATOR_APPROVAL_QUEUE_AND_DRY_RUN_HANDOFF`

## Intent

V62 turns a V61 dispatch authorization view model into an explicit operator approval checkpoint. The checkpoint is visible in the cockpit and can emit a dry-run handoff preview, but it cannot execute provider calls.

## Workflow

```text
V59 route preview
→ V61 dispatch authorization verdict
→ V62 operator approval queue card
→ operator decision state
→ dry-run handoff receipt preview
→ future live driver branch, if separately authorized
```

## Approval states

```text
QUEUED_FOR_OPERATOR_REVIEW
BLOCKED_AUTHORIZATION_NOT_APPROVABLE
BLOCKED_MISSING_AUTHORIZATION_EVIDENCE
BLOCKED_MISSING_OPERATOR_APPROVAL_EVIDENCE
OPERATOR_DENIED
DRY_RUN_HANDOFF_READY
EXPIRED_REQUIRES_REVIEW_REFRESH
```

## UI surfaces

```text
OPERATOR_APPROVAL_QUEUE
GOVERNOR_EVIDENCE_RAIL
APPROVAL_DECISION_CARD
DENIAL_REASON_LANE
DRY_RUN_HANDOFF_PREVIEW
NON_AUTHORITY_BOUNDARY_STRIP
```

## Rule

A human approval must be explicit, scoped, and evidenced. Even when approved, V62 can only prepare a dry-run handoff receipt.

## Forbidden actions

```text
live_external_model_dispatch
browser_session_mutation
credential_access
form_submission
paid_cloud_launch
source_summary_rewrite
canonical_graph_write
unrestricted_agent_activation
production_authority
```
