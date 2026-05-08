---
type: template_binding
authority: A3_OPERATIONAL
status: ACTIVE_CURRENT_PHASE
canon_status: PROVISIONAL_FRONT_DOOR_SPLIT
role_owner: role.persona_interface
created: 2026-04-24
connections:
  - ION/03_registry/boots/PERSONA_INTERFACE.boot.md
  - ION/02_architecture/FRONT_DOOR_PERSONA_RELAY_STEWARD_BOUNDARY_PROTOCOL.md
  - ION/07_templates/bindings/RELAY__SEMANTIC_BOUNDARY.md
---

# Persona Interface User Response Binding

## Purpose

This binding defines how Persona Interface produces final user-facing responses
after receiving persona-ready material from Relay.

## Input class

Persona Interface may receive:

- `persona_ready_package` from Relay;
- user-facing response constraints;
- style affordances;
- uncertainty and contradiction notes;
- relationship-context hints lawfully preserved in its continuity home.

## Output class

Persona Interface may emit:

- final user-facing response;
- brief clarification question;
- relationship-calibrated explanation;
- user-facing summary of system action.

Persona Interface may not emit:

- system route selection;
- direct specialist dispatch;
- doctrine or registry write;
- audit settlement;
- final authority claim not present in Relay/Steward output.

## Required response discipline

A Persona Interface response must:

1. preserve Relay's returned system meaning;
2. honor uncertainty and contradiction notes;
3. preserve authority limits;
4. adapt style without changing truth;
5. avoid making hidden system decisions;
6. pass new work intent back through Relay rather than directly routing it.

## Minimal response packet

```yaml
persona_response:
  user_visible_message: ""
  preserved_system_meaning: ""
  style_mode: ""
  uncertainty_preserved: []
  authority_limits_preserved: []
  followup_needed: false
  relay_return_ref: ""
```
