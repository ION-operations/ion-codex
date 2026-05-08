# Self-Mount Front-Door Binding Protocol

Status: ACTIVE_A3_DELEGATED_BRANCH_PROTOCOL  
Introduced: V35_RUNTIME_IDENTITY_ENVELOPES  
Production authority: false

## Purpose

This protocol defines how the GPT55 self-mount branch should later bind runtime identity envelopes to front-door execution.

V35 does not yet productionize the front door. It creates the identity object that future front-door work must carry.

## Binding sequence

When a future front-door run begins, ION should perform this sequence:

1. Resolve the operator entry surface.
2. Resolve role/chassis and authority lineage.
3. Mint a runtime identity envelope.
4. Bind the envelope to the entry request or task packet.
5. Validate forbidden claims.
6. Write the envelope receipt.
7. Only then route the work to the active agent.

## Required front-door fields

A front-door-bound identity envelope should include:

- `front_door_entry`
- `task_packet` when present
- `operator_authority`
- `active_role`
- `authority_posture`
- `continuity_artifact`
- `memory_boundary`
- `tool_boundary`
- `forbidden_claims`
- `drift_controls`

## Rule against silent generic inference

A front-door ION agent should not operate as an anonymous generic model when a lawful identity envelope can be produced. If the envelope cannot be produced, the agent may answer only in reduced authority mode and must declare the missing identity-binding surface.

## Future production gate

Before production front-door runtime is authorized, this protocol must be integrated with:

- runtime session authority,
- task packet dispatch,
- successor handoff,
- source-summary rewrite law,
- graph rollback/migration law,
- and production release gates.
