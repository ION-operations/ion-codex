# Agent Context Branches

Status: active provisional branch-capsule lane
Created: 2026-05-11

This folder holds per-conversation and per-agent branch capsules.

Branch capsules are local working context. They are not settled shared ION memory.

Protocol:

```text
ION/02_architecture/ION_AGENT_BRANCH_CAPSULE_PROTOCOL_V0_1.md
```

Settlement protocol:

```text
ION/02_architecture/ION_MULTI_AGENT_CONTEXT_AND_WORKPACKET_SETTLEMENT_PROTOCOL_V0_1.md
```

Core law:

```text
Every active agent/conversation gets a unique branch capsule.
Shared Codex solo Capsule is read-only base context.
Only context settlement merges branch results into shared context.
```

Folder pattern:

```text
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

Templates live in:

```text
templates/
```

Do not manually assign `C-###` checkpoints from branch capsules.
