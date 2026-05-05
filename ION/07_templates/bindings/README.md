---
type: template_binding_index
authority: A3_OPERATIONAL
created: 2026-04-03T19:23:00-04:00
updated: 2026-04-22T20:05:00-04:00
status: ACTIVE_FIRST_PASS
topic: First-pass template bindings for the active ION root
---

# ION Template Bindings

This directory contains the first-pass **binding layer** above the shared core templates.

Bindings are not full replacement templates.
They are role-specific usage rules for a shared template.

## Layering rule

- Shared templates in `actions/` and `reports/` remain the common machine language.
- Bindings in `bindings/` refine how a role uses one of those shared templates.
- Boots remain the source of identity, continuity load order, lane law, and authority ceiling.

## Current first-pass bindings

### Core and support roles

- `MASON__CODE.md`
- `THOTH__RESEARCH.md`
- `NEMESIS__AUDIT.md`
- `RELAY__HANDOFF.md`
- `VESTIGE__EVIDENCE.md`

### Current-phase orchestration bindings

- `STEWARD__TASK.md`
- `STEWARD__STATUS_REPORT.md`
- `STEWARD__PROPOSAL.md`
- `STEWARD__TEMPLATE_SURFACE_CHANGE.md`

### Historical carrier-compatibility bindings

These are retained as historical witness / compatibility material for older Codex-named artifacts.
They are not active current-phase role truth.

- historical_witness_only: `CODEX__TASK.md`
- historical_witness_only: `CODEX__STATUS_REPORT.md`
- historical_witness_only: `CODEX__PROPOSAL.md`
- historical_witness_only: `CODEX__CODE.md`
- historical_witness_only: `CODEX__CSR.md`
- historical_witness_only: `CODEX__REASONING_JOURNAL.md`

## Why this is not per-agent template duplication

The system should not fork the entire template tree for every agent.

Bindings are narrower:

- they preserve shared artifact shape
- add only the role-specific obligations that matter
- and keep cross-role comparability intact

## Current-phase note

Current-phase orchestration uses **Steward** as truename.
Carrier differences should now be described through mount law rather than through a live
historical carrier token. Preserve the Codex-facing bindings only where historical continuity or
artifact interpretation requires them.

## Status

This is an active current-phase layer.
It is not yet ratified constitutional canon.
