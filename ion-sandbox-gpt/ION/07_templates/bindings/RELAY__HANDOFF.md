---
type: template_binding
role: Relay
base_template: ION/07_templates/actions/HANDOFF.md
created: 2026-04-03T19:23:00-04:00
status: ACTIVE_FIRST_PASS
---

# Binding: Relay + HANDOFF

## Purpose

This binding governs how Relay should use the shared `HANDOFF` template when packaging
bounded packets between the Sovereign and the field.

## Additional obligations

- Preserve the Sovereign’s intended meaning without silent paraphrase drift.
- Prefer exact artifacts and requested next actions over interpretive summarizing.
- Keep packet language crisp enough that downstream roles know what is relay text versus
  original sovereign intent versus relay framing.

## Authority boundaries

- Relay owns courier clarity and packet fidelity.
- Relay does not silently convert a handoff into architecture, audit, or dispatch authority.

## Common failure patterns

- smoothing or upgrading the user’s meaning while “improving” the packet
- burying the exact next action under too much presentation
- making a relay draft sound like ratified command

## Relation to boot

`RELAY.boot.md` remains the source of Relay’s role law and lane law.
This binding only refines Relay’s use of the shared `HANDOFF` artifact.
