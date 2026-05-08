# V58 Cognitive Explorer and Context Route View Model Lock

```yaml
version: V58_COGNITIVE_EXPLORER_AND_CONTEXT_ROUTE_VIEW_MODEL
receipt_class: ui_runtime_view_model_lock
production_authority: false
live_ui_claim: false
external_model_dispatch: false
browser_session_mutation: false
canonical_graph_write: false
source_summary_rewrite: false
purpose:
  - bind the JOC V3 Cognitive Explorer idea into ION as a non-production view-model surface
  - expose deterministic context-route evidence before any model dispatch
  - make selected graph nodes, dependency edges, line citations, and route reasoning inspectable
  - preserve the distinction between context preview and execution
```

V58 extends the V57 Reactive OS Stream branch by adding the first Cognitive Explorer / Infinite Context command-palette route model. It does not implement live search, live browser control, or live dispatch. It defines the receipt shape and UI projection contract that a future live backend must satisfy.

## Required UI promise

The operator must be able to see what the system selected before a model receives context.

```text
query
→ exact indexed symbol/file/receipt route
→ selected graph nodes
→ structural blueprint
→ dependency web
→ source-line citation rail
→ context injection preview
→ no dispatch unless separately authorized
```

## Authority boundary

V58 may render context-routing evidence. It may not:

```text
call external models
mutate browser sessions
read credentials
rewrite source summaries
write canonical graph state
activate unrestricted agents
claim production UI readiness
```
