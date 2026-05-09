# Single-Carrier Sequential Runtime Protocol

status: ACCEPTED_SANDBOX_LINE_PROTOCOL
created_at: 2026-05-07T12:34:24+00:00
carrier_scope: GPT_SANDBOX_CARRIER
production_authority: false
live_execution_authority: false

## Purpose

This protocol restores the baseline ION runtime invariant:

```text
ION must be runnable by one capable LLM carrier, sequentially.
```

External workers, Codex, MCP, GitHub data-plane automation, daemon execution,
browser extensions, and multi-agent swarm execution are optional expansions.
They are not the baseline runtime.

## Required front-door topology

Persona is mandatory at both edges of the baseline sequence.

```text
PERSONA_INTERFACE ingress
→ RELAY
→ STEWARD
→ VIZIER
→ MASON
→ NEMESIS / VICE when required
→ SCRIBE
→ STEWARD FINAL
→ PERSONA_INTERFACE response
→ RECEIPT / NEXT STATE
```

## Persona boundary law

Persona is not tone, style, friendliness, or roleplay wrapper. Persona is ION's
human-facing ingress and egress boundary.

Ingress responsibilities:

- receive human language;
- preserve user intent;
- render it into ION-admissible intent;
- route inward through Relay / Steward without exposing unnecessary machinery.

Egress responsibilities:

- receive internal decisions or state projections;
- render them back to the user clearly;
- hide machinery unless useful or requested;
- preserve trust, continuity, and usability.

## Relay boundary law

Relay is not Persona and not Steward. Relay preserves signal integrity between
Persona, Steward, and other internal phases. Relay may translate, package,
handoff, and return meaning, but it does not grant release authority.

## Carrier law

A single carrier may execute the role phases sequentially in one context when:

- the carrier profile allows sequential role execution;
- production authority remains false;
- live execution authority remains false;
- the packet requires context proof and template-action proof;
- each role phase has an explicit section;
- the result is treated as a candidate return until Steward/human review.

## Runtime artifact law

The kernel runner materializes:

1. one single-carrier sequential packet;
2. explicit phase order;
3. role/context surface references;
4. required proof headings;
5. a sequence receipt candidate;
6. no external carrier dependency.

The runner does not call external agents. It does not execute live production
changes. It does not push Git. It does not use MCP. It does not silently update
accepted state.

## Acceptance

A valid baseline package must prove:

- the sequence starts with Persona ingress;
- the internal role sequence includes Relay and Steward before specialist work;
- the final user-facing output passes through Persona response;
- the packet can be executed by one LLM carrier in one chat;
- context proof and template-action proof are required;
- a receipt candidate is produced;
- tests prove no external carrier dependency.
