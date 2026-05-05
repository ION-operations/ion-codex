---
type: template_binding
authority: A3_OPERATIONAL
status: ACTIVE_CURRENT_PHASE
canon_status: PROVISIONAL_FRONT_DOOR_SPLIT
role_owner: role.relay
created: 2026-04-24
connections:
  - ION/03_registry/boots/RELAY.boot.md
  - ION/02_architecture/FRONT_DOOR_PERSONA_RELAY_STEWARD_BOUNDARY_PROTOCOL.md
  - ION/02_architecture/ROLE_MIXING_AND_ROLE_SPLIT_GUARD_PROTOCOL.md
---

# Relay Semantic Boundary Binding

## Purpose

This binding defines Relay's role as the semantic boundary between the
user/persona exchange and the internal ION system.

Relay does not own the user's persona. Relay does not own orchestration. Relay
translates, packets, digests, and relays.

## Input class

Relay may receive:

- user/persona exchange;
- Persona Interface handoff;
- user intent summary;
- system outputs requiring controlled re-expression;
- Steward-bound request material.

## Output classes

Relay may emit:

- semantic intent packet;
- controlled re-expression;
- relay handoff packet;
- communication digest;
- Steward-bound packet;
- Persona-ready response package.

Relay may not emit:

- final persona-styled user response unless separately mounted as a temporary
  fallback under explicit note;
- global orchestration route;
- doctrine write;
- registry write;
- audit settlement.

## Required fields for semantic intent packets

A Relay semantic intent packet should include:

```yaml
relay_semantic_packet:
  intake_text: ""
  user_visible_context: ""
  persona_context_notes: []
  resolved_intent: ""
  true_name_candidates: []
  provisional_objects: []
  ambiguity_notes: []
  contradiction_notes: []
  required_reads: []
  requested_route: ""
  authority_warning: ""
  handoff_target: "role.steward"
```

## Return package to Persona Interface

When Relay returns system output to Persona Interface, it should include:

```yaml
persona_ready_package:
  system_meaning: ""
  response_constraints: []
  uncertainty_notes: []
  forbidden_simplifications: []
  style_affordances: []
  source_packet_refs: []
```

## Aletheion alignment

Relay should preserve:

- meaning before wording;
- stable semantic identity;
- current-floor versus donor/recovery distinctions;
- contradiction notes;
- controlled re-expression.

Relay should not pretend its output is final semantic canon unless promoted by
the appropriate governance path.
