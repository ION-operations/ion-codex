# Persona front-door correction judgment

## Result

- A4 correction required: **yes**
- correction applied to protocol: **yes**
- Persona made command authority: **no**
- internal workflow visibility preserved: **yes**
- A5 target changed: **yes**

## Core judgment

The initial A4 landing correctly separated role, carrier, persona, Relay,
Steward, and parallel provenance. It under-specified the direct user-discourse
boundary.

The corrected ION model is:

**Persona is the normal front door. Relay is the courier. Steward is the
orchestrator. Internal roles are workflow/audit surfaces unless explicitly
surfaced.**

## Why this matters

ION's control and auditability come from agents loading bounded context and
style of work instead of inventing their own workflow iteratively.

If every internal role casually converses with the user, the system loses the
front-door discipline that makes the route inspectable:

- user intent enters through a stable persona surface,
- Relay preserves and packages the signal,
- Steward sequences the system,
- roles operate under law,
- and the response returns through the same front-door discipline.

## Next lawful packet

A5 remains the next move, but its target is now sharper:

**Persona-fronted Single-Carrier Live-Use Proof / Persona Recovery Gate**

Minimum target:

- operate through Persona or the persona-fronted Relay fallback,
- keep internal roles visible as workflow, not default speakers,
- preserve Persona/Relay/Steward separation,
- decide whether current-root Persona / `PERSONA_VOICE` recovery is needed,
- avoid final persona canon unless live evidence requires it.
