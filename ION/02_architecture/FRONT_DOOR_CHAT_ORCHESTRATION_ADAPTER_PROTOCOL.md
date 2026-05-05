# Front Door Chat Orchestration Adapter Protocol

Status: ACTIVE_PROVISIONAL  
Authority: A3_OPERATIONAL  
Date: 2026-04-24  
Scope: Runtime entry path for browser/API/chat adapters after the Persona Interface / Relay / Steward split.

## Purpose

This protocol defines the smallest lawful executable chat path that connects the
front-door split to kernel runtime/session and dispatch surfaces.

It does not define a browser server, model call, or full autonomous Steward loop.
It defines the internal runtime adapter that those surfaces must call.

## Governed path

Inbound path:

```text
User text
  -> Persona Interface ingress
  -> Relay semantic-boundary packet
  -> Steward routing envelope
  -> runtime session queue
  -> Steward work unit
  -> kernel dispatch packet
```

Return path:

```text
Steward / system output
  -> Relay controlled re-expression package
  -> Persona Interface response package
  -> User
```

## Role separation law

The adapter must preserve these role boundaries:

- Persona Interface owns user-facing ingress and final response rendering.
- Relay owns semantic-boundary translation, digesting, packetization, and return packaging.
- Steward owns orchestration/routing work and must consume Relay boundary packets, not raw user text alone.

Forbidden collapses:

- Persona Interface may not act as Steward.
- Relay may not act as Persona Interface.
- Relay may not act as Steward.
- Persona style may not become semantic truth.
- Raw user wording may not become governed write authority without Relay boundary packaging.

## Runtime/session bridge

The adapter must create or attach to a runtime session authority center before
placing Steward work in the queue.

Queue items produced by this path must reference:

- Persona ingress artifact
- Relay semantic-boundary packet
- Steward routing envelope
- generated Steward work unit
- generated context package

## Dispatch posture

A chat adapter may either:

1. queue a Steward work unit without dispatch, or
2. dispatch it immediately through the runtime-session queue dispatcher.

Immediate dispatch is allowed only when:

- the generated WorkUnit is PENDING,
- no unresolved dependencies block it,
- the context package exists,
- the session is active,
- and the queue item is DISPATCH_READY.

## Authority posture

This adapter does not turn user text into governed state.

It creates a routeable work unit for Steward. Any later write must still pass
through ordinary governed-write law.

## Enactment surfaces

- `ION/04_packages/kernel/front_door_runtime_entry.py`
- `ION/04_packages/kernel/front_door_chat_orchestration.py`
- `ION/04_packages/kernel/operator_cli.py`
- `ION/tests/test_kernel_front_door_runtime_entry.py`
- `ION/tests/test_kernel_front_door_chat_orchestration.py`

## Open work

Future browser/API/chat servers should call:

- `FrontDoorChatOrchestrationAdapter.submit_user_turn(...)`
- `FrontDoorChatOrchestrationAdapter.prepare_system_return(...)`

rather than bypassing Persona Interface, Relay, or Steward boundaries.
