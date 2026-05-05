# ION Full Operationalization and Testing Protocol

## Version

`V63_PROTOCOLIZATION__FULL_OPERATIONALIZATION_AND_TESTING`

## Purpose

This protocol turns the post-V62 strategic picture into an ION-native operational map. It defines what is already working, what must still be implemented, what must be tested, and which authority gates must remain closed until a later branch explicitly opens them.

This protocol is not a live-execution grant. It is a readiness and testing law.

## Current branch posture

The current root sits at the V62 boundary:

```text
V59 mission/model route preview
→ V60 UI/model-governor consolidation
→ V61 dispatch authorization/governor verdict
→ V62 operator approval queue
→ dry-run handoff preview
→ future live driver branch only if separately authorized
```

V62 can model a route, project model/provider economics, apply budget and API-rate governors, render a dispatch authorization view model, queue an operator approval card, and produce a dry-run handoff preview. That is not live execution. It is the governed edge immediately before live execution.

## Operational definition

ION is operational when an external or local AI agent can mount a governed ION workspace, receive a bounded boot packet, inspect the current horizon, request or generate a dry-run plan, queue any privileged action for approval, and return all execution results through receipts and proposed deltas without bypassing kernel truth.

ION is production-operational only when this loop survives across local, IDE, MCP, cockpit, and cloud surfaces:

```text
mount
→ bounded context
→ route preview
→ policy/governor verdict
→ approval queue
→ dry-run or authorized execution
→ receipt
→ state-root update
→ rollback/replay evidence
```

## Layered readiness model

### L0 — Doctrine and protocol integrity

ION must preserve the constitutional rule that protocol, templates, receipts, state roots, and approval boundaries outrank convenience. No product surface may claim authority merely because it can display, call, or route a tool.

Required evidence:

```text
SOVEREIGN_CONSTITUTION.md remains authoritative
SOVEREIGN_KERNEL.md remains authoritative
CANONICAL_WORKFLOW.md remains active
relevant architecture protocols are present and indexed
stale aliases and obsolete authority claims are retired or lineage-bound
```

### L1 — Kernel and state substrate

The kernel must provide deterministic local operation, filesystem-backed state, runtime sessions, receipts, queues, route states, governors, and checkpoint surfaces.

Required evidence:

```text
kernel package imports cleanly
operator CLI status works
runtime/session store tests pass
receipt tests pass
route/governor tests pass
bundle/checkpoint integrity tests pass
```

### L2 — Cockpit projection layer

The JOC cockpit may display system state, route projections, approval cards, decision evidence, model route matrices, budget posture, context routes, and dry-run handoff previews. It may not itself become execution authority.

Required evidence:

```text
cockpit component contracts exist
approval queue and dry-run handoff panels exist
frontend package can typecheck and build
UI fixtures match schema surfaces
UI copy states non-authority boundaries visibly
```

### L3 — MCP mount/front-door layer

MCP becomes a governed access membrane for AI clients. It exposes resources, tools, prompts, mount sessions, boot packets, and receipts. It does not replace ION kernel truth and does not create hidden autonomy.

Required evidence:

```text
ion.mount exists
mount/session schema exists
boot packet projection exists
read-only resources exist
job planning is dry-run-first
live requests resolve to APPROVAL_REQUIRED or REFUSED
all mount and tool calls emit receipts
```

### L4 — Local founder/developer execution bridge

The local bridge may run on an operator-controlled computer and expose selected local roots through a local MCP/CLI surface. It remains supervised.

Required evidence:

```text
local root selection is explicit
no arbitrary filesystem expansion is implied
local tests can be requested as jobs
local mutations are dry-run or approval-bound
local export/import checkpoint remains available
```

### L5 — Hosted account/workspace state plane

Hosted ION stores per-user and per-organization state roots, event logs, receipts, bundles, approvals, and job metadata. The hosted plane protects ION core implementation while giving each user a unique ION state instance.

Required evidence:

```text
account/workspace/state-root model exists
tenant state is separated from core source
object storage and database responsibilities are defined
import/export and rollback semantics are deterministic
scopes and roles are explicit
```

### L6 — Isolated execution plane

Cloud execution must be isolated from the MCP control plane. High-risk execution requires hardened containers, microVMs, dedicated VMs, or stronger isolation. Kubernetes is an orchestration candidate, not the first authority surface.

Required evidence:

```text
control plane and execution plane are separated
worker identity and job claims are receipt-bound
network and secret access are policy-bound
untrusted execution is sandboxed
rollback/replay drills exist
```

## Current accepted truth

The current project is not merely a document archive. It contains a kernel package, a CLI, typed runtime/session surfaces, dispatch/authorization view models, approval queue logic, dry-run handoff projection, registry schemas, policies, and a cockpit scaffold.

The current project is also not yet a finished product. The following remain open operational gaps:

```text
fresh full-suite V62 certification receipt
manual index regeneration / count reconciliation
runnable packaged cockpit application
MCP server package
account/workspace/state-root protocol implementation
hosted state plane
live driver rehearsal
sandboxed execution plane
production release packaging
```

## Readiness gates

### Gate A — Protocolized

All relevant surfaces are documented and no live execution authority is claimed.

### Gate B — Locally testable

The kernel imports, selected tests pass, schemas load, policies parse, CLI status works, and mount/session resources can be produced locally.

### Gate C — Locally mountable

An IDE or local AI client can connect through MCP or CLI, call `ion.mount`, read an ION boot packet, list receipts, inspect the current horizon, and request a dry-run plan.

### Gate D — Approval-safe

Every privileged action resolves to one of:

```text
READ_ONLY
DRY_RUN
APPROVAL_REQUIRED
REFUSED
```

No V63 branch may resolve a tool call to `LIVE_EXECUTED`.

### Gate E — Hosted beta

A user account can create or resume a workspace, store a state root, export and import a bundle, and connect a remote MCP client with scoped authorization.

### Gate F — Production candidate

The hosted system supports tenant isolation, rollback, replay, observability, rate/cost governors, operator approvals, supportable upgrades, and signed release artifacts.

## Mandatory test families

```text
T01 doctrine/protocol presence tests
T02 schema validation tests
T03 kernel import and CLI status tests
T04 runtime session store tests
T05 receipt ledger tests
T06 route/model/budget/API governor tests
T07 V61 dispatch authorization tests
T08 V62 operator approval/dry-run tests
T09 MCP mount/session invariant tests
T10 MCP approval-bypass refusal tests
T11 bundle export/import integrity tests
T12 cockpit type/build/schema fixture tests
T13 rollback/replay determinism tests
T14 tenant isolation tests
T15 sandboxed execution boundary tests
```

## Operational invariant

ION must never confuse visibility with authority.

```text
A visible route is not dispatch authority.
A supervised approval card is not execution.
An MCP tool call is not kernel truth.
A returned external payload is not a committed delta.
A hosted account session is not live execution permission.
A Kubernetes worker is not safety.
```

## Next branch implication

The next lawful branch should focus on MCP mount/session protocolization and local read-first implementation before any hosted execution or cloud orchestration.

Recommended branch name:

```text
V63_ION_MCP_MOUNT_AND_ACCOUNT_CONNECTION_PROTOCOL
```
