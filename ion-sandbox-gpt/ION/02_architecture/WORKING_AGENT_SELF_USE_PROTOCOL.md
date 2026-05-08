---
type: protocol
authority: A2_EXECUTOR
created: 2026-04-08T23:55:00-04:00
status: ACTIVE
connections:
  - ION/01_doctrine/CANONICAL_WORKFLOW.md
  - ION/AGENT_CONTRACT.md
  - ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md
  - ION/02_architecture/MANUAL_AUTOMATION_FALLBACK_PROTOCOL.md
  - ION/06_intelligence/research/2026-04-08_k2_packet_handoff_standardization_reasoning_journal.md
---

# Working-Agent Self-Use Protocol

## Supreme statement

The active working agent must follow the same canonical ION workflow while evolving ION itself.

This is not optional discipline around the workflow. It is the workflow applied to the builder.

## Required source surfaces

Before a multi-turn, drift-sensitive, or automation-adjacent pass, the working agent must read and update:

1. its boot + private `MINI.md`
2. its private `CAPSULE.md`
3. the governing task, packet, or manual-equivalent bounded objective
4. a `REASONING_JOURNAL` when the pass is multi-turn, drift-sensitive, or likely to widen scope
5. a `ROLE_SESSION` and `HANDOFF` / `CURSOR_HANDOFF` bundle when the pass creates a meaningful next executor or next packet

## Packet minimum

A lawful self-use packet should make these things reconstructible by a fresh capable executor:

- what bounded step was chosen,
- why this step was chosen now,
- what exact files were in scope,
- what was intentionally out of scope,
- what artifacts were produced,
- and what the next lawful step should be.

## Manual / automation symmetry

The self-use law is the same under:
- chat/manual lead-dev work,
- IDE-carried work,
- supervised daemon-assisted work,
- and future external/swarm carriers.

The carrier may change. The requirement for bounded continuity, proposal return, and lawful handoff does not.

## Minimum outputs for a significant pass

For a significant pass, the working agent should leave:

1. updated private continuity (`agents/{role}/MINI.md`, `agents/{role}/CAPSULE.md`)
2. a reasoning journal or equivalent bounded preflight/postflight witness when required
3. a router/session bundle or equivalent handoff artifact
4. explicit next-step language that does not silently self-authorize wider work

## What is forbidden

- building multiple packets of work without updating private continuity
- doing multi-turn architectural work without a reasoning-journal checkpoint when one is required
- silently jumping from one packet to the next without a session or handoff artifact
- treating root projections as source continuity
- implying that because the builder understands the state, a fresh executor should infer it without explicit packet surfaces

## Success condition

A fresh capable executor should be able to load the working agent's lane, read the bounded packet surfaces, and continue the next lawful step without re-deriving the whole organism from memory.
