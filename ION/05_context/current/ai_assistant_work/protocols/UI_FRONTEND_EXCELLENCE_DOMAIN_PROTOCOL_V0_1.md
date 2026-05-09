# UI Frontend Excellence Domain Protocol v0.1

Status: candidate protocol, not accepted canon
Created: 2026-05-09T02:54:41Z
Domain: `ui_frontend_excellence_domain`

## Purpose

This protocol defines how ION routes, designs, builds, and validates advanced frontend/work-surface applications. It exists because ordinary UI/UX guidance is not enough for ION cockpit, Codex chat, capsule memory, agent timeline, JOC, and proof-heavy interfaces.

## Source Priority

Use sources in this order:

1. Current active ION protocol/state/receipt files.
2. Active project design system and running UI.
3. JOC maintained-work-surface and cockpit protocols.
4. Opus drawer/page/icon-bar canon.
5. Opus AI-driver, mission, session, compute, and IDE layout canon.
6. V3 Intelligence Map and reactive OS stream canon.
7. Echo Forge phase/timeline/event-stream canon.
8. Victus provenance and typed-state lessons.
9. Material/shader craft canon for selected tactile controls.
10. Generic frontend taste only after the above are satisfied.

## Non-Monolith Law

A JOC/ION UI must not become one large scrolling dashboard. Use stable shell zones:

```text
TOP_BAR
LEFT_ICON_RAIL
LEFT_DRAWER
MAIN_WORK_SURFACE
RIGHT_INSPECTOR
RIGHT_ICON_RAIL
BOTTOM_TIMELINE
```

Sparse content belongs in drawers, tabs, inspectors, route panels, or timeline surfaces, not standalone pages. Large information areas must be decomposed into tabs or lenses before they become scroll-heavy.

## User-Facing Law

The user should talk to the system naturally. Internal ION objects should be rendered as:

- route
- status
- proof
- memory/context layer
- timeline event
- receipt
- next step
- blocked gate

Do not make the user manually operate packets, queues, pins, lanes, or receipts unless the user explicitly asks for internals.

## Mission / Session / Driver Surface Law

When the app touches AI sessions, local services, tunnels, Codex runs, MCP actions, browser automation, or compute routing, the UI must expose:

- connection health
- pending/active/completed work
- route/target selection
- injection/extraction or request/response proof where applicable
- quota/cost/resource posture when relevant
- failure and retry state
- receipt or evidence trail

Do not hide automation behind a blank spinner. The operator should be able to see what the system is waiting on.

## Intelligence Map Law

When context, files, memories, capsules, or sources are selected for an AI, the UI should visualize the selection path when practical:

- selected source/file/function/context packet
- reason it was selected
- source priority or confidence
- omitted or reserve context
- dependency/import/lineage relation when available

This is not hidden reasoning. It is visible evidence about input selection and context routing.

## Material Craft Law

The base cockpit should stay dense, legible, and restrained. High-end material/shader effects may be used for selected controls only when they improve tactile comprehension. They must obey one light source, material/depth separation, reduced motion needs, and performance limits.

## Required Work Loop

For any major UI/frontend task:

1. Inspect product intent and active UI.
2. Load relevant canon and design-system constraints.
3. Produce a work-surface architecture before components.
4. Model screen, loading, empty, error, permission, and slow-response states.
5. Bind data/state to visible zones.
6. Define mission/session/driver/compute surfaces when relevant.
7. Define context selection visualization when relevant.
8. Implement bounded components.
9. Validate with build/tests and screenshots when possible.
10. Record proof, risks, non-claims, and next packet.

## Agent Route

Default route:

```text
JOC_UI_CANON_STEWARD
-> FRONTEND_WORK_SURFACE_ARCHITECT
-> INTERACTION_STATE_WEAVER
-> COMPONENT_BUILDER
-> VISUAL_PROOF_AUDITOR
-> CONTEXT_VISUALIZATION_CARTOGRAPHER when memory/context UI is involved
```

## Proof Gates

Minimum proof for completion:

- source evidence named
- shell zones named or deliberately waived
- screen states covered
- drawer/rail/tab behavior specified
- user-facing wording separated from internal terms
- loading/slow-response behavior included
- responsive behavior stated
- accessibility basics stated
- visual validation performed or marked unrun
- receipt or validation note written for state-bearing work

## Refusal / Blocker Triggers

Block or reroute if:

- generic component coding starts before architecture/state modeling
- UI exposes confusing internal ION chores to the user
- a page becomes a monolithic scrolling surface
- no loading/slow-response state exists for chat/tool calls
- proof/timeline/memory state is hidden with no alternate lens
- design violates active JOC/DXL constraints without an explicit reason
- AI session, tunnel, or service state is hidden behind an uninformative spinner
- context selection is opaque when the feature depends on retrieval or capsule memory

## Non-Claims

This protocol is candidate current-context law only. It does not mutate accepted ION architecture, product front door, or production UI without explicit acceptance and receipt.
