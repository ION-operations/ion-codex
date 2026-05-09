# UI Frontend Canon Synthesis Report

Status: candidate report, not accepted canon
Created: 2026-05-09T02:54:41Z
Scope: active ION root plus read-only JOC, Opus, Echo Forge, and Victus evidence sources

## Result

The UI work should not remain a generic UI/UX subtask. The evidence supports a new candidate specialist domain:

```text
ui_frontend_excellence_domain
```

This domain should own JOC-grade application shells, agent-visible work surfaces, context visualization, proof/timeline UI, and frontend validation. It complements the existing `ui_ux_domain`; it does not replace it.

## Canon Synthesis

### JOC

JOC canon says the app shell is a maintained operational surface, not a page or dashboard. The base shell is:

```text
TOP_BAR
LEFT_ICON_RAIL
LEFT_DRAWER
MAIN_WORK_SURFACE
RIGHT_INSPECTOR
RIGHT_ICON_RAIL
BOTTOM_TIMELINE
```

The shell must keep dense information visible without turning the page into one scrolling monolith.

### Opus

Opus adds the drawer governance:

```text
icon bar -> drawer -> tabs -> bounded panels
```

The right side can split into full, top, or bottom drawer modes. Drawer width and panel layout are controlled by function, not by random card expansion. If a drawer needs scrolling too much, the information should be split into a tab or a different surface.

Opus also adds mission and session architecture. A serious JOC/ION app is not just a chat surface; it is a visible orchestration system for sessions, missions, dispatch targets, responses, synthesis, project catalog, AI drivers, session health, quota, memory, and extraction/injection proof.

The compute/IDE layout extends this further:

```text
activity bar -> tabs/split panes -> editor/work surface -> inspector -> bottom output/timeline -> status bar -> command palette
```

This matters for ION because Codex/capsule/chat UI needs IDE-grade interaction states and resource visibility, not only a browser-chat clone.

### Echo Forge

Echo Forge contributes a live process timeline:

```text
Memory -> Plan -> Execute -> Verify -> Retry -> Audit -> Synthesize -> Reflect -> Evolve
```

For ION, this becomes a visible agent/tool/context stream. Users should see what phase the system is in, why a response is slow, what was inspected, what proof exists, and what remains blocked.

### Victus

Victus contributes provenance law. UI state is not just UI state; it is a typed, traceable, durable work object. The UI must avoid overwritten monolithic state and instead preserve lineage:

```text
contextualize -> reflect -> plan -> gate -> execute -> audit -> deliver
```

### Active ION

Active ION adds maintained-work-surface law:

```text
pressure -> synthesis -> evidence -> recognition -> formalization -> receipt -> continuation
```

This means an ION UI must render the work, the proof, the route, the uncertainty, the queue, and the next lawful movement. It must not force the user to manually operate internal machinery.

### V3 Intelligence Map

The UI canon bundle adds a more aggressive cognitive UI target:

```text
instant index search -> structural blueprint -> dependency web -> reactive OS stream -> visibly selected context
```

The important principle is algorithmic certainty: the UI should show why a file, function, source, or context packet was selected instead of asking the user to trust a black box.

### Material / Shader Canon

The shader notes are not base shell law. They are a craft layer for high-value tactile controls. Useful principles:

- one coherent light source
- gradients model material
- shadows model depth
- contact shadow and cast shadow are different
- SVG filters can add material grain
- physics-style motion can make controls feel substantial

For JOC/DXL shells, apply this sparingly. The main cockpit remains dense, restrained, legible, and proof-oriented.

## Product Rule

The user-facing app should feel like a high-quality chat/work cockpit. It should not expose raw internal chores as confusing buttons. Internal ION objects are shown as status, proof, timeline, route, and memory/context visualization.

## Domain Implication

The new domain should dispatch before generic implementation whenever work involves:

- an ION app shell
- a Codex/capsule/chat interface
- an agent cockpit
- a proof/timeline/receipt view
- dense operational state
- context visualization
- drawer/rail/page architecture
- visual validation requirements

## Non-Claims

- This report is not accepted canon.
- It does not claim the current app UI is fixed.
- It does not claim external archives are complete.
- It does not mutate production UI.
