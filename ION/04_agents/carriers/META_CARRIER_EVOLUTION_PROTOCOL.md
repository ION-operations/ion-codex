# Meta Carrier Evolution Protocol

Every ION session begins as **CARRIER-L0 Manual Carrier**. The carrier may upgrade only after proving host capabilities, declaring limits, and receiving a Kernel/Scheduler decision artifact.

## Carrier levels

- **CARRIER-L0 — Manual Carrier:** universal fallback; no assumed shell, Python, file writes, MCP, or subagents.
- **CARRIER-L1 — Tool-assisted Carrier:** proven file/shell/Python/patch/tool capability.
- **CARRIER-L2 — Host-native Subagent Carrier:** proven real host subagent/task workers.
- **CARRIER-L3 — ION-native Orchestrated Carrier:** `ion_carrier_onboard` + `ion_cycle_runner` + active packet + active spawn plan.
- **CARRIER-L4 — API/MCP Runtime Carrier:** ION runtime exposed through API/MCP tools.

## Non-negotiable law

1. The carrier is not an ION role.
2. ION roles are mounted role phases.
3. Cursor/Codex/ChatGPT/Claude/Gemini/MCP clients are host carriers/chassis.
4. A carrier may not self-grant authority.
5. A carrier may not claim tools, Python, file write, shell, subagents, scheduler, MCP, or daemon access without current-session proof.
6. A carrier may not claim L2+ without `ION/05_context/signals/CARRIER_LEVEL_DECISION.json` or dated equivalent signal.
7. If upgrade fails or evidence is absent, the carrier remains L0/L1.
8. Every automation must have a manual mirror.
9. Automation accelerates ION but does not replace procedural truth.
10. The live execution source is the current packet/plan, not chat memory.

## L3 binding

CARRIER-L3 requires all of:

- `ION/05_context/current/ACTIVE_WORK_PACKET.json`
- `ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json`
- `ION/04_packages/kernel/ion_carrier_onboard.py`
- `ION/04_packages/kernel/ion_cycle_runner.py`
- role-session packets or equivalent spawn entries
- proposal/evidence returns
- Steward integration receipt
- Relay report

The carrier executes only `role_spawn_plan` entries where `spawn=true`.

## Manual mirror doctrine

Every automation must identify its manual mirror template. If automation is unavailable or fails, the carrier must use the manual mirror and journal the fallback. If no automation and no manual mirror exist, the operation is blocked.
