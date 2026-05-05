# ION Ultimate AI Chat Demo Spine Plan

## Goal

Build the most impressive narrow demo of ION as an AI chat assistant powered by an evented living context graph.

## Product experience

The user experiences one excellent assistant. Internally, the assistant is role-separated:

```text
Persona Interface -> Relay -> Steward -> evented graph operation -> Relay -> Persona Interface
```

## Demo promise

Show that ION is not just chatting. It turns user intent into graph-native work, acts through templates, validates completion, triggers lawful automation, emits receipts, and returns a high-quality user-facing response.

## First demo path

```text
User asks: "Refresh the project summary and tell me what changed."

Persona Interface:
  captures user-facing intent and relationship context.

Relay:
  emits semantic-boundary packet:
    operation: summary_refresh
    graph_region: project_summary
    authority: projection_update_candidate
    requested_receipts: validation, reaction, summary_update

Steward:
  routes to summary-refresh template/work unit.

Evented file graph:
  instantiates or updates a summary-refresh template file.
  validates completion.
  extracts affected graph nodes/edges.
  routes summary/index reaction.
  emits receipts.

Return:
  Relay packages system-native result.
  Persona Interface responds with a polished summary, receipt digest, and next options.
```

## Why this is impressive

It demonstrates:

- persistent front-door persona separation;
- true semantic boundary instead of raw prompt routing;
- graph-region orchestration;
- template-instantiated file mechanics;
- automation triggered by valid completion;
- receipts and audit trail;
- user-facing explanation of what changed.

## Non-goals for first demo

- full multi-agent API swarm;
- full browser polish before proof;
- unrestricted daemon autonomy;
- all graph region types;
- external paid API calls.

## Next build step

Create a local CLI/API demo command that runs the entire path over a tiny sample project graph. Then wrap that command in a browser UI.
