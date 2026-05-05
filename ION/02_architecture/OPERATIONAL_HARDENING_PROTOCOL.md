---
type: protocol
authority: A3_OPERATIONAL
created: 2026-04-08T23:10:00-04:00
status: ACTIVE
owner: Steward working session
purpose: Define the truthful hardening contract for the supervised operational runtime surface
connections:
  - ION/02_architecture/SUPERVISED_AUTOMATION_POLICY_PROTOCOL.md
  - ION/02_architecture/SUPERVISED_DAEMON_SERVICE_PROTOCOL.md
  - ION/02_architecture/OPERATOR_CONTROL_PROTOCOL.md
  - ION/02_architecture/RECOVERY_AND_REPLAY_PROTOCOL.md
  - ION/02_architecture/EXTERNAL_EXECUTION_MCP_BRIDGE_PROTOCOL.md
  - ION/06_intelligence/specs/T45_OperationalHardeningLifecycle.spec.md
  - ION/06_intelligence/specs/T46_OperationalAcceptancePackaging.spec.md
---

# Operational Hardening Protocol

## Intent

Operational hardening packages the already-landed supervised runtime surface into a truthful operator mode.
It does not create unattended autonomy.
It makes startup, shutdown, runbooks, and acceptance status explicit and machine-readable.

## Governing law

1. Kernel truth remains primary.
2. Service-facing artifacts remain operational witness, not doctrine.
3. Operator control remains the direct authority for enabled / draining / stopped posture.
4. Startup may only activate the preferred supervised runtime mode through explicit policy and explicit operator intent.
5. Shutdown may only change runtime posture through explicit operator action.
6. Runbooks and acceptance checklists describe the current service floor; they do not grant action authority.

## Required hardening surfaces

### Lifecycle
- supervised runtime startup request
- supervised runtime shutdown request
- machine-readable lifecycle receipts
- machine-readable lifecycle ledger
- runtime state file naming the preferred active automation mode

### Status
- unified runtime status snapshot
- latest daemon-service evidence
- child-work / replay / external-bridge counts
- explicit operator control posture

### Runbooks
- bounded startup sequence
- bounded shutdown sequence
- explicit reference to daemon service, child-work, replay, and external bridge paths

### Acceptance
- checklist aligned to the operationalization master plan acceptance criteria
- evidence paths for each criterion
- truthful unsatisfied states when evidence is absent

## Non-goals

- no hidden deployment daemon
- no background restart loop
- no platform installer or packaging claim beyond the active repository surface
- no promotion of runbooks or checklists into runtime authority
