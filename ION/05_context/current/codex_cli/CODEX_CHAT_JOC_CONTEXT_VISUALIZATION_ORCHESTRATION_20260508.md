---
type: orchestration_plan
authority: A3_OPERATIONAL
created: 2026-05-08
status: PLANNED
production_authority: false
live_execution_authority: false
implementation_allowed_without_further_review: false
---

# Codex Chat JOC Shell And Context Visualization Orchestration

## Trigger

Operator feedback on 2026-05-08 identified the remaining UI failure:

- the current Codex Chat app still reads as a monolith;
- support drawers add more wall-like vertical content instead of separating state;
- the left rail does not open real page-local drawer systems;
- the right inspector is overloaded instead of acting as a persistent assistant/context/receipt rail;
- the bottom activity strip is a small feed, not the JOC timeline drawer system;
- the context system is powerful but not visible as a living, rolling memory model.

This plan supersedes any UI direction that allows one large scrolling dashboard.
It does not authorize implementation by itself.

## Evidence Read

Active ION root:

- `ION/01_doctrine/MAINTAINED_WORK_SURFACE_CANON.md`
- `ION/02_architecture/VISUAL_CLOSURE_GRAPH_PROJECTION_AND_UI_WORK_SURFACE_PROTOCOL.md`
- `ION/02_architecture/ION_JOC_COCKPIT_SHELL_COMPONENT_CONTRACT_PROTOCOL.md`
- `ION/02_architecture/ION_JOC_COGNITIVE_EXPLORER_AND_CONTEXT_ROUTE_VIEW_MODEL_PROTOCOL.md`
- `ION/02_architecture/ION_AGENT_CONTEXT_CONTINUITY_TIMELINE_AND_ROUTE_MAP_PROTOCOL.md`
- `ION/02_architecture/ION_CONTEXT_METABOLISM_AND_LIFECYCLE_PROTOCOL.md`
- `ION/03_registry/joc_cockpit_layout_manifest.yaml`
- `ION/08_ui/joc_cockpit_shell/JocCockpitShell.tsx`
- `ION/08_ui/joc_cockpit_shell/joc-cockpit.css`
- `ION/05_context/current/codex_cli/CODEX_CAPSULE_CHAT_APP_UI_ORCHESTRATION_20260507.md`
- `ION/05_context/current/codex_cli/CODEX_CHAT_UI_RECOVERY_ORCHESTRATION_20260507.md`
- `ION/04_packages/kernel/ion_codex_chat_app_ui.py`

Approved external archaeology, read-only:

- `/home/sev/ION - Production/AIM-ION/packages/joc/plans/01-architecture-and-layout.md`
- `/home/sev/ION - Production/AIM-ION/packages/joc/plans/09-context-node-graph-visualization.md`
- `/home/sev/ION - Production/AIM-ION/packages/joc/plans/10-left-drawer-system.md`
- `/home/sev/ION - Production/AIM-ION/packages/joc/src/components/layout/LeftDrawerSystem.tsx`
- `/home/sev/ION - Production/AIM-ION/packages/joc/src/components/layout/AssistantRail.tsx`
- `/home/sev/ION - Production/AIM-ION/packages/joc/src/pages/ContextGraphPage.tsx`
- `/home/sev/AIMOS - Builds/AIM-OS-FRESH/echo-forge-loop/README.md`
- `/home/sev/AIMOS - Builds/AIM-OS-FRESH/echo-forge-loop/docs/ECHO_FORGE_LOOP_APP_DOCUMENTATION.md`
- `/home/sev/AIMOS - Builds/AIM-OS-FRESH/echo-forge-loop/src/components/shell/CognitiveShell.tsx`
- `/home/sev/AIMOS - Builds/AIM-OS-FRESH/echo-forge-loop/src/components/shell/BottomDock.tsx`
- `/home/sev/AIMOS - Builds/AIM-OS-FRESH/echo-forge-loop/src/components/shell/RightPanel.tsx`
- `/home/sev/AIMOS - Builds/AIM-OS-FRESH/echo-forge-loop/src/components/chat/RunDashboard.tsx`
- `/home/sev/AIMOS - Builds/AIM-OS-FRESH/echo-forge-loop/src/components/chat/XRayMessage.tsx`
- `/home/sev/AIMOS - Builds/AIM-OS-FRESH/echo-forge-loop/src/components/chat/stream.ts`
- `/home/sev/AIMOS - Builds/AIM-OS-FRESH/echo-forge-loop/src/components/chat/types.ts`
- `/home/sev/AIMOS - Builds/AIM-OS-FRESH/echo-forge-loop/src/components/chat/ConversationSidebar.tsx`
- `/home/sev/ION - Production/operation-victus/victus/context_assembler.py`
- `/home/sev/ION - Production/operation-victus/victus/memory_bus.py`
- `/home/sev/ION - Production/AIM-ION/docs/Aether-OS/design/victus_architecture.md`
- `/home/sev/ION - Production/AIM-ION/docs/Aether-OS/design/aether_victus_synthesis.md`
- `/home/sev/Desktop/Other/tools/smart_memory_chat.py`
- `/home/sev/ION - Production/ClaudePortal/src/components/ContextVisualization.tsx`

External roots were read for lineage only. They are not active project roots and
are not edit targets under this plan.

## External Archaeology Findings

### JOC / AIM-ION

The older JOC plans are explicit that the cockpit is not a scroll page. It is a
grid shell with stable bars and drawer slots:

```text
top bar
left icon rail
left page drawer
main page surface
right universal drawer
right icon rail
bottom status / timeline bar
```

The left side is page-specific and registered per route. The right side is
universal and follows the user across pages. Drawer content is panelized, with
loading, error, collapse, header actions, and keyboard behavior. This directly
supports the operator feedback: the next Codex Chat UI must not add more
vertical `details` stacks; it must route state into the correct shell region.

The AIM-ION Context Node Graph plan also gives the correct mental model for the
context visualization: it is a process/provenance graph, not a knowledge graph
alone. It should show how context was assembled, which sources contributed,
where branches diverged, where merges occurred, and which context became
prompt-visible.

### Echo Forge

Echo Forge proves the right shape for a high-quality AI chat runtime surface:

```text
Memory -> Plan -> Execute -> Verify -> Retry -> Audit -> Synthesize -> Reflect -> Evolve
```

Its chat stream uses typed events such as `thinking`, `memory_detail`,
`open_questions`, `plan`, `task_start`, `task_delta`, `task_verified`,
`audit_decision`, `synthesis_complete`, `reflection`, `knowledge_update`, and
`run_complete`.

For ION Codex Chat, these events should be translated into visible protocol
state and run trace events. They must not be labeled as raw hidden reasoning.
The user should see what phase the carrier is in, what evidence was selected,
what was verified, what was retried, and what receipts were produced.

Echo Forge's `XRayMessage` also gives a useful compacted-history pattern:
older text can become a compressed DAG node with a summary, tags, highlights,
and dimmed original text. That maps cleanly to Mini as lookup/receipt index and
Capsule as the active minimum working context.

### Victus

Victus contains the most direct capsule/context lineage:

```text
Layer 1: Active Crucible
Layer 2: X-Ray DAG compressed history
Layer 3: Priority Capsules
Layer 4: Background Swarm / Polycaste history
```

This is the same product direction the operator described: the AI works from a
Capsule-level minimum context, while Mini acts more like a lookup/receipt index
and older material is compressed, routed, or held outside the immediate prompt.

Victus also names the missing governance object: a protocol/navigation manifest
with branch topology. A plain capsule is a sticky note; a protocol manifest is a
map of lawful routes, gates, next files, evidence, constraints, and branch
options. ION Codex Chat should eventually show this as a route map and should
let the backend use it to decide when to continue locally, request deeper
context, queue work, or escalate to a stronger ION workflow.

The Aether/Victus C1/C2/C3 model maps well to Codex:

```text
C1 Organizer: classify, route, assemble context, choose protocol branch.
C2 Reactive Worker: answer, retrieve, run bounded tools, update visible trace.
C3 Escalation: deep research, recovery, agent work, full ION workflow.
```

This should become explicit in the model move policy and visible as an
escalation state, not hidden inside UI labels.

### Smart Memory / Context Budgeting

The older smart memory chat ranks candidate memories by word overlap, entity
match, topic/category match, and importance. ION Codex Chat should expose why a
memory segment was selected or omitted instead of merely showing that it exists.

The ClaudePortal context visualization adds another missing surface: token
budget, context usage, MCP/tool load state, skills, memory files, and collapse
status. ION should expose this as context budget and collapse health, not as a
large diagnostics paragraph.

## Correct Product Shape

The app is **ION Codex Chat**: a ChatGPT/Codex-quality chat interface using
Capsule/Mini/HOT_CONTEXT/context packages behind the scenes, with JOC-grade
inspectability around it.

The user talks to Codex. The user does not manually manage lanes, queue internals,
pins, capsules, or proof rails. Internal ION state is visible, not dumped.

The primary UI law:

```text
chat first
+ JOC shell regions
+ visual context/memory strata
+ evidence and route proof
- monolithic scrolling dashboard
- user-facing internal chores
```

## Shell Law

The next shell must implement the JOC contract as a stable outer shell. The
active-root canon names five high-level regions; the older JOC implementation
spells that out as seven concrete areas:

```text
TOP_BAR
LEFT_ICON_RAIL
LEFT_DRAWER
MAIN_WORK_SURFACE
RIGHT_INSPECTOR
RIGHT_ICON_RAIL
BOTTOM_TIMELINE
```

### Top Bar

Purpose: global app/page navigation and compact authority/status.

Required behavior:

- fixed height;
- page tabs, not panel headings;
- active root/status/model chips;
- public/local/service/auth indicators;
- no long text blocks;
- no hidden critical state.

Initial pages:

```text
Chat
Context
Runs
Agents
Receipts
Settings
```

### Left Rail And Left Drawer

Purpose: page-local instruments.

Required behavior:

- icon-only vertical rail;
- each icon opens one left drawer for the active page;
- drawer contents use tabs when the content would otherwise scroll heavily;
- left drawer is not the global app navigation;
- no internal action language unless the action is truly user-facing.

Chat page left drawers:

```text
Composer
Models
Skills
Context Lens
Run Mode
```

Context page left drawers:

```text
Windows
Routes
Receipts
Compaction
```

### Main Work Surface

Purpose: one focused page body.

Required behavior:

- Chat page main body is the live conversation timeline;
- Context page main body is the visual memory/context map;
- Runs page main body is execution/run state;
- Receipts page main body is receipt search/list;
- only the main body may have substantial content scroll for chat/history;
- non-chat pages move the chat into the right inspector as a compact assistant rail.

### Right Inspector

Purpose: persistent AI/user/context state rail.

Required behavior:

- on Chat page: show selected turn context, response carrier, context package,
  receipts, and route proof for the active/selected turn;
- on non-chat pages: show compact Codex Chat with composer and recent messages;
- no giant open drawer stack;
- use tabs for `Assistant`, `Context`, `Evidence`, `User`, `Settings`.

The right icon rail must remain available across pages and switch the universal
right drawer between assistant chat, live feed, context budget, receipts, system
health, and settings.

### Bottom Timeline

Purpose: temporal truth, not decoration.

Required behavior:

- drawer-like bottom region with compact event lanes;
- shows model calls, route loads, queue events, tool calls, receipts, human gates,
  service state, and user corrections;
- supports event filters/tabs instead of long scroll;
- links each event to the related chat turn, receipt, or context package.

## Smart Chat Context Visualization

The app should expose how the backend sees and metabolizes conversation/context
without exposing private hidden reasoning.

Allowed visible surfaces:

```text
selected source paths
context windows
prompt package summaries
Capsule rows
Mini lookup rows
HOT_CONTEXT slices
long-horizon epochs
Victus Active Crucible window
X-Ray DAG compressed nodes
Priority Capsule sources
Background Swarm / external findings summaries
route-deeper candidates
model move and reasoning-effort selection
tool calls and command receipts
response carrier status
accepted/rejected/held proof states
compaction and lifecycle class
token/context budget and collapse status
```

Forbidden visible claims:

```text
raw hidden chain-of-thought
secret token values
unread files presented as read
unaccepted worker speculation presented as state
production/live authority unless separately granted
```

### Memory Strata

Render conversation/context text in layers:

```text
LIVE_INPUT
  bright foreground; current user/assistant turn; direct prompt input.

ACTIVE_CRUCIBLE
  bright/normal foreground; recent rolling chat window currently inside the
  direct carrier call.

ACTIVE_CONTEXT
  normal foreground; Capsule minimum context and current mission package.

HOT_CONTEXT
  warm accent; active queues, recent receipts, current objective, service state.

X_RAY_DAG
  dim-but-hoverable compact node; compressed older chat/history with summary,
  tags, highlights, and provenance.

MINI_LOOKUP
  muted accent; receipt index and summary available for lookup, not primary prompt.

LONG_HORIZON
  dim text; older accepted epochs available by route.

COLD_EVIDENCE
  dark/dim text; old proof/history not currently injected.

OMITTED_OR_BLOCKED
  low-contrast or struck boundary tag; not loaded due budget, authority, or relevance.
```

Each visible segment should carry tags such as:

```text
read
selected
summarized
compacted
route-only
not-loaded
blocked
receipt-backed
speculative
accepted
held
selected_by_entity
selected_by_topic
selected_by_importance
token_budget_limited
requires_escalation
```

This is the "smart chat" surface: the user can see which older text remains
near the AI, which text became a Capsule row, which text became Mini lookup, and
which text moved to long-horizon/cold evidence.

## Data Model Required Before UI Rewrite

Add a model projection before styling the next shell:

```text
codex_chat_memory_visualization:
  selected_turn_id
  visible_windows
  memory_segments
  context_route_edges
  compaction_events
  prompt_package_summary
  protocol_manifest_summary
  token_budget_summary
  carrier_phase_events
  source_refs
  forbidden_or_omitted_refs
```

`memory_segments[]` should include:

```text
segment_id
turn_id
source_path
source_kind
text_preview
window_class
lifecycle_class
prompt_inclusion_state
compaction_state
authority_state
receipt_refs
route_refs
display_tone
selection_signals
token_estimate
confidence
source_system
agent_role
protocol_branch_id
escalation_class
```

This keeps visual design honest: UI color is derived from backend state, not
invented styling.

`context_route_edges[]` should include:

```text
edge_id
from_segment_id
to_segment_id
edge_type
source_system
confidence
receipt_refs
display_style
```

Initial `edge_type` values:

```text
retrieved
created
summarized_to
compressed_to
branched_to
merged_into
invalidated_by
omitted_due_budget
omitted_due_authority
escalated_to
```

`protocol_manifest_summary` should expose only safe route metadata:

```text
current_branch_id
available_branch_count
selected_gate
c1_c2_c3_mode
next_files_or_sources
blocked_routes
required_human_acceptance
```

## Current UI Failure Map

Current file: `ION/04_packages/kernel/ion_codex_chat_app_ui.py`

What is useful:

- chat turns work;
- response carrier works;
- pending UX now works;
- model exposes useful drawers;
- service can run locally and publicly through the cockpit path.

What must change:

- one Python module still owns too much HTML, CSS, and JS;
- the current renderer is 1080 lines and mixes shell, chat, drawers, CSS, JS,
  trace rendering, Mini/Capsule rendering, and inspector rendering;
- right inspector is a vertical stack of `details` drawers;
- bottom activity is too shallow to be the timeline drawer;
- left rail anchors do not govern true page/drawer state;
- context is summarized as text, not visualized as windows/routes/lifecycle;
- the app still makes the user inspect internal machinery instead of presenting
  an intelligible maintained work surface.

## Implementation Phases

### Phase 0 - Contract And Fixtures

Deliverables:

- add memory visualization projection to the Codex chat model;
- add route edge and protocol manifest summary dataclasses;
- add carrier phase event projection from the response carrier trace;
- add token/context budget summary projection;
- add fixture/state tests for memory strata and prompt inclusion state;
- no visual rewrite yet.

Acceptance:

- model can answer "what did this turn read/use/omit/compact?";
- model can answer "why was this segment selected or omitted?";
- model can answer "which C1/C2/C3 mode and protocol branch are active?";
- no token/secret values stored;
- tests cover window classes and lifecycle classes.

### Phase 1 - Shell Component Split

Deliverables:

- split Python UI renderer into modules:
  - `ion_codex_chat_shell_ui.py`
  - `ion_codex_chat_main_ui.py`
  - `ion_codex_chat_left_drawer_ui.py`
  - `ion_codex_chat_right_inspector_ui.py`
  - `ion_codex_chat_timeline_ui.py`
  - `ion_codex_chat_memory_visualization_ui.py`
- preserve `/cockpit/chat` and `/cockpit/chat/turn` behavior.

Acceptance:

- no single renderer file owns shell, chat, inspector, timeline, CSS, and JS;
- tests assert the five JOC zones;
- pending browser smoke still passes.

### Phase 2 - JOC Shell Behavior

Deliverables:

- top page tabs;
- left rail with page-local drawers;
- right icon rail with universal drawers;
- right inspector tabs;
- bottom timeline drawers/filters;
- Chat page as default main page;
- non-chat pages with compact chat in right inspector.

Acceptance:

- no giant open drawer stack;
- main page content is focused;
- support data appears in the correct region;
- user can type and send from the first screen with no internal chore language.

### Phase 3 - Smart Context Visualization

Deliverables:

- memory strata view;
- segment coloring/tags from backend window/lifecycle state;
- Contextual Matryoshka view for Active Crucible, X-Ray DAG, Priority Capsule,
  and Background Swarm summary layers;
- context route graph showing retrieved/created/compressed/branched/merged/
  omitted edges;
- route map links to source refs;
- compaction event timeline;
- context budget and collapse status strip;
- selected-turn "what Codex saw" inspector.

Acceptance:

- the UI visibly distinguishes live input, Active Crucible, active Capsule,
  HOT_CONTEXT, X-Ray DAG, Mini lookup, long-horizon, cold evidence, and
  omitted/blocked context;
- selecting a message shows why related context was loaded or not loaded;
- selecting a compact node shows summary, tags, highlights, source refs,
  confidence, and receipt links;
- no hidden reasoning is exposed or implied.

### Phase 4 - React/Vite Consideration

Only after the model contract and Python shell behavior are stable, decide
whether to move the UI into `ION/08_ui/` as a real frontend app. The existing
JOC React shell is design lineage and component reference, but this repo does
not yet prove a standalone frontend package pipeline for Codex Chat.

## Test Plan

Required test classes:

```text
model projection tests
HTML shell structure tests
accessibility/name tests for nav/drawer controls
Playwright pending-submit smoke
Playwright page/drawer/timeline smoke
no-secret rendering tests
no-internal-chore-language tests
```

Required browser behaviors:

- Send clears textarea immediately;
- Send is disabled during response;
- duplicate submit is blocked;
- Chat page renders first;
- clicking top tabs changes main page without losing chat state;
- left rail opens page-local drawer;
- right inspector tabs change inspector state;
- bottom timeline events are visible and filterable;
- selecting a chat turn updates memory/context visualization.

## Non-Goals

- no production authority;
- no raw hidden reasoning display;
- no manual lane/queue/pin workflow for ordinary chat;
- no external-root research without operator approval;
- no full React migration before the model contract is stable.

## Next Lawful Action

Implement Phase 0 first: add the memory visualization model projection and tests.
Then refactor the UI shell in bounded slices, preserving the now-tested response
carrier and pending-submit behavior.
