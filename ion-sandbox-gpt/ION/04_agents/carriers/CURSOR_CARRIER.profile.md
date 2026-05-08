# Cursor Carrier Profile

carrier_id: CURSOR_CARRIER
host_family: cursor
default_level: L0
candidate_levels: [L1, L2, L3]
default_return_agent: CURRENT_CARRIER

## Host-specific principle

Cursor is a carrier, not ION itself. Cursor may have file editing, shell, test, and host-native subagent abilities, but none of those are assumed by ION until proven in a Carrier Capability Survey and approved by a Carrier Level Decision artifact.

## Common possible capabilities

- Repo read access.
- Repo write access.
- Shell command execution.
- Python/test execution.
- Host-native Task/subagent support.
- Patch creation.
- Validation command execution.

## Upgrade constraints

L1 may be requested when Cursor proves file/tool/test ability.

L2 may be requested when Cursor proves real host-native subagent support. A Cursor `Task` is not lawful ION subagent execution until the Carrier records:
- Agent Spawn Request.
- Host-native spawn proof or transcript.
- Agent Result Packet.
- Return to CURRENT_CARRIER or scheduler-declared target.

L3 may be requested only when current repo evidence proves `ion_cycle_runner` plus `ACTIVE_ROLE_SPAWN_PLAN.json` or current equivalent deterministic spawn law.

## Forbidden

- Do not assume Cursor Composer/Agent equals ION Scheduler.
- Do not treat free-form Cursor subagent use as lawful spawn.
- Do not skip packet/spawn/journal artifacts.
- Do not self-approve carrier upgrade.
