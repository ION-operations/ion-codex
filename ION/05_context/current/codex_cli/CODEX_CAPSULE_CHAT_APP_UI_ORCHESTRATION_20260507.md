---
type: implementation_orchestration
authority: A3_OPERATIONAL
created: 2026-05-07
status: ACTIVE
production_authority: false
live_execution_authority: false
---

# Codex Chat App UI Orchestration

## Purpose

Build the proper user-facing Codex Chat app: a local web chat that feels
closer to Codex IDE / ChatGPT browser chat than a terminal, while using ION/JOC
for context, evidence, receipts, model routing, and operator visibility.

The app is not a second ION, not a second agent system, and not a replacement
for full ION Persona / Relay / Steward. It is the polished front door for Codex,
with Capsule operating as background context.

## Research Basis

Local evidence already supports this direction:

- `workpackets/ION_LOCAL_CODEX_IDE_MVP_PACKET_2026-05-07.md` says the IDE is a
  front door/cockpit over existing ION owners, not a second ION.
- `workpackets/ION_ACTIONS_CODEX_IDE_FULL_EXECUTION_PLAN_2026-05-07.md` says
  the IDE/cockpit should expose owner status and create packets/validation
  requests, not directly mutate canonical state.
- `ION/03_registry/joc_cockpit_layout_manifest.yaml` defines the JOC zones:
  top bar, left rail, main work surface, right inspector, bottom timeline.
- `ION/08_ui/joc_cockpit_shell/JocCockpitShell.tsx` shows the JOC shell pattern:
  top nav, icon rail, maintained work surface, receipt inspector, runtime
  stream.
- `ION/05_context/current/codex_cli/CODEX_CAPSULE_CHAT_REBUILD_ORCHESTRATION_20260507.md`
  establishes the corrected product target: one Capsule Codex chat with bounded
  full-ION comms.

## Product Judgment

The primary screen must be a chat, not a dashboard.

Dashboard/cockpit material belongs in drawers and inspectors around the chat.
The operator should be able to type a normal message and get a useful response
without understanding lanes, queue IDs, pins, model matrices, or receipt paths.

```text
Primary experience:
operator message -> assistant response -> optional Run task mode -> proof/return

Supporting experience:
Capsule, Mini, HOT_CONTEXT, queue status, receipts, ION comms, model routing,
runner state, and task returns are visible in drawers.
```

## UX Shape

Use a dense but calm application shell:

```text
TOP_BAR
  app identity, root/status chips, model/profile selector, public/local status

LEFT_RAIL
  Chat
  Context
  Runs
  Receipts
  ION
  Settings

MAIN_CHAT
  message timeline
  assistant response cards
  execution status cards
  task return/proof cards
  composer

RIGHT_INSPECTOR
  Capsule/Mini context summary
  active context package
  selected model move
  current run/queue details
  receipt/proof details

BOTTOM_ACTIVITY
  compact runtime stream: queued, runner started, return accepted/refused,
  service status, tunnel/auth status
```

This adapts the JOC shell but reverses emphasis: chat is the maintained work
surface. JOC evidence is support, not the main chore.

## Core Views

### Chat

Default landing view. Contains:

- conversational timeline;
- compact status row for Capsule ready, queue count, runner active, public URL;
- composer with primary `Send` button;
- one `Send` button;
- mode selector: `Chat`, `Run task`, and later `queue_and_start`
  when enabled;
- inline execution/proof cards linked to each user turn.

### Context

Drawer/view for:

- Mini brief;
- Capsule recent rows;
- long-horizon epoch summary;
- HOT_CONTEXT route status;
- route validation findings;
- "copy Mini" and "open evidence path" style controls later.

### Runs

Drawer/view for:

- queued Codex work requests;
- active runner state;
- latest run packet;
- prompt path;
- last return path;
- proof gate status;
- accepted/refused task returns.

### Receipts

Receipt rail:

- Capsule posts;
- ChatOps receipts;
- task returns;
- action gateway receipts;
- proof receipts;
- refusal records.

### ION

Secondary comms/diagnostic view:

- bounded notes to existing full ION comms;
- Relay/Steward status projections when available;
- agent broker status;
- no second queue or alternate ION truth.

### Settings

Local operator settings:

- execution mode default;
- runner-start gate visibility;
- local/public URL status;
- auth/session status;
- model-move policy view;
- no secrets shown.

## Backend Contract

Keep the current stdlib server path as the source of truth for the first app
slice:

```text
GET  /chat
GET  /chat/model.json
POST /chat/turn
POST /chat/queue       internal/support endpoint
POST /chat/memory      internal/support endpoint
```

`POST /chat/turn` is the real product endpoint. It accepts:

```text
lane_id=codex_general
message=<operator text>
execution_mode=respond_only|queue_for_codex|queue_and_start
```

The model should expose a richer UI contract without changing authority:

```text
product
execution_bridge
lanes.codex_general.turns
codex_solo_context
codex_queue.runner
ion_comms
shared_digest
memory
receipts/runs pointers
```

## Frontend Strategy

Phase 1 should stay dependency-light and use the existing Python-rendered app so
the local service keeps working.

Phase 2 may introduce a real React/Vite app under `ION/08_ui/` only after the
server model contract is stable. The existing `ION/08_ui/joc_cockpit_shell`
files are source/design lineage but currently do not include a standalone
package manifest, so do not assume a working frontend build pipeline exists.

## Implementation Phases

### Phase 1 — Chat Product Model

Goal: make `/chat/model.json` the correct product model.

Deliverables:

- turn groups with user/assistant/execution/proof relation;
- current conversation summary;
- composer config;
- execution bridge config;
- drawer model for Capsule, Runs, Receipts, ION, Settings;
- focused tests.

Acceptance:

- normal turn shows assistant response;
- `Run task` queues through existing owner;
- model says no second queue and no global context injection.

### Phase 2 — Python-Rendered Chat UI

Goal: replace the current control-wall HTML with a polished chat-first shell.

Deliverables:

- main chat timeline;
- fixed composer;
- icon rail;
- right inspector;
- bottom activity strip;
- responsive mobile layout;
- no visible queue/pin/lane chores as primary controls.

Acceptance:

- user can understand where to type immediately;
- queue and receipt details are visible but secondary;
- text fits on desktop and mobile;
- tests assert key HTML structure and absence of control-wall copy.

### Phase 3 — Return Hydration

Goal: pull Codex task returns/proof into the same chat timeline.

Deliverables:

- map queued request/run/task return to originating chat turn;
- execution card updates from queued -> running -> returned -> accepted/refused;
- proof details expandable in inspector;
- Capsule post suggestion or automatic post only after material accepted proof.

Acceptance:

- a queued work packet's return appears under the originating chat turn;
- blocked/refused proof is visible as refusal, not hidden failure.

### Phase 4 — JOC/ION Drawer Depth

Goal: add high-value ION/JOC inspection without overwhelming the chat.

Deliverables:

- Capsule drawer;
- Runs drawer;
- Receipts drawer;
- ION comms drawer;
- model route drawer;
- service/public URL status.

Acceptance:

- drawers explain current state by evidence, not decorative metrics;
- no drawer requires user to manually operate internal ION mechanics.

### Phase 5 — React App Candidate

Goal: only after the server model is stable, decide whether to move the UI to a
proper component app.

Candidate structure:

```text
ION/08_ui/codex_capsule_chat_app/
  package.json
  src/
    App.tsx
    components/
    styles.css
```

The React app should consume the same `/chat/model.json` contract and preserve
the stdlib server as the local authority/API owner.

## Non-Goals

- no production deployment claim;
- no arbitrary shell;
- no secrets display;
- no global Codex CLI prompt injection;
- no second queue;
- no second ION agent system;
- no manual lane/queue/pin workflow as the main UX;
- no React build before the server-side model contract is stable.

## First Build Slice

Implement Phase 1 and Phase 2 together only as far as needed to make `/chat`
usable:

1. Add a chat UI view model derived from `build_dual_codex_chat_model`.
2. Render message timeline grouped by user turn.
3. Render assistant and execution-status turns inline.
4. Add composer with `Send` and `Run` actions.
5. Move Capsule/Run/Receipt details into drawers/inspector.
6. Add focused HTML/model tests.

Do not start services automatically during implementation. Service restart is a
separate operator action.
