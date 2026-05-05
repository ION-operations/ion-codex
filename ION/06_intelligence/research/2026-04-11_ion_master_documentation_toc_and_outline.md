---
type: research
authority: A3_OPERATIONAL
created: 2026-04-11T12:00:00-04:00
status: ACTIVE
purpose: Single master TOC and section outline for the full ION estate documentation effort (encyclopedia scope)
ratification: NOT_RATIFIED
connections:
  - ION/README.md
  - ION/MASTER_ORCHESTRATION_INDEX.md
  - ION/01_doctrine/CANONICAL_WORKFLOW.md
  - ION/AGENT_CONTRACT.md
  - ION/SYSTEM_MAP.md
  - ION/06_intelligence/orchestration/2026-04-09_ion_full_system_architecture_and_end_state_framework.md
  - ION/06_intelligence/orchestration/2026-04-10_post_m16_state_forward_path_and_codex_handoff.md
  - ION/06_intelligence/research/2026-04-11_codex_ion_identity_origin_destination_recovery_index.md
---

# ION master documentation — table of contents and outline

This file is the **authoritative outline** for documenting the entire ION project in the active working root (`ION_Working_Branch_M16/ION`). Each section below is a **documentation chapter** to be filled over multiple sessions. Detailed prose belongs in dedicated artifacts (this outline stays navigable).

## How to use this outline

1. **Anchor first:** read `ION/README.md` then follow its read order through doctrine, contract, system map, full-system architecture, and `ION/MASTER_ORCHESTRATION_INDEX.md`.
2. **Three views:** for every topic, eventually capture **law** (protocols), **code** (kernel modules), **proof** (tests).
3. **Milestone spine:** map features to **K / L / M** (and J where operational) using `ION/STATUS.md` and post-Mn handoff docs as the current-state witness.
4. **Nested tree:** explicitly reconcile `ION/ION/` (nested copy or partial mirror) during inventory — do not assume identity with the parent `ION/` tree without verification.

---

## Part I — Entry, authority, and scope

| § | Chapter | Primary sources | Notes |
|---|---------|-----------------|-------|
| I.1 | Operator read order and trust anchors | `ION/README.md`, `ION/STATUS.md` | What to read first; what is projection vs source continuity |
| I.2 | Doctrine: canonical workflow | `ION/01_doctrine/CANONICAL_WORKFLOW.md` | One loop; manual/automation symmetry |
| I.3 | Executor contract | `ION/AGENT_CONTRACT.md` | Obligations of every executor class |
| I.4 | System map (module families) | `ION/SYSTEM_MAP.md` | Map families → kernel files |
| I.5 | Full-system architecture and end state | `ION/06_intelligence/orchestration/2026-04-09_ion_full_system_architecture_and_end_state_framework.md` | North star |
| I.6 | Master orchestration and completion law | `ION/MASTER_ORCHESTRATION_INDEX.md` | Completion-scale entry; doctrine anchors list |
| I.7 | Current posture and next center (M17+) | `ION/06_intelligence/orchestration/2026-04-10_post_m16_state_forward_path_and_codex_handoff.md`, `ION/STATUS.md` | Frontier after M16 |
| I.8 | Legacy / archival plan context | `ION/PLAN.md` | Consolidation blueprint; not the sole active driver |
| I.9 | Recovery and identity (compact re-entry) | `ION/06_intelligence/research/2026-04-11_codex_ion_identity_origin_destination_recovery_index.md` | Bounded answers for what / where / whither |

---

## Part II — Architecture protocols (`ION/02_architecture/`)

Document each protocol with: **purpose**, **relationship to K/L/M**, **kernel touchpoints**, **tests** (if any). Grouped below for writing batches.

### II.A — Horizon and workflow rehearsal

- `HORIZON_ORCHESTRATION_PROTOCOL.md`
- `HORIZON_STATE_AND_TIGHTENING_PROTOCOL.md`
- `HORIZON_PACKET_ENACTMENT_PROTOCOL.md`
- `HORIZON_ENACTMENT_RECEIPT_PROTOCOL.md`
- `HORIZON_TO_EXECUTION_WORKFLOW_REHEARSAL_PROTOCOL.md`

### II.B — Scheduler, capabilities, takeover, equivalence, continuation

- `LAWFUL_ORCHESTRATION_SCHEDULER_PROTOCOL.md`
- `EXECUTOR_CAPABILITY_REGISTRY_PROTOCOL.md`
- `HANDOFF_TAKEOVER_NORMALIZATION_PROTOCOL.md`
- `MANUAL_AUTOMATION_EQUIVALENCE_PROTOCOL.md`
- `CONTEXT_PERFECT_CONTINUATION_PROTOCOL.md`
- `PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md`
- `MANUAL_AUTOMATION_FALLBACK_PROTOCOL.md`

### II.C — Bounded parallelism, allocator, settlement, branch, fan-in

- `BOUNDED_PARALLELISM_AND_SETTLEMENT_PROTOCOL.md`
- `BOUNDED_MULTI_AGENT_ALLOCATOR_PROTOCOL.md`
- `FAN_IN_MERGE_REVIEW_SETTLEMENT_PROTOCOL.md`
- `BRANCH_BUDGET_RECURSION_AND_DRIFT_CONTROL_PROTOCOL.md`
- `BRANCH_HORIZON_SCHEDULE_SYNCHRONIZATION_PROTOCOL.md`
- `BRANCH_RESCHEDULING_AND_REBINDING_PROTOCOL.md`

### II.D — Schedule lifecycle (M6–M16 cluster)

- `SCHEDULE_STALE_RETRY_AND_REASSIGNMENT_PROTOCOL.md`
- `SCHEDULE_DISPATCH_AND_ASSIGNMENT_RECONCILIATION_PROTOCOL.md`
- `SCHEDULE_COMPLETION_AND_ASSIGNMENT_RELEASE_PROTOCOL.md`
- `SCHEDULE_SETTLEMENT_AND_FUTURE_REENTRY_PROTOCOL.md`
- `SCHEDULE_LINEAGE_AND_SUPERSESSION_ARCHIVAL_PROTOCOL.md`
- `SCHEDULE_LINEAGE_REPLAY_AND_ACTIVE_CYCLE_RECONSTRUCTION_PROTOCOL.md`
- `SCHEDULE_RESUME_PROJECTION_PROTOCOL.md`
- `SCHEDULE_RESUME_BUNDLE_MATERIALIZATION_PROTOCOL.md`
- `SCHEDULE_TAKEOVER_ENTRY_ACTIVATION_VALIDATION_PROTOCOL.md`
- `ACTIVATION_SUMMARY_HANDOFF_CAPSULE_MATERIALIZATION_PROTOCOL.md`
- `HANDOFF_CAPSULE_EXECUTOR_ENTRY_REHEARSAL_PROTOCOL.md`

### II.E — Operator, daemon, automation, hardening, external bridge

- `OPERATOR_ENTRY_SURFACE_PROTOCOL.md`
- `OPERATOR_CONTROL_PROTOCOL.md`
- `SUPERVISED_DAEMON_SERVICE_PROTOCOL.md`
- `SUPERVISED_AUTOMATION_POLICY_PROTOCOL.md`
- `AUTOMATION_STATE_PROTOCOL.md`
- `OPERATIONAL_HARDENING_PROTOCOL.md`
- `EXTERNAL_EXECUTION_MCP_BRIDGE_PROTOCOL.md`
- `RECOVERY_AND_REPLAY_PROTOCOL.md`
- `CHILD_WORK_OPERATIONALIZATION_PROTOCOL.md`

### II.F — Bootstrap and working-agent

- `bootstrap` family (see `bootstrap_init.py` / `bootstrap_bridge.py` / `bootstrap_activation.py` naming in protocols if split)
- `WORKING_AGENT_SELF_USE_PROTOCOL.md`
- `HANDOFF_TAKEOVER_NORMALIZATION_PROTOCOL.md` (cross-link Part II.B)

### II.G — Context, rank, multi-chat, IDE

- `CONTEXT_PLANES.md`
- `CONTEXT_MODE_PROTOCOL.md`
- `RANK_AND_PRECEDENCE_PROTOCOL.md`
- `MULTI_CHAT_COORDINATION.md`
- `ION_OVER_CURSOR_PROTOCOL.md`
- `CODEX_LEAD_ORCHESTRATION_PROTOCOL.md`
- `CONTINUITY_ARCHITECTURE.md`

### II.H — Runtime reports (family)

All `RUNTIME_REPORT_*` protocols, including governance, trace, digest, browser, visibility, provenance, temporal, comparative, operator digest, triggers, anchors, crosslink, navigation, artifact — **one sub-index table** listing each file and its role in the witness layer.

### II.I — Domain, semantic, relay, archaeology

- `INTELLIGENT_DOMAIN_PROTOCOL.md`
- `TRUE_NAME_AND_SEMANTIC_LAYER_PROTOCOL.md`
- `MANIFEST_AND_ROUTE_STATE_PROTOCOL.md`
- `RUNTIME_STATE_*` protocols (binding, query, reporting, sync as applicable)
- `SOVEREIGN_RELAY_PROTOCOL.md`
- `ARCHAEOLOGY_DAEMON_PROTOCOL.md`, `ARCHAEOLOGY_DAEMON_CONTRACT.md`
- `CONJUGATE_DAIMON_PROTOCOL.md`
- `AGENT_REASONING_PROTOCOL.md`

### II.J — Template binding

- `TEMPLATE_BINDING_PROTOCOL.md`

---

## Part III — Kernel implementation (`ION/04_packages/kernel/`)

### III.1 — Truth and storage

- `model.py`, `store.py`, `index.py`, `graph.py` — entities, persistence, queries, graph role

### III.2 — Operator surface

- `operator_cli.py`, `__main__.py` — **CLI command tree** (single appendix: command → behavior → receipt)

### III.3 — Packets, horizon, sequential routing

- `packet_validation.py`, `horizon_state.py`, `sequential_kernel.py`, related receipts in `model`/`store`

### III.4 — Scheduling and execution

- `scheduler.py`, `executor_registry.py`, `dispatch.py`, `execution.py`, `validation.py`, `commit.py`, `threshold.py`, `governed_write.py`

### III.5 — Takeover, equivalence, continuation

- `takeover.py`, `equivalence.py`, `continuation.py`

### III.6 — Allocator, settlement, branch controls, horizon sync, rescheduling

- `allocator.py`, `settlement.py`, `branch_controls.py`, `branch_horizon_sync.py`, `branch_rescheduling.py`

### III.7 — Schedule controls and reconciliation

- `schedule_controls.py`, `schedule_dispatch_reconciliation.py`, `schedule_completion_release.py`, `schedule_settlement.py`, `schedule_lineage.py`, `schedule_lineage_replay.py`, `schedule_resume_projection.py`, `schedule_resume_bundle.py`, `schedule_takeover_activation.py`, `schedule_handoff_capsule.py`, `schedule_handoff_entry_rehearsal.py`

### III.8 — Daemon and supervised runtime

- `daemon.py`, `daemon_actions.py`, `daemon_loop.py`, `daemon_service.py`, `automation_policy.py`, `operator_control.py`, `operational_hardening.py`, `automation_state.py`

### III.9 — Bootstrap

- `bootstrap_init.py`, `bootstrap_bridge.py`, `bootstrap_activation.py`

### III.10 — Child work, recovery, external execution

- `children.py`, `planner_gate.py`, `child_work_service.py`, `recovery_replay.py`, `external_execution_bridge.py`

### III.11 — Context, capsule, manifest

- `context_compiler.py`, `capsule_manager.py`, `manifest_state.py`

### III.12 — Questions, reviews, signals

- `questions.py`, `question_answers.py`, `reviews.py`, `signals.py`, `signal_followups.py`

### III.13 — Runtime reporting (code)

- All `runtime_report_*.py`, `runtime_reporting.py`, `runtime_state_*.py`, `receipts.py` — map each to Part II.H protocols

---

## Part IV — Context and coordination (`ION/05_context/`)

| § | Chapter | Primary sources |
|---|---------|-----------------|
| IV.1 | Directory layout | `signals/`, `comms/`, `inbox/`, `history/` |
| IV.2 | Signal schema and routing | `*.signal.md` frontmatter patterns |
| IV.3 | Kernel router runs and startup packets | `comms/kernel_router_runs/` |
| IV.4 | Migration and operational ledgers | `comms/migration_ledgers/` |
| IV.5 | Sovereign and roundtable comms | `comms/sovereign/`, `comms/roundtable/` |
| IV.6 | History stores (receipts, daemon, supervised runtime) | `history/*` |

---

## Part V — Intelligence layer (`ION/06_intelligence/`)

| § | Chapter | Primary sources |
|---|---------|-----------------|
| V.1 | Orchestration — full system, roadmap, trajectory, post-Mn handoffs | `orchestration/` |
| V.2 | Research — dated artifacts, indices, recovery | `research/` |
| V.3 | Audits | `audits/` |
| V.4 | Decisions, specs | `decisions/`, `specs/` |
| V.5 | Archaeology (e.g. vestige) | `archaeology/` |
| V.6 | Relay and roundtable | `relay/`, `roundtable/` |
| V.7 | Daimon | `daimon/` |

---

## Part VI — Registry, agents, templates

| § | Chapter | Primary sources |
|---|---------|-----------------|
| VI.1 | Boots and registries | `ION/03_registry/boots/`, `domains/`, `semantic_identities/` |
| VI.2 | Agent lanes | `ION/agents/*` — MINI/CAPSULE per role; projection vs source |
| VI.3 | Templates | `ION/07_templates/` — bindings, confidence, reports, actions |

---

## Part VII — Tests as specification (`ION/tests/`)

| § | Chapter | Primary sources |
|---|---------|-----------------|
| VII.1 | Per-file test map | `test_kernel_*.py` → feature → protocol |
| VII.2 | Integration proof | `test_kernel_workflow_rehearsal.py` — end-to-end narrative |
| VII.3 | pytest and entry | how to run, env assumptions |

---

## Part VIII — Synthesis artifacts (to author after Parts I–VII)

| Artifact | Purpose |
|----------|---------|
| K/L/M glossary | One row per milestone term: definition, protocol(s), module(s), test(s) |
| Current vs end-state delta | From roadmap + post-M16 handoff + `MASTER_ORCHESTRATION_INDEX.md` |
| CLI quick reference | Single table: `python -m kernel ...` subcommands |
| Optional diagrams | Workflow loop, store/index flow, schedule lifecycle |

---

## Part IX — Inventory and nested tree (explicit)

| Task | Outcome |
|------|---------|
| Compare `ION/` vs `ION/ION/` | Table of paths that differ, are duplicated, or are unique |
| File counts by top-level dir | Baseline for coverage |
| Authority tagging | Spreadsheet or table: A1/A2/A3 from frontmatter where present |

---

## Definition of done (documentation effort)

- [ ] Every Part above has at least one **filled** subordinate doc or section (not only titles).
- [ ] Every `02_architecture` protocol has a **summary** + links to code/tests where applicable.
- [ ] `SYSTEM_MAP` families have a **closed file list** under Part III.
- [ ] K/L/M frontier matches **`ION/STATUS.md`** and latest post-Mn handoff unless contradictions are explicitly documented.
- [ ] This TOC is **updated** when new major artifacts land (new protocol, new kernel module family, new signal class).

---

## Session log (append one block per documentation pass)

```text
Date:
Scope (which Parts/sections):
Artifacts read:
Contradictions found:
Next session focus:
```
