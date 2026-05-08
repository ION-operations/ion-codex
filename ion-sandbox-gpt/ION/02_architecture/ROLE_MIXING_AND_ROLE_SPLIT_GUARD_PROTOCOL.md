---
type: protocol
authority: A3_OPERATIONAL
status: ACTIVE_CURRENT_PHASE
created: 2026-04-24
canon_status: PROVISIONAL_ROLE_GOVERNANCE
connections:
  - ION/03_registry/agent_roster_registry.yaml
  - ION/02_architecture/FRONT_DOOR_PERSONA_RELAY_STEWARD_BOUNDARY_PROTOCOL.md
  - ION/02_architecture/ROLE_CHASSIS_MOUNT_PROTOCOL.md
  - ION/02_architecture/TEMPLATE_BINDING_PROTOCOL.md
  - ION/02_architecture/TRUE_NAME_AND_SEMANTIC_LAYER_PROTOCOL.md
---

# Role Mixing and Role Split Guard Protocol

## 0. Purpose

This protocol prevents ION roles from absorbing incompatible burdens merely
because one carrier, chat, or file lane happened to carry them historically.

ION must preserve separate planes for:

- role;
- carrier/chassis;
- domain;
- template;
- continuity home;
- authority class;
- user-facing persona surface.

## 1. Anti-role-mixing rule

A role may not carry both a user-bonded relational persona burden and a
system-routing/courier/orchestration burden once those burdens create distinct
continuity, privacy, authority, or output-shape requirements.

When such conflict appears, the correct operation is `ROLE_SPLIT`, not informal
role blending.

## 2. Role split trigger

A role split should be considered when a burden is:

- persistent;
- distinct from the existing role domain;
- repeatedly invoked;
- continuity-bearing;
- chassis-independent;
- semantically drift-risky if kept implicit;
- governed by different template or authority rules.

## 3. Role split output requirements

A lawful `ROLE_SPLIT` should produce:

1. a settlement note;
2. registry update;
3. boot record for the new or narrowed role;
4. continuity-home declaration;
5. template binding update;
6. forbidden-collapse list;
7. migration note for any inherited files;
8. semantic review path for any new true name.

## 4. Template ownership headers

Front-door templates should declare:

- role owner;
- allowed continuity sources;
- allowed output class;
- forbidden authority actions;
- handoff target;
- whether the surface is user-facing, relay-facing, or orchestration-facing;
- whether Aletheion-style translation is expected.

## 5. Continuity separation rule

At minimum:

- Persona Interface owns user-bonded relationship continuity.
- Relay owns relay/courier/semantic-boundary continuity.
- Steward owns orchestration continuity.
- Codex owns no independent orchestration true-name status; Codex remains a
  carrier/chassis alias unless later settlement says otherwise.

Only bounded packets, controlled re-expressions, and governed handoffs should
cross these lanes.

## 6. Forbidden role inflation

Do not mint new roles merely to solve:

- a template problem;
- a writing-style preference;
- a temporary staffing mood;
- a carrier limitation;
- a one-off domain request.

Use template binding, mount posture, or support-role activation first unless the
role-split trigger test is met.

## 7. Review gate

Any proposed new front-door or leadership role must pass:

- registry check;
- donor-line comparison;
- contradiction check;
- continuity-home review;
- template-binding review;
- authority and forbidden-collapse review;
- controlled re-expression validation.
