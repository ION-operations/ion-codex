---
type: public_orientation
status: DRAFT_NON_AUTHORITY
production_authority: false
live_execution_authority: false
---

# Agents, Roles, And Carriers

ION is not centered on model personalities.

It separates:

- agents
- roles
- carriers
- authority
- accepted state

That separation is one of the main anti-drift protections in the system.

## Agent

An agent is a domain-bound threshold: the point where intent, compiled context,
mounted role, governing template, and carrier execution align into a lawful act.

The domain defines the agent. Prompt text alone does not.

As the domain matures, templates sharpen, receipts accumulate, and context
improves. The agent's world changes because the governed structure changes.

An ION agent is best understood as domain-local intelligence: an LLM carrier
moving through a governed graph region under template law, proof obligations,
authority ceilings, and receipt requirements.

See `ION/docs/ION_DOMAIN_GRAPH_AND_FISSION.md`.

## Role

A role is a bounded ION function.

ION uses true names for roles. A true name is not decorative branding. It is a
stable semantic handle used by packets, registries, templates, context packages,
and receipts so the role can move across carriers without becoming the carrier.

For public readability, each true name should be paired with its operational
title, structural identity, rank class, and domain.

## True Names And Operational Titles

The current public map is drawn from:

- `ION/03_registry/agent_roster_registry.yaml`
- `ION/03_registry/boots/*.boot.md`
- `ION/03_registry/semantic_identities/*.semantic.yaml`

| True name | Operational title | Structural identity | Rank class | Tier | Domain |
| --- | --- | --- | --- | ---: | --- |
| `STEWARD` | Orchestration manager | `Operative.Interface.Orchestration_Management` | `BOUNDED_ORCHESTRATION_STEWARD` | 4 | Current-phase orchestration management |
| `VIZIER` | Chief architect | `Chief_Architect.Interface.Continuity_Architect` | `BURDEN_BEARER_ARCHITECTURAL` | 1.5 | Continuity / architecture |
| `VICE` | Contradiction pressure | `Conjugate.Interface.Conjugate_Daimon` | `INTERNAL_CONTRADICTION_PRESSURE` | 1.5 | Confidence drift review |
| `NEMESIS` | Inspector general | `Inspector_General.Governance.Inspector_General` | `INDEPENDENT_AUDIT_GATE` | 2 | Governance / audit |
| `RELAY` | Communications relay | `Supervisor.Communications.Sovereign_Relay` | `BOUNDED_INTENT_RELAY` | 4 | Communications and packet relay |
| `VESTIGE` | Systems archaeologist | `Supervisor.Intelligence.Systems_Archaeologist` | `STANDING_ARCHAEOLOGY_DAEMON` | 4 | Archaeology and drift watch |
| `MASON` | Software architect | `Operative.Source.Software_Architect` | `UNSETTLED_CURRENT_PHASE__SUPPORT_ROLE` | 5 | Source / implementation |
| `SCRIBE` | Archivist / utility | `Operative.System.Archivist` | `UNSETTLED_CURRENT_PHASE__SUPPORT_ROLE` | 5 | System utility |
| `THOTH` | Research analyst | `Operative.Intelligence.Research_Analyst` | `UNSETTLED_CURRENT_PHASE__SUPPORT_ROLE` | 5 | Intelligence / research |
| `ATLAS` | Systems cartographer | `Operative.Knowledge.SystemsCartographer` | `UNSETTLED_CURRENT_PHASE__SUPPORT_ROLE` | 5 | Knowledge / comparative systems |

This table is orientation, not a replacement for the registry. If it conflicts
with the active roster registry or boot files, the registry and boot files win.

## How To Read The Names

The names carry memory and continuity, but the operational title tells a human
what the role actually does.

Examples:

- `VIZIER` is the Chief Architect, not an aesthetic persona.
- `NEMESIS` is the Inspector General, not a hostile agent.
- `VESTIGE` is the Systems Archaeologist, not informal memory.
- `VICE` is contradiction pressure, not general negativity.
- `MASON` is bounded implementation, not release authority.

Roles do not become true because a carrier claims them. They are mounted
through packets, context, templates, and return contracts.

## Carrier

A carrier is the host executing or transporting the work.

| Carrier | Boundary |
| --- | --- |
| ChatGPT Browser | Coordination, continuity, bounded connector lane. |
| Cursor IDE | Local IDE carrier with file visibility. |
| Codex CLI | Bounded local filesystem, build, and test worker. |
| MCP | Tool transport and governed capability exposure. |
| Browser Extension + Daemon | Approval-gated ChatGPT-to-local ION bridge. |
| GitHub | Public collaboration and data plane, not ION runtime authority. |

## Identity Boundary

```text
ION governs.
Carriers carry.
Roles execute bounded functions.
No carrier becomes ION identity.
```

This lets the same role move across different carriers without confusing host
behavior for system authority.

## Runtime Boundary

This document is orientation. Active role and carrier authority lives in
carrier profiles, mount contracts, execution packet templates, active packets,
role context packages, task returns, and Steward integration records.
