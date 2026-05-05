---
type: role_session
template: ROLE_SESSION
created: 2026-05-03T00:07:08-04:00
status: PLANNED
workstream: relay
role: relay
objective: V107 no silent deletion and trunk preservation gate: protected deletions block packaging, previous full zip comparison is required, canonical root full-project package emitted with preservation report
source_task: carrier_continue:v107 no silent deletion and trunk preservation gate: protected deletions block packaging, previous full zip comparison is required, canonical root full-project package emitted with preservation report
next_role: vizier
---

# Role Session: relay

## Role

relay

## Purpose

perform the courier pass

## Source Task / Objective

- objective: V107 no silent deletion and trunk preservation gate: protected deletions block packaging, previous full zip comparison is required, canonical root full-project package emitted with preservation report
- source_task: carrier_continue:v107 no silent deletion and trunk preservation gate: protected deletions block packaging, previous full zip comparison is required, canonical root full-project package emitted with preservation report

## Required Reads

- relay.boot: ION/03_registry/boots/RELAY.boot.md
- relay.continuity: ION/06_intelligence/relay/relay/continuity.md
- relay.profile: ION/06_intelligence/relay/relay/sovereign_profile.md
- relay.digest: ION/06_intelligence/relay/relay/interaction_digest.md
- relay.persona: ION/06_intelligence/relay/relay/persona_state.md
- relay.signals: ION/05_context/signals
- relay.projection.MINI.md: ION/MINI.md [optional]
- relay.projection.STATUS.md: ION/STATUS.md [optional]
- relay.projection.CAPSULE.md: ION/CAPSULE.md [optional]

## Expected Output

- Produce the relay pass for the bounded `relay` objective.
- Preserve provenance explicitly if any cross-role judgment is made.
- Update only the artifacts that the governing task or lane actually permits.

## Next Target

- next_role: vizier

## Notes

- This is a generated sequential-kernel session scaffold, not a claim that the role pass already happened.
