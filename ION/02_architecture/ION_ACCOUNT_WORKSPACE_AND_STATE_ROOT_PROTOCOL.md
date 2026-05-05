# ION Account, Workspace, and State Root Protocol

## Version

`V63_ION_ACCOUNT_WORKSPACE_AND_STATE_ROOT_PROTOCOL`

## Purpose

Define the product-state model required for ION to move from portable ZIPs to account-connected local and hosted operation.

The protocol separates ION core software from user-specific ION state.

## Core distinction

```text
ION Core
  protected kernel, doctrine, schemas, tests, cockpit, MCP server, release logic

ION State
  user/workspace-specific continuity, files, receipts, queues, context indexes,
  decisions, bundles, event logs, branch posture, and state roots

ION MCP
  governed mount/control interface between AI clients and ION core/state

ION Cloud
  hosted account, storage, policy, queue, worker, billing, and isolation layer
```

## Product rule

Each user should not receive a fork of the whole ION codebase as their default ION. Each user should receive a governed state instance mounted onto a versioned ION core.

## Identity hierarchy

```text
account
  → organization
    → workspace
      → state_root
        → project
          → branch
            → horizon
              → session
                → job / approval / receipt
```

## Workspace

A workspace is the tenant/project boundary. It owns:

```text
state roots
event log
receipts
operator approval queue
job queue metadata
context indexes
bundle exports/imports
connected repositories or local roots
policy profile
model/provider settings
role bindings
```

## State root

A state root is a content-addressed or integrity-addressed snapshot of the workspace's canonical continuity state.

A state root should include or reference:

```text
manifest
branch/version posture
active horizon
runtime/session state
approval queue state
job state
receipt ledger cursor
context indexes
selected file manifests
bundle/import/export metadata
policy versions
```

## Event log

Every important transition appends an event:

```text
workspace_created
state_imported
state_exported
mount_started
mount_resumed
scope_granted
scope_denied
boot_packet_emitted
job_planned
job_submitted_dry_run
approval_requested
operator_decision_recorded
execution_return_received
state_root_promoted
rollback_requested
rollback_completed
session_unmounted
```

## Receipt ledger

Receipts are the audit-visible commitments over events and state transitions. They must be sufficient to answer:

```text
who requested the action
which client/session requested it
which state root it referenced
which scopes were granted or denied
which policy version applied
which evidence was used
what result was produced
whether the result changed canonical state
```

## Bundle relationship

A bundle is the portable form of selected state roots, events, receipts, and manifests. The current ZIP workflow should evolve into a formal bundle system.

A bundle must not be treated as a loose archive. It must validate against:

```text
bundle schema
state-root manifest
file hashes or integrity records
receipt/event chain
policy/schema versions
export scope
import target compatibility
```

## Hosted storage split

Recommended hosted responsibilities:

```text
Postgres:
  accounts, orgs, workspaces, role bindings, sessions, approvals, jobs,
  receipt index, state-root metadata, policy versions

Object storage:
  bundles, receipts, snapshots, exported zips, imported archives, large files,
  evidence packets

Queue:
  dry-run jobs, export/import jobs, future execution jobs, replay/rollback jobs

Vault:
  user secrets, provider tokens, local bridge credentials, service tokens
```

## Local storage split

Local founder/developer mode may preserve the current filesystem-centered model. It should still formalize:

```text
state root path
runtime session path
receipt path
bundle export path
selected local roots
local token/identity source
approval queue path
```

## Authority rules

1. Account login is not execution authority.
2. Workspace membership is not execution authority.
3. A mounted session is not execution authority.
4. A state root is not mutable without a governed event and receipt.
5. A bundle import is not accepted until validation succeeds.
6. A live approval is valid only for the exact job, state root, scope set, and policy version it approved.
7. A cloud worker may not promote state without receipt chain validation.

## Product onboarding target

A non-founder user should eventually experience:

```text
create account
create workspace
import zip / connect repo / connect local bridge
ION indexes state and emits first state root
connect AI client through MCP
agent calls ion.mount
ION returns boot packet and current horizon
agent works through dry-run and approval surfaces
```

## Non-goals for V63

```text
no full hosted SaaS implementation
no multi-tenant execution plane
no live model dispatch
no credential vault implementation
no Kubernetes deployment
no paid cloud launch
```
