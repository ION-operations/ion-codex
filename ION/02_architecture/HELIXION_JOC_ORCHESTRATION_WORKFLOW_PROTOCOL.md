# Helixion JOC Orchestration Workflow Protocol

Status: active planning/control-plane protocol
Created: 2026-05-10
Authority: A3 operational planning candidate
Production authority: false
Live execution authority: false
Secrets authority: false

## Purpose

This protocol defines the ION-native orchestration lane for rebuilding Helixion/JOC as the command cockpit for ION, dAimon, WisdomNET, Codex, the browser extension, Custom GPT Actions, page perception, queue packets, projects, docs, packages, receipts, and service control.

It exists to keep future work from drifting into disconnected notes, ad-hoc UI edits, or unauthorized automation.

The lane is governed by existing ION workflow:

```text
operator intent
-> context mount
-> skill activation
-> native lens route
-> context package
-> bounded work packet
-> implementation or queue handoff
-> proof and receipts
-> Capsule/Mini/context refresh
-> cockpit projection
```

## Source authorities

The orchestration lane inherits these sources:

```text
ION/02_architecture/HELIXION_JOC_DAIMON_WISDOMNET_MASTER_EVOLUTION_PLAN.md
ION/03_registry/helixion_joc_evolution_registry.yaml
ION/05_context/current/helixion_joc_rebuild/HELIXION_JOC_REBUILD_CURRENT_PLAN.json
ION/02_architecture/DAIMON_EXTENSION_JOC_AUTOMATION_LINEAGE_SYNTHESIS.md
ION/02_architecture/PORTABLE_ION_PAGE_COMPANION_001_PRODUCT_CONTEXT.md
ION/02_architecture/DOM_PERCEPTION_001_BROWSER_PERCEPTION_DOMAIN_DESIGN.md
ION/02_architecture/ION_SKILL_ACTIVATION_PROTOCOL.md
ION/02_architecture/ION_CODEX_CHAT_ENGINE_PROTOCOL.md
ION/02_architecture/CONTEXT_NODE_AND_PACKAGE_PROTOCOL.md
ION/02_architecture/ION_AGENT_CONTEXT_CONTINUITY_TIMELINE_AND_ROUTE_MAP_PROTOCOL.md
ION/02_architecture/ION_CARRIER_CYCLE_PLAN_PROTOCOL.md
ION/02_architecture/ION_CARRIER_TASK_RETURN_INTAKE_PROTOCOL.md
ION/02_architecture/ION_JOC_REACTIVE_OS_STREAM_AND_AUTOMATION_VIEW_MODEL_PROTOCOL.md
ION/02_architecture/ION_JOC_DRY_RUN_DISPATCH_EXECUTION_TRACE_VIEW_MODEL_PROTOCOL.md
ION/02_architecture/ION_CUSTOM_GPT_ACTION_GATEWAY_PROTOCOL.md
ION/02_architecture/LOCAL_BROWSER_EXECUTION_SANDBOX_SPEC_PROTOCOL.md
ION/02_architecture/ION_BROWSER_FILE_ATTACHMENT_AUTOMATION_PROTOCOL.md
```

## Role of this lane

This lane is the planning and control package for Helixion/JOC evolution.

It may:

```text
compile the correct context package
select the helixion-joc-orchestration skill
route to existing Codex queue or full ION handoff
define work packets
define UI phase gates
define receipt expectations
update planning registries and current context
prepare future automation scaffolding
```

It may not:

```text
grant production authority
grant live execution authority
grant secrets authority
grant unrestricted browser control
silently run Codex work
silently mutate service state
silently send browser messages
promote page observations to accepted ION state
replace Steward, proof, or receipt gates
```

## Context package law

Every serious Helixion/JOC rebuild task must mount:

```text
minimum_working_capsule
mini_lookup_index
active_authority_package
mission_active_package
helixion_joc_orchestration_package
```

Route deeper only when necessary:

```text
route_depth_package
evidence_receipt_package
recovery_package
```

The package must include:

```text
identity envelope
authority envelope
product taxonomy
active source map
current phase state
feature inheritance map
kernel/tool owner map
UI/app owner map
queue/gateway owner map
skill/template/proof route
forbidden capability list
output contract
receipt targets
```

## Skill activation

The associated skill is:

```text
skill_id: helixion-joc-orchestration
display_name: Helixion JOC Orchestration
```

The skill is selected for:

```text
Helixion app rebuild
JOC/ION cockpit planning
dAimon extension orchestration
WisdomNET cockpit planning
browser queue architecture
context package assembly for this rebuild
orchestration protocol or workflow updates
```

The skill activates templates and proof contracts but does not make output accepted state by itself.

## Native lens route

Use these lenses by default:

```text
Relay: normalize operator intent into a bounded rebuild packet.
Steward: classify authority, risk, gates, and forbidden capabilities.
Vizier: own architecture, sequencing, and product decomposition.
Context Cartographer: mount Capsule/Mini/package/route context and prevent wrong-root drift.
Mason/Codex: implement bounded code/documentation slices after packet approval.
Nemesis: review proof obligations, regressions, unsafe authority creep, and UI drift.
Scribe: write receipts, context package deltas, and Capsule/Mini updates.
WisdomNET Curator: keep candidate/trusted federation boundaries explicit.
```

## Carrier routing

Correct carrier routing:

```text
small documentation or registry slice
-> local Codex direct edit under current chat
-> receipt/current context update

implementation slice
-> bounded local Codex edit when directly authorized
-> no tests unless explicitly requested
-> receipt/current context update

multi-role or high-risk slice
-> generate carrier-cycle plan
-> spawn only generated role rows
-> record task returns
-> Steward integration queue

browser/GPT Actions slice
-> typed gateway packet
-> browser queue status/receipt
-> extension carrier visibility
-> no silent sensitive send
```

Forbidden routing:

```text
operator phrase decides agents to spawn
raw worker prose becomes accepted state
new queue created when existing browser queue/Codex queue should be used
extension bypasses gateway receipts
Custom GPT Action treated as authority
browser automation proceeds without sandbox and operator gates
```

## Build phase contract

Each phase must declare:

```yaml
phase_id:
objective:
source_refs:
context_package:
skill_id:
allowed_files:
forbidden_actions:
authority:
  production_authority: false
  live_execution_authority: false
  secrets_authority: false
gates:
outputs:
receipt_targets:
next_phase_trigger:
```

## Phase sequence

```text
P0: master plan and registry
P1: unified view-model and context-package foundation
P2: local Helixion JOC shell rebuild
P3: browser extension portable JOC micro-shell
P4: queue packet execution cockpit
P5: page perception and workflow memory
P6: projects/docs/packages context surfaces
P7: WisdomNET candidate hub
P8: advanced automation lanes only after sandbox gates
```

## Automation ladder

This lane supports:

```text
MANUAL: operator carries action, dAimon/ION drafts.
ASSISTED: context packages, previews, target maps, work packets.
GATED_AUTOMATION: approved queue, approved local mutation, receipts.
SUSPENDED: pause/kill or risk gate blocks progression.
DISABLED: forbidden capability in current scope.
```

It does not currently support:

```text
RUNTIME_ACTIVE unrestricted browser automation
production mutation
credential or secret access
purchase/submission/account operation
```

## Context refresh rule

After material work in this lane:

```text
write or update current package/receipt
update HELIXION_JOC_REBUILD_CURRENT_PLAN.json
update helixion_joc_evolution_registry.yaml if ownership or phase state changed
post or prepare Capsule/Mini receipt only when material and accepted
do not claim verification unless validation was explicitly run
```

## Future automation target

The future reusable automation is a two-layer system:

```text
Codex skill: ion-orchestration
  teaches future Codex chats how to run this workflow efficiently

ION skill: helixion-joc-orchestration
  participates in Codex Chat Engine skill activation and trace visibility
```

This keeps Codex ergonomics and ION proof law separate.

