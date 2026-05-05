---
type: architecture_protocol
authority: A3_OPERATIONAL
created: 2026-04-08T23:50:00-04:00
status: ACTIVE
purpose: Normalize the canonical markdown packet families used for human/executor continuity so takeover, review, and manual fallback follow one legible law
connections:
  - ION/01_doctrine/CANONICAL_WORKFLOW.md
  - ION/AGENT_CONTRACT.md
  - ION/02_architecture/BRIDGE_PACKET_STATUS_CLARIFICATION.md
  - ION/02_architecture/HANDOFF_TAKEOVER_NORMALIZATION_PROTOCOL.md
  - ION/02_architecture/MANUAL_AUTOMATION_FALLBACK_PROTOCOL.md
  - ION/02_architecture/OPERATOR_ENTRY_SURFACE_PROTOCOL.md
  - ION/02_architecture/ROLE_CHASSIS_MOUNT_PROTOCOL.md
  - ION/02_architecture/DISAGREEMENT_ESCALATION_PROTOCOL.md
  - ION/02_architecture/EXTERNAL_ZIP_RETURN_BRIDGE_PROTOCOL.md
  - ION/02_architecture/WORKING_AGENT_SELF_USE_PROTOCOL.md
  - ION/07_templates/actions/TASK.md
  - ION/07_templates/actions/ROLE_SESSION.md
  - ION/07_templates/actions/HANDOFF.md
  - ION/07_templates/actions/CURSOR_HANDOFF.md
  - ION/07_templates/actions/MANUAL_AUTOMATION_FALLBACK.md
  - ION/07_templates/actions/ROLE_CHASSIS_MOUNT.md
  - ION/07_templates/actions/DISAGREEMENT_ESCALATION.md
  - ION/07_templates/actions/EXTERNAL_RETURN.md
  - ION/04_packages/kernel/packet_validation.py
---

# Packet and Handoff Standardization Protocol

## Principle

Workflow packets are not prose convenience. They are bounded continuity carriers.

A lawful packet family should let a fresh capable executor understand:
- what kind of packet it is,
- what it is allowed to mean,
- what exact action it is requesting or recording,
- and what should happen next without hidden oral context.

## Scope

This protocol governs the human/executor markdown packet families used in the canonical workflow.

It does **not** replace machine-generated JSON dispatch packets, service receipts, or runtime-report artifacts. Those remain separate generated-state families.

## Canonical packet taxonomy

### 1. `task`
Use for one bounded work assignment.

### 2. `role_session`
Use for one bounded executor/role pass inside a larger run.

### 3. `handoff`
Use for one bounded transfer from one executor/role to another.

### 4. `cursor_handoff`
Use for one IDE/chat-targeted handoff with explicit load order and boundaries.

### 5. `manual_automation_fallback`
Use when the lawful workflow step must be carried manually because an automation carrier is blocked, disabled, unavailable, or intentionally paused.

## Current-phase bridge boundary

This protocol defines the canonical five-family packet floor only.

The current branch also uses these governed current-phase bridge packet types:

- `role_chassis_mount`
- `disagreement_escalation`
- `external_return`

Those bridge packets are active under their own bridge protocols and templates, but they
remain outside the canonical packet taxonomy and outside the current packet-validator
floor.

For the branch's explicit reading of that boundary, see
`ION/02_architecture/BRIDGE_PACKET_STATUS_CLARIFICATION.md`.

## Required frontmatter law

All new canonical packets in these families should begin with frontmatter.

Minimum shared fields:
- `type`
- `template`
- `created`
- `status`

Family-specific required fields:

### `task`
- `agent`
- `priority`
- `from`
- `target`

### `role_session`
- `role`
- `objective`

### `handoff`
- `from`
- `to`
- `objective`

### `cursor_handoff`
- `target_surface`
- `objective`

### `manual_automation_fallback`
- `automation_surface`
- `reason`

## Required body law

### `task`
- Goal
- Source / Context
- Requirements
- Deliverables
- Constraints
- Completion Signal

### `role_session`
- Role
- Purpose
- Source Task / Objective
- Required Reads
- Expected Output
- Next Target
- Notes

### `handoff`
- From
- To
- What was completed
- What remains
- Exact artifacts to read
- Risks / warnings
- Requested next action

### `cursor_handoff`
- Role / chassis target
- Load order
- Exact files to read first
- Task to perform
- Boundaries
- Expected output artifact

### `manual_automation_fallback`
- Carrier blocked or disabled
- Lawful bounded inputs
- Manual fallback step
- Outputs emitted

## Legacy compatibility

Older packet surfaces may still exist without frontmatter or with thinner headings.
Those should be treated as legacy packets rather than silently redefined as canonical.

Validation helpers may therefore support a legacy-tolerant mode for archaeology and migration,
but all newly created canonical packets should satisfy the stricter normalized form.

## Validation law

Normalized packets should be machine-checkable for:
- packet-family recognition,
- required frontmatter presence,
- required heading presence,
- and obvious type/title mismatches.

The packet validator is a support surface. It does not confer authority; it only checks conformance.

For current-phase bridge packets, an `UNSUPPORTED_TYPE` result should be read as "outside
the canonical validator floor" rather than as an automatic claim that the packet is
unlawful.

## Takeover assessment law

Continuation-normalized packets should also be assessable for bounded takeover sufficiency.

The current continuation-normalized families are:
- `handoff`
- `cursor_handoff`
- `role_session`
- `manual_automation_fallback`

Those families may now emit durable takeover-assessment receipts under the L2 takeover protocol.

`task` remains canonical, but it is not yet guaranteed takeover-sufficient by law.
That insufficiency should stay visible rather than being silently guessed away.

## Working-agent self-use link

The working agent should use these same packet families on itself during meaningful passes.
That means the builder should leave normalized role-session, handoff, and fallback artifacts when the pass warrants them.

## Canonical examples

### Example `role_session`

```markdown
---
type: role_session
template: ROLE_SESSION
created: 2026-04-08T23:50:00-04:00
status: COMPLETE
role: Steward
objective: Normalize packet taxonomy for the current root
---

# Role Session: Steward

## Role
Current-phase orchestration steward.

## Purpose
Land K2 packet and handoff standardization.

## Source Task / Objective
Normalize the packet families used for takeover and manual fallback.

## Required Reads
- `ION/MASTER_ORCHESTRATION_INDEX.md`
- `ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md`

## Expected Output
Protocol, validator, tests, and updated templates.

## Next Target
Handoff to the next K3 horizon-groundwork executor.

## Notes
One bounded completion packet only.
```

### Example `handoff`

```markdown
---
type: handoff
template: HANDOFF
created: 2026-04-08T23:55:00-04:00
status: ACTIVE
from: Steward
to: Next executor
objective: Start K3 horizon groundwork from a normalized packet floor
---

# Handoff: K3 Horizon Groundwork

## From
Steward.

## To
Next executor.

## What was completed
K2 packet and handoff standardization landed.

## What remains
K3 horizon record and tightening groundwork.

## Exact artifacts to read
- `ION/06_intelligence/research/2026-04-08_k3_horizon_groundwork_next_workload_plan.md`

## Risks / warnings
Do not widen packet taxonomy beyond the canonical families without explicit need.

## Requested next action
Implement the living horizon state family and its proof surfaces.
```

## Success condition

Packet meaning should become quickly inferable, validation should be available, and a fresh executor should need less hidden context to continue the same lawful loop.

## Activation-boundary clarification

Packet legality and handoff legibility prove that a work artifact is bounded, interpretable, and continuity-safe.
They do **not** by themselves authorize enactment crossing.
A lawful packet may therefore remain packet-valid yet activation-denied, activation-deferred, or activation-escalated until `ION/02_architecture/ACTIVATION_AUTHORITY_PROTOCOL.md` has been satisfied.
