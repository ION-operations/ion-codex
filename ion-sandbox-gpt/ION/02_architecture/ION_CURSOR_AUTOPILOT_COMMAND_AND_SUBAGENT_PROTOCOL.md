# ION Cursor Autopilot Command and Subagent Protocol

## Purpose

This protocol makes `/ion` the single Cursor-side reset-and-run command for ION. It aligns Cursor rules, skills, commands, subagents, MCP, and the future cockpit extension around one host-control posture.

## Core law

`/ion` means: mount the parent Cursor chat as `CURSOR_CARRIER_CONTROL_SURFACE`, refresh ION runtime packets, execute generated spawn rows only, proof-gate worker returns, and continue until a human gate, workflow failure, rejected return, or no open work.

The parent Cursor chat is not STEWARD, RELAY, PERSONA_INTERFACE, or any specialist role.

## Surface map

| Cursor surface | ION use |
|---|---|
| `.cursor/commands/ion.md` | hard reset-and-run carrier command |
| `.cursor/rules/ion-autopilot-command.mdc` | always-on identity and sequence guard |
| `.cursor/skills/ion-autopilot/SKILL.md` | dynamically loaded workflow memory |
| `.cursor/agents/ion-*.md` | subagent carrier-slot definitions |
| `.cursor/mcp.json` | bounded local ION MCP tool server |
| Cursor extension | eventual primary user-facing ION cockpit/persona UI |

## `/ion` semantics

- `/ion` with no argument is `continue`.
- `/ion <message>` records `<message>` as the operator directive and then runs the carrier workflow.
- Plain `continue`, `proceed`, or `resume` should be treated as `/ion` for ION projects.

## No-user-upkeep law

The user must not be asked to choose routine agents, refresh packets, organize context, update manifests, run routine audits, or sequence ION work. The system asks the user only for human gates, preferences, external permissions, or scope decisions.

## Subagent law

Cursor subagents are carrier slots, not autonomous ION authorities. They must be invoked only from generated spawn rows and must receive generated context packages. Their first output section must be `### CONTEXT PROOF`.

## Extension direction

The long-term operator experience should be:

1. the user speaks to Persona/ION in the extension;
2. the extension queues the operator message;
3. `/ion` or the extension command triggers carrier automation;
4. the cockpit shows live packets, agent comms, gates, receipts, and timeline;
5. the parent Cursor chat becomes mostly a host automation lane.
