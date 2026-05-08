# Carrier Upgrade Request

Use this template when a carrier requests elevation from its current proven level.
A carrier may not self-approve this request.

## Request

- Request ID:
- Session ID:
- Carrier ID:
- Host:
- Current level: L0 / L1 / L2 / L3 / L4
- Requested level: L0 / L1 / L2 / L3 / L4

## Reason for upgrade

- Objective requiring upgrade:
- Why the current level is insufficient:

## Proven host capabilities

List evidence paths only. Do not cite chat memory as proof.

| Capability | Evidence path | Notes |
|------------|---------------|-------|
| File read | | |
| File write | | |
| Shell | | |
| Python / pytest | | |
| ion_carrier_onboard | | |
| ion_cycle_runner | | |
| Host-native subagents | | |
| MCP/API | | |

## Requested new abilities

- [ ] File edits
- [ ] Python execution
- [ ] Shell execution
- [ ] Host-native subagent spawn
- [ ] ION-native orchestrated spawn
- [ ] MCP/API calls
- [ ] Export/package generation

## Risks

- Authority risk:
- Context drift risk:
- Host limitation risk:
- Rollback/fallback risk:

## Required constraints

- production_authority: false
- live_execution_authority: false
- allowed_paths:
- forbidden_paths:
- return_contract:

## Fallback if denied

Describe the L0/L1 manual-template path that continues lawfully if upgrade is rejected.

## Kernel/Scheduler decision

Decision must be recorded in `ION/05_context/signals/CARRIER_LEVEL_DECISION.json` or a dated `.signal.md` equivalent.

- Decision: Approved / Rejected / Modified / Deferred
- Approved level:
- Decision artifact path:
- Decision notes:
