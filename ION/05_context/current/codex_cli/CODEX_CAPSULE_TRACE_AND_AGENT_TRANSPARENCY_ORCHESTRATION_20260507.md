---
type: implementation_orchestration
authority: A3_OPERATIONAL
created: 2026-05-07
status: ACTIVE
production_authority: false
live_execution_authority: false
---

# Codex Capsule Trace And Agent Transparency Orchestration

## Purpose

Make the Codex Capsule chat transparent enough for serious ION development
without exposing hidden chain-of-thought, secrets, raw shell control, or a second
agent system.

The app should show what happened, what evidence was used, what tools ran, what
files were touched, what proof passed or failed, and which ION owner is
responsible for the next state transition.

## Boundary

Visible:

- user turn and assistant response;
- mounted Capsule/Mini/HOT_CONTEXT/route refs;
- model move and reasoning-effort selection;
- tool and queue requests;
- run packets, task returns, proof gate decisions, touched paths;
- agent broker invocations and their bounded Codex work requests;
- friction/recovery events when the system detects drift or missing substrate.

Not visible:

- raw hidden reasoning or private chain-of-thought;
- secrets, tokens, credentials, or unrestricted environment values;
- raw command output beyond bounded previews;
- direct shell, production deployment, git push, or delete controls.

## Trace Model

Each user turn may have a `turn_trace`:

```text
operator_message
context_mount
assistant_response
execution_bridge | tool_call
runner
proof_return
capsule_receipt
friction_event
```

Trace events are receipts and operational evidence, not ION law. They support
debugging and operator trust while preserving the normal chat as the primary
surface.

## Agent Surface

The chat app may show Agents, but it must read from the existing ION agent
invocation broker:

```text
ION/04_packages/kernel/ion_agent_invocation_broker.py
```

The Codex Capsule chat must not create:

- a second queue;
- a second agent system;
- a separate source of truth for full ION role work.

Native Codex session subagents may be used by the developer to build ION faster
when explicitly requested, but durable ION agent execution must flow through the
broker, queue runner, proof gate, and receipts.

## UI Shape

Default chat stays simple:

```text
user message
assistant response
optional execution/proof card
collapsed Turn trace drawer
```

Inspector/drawers show:

- Timeline;
- Agents;
- Capsule;
- Runs;
- Receipts;
- ION;
- Settings.

The operator should not need to understand queue IDs, lane internals, spawn
plans, or receipt paths to ask the chat for help. Those details are always
available for diagnosis.

## Acceptance

- `/chat/model.json` exposes a first-class turn trace index.
- chat turn groups carry their corresponding trace.
- rendered chat shows a collapsed per-turn trace drawer.
- trace policy explicitly says raw hidden reasoning is not exposed.
- Agents drawer is backed by the existing ION broker and says it does not create
  a second agent system.
- tests cover trace creation, proof return trace hydration, and agent drawer
  presence.
