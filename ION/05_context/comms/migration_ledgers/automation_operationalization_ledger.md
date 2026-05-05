---
type: migration_ledger
authority: A3_OPERATIONAL
created: 2026-04-08T18:50:00-04:00
status: ACTIVE
owner: Codex working session
purpose: Packet ledger for supervised automation operationalization after the post-I6 rebase
connections:
  - ION/PLAN.md
  - ION/06_intelligence/audits/2026-04-08_ion_operational_rebase_audit.md
  - ION/06_intelligence/research/2026-04-08_ion_operationalization_master_plan.md
  - ION/04_packages/kernel/daemon.py
  - ION/04_packages/kernel/daemon_loop.py
  - ION/04_packages/kernel/planner_gate.py
  - ION/04_packages/kernel/governed_write.py
---

# Automation Operationalization Ledger

## Governing frame

This ledger begins after the I6 bridge-history family-summary packet.
The witness-chain stack remains present and valid, but it is no longer the primary expansion target.
The active target is supervised operational automation.

## Core law

1. Kernel truth remains primary.
2. Witness/report/provenance surfaces remain subordinate.
3. All new automation must remain supervised unless explicitly ratified otherwise.
4. Operator control must become explicit before broader daemon claims.
5. Recovery and replay must exist before any stronger operational autonomy claim.
6. New witness-chain packets are frozen by default unless directly required by operationalization.

## Packet ledger

| packet_id | objective | allowed_files | non_goals | status | next_lawful_packet |
|---|---|---|---|---|---|
| J0 | Land the operational rebase audit, master plan, and active operationalization ledger | audit, plan, ledger, `PLAN.md`, legacy migration note | no new daemon claims; no new witness-tier expansion | COMPLETE | J1 |
| J1 | Land the supervised automation floor: policy matrix, operator controls, and daemon service harness | `ION/02_architecture/SUPERVISED_AUTOMATION_POLICY_PROTOCOL.md`, `ION/02_architecture/SUPERVISED_DAEMON_SERVICE_PROTOCOL.md`, `ION/02_architecture/OPERATOR_CONTROL_PROTOCOL.md`, `ION/06_intelligence/specs/T38_*.md`, `ION/06_intelligence/specs/T39_*.md`, `ION/06_intelligence/specs/T40_*.md`, `ION/04_packages/kernel/automation_policy.py`, `ION/04_packages/kernel/operator_control.py`, `ION/04_packages/kernel/daemon_service.py`, tests | no unattended daemon claim; no external execution; no witness-stack expansion beyond direct service receipts | COMPLETE | J2 |
| J2 | Operationalize child-work issuance under supervised service mode | planner gate, child issuance, daemon service integration, protocol/spec surfaces, tests | no unattended multi-agent field; no MCP bridge yet | COMPLETE | J3 |
| J3 | Land recovery and replay receipts plus bounded run resumption | recovery protocol/spec, daemon service receipts, replay helper, tests | no hidden auto-resume; no unattended restart loop | COMPLETE | J4 |
| J4 | Land external execution / MCP service bridge for supervised automation | MCP-facing service protocol/spec and bounded integration surfaces | no uncontrolled external writes; no authority collapse | COMPLETE | J5 |
| J5 | Harden the supervised operational runtime and document live operator run mode | service runbooks, startup/shutdown contract, acceptance checklist, selective packaging | no autonomy overclaim; no witness-chain growth as substitute for ops | COMPLETE | K1 |

## J1 landing note

J1 establishes the first truthful supervised automation floor:
- explicit automation policy evaluation
- explicit operator hold / resume / stop state
- explicit daemon service runner over the already landed daemon loop
- service receipts and service ledger outputs

What remains intentionally deferred:
- child-work issuance policy integration
- recovery / replay
- external execution / MCP bridge
- any claim of unattended autonomy


## J2 landing note

J2 establishes supervised child-work issuance as a first-class service path:
- explicit manifest or question/delta selection
- automation-policy evaluation for `ISSUE_CHILD_WORK`
- operator stop/hold enforcement
- review-pressure and spawn-policy approval checks
- durable child-work service receipts and ledger rows
- daemon-service delegation into the new child-work service

What remains intentionally deferred:
- recovery/replay for interrupted child-work service runs
- unattended issuance loops
- external execution / MCP surfaces


## J3 landing note

J3 establishes the first truthful daemon-service recovery/replay floor:
- machine-readable resumable / non-resumable classification in daemon-service receipts
- explicit replay selection by receipt or latest resumable ledger candidate
- stale resumable detection
- bounded replay receipts and replay ledger rows
- replay through the live daemon-service policy/control path rather than a bypass

What remains intentionally deferred:
- unattended restart loops
- automatic replay of child-work issuance runs
- external execution / MCP recovery surfaces

## J4 landing note

J4 establishes the first truthful external execution / MCP bridge floor:
- explicit export of lawful external execution packets through the normal dispatch path
- explicit acceptance of returned external execution payloads through the normal execution path
- machine-readable MCP automation surfaces embedded in exported packets
- automation-policy action classes for external export and external return acceptance
- daemon-service delegation into the new bridge

What remains intentionally deferred:
- no direct external governed-write application
- no hidden autonomous MCP loop
- no authority promotion from bridge artifacts into kernel truth
- no operational hardening/runbook packaging yet



## J5 landing note

J5 establishes a truthful operational hardening floor for the supervised runtime:
- explicit supervised runtime startup / shutdown lifecycle receipts
- preferred active automation mode persisted in machine-readable runtime state
- bounded operator runbooks generated from the live service/control surface
- operational acceptance checklist aligned to the master-plan criteria

What remains intentionally deferred:
- installer/deployment packaging outside the repository
- unattended service management
- platform-native process supervisors
- any autonomy claim beyond the supervised active root
