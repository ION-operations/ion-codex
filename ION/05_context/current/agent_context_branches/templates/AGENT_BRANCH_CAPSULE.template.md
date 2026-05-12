# Agent Branch Capsule

schema_id: ion.agent_branch_capsule.markdown.v1
status: BRANCH_WORKING_CONTEXT
production_authority: false
live_execution_authority: false
secrets_authority: false

## Identity

AGENT_TAG: `<agent_tag>`
CONVERSATION_TAG: `<conversation_tag>`
TASK_TAG: `<task_tag>`
CONTEXT_INSTANCE: `<ctx_YYYYMMDDTHHMMSSZ_agent_tag>`
BRANCH_ID: `<branch_YYYYMMDDTHHMMSSZ_agent_tag>`
BRANCH_TYPE: `<conversation|agent|task|workpacket>`
PARENT_CONTEXT: `<parent_context_id>`
PARENT_BRANCH: `<parent_branch_id_or_none>`
ROOT: `/home/sev/ION - Production/ION_CODEX FULL`
SHARED_CONTEXT_WRITE: false
SETTLEMENT_REQUIRED: true

## Loaded refs

```text
<repo-relative refs loaded by this branch>
```

## Write scope

```text
<repo-relative paths this branch may edit>
```

## Current objective

```text
<bounded task objective>
```

## Local branch memory

```text
<task-local observations and decisions>
```

## Candidate receipts

```text
<receipt refs produced by this branch>
```

## Settlement requests

```text
<settlement inbox refs or branch-local settlement requests>
```

## Drift status

```text
DRIFT_STATUS: clear|blocked|drift_detected
FINDINGS:
- <finding>
```

## Non-claims

```text
This branch capsule is not shared accepted context.
This branch capsule does not assign C-numbers.
This branch capsule does not grant production/live/secrets authority.
```
