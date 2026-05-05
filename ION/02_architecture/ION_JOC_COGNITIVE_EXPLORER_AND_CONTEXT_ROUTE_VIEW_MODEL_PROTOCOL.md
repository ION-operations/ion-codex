# ION/JOC Cognitive Explorer and Context Route View Model Protocol

## Status

```yaml
version: V58_COGNITIVE_EXPLORER_AND_CONTEXT_ROUTE_VIEW_MODEL
authority_scope: COGNITIVE_EXPLORER_ROUTE_VIEW_MODEL_RECEIPT_ONLY
production_authority: false
live_ui_claim: false
```

## Doctrine

The Cognitive Explorer is the UI organ that turns context routing from hidden retrieval into visible operating state. It is not a semantic-RAG result list. It is a route proof surface: it shows exact symbols, file paths, dependency edges, receipt families, fallback boundaries, and line-citation rails before any context is injected into an AI mission.

## Required surfaces

```text
COGNITIVE_EXPLORER
INFINITE_CONTEXT_COMMAND_PALETTE
SELECTED_CONTEXT_LENS
STRUCTURAL_BLUEPRINT_VIEW
DEPENDENCY_WEB_VIEW
SOURCE_LINE_CITATION_RAIL
ROUTE_REASONING_PANEL
```

## Required route classes

```text
EXACT_SYMBOL
FILE_PATH
DEPENDENCY_EDGE
RECEIPT_FAMILY
FALLBACK_BOUNDARY
```

## Valid route loop

```text
operator query
→ exact index / route resolver preview
→ selected node set
→ dependency edge set
→ source citation set
→ route reasoning
→ injection preview
→ optional dispatch proposal
```

The final step is proposal-only in V58. Dispatch remains outside V58 authority.

## Failure modes blocked

```text
hidden semantic retrieval presented as proof
selected context without source citations
dependency graph visualization without edge evidence
command palette that dispatches without showing route
context injection that silently grants browser/session authority
source-summary rewrite smuggled through context preview
canonical graph write smuggled through explorer selection
```

## UI law

The operator should never have to ask, “what did the AI actually read?” The cockpit must show selected nodes, citations, and route reasoning before model dispatch.
