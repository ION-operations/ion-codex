---
protocol_id: ion.codex_chat_engine_protocol.v1
status: ACTIVE_PROVISIONAL
rank: A3_OPERATIONAL
created: 2026-05-08
scope: codex_chat_engine_capsule_skill_native_routing
production_authority: false
live_execution_authority: false
---

# ION Codex Chat Engine Protocol

## Purpose

The Codex Chat Engine turns a normal operator message into a high-quality chat
response path without making the operator manage ION internals. It is the
functional core under the UI.

The UI renders the engine. The engine does not render the UI.

## Target

The quality target is ChatGPT-browser-level conversation or better, integrated
with ION context, skills, templates, model moves, native lenses, proof gates,
and receipts.

```text
operator message
-> context mount
-> skill activation
-> ION native lens selection
-> model/thinking route
-> response mode
-> direct answer or existing Codex queue / full ION handoff
-> proof and receipt hydration
-> Capsule settlement when material
```

## Response Modes

The engine may select:

- `answer`: produce a normal useful assistant response;
- `clarify`: ask a concise question only when needed;
- `plan`: produce an executable plan without editing;
- `queue_work`: send bounded work to the existing Codex queue;
- `recover`: stop drift, inspect evidence, and repair orientation;
- `ion_handoff`: route into the full ION Relay/Steward workflow.

## Native Lenses

ION natives are not extra chatbots for every turn. They are lenses or workflow
routes selected only when useful.

- Persona: user-facing continuity and clarity.
- Relay: intent normalization and packet shape.
- Steward: authority, risk, and route legitimacy.
- Vizier: architecture and planning depth.
- Thoth: research and explanation.
- Mason/Codex: implementation.
- Nemesis: proof, audit, regression review.
- Vice: future-risk and contradiction pressure.
- Scribe: receipts and context settlement.
- Context Cartographer / Ionologist: context mount and drift prevention.
- Template Curator: skill/template/proof contract correctness.
- Vestige / Atlas: lineage and external/historical evidence.

The selected lenses must be visible as trace data. The operator should not have
to select them manually for ordinary chat.

## Carrier Strategy

The engine must use existing ION owners:

- normal answer: GPT-5.5 Codex chat response contract;
- implementation: existing Codex work queue;
- recovery: GPT-5.5 recovery plan or proof-gated Codex work;
- full ION: existing Relay/Steward/agent surfaces.

Current implementation may return a local response contract while preparing the
Codex carrier path. It must not pretend a model call occurred unless a carrier
run and receipt prove it.

## Contract

Every engine turn should expose:

```yaml
response_mode:
selected_skill:
selected_native_lenses:
model_move:
context_refs:
carrier_strategy:
assistant_response:
queue_recommendation:
proof_expectations:
authority:
  production_authority: false
  live_execution_authority: false
  secrets_authority: false
```

The assistant response is conversational. Proof/queue/native details belong in
trace and drawers unless the operator asks for them.

## Non-Claims

This protocol does not grant production authority, live execution authority,
secrets authority, git push authority, arbitrary shell authority, or state
acceptance. The engine is an orchestration and response layer under existing
ION proof law.
