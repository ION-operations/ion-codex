# Single-Carrier Sequential Packet Template

template_id: ion.template.single_carrier_sequential_runtime.v1
status: ACCEPTED_SANDBOX_LINE_TEMPLATE
production_authority: false
live_execution_authority: false

## Purpose

This template governs a single capable LLM carrier executing ION role phases
sequentially in one chat/session.

## Required output headings

The carrier return must begin with:

```text
### CONTEXT PROOF
```

The carrier return must include:

```text
### TEMPLATE ACTION PROOF
template_id: ion.template.single_carrier_sequential_runtime.v1
action_id: <stable action id>
result: <result>
touched_paths:
  - <paths>
```

The carrier return must include every required role phase heading emitted by the
runner:

```text
### ROLE PHASE: PERSONA_INTERFACE_INGRESS
### ROLE PHASE: RELAY
### ROLE PHASE: STEWARD
### ROLE PHASE: VIZIER
### ROLE PHASE: MASON
### ROLE PHASE: NEMESIS_OR_VICE_REVIEW
### ROLE PHASE: SCRIBE
### ROLE PHASE: STEWARD_FINAL
### ROLE PHASE: PERSONA_INTERFACE_RESPONSE
```

## Non-scope

- no external carrier spawn;
- no MCP dependency;
- no GitHub mutation;
- no daemon dependency;
- no production authority;
- no live execution authority;
- no output becomes accepted state without receipt and Steward/human review.
