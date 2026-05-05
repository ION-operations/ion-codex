# ION Work Packet — Codex Agent Cockpit

## Status

`PROPOSED_WORK_PACKET`

## Objective

Expose Codex CLI as a bounded local worker lane inside the ChatGPT browser extension cockpit.

Codex must remain controlled by the local daemon/ION kernel. The extension commands, inspects, approves, and displays. Codex does not live inside the extension.

## Architecture

```text
ChatGPT DOM cockpit
-> extension background bridge
-> local ION daemon
-> Codex queue
-> Codex CLI worker
-> proof-bearing return
-> task return intake
-> Steward integration queue
-> receipt/status back to extension
```

## Scope

Implement UI and bridge calls for:

```text
Codex queue status
queued/running/blocked/returned/accepted/superseded states
request bounded Codex work packet
preview objective before enqueue
show latest Codex returns
submit return to ION task intake if existing API supports it
open/queue Steward review
logs and diagnostics
```

## Agent Tab Behavior

The Agent tab should show:

```text
ION daemon status
Codex queue count
running item if any
recent returns
blocked returns
action buttons:
  - request Codex work
  - refresh queue
  - view latest return
  - queue review
```

## Required User Approval

Actions requiring explicit approval:

```text
enqueue Codex work
start/process Codex queue
submit task return
queue Steward review
```

The extension may refresh status without approval.

## Work Request Shape

A Codex work request should include:

```text
objective
scope
allowed paths
forbidden actions
expected output
proof obligations
max runtime
requested_by carrier
template/action relation if known
```

## Acceptance Criteria

```text
Agent tab displays Codex queue status from daemon
user can preview bounded work request before enqueue
enqueue uses existing daemon/ION endpoint
queue refresh works
latest return can be viewed
blocked/proof-blocked states are visible, not hidden
no Codex execution starts silently
no raw Codex output is treated as accepted ION state
```

## Validation

```text
daemon offline -> Agent tab shows degraded state
daemon online -> queue status visible
enqueue test bounded no-op objective
confirm queue item appears
process manually or through approved action only
confirm return state is visible
confirm no silent Steward acceptance
```

## Authority Boundary

Allowed:

```text
status reads
approved enqueue
approved queue processing if endpoint exists
approved task-return submission
```

Forbidden:

```text
silent Codex run
silent patch apply
silent git commit/push
secret access
production/deployment changes
```
