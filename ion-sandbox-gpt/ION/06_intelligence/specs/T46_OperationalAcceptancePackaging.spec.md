---
type: spec
authority: A3_OPERATIONAL
created: 2026-04-08T23:13:00-04:00
status: ACTIVE
owner: Codex working session
purpose: Define operational runbook and acceptance-checklist packaging for the supervised runtime surface
connections:
  - ION/02_architecture/OPERATIONAL_HARDENING_PROTOCOL.md
  - ION/04_packages/kernel/operational_hardening.py
  - ION/06_intelligence/research/2026-04-08_ion_operationalization_master_plan.md
---

# T46 — Operational Acceptance Packaging

## Required outputs

### Runbook
Generated under:
- `ION/05_context/runtime_reports/operations/runbooks/`

Required content:
- current preferred active mode
- current operator service mode
- latest daemon-service evidence
- startup sequence
- shutdown sequence
- acceptance overview

### Acceptance checklist
Generated under:
- `ION/05_context/runtime_reports/operations/acceptance/`

Required content:
- all master-plan acceptance criteria
- satisfaction boolean per criterion
- evidence paths per criterion

## Master-plan acceptance criteria

1. Operator control posture is machine-readable.
2. Daemon service start path is explicit and supervised.
3. Refusal remains lawful and explicit.
4. Child-work issuance is approval-aware.
5. Recovery and replay exist before stronger autonomy claims.
6. Witness/report surfaces remain subordinate to the operational kernel.
