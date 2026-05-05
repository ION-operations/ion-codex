# ION V99 Agent Context Continuity and Runtime Separation Design

**Date:** 2026-05-01  
**Branch / pass name:** `V99_AGENT_CONTEXT_CONTINUITY_AND_RUNTIME_SEPARATION_DESIGN`  
**Artifact class:** design lock + lead-dev context control surface overlay  
**Authority posture:** non-production; this pass adds a context-system design and lead-dev carrier continuity surface. It does not claim the autonomous loop is implemented.

---

## 0. What this pass does

This pass captures the deeper context-system architecture requested by the operator. It turns the discussion into repo-addressable design surfaces:

```text
ION/02_architecture/ION_AGENT_CONTEXT_CONTINUITY_TIMELINE_AND_ROUTE_MAP_PROTOCOL.md
ION/05_context/current/agent_context_systems/LEAD_DEV_CONTEXT_CONTROL_SURFACE.context_system.md
ION/05_context/current/ION_RUNTIME_SEPARATION_PLAN_V99.json
ION/05_context/current/PRODUCTIZED_RUNTIME_MANIFEST_V99.json
ION/05_context/signals/v99_agent_context_continuity_and_runtime_separation_receipt_20260501.txt
```

The pass intentionally does not pretend to implement `ion_autonomous_loop.py`. V98 correctly identifies that as the next enforcement step. V99 exists to lock the context architecture so the loop knows what kind of packages, routes, timelines, and receipts it must eventually create.

---

## 1. Current artifact reading

The latest uploaded line has the following shape:

```text
V96 = full runtime base / current consolidated root candidate.
V97 = small lead-dev survival audit overlay.
V98 = small master orchestration, automation, template enforcement, and UI recovery overlay.
```

This matters because V97/V98 are not full roots. They are overlays to apply to a full base. Treating them as standalone projects would recreate the same drift ION is trying to prevent.

V98 is directionally correct: it names the missing survival spine as a host-independent autonomous loop, with local deterministic worker first, template-action proof, Steward integration, explicit stop reasons, receipts, and cockpit state.

---

## 2. The AI context system in ION

The strongest way to describe ION's AI context architecture is:

```text
ION does not give an AI a memory. ION gives an AI a governed context economy.
```

A normal chat context is a flat, decaying text buffer. ION instead wants the AI to receive a lawful context package with explicit identity, mission, authority, route map, evidence, template, output contract, and receipt obligations.

An ION AI context is therefore not merely what the model can remember. It is the live boundary between:

```text
what the role is;
what the role may do;
what the role currently needs;
what the role may inspect next;
what the role must not conflate;
what output shape is valid;
what evidence will make the output accepted;
what future context changes if accepted.
```

This is the correct successor to legacy boot-file or MINI/CAPSULE onboarding. Boot files can preserve identity lineage, but they do not guarantee that the AI actually has the working context needed for the current task.

---

## 3. Main Context Package

Each AI should receive a **Main Context Package** compiled by ION.

A good package contains:

```text
1. True name and role identity.
2. Authority ceiling and forbidden conflations.
3. Live ION definition relevant to that role.
4. Current objective and exit condition.
5. Active queues/gates/returns that affect this role.
6. Required evidence surfaces already loaded.
7. Route-deeper map to unloaded surfaces.
8. Token/cost/depth budget.
9. Template/action contract.
10. Output contract and receipt path.
11. Context-load proof requirements.
12. Delta/timeline update requirements.
```

The package must not be a pointer file. It should contain the actual condensed context for the current step, plus routes for deeper context when necessary.

The route map is what gives the AI the feeling of a navigable world without forcing all history into the prompt.

---

## 4. Rolling context windows

ION should maintain several rolling windows simultaneously.

The **durable identity window** changes rarely. It prevents role drift.

The **mission window** changes quickly. It says what the role is doing now.

The **evidence window** carries exact files, commands, tests, receipts, and claims.

The **route-deeper window** is a navigation graph, not bulk history.

The **template/action window** defines what the role must fill.

The **conversation/front-door window** belongs mostly to Persona and Relay. It should be based on accepted state, not unintegrated worker speculation.

The **model/carrier window** captures host constraints: ChatGPT, Cursor, Codex, MCP, API, local model, or deterministic worker.

The **context delta window** records what changed and which future packages must refresh.

This is the real solution to the repeated problem where an AI either receives too little context and pretends, or receives too much undifferentiated context and drowns.

---

## 5. How templates evolve context

Templates are not stationery. In ION, a completed template is a state event.

The ideal chain is:

```text
template/action selected
→ role package compiled
→ role fills bounded output
→ context proof accepted
→ template action proof accepted
→ Steward integrates
→ receipts written
→ indexes/projected files refreshed
→ affected role timelines receive context deltas
→ future packages change
```

That means templates evolve context by creating accepted, typed events. The template determines which downstream indexes, registries, context cards, and timelines should be touched.

This is why the evented-template runtime is central. It is the difference between a model saying something plausible and ION turning that result into maintained state.

---

## 6. Persona, Relay, Steward, and rolling front-door context

The front door must not be a magical persona pretending to know everything.

The correct split remains:

```text
Persona Interface — user-facing expression, continuity, tone, relationship horizon.
Relay — packetization, provenance, semantic transport, grounding.
Steward/Vizier — routing, authority, gate control, integration.
```

Persona should see a user-facing package: accepted state, current uncertainty, what can be said honestly, and what should remain internal. Relay should see packet and provenance context. Steward should see integration authority, queues, returns, blockers, gates, and next-action options.

The parent carrier chat is not this triad. It runs commands and moves packets. If the carrier starts acting as Steward from memory, ION has already degraded.

---

## 7. Context graph and route-deeper maps

The user's instinct about a full map of branches, token costs, past context packages, and navigable timelines is exactly the missing layer.

The role should receive something like:

```text
Loaded now:
- current mission packet
- role law
- exact template
- relevant active queue/gate state

Available routes:
- deeper law route: 8k tokens, open if authority conflict arises
- template route: 4k tokens, open if output shape unclear
- runtime route: 12k tokens, open if command fails
- historical lineage route: 40k tokens, open only for stale-canon dispute
- UI route: 8k tokens, open if operator visibility is affected
```

This would let ION stop loading everything by default while still preventing agents from pretending they know what they have not read.

---

## 8. Lead-dev self-context layer

The lead-dev layer should exist, but not as a new fantasy agent.

The correct object is a **carrier-side context control surface** for GPT-5.5 in this workstream. It records:

```text
- current full base zip;
- overlays applied;
- files actually inspected;
- claims proven vs planned;
- current invariant;
- next exit condition;
- packaging boundary;
- uncertainty and failed operations.
```

This is now represented by:

```text
ION/05_context/current/agent_context_systems/LEAD_DEV_CONTEXT_CONTROL_SURFACE.context_system.md
```

That file is deliberately marked `not_an_ion_worker_role: true`. It is a continuity discipline for the lead-dev carrier, not a new ordinary runtime role that violates the V98 freeze.

---

## 9. Runtime separation

ION needs a cleaner productized shape.

The live runtime should distinguish:

```text
runtime_core       kernel modules, CLI, registries, templates needed to run
runtime_state      current packets, queues, gates, receipts, active context systems
execution_cycles   generated packages and returns from actual runs
ui_surface         cockpit shell and active view model
historical_archive donor branches, old zips, stale reports, old receipts
release_overlay    small patch/update zips
```

The existing folder names can stay, but packaging must respect the distinction. A compact sandbox runnable zip should include runtime core, required templates, current runtime state, tests, and current docs. It should not include every historical archive unless it is explicitly an archive edition.

---

## 10. The key practical repair sequence

The next implementation should not expand theory. It should build enforcement.

```text
V100 target: ion_autonomous_loop.py
```

The loop must:

```text
1. accept a goal;
2. classify/queue the goal;
3. build a context-window plan;
4. select one role;
5. compile one role package;
6. select one template/action contract;
7. run a local deterministic worker;
8. reject returns missing CONTEXT PROOF;
9. reject returns missing TEMPLATE ACTION PROOF;
10. intake valid return;
11. run Steward integration;
12. write receipt;
13. update cockpit view state;
14. stop with an explicit reason.
```

Only after this passes should Cursor/MCP/API workers re-enter as external carriers.

---

## 11. What this pass proves and does not prove

Proves:

```text
- the context architecture has been specified as package + timeline + route map;
- the lead-dev carrier continuity surface has been defined;
- runtime/core/state/archive separation has been made explicit;
- the next implementation target is still the V98 autonomous loop, not more doctrine.
```

Does not prove:

```text
- autonomous loop execution;
- template action gate enforcement in code;
- Steward integration command;
- cockpit survival-loop rendering;
- full consolidated zip integrity;
- production readiness.
```

---

## 12. Final judgment

The user's proposed direction is not extra complexity. It is the missing abstraction that makes ION sane.

The AI does need a main context package. It does need a route map. It does need token/cost/depth awareness. It does need a timeline of prior packages. It does need a template system that projects completed events into indexes, blockers, receipts, and context deltas. And the lead-dev carrier does need its own continuity discipline so it stops becoming another amnesic host trying to reason from fragments.

But the order matters:

```text
1. Lock the context model.
2. Build the local autonomous loop.
3. Enforce template action proof.
4. Integrate accepted returns through Steward.
5. Expose all of it in the cockpit.
6. Then reconnect Cursor/MCP/API carriers.
```

That is the path that turns ION from a profound architecture into a runnable machine.
