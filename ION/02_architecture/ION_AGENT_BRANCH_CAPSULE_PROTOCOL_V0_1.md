# ION Agent Branch Capsule Protocol v0.1

Status: active provisional protocol
Created: 2026-05-11
Authority: context isolation and settlement workflow only
Production authority: false
Live execution authority: false

## Purpose

This protocol prevents wrong-context work by giving every active conversation and agent its own uniquely named context capsule branch.

The shared Codex solo Capsule remains settled base context. It is not a multi-agent scratchpad.

## Core law

Every active agent/conversation must operate from a unique branch capsule.

```text
shared context = settled base memory
branch capsule = local working memory for one conversation/agent/task
settlement = only path back to shared context
```

Agents must not write directly into shared context:

```text
ION/05_context/current/codex_solo/CAPSULE.md
ION/05_context/current/codex_solo/MINI.md
ION/05_context/current/codex_solo/HOT_CONTEXT.md
ION/05_context/current/codex_solo/STATUS.json
ION/05_context/current/codex_solo/ROUTE.json
```

## Relationship to settlement protocol

This protocol extends:

```text
ION/02_architecture/ION_MULTI_AGENT_CONTEXT_AND_WORKPACKET_SETTLEMENT_PROTOCOL_V0_1.md
```

Branch capsules produce candidate receipts and settlement packets. The context settler serializes accepted updates into shared context.

## Branch hierarchy

Use this lineage model:

```text
GLOBAL ION CONTEXT
  -> project/session capsule
    -> conversation capsule
      -> agent branch capsule
        -> task/workpacket capsule
```

Each branch names its parent explicitly. Branches may inherit from parents, but they cannot overwrite parents.

## Required identity fields

Every branch capsule requires:

```json
{
  "context_instance_id": "ctx_YYYYMMDDTHHMMSSZ_agent_or_task",
  "branch_id": "branch_YYYYMMDDTHHMMSSZ_agent_or_task",
  "branch_type": "conversation|agent|task|workpacket",
  "agent_tag": "codex_ui_recovery",
  "conversation_tag": "helixion_joc_recovery",
  "task_tag": "anchored_pages_recovery",
  "parent_context_id": "ctx_shared_codex_solo_current",
  "root": "/home/sev/ION - Production/ION_CODEX FULL",
  "loaded_refs": [],
  "write_scope": [],
  "shared_context_write": false,
  "settlement_required": true
}
```

## Required startup identity card

Every agent should expose a short identity card before material work:

```text
AGENT_TAG: codex_ui_recovery
CONVERSATION_TAG: helixion_joc_recovery
TASK_TAG: anchored_pages_recovery
CONTEXT_INSTANCE: ctx_20260511T150210Z_codex_ui_recovery
BRANCH_ID: branch_20260511T150210Z_codex_ui_recovery
PARENT_CONTEXT: ctx_shared_codex_solo_current
ROOT: /home/sev/ION - Production/ION_CODEX FULL
SHARED_CONTEXT_WRITE: false
SETTLEMENT_REQUIRED: true
```

If the agent cannot name these fields, it must treat itself as unmounted and request or create a branch capsule before continuing.

## Branch folder layout

```text
ION/05_context/current/agent_context_branches/
  README.md
  BRANCH_CAPSULE_REGISTRY_V0_1.json
  templates/
    AGENT_BRANCH_CAPSULE.template.md
    AGENT_BRANCH_STATUS.template.json
    AGENT_CONTEXT_IDENTITY_CARD.template.md
  <conversation_tag>/
    <agent_tag>/
      CAPSULE.md
      MINI.md
      STATUS.json
      LOADED_REFS.json
      RECEIPTS/
      TASK_RETURNS/
      SETTLEMENT_REQUESTS/
```

## Branch capsule rules

Branch capsules may contain:

```text
local task summary
loaded refs
agent-specific assumptions
work scope
candidate receipts
task returns
non-claims
settlement requests
```

Branch capsules must not contain:

```text
accepted shared C-number assignments
claims of shared current state
production authority
live execution authority
secrets
credential material
hidden chain of thought
unverified visual proof claims
```

## Wrong-context detection

An agent is in drift if any of these are true:

```text
missing context_instance_id
missing conversation_tag
missing agent_tag
parent_context_id unknown
root does not match current active ION root
loaded refs do not include required parent route/capsule proof
write scope overlaps another active claim
branch status says blocked/drifted
agent attempts to write shared context directly
agent assigns C-number directly
```

Drift outcome:

```text
stop material writes
write branch drift receipt
submit context_settlement conflict packet
await settlement or operator direction
```

## Settlement request flow

```text
agent branch capsule
-> candidate receipt/task return
-> branch SETTLEMENT_REQUESTS/
-> context_settlement/inbox/
-> context settler review
-> accepted/conflict/deferred outcome
-> shared context update only by settler
```

## Naming rules

Use stable, readable tags:

```text
conversation_tag = product_or_session_name
agent_tag = role_or_lane_name
task_tag = bounded_objective
branch_id = branch_<utc_timestamp>_<agent_tag>
context_instance_id = ctx_<utc_timestamp>_<agent_tag>
```

Examples:

```text
conversation_tag: helixion_joc_recovery
agent_tag: codex_ui_recovery
task_tag: anchored_pages_drawer_canon
branch_id: branch_20260511T150210Z_codex_ui_recovery
```

## Branch-to-branch lineage

One branch may fork another branch only when it records:

```text
parent_branch_id
fork_reason
refs_inherited
refs_excluded
authority_boundary
settlement_target
```

Forked branches do not inherit write authority. They inherit evidence only.

## Human-visible UI implication

The Helixion/JOC/dAimon cockpit should eventually show:

```text
active agents
their branch names
parent context
loaded refs
write scope
drift status
settlement status
latest receipt
```

This makes wrong-context issues visible to the operator and to the AI chat.

## Non-claims

This protocol does not:

```text
create a settled branch for the current conversation
move existing agents into branches
resolve the C-088 conflict
update shared Capsule/Mini/HOT_CONTEXT
run tests
reload services
grant production or live execution authority
```

## Required next implementation lane

Future implementation should add:

```text
branch creation helper
branch registry validator
context identity card renderer
settlement request generator
wrong-context drift detector
cockpit branch visibility page/drawer
```

These are separate implementation packets and must not bypass settlement.
