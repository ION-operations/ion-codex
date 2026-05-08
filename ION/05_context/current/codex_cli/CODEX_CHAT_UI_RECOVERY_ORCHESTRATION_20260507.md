---
type: recovery_orchestration
authority: A3_OPERATIONAL
created: 2026-05-07
status: ACTIVE
production_authority: false
live_execution_authority: false
---

# Codex Chat UI Recovery Orchestration

## Trigger

Operator feedback on 2026-05-07 identified a product framing failure in the
chat UI:

- the screen looked like "chat with Capsule" instead of Codex chat using
  Capsule context;
- the composer exposed both `Send` and `Run with Codex`, creating two competing
  primary actions;
- the inspector presented too much internal material at once;
- lane/queue/pin style control language from the earlier failed UI must not
  return as the primary workflow.

## Corrected Mental Model

The product surface is:

```text
Codex Chat
  uses Capsule/Mini/HOT_CONTEXT/context packages behind the scenes
  can queue proof-gated work through the existing Codex owner
  can communicate with full ION through existing ION comms/receipts
```

The user should not feel like they are editing Capsule. Capsule is evidence and
working context, not the person they are chatting with.

## UI Rules

- The first visible product name is `ION Codex Chat`.
- The chat region is labelled `Codex Chat`.
- The text area says `Ask Codex`.
- The composer has one submit button: `Send`.
- Execution posture is a mode choice: `Chat` or `Run task`.
- Context, Timeline, Agents, Runs, Receipts, ION, and Settings are support
  drawers, collapsed by default.
- The `capsule` drawer key remains only as a compatibility alias for internal
  model consumers; the visible drawer is `Context`.

## Non-Goals

- no manual lane chores as the user-facing workflow;
- no separate queue or second agent system;
- no claim of production/live authority;
- no raw hidden reasoning display;
- no removal of Capsule as the context substrate.

## Acceptance

- rendered `/chat` HTML contains `ION Codex Chat`, `Ask Codex`,
  `composer-mode`, `Chat`, and `Run task`;
- rendered `/chat` HTML does not contain `Codex Capsule Chat`,
  `Message Codex Capsule`, or `Run with Codex`;
- the right inspector uses collapsed `details.inspector-card` drawers;
- focused tests cover the corrected labels and compatibility drawer alias.
