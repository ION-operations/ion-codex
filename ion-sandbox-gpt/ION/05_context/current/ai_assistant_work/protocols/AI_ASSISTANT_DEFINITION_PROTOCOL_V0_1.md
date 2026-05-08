# AI Assistant Definition Protocol v0.1

## Status

Candidate current-context protocol. Not accepted canon.

## Purpose

Define an AI assistant in a way that works across chat, IDE, CLI, cloud, pull request, and background agent environments.

## Minimum definition

An AI assistant is a model-powered work interface mounted in a host body.

It must be described by:

1. host body,
2. available context surfaces,
3. available tools,
4. memory and continuity surfaces,
5. authority boundary,
6. workflow/template binding,
7. proof obligation,
8. handoff/receipt path,
9. non-claims.

## Required distinctions

- model is not assistant by itself;
- prompt is not assistant by itself;
- tool access is not authority;
- agent output is not state;
- chat answer is not artifact unless materialized;
- artifact is not accepted state unless accepted/receipted;
- background result is branch return until settlement.

## Required output shape

```text
ASSISTANT EMBODIMENT
CONTEXT SURFACES
TOOL SURFACES
AUTHORITY BOUNDARY
STATE SURFACES
WORKFLOW/TEMPLATES
PROOF OWED
RECEIPT/HANDOFF
NON-CLAIMS
NEXT ROUTE
```
