---
type: operational_runbook
authority: A3_OPERATIONAL
generated_at: 2026-04-12T15:08:04-04:00
status: ACTIVE
preferred_active_mode: true
service_mode: ENABLED
---

# Supervised Runtime Runbook

## Current status

- Preferred active automation mode: enabled
- Operator service mode: ENABLED
- Latest daemon service status: EXECUTED
- Latest daemon service receipt: ION/05_context/history/daemon_service_receipts/daemon-service-2026-04-10t18-07-40-00-00.daemon_service_receipt.json
- Child-work service events: 0
- Recovery/replay events: 0
- External execution bridge events: 0

## Startup sequence

1. Ensure operator control state is lawful and no scope hold blocks the intended run.
2. Start supervised runtime through `KernelOperationalHardeningManager.start_supervised_runtime(...)`.
3. Run bounded daemon service cycles through `KernelDaemonService.run(...)` with explicit policy and operator context.
4. Use child-work issuance, recovery/replay, and external execution bridge only through their supervised service paths.

## Shutdown sequence

1. Request draining shutdown when in-flight work should finish without admitting new service action.
2. Request stopped shutdown for an immediate operator-controlled stop.
3. Confirm the resulting operator service mode in the operator control state and supervised runtime lifecycle receipt.

## Acceptance overview

- [x] A1: Operator control state is machine-readable (service_mode=ENABLED).
- [x] A2: Daemon service has executed or been invoked through the supervised service path.
- [x] A3: Automation actions can be refused lawfully through the policy floor.
- [x] A4: Child-work issuance has an approval-aware supervised service path.
- [x] A5: Recovery and replay are available before stronger autonomy claims.
- [x] A6: Witness/report surfaces remain subordinate to the operational kernel by plan and protocol.
