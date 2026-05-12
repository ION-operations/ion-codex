# Helixion JOC dAimon WisdomNET Master Evolution Plan

Status: active master rebuild plan
Created: 2026-05-10
Authority posture: planning and product architecture; no new runtime authority granted by this document
Primary decision: Helixion is rebuilt as the JOC cockpit glass for ION, dAimon, WisdomNET, Codex, the browser extension, and GPT Actions packet work

## 1. Purpose

This plan consolidates the older JOC line, the current ION runtime, the portable dAimon companion, the browser extension, Custom GPT Actions, Codex Capsule Chat, Helixion local app, and the WisdomNET federation concept into one rebuild program.

The rebuild must not invent a new automation model. It must use the inherited JOC cockpit grammar, ION proof/receipt law, browser sandbox rules, queue packet rails, and local steward authority boundaries.

The outcome is a family of connected cockpit surfaces:

```text
Full Helixion app
-> desktop/local/cloud JOC cockpit for ION, dAimon, WisdomNET, Codex, projects, queues, receipts, graph, services

Mini-Helixion browser extension
-> portable dAimon JOC micro-shell on pages and in ChatGPT

Custom GPT Action Gateway
-> typed packet bridge into ION queues and status surfaces

Codex Capsule Chat
-> bounded Codex/ION chat workbench with visible context, memory, queue, receipts, and response carriers

WisdomNET
-> future federation hub for safe evolved packs, connectors, workflow states, and domain intelligence
```

## 2. Product taxonomy

### ION

ION is the law and state substrate.

ION owns:

```text
state-transition law
context graph
domain registry
templates
context packages
proof gates
receipt ledger
settlement
carrier routing
agent/domain orchestration
continuity bundles
work queues
risk and authority boundaries
```

ION answers what is allowed to become state, what remains candidate, what proof is owed, what scope a carrier has, and what future work may inherit.

### dAimon

dAimon is the user-facing integration agent/product.

dAimon appears across pages, ChatGPT, Helixion, docs, APIs, dashboards, SaaS apps, project surfaces, and future IDE panes. It helps the operator understand, connect, configure, capture, automate, and route work safely.

dAimon must feel like one continuous companion, not separate chats per page. Each page creates a governed branch of the shared ION context graph.

### Helixion

Helixion is the cockpit glass.

Helixion is the full visual application where the operator sees ION law, dAimon field work, Codex lanes, browser queues, service health, projects, context packages, receipts, automation state, and WisdomNET evolution.

The local Helixion app currently functions as a local-only visibility surface. Its rebuild target is the full JOC shell, not a generic dashboard.

### WisdomNET

WisdomNET is the federation layer.

WisdomNET collects and evaluates evolved ION/dAimon states, connectors, page models, workflows, domain packs, receipts, and reusable integration knowledge. It is not a global memory dump. It is a governed network of candidate and trusted evolutions.

WisdomNET must rank, test, scope, and distribute packs only with proof and safety metadata.

## 3. Canonical source map

The rebuild is grounded in these current and inherited artifacts.

| Source | Path | Role in rebuild |
| --- | --- | --- |
| JOC UI architecture canon | `_ui_canon_bundle/CANON_JOC_UI_ARCHITECTURE.md` | Binding 5-zone cockpit layout and desktop command-surface model. |
| JOC UI requirements | `_ui_canon_bundle/JOC_UI_REQUIREMENTS.md` | DXL matte-black instrument-panel visual language. |
| JOC master vision | `_ui_canon_bundle/OPUS1_JOC_MASTER_VISION.md` | Mission dashboard, AI fleet, dispatch, session, and synthesis principles. |
| JOC UI design | `_ui_canon_bundle/OPUS1_JOC_UI_DESIGN.md` | Lucid drawer, right inspector, bottom timeline, and dynamic surface patterns. |
| Portable companion product context | `ION/02_architecture/PORTABLE_ION_PAGE_COMPANION_001_PRODUCT_CONTEXT.md` | One dAimon companion across pages with graph branches. |
| DOM perception design | `ION/02_architecture/DOM_PERCEPTION_001_BROWSER_PERCEPTION_DOMAIN_DESIGN.md` | Page/DOM/AX/visual geometry/event perception model. |
| dAimon extension lineage synthesis | `ION/02_architecture/DAIMON_EXTENSION_JOC_AUTOMATION_LINEAGE_SYNTHESIS.md` | Decision that older JOC is the primary UI/automation model for portable dAimon. |
| Reactive OS stream protocol | `ION/02_architecture/ION_JOC_REACTIVE_OS_STREAM_AND_AUTOMATION_VIEW_MODEL_PROTOCOL.md` | Required automation event visibility fields and blocked-capability stream. |
| Browser sandbox protocol | `ION/02_architecture/LOCAL_BROWSER_EXECUTION_SANDBOX_SPEC_PROTOCOL.md` | Safety floor for browser execution and visual automation. |
| Browser file attachment protocol | `ION/02_architecture/ION_BROWSER_FILE_ATTACHMENT_AUTOMATION_PROTOCOL.md` | First concrete attach/drop calibration and operator-present automation lane. |
| dAimon/WisdomNET product concept | `workpackets/ion_daimon_wisdomnet_product_concept.md` | Product layer definitions for ION, dAimon, WisdomNET, Mini-Helixion. |
| Helixion IDE bridge workpacket | `workpackets/ION_Helixion_IDE_Bridge_v0_Workpacket.md` | Browser GPT as face, Helixion as cockpit glass, local steward as hard authority, Codex as hands. |
| Extension DOM cockpit shell packet | `workpackets/ion_extension_work_packets/ION_EXT_DOM_COCKPIT_SHELL_PACKET.md` | Composer-anchored ChatGPT cockpit rail and tab/panel model. |
| Extension Codex agent cockpit packet | `workpackets/ion_extension_work_packets/ION_EXT_CODEX_AGENT_COCKPIT_PACKET.md` | Codex lane in extension via local daemon, queue, proof returns, and approvals. |
| React JOC shell | `ION/08_ui/joc_cockpit_shell/JocCockpitShell.tsx` | Existing 5-zone runtime shell to become the canonical visual implementation target. |
| Runtime cockpit CSS | `ION/08_ui/joc_cockpit_shell/ion-runtime-cockpit.css` | Existing live runtime panel styling, to be aligned fully with DXL canon. |
| Cockpit view model | `ION/04_packages/kernel/ion_cockpit_view_model.py` | Normalized runtime projection for shell rendering. |
| Local cockpit app | `ION/04_packages/kernel/ion_local_cockpit_app.py` | Current local Helixion visibility app; target for JOC rebuild/integration. |
| Codex Capsule Chat | `ION/04_packages/kernel/ion_dual_codex_chat.py` | Primary Codex chat model with Capsule/Mini/context package visibility and bounded queue behavior. |
| Action gateway OpenAPI | `ION/09_integrations/custom_gpt_action_gateway/openapi.yaml` | Typed gateway including browser queue status, enqueue, receipts, action validation, and action submit. |

## 4. Non-negotiable design law

### 4.1 The rebuilt Helixion app is a JOC cockpit

The rebuilt app must use the JOC 5-zone system:

```text
top status bar
left mode rail
main work surface
right inspector/drawers
bottom timeline/log rail
```

It must be a command dashboard, not a consumer SaaS dashboard, tab manager, generic extension popup, or decorative chatbot shell.

### 4.2 The visual language is DXL

Required posture:

```text
matte black instrument panel
compact monospace labels
dense telemetry
precise custom SVG icons
small status dots
thin bars
minimal rounded corners
no emoji
no purple/blue default accent bias
no large empty SaaS whitespace
no placeholder surfaces
```

### 4.3 Automation must be visible and receipted

Any automation-like behavior must show:

```text
loop identity
phase
status
claim lane
authority scope
evidence references
blocked capabilities
repair requirement
receipt path or reason no receipt exists
```

If the UI cannot show this, the behavior is not ready for the cockpit.

### 4.4 Browser control remains bounded

The browser sandbox floor remains binding:

```text
no unrestricted browser control
no credential capture
no secret extraction
no purchases
no destructive actions
no account operations
no production mutation
no silent sensitive send
no silent promotion of page observations to accepted ION state
```

Allowed v1 behavior is bounded observation, packet queueing, visible autoplay for approved packets, result capture, gated local mutation, and attachment/drop calibration with proof.

## 5. Target product surfaces

### 5.1 Full Helixion app

The full Helixion app is the main operator console.

Required zones:

| Zone | Required content |
| --- | --- |
| Top bar | ION identity, active project/context branch, carrier state, service health, queue/autoplay mode, kill switch, blocked-capability summary. |
| Left rail | Dashboard, Chat, Queue, Page/DOM, Projects, Docs, Packages, WisdomNET, Services, Settings, Diagnostics. |
| Main surface | Active work mode: mission dashboard, Codex chat, queue packet, project package, page branch, WisdomNET pack, service console. |
| Right inspector | Context refs, packet JSON, evidence, DOM target, receipts, approval gate, file/package metadata, model route. |
| Bottom rail | Reactive OS stream, queue lifecycle, service events, warnings, receipts, repair tasks. |

The current local HTML app should be rebuilt or replaced so it renders the same DXL/JOC grammar as the React JOC shell.

### 5.2 Mini-Helixion browser extension

The extension is a portable JOC micro-shell.

Required browser surfaces:

| Surface | Purpose |
| --- | --- |
| Top monitoring rail | Minimal page/carrier health, not overlapping host controls. |
| Composer-attached tab rail | ChatGPT carrier controls attached to the composer. |
| Bottom plain telemetry bar | Diagnostics and queue health at the bottom when appropriate. |
| Right queue panel | Expert queue panel for staged messages, autoplay, pause, next, receipts. |
| Settings/capture panel | Element capture, attach target calibration, drop zone calibration, anchor selection, inspector control. |
| Page companion panel | dAimon page-aware chat, DOM evidence, workflow capture, API/page integration guidance. |

The extension must ignore its own panels during page inspection. The inspector must operate on the page, not on ION overlay UI.

### 5.3 Codex Capsule Chat

The Codex chat becomes a first-class Helixion workbench, not an isolated side app.

Required capabilities:

```text
show Capsule, Mini, Hot Context, route, and context packages
show what context Codex sees
show current project and branch assumptions
show queue mode: respond_only, queue_for_codex, queue_and_start
show Codex work queue, returns, receipts, blocked returns
show response carrier status
show ION pipeline stages
show explicit authority boundaries for each turn
```

The chat interface must help the operator understand how Codex is using ION/Capsule rather than hiding it behind a normal chatbot UI.

### 5.4 GPT Actions and browser queue gateway

GPT Actions are typed API bridges. They are not the autoplay loop and not background agency.

Target flow:

```text
Custom GPT
-> Action call
-> ION gateway
-> bounded queue packet
-> browser extension carrier sees eligible packet
-> extension waits for assistant output to stop
-> extension injects next approved prompt
-> assistant answers
-> extension captures result
-> gateway records receipt
-> next packet becomes eligible
```

The JOC must show every packet as a governed object, not as raw text spam.

### 5.5 WisdomNET hub

WisdomNET is a future full surface, but its data model must be reserved now.

Required concepts:

```text
trusted packs
candidate packs
domain packs
connector packs
page models
workflow recipes
integration receipts
safety scores
local-only states
enterprise-scoped states
global candidate states
conflict reports
ranked adoption channels
```

WisdomNET content must remain candidate until tested, scoped, and receipted.

## 6. Architecture model

### 6.1 Layer stack

```text
UI layer
  Helixion JOC shell
  Mini-Helixion extension shell
  Codex chat workbench

View-model layer
  cockpit projection
  queue projection
  page perception projection
  Codex chat model
  service console model
  WisdomNET pack projection

Gateway/queue layer
  Custom GPT Actions gateway
  browser queue
  Codex queue
  operator queue
  human gates
  stewardship queue

Context graph layer
  global user/project context
  page branches
  chat branches
  workflow branches
  project package branches
  receipts and settlement edges

Carrier layer
  ChatGPT browser carrier
  dAimon extension carrier
  Codex CLI/local worker carrier
  local Helixion app
  future IDE/desktop carriers

Safety/authority layer
  browser sandbox
  automation state protocol
  file attachment protocol
  human gates
  proof receipts
  blocked capability rail
```

### 6.2 Required normalized object types

The rebuild should converge on these objects:

```text
CockpitSurface
CarrierState
QueuePacket
AutoplayRun
PageBranch
DomEvidence
CaptureTarget
AttachTarget
DropTarget
ApprovalGate
CodexChatTurn
ContextPackage
ProjectPackage
WisdomPack
ServiceHealth
Receipt
RepairTask
BlockedCapability
```

Every UI panel should render these objects rather than inventing local one-off state.

## 7. Feature inheritance map

| Planned feature | Inherited protocol/model | Rebuild rule |
| --- | --- | --- |
| JOC full app shell | JOC canon, React JOC shell | Preserve 5-zone cockpit and DXL density. |
| Extension composer cockpit | DOM cockpit workpacket, portable companion | Keep composer anchoring and upward panel, but render as micro-JOC. |
| Queue/autoplay | Dry-run dispatch trace, action gateway browser queue | Show packet phases, output detector, pause, kill, receipts. |
| Page/DOM perception | DOM perception design, local visual harness | Page evidence is provisional until settlement. |
| Element capture frame | DOM perception, file attachment calibration model | Capture targets must show selector, rect, confidence, evidence, delete/load/save. |
| Attach/drop calibration | Browser file attachment automation protocol | Must preview target, stale-check, require approval for assisted actions. |
| Docs/projects favorites | Package/drop system plus project package context | Double-click zip/drop is operator augmentation, not silent arbitrary upload. |
| Codex chat tab | Codex Capsule Chat | Show Capsule/Mini/context use and queue/receipt states. |
| dAimon companion chat | Portable companion, dAimon build draft | Help configure systems/APIs/workflows, no secret collection. |
| Diagnostics | Reactive OS stream, browser sandbox | Show lag, anchor health, queue health, service health, page mutation. |
| WisdomNET hub | dAimon/WisdomNET product concept | Candidate/trusted pack system with proof and federation gates. |

## 8. Build phases

### Phase 0: Master plan and registry

Deliverables:

```text
master evolution plan
source/feature/gate registry
current ION continuity snapshot
readiness gates
```

Exit gate:

```text
every major planned feature maps to an inherited protocol or is marked new with safety gates
```

### Phase 1: Unified view-model foundation

Deliverables:

```text
extend cockpit projection with Helixion, dAimon, WisdomNET, extension, browser queue, page branch, and Codex chat summary sections
define shared object names and source paths
ensure local app and React shell can consume the same projection shape
```

Implementation targets:

```text
ION/04_packages/kernel/ion_cockpit_view_model.py
ION/04_packages/kernel/ion_local_cockpit_app.py
ION/08_ui/joc_cockpit_shell/ionRuntimeCockpitTypes.ts
ION/08_ui/joc_cockpit_shell/JocCockpitShell.tsx
```

Quality gate:

```text
view model must expose visible authority state, blocked capabilities, receipts, service health, queue state, and context references
```

### Phase 2: Rebuild local Helixion app as JOC cockpit

Deliverables:

```text
replace generic local cockpit HTML styling with DXL JOC shell
top status bar, left rail, main surface, right inspector, bottom stream
service reset alerts as visual console-grade warnings with action buttons
Codex Capsule Chat mounted as a main workbench
queue, receipts, projects, docs/packages, diagnostics surfaces
```

Implementation targets:

```text
ION/04_packages/kernel/ion_local_cockpit_app.py
ION/04_packages/kernel/ion_codex_chat_app_ui.py
ION/04_packages/kernel/ion_dual_codex_chat.py
```

Quality gate:

```text
the app must no longer read visually like a generic SaaS dashboard; it must read like the JOC command surface
```

### Phase 3: Convert extension to portable JOC micro-shell

Deliverables:

```text
right queue panel
settings capture/calibration workbench
docs tab favorites with zip/drop progress
projects tab for ION context packages
prompt library tab
diagnostics tab and bottom telemetry bar
top rail collision fixes
page-only inspector filtering
circle tag details with icon-button detail panel
```

Implementation targets:

```text
ION/09_integrations/browser_extension/ion_chatops_bridge/src/content.ts
ION/09_integrations/browser_extension/ion_chatops_bridge/src/background.ts
ION/09_integrations/browser_extension/ion_chatops_bridge/src/schema.ts
ION/09_integrations/browser_extension/ion_chatops_bridge/manifest.json
```

Quality gate:

```text
no overlay should inspect itself; no queue button should drift with composer resize; no sensitive send happens silently
```

### Phase 4: Queue and packet execution cockpit

Deliverables:

```text
browser queue packet list
auto-play controls
next packet manual send
output-stopped detector state
claim/result lifecycle
gateway receipt round-trip
idempotency and max-turn controls
operator approval gate for risky packets
```

Implementation targets:

```text
ION/09_integrations/custom_gpt_action_gateway/
ION/09_integrations/browser_extension/ion_chatops_bridge/
ION/04_packages/kernel/ion_chatgpt_browser_mcp_connector_contract.py
ION/04_packages/kernel/ion_codex_queue_runner.py
```

Quality gate:

```text
every packet has visible state from enqueue to receipt or blocker
```

### Phase 5: Page perception and workflow memory

Deliverables:

```text
page branch model
DOM/AX/visual evidence panel
element capture frame
target selector save/load/delete
workflow capture
API/settings assistant guidance
candidate-to-settled context promotion path
```

Quality gate:

```text
page observations must remain provisional until explicitly settled with receipt
```

### Phase 6: Projects, docs, packages, and local context surfaces

Deliverables:

```text
Docs tab with favorite folders, thumbnails, search/open home tree, zip/drop progress
Projects tab for current ION assembled context packages and latest versions
Packages tab shared drop system improvements
context package inspector
onboard/rescan icon protocol with project name/version/sync state
```

Quality gate:

```text
file/folder actions must show source, size, zip progress, hash when available, drop target, result, and repair path
```

### Phase 7: WisdomNET candidate hub

Deliverables:

```text
local WisdomNET pack registry
candidate pack cards
trusted vs local-only status
receipt/evidence inspector
conflict and safety scoring surfaces
export/import pack path
```

Quality gate:

```text
no WisdomNET pack becomes trusted by UI display alone; trust requires proof and adoption gate
```

### Phase 8: Advanced automation lanes

Deliverables:

```text
only after earlier gates pass
local visual harness integration
screen automation sandbox prototype for fixtures/loopback targets
operator-present browser helper lanes
stronger attach/file-picker lane
dry-run-to-live trace parity
```

Quality gate:

```text
no live account, credential, purchase, destructive, production, or unrestricted browser automation
```

## 9. Readiness gates before implementation

Before a code phase starts, the following must be true:

```text
source map exists
feature inheritance map exists
authority posture is explicit
new surfaces have named object types
blocked capabilities are listed
receipt expectations are listed
operator approval requirements are listed
UI canon is known
rollback/repair behavior is known
```

This document satisfies the Phase 0 planning gate, but code implementation should proceed phase by phase.

## 10. Implementation priority

Recommended first build order:

1. Normalize the Helixion view model so full app, React shell, and extension can speak the same object language.
2. Rebuild the local Helixion app shell into DXL JOC layout using the existing local-only authority boundary.
3. Mount Codex Capsule Chat as a JOC workbench with context visibility.
4. Convert the extension queue/settings/docs/projects/prompt library panels into micro-JOC panels.
5. Wire browser queue packets and receipts into a shared packet rail.
6. Add page perception/capture/target calibration as a proper evidence and settings workbench.
7. Add WisdomNET candidate pack surfaces only after local package/project/doc surfaces are stable.

## 11. Current implementation assessment

### Strong foundations

```text
React JOC shell already encodes a 5-zone cockpit layout.
Cockpit view model already normalizes several runtime files.
Codex Capsule Chat already exposes Capsule/Mini/context package concepts.
Custom GPT Action Gateway already includes browser queue endpoints.
Browser extension already has composer attachment, packages/drop concepts, queue controls, diagnostics, settings, and target calibration history.
JOC canon and safety protocols already exist.
```

### Main gaps

```text
Local Helixion app visual shell is too generic and not yet a DXL JOC cockpit.
Extension panels need consolidation into a portable JOC micro-shell.
Queue, docs, projects, prompt library, page perception, and diagnostics need one object model.
WisdomNET is conceptually defined but not yet represented as a cockpit surface.
Codex chat must reveal context, Capsule/Mini, route, receipts, and response carriers more clearly.
Service/daemon reset and health problems need user-facing console-grade alerts and repair buttons.
```

## 12. Authority statement

This rebuild expands visibility, structure, and operator control. It does not expand live authority by default.

Allowed in v1:

```text
visible autoplay queue for bounded packets
operator-approved local mutation
DOM/page perception as provisional evidence
attachment/drop target calibration
typed GPT Action enqueue
result capture with receipts
Codex queue visibility and approved enqueue
service health and reset controls with confirmation
```

Forbidden in v1:

```text
silent sensitive send
credential access
secret harvesting
purchases
destructive actions
production mutation
unrestricted browser control
silent account operation
silent promotion of page memory to accepted ION state
```

## 13. Definition of masterpiece for this rebuild

The rebuild is successful when:

```text
the operator can open Helixion and see the whole ION/dAimon/Codex/browser/WisdomNET machine at a glance
the extension feels like the same JOC cockpit compressed into a page companion
every queue/autoplay/action has a packet, phase, authority, evidence, and receipt
Codex chat visibly shows what it sees and what it can/cannot do
page and DOM learning becomes branch-aware and proof-aware
docs/projects/packages become fast operator surfaces, not file-browser chores
daemon/service problems are visible with repair buttons
WisdomNET has a clear candidate/trusted pack path
the system feels powerful without pretending to have unsafe hidden agency
```

