---
type: protocol_stub
authority: A3_PROPOSED
status: DRAFT_NON_PRODUCTION
created: 2026-05-05
production_authority: false
live_execution_authority: false
---

> Operational mount order is governed by `ION/02_architecture/ION_MOUNT_CONTRACT.md`.

# ION ChatOps YAML Action Protocol

## Purpose

This protocol defines the machine-readable action block Sev can emit in ChatGPT
Browser when MCP is absent, stale, or too fragile for large payloads.

ChatGPT text is the protocol surface. The browser extension detects fenced YAML
blocks containing `ion_action:`, validates them, asks Braden for approval, and
posts approved JSON to the local ChatOps daemon.

YAML actions are carrier packets for the same ION core engine used by other
carriers. They are not a new authority language and they do not bypass ION
proof gates, Steward integration, task returns, or receipt rules.

## Action Shape

```yaml
ion_action:
  schema: ion.chatops.action.v1
  action_id: sev-YYYYMMDD-HHMMSS-slug
  intent: write_file_draft
  actor:
    callsign: Sev
    carrier: chatgpt_browser
  authority:
    human_sovereign: Braden
    requires_approval: true
    production_authority: false
    live_execution_authority: false
  target: {}
  content: {}
  context_refs: []
  receipts:
    requested: []
```

## Required Fields

- `schema: ion.chatops.action.v1`
- `action_id`
- `intent`
- `actor.callsign: Sev`
- `actor.carrier: chatgpt_browser`
- `authority.human_sovereign: Braden`
- `authority.requires_approval`
- `authority.production_authority: false`
- `receipts.requested`

## Supported MVP Intents

```text
register_artifact
write_file_draft
create_codex_work_packet
create_github_issue_draft
```

Aliases accepted by the local daemon:

```text
create_github_issue -> create_github_issue_draft
```

## Later Intents

```text
invoke_agent
create_github_branch_plan
request_git_diff
request_status
apply_patch
commit_branch
push_scoped_branch
open_pull_request
run_tests
cancel_agent
ack_receipt
```

Later intents remain blocked until policy, tests, and receipts exist.

## Hard-Gated Intents

```text
delete_file
overwrite_protected_file
push_main
access_credential
production_deploy
broad_shell
```

## Approval

Mutating actions require Braden approval through the extension UI before
submission. The MVP daemon checks:

```yaml
approval:
  approved: true
  approved_by: Braden
  approval_token: ION_CHATOPS_APPROVED
```

The approval token is not a credential. It is local ceremony evidence that the
extension showed the action to Braden.

## Receipts

Daemon receipts use:

```yaml
ion_chatops_receipt:
  schema: ion.chatops.receipt.v1
  receipt_id: string
  action_id: string
  created_at: iso8601
  actor:
    callsign: Sev
    carrier: chatgpt_browser
  approved_by: Braden
  intent: string
  status: accepted|rejected|completed|failed
  target_refs: []
  files_touched: []
  github_refs: []
  sha256: {}
  validation: {}
  failure_classification: null
```

## Failure Classes

```text
CHATOPS_SCHEMA_FAILURE
USER_APPROVAL_REJECTED
LOCAL_DAEMON_FAILURE
GITHUB_DATA_PLANE_FAILURE
ION_PACKET_WRITE_FAILURE
CODEX_BACKEND_FAILURE
CARRIER_ADAPTER_FAILURE
ION_CORE_FAILURE
POLICY_BLOCK_WORKING_AS_DESIGNED
```
