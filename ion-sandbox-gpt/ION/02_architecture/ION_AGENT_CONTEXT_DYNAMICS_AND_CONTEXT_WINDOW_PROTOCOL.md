---
protocol_id: ion.agent_context_dynamics_and_context_window.protocol.v1
status: ACTIVE_PLANNING_LAYER
rank: A2_CONTEXT_AUTHORITY
created: 2026-04-29
binds:
  - ION/02_architecture/ION_AGENT_CONTEXT_SYSTEMS_PROTOCOL.md
  - ION/02_architecture/HORIZON_ORCHESTRATION_PROTOCOL.md
  - ION/02_architecture/BRANCH_BUDGET_RECURSION_AND_DRIFT_CONTROL_PROTOCOL.md
  - ION/02_architecture/PERSONA_CONTEXT_BUDGET_AND_HORIZON_PROTOCOL.md
  - ION/02_architecture/FRONT_DOOR_PERSONA_RELAY_STEWARD_BOUNDARY_PROTOCOL.md
  - ION/04_packages/kernel/ion_agent_context_dynamics.py
---

# ION Agent Context Dynamics and Context Window Protocol

## 1. Purpose

V81/V82 made ION agents into governed context systems and forced generated Cursor Task packages to prepend Agent Context System authority before legacy MINI/CAPSULE witness material. V91 adds the missing dynamic layer: the runtime must plan which context windows should be alive for a turn, how deep each role should load, what route-deeper branches are available, what budget is implied, and which front-door roles participate before the user sees output.

This protocol exists because an ION agent must not simply be a static card plus a prompt. The intended agent is an evolving context organism with:

- durable semantic identity;
- role-specific domain law;
- active mission context;
- route-deeper maps;
- context deltas and receipts;
- horizon-aware attention leases;
- token/cost sensitivity;
- and proof-gated returns.

## 2. Current implementation level

As of V91, ION has:

- per-agent context-system cards;
- an Agent Context System registry;
- V82 runtime package ordering;
- parent-prefetched bounded context payloads;
- context-load receipts;
- proof-gated Task-return intake;
- Steward integration queue;
- operator queue and human gate queue;
- and a new dynamic context-window planner.

ION does not yet have the complete final vision. The remaining work includes:

- persisted per-agent context timelines;
- automatic graph traversal and semantic reranking;
- model-specific token accounting;
- SDK-driven autorun bound to the planner;
- context-delta writeback after every accepted step;
- and a cockpit graph showing context leases, package depth, and route-deeper events live.

## 3. Context window law

For every active turn, ION should produce an `ACTIVE_AGENT_CONTEXT_WINDOW_PLAN.json` describing:

1. operator-message classification;
2. active queue/gate pressure;
3. front-door team posture;
4. each role's attention lease;
5. each role's budget class and estimated tokens;
6. each role's required context layers;
7. route-deeper surfaces;
8. forbidden conflations;
9. drift controls;
10. and timeline events expected from the run.

The context window plan does not replace the generated context package. It governs how those packages should be composed and audited.

## 4. Attention leases

A role should not carry full deep context forever. Each role receives an attention lease:

- `active`: role should be considered in this turn and may be spawned or compiled into a package.
- `warm`: role remains front-door relevant or likely needed but should not receive deep context unless triggered.
- `dormant`: role remains registered but should not consume active context budget.

A role's attention lease is derived from operator intent, active queues, human gates, accepted returns, current objective, and route-deeper triggers.

## 5. Budget classes

The planner estimates context budgets using character limits and estimated tokens. V91 uses a conservative `chars/4` estimate because exact tokenization depends on carrier/model provider. Future model-router and SDK integration should replace this estimate with provider-native token counters.

Every role has minimum, normal, and deep context budgets. The runtime should load the smallest sufficient package and deepen only when evidence requires it.

## 6. Route-deeper law

A route-deeper surface is not always loaded. It is a lawful affordance for additional context. A role may route deeper when:

- the active package identifies a contradiction;
- required evidence is missing;
- a human gate refers to a deeper authority;
- a worker return references a surface not in the active package;
- or a domain-specific route trigger fires.

The route-deeper act should produce a context timeline event and, when material, a context delta receipt.

## 7. Front-door team law

The front-door team is not the Cursor parent chat. The Cursor parent chat is the host-side `CURSOR_CARRIER_CONTROL_SURFACE`.

The logical front-door team is:

1. **RELAY** — transforms user intent into system-ready packets and accepted system state into persona-ready packets.
2. **STEWARD** — routes work, manages gates, directs specialists, and integrates accepted returns.
3. **PERSONA_INTERFACE** — renders accepted Relay/Steward state into honest user-facing discourse.

These roles are logically resident but not necessarily spawned as full workers every turn. Their state should be compiled when needed. The user must not be asked to choose routine agents, refresh context, organize files, or maintain ION. The user is asked only for explicit human gates, preference/direction, credential/external permission, or scope authorization.

## 8. No-user-upkeep law

ION work and upkeep are system responsibilities. The operator may guide direction, set scope, authorize gates, and evaluate results. The operator should not be burdened with:

- selecting ordinary role sequence;
- refreshing packets;
- updating agent context files manually;
- deciding whether Steward/Relay/Persona should be spawned;
- or re-explaining the workflow when active packets already specify it.

If Cursor asks those questions during ordinary continuation, that is a carrier-control failure.

## 9. Drift controls

Every active context package and worker return remains subject to:

- Agent Context System surfaces before MINI/CAPSULE;
- context-load proof;
- Task-return intake;
- Steward integration queue only;
- human gate queue when blocking;
- workflow audit;
- and receipt-backed claims.

## 10. Success condition

V91 succeeds when ION can produce a durable active context-window plan and front-door team plan, making explicit which agent context systems are active, warm, or dormant; how deep they should load; what budget they imply; what routes are available; and how Persona/Relay/Steward should cooperate without asking the user to manage routine ION work.
