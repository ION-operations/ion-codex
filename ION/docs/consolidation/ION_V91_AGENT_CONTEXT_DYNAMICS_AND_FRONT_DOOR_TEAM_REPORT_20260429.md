# ION V91 — Agent Context Dynamics and Front-Door Team Report

## Summary

V91 adds the missing planning layer between static Agent Context System cards and generated Cursor Task packages.

V81/V82 made agents into governed context systems and forced context-system surfaces before MINI/CAPSULE. V91 adds dynamic context-window planning: attention leases, role-specific context budgets, route-deeper surfaces, front-door team posture, and explicit no-user-upkeep law.

## New runtime outputs

```text
ION/05_context/current/ACTIVE_AGENT_CONTEXT_WINDOW_PLAN.json
ION/05_context/current/ACTIVE_FRONT_DOOR_TEAM_PLAN.json
```

## New kernel module

```text
ION/04_packages/kernel/ion_agent_context_dynamics.py
```

## New protocols

```text
ION/02_architecture/ION_AGENT_CONTEXT_DYNAMICS_AND_CONTEXT_WINDOW_PROTOCOL.md
ION/02_architecture/ION_FRONT_DOOR_AUTONOMOUS_TEAM_WORKFLOW_PROTOCOL.md
```

## What is now explicit

- The current implementation is real but not final: static context cards + V82 packaging + V91 planning, not yet full graph-reranked evolving memory.
- Persona/Relay/Steward are the logical front-door team, but the Cursor parent chat remains carrier-control.
- The user should not manage routine ION upkeep, agent selection, packet refresh, or sequence.
- Human gates are the normal reason to ask the user for action.
- Roles receive attention leases and budgets rather than always carrying deep context.

## Validation commands

```bash
PYTHONPATH=ION/04_packages python3 -m kernel.ion_agent_context_dynamics --ion-root . --operator-message "continue" --write --json
PYTHONPATH=ION/04_packages python3 -m pytest -q ION/tests/test_kernel_ion_agent_context_dynamics.py
```
