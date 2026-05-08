---
type: clarification
authority: A3_OPERATIONAL
created: 2026-04-22T18:35:00-04:00
status: ACTIVE
purpose: Clarify the current-phase disposition of Weaver in the active ION root
connections:
  - ION/02_architecture/CODEX_LEAD_ORCHESTRATION_PROTOCOL.md
  - ION/03_registry/agent_roster_registry.yaml
  - ION/06_intelligence/orchestration/2026-04-22_current_phase_agent_roster_settlement_packet.md
  - ION/06_intelligence/research/2026-04-22_codex_canonical_agent_roster_and_evolution_dynamics_proposal.md
  - ION/03_registry/current_phase_template_surface_registry.yaml
---

# Weaver Current-Phase Disposition Clarification

## Purpose

Close one roster ambiguity cleanly:

- `Weaver` is named in current orchestration prose,
- but the active root does not currently show the rest of the surfaces that would
  make Weaver a real live role.

This clarification prevents the branch from counting protocol folklore as roster closure.

## What exists

The active root does contain one real current-phase mention of `Weaver`:

- `ION/02_architecture/CODEX_LEAD_ORCHESTRATION_PROTOCOL.md`

There, Weaver is described as the support role for:

- UI implementation
- presentation implementation

when that burden is explicitly in scope.

That mention is real and should not be erased.

## What does not exist in the active root

This pass did **not** find:

- a `ION/03_registry/boots/WEAVER.boot.md`
- a `ION/03_registry/semantic_identities/WEAVER.semantic.yaml`
- a Weaver-specific continuity home under `ION/agents/weaver/`
- a lane-native Weaver continuity root
- a Weaver-specific template binding in `ION/07_templates/bindings/`
- a Weaver-specific current-phase registry row outside the orchestration prose mention

The current-phase template surface registry likewise does not name Weaver surfaces as active.

## Correct current-phase reading

The truthful reading is therefore:

- `Weaver` is a **reserved optional support-role label**
- `Weaver` is **not** currently a live roster member on the same footing as
  booted support roles such as Relay, Vestige, Mason, Scribe, Thoth, or Atlas
- `Weaver` should remain outside the counted live roster until a real workload
  justifies boot, continuity, and binding surfaces

This means the branch may still refer to Weaver as a **future-ready role label**.
It should not speak as though Weaver is already instantiated.

## Operational consequence

For the current phase:

1. do **not** count Weaver in live roster totals
2. do **not** write as though Weaver has a settled continuity lane
3. do **not** promote Weaver semantically from protocol mention alone
4. if UI/presentation work appears, first emit a bounded activation / setup packet
   that creates the minimum lawful surfaces:
   - boot
   - continuity home
   - at least one binding or equivalent packet grammar

Only after that should semantic-promotion pressure even be considered.

## Final judgment

Weaver should remain a **reserved optional support-role label, not live current-phase roster truth**.

That keeps the branch honest while preserving a clean name for later UI/presentation burden if that burden becomes real.
