---
protocol_id: ion.agent_context_continuity_timeline_and_route_map.protocol.v1
status: ACTIVE_DESIGN_LOCK
rank: A2_CONTEXT_AUTHORITY
created: 2026-05-01
branch: V99_AGENT_CONTEXT_CONTINUITY_AND_RUNTIME_SEPARATION_DESIGN
binds:
  - ION/02_architecture/ION_AGENT_CONTEXT_SYSTEMS_PROTOCOL.md
  - ION/02_architecture/ION_AGENT_CONTEXT_DYNAMICS_AND_CONTEXT_WINDOW_PROTOCOL.md
  - ION/02_architecture/ION_COMPILED_ROLE_CONTEXT_BUNDLE_INVARIANT_PROTOCOL.md
  - ION/02_architecture/META_TEMPLATE_CONSTITUTION_PROTOCOL.md
  - ION/02_architecture/EVENTED_TEMPLATE_FILE_GRAPH_PROTOCOL.md
  - ION/02_architecture/ION_PRODUCTIZED_RUNTIME_BOUNDARY_PROTOCOL.md
---

# ION Agent Context Continuity, Timeline, and Route Map Protocol

## 1. Purpose

ION agents must not be treated as role names plus prompts. An ION agent is a governed, evolving context system whose live context is compiled from durable identity, mission state, route maps, templates, receipts, prior packages, and accepted deltas. This protocol defines the next context-system shape required for ION to become understandable to weak carriers and durable enough for high-end agents to resume serious work without the user re-explaining the project.

This protocol does not replace the existing Agent Context Systems Protocol or the Agent Context Dynamics planner. It extends them with a navigable context timeline and route map layer.

The target state is:

```text
agent true name
→ durable role context system
→ current attention lease
→ active mission package
→ route map to deeper branches
→ token/cost/depth budget
→ template/action contract
→ context load proof
→ task return
→ template action proof
→ Steward integration
→ context delta receipt
→ next package/timeline event
```

## 2. Core model

Every serious ION role receives a **Main Context Package**. That package is not merely a prompt. It is a compiled, bounded, evidence-indexed state object with the following parts:

```text
1. Identity Envelope
2. Authority Envelope
3. Live ION Definition Slice
4. Role Domain Slice
5. Mission Slice
6. Active Work State Slice
7. Route Map Slice
8. Template Contract Slice
9. Budget/Depth Slice
10. Recent Timeline Slice
11. Prior Package Index Slice
12. Forbidden Drift Slice
13. Output Contract Slice
14. Receipt Targets
```

The package may be rendered as Markdown for human/model readability, but it must also have a machine-readable receipt and index. The Markdown is the executable briefing; the receipt is the proof surface.

## 3. Context timeline law

Each role must have a timeline capable of answering:

```text
What did this role know last time?
What changed since then?
Which package was loaded?
Which routes were available but not loaded?
Which templates were active?
Which output was accepted, rejected, held, or gated?
Which context deltas now affect future packages?
```

A context timeline event is not a generic log entry. It is an event in the agent's memory economy. It determines what should be summarized, retained, deepened, or forgotten from the next package.

Required event classes:

```text
context_package_compiled
context_package_loaded
route_deeper_requested
route_deeper_granted
route_deeper_denied
context_delta_proposed
context_delta_accepted
context_delta_rejected
template_contract_selected
template_action_accepted
template_action_rejected
steward_integrated
human_gate_opened
human_gate_resolved
package_superseded
package_archived
```

## 4. Route map law

The role's package must include the routes to other branches without loading every branch. A route is a lawful affordance, not a pointer dump. Each route must say:

```text
route_id
surface_path_or_query
why_available
when_to_open
expected_token_cost
authority_risk
owning_role
allowed_action_after_reading
receipt_required
```

Example route classes:

```text
canonical_law_route
active_state_route
historical_lineage_route
template_shape_route
runtime_command_route
ui_visibility_route
provider_cost_route
proof_receipt_route
stale_surface_route
archive_recovery_route
```

The main package should carry enough route data for judgement but not enough bulk to drown the role. Deep context should be pulled only by trigger.

## 5. Rolling context windows

ION context must use multiple rolling windows, not one giant blob.

### 5.1 Durable identity window

Slow-changing. Contains true name, role boundary, authority ceiling, forbidden conflations, and permanent doctrine relevant to the role.

### 5.2 Operational mission window

Fast-changing. Contains the current goal, active work packet, active spawn row, relevant queue/gate state, and current exit condition.

### 5.3 Evidence window

Bounded. Contains exact file paths, snippets, test names, receipts, and hashes required to support the current claim or action.

### 5.4 Route-deeper window

Map-only by default. Shows where deeper context lives and when opening it is lawful.

### 5.5 Template/action window

Contains the exact output shape the role must fill. This window becomes hard-gated by `TEMPLATE ACTION PROOF`.

### 5.6 Conversation/front-door window

Persona/Relay-specific. Contains the user-facing history and accepted state summary, not raw unintegrated worker speculation.

### 5.7 Model/carrier window

Carrier-specific. Contains prompt shape, host limits, tool availability, token budget, and what the host must not pretend to do.

### 5.8 Context delta window

The bridge from one package to the next. It records what changed, who is affected, and which future package layers must refresh.

## 6. Package compilation sequence

A lawful package compiler should execute this order:

```text
1. Resolve shell root.
2. Resolve role true name and role context-system card.
3. Resolve active operator objective and queue/gate pressure.
4. Determine attention lease: active/warm/dormant/blocked/retired.
5. Select depth: minimum/normal/deep.
6. Select template/action contract.
7. Read durable base surfaces.
8. Read active runtime packet surfaces.
9. Read mission-specific evidence surfaces.
10. Build route map without overloading history.
11. Attach token/cost/depth budget.
12. Attach output contract and receipt target.
13. Write compiled package.
14. Write context load receipt.
15. Update role context timeline.
```

The package is invalid if it says only "read these 20 files." Paths are provenance anchors and route affordances; the active package must load the context needed for the step.

## 7. Token/cost/depth semantics

The context system should know the cost of thought.

Each package should declare:

```text
carrier_or_model
context_limit_estimate
package_char_count
package_token_estimate
reserved_output_budget
route_deeper_budget
budget_class
compression_ratio_vs_source
omitted_high_risk_surfaces
```

The active budget classes are:

```text
minimum — enough to execute a constrained step
normal — enough to reason safely about ordinary task implications
deep — enough to handle architecture, conflict, recovery, or high-risk routing
forensic — enough to reconstruct lineage; rarely loaded into a worker directly
```

## 8. Template evolution and context evolution

Templates evolve context by forcing work into stable shapes. The completed template is the event. Indexes, registries, summaries, receipts, graph updates, and future packages are projections from that completed event.

Correct flow:

```text
template filled
→ template action proof validated
→ event recorded
→ affected indexes refreshed
→ affected role context timelines updated
→ context deltas written
→ next packages compile from accepted deltas
```

Incorrect flow:

```text
agent improvises prose
→ prose is treated as state
→ later agent reads prose as authority
→ drift becomes canon
```

## 9. Lead-dev context control surface

The GPT-5.5 lead-dev continuity layer should not be installed as another ordinary ION role before the survival loop passes. It should be represented as a **carrier-side context control surface** that compiles the project state needed for this ChatGPT instance to act as lead developer across uploaded bundles.

Its job is:

```text
- identify the authoritative uploaded base and overlays;
- preserve what was actually inspected;
- maintain a current true-north plan;
- track which claims are proven vs planned;
- compile next work packets for local implementation;
- avoid inventing runtime success not backed by tests;
- hand back compact overlays or full zips honestly;
- keep ION's no-user-upkeep law centered.
```

It is not allowed to claim persistent hidden control over ION. It is a package discipline for this carrier, not a mystical resident AI.

## 10. Runtime separation requirement

ION must separate:

```text
runtime_core/        kernel modules, CLI, registries, templates required to run
runtime_state/       current active packets, queues, gates, receipts, context systems
execution_cycles/    generated packages and return evidence from runs
ui_surface/          cockpit shell and view model
historical_archive/  older docs, donor branches, prior zips, obsolete receipts
release_overlay/     small patch zips containing only changed files
```

The repository may keep the existing folder names, but the productized zip must respect the conceptual separation. The live runtime zip should not carry massive historical bulk unless explicitly packaged as an archive edition.

## 11. Acceptance condition

This protocol is active when:

```text
- each active role has a context-system card;
- each generated role package has a route map and budget/depth declaration;
- each generated package has a context load receipt;
- each accepted return has both CONTEXT PROOF and TEMPLATE ACTION PROOF;
- each accepted context change produces a context delta/timeline event;
- UI/cockpit can show the package, route map, template gate, and why-stopped state;
- lead-dev carrier work distinguishes full base zips from overlay zips.
```

Until this is enforced in code, this protocol is a design lock and implementation target, not production proof.
