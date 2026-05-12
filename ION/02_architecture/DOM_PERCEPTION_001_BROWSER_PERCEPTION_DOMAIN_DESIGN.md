# DOM_PERCEPTION_001_BROWSER_PERCEPTION_DOMAIN_DESIGN

Status: proposal
Created: 2026-05-10
Work request: `codex_req_2026-05-10T172639Z0000_dom_perception_001_domain_design_design_the_ion_daimon_browser_perception_domain`
Product constraint: `PORTABLE_ION_PAGE_COMPANION_001_PRODUCT_CONTEXT`

## Purpose

Design the ION/dAimon Browser Perception domain for page, chat, and extension intelligence without granting unsafe autonomous browser authority.

DOM Perception is how ION sees a page. The Portable ION Page Companion is how the user carries ION onto pages. Mini-Helixion is the embedded cockpit surface. The Living Operational Graph is where page branches, workflow branches, settlement edges, and receipt edges become inspectable.

## Boundary

This packet is design-only.

It does not implement invasive page mutation, browser control, navigation, form submission, provider calls, deployment, or production authority.

All page observations are provisional until settled by an explicit context package, receipt, or operator confirmation.

## Safety law inherited by this domain

- Observe by default.
- Plan before acting.
- Preview before clicking.
- Ask before navigation/forms.
- Receipt every state-bearing workflow.
- Never treat page memory as accepted context without settlement.

## Perception stack

Browser Perception is multi-source because modern pages are dynamic, virtualized, and fragile.

- DOM source: structure, attributes, text nodes, forms, regions, stable anchors, shadow roots where permitted.
- Accessibility source: screen-reader-visible roles, names, states, relationships, hidden/inaccessible gaps.
- Visual geometry source: bounding boxes, viewport regions, occlusion, sticky layers, scroll containers, visible density.
- Mutation timeline source: route transitions, streaming messages, virtualized list churn, debounced mutation batches.
- Event/action source: user-visible interactions, extension panel events, carrier messages, workflow approvals, receipts.
- Human semantics source: user explanations, labels, task intent, page purpose, and mismatch reports.

The synthesizer merges these into page state objects with provenance, freshness, confidence, scope, and redaction metadata.

## Required domains

### browser_perception_core

Owns the shared capture lifecycle, scope negotiation, redaction policy, event bus, snapshot freshness model, and common object IDs.

Outputs:

- capture scope receipts
- page session IDs
- source snapshot envelopes
- freshness and confidence metadata

### chatgpt_dom_reader

Specialized reader for ChatGPT-like long chat pages. It maps composer, transcript, turns, tool cards, citations, attachments, streaming states, hidden buttons, and virtualized or offscreen sections.

Outputs:

- chat thread map
- turn region map
- composer state object
- tool/action trace references

### page_state_cartography

Builds semantic page maps from DOM, AX, geometry, and route state. It tracks page class, stable landmarks, task areas, forms, lists, panels, modals, and navigation regions.

Outputs:

- page topology map
- page branch identity candidates
- semantic region inventory

### accessibility_tree_reader

Reads screen-reader-visible structure and exposes where DOM-visible and user-visible states diverge from accessibility-visible states.

Outputs:

- AX region map
- role/name/state relationships
- accessibility gap report

### visual_geometry_reader

Maps bounding boxes, viewport coordinates, scroll containers, sticky overlays, occlusion, z-order risk, and visible density.

Outputs:

- visual region map
- viewport occupancy report
- click-target geometry evidence for preview-only planning

### mutation_timeline_monitor

Tracks debounced mutation batches, route changes, streaming states, virtual list churn, lazy loading, and stale snapshot risk.

Outputs:

- mutation timeline
- stability windows
- refresh triggers
- mutation storm warnings

### long_chat_resilience

Finds and mitigates long-chat lag, freeze, scroll loss, excessive DOM growth, virtualized transcript gaps, streaming partial state, and recovery hazards.

Outputs:

- chat performance profile
- thread segmentation plan
- stale/offscreen content warning
- freeze-risk mitigations

### extension_cockpit_surface

Feeds the Mini-Helixion cockpit with page-aware perception summaries, active branch state, worker ticker data, workflow drafts, and context package status.

Outputs:

- cockpit event trace
- top ticker facts
- bottom panel data contracts
- page branch summary

### action_trace_and_agent_comms

Records plans, approvals, dry-runs, user actions, carrier messages, context package promotions, and task returns. It does not perform unsafe autonomous browser control.

Outputs:

- extension action trace events
- workflow approval receipts
- carrier context refs
- replayable workflow draft references

### perception_security_and_privacy

Owns no-secrets posture, redaction, per-page scopes, iframe/shadow DOM boundaries, forbidden field classification, local retention, and context settlement gates.

Outputs:

- redaction report
- sensitive-field exclusions
- scope violation warnings
- settlement readiness status

## Perception agents and roles

- DOM_CARTOGRAPHER maps DOM regions, selector candidates, semantic anchors, unstable selectors, shadow boundaries, and region lineage.
- ACCESSIBILITY_CARTOGRAPHER maps AX tree roles, names, states, relationships, hidden gaps, and screen-reader-visible structure.
- VISUAL_GEOMETRY_CARTOGRAPHER maps bounding boxes, scroll layers, occlusion, viewport regions, sticky overlays, and geometry hazards.
- MUTATION_WATCHER tracks dynamic changes, debounced mutation batches, route transitions, streaming states, and stability windows.
- CHAT_LENGTH_NEMESIS finds long-chat lag, freeze, scroll, virtualization, and transcript inspection failure modes.
- EXTENSION_PERFORMANCE_STEWARD protects page performance through batching, throttling, observer caps, storage quotas, and event bus budgets.
- PERCEPTION_SYNTHESIZER merges DOM, AX, visual, timeline, and human semantics into trustworthy page state objects.
- COCKPIT_SCRIBE records action traces, carrier messages, context package refs, receipts, and Mini-Helixion panel events.

## Page state trust model

Each page state object must mark facts as one of:

- observed_current: directly observed inside the current freshness window
- observed_stale: directly observed but outside freshness budget
- inferred: model or heuristic interpretation from observed sources
- user_asserted: user-provided page/task explanation
- settled_context: promoted by settlement receipt into accepted ION context
- contradicted: source disagreement or later observation invalidated the fact

No inferred or stale field may be used as accepted context without settlement.

## Page branch binding

Every capture belongs to a branch:

- global_chat_graph_id
- page_branch_id
- page_session_id
- optional workflow_branch_id
- settlement_state
- receipt_refs

The companion can carry page memory between pages, but memory remains provisional until settled. A ChatGPT/Codex context package must include branch IDs, source capture refs, redaction posture, and settlement state.

## Long chat resilience model

Long chat handling should avoid full-page brute force reads.

- Segment transcript into visible, near-visible, indexed, and unresolved ranges.
- Track stable turn anchors from multiple sources rather than brittle selectors alone.
- Defer offscreen expansion until user requests or workflow requires it.
- Detect virtualized gaps and mark them as unresolved instead of hallucinating continuity.
- Use idle-time sampling, backpressure, and mutation debouncing.
- Preserve scroll anchors and viewport state before any user-approved navigation or replay.
- Keep streaming messages as partial until terminal markers settle.

## Performance budget

Default posture is passive and low overhead.

- Avoid synchronous full DOM walks on large pages.
- Prefer bounded region sampling, idle callbacks, and capped observers.
- Debounce MutationObserver batches and emit summaries, not raw storms.
- Limit retained snapshots by branch, page class, and user scope.
- Push expensive synthesis to extension worker or background context when available.
- Fail closed into stale or partial state rather than blocking the page.

## Privacy and security posture

- No credential capture.
- No secret extraction.
- No hidden page scraping beyond declared scope.
- No cross-origin iframe inspection without explicit capability and browser permission.
- Sensitive fields are masked, summarized, or excluded before graph promotion.
- Page memory cannot silently override accepted ION context.
- Receipts must identify capture scope, redaction policy, and settlement state.

## Integration points

- Portable ION Page Companion: supplies page branch, scope, user consent, and companion panel.
- Mini-Helixion: consumes cockpit event traces, active page summary, worker ticker, and workflow drafts.
- Living Operational Graph: stores branch nodes, workflow nodes, settlement edges, conflict edges, and receipt edges.
- ChatGPT Browser MCP connector: transports bounded carrier messages, task returns, context refs, artifact paths, and receipts.
- Future workflow automation: may consume workflow drafts only through plan, preview, approval, and receipt gates.

## Acceptance criteria

- The domain can describe a page without mutating it.
- DOM, AX, visual geometry, mutation, and human semantics remain distinguishable sources.
- Long ChatGPT-like threads can be represented with gaps and freshness states rather than false completeness.
- The Mini-Helixion cockpit can show page branch, perception status, workflow drafts, and receipt state.
- The Living Graph can inspect page/context/workflow relationships.
- Any future state-bearing action must pass through visible plan, preview where applicable, user approval, and receipt.
