# ION MCP Front Door and Mount Session Protocol

## Version

`V63_ION_MCP_MOUNT_AND_ACCOUNT_CONNECTION_PROTOCOL`

## Purpose

Define how MCP may be used as ION's governed front door for ChatGPT, Codex, Cursor, VS Code, Claude, local agents, and future AI clients.

MCP is an access membrane. It is not the ION kernel, not the scheduler, not the receipt ledger, not the approval authority, and not the execution engine.

## Core law

1. MCP is subordinate to ION kernel truth, doctrine, receipts, and operator control.
2. MCP may expose resources, tools, prompts, and future UI surfaces, but those surfaces are projections and request channels unless separately promoted by ION law.
3. MCP may create or resume an ION mount session only through a validated mount packet.
4. MCP tools may not mutate kernel truth directly.
5. MCP tools may not bypass the operator approval queue.
6. MCP tools may not authorize provider calls, browser mutation, paid cloud launch, credential access, or production deployment in V63.
7. Returned tool outputs must enter ION as receipts, plans, dry-run artifacts, approval requests, or proposed deltas.
8. Every mount, scope grant, denial, plan, job submission, approval request, export, import, and unmount must be receipt-addressable.

## Design position

The ZIP is the current portable state-carrier. MCP becomes the live mount-port.

```text
Today:
  upload zip → agent inspects project → agent infers state

V63 direction:
  connect MCP → ion.mount → ION returns boot packet → agent operates through tools
```

## Client classes

### Local founder / IDE client

```text
transport: stdio or localhost Streamable HTTP
state: local filesystem state root
identity: local operator or environment token
risk: raw source protection is weaker, local power is high
use: founder workflow, Codex CLI, Cursor, VS Code, local agents
```

### Hosted AI client

```text
transport: remote Streamable HTTP
state: hosted tenant workspace
identity: OAuth / account-scoped token
risk: multi-tenant security and cloud cost
use: ChatGPT custom app, cloud IDE agents, remote Claude/Codex clients
```

### Enterprise / sovereign deployment

```text
transport: private remote endpoint or VPC-local MCP
state: dedicated org workspace or isolated deployment
identity: enterprise auth, service actors, operator roles
risk: compliance, isolation, audit depth
use: organizations and research labs
```

## Mount lifecycle

```text
1. MCP protocol initialize occurs.
2. Client discovers tools/resources/prompts.
3. Client calls ion.mount with a mount packet.
4. ION validates account/user/workspace/state-root and requested scopes.
5. ION binds or resumes a runtime session.
6. ION emits a mount receipt.
7. ION returns a session object and boot packet handles.
8. All future calls are bound to the mounted session.
9. Privileged requests produce approval queue items or refusals.
10. Unmount closes or pauses the session and emits a receipt.
```

## Required mount packet fields

```text
version
client.name
client.transport
client.capabilities
actor.user_id
actor.org_id optional
actor.workspace_role optional
workspace.workspace_id
workspace.state_root_hint optional
requested_scopes
requested_mode
resume.session_id optional
resume.event_cursor optional
approval_context optional
roots optional for local selected roots
metadata optional
```

## Session object fields

```text
version
session_id
transport_session_id optional
workspace_id
subject.user_id
subject.org_id optional
subject.role optional
granted_scopes
denied_scopes
execution_mode
state_root
event_cursor
approval_queue_ref
receipts_resource_uri
jobs_resource_uri
resource_uris
tool_names
prompt_names
created_at
last_seen_at
expires_at
policy_version
```

## Mandatory MCP resources

Resources are observability surfaces, not authority surfaces.

```text
ion://session/current
ion://boot/current
ion://workspace/current/state-root
ion://workspace/current/horizon
ion://workspace/current/manifest
ion://workspace/current/approvals
ion://workspace/current/jobs
ion://workspace/current/receipts
ion://workspace/current/bundles
ion://workspace/current/policies
```

## Mandatory MCP tools

V63 baseline tools:

```text
ion.mount
ion.session.get
ion.session.unmount
ion.boot_packet.get
ion.state.current
ion.horizon.current
ion.receipts.list
ion.receipt.get
ion.approvals.list
ion.job.plan
ion.job.submit_dry_run
ion.bundle.export_preview
ion.scope.request
```

Forbidden or future-only tools:

```text
ion.job.execute_live
ion.operator.approve_live
ion.secrets.write
ion.browser.mutate
ion.provider.dispatch
ion.workspace.admin_destructive
ion.kernel.write_direct
```

## Tool result law

Every tool result must declare one execution resolution:

```text
READ_ONLY
DRY_RUN
APPROVAL_REQUIRED
REFUSED
```

The following result is forbidden in V63:

```text
LIVE_EXECUTED
```

## Scope model

Baseline scopes:

```text
ion.mount.basic
ion.state.read
ion.horizon.read
ion.receipts.read
ion.approvals.read
ion.jobs.plan
ion.jobs.submit_dry_run
ion.bundles.export_preview
```

Privileged/future scopes:

```text
ion.approvals.write
ion.jobs.execute.live
ion.provider.call
ion.browser.mutate
ion.secrets.read
ion.secrets.write
ion.workspace.admin
ion.kernel.write
```

## Boot packet law

After mount, the first returned ION-native artifact should be a boot packet. The boot packet must tell the agent:

```text
who/what is mounted
which workspace/state root is active
current branch/version posture
current horizon
allowed scopes/tools
blocked scopes/tools
first required calls
forbidden claims/actions
receipt and approval handles
```

The boot packet replaces the need for the agent to infer live state from a full ZIP scan in every session.

## Required first-call discipline

Any mounted AI agent must begin with:

```text
ion.mount
ion.boot_packet.get
ion.horizon.current
ion.state.current or ion.session.get
```

Then it may request context or propose a dry-run job.

## MCP bypass prohibition

MCP may not:

```text
write canonical graph state directly
write governed source directly
mark a job executed without queue/receipt chain
reuse stale approval against a changed state root
escalate scope without an explicit policy result
interpret external client confirmation as ION approval
commit returned execution output directly
```

## Relationship to existing ION surfaces

```text
runtime_session_store.py         → session substrate
api_runtime_entry.py             → external/API carrier entry precedent
front_door_self_mount_binding.py → mount identity/provenance precedent
external_execution_bridge.py     → external execution boundary precedent
joc_operator_approval_queue_*    → approval checkpoint authority
receipts.py                      → receipt family substrate
store.py                         → local filesystem state substrate
```

## Branch rule

V63 may prove that ION can be mounted. V63 may not prove live autonomous execution.
