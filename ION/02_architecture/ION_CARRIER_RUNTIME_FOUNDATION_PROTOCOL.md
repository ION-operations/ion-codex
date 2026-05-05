# ION Carrier Runtime Foundation Protocol

## Canonical cycle

```text
operator / daemon / MCP invokes ION
→ carrier starts at L0 and proves capabilities
→ ion_carrier_onboard emits ACTIVE_WORK_PACKET.json
→ ion_cycle_runner emits ACTIVE_ROLE_SPAWN_PLAN.json
→ carrier executes only spawn=true role entries
→ role returns are proposal/evidence
→ STEWARD integrates
→ RELAY reports
```

## Core distinction

- **Carrier:** external host/chassis that can run tools or hold context.
- **Carrier Agent:** boundary adapter that proves capabilities, calls onboarding/planning, executes approved spawn rows, and records evidence.
- **ION Role:** mounted role phase such as STEWARD, VIZIER, MASON, VICE, NEMESIS, RELAY, PERSONA, SCRIBE, AUDITOR, or VESTIGE.
- **Spawn plan:** machine-readable plan deciding what role entries execute in this cycle.

## Default rule

The carrier never decides which roles to run from chat memory. It reads `ACTIVE_ROLE_SPAWN_PLAN.json` and executes only `spawn=true` entries.

## Authority order

1. `ACTIVE_ROLE_SPAWN_PLAN.json`
2. `ACTIVE_WORK_PACKET.json`
3. Kernel trace / generated role packet
4. Current operator objective
5. Historical context, MINI/CAPSULE, and chat memory only as non-primary context

## Failure behavior

- No active work packet: run `ion_carrier_onboard` or stop.
- No active spawn plan: run `ion_cycle_runner` or remain at L0/L1 and do not claim L3.
- Capability unproven: do not claim it.
- Upgrade decision absent: remain L0/L1.
- Carrier drift: invalidate the run and rerun from onboarding.
