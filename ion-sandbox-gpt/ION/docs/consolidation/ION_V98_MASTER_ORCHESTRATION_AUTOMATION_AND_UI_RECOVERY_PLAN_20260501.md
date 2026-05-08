# ION V98 Master Orchestration, Automation, Template Enforcement, and UI Recovery Plan

**Date:** 2026-05-01  
**Branch / pass name:** `V98_MASTER_ORCHESTRATION_AUTOMATION_AND_UI_RECOVERY_PLAN`  
**Artifact class:** internal lead-dev master plan, survival roadmap, automation/UI recovery contract  
**Authority posture:** non-production. This file does not claim ION is production-ready or autonomous. It defines what must now be implemented, tested, and made visible before ION may again claim operational maturity.

---

## 0. Lead-developer commitment

I accept the lead-developer responsibility for the next survival phase **only under a stricter standard than the project has used so far**.

ION is worth saving because its root design is coherent, unusual, and technically valuable: governed AI work should become inspectable state through templates, agents, packets, receipts, graph/event pressure, review, continuation, and user-visible work surfaces. But ION is not worth continuing as an expanding mythology. From V98 onward, ION must be treated as a machine whose claims are valid only when they are enforced by commands, tests, receipts, or cockpit-visible state.

The next phase must therefore satisfy four conditions:

```text
1. Automation is not prose. Automation is a command that advances work.
2. Template canon is not prose. Template canon rejects non-template action.
3. Agent orchestration is not prose. Agent orchestration produces role packages, accepts/rejects returns, and integrates state.
4. UI is not polish. UI is the operator's sanity layer and proof surface.
```

The project may continue only if it becomes simpler at the operational center, even while retaining depth around that center.

---

## 1. The current crisis in one sentence

ION's original automation/template vision is real, but the current project has too much authority expressed as protocols and too little authority forced through a single host-independent executor and visible cockpit.

The recent Cursor phase exposed this directly:

```text
- Cursor Auto mode could not reliably remember or enact ION.
- Multiple control stories existed at once.
- Legacy context law survived beside new context law.
- Templates existed, but global template enforcement was not the unavoidable gate for every action.
- UI existed as JOC shell/plans, but not yet as the user's live sanity surface.
- The user saw mostly AI narration, not ION's actual state.
```

The next work must not argue with this. It must eliminate it.

---

## 2. What ION is, restated as executable truth

ION is an AI orchestration runtime and maintained-work-surface system.

The correct operational definition:

```text
ION converts user pressure/objectives into governed, template-bound, agent-mediated, receipt-bearing workflow that can be inspected, resumed, audited, repaired, and continued without the user manually sequencing internal work.
```

The canonical loop:

```text
user pressure / objective
→ front-door intake
→ operator message classification
→ queue or gate update
→ workflow planner
→ role/team selection
→ template selection
→ dynamic context-window plan
→ compiled role context package
→ worker execution or local simulation
→ template-bound return
→ proof/template gate
→ Steward integration
→ receipt
→ cockpit-visible state update
→ next-step decision
→ repeat until gate/completion
```

ION is not operational unless this loop can run.

---

## 3. Non-negotiable survival laws

### 3.1 No-user-upkeep law

The user must not manage ION's internal upkeep.

The user may:

```text
- state direction or objective;
- type /ion, continue, proceed, or equivalent;
- approve or deny human gates;
- correct facts or scope;
- inspect and steer from the UI;
- grant external/credential authority when explicitly gated.
```

The user must not be asked to:

```text
- decide which ordinary agent to spawn;
- remember the run sequence;
- pick the correct packet command;
- explain ION's own workflow back to the carrier;
- update context packages manually;
- sequence Steward/Relay/Mason/Nemesis by hand;
- determine whether template/receipt law applies.
```

If the system asks these questions during ordinary work, it has failed the run.

### 3.2 One-command survival law

There must be one host-independent command that proves the core loop.

Target command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_autonomous_loop --ion-root . --goal "Find one contradiction and propose one patch" --max-steps 3 --write --json
```

This command must not rely on Cursor Auto mode. It may use local simulation at first. Later it may use model adapters, MCP, or SDK workers, but the first proof must work locally.

### 3.3 Template-gate law

A meaningful action cannot become accepted state unless it passes a template/action contract.

Every accepted worker return must identify:

```text
- template_id or action_contract_id;
- role binding;
- input packet path;
- output packet path;
- allowed mutation scope;
- evidence/read paths;
- validation command claims;
- receipt path;
- next-state proposal.
```

A return beginning with `### CONTEXT PROOF` is not enough. Context proof proves load posture. It does not prove template-conformant work. V98+ must add a second gate:

```text
CONTEXT PROOF + TEMPLATE ACTION PROOF
```

### 3.4 Steward integration law

Steward must not be a vibe. Steward integration must be an executable step.

Steward integration must:

```text
1. read accepted returns only;
2. classify each return as integrate/reject/hold/gate;
3. update active runtime state or produce a bounded proposal;
4. write a receipt;
5. choose next step or stop at a gate.
```

If accepted worker returns remain in `ACTIVE_STEWARD_INTEGRATION_QUEUE.json` without a consuming integration step, ION is not autonomous.

### 3.5 UI proof law

The UI is not optional.

The user needs to see:

```text
- current objective;
- active plan;
- active/warm/dormant agents;
- current context package status;
- template/action gate status;
- worker returns;
- accepted/rejected state;
- Steward integration queue;
- human gates;
- receipts;
- why ION stopped;
- what ION will do next.
```

If the user has to trust a drifting AI narration, ION has failed its maintained-work-surface promise.

### 3.6 No new expansion before survival proof

Until the minimal autonomous loop passes:

```text
- no new agent names;
- no new UI dreams beyond the required cockpit MVP;
- no new Cursor rule expansions;
- no broad MCP/API authority expansion;
- no production claims;
- no new doctrine unless it is tied to a testable gate.
```

---

## 4. Current assets that must be preserved

The project already contains valuable assets. The recovery plan must not delete them blindly.

### 4.1 Template and evented-template machinery

Preserve and harden:

```text
ION/07_templates/
ION/03_registry/template_metadata_contract_registry.yaml
ION/03_registry/template_completion_watch_registry.yaml
ION/04_packages/kernel/template_metadata_contracts.py
ION/04_packages/kernel/template_completion_events.py
ION/04_packages/kernel/template_reaction_selection.py
ION/04_packages/kernel/template_index_projection.py
ION/04_packages/kernel/template_graph_writeback_proposals.py
ION/04_packages/kernel/template_graph_writeback_review.py
ION/04_packages/kernel/template_graph_commit.py
```

These are central to ION's identity. The recovery path must make them unavoidable gates, not optional modules.

### 4.2 Carrier/continuation machinery

Preserve and simplify:

```text
ION/04_packages/kernel/ion_carrier_continue.py
ION/04_packages/kernel/ion_operator_message_classifier.py
ION/04_packages/kernel/ion_operator_message_queue.py
ION/04_packages/kernel/ion_human_gate_queue.py
ION/04_packages/kernel/ion_cycle_runner.py
ION/04_packages/kernel/ion_carrier_task_return.py
ION/04_packages/kernel/ion_cursor_autopilot_packet.py
```

These pieces are useful, but they must be subordinated to the host-independent loop. Cursor-specific carrier logic is no longer the center.

### 4.3 Agent context systems

Preserve and complete:

```text
ION/02_architecture/ION_AGENT_CONTEXT_SYSTEMS_PROTOCOL.md
ION/03_registry/agent_context_system_registry.yaml
ION/05_context/current/agent_context_systems/
ION/04_packages/kernel/ion_agent_context_systems.py
ION/04_packages/kernel/ion_agent_context_dynamics.py
ION/05_context/current/ACTIVE_AGENT_CONTEXT_WINDOW_PLAN.json
```

The agent context system is the correct successor to old `MINI.md`/`CAPSULE.md` as primary active context authority. Old mini/capsule surfaces may survive only as historical/witness inputs, not required runtime blockers.

### 4.4 Front-stage council / maintained work surface

Preserve and restore tests for:

```text
ION/01_doctrine/MAINTAINED_WORK_SURFACE_CANON.md
ION/02_architecture/FRONT_STAGE_COUNCIL_PROTOCOL.md
ION/02_architecture/FRONT_STAGE_COUNCIL_RUNTIME_RECEIPT_PROTOCOL.md
ION/04_packages/kernel/maintained_work_surface.py
ION/04_packages/kernel/front_stage_council_receipt.py
ION/tests/test_kernel_maintained_work_surface.py
ION/tests/test_kernel_front_stage_council_receipt.py
```

The maintained work surface and Front-Stage Council are the user-facing truth model. They cannot remain documentary only.

### 4.5 JOC cockpit/UI lineage

Preserve and promote:

```text
ION/08_ui/joc_cockpit_shell/
ION/04_packages/kernel/ion_cockpit_view_model.py
ION/05_context/current/ACTIVE_COCKPIT_VIEW_MODEL.json
ION/09_integrations/cursor_extension/
ION/03_registry/joc_cockpit_layout_manifest.yaml
ION/02_architecture/ION_JOC_*_PROTOCOL.md
```

The UI is now a survival requirement. It must show the loop.

---

## 5. Current blockers and required repairs

### Blocker A — Legacy MINI/CAPSULE required by sequential kernel

Observed defect:

```text
sequential_kernel.py still treats ION/agents/{role}/MINI.md and CAPSULE.md as required role continuity targets.
```

But the productized root does not contain `ION/agents/`, and newer law says old mini/capsule are witness inputs, not primary context authority.

Required repair:

```text
- Modify sequential_kernel.py so Agent Context System cards and generated active packages are primary required surfaces.
- Demote old ION/agents/*/MINI.md and CAPSULE.md to optional legacy witness inputs.
- Add an audit that fails if legacy mini/capsule are required in a productized runtime without existing files.
- Add tests for all core roles: Steward, Relay, Mason, Nemesis, Vizier, Scribe, Context Cartographer, Runtime Cartographer.
```

Exit condition:

```text
ion_cycle_runner can generate a valid plan without ION/agents/*/MINI.md or CAPSULE.md.
```

### Blocker B — V96 test surface shrinkage

Observed defect:

```text
V96 productized runtime omitted important older tests, including V40/V41 surfaces.
```

Required repair:

```text
- Restore test files from the last full known source where they existed.
- Split tests into required survival tests, regression tests, and archived historical tests.
- Ensure productized runtime does not omit required survival tests.
```

Exit condition:

```text
python3 -m pytest ION/tests -q can run a bounded survival suite and report honest pass/fail.
```

### Blocker C — No minimal autonomous loop command

Observed defect:

```text
The project can prepare packets and plans, but it does not yet prove a host-independent loop that executes, validates, integrates, and chooses next state.
```

Required repair:

```text
Add ION/04_packages/kernel/ion_autonomous_loop.py
```

Initial mode:

```text
local-simulated-worker mode
```

The first implementation does not need external LLM calls. It must prove the system can run its own loop mechanics.

Exit condition:

```text
ion_autonomous_loop writes an autonomous run receipt and either advances one step, integrates one accepted return, or stops at an explicit gate.
```

### Blocker D — Template enforcement not universal

Observed defect:

```text
Template modules exist, but accepted worker returns are not universally forced through template/action contracts.
```

Required repair:

```text
Add ION/04_packages/kernel/ion_template_action_gate.py
```

It must validate:

```text
- declared template/action contract;
- role binding;
- allowed input/output shape;
- required receipt fields;
- allowed mutation scope;
- graph/event transition class if applicable.
```

Exit condition:

```text
A return without TEMPLATE ACTION PROOF cannot enter Steward integration.
```

### Blocker E — Steward integration is not yet a consuming executor

Observed defect:

```text
ACTIVE_STEWARD_INTEGRATION_QUEUE exists, but the project lacks a simple canonical command that consumes it and writes next state.
```

Required repair:

```text
Add ION/04_packages/kernel/ion_steward_integrate.py
```

Initial mode:

```text
local deterministic integration of accepted return metadata
```

Exit condition:

```text
Accepted return leaves queue or receives HOLD/GATE status with receipt.
```

### Blocker F — UI does not yet prove workflow live

Observed defect:

```text
JOC shell and cockpit view model exist, but the user does not yet have a reliable visual surface showing the live automation loop end-to-end.
```

Required repair:

```text
Make ACTIVE_COCKPIT_VIEW_MODEL.json include the survival loop state.
Add/expand panels for autonomous loop, template gate, Steward integration, and why-stopped diagnosis.
```

Exit condition:

```text
After ion_autonomous_loop runs, the cockpit view model shows every stage of the run and why it stopped or continued.
```

### Blocker G — Production readiness lineage drift

Observed defect:

```text
production_readiness.py still carries older gate sequence language while later V41/V42/V96 states exist.
```

Required repair:

```text
Separate branch lineage from production-gate namespace in runtime reports.
```

Exit condition:

```text
production_readiness report does not confuse old branch labels with current productized runtime line.
```

### Blocker H — Cursor remains overrepresented

Observed defect:

```text
Too much recent effort tries to make Cursor Auto mode behave as ION's main carrier.
```

Required repair:

```text
- Freeze Cursor Auto mode as non-primary.
- Keep Cursor only as editor, optional MCP client, optional extension host.
- Build local loop first.
```

Exit condition:

```text
ION can prove its core loop without Cursor.
```

---

## 6. Required architecture for the minimal autonomous loop

### 6.1 New module: `ion_autonomous_loop.py`

Responsibilities:

```text
1. Accept goal/operator message.
2. Classify message.
3. Update operator queue/human gates as needed.
4. Build context dynamics plan.
5. Build work packet/spawn plan.
6. Select next executable role row.
7. Compile role context package and compiled bundle.
8. Select required template/action contract.
9. Execute worker adapter.
10. Validate context proof.
11. Validate template action proof.
12. Intake return.
13. Run Steward integration.
14. Write loop receipt.
15. Decide next step or stop reason.
16. Write cockpit view model.
```

### 6.2 Worker adapter modes

Initial modes:

```text
local_simulated_worker
manual_return_file
```

Future modes:

```text
openai_api_worker
cursor_mcp_worker
cursor_sdk_worker
local_model_worker
```

The first proof must not depend on an LLM. The local simulated worker can produce a deterministic valid/invalid return based on a role package. This proves the orchestration substrate.

### 6.3 Stop reasons

The loop must always stop explicitly:

```text
STOP_NO_WORK
STOP_HUMAN_GATE_OPEN
STOP_TEMPLATE_GATE_REJECTED
STOP_CONTEXT_PROOF_REJECTED
STOP_STEWARD_HOLD
STOP_MAX_STEPS_REACHED
STOP_AUDIT_FINDING
STOP_ERROR_WITH_RECEIPT
STOP_COMPLETED
```

The UI must display this.

### 6.4 Loop receipt

Write:

```text
ION/05_context/signals/v98_autonomous_loop_receipt_<timestamp>.json
```

Required fields:

```text
run_id
goal
steps
selected_roles
context_packages
template_contracts
returns
context_gate_results
template_gate_results
steward_integration_results
files_written
stop_reason
next_recommended_action
```

---

## 7. Required template/action gate model

### 7.1 Template action proof header

Every worker return must include:

```text
### CONTEXT PROOF
...
### TEMPLATE ACTION PROOF
- template_id:
- role_binding:
- input_packet:
- output_shape:
- allowed_paths:
- forbidden_paths:
- receipt_fields:
- validation_claims:
```

### 7.2 Template gate decisions

```text
ACCEPT_TEMPLATE_ACTION
REJECT_MISSING_TEMPLATE_ID
REJECT_ROLE_TEMPLATE_MISMATCH
REJECT_OUTPUT_SHAPE_MISSING
REJECT_UNAUTHORIZED_PATH
REJECT_RECEIPT_FIELDS_MISSING
REJECT_VALIDATION_CLAIM_UNBACKED
HOLD_REQUIRES_TEMPLATE_CURATOR
```

### 7.3 Template registry linkage

The gate should consult:

```text
ION/07_templates/
ION/03_registry/template_metadata_contract_registry.yaml
ION/03_registry/template_completion_watch_registry.yaml
ION/07_templates/bindings/
```

If the role has a binding template, it must use it.

Examples:

```text
MASON → ION/07_templates/bindings/MASON__CODE.md
NEMESIS → ION/07_templates/bindings/NEMESIS__AUDIT.md
RELAY → ION/07_templates/bindings/RELAY__HANDOFF.md
PERSONA_INTERFACE → ION/07_templates/bindings/PERSONA_INTERFACE__USER_RESPONSE.md
STEWARD → ION/07_templates/bindings/STEWARD__TASK.md or STEWARD__STATUS_REPORT.md
```

---

## 8. Agent orchestration plan

### 8.1 Always-logical front-door team

Persona, Relay, and Steward are always logically present.

They do not always need to spawn as heavy workers, but their functions must always be represented:

```text
Persona Interface → user-facing intake/output posture
Relay → packetization, grounding, transport
Steward/VZ → authority, routing, integration, gate decisions
```

### 8.2 Role activation leases

Each role must be one of:

```text
active
warm
dormant
blocked
retired
```

Active roles can run. Warm roles influence plan/context. Dormant roles are known but not loaded. Blocked roles require a gate. Retired roles are historical only.

### 8.3 Core role duties

#### Steward

```text
Orchestration, integration, gate control, accepted-return settlement, next-step decision.
```

Must be executable through `ion_steward_integrate.py`.

#### Relay

```text
Intent packetization, handoff, provenance, semantic grounding, user-output grounding.
```

Must not integrate raw returns.

#### Persona Interface

```text
User-facing expression from accepted state and visible uncertainty.
```

Must not claim all of ION or fabricate hidden truth.

#### Context Cartographer

```text
Context graph/package compiler, context window planning, route-deeper map, context delta receipts.
```

Owns agent context evolution.

#### Runtime Cartographer

```text
Runtime path, loop execution, carrier/host mechanics, command audits.
```

Owns making ION actually run.

#### Template Curator

```text
Template contract selection, template shape evolution, receipt shape governance.
```

Owns the template gate.

#### Mason

```text
Bounded implementation only, no broad architecture expansion.
```

#### Nemesis

```text
Adversarial audit, evidence pressure, validation of claims.
```

#### Scribe

```text
Accepted reports, receipts, manifests, not invented validation.
```

#### Vestige

```text
Lineage, recovery, stale-surface classification.
```

#### Vizier

```text
Architecture implications, dependency planning, route shape.
```

#### Thoth

```text
Reasoning/research synthesis, non-mutating by default.
```

---

## 9. UI/cockpit plan as survival infrastructure

The UI must not be delayed until after automation. It must be built alongside the minimal loop because the UI is how the user and future agents see whether automation is actually working.

### 9.1 Required MVP cockpit panels

The V98/V99 cockpit must show:

```text
1. Current Objective
2. Autonomous Loop State
3. Operator Queue
4. Human Gates
5. Active Plan / Spawn Rows
6. Agent Context Window Plan
7. Template Action Gate
8. Task Return Ledger
9. Steward Integration Queue
10. Receipt Timeline
11. Why ION Stopped
12. Next Recommended Action
```

### 9.2 Required cockpit states

```text
READY
RUNNING
WAITING_FOR_WORKER
WAITING_FOR_STEWARD
BLOCKED_BY_GATE
REJECTED_CONTEXT_PROOF
REJECTED_TEMPLATE_ACTION
DEGRADED_AUDIT_FINDING
COMPLETED
ERROR_WITH_RECEIPT
```

### 9.3 UI must answer these questions instantly

```text
What is ION doing?
Why did ION choose that role?
What context did the role receive?
Which template governs the work?
What did the worker return?
Was it accepted or rejected?
Did Steward integrate it?
What receipt proves it?
Why did ION stop?
What happens if I click/trigger Continue?
```

### 9.4 Persona in the UI

The extension/cockpit should eventually become the user-facing ION interface.

User flow:

```text
User writes to Persona panel
→ message enters operator queue
→ /ion or extension Continue runs loop
→ cockpit displays live progress
→ Persona panel reports accepted state
```

The user should not primarily communicate with the carrier chat. The carrier should become an execution lane. The UI should become the relationship/control surface.

### 9.5 Timeline as sanity layer

The bottom timeline should show events such as:

```text
operator_message_queued
message_classified
work_packet_refreshed
context_window_planned
spawn_plan_written
role_package_compiled
template_contract_selected
worker_return_generated
context_proof_accepted
template_action_accepted
steward_integrated
receipt_written
cockpit_updated
loop_stopped
```

If this timeline is empty or vague, ION is not visible enough.

---

## 10. Testing and guarantee strategy

ION cannot be guaranteed by one test suite. It needs layered guarantees.

### 10.1 Survival tests

These are mandatory for every productized runtime:

```text
test_kernel_ion_autonomous_loop.py
test_kernel_ion_template_action_gate.py
test_kernel_ion_steward_integrate.py
test_kernel_sequential_kernel_context_system_primary.py
test_kernel_ion_cockpit_view_model_survival_loop.py
```

### 10.2 Regression tests to restore

Restore V40/V41 and template runtime tests:

```text
test_kernel_maintained_work_surface.py
test_kernel_front_stage_council_receipt.py
test_template_metadata_contracts.py
test_template_completion_events.py
test_template_reaction_selection.py
test_template_index_projection.py
test_template_graph_writeback_proposal.py
test_template_graph_writeback_review.py
test_template_graph_commit.py
```

### 10.3 Golden path tests

Golden path 1:

```text
Goal: "Find one contradiction and propose one patch"
Expected: loop runs one role, validates template return, Steward integrates, receipt written.
```

Golden path 2:

```text
Goal: "continue"
Expected: operator queue or active plan is consumed; if no work exists, system schedules self-audit/evolution plan instead of asking user what to do.
```

Golden path 3:

```text
Goal: invalid worker return
Expected: context/template gate rejects; Steward does not integrate; cockpit shows why.
```

Golden path 4:

```text
Goal: human-gated destructive operation
Expected: human gate opens; loop stops; UI shows gate.
```

### 10.4 UI proof tests

```text
- cockpit view model contains loop_state
- cockpit view model contains stop_reason
- cockpit view model contains template_gate result
- cockpit view model contains Steward integration result
- missing active packet appears as degraded, not silent pass
```

### 10.5 Release verifier

Before any new full zip is called consolidated:

```text
1. zip integrity passes;
2. required root files exist;
3. survival tests pass;
4. active packets build cleanly;
5. no required legacy MINI/CAPSULE references remain;
6. cockpit view model emits;
7. productized runtime manifest lists included/excluded surfaces;
8. latest receipt records failed tests honestly.
```

---

## 11. Roadmap from V98 onward

### V98 — Minimal Autonomous Loop Survival Proof

Goal:

```text
Build host-independent local autonomous loop proving the core workflow without Cursor.
```

Add:

```text
ION/04_packages/kernel/ion_autonomous_loop.py
ION/04_packages/kernel/ion_template_action_gate.py
ION/04_packages/kernel/ion_steward_integrate.py
ION/tests/test_kernel_ion_autonomous_loop.py
ION/tests/test_kernel_ion_template_action_gate.py
ION/tests/test_kernel_ion_steward_integrate.py
```

Exit:

```text
one command runs one complete template-bound loop and writes receipt.
```

### V99 — Legacy Context Repair and Test Restoration

Goal:

```text
Repair sequential_kernel legacy MINI/CAPSULE dependency and restore required tests.
```

Exit:

```text
cycle plan valid without ION/agents/*/MINI.md or CAPSULE.md; restored tests present.
```

### V100 — Cockpit Survival MVP

Goal:

```text
Make UI show autonomous loop state, template gates, Steward integration, why-stopped.
```

Exit:

```text
ACTIVE_COCKPIT_VIEW_MODEL.json displays full survival-loop state.
```

### V101 — Front-Door Persona/Relay Runtime

Goal:

```text
Make user-facing intake/output route through Persona/Relay/Steward packet discipline.
```

Exit:

```text
User message becomes operator queue item; accepted output comes from front-stage receipt.
```

### V102 — Context Timeline and Delta Receipts

Goal:

```text
Make agent context systems evolve through accepted context deltas.
```

Exit:

```text
Each run writes per-agent context timeline/delta receipt when relevant.
```

### V103 — Graph/Template Runtime Reconciliation

Goal:

```text
Unify evented template runtime with current agent workflow loop.
```

Exit:

```text
template completion/reaction/proposal/review/commit path can operate inside the autonomous loop.
```

### V104 — MCP/API Worker Adapter

Goal:

```text
Attach external/model workers to proven local loop with strict gates.
```

Exit:

```text
external worker cannot bypass context/template/Steward gates.
```

### V105 — Production Readiness Namespace Repair

Goal:

```text
Repair production_readiness lineage drift and separate branch versions from production gates.
```

Exit:

```text
production readiness report reflects current runtime while preserving NOT_PRODUCTION_READY.
```

### V106 — Release Candidate Verifier Revival

Goal:

```text
Revive release verifier for productized runtime with survival-loop evidence.
```

Exit:

```text
release candidate can prove root, tests, receipts, manifests, cockpit state, and boundaries.
```

---

## 12. Current plans/goals/orchestrations inventory

### 12.1 Automation goals

```text
- one-command continuation
- operator queue consumption
- autonomous loop execution
- template-bound action enforcement
- context-proof enforcement
- Steward integration
- next-step decision
- stop-at-gate behavior
```

### 12.2 Agent/context goals

```text
- per-agent context systems
- dynamic context windows
- active/warm/dormant role planning
- route-deeper maps
- context delta receipts
- token/cost-aware context compilation
- removal of stale MINI/CAPSULE as required surfaces
```

### 12.3 UI goals

```text
- live cockpit view model
- JOC shell bound to runtime packets
- persona/user input panel
- live timeline
- agent communication graph
- template gate panel
- Steward integration panel
- human gate panel
- why-stopped panel
- receipt rail
```

### 12.4 Runtime/proof goals

```text
- local autonomous executor
- local simulated worker
- template gate
- Steward integrate command
- survival tests
- restored regression tests
- release verifier
```

### 12.5 Future external-host goals

```text
- MCP bridge retained but not primary
- Cursor extension retained as UI host
- Cursor Auto mode retired as primary carrier
- model/API worker adapters introduced only after local loop proof
```

---

## 13. What must be frozen or demoted

Freeze/demote until survival proof:

```text
- Cursor Auto mode as primary carrier
- new Cursor rules except emergency canonical fixes
- broad UI aesthetics beyond survival cockpit
- new agent names
- new doctrine branches
- production-ready claims
- broad MCP/API authority
- unrestricted daemon claims
```

Do not delete yet:

```text
- old encyclopedia artifacts
- historical receipts
- V40/V41 docs/tests
- JOC shell
- template runtime modules
- front-stage council modules
- release verifier lineage
```

Move to archive later if not needed for survival loop.

---

## 14. Productized runtime shape after recovery

The correct productized root should contain:

```text
pyproject.toml
AGENTS.md
START_HERE_FOR_ANY_AGENT.md
ION/REPO_AUTHORITY.md
ION/00_BOOTSTRAP/
ION/01_doctrine/
ION/02_architecture/
ION/03_registry/
ION/04_packages/kernel/
ION/05_context/current/
ION/05_context/signals/
ION/07_templates/
ION/08_ui/joc_cockpit_shell/
ION/09_integrations/cursor_extension/
ION/tests/
ION/docs/consolidation/
```

It should not contain massive historical archive bodies in the live runtime zip, but it must not drop required tests or evidence surfaces.

---

## 15. Lead-dev operating procedure from here

Every future pass must state:

```text
1. What invariant is being enforced?
2. What command proves it?
3. What test proves it?
4. What receipt records it?
5. What cockpit state exposes it?
6. What was not proven?
```

A pass is not acceptable if it only adds prose.

V98 is allowed to add this master plan because the user explicitly requested a planning/orchestration expansion. After V98 plan, implementation must resume at the minimal autonomous loop.

---

## 16. Final lead-dev judgment

ION should not be cancelled today.

It should also not continue as it has.

The project is advanced enough that deleting it would throw away real architecture, template runtime lineage, agent context work, front-stage council doctrine, UI shell work, and the core maintained-work-surface insight. But the project is also unstable enough that continuing to expand sideways would be irresponsible.

The correct path is a survival sprint:

```text
V98: master recovery plan and UI/automation target lock.
V99/V100 implementation order may shift, but the first executable target remains ion_autonomous_loop.
```

The ultimate standard:

```text
If ION cannot run one template-bound autonomous loop without user sequencing, it is not yet ION.
If it can, then the rest of the project has a real spine to grow from.
```

This document is therefore both a plan and a boundary: ION lives only through executable automation, template enforcement, visible state, and honest receipts.
