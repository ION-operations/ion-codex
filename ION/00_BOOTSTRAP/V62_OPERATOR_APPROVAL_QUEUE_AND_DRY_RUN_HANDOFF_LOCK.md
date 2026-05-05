# V62 Operator Approval Queue and Dry-Run Dispatch Handoff Lock

**Branch:** `V62_OPERATOR_APPROVAL_QUEUE_AND_DRY_RUN_HANDOFF`  
**Date:** 2026-04-26  
**Authority posture:** UI/runtime projection only. No live provider dispatch, browser mutation, credential access, paid cloud launch, or production authority.

## Purpose

V62 binds V61 dispatch authorization verdicts into an operator-visible approval queue and dry-run handoff preview.

The branch preserves the V61 rule:

```text
A visible dispatch route is not dispatch authority.
```

V62 adds the next rule:

```text
A supervised approval card is not execution. It is an auditable checkpoint that may produce a dry-run handoff receipt only.
```

## Required surfaces

```text
ION/02_architecture/ION_JOC_OPERATOR_APPROVAL_QUEUE_AND_DRY_RUN_HANDOFF_PROTOCOL.md
ION/03_registry/joc_operator_approval_queue.schema.json
ION/03_registry/joc_operator_approval_policy.yaml
ION/04_packages/kernel/joc_operator_approval_queue_view_model.py
ION/tests/test_kernel_joc_operator_approval_queue_view_model.py
ION/08_ui/joc_cockpit_shell/operatorApprovalTypes.ts
ION/08_ui/joc_cockpit_shell/OperatorApprovalQueuePanel.tsx
ION/08_ui/joc_cockpit_shell/DryRunDispatchHandoffPanel.tsx
ION/08_ui/joc_cockpit_shell/operator-approval.css
ION/docs/ui/ION_JOC_OPERATOR_APPROVAL_AND_DRY_RUN_HANDOFF_CANON.md
```

## Non-authority boundary

V62 may render approval state, denial state, missing-evidence state, and dry-run handoff readiness. It may not call a provider, mutate a browser session, access credentials, submit a form, spend money, or claim production readiness.
