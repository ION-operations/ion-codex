---
type: settlement_note
authority: A3_OPERATIONAL
created: 2026-04-22T21:20:00-04:00
status: ACTIVE_CURRENT_PHASE
topic: Retire Codex as a live current-phase role and boot; preserve only as historical carrier witness
connections:
  - ION/02_architecture/STEWARD_CURRENT_PHASE_ORCHESTRATION_PROTOCOL.md
  - ION/02_architecture/ROLE_CHASSIS_MOUNT_PROTOCOL.md
  - ION/02_architecture/TRUE_NAME_AND_SEMANTIC_LAYER_PROTOCOL.md
  - ION/02_architecture/RANK_AND_PRECEDENCE_PROTOCOL.md
  - ION/03_registry/agent_roster_registry.yaml
  - ION/03_registry/semantic_identities/CODEX.semantic.yaml
---

# Codex Current-Phase Role And Boot Retirement Note

## Judgment

The active branch should no longer model `Codex` as a live current-phase role, agent, or boot.

Current-phase workflow must remain lawful across:

- IDE-native execution
- browser-carried execution
- API-carried execution
- any other mounted chassis permitted by carrier law

Those differences are real at the level of carrier, mount, and capability posture.
They are **not** grounds for a separate current-phase roster entity.

## Settled current-phase rule

1. `Steward` remains the current-phase orchestration truename.
2. Carrier differences belong to mount/chassis law rather than roster law.
3. `Codex` is preserved only as a historical carrier label for older artifacts and earlier branch posture.
4. `Codex` must not be counted as a live current-phase role, support role, or front-door component.

## Operational consequences

- `role.codex` is removed from the live current-phase roster.
- `ION/03_registry/boots/CODEX.boot.md` is retained only as a retired historical witness surface and must not be mounted as an active boot.
- `ION/03_registry/semantic_identities/CODEX.semantic.yaml` is historical-only and must not be read as current live role truth.
- Codex-named bindings and Codex-named orchestration protocol surfaces are compatibility/history witnesses only unless explicitly reactivated by a later packet.
- The default front door is now `Steward + Relay`, with escalation and specialist activation under existing packet, audit, and support-role law.

## Reason

The branch should not imply that workflow truth changes merely because the current carrier happens to be:

- an IDE extension,
- a browser chat surface,
- an API worker,
- or another mounted runtime.

That distinction belongs to carrier and capability law, not to the existence of a separate named agent.

## Non-claim

This note does **not** claim that carrier differences are unreal.
It claims only that they should be handled through:

- role/chassis mount law,
- executor capability law,
- and bounded packet routing,

rather than through a distinct `Codex` current-phase roster entity.
