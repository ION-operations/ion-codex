---
type: implementation_orchestration
authority: A3_OPERATIONAL
created: 2026-05-07
status: ACTIVE
production_authority: false
live_execution_authority: false
---

# Codex Capsule Chat Rebuild Orchestration

## Correction

The product target is not a forced two-chat app.

The target is one primary Codex CLI chat mounted through the Capsule/Mini/HOT_CONTEXT system. Full ION already has its own Relay/Steward/workflow communication surfaces, so the Capsule chat should interoperate with those existing surfaces rather than duplicate them.

## Product Shape

```text
Operator
-> Codex Capsule Chat
-> Capsule / Mini / HOT_CONTEXT / route packages
-> bounded Codex CLI work packets when work needs execution
-> receipts / task returns / Capsule post

Codex Capsule Chat
<-> existing ION comms / queue / receipt owners
<-> full ION Persona / Relay / Steward workflow
```

## Non-Negotiables

- The primary UI behavior is normal chat: user message in, visible assistant response out.
- Queue, pin, lane, receipt, and model routing concepts are support surfaces, not required user chores.
- Capsule context is opt-in for the Codex Capsule chat/profile.
- Do not globally inject Capsule into every Codex CLI instance.
- Do not create a second ION queue, second agent system, or parallel truth surface.
- Full ION communication remains owned by existing Relay/Steward/workflow queues and receipts.

## Implementation Phases

1. Correct the current chat projection from dual-chat-first to single Capsule-chat-first.
2. Keep bounded queue/memory/comms functions available as backend capabilities, but remove them as primary UI chores.
3. Generate a visible assistant response for normal chat turns so the app is not an inert transcript recorder.
4. Add an ION comms drawer that routes to existing full ION surfaces as a secondary adapter.
5. Validate that Codex solo context stays ready and route files remain intact.
6. Connect the chat turn to the existing Codex work queue through an opt-in execution bridge, with progress and returned proof visible in the same conversation.
7. Later slice: redesign the front end as a polished chat-first app with drawers, not a control wall.

## Current Acceptance Gate

```text
POST /chat/turn with lane_id=codex_general
-> records the operator turn
-> records a codex_capsule assistant_response turn
-> response cites Capsule/HOT_CONTEXT and current queue/model context
-> does not start production/live execution
```

## Execution Bridge

Normal chat turns default to `respond_only`.

When the operator chooses `queue_for_codex`, the same chat message routes into
the existing `ion_request_codex_work_packet` owner. The UI may call this through
the same `/chat/turn` endpoint with `execution_mode=queue_for_codex`; it should
not expose raw queue plumbing as the main experience.

`queue_and_start` remains gated by
`ION_CODEX_CAPSULE_CHAT_ALLOW_RUNNER_START=1`. Without that env flag, the app
may queue the packet but must refuse runner start and report that refusal inside
the chat.

## Current Evidence

- `ION/04_packages/kernel/ion_dual_codex_chat.py`
- `ION/04_packages/kernel/ion_codex_solo_context.py`
- `ION/docs/setup/ION_DUAL_CHAT_AND_CODEX_SOLO_CONTEXT_RUNBOOK.md`
- `ION/tests/test_kernel_ion_dual_codex_chat.py`
- `ION/tests/test_kernel_ion_codex_solo_context.py`
