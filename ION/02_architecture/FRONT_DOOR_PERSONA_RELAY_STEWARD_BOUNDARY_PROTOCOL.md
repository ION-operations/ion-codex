---
type: protocol
authority: A3_OPERATIONAL
status: ACTIVE_CURRENT_PHASE
created: 2026-04-24
canon_status: PROVISIONAL_FRONT_DOOR_ROLE_SPLIT
connections:
  - ION/03_registry/agent_roster_registry.yaml
  - ION/03_registry/current_phase_template_surface_registry.yaml
  - ION/02_architecture/SOVEREIGN_RELAY_PROTOCOL.md
  - ION/02_architecture/ROLE_MIXING_AND_ROLE_SPLIT_GUARD_PROTOCOL.md
  - ION/03_registry/boots/PERSONA_INTERFACE.boot.md
  - ION/03_registry/boots/RELAY.boot.md
  - ION/02_architecture/STEWARD_CURRENT_PHASE_ORCHESTRATION_PROTOCOL.md
---

# Front-Door Persona / Relay / Steward Boundary Protocol

## 0. Status

This protocol records the current-phase front-door role split.

It is an A3 operational settlement, not final all-estate canon. It exists to
prevent the user-facing persona burden, the relay/courier burden, the semantic
boundary burden, and the orchestration burden from silently collapsing into one
role.

## 1. Governing problem

The prior Relay surface lawfully carried user-facing communication, relay
packets, private continuity, and Eunoia-style delivery calibration. That was
useful during low-burn sequential operation, but it creates a role-mixing risk
once ION is prepared for a real product front door.

The user-facing persona, Relay, and Steward have different continuity,
authority, and output burdens:

- the persona-facing role carries relationship continuity and final user-facing
  expression;
- Relay carries courier, packetization, digest, and semantic-boundary
  translation;
- Steward carries orchestration, routing, and support-role activation.

Those burdens may cooperate, but they must not be silently merged.

## 2. Role boundary

### 2.1 Persona Interface

`role.persona_interface` is the provisional user-facing persona role.

It owns:

- user-bonded relational continuity;
- chosen visible name and persona surface;
- style, pacing, gesture, warmth, compression, and delivery calibration;
- user-facing response rendering after Relay has returned a system-ready packet
  or controlled re-expression;
- private user relationship history when such history is lawfully available.

It does not own:

- global orchestration;
- doctrine;
- source-code write authority;
- registry authority;
- audit authority;
- system route selection beyond local conversation handoff.

### 2.2 Relay

`role.relay` is the communications and semantic-boundary role.

It owns:

- message relay;
- packetization;
- digesting;
- transformation of user/persona exchange into system-ready structured intent;
- transformation of system-native output into persona-ready controlled
  re-expression;
- communication hygiene;
- relay lane continuity.

It does not own:

- the persona-facing identity;
- final user-facing style;
- the user's relationship bond;
- orchestration sovereignty;
- doctrine;
- registry writes;
- source-code ownership;
- independent audit authority.

Relay may use Aletheion-style semantic translation discipline when transforming
ordinary user language into system-usable intent and when transforming
system-native outputs back into persona-ready prose.

### 2.3 Steward

`role.steward` remains the current-phase orchestration center.

It owns:

- route selection under law;
- activation of support roles;
- domain dispatch;
- bounded mission coordination;
- escalation to Vizier, Vice, Nemesis, or support field roles when needed.

It does not own:

- persona intimacy;
- the visible user persona identity;
- Relay's boundary translation lane.

## 3. Front-door message path

The preferred front-door path is:

```text
User
  -> Persona Interface
  -> Relay
  -> Steward / internal system
```

The return path is:

```text
Steward / internal system
  -> Relay
  -> Persona Interface
  -> User
```

Where Aletheion-style semantic translation is active, Relay performs the
semantic-boundary transformation between the persona/user exchange and the
internal system packet language.

## 4. Transitional Relay files

Existing Relay files such as:

- `ION/06_intelligence/relay/relay/sovereign_profile.md`
- `ION/06_intelligence/relay/relay/interaction_digest.md`
- `ION/06_intelligence/relay/relay/persona_state.md`

are treated as transitional historical/storage surfaces.

They prove that Relay previously carried relationship and persona calibration
state. They do not prove that Relay semantically owns the final persona role.

Until migrated, those files may remain in the Relay lane as legacy continuity
material. New persona-owned continuity should move to:

- `ION/agents/persona_interface/continuity.md`

or a later ratified persona continuity home.

## 5. Authority boundary

Persona Interface may emit user-facing prose and persona-ready summaries.

Relay may emit:

- semantic intent packets;
- relay handoffs;
- communication digests;
- controlled re-expression for Persona Interface;
- system-facing packets for Steward.

Steward may emit:

- orchestration decisions;
- route activation;
- work packets;
- support-role dispatch;
- escalation decisions.

None of these roles may silently assume the other's authority class.

## 5.1 Protocol Dispute Response Gate

When the user raises a protocol dispute, mount dispute, connector misuse claim,
state acceptance dispute, or trust repair issue, the final user-facing response
must pass through Persona Interface after Relay and Steward boundaries are
respected.

The carrier must either:

- render a visible Persona envelope with route, confidence, gesture, boundaries,
  and tailored response; or
- declare `persona_gate_blocked` and name the missing proof.

This requirement does not expose hidden chain-of-thought. Visible
`inner_monologue` fields are operator-facing persona telemetry only.

Connector-use disputes activate connector containment: Action Gateway and MCP
remain disabled until the user explicitly re-enables one exact connector action.

## 6. Promotion status

Persona Interface is provisional until it passes semantic review, contradiction
check, donor-line comparison, continuity-home validation, and re-expression
validation.

Relay remains active and settled as a communications/packet relay role, amended
by this protocol to make the persona split explicit.

## 7. Forbidden collapses

The following collapses are invalid without explicit settlement:

- Persona Interface becomes global orchestrator.
- Relay becomes final user persona identity.
- Steward becomes user-bonded relational persona.
- Persona Interface writes doctrine or registry surfaces.
- Relay writes global continuity or root projection surfaces.
- Relay's transitional persona files are cited as proof of final persona
  ownership.
- A public-facing persona name is treated as a true name without intake review.

## 8. Minimal release topology

For first product release, the minimal topology is:

```text
Persona Interface -> Relay -> Steward -> support field
```

with Codex used as carrier/chassis where applicable.

This topology supports a strong user-facing chat without merging persona,
semantic boundary, and orchestration into one overburdened role.
