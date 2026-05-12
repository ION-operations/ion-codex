# DOM_PERCEPTION_001_VALIDATION_STRATEGY

Status: proposal
Created: 2026-05-10

## Purpose

Define validation gates for Browser Perception before implementation.

## Fixture classes

- Static semantic page fixture with landmarks, forms, lists, buttons, dialogs, and hidden regions.
- Long ChatGPT-like thread fixture with hundreds of turns, streaming partial turns, tool cards, citations, and composer state.
- Virtualized list fixture with recycled nodes and offscreen gaps.
- Selector drift fixture with generated class names, hydration changes, and route transitions.
- Shadow DOM and iframe fixture with same-origin and cross-origin boundaries.
- Mutation storm fixture with frequent DOM changes and route events.
- Secret/redaction fixture with password fields, tokens, private text, and user-excluded regions.

## Validation gates

- DOM region maps include source, selector candidates, semantic anchors, freshness, and redaction state.
- AX snapshots include roles, names, states, relationships, and DOM/AX mismatch reports.
- Visual maps include bounding boxes, viewport coordinates, scroll containers, sticky overlays, and occlusion risks.
- Mutation timelines are debounced, bounded, and able to mark stale snapshots.
- Long chat audits mark unresolved offscreen or virtualized gaps instead of claiming completeness.
- Performance budgets fail closed into partial/stale state rather than blocking the page.
- Redaction tests prove secrets are masked or excluded before graph promotion.
- Snapshot freshness tests prevent stale targets from being used in action plans without refresh.
- Cockpit traces preserve plan, preview, approval, execution, and receipt stages.

## Non-goals for this packet

- No live browser execution.
- No browser automation.
- No provider calls.
- No deployment.
- No production authority.

## Recommended first implementation tests

- JSON schema validation for all proposed schema files.
- Synthetic fixture capture for DOM, AX, visual, and mutation sources.
- Long thread fixture performance budget under controlled page size.
- Redaction fixture with explicit forbidden field assertions.
- Workflow replay dry-run that produces a plan and preview without clicking.
