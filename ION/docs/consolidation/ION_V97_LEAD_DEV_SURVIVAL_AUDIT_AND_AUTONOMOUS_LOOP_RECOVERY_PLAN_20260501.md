# ION V97 Lead-Dev Survival Audit and Autonomous Loop Recovery Plan

**Date:** 2026-05-01  
**Branch / pass name:** `V97_LEAD_DEV_SURVIVAL_AUDIT_AND_AUTONOMOUS_LOOP_RECOVERY`  
**Artifact class:** internal lead-dev survival document, project recovery map, non-production audit  
**Authority posture:** this document is **not** a production-ready claim, not a global canon ratification, not a proof that ION is autonomous. It is a hard internal recovery map that records what ION is, what is worth saving, what is broken, what is missing, and what must be proven next.

---

## 0. Why this document exists

This file exists because ION reached a crisis point.

The immediate human symptom was not merely frustration with an IDE. The deeper symptom was that the system’s lived behavior contradicted its stated identity. The project has always been meant to automate long-horizon AI work through governed templates, context packages, receipts, agents, queues, graph/event pressure, and continuation. Yet the recent Cursor-hosted workflow repeatedly collapsed back into a weak parent chat asking the user what to do, improvising edits, or forgetting the workflow.

That cannot be dismissed as “Cursor being dumb.” Cursor was inadequate as a primary host carrier, but Cursor also exposed real repo weaknesses:

- multiple written workflow spines existed at once;
- shell-root law was not singular;
- CLI entrypoints were not singular;
- subagent law and saved subagent definitions were not equally strict;
- older `MINI.md`/`CAPSULE.md` continuity law still existed in places after the newer Agent Context System law demoted those surfaces;
- productized zips dropped important historical tests and evidence surfaces;
- the system still lacked one brutally simple autonomous executor command that proves the core loop without Cursor Auto mode.

The purpose of V97 is to stop expansion, stop consolation, stop doctrine drift, and establish a survival recovery plan.

This document takes the lead-dev position that ION is worth saving **only if** the next work proves the autonomous, template-bound loop in a minimal, host-independent way.

---

## 1. Lead-dev verdict

### 1.1 ION is worth saving

ION is worth saving because the root idea is coherent and unusually strong:

> ION turns AI collaboration into governed, inspectable, resumable, auditable, template-bound maintained state.

The project contains real conceptual and runtime assets:

- evented-template runtime modules;
- template registries and template surfaces;
- role and context-package machinery;
- front-stage Persona/Relay/Steward doctrine;
- active packet files;
- operator queue and human gate queue;
- task-return intake;
- compiled role context bundles;
- agent context-system cards;
- context dynamics plan;
- MCP and Cursor extension scaffolds;
- JOC cockpit UI lineage;
- production-readiness and release-verifier concepts;
- extensive receipts and reports.

That is not empty theatre. There is real machinery here.

### 1.2 ION is not currently what it claims to become

ION is not yet a finished autonomous operating system. The strongest current defect is not lack of vision. It is lack of a single enforced, host-independent execution loop.

The current project is best described as:

```text
A powerful, partially executable AI orchestration prototype whose doctrine and runtime are ahead of its minimal autonomous executor.
```

The project must stop behaving as if more doctrine or more host rules will save it. The next proof must be executable.

### 1.3 Cursor Auto mode failed as primary carrier

Cursor Auto mode should no longer be treated as the primary ION host. It can be a code editor, possible extension host, or optional MCP client. It must not be treated as the entity that “understands” ION.

Cursor Auto failed because it was asked to maintain too much protocol in a conversational context. ION’s own goal is to make that unnecessary. A weak host should carry packets, not infer the operating system.

### 1.4 The next survival standard

ION survives only if V97/V98 proves:

```text
one command
→ one goal
→ one workflow decision
→ one template-bound context package
→ one bounded worker or local simulation
→ one template-bound return
→ proof gate
→ Steward integration
→ receipt
→ next-step decision or explicit gate
```

The user must not sequence the agents. The user may provide direction or resolve gates. Everything else is ION’s job.

---

## 2. The root ION identity, restated without mythology

ION is an AI work orchestration runtime and maintained-work-surface architecture.

Its intended function is:

```text
user pressure / objective
→ front-door intake
→ intent packetization
→ authority classification
→ workflow planning
→ template selection
→ context package compilation
→ agent/worker execution
→ template-bound result
→ receipt
→ integration
→ graph/state update
→ next continuation
```

ION is not just:

- a README;
- a set of prompts;
- a chatbot persona;
- a memory/RAG layer;
- a pile of Markdown protocols;
- a Cursor rules folder;
- a UI dashboard.

ION is only ION when work becomes governed state and the next lawful action can be resumed without hidden oral context.

---

## 3. Non-negotiable canon that must be preserved

### 3.1 Automation canon

ION was always meant to automate workflow. A user should not need to tell ION which agent to spawn, which packet to refresh, which context to load, or which receipt to write.

The user may set direction, say `continue` or `/ion`, answer a human gate, grant or deny authority, correct the system, inspect, and steer. The user should not be required to manage internal upkeep.

### 3.2 Template canon

Agents must not perform arbitrary unstructured work. Meaningful work must be bound to templates or equivalent runtime contracts.

Canonical movement should be template-bound:

```text
intake
context package
mission packet
task output
agent return
receipt
repair event
graph proposal
review verdict
bounded commit
handoff
status report
```

A non-template action should either be rejected or converted into a template-bound event before it can become accepted state.

### 3.3 Maintained work surface canon

ION turns collaboration itself into infrastructure. User intent, AI synthesis, artifacts, visual evidence, claim classes, receipts, gates, and continuation obligations must become inspectable state, not transient chat performance.

### 3.4 Front-stage council canon

The user-facing ION surface is not one magical Persona pretending to contain all truth.

The governing front-stage split is:

```text
Persona Interface → user-facing expression and relationship horizon
Relay → grounding, packetization, transport, provenance, semantic boundary
Steward/VZ → authority, risk, claim class, work legitimacy, orchestration
```

Persona may render accepted state. Relay grounds and packages. Steward/VZ authorizes and integrates. These should be logically present in the workflow even when not fully spawned as separate workers every turn.

### 3.5 Agent role canon

Agents are not fantasy identities. They are governed role surfaces with true names, scope, templates, authority ceilings, receipts, and context packages.

### 3.6 Evidence discipline canon

No claim counts merely because it appears in fluent prose. Evidence must be expressed through files, commands, tests, receipts, manifests, hashes, or explicit boundaries.

### 3.7 Non-production boundary

The project must not claim production readiness until production gates, adversarial audit, release candidate, and verifier conditions pass. The current survival work is not a production claim.

---

## 4. What is actually present in the current V96 runtime

### 4.1 Top-level authority surfaces

The root contains:

```text
pyproject.toml
ION/REPO_AUTHORITY.md
AGENTS.md
START_HERE_FOR_ANY_AGENT.md
.cursor/
.vscode/
ION/
```

This supports the shell-root invariant:

```text
shell root = directory containing pyproject.toml and ION/REPO_AUTHORITY.md as siblings.
```

### 4.2 Active runtime packets

The current runtime includes active packet files:

```text
ION/05_context/current/ACTIVE_WORK_PACKET.json
ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json
ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json
ION/05_context/current/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json
ION/05_context/current/ACTIVE_STEWARD_INTEGRATION_QUEUE.json
ION/05_context/current/ACTIVE_OPERATOR_MESSAGE_QUEUE.json
ION/05_context/current/ACTIVE_HUMAN_GATE_QUEUE.json
ION/05_context/current/ACTIVE_CURSOR_AUTOPILOT_PACKET.json
ION/05_context/current/ACTIVE_AGENT_CONTEXT_WINDOW_PLAN.json
ION/05_context/current/ACTIVE_FRONT_DOOR_TEAM_PLAN.json
ION/05_context/current/ACTIVE_COCKPIT_VIEW_MODEL.json
ION/05_context/current/ACTIVE_MCP_BRIDGE_STATE.json
```

This is strong evidence that the project is not merely prose. It has packet state.

### 4.3 Carrier and Cursor-control modules

The current runtime contains:

```text
ION/04_packages/kernel/ion_carrier_continue.py
ION/04_packages/kernel/ion_carrier_task_return.py
ION/04_packages/kernel/ion_carrier_workflow_audit.py
ION/04_packages/kernel/ion_cursor_autopilot_packet.py
ION/04_packages/kernel/ion_cursor_autopilot_audit.py
ION/04_packages/kernel/ion_cursor_canonical_workflow_audit.py
ION/04_packages/kernel/ion_compiled_role_context_bundle_audit.py
ION/04_packages/kernel/ion_operator_message_classifier.py
ION/04_packages/kernel/ion_operator_message_queue.py
ION/04_packages/kernel/ion_human_gate_queue.py
ION/04_packages/kernel/ion_status.py
```

These are real control-loop components, but they are not yet enough to prove host-independent autonomy.

### 4.4 Agent context-system layer

The current runtime contains:

```text
ION/02_architecture/ION_AGENT_CONTEXT_SYSTEMS_PROTOCOL.md
ION/03_registry/agent_context_system_registry.yaml
ION/05_context/current/agent_context_systems/*.context_system.md
ION/04_packages/kernel/ion_agent_context_systems.py
ION/04_packages/kernel/ion_agent_context_dynamics.py
```

It includes role context-system cards for:

```text
STEWARD
VIZIER
MASON
NEMESIS
VICE
RELAY
VESTIGE
THOTH
SCRIBE
PERSONA_INTERFACE
ATLAS
IONOLOGIST
CONTEXT_CARTOGRAPHER
RUNTIME_CARTOGRAPHER
CANON_LIBRARIAN
TEMPLATE_CURATOR
```

This is one of the most important salvageable advances.

### 4.5 Template system surfaces

The current runtime contains substantial template surfaces under:

```text
ION/07_templates/
```

Important subdirectories include:

```text
actions/
agents/
automation/
bindings/
carriers/
confidence/
context/
context_graph/
custom_gpt/
```

Important context templates include:

```text
ION/07_templates/context/AGENT_CONTEXT_PACKAGE.md
ION/07_templates/context/AGENT_CONTEXT_SYSTEM_CARD.md
ION/07_templates/context/AGENT_CONTEXT_BUILD_STEP.md
ION/07_templates/context/AGENT_CONTEXT_PACKAGE_INDEX.md
ION/07_templates/context/AGENT_DYNAMIC_CONTEXT_WINDOW_PLAN.md
ION/07_templates/context/ION_CONTEXT_DELTA_RECEIPT.md
ION/07_templates/context/ION_CONTEXT_LOAD_PROOF.md
ION/07_templates/context/EVENTED_TEMPLATE_FILE_OBJECT.md
```

This confirms that templates exist and are central.

### 4.6 Evented-template runtime modules

The current runtime contains evented-template/kernel modules, including:

```text
ION/04_packages/kernel/template_metadata_contracts.py
ION/04_packages/kernel/template_completion_events.py
ION/04_packages/kernel/template_reaction_selection.py
ION/04_packages/kernel/template_index_projection.py
ION/04_packages/kernel/template_graph_writeback_proposals.py
ION/04_packages/kernel/template_graph_writeback_review.py
ION/04_packages/kernel/template_graph_commit.py
```

This is the old ION heart and must be preserved.

### 4.7 UI/JOC cockpit lineage

The runtime contains:

```text
ION/08_ui/joc_cockpit_shell/
ION/09_integrations/cursor_extension/
ION/04_packages/kernel/ion_cockpit_view_model.py
```

The UI is not the survival priority, but it is an important future observation surface once the autonomous loop is proven.

### 4.8 MCP and SDK surfaces

The runtime contains:

```text
ION/09_integrations/mcp/ion_mcp_server.py
ION/09_integrations/cursor_sdk/
.cursor/mcp.json
```

These should be treated as optional host bridges, not primary authority.

---

## 5. The most important current defects

### 5.1 Defect A — the autonomous executor is not proven

ION still lacks one central command that proves the full loop:

```text
goal
→ queue
→ planner
→ template-bound role package
→ worker execution or simulation
→ template-bound return
→ proof/template gate
→ Steward integration
→ receipt
→ next step
```

There are many partial components, but no single minimal host-independent proof loop currently dominates the project.

This is the highest-priority blocker.

### 5.2 Defect B — `sequential_kernel.py` still preserves old MINI/CAPSULE requirements

Static inspection of `ION/04_packages/kernel/sequential_kernel.py` shows role continuity targets still referencing old paths such as:

```text
ION/agents/steward/MINI.md
ION/agents/steward/CAPSULE.md
ION/agents/vizier/MINI.md
ION/agents/vizier/CAPSULE.md
ION/agents/mason/MINI.md
ION/agents/mason/CAPSULE.md
```

The productized V96 root does not contain `ION/agents/`.

This contradicts the newer Agent Context System law that says MINI/CAPSULE are witness inputs, not primary context authority. It also contradicts productized runtime packaging if those files are omitted.

Repair requirement:

```text
sequential_kernel.py must be updated so required continuity targets resolve through Agent Context System cards and compiled context bundles. Legacy MINI/CAPSULE may remain optional witness inputs only if present.
```

### 5.3 Defect C — test surfaces were reduced too aggressively in V96

The V96 productized root contains only a small subset of tests. Earlier encyclopedia and V40/V41 surfaces expect tests such as:

```text
ION/tests/test_kernel_maintained_work_surface.py
ION/tests/test_kernel_front_stage_council_receipt.py
ION/tests/test_kernel_production_readiness.py
```

Some of these are absent from the V96 productized root. This makes V96 unsafe to call a full runtime consolidation.

Repair requirement:

```text
Restore the focused historical/runtime tests required to verify old canon surfaces, or clearly mark V96 as a reduced survival runtime instead of full consolidated runtime.
```

### 5.4 Defect D — production-readiness lineage remains stale

The project still contains production-readiness surfaces whose next-sequence language may not match the later V40/V41/V42/V96 branch reality.

This does not mean ION is production-ready or failed. It means branch numbers and production gates must be separated. This was already recognized in the encyclopedia.

Repair requirement:

```text
Create a branch/gate namespace reconciliation module and report that separates live branch lineage from production-gate sequence.
```

### 5.5 Defect E — template canon is present but not universally enforced

The template system exists. The evented-template runtime exists. But the newer carrier loop does not yet prove that every agent action is rejected unless it is template-bound or converted into a template-bound receipt.

Repair requirement:

```text
Add a template-action gate to the minimal autonomous loop. A worker return must identify its template contract and produce a valid template-bound receipt or be rejected.
```

### 5.6 Defect F — Steward integration queue exists but integration loop is incomplete

`ACTIVE_STEWARD_INTEGRATION_QUEUE.json` exists, and task-return intake can feed it. But the next crucial behavior is not yet proven:

```text
Steward consumes accepted returns, writes integration receipt, updates work state, chooses next step.
```

Repair requirement:

```text
Build a minimal Steward integration executor that consumes accepted returns and emits the next continuation state.
```

### 5.7 Defect G — Cursor host rules became a distraction

Cursor rules, commands, skills, hooks, MCP, subagents, and extension files are valuable only if the kernel loop exists. They should no longer be expanded before the minimal autonomous loop is proven.

Repair requirement:

```text
Freeze Cursor host expansion until V97/V98 minimal autonomous loop passes.
```

---

## 6. What must not be deleted

Even if the Cursor path is frozen, the following should be preserved because they represent core ION value.

### 6.1 Evented-template runtime

Preserve:

```text
ION/07_templates/
ION/04_packages/kernel/template_metadata_contracts.py
ION/04_packages/kernel/template_completion_events.py
ION/04_packages/kernel/template_reaction_selection.py
ION/04_packages/kernel/template_index_projection.py
ION/04_packages/kernel/template_graph_writeback_proposals.py
ION/04_packages/kernel/template_graph_writeback_review.py
ION/04_packages/kernel/template_graph_commit.py
```

### 6.2 Front-stage council / maintained work surface

Preserve:

```text
ION/01_doctrine/MAINTAINED_WORK_SURFACE_CANON.md
ION/02_architecture/FRONT_STAGE_COUNCIL_PROTOCOL.md
ION/02_architecture/FRONT_STAGE_COUNCIL_RUNTIME_RECEIPT_PROTOCOL.md
ION/02_architecture/REPRESENTATIONAL_INTEGRITY_PROTOCOL.md
ION/04_packages/kernel/front_stage_council_receipt.py
ION/04_packages/kernel/maintained_work_surface.py
```

### 6.3 Agent Context Systems

Preserve:

```text
ION/02_architecture/ION_AGENT_CONTEXT_SYSTEMS_PROTOCOL.md
ION/03_registry/agent_context_system_registry.yaml
ION/05_context/current/agent_context_systems/
ION/04_packages/kernel/ion_agent_context_systems.py
ION/04_packages/kernel/ion_agent_context_dynamics.py
```

### 6.4 Carrier packet spine

Preserve:

```text
ION/04_packages/kernel/ion_carrier_continue.py
ION/04_packages/kernel/ion_cycle_runner.py
ION/04_packages/kernel/ion_carrier_task_return.py
ION/04_packages/kernel/ion_operator_message_queue.py
ION/04_packages/kernel/ion_human_gate_queue.py
ION/04_packages/kernel/ion_status.py
```

### 6.5 Receipts and reports

Preserve receipts, reports, manifests, and key active packet outputs. They are necessary to reconstruct lineage.

---

## 7. What should be frozen or demoted

### 7.1 Cursor Auto mode as primary carrier

Cursor Auto mode should be demoted to failed/unsafe primary carrier. It may remain an editor or optional extension host.

### 7.2 New UI work

The cockpit is valuable, but UI expansion must freeze until the minimal autonomous loop is proven.

### 7.3 New agent naming

No new agents should be created until the existing role system is made executable.

### 7.4 New doctrine

No new doctrine should be added unless it directly supports executable enforcement.

### 7.5 New Cursor rules

No new Cursor rules should be added until the kernel loop is proven. Rules cannot substitute for runtime enforcement.

---

## 8. Required V97/V98 survival implementation

The next real implementation should be named:

```text
V98_MINIMAL_AUTONOMOUS_LOOP_SURVIVAL_PROOF
```

V97 is this survival audit and recovery plan. V98 should build the proof.

### 8.1 New module

Add:

```text
ION/04_packages/kernel/ion_autonomous_loop.py
```

### 8.2 CLI

The command should be:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_autonomous_loop --ion-root . --goal "Find one repo contradiction and propose one patch" --max-steps 3 --write --json
```

### 8.3 Required behavior

The command must:

1. resolve shell root;
2. classify the goal;
3. append or consume an operator message queue item;
4. select exactly one next work item;
5. choose exactly one role for the first pass;
6. compile a context package from Agent Context System surfaces, not legacy MINI/CAPSULE;
7. bind the task to a template contract;
8. execute either a local deterministic worker simulation or a real bounded worker adapter;
9. require the return to include `### CONTEXT PROOF` and a template contract declaration;
10. run return intake;
11. run template-action gate;
12. feed accepted return into Steward integration;
13. write Steward integration receipt;
14. decide whether next step exists or a gate is required;
15. write a final loop receipt.

### 8.4 Required output files

The command should write:

```text
ION/05_context/current/ACTIVE_AUTONOMOUS_LOOP_STATE.json
ION/05_context/current/ACTIVE_AUTONOMOUS_LOOP_PLAN.json
ION/05_context/current/ACTIVE_AUTONOMOUS_LOOP_LAST_RETURN.md
ION/05_context/current/ACTIVE_AUTONOMOUS_LOOP_STEWARD_INTEGRATION.json
ION/05_context/signals/v98_minimal_autonomous_loop_receipt_<date>.txt
ION/docs/consolidation/ION_V98_MINIMAL_AUTONOMOUS_LOOP_SURVIVAL_PROOF_REPORT_<date>.md
```

### 8.5 Acceptance tests

Add:

```text
ION/tests/test_kernel_ion_autonomous_loop.py
```

Tests must prove:

```text
- valid goal creates loop state
- loop selects a role without user sequencing
- context package uses Agent Context System, not required legacy MINI/CAPSULE
- non-template return is rejected
- return without CONTEXT PROOF is rejected
- valid deterministic worker return is accepted
- Steward integration receipt is written
- next step or stop condition is recorded
```

---

## 9. Template-action gate requirement

V98 must add or reuse a module such as:

```text
ION/04_packages/kernel/ion_template_action_gate.py
```

Purpose:

```text
Reject agent returns that do not identify and satisfy a template/action contract.
```

Minimum required fields in a valid return:

```text
### CONTEXT PROOF
role:
context_package_path:
loaded_surfaces:

### TEMPLATE CONTRACT
contract_id:
template_path:
output_class:
required_fields_satisfied:

### RESULT
findings_or_patch:
changed_files:
validation:
risks:
next_recommended_action:
```

This bridges the newer context-proof gate with the older evented-template heart.

---

## 10. Sequential kernel repair requirement

V98 or the preceding quick repair must modify `sequential_kernel.py`.

Current bad pattern:

```text
required continuity_targets include ION/agents/<role>/MINI.md and CAPSULE.md
```

Correct pattern:

```text
required continuity target = role Agent Context System card
optional witness target = legacy MINI/CAPSULE if present
required executable target = compiled role context bundle / generated context package
```

This must be audited by a new test:

```text
ION/tests/test_kernel_sequential_kernel_context_system_alignment.py
```

Acceptance:

```text
- validate_current_runtime does not fail because ION/agents/*/MINI.md is absent
- each role has an Agent Context System target
- legacy MINI/CAPSULE targets are optional witness inputs only
```

---

## 11. Full test restoration requirement

V96 productized packaging became too aggressive.

Required action:

1. Compare V96 `ION/tests/` against V88 and earlier canonical roots.
2. Restore tests required for:
   - maintained work surface;
   - front-stage council receipt;
   - production readiness;
   - evented-template runtime;
   - release verifier where available;
   - carrier loop;
   - context systems;
   - compiled role bundles.
3. Separate tests into:
   - survival tests;
   - focused runtime tests;
   - historical/canon tests;
   - production-gate tests.

Do not call the project consolidated/full unless test surfaces are intentionally preserved or explicitly demoted.

---

## 12. Future roadmap after survival proof

Only after V98 passes should future plans resume.

### 12.1 V99 — Template-Enforced Agent Movement

Make the template-action gate universal across role returns and Steward integration.

### 12.2 V100 — Steward Integration Executor

Build real Steward integration that consumes accepted returns, updates active work state, opens gates, and chooses next work.

### 12.3 V101 — Context Timeline and Delta Receipts

Add per-agent context timelines and context delta receipts.

### 12.4 V102 — Context Graph Route Planner

Implement graph-aware route-deeper planning across context groups.

### 12.5 V103 — Token/Cost-Aware Context Compiler

Bind context package generation to model/context budget and provider routing.

### 12.6 V104 — Host Adapter Layer

Add model/API/SDK worker adapters only after the local deterministic loop passes.

### 12.7 V105 — Cockpit Reactivation

Reactivate the JOC/Cursor cockpit as observer/controller once the loop has state worth observing.

### 12.8 V106 — MCP / Remote Control Gate

Only after the loop is safe should MCP remote control be reintroduced with permissions, auth, and command gate.

### 12.9 V107 — Production Gate Namespace Repair

Reconcile live branch versions with production gates and production-readiness sequence.

### 12.10 V108 — Adversarial Production Audit Preparation

Begin adversarial audit only after local loop, template enforcement, and Steward integration are proven.

---

## 13. Agent role survival map

### STEWARD

Must become the integration executor, not a vague orchestrator. It consumes accepted returns and writes next state.

### RELAY

Must packetize user intent and accepted state. It must not create authority.

### PERSONA_INTERFACE

Must speak from accepted state. It must not pretend to be all of ION.

### CONTEXT_CARTOGRAPHER

Must own context-package compilation and context timeline evolution.

### RUNTIME_CARTOGRAPHER

Must own actual executable path, CLI, gates, audits, and host adapters.

### CANON_LIBRARIAN

Must classify live/donor/archive/stale authority and prevent old surfaces from becoming current by accident.

### TEMPLATE_CURATOR

Must own template contracts and receipt shapes. This role is essential for restoring template enforcement.

### MASON

Must implement bounded patches from exact contracts. Mason should not design the architecture while patching.

### NEMESIS

Must reject false proof, unbacked validation, non-template returns, and overclaims.

### VIZIER

Must handle architecture sequencing and dependency implications.

### VESTIGE

Must recover lineage and stale context, but not promote donor authority.

### THOTH

Must perform deep reasoning and research synthesis under non-mutating boundaries.

### SCRIBE

Must write reports and receipts from accepted state only.

### VICE

Must track contradictions and future-answerability risks.

### ATLAS

Must provide external systems reference and provider routing context without becoming ION continuity authority.

---

## 14. No-user-upkeep law

This law must become executable.

```text
The user is not ION’s scheduler.
The user is not ION’s context manager.
The user is not ION’s task router.
The user is not ION’s receipt writer.
The user is not ION’s test selector.
The user is not ION’s agent-spawn planner.
```

The user provides direction and resolves explicit gates.

Every time ION asks the user to sequence ordinary work, that is a failure.

---

## 15. Kill conditions

The project should be frozen or canceled if the following remain true after the survival sprint:

```text
- no one-command autonomous loop exists;
- non-template worker returns can become accepted state;
- Steward cannot integrate accepted returns;
- the system cannot decide a next step without user sequencing;
- old MINI/CAPSULE required paths still block the new context system;
- production/readiness claims continue to exceed focused evidence;
- Cursor Auto mode is reintroduced as primary carrier before local loop passes.
```

These are not emotional conditions. They are engineering conditions.

---

## 16. Why ION should not be erased today

Do not erase ION because Cursor failed.

Do not erase ION because V96 is imperfect.

Erase ION only if the minimal autonomous loop cannot be built or proven.

The project contains too much real machinery and too much correct design to delete before this proof. But the project also contains too much drift to continue expanding without the proof.

The correct posture is:

```text
Freeze expansion.
Preserve V96/V97.
Build V98 survival proof.
Make the result decisive.
```

---

## 17. Current lead-dev operating rules

From this document forward, lead-dev work should follow these rules:

1. No new doctrine unless paired with enforcement.
2. No new UI unless the runtime state exists.
3. No new Cursor law unless the local loop passes.
4. No new agents until existing roles are executable.
5. No production claim without verifier.
6. No full-consolidation claim if tests are dropped.
7. No context-system claim if legacy paths remain required.
8. No automation claim unless one command advances work.
9. No template claim unless non-template action is rejected.
10. No Steward claim unless accepted returns are integrated.

---

## 18. Immediate next work packet

```yaml
work_packet_id: v98_minimal_autonomous_loop_survival_proof
objective: Build and verify the smallest host-independent ION autonomous loop.
authority_posture: survival_proof_only_not_production
must_not_do:
  - expand Cursor rules
  - expand UI/cockpit
  - add new agents
  - add new doctrine without enforcement
  - claim production readiness
required_repairs:
  - sequential_kernel context-system alignment
  - template-action gate
  - autonomous loop executor
  - Steward integration minimal executor
  - focused tests
  - receipt/report
acceptance:
  - one CLI command advances a goal through template-bound workflow without user sequencing
  - invalid/non-template returns are rejected
  - valid deterministic return is accepted and integrated
  - next step or gate is recorded
```

---

## 19. Final statement

ION is not dead.

ION is not production.

ION is not currently allowed to keep expanding sideways.

The project must now prove its root promise:

```text
Automated, template-bound, receipt-bearing, agent-mediated continuation without user micromanagement.
```

If V98 proves that, ION has a future.

If V98 cannot prove that, the project should be frozen with dignity instead of continuing to exhaust its builder.
