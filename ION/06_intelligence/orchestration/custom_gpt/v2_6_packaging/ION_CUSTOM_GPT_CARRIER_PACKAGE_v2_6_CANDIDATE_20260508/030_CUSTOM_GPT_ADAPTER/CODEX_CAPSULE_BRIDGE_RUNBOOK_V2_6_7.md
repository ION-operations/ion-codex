# Codex Capsule Bridge Runbook v2.6.7

## Goal

Run a bounded GPT <-> Codex Capsule coordination loop without manual paste for
routine relay.

## Standard Flow

1. Read lane state with `ion_codex_capsule_chat_status`.
2. Send work intent with `ion_codex_capsule_message_send`.
3. Poll response with `ion_codex_capsule_message_poll` until settled or blocked.
4. If queue execution is required, create bounded queue work with
   `ion_codex_capsule_sync_to_queue`.
5. Report visible non-claims: candidate vs accepted state.

## When To Use Queue Sync

Use queue sync only when the requested work needs Codex queue runner execution
or proof-return artifacts. For read-only or conversational coordination, stay in
Capsule lane and do not sync to queue.

## Required Boundaries

- Never claim background execution without telemetry or receipts.
- Never treat capsule message text as accepted state by itself.
- Preserve project/package context in the message body so the Codex lane can
  prove continuity.
