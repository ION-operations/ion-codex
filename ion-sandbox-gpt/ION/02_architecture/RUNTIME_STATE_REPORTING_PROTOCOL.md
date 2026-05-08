# RUNTIME STATE REPORTING PROTOCOL

## Purpose

C4 promotes runtime-state visibility from internal service consumption into bounded operator-facing packet rendering.
The goal is not a new reporting daemon. The goal is truthful exposure of live route and automation posture in
status, planner, and review surfaces that already exist in the kernel workflow.

## Lawful Boundaries

- Reporting may read `manifest_route_state` and `automation_state` and compose bounded summaries.
- Reporting may not invent runtime authority, dispatch permission, or review clearance beyond what the live state says.
- Reporting must keep continuity prose distinct from machine-readable runtime state.
- Reporting should reuse the current template/report surfaces where possible rather than proliferating new runtime-only doctrine.

## Required C4 Rendering Surfaces

1. Scope status reports must be able to summarize route posture, automation posture, dispatch posture, and runtime refs.
2. Planner-manifest packets must be able to expose live runtime posture alongside child intent and source-question evidence.
3. Review packets must be able to expose held-delta review pressure alongside the current runtime posture that triggered or preserves that pressure.

## Canonical Reporting Objects

- `KernelRuntimeStateReporter`
- `RuntimeScopeStatusBundle`

## Output Discipline

- Status rendering should remain operator-readable markdown.
- Planner and review packets should remain bounded and directly traceable to persisted kernel records.
- Rendered packets may quote runtime ids and machine-readable refs, but should not require an external daemon to interpret them.

## Non-goals

- no autonomous reporting loop
- no packet persistence family added by default
- no continuity markdown reclassification

## Runtime/session clarification

Runtime-state reporting may render runtime/session posture for operators.
It does **not** create session identity, queue ownership, or API carrier entry
authority.
Those authority surfaces now remain explicitly governed by the emitted Lane C
runtime/session trio.
