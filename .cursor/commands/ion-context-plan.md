# /ion-context-plan

Build the current dynamic ION agent context-window plan.

Run from the shell root:

```bash
PYTHONPATH=ION/04_packages python3 -m kernel.ion_agent_context_dynamics --ion-root . --operator-message "${input:operatorMessage}" --write --json
```

Then open:

```text
ION/05_context/current/ACTIVE_AGENT_CONTEXT_WINDOW_PLAN.json
ION/05_context/current/ACTIVE_FRONT_DOOR_TEAM_PLAN.json
```

Do not ask the operator which routine agents to spawn. Use the emitted plan and the active carrier turn packet.
