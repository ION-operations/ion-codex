---
type: research
authority: A3_OPERATIONAL
created: 2026-04-08T18:40:00-04:00
status: ACTIVE
owner: Codex working session
purpose: Master plan for supervised automation operationalization after the post-I6 audit and rebase
connections:
  - ION/PLAN.md
  - ION/06_intelligence/audits/2026-04-08_ion_operational_rebase_audit.md
  - ION/05_context/comms/migration_ledgers/automation_operationalization_ledger.md
---

# ION Operationalization Master Plan

## Endgame

The next endgame is not another witness tier.
It is a supervised operational field.

ION should become a kernel that can lawfully and repeatably:
- accept incoming pressure,
- run bounded daemon cycles under operator supervision,
- maintain route and automation state,
- issue child work when lawful,
- apply governed writes when lawful,
- escalate review when required,
- recover from interruption,
- surface all of the above through subordinate witness artifacts.

## Phase discipline

### Freeze rule

The runtime-report witness chain from D1 through I6 is now considered sufficiently deep for the current phase.
New work in that family should be limited to:
- bug fixes,
- direct support for operational packets,
- compatibility work required by daemon service or recovery.

## Operational phases

### J0 — Operational rebase framing

Deliverables:
- strategic audit
- new operationalization ledger
- addendum in `PLAN.md`
- explicit freeze on further witness-chain expansion as a default

Exit condition:
- the repo has one active operational ledger and one active operationalization plan

### J1 — Supervised automation floor

Deliverables:
- supervised automation policy protocol
- supervised daemon service protocol
- operator control protocol
- T38–T40 specs
- initial kernel implementations for:
  - automation policy evaluation
  - operator hold / resume / stop state
  - supervised daemon service runner
- tests and service receipts

Exit condition:
- daemon service can run lawfully under explicit policy and explicit operator control

### J2 — Child-work operationalization

Deliverables:
- child-work operationalization protocol
- planner-child issuance policy binding
- daemon-service integration for lawful child issuance
- explicit review / approval gates for child work
- receipts for issued child work under supervised service mode

Exit condition:
- child issuance is a first-class supervised automation path, not just an internal helper

**Status:** COMPLETE (2026-04-08)

Landing notes:
- `kernel/child_work_service.py` now binds planner-gated issuance to automation policy and operator control.
- `kernel/daemon_service.py` now exposes supervised child-work issuance as a delegated service action.
- runtime dispatch posture, review pressure, and spawn-policy approval are now part of issuance law.

### J3 — Recovery and replay

Deliverables:
- recovery / replay protocol
- daemon service run receipts
- resumable / non-resumable classification
- replay helper for interrupted runs
- stale state detection and controlled resumption

Exit condition:
- the operator can recover a bounded interrupted service run lawfully and transparently

**Status:** COMPLETE (2026-04-08)

Landing notes:
- `kernel/daemon_service.py` now writes machine-readable recovery classifications into daemon-service receipts and ledger rows.
- `kernel/recovery_replay.py` now exposes explicit replay selection, stale detection, lawful replay delegation, and replay receipts.
- replay re-enters the live daemon-service policy/control path rather than bypassing it.

### J4 — External execution / MCP bridge

Deliverables:
- service-facing execution contract
- MCP-facing automation surfaces
- external execution boundaries
- approval and refusal conditions for external action classes

Exit condition:
- the kernel can expose supervised operational automation to external execution surfaces without collapsing authority boundaries

**Status:** COMPLETE (2026-04-08)

Landing notes:
- `kernel/external_execution_bridge.py` now exports lawful external execution packets through the existing dispatch path and accepts bounded external execution returns through the existing execution path.
- `kernel/automation_policy.py` now recognizes external boundary action classes for export and return acceptance.
- `kernel/daemon_service.py` now exposes the bridge as a supervised service delegation rather than a side channel.

### J5 — Operational hardening

Deliverables:
- service startup / shutdown contract
- bounded runbooks
- operational acceptance checklist
- packaging of the supervised runtime surface as the preferred active automation mode

Exit condition:
- the repo has a truthful supervised operational mode that can be described without overclaiming autonomy

**Status:** COMPLETE (2026-04-08)

Landing notes:
- `kernel/operational_hardening.py` now packages supervised runtime startup, shutdown, lifecycle receipts, status snapshots, runbooks, and acceptance checklists.
- the supervised runtime surface now persists a preferred active automation mode under `ION/05_context/history/supervised_runtime/`.
- operational runbooks and acceptance packets now render under `ION/05_context/runtime_reports/operations/` without claiming deployment autonomy.

## Automation families that should become live

### A. Daemon service
- start
- run bounded steps
- stop / drain / refuse
- persist service receipts

### B. Pressure intake
- signal consumption
- review pressure recognition
- runtime-state aware dispatch posture

### C. Work issuance
- planner manifest maintenance
- child-work issuance
- review-gated branching

### D. Write application
- threshold evaluation
- governed-write permissioning
- post-write runtime-state sync

### E. Recovery
- interrupted run detection
- replay eligibility
- bounded resumption

### F. External bridge
- MCP / external execution
- explicit permission classes
- refusal boundaries

## Acceptance criteria for the operational phase

1. The operator can say whether automation is enabled, held, draining, or stopped and the kernel can prove it.
2. A daemon run can be started only through explicit policy and explicit control state.
3. The kernel can refuse action lawfully instead of silently doing nothing.
4. Child issuance has an approval policy.
5. Recovery and replay are available before stronger autonomy claims are made.
6. Witness surfaces remain subordinate to the operational kernel.

### K1 — Operational packaging and CLI surface

Deliverables:
- command-line entrypoints for supervised runtime lifecycle and status rendering
- bounded operator-facing invocation examples
- packaging notes for local IDE/runtime use

Exit condition:
- an operator can discover and invoke the preferred supervised runtime mode from the repo surface without needing internal module knowledge
