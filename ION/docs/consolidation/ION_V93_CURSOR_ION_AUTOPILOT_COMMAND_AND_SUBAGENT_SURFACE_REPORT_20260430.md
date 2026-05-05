# ION V93 Cursor /ion Autopilot Command and Subagent Surface Report

## Summary

V93 makes `/ion` the canonical Cursor-side carrier-control reset-and-run command. `/ion` with no argument means `continue`; `/ion <message>` means classify/queue the message and run the ION workflow.

The parent Cursor chat remains `CURSOR_CARRIER_CONTROL_SURFACE`, not STEWARD/RELAY/PERSONA. Cursor subagents are added as project-scoped carrier-slot definitions that must run only from generated ION context packages and must return `### CONTEXT PROOF`.

## Added surfaces

- `.cursor/commands/ion.md`
- `.cursor/rules/ion-autopilot-command.mdc`
- `.cursor/skills/ion-autopilot/SKILL.md`
- `.cursor/agents/ion-*.md`
- `ION/04_packages/kernel/ion_cursor_autopilot_packet.py`
- `ION/04_packages/kernel/ion_cursor_autopilot_audit.py`
- `ION/02_architecture/ION_CURSOR_AUTOPILOT_COMMAND_AND_SUBAGENT_PROTOCOL.md`
- `ION/tests/test_kernel_ion_cursor_autopilot.py`

## Runtime effect

Cursor now has one explicit command that should re-establish the workflow even when Auto mode drifts. The command tells Cursor to build an autopilot packet, run carrier continuation, read active packets, use MCP where available, launch only generated subagent rows, run return intake, and stop only at a gate/failure/completion.

## Future extension link

The desired final operator UX is not endless typing in parent chat. The operator should converse with ION/Persona in the Cursor cockpit extension, while `/ion` or an extension command drives the parent carrier-control automation lane.
