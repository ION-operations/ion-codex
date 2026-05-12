# Helixion JOC Orchestration Context Package

package_id: helixion_joc_orchestration_package
status: active_context_package
created: 2026-05-10
authority: planning/control-plane context only
production_authority: false
live_execution_authority: false
secrets_authority: false

## 1. Identity envelope

This package is the current main context package for orchestrating the full Helixion/JOC rebuild across:

```text
ION core law and state
dAimon portable companion
WisdomNET federation hub
Helixion local/public cockpit
Codex Capsule Chat
browser extension Mini-Helixion
Custom GPT Action Gateway
browser queue and Codex queue
page/DOM perception
docs/projects/packages surfaces
```

It is not a prompt dump. It is a bounded package with route map, gates, output contract, and receipt targets.

## 2. Authority envelope

Allowed:

```text
planning
documentation
context package assembly
registry updates
view-model planning
bounded local code edits when explicitly asked
approved queue packet design
operator-visible service repair plan
```

Forbidden:

```text
production mutation
live execution authority
secrets authority
credential handling
unrestricted browser control
silent browser send
purchases
destructive actions
silent page-memory promotion
raw worker prose as accepted state
```

## 3. Minimum context mount

Always mount first:

```text
ION/05_context/current/codex_solo/CAPSULE.md
ION/05_context/current/codex_solo/MINI.md
ION/05_context/current/codex_solo/HOT_CONTEXT.md
ION/05_context/current/codex_solo/STATUS.json
```

Then mount this package:

```text
ION/05_context/current/helixion_joc_rebuild/HELIXION_JOC_ORCHESTRATION_CONTEXT_PACKAGE.md
ION/05_context/current/helixion_joc_rebuild/HELIXION_JOC_ORCHESTRATION_CONTEXT_PACKAGE.json
```

Route deeper only when the current task requires exact source:

```text
ION/02_architecture/HELIXION_JOC_DAIMON_WISDOMNET_MASTER_EVOLUTION_PLAN.md
ION/02_architecture/HELIXION_JOC_ORCHESTRATION_WORKFLOW_PROTOCOL.md
ION/03_registry/helixion_joc_evolution_registry.yaml
ION/05_context/current/helixion_joc_rebuild/HELIXION_JOC_REBUILD_CURRENT_PLAN.json
ION/02_architecture/DAIMON_EXTENSION_JOC_AUTOMATION_LINEAGE_SYNTHESIS.md
ION/02_architecture/PORTABLE_ION_PAGE_COMPANION_001_PRODUCT_CONTEXT.md
ION/02_architecture/DOM_PERCEPTION_001_BROWSER_PERCEPTION_DOMAIN_DESIGN.md
ION/02_architecture/ION_SKILL_ACTIVATION_PROTOCOL.md
ION/03_registry/ion_skill_registry.yaml
ION/02_architecture/ION_CODEX_CHAT_ENGINE_PROTOCOL.md
ION/05_context/current/ai_assistant_work/protocols/UI_FRONTEND_EXCELLENCE_DOMAIN_PROTOCOL_V0_1.md
ION/05_context/current/ai_assistant_work/domains/ui_frontend_excellence_domain.domain_packet.yaml
ION/05_context/current/ai_assistant_work/template_specs/joc_work_surface_ui_packet.template_spec.yaml
ION/05_context/current/ai_assistant_work/next/HELIXION_JOC_WORK_SURFACE_UI_PACKET_20260511.json
ION/05_context/current/codex_cli/CODEX_CHAT_JOC_CONTEXT_VISUALIZATION_ORCHESTRATION_20260508.md
ION/04_packages/kernel/ion_skill_activation.py
ION/04_packages/kernel/ion_codex_solo_context.py
ION/04_packages/kernel/ion_cockpit_view_model.py
ION/04_packages/kernel/ion_local_cockpit_app.py
ION/04_packages/kernel/ion_dual_codex_chat.py
ION/04_packages/kernel/ion_custom_gpt_action_gateway.py
ION/04_packages/kernel/ion_codex_queue_runner.py
ION/09_integrations/browser_extension/ion_chatops_bridge/
```

## 4. Product split

```text
ION = law, state, proof, context graph, queues, receipts, settlement.
dAimon = user-facing portable integration companion.
Helixion = cockpit glass and local/public operator app.
WisdomNET = federation hub for candidate/trusted packs, connectors, workflows, and page models.
Mini-Helixion extension = browser-carrier JOC micro-shell.
Codex Capsule Chat = Codex workbench showing Capsule/Mini/context/queue/receipts.
Custom GPT Actions = typed API bridge, not agency.
```

## 5. Orchestration skill

Use:

```text
skill_id: helixion-joc-orchestration
codex_skill: ion-orchestration
```

The skill should select these lenses:

```text
Relay
Steward
Vizier
Context Cartographer
Mason/Codex
Nemesis
Scribe
WisdomNET Curator
JOC UI Canon Steward
Frontend Work Surface Architect
Interaction State Weaver
Context Visualization Cartographer
Visual Proof Auditor
```

## 6. Workstream map

```text
W1: context and orchestration package
W2: local Helixion JOC shell
W3: Codex Capsule Chat as JOC workbench
W4: extension portable JOC micro-shell
W5: browser queue/action gateway cockpit
W6: page perception/capture/workflow memory
W7: docs/projects/packages context surfaces
W8: WisdomNET candidate hub
W9: sandboxed advanced automation
W10: UI frontend excellence workflow gate
```

## 7. Current phase state

```text
P0 master plan and registry: complete
P1 unified projection and context package: active
P2 local shell seed: started
P3 extension micro-shell: planned
P4 queue cockpit: planned
P5 page perception: planned
P6 docs/projects/packages: planned
P7 WisdomNET: planned
P8 advanced automation: gated future
P9 UI workflow correction: active; use joc_work_surface_ui_packet before broad UI implementation
```

## 7.1 UI/frontend workflow gate

For any Helixion/JOC/Codex Chat/dAimon cockpit UI work, do not proceed as a generic frontend task.
Mount the candidate UI frontend excellence domain and route through:

```text
JOC_UI_CANON_STEWARD
-> FRONTEND_WORK_SURFACE_ARCHITECT
-> INTERACTION_STATE_WEAVER
-> CONTEXT_VISUALIZATION_CARTOGRAPHER when context/memory/proof UI is involved
-> COMPONENT_BUILDER
-> VISUAL_PROOF_AUDITOR
```

Required packet:

```text
ION/05_context/current/ai_assistant_work/next/HELIXION_JOC_WORK_SURFACE_UI_PACKET_20260511.json
```

Non-monolith law is active for this rebuild. A large scrolling panel board is not a settled JOC app.

## 8. Kernel/tool owners

```text
ion_cockpit_view_model.py: normalized runtime projection
ion_local_cockpit_app.py: local Helixion visibility app
ion_dual_codex_chat.py: Codex Capsule Chat model and turn handling
ion_codex_chat_engine.py: chat engine route, skills, lenses, response mode
ion_skill_activation.py: deterministic skill selection and activation record
ion_codex_solo_context.py: Capsule/Mini/HOT_CONTEXT/context packages
ion_codex_queue_runner.py: bounded Codex queue runner and worker lifecycle
ion_custom_gpt_action_gateway.py: action gateway, browser queue, receipts
ion_chatgpt_browser_mcp_connector_contract.py: MCP connector tools and queues
```

## 9. Output contract

For any future work under this package, output must state:

```text
phase
objective
files touched or planned
source refs used
authority boundaries
what was implemented vs only planned
receipt/context update path
next gate
```

Do not claim tests, service restart, browser reload, public URL deployment, or live proof unless performed with explicit approval and receipt.

## 10. Receipt targets

Primary:

```text
ION/05_context/current/helixion_joc_rebuild/HELIXION_JOC_ORCHESTRATION_CONTEXT_LOAD_RECEIPT.json
ION/05_context/current/helixion_joc_rebuild/HELIXION_JOC_REBUILD_CURRENT_PLAN.json
ION/05_context/current/helixion_joc_rebuild/HELIXION_JOC_UI_WORKFLOW_GATE_RECEIPT_20260511.json
```

If material implementation is accepted:

```text
ION/05_context/current/codex_solo/history/
ION/05_context/current/codex_solo/CAPSULE.md
ION/05_context/current/codex_solo/MINI.md
```

Only update Capsule/Mini through the existing receipt-post pattern.
