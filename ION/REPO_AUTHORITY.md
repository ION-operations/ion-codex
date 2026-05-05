---
type: repo_authority
authority: A1_CANONICAL
created: 2026-04-13T16:20:00-04:00
status: ACTIVE
---

> Operational mount order is governed by `ION/02_architecture/ION_MOUNT_CONTRACT.md`.

# ION Repo Authority

This file answers one startup question only:

**What is authoritative in this repository right now?**

## Canonical root

The canonical content root in this repository is **this `ION/` directory
itself**.

Use these root assumptions:

- package root: `ION/04_packages/kernel/`
- test root: `ION/tests/`
- doctrine root: `ION/01_doctrine/`
- architecture root: `ION/02_architecture/`
- registry root: `ION/03_registry/`
- templates root: `ION/07_templates/`

## Shell-root distinction

This extracted branch also has a **shell root** one level above this content
root:

`.`

That shell root carries:

- `pyproject.toml`
- editable-install semantics
- pytest configuration for `ION/tests`

Practical rule:

- use the **content root** for ordinary reading and code navigation
- use the **shell root** for package-aware commands such as editable install
  and pytest runs that rely on `pyproject.toml`

## Cursor carrier lane (IDE / local Steward mount)

For Cursor-as-carrier work aligned with `ION/02_architecture/ION_OVER_CURSOR_PROTOCOL.md`
and `.cursor/rules/ion-carrier-mount.mdc`:

- **Cursor** is chassis/carrier; **ION roles** are mounted identities (boots + bounded packets).
- The **Cursor parent chat** is an available carrier by default; it operates as **task-scoped local STEWARD carrier** for orchestration only after explicit mount with bounded mission, this `ION/REPO_AUTHORITY.md`, and `ION/03_registry/boots/STEWARD.boot.md`.
- **Cursor subagents** (for example Task) are **carrier slots**, not roles; prompts are **WorkPacket / ContextPackage** renderings; subagent returns are **proposals** until integrated by the mounted parent flow.
- **Manual mode** is **template-bound** automation-equivalent execution (`MANUAL_AUTOMATION_FALLBACK_PROTOCOL.md` / equivalence protocol).
- **`ION/07_templates/`** is the template substrate; **MINI.md / CAPSULE.md** are not the primary carrier context authority for this lane.
- This lane carries **no production authority**, **no live MCP execution** claim, and **no separate Cursor agent ontology** beyond carrier + mounted role law above.

## Meta Carrier evolution (manual-first)

Carrier **level** (L0 manual → L4 runtime) is **not** chat authority. It is bound by:

- `ION/04_agents/carriers/META_CARRIER_EVOLUTION_PROTOCOL.md` — manual-first upgrades, proof, decision artifacts;
- `ION/03_registry/capabilities/capability_registry.json` — capability ↔ manual mirror ↔ required proof;
- `ION/07_templates/carriers/CARRIER_CAPABILITY_SURVEY.md` — survey fields **reuse** `ACTIVE_WORK_PACKET` / spawn plan / signal paths.

**Packet law is unchanged:** `ACTIVE_WORK_PACKET.json`, `ACTIVE_ROLE_SPAWN_PLAN.json` (when present), `kernel.ion_cycle_runner`, `validation_commands`, and `MANUAL_AUTOMATION_FALLBACK_PROTOCOL.md` remain the routing spine. Meta layer only constrains **what the host may claim** before obeying those artifacts.

## Historical path alias

Many recovery and handoff documents still refer to:

`ION_Working_Branch_M16/ION`

Inside this repository, treat that string as a **historical alias** for the current root:

`ION/`

Those older references are not new competing roots. They record the path name of the extracted recovery branch at the time those documents were written.

## Nested packaged-path correction

This repository also contains a nested path:

`ION/ION/05_context/...`

That nested `ION/` directory is **not** a second runnable root.

Treat it as an embedded context/history residue lane inside the packaged root.
It currently contains runtime witness material such as daemon ledgers, archived
signals, and kernel-store residue.

Practical rule:

- `ION/04_packages/`, `ION/tests/`, `ION/03_registry/`, and the rest of the
  startup surface refer to the packaged root itself
- `ION/ION/05_context/...` refers to embedded residue under that root
- top-level production `ION/` in the wider workspace remains a different root
  and is handled by the reintegration registries, not by this repo-local
  authority file alone

## Historical startup bundle disposition

The April 17 root-authority startup bundle was a reintegration witness surface,
not current carrier onboarding law. It is retired from hot startup authority as
of V123 because it centered a `START_HERE.md` read path and conflicted with
ION-native carrier onboarding.

Contained evidence lives under:

`ION/05_context/archive/containment/V123_ROOT_ONBOARDING_SHIMS/root_authority_bundle_2026-04-17/`

Do not use that bundle as the first read for current carrier mount. Use the
mount contract, carrier registries, execution packet templates, active packets,
and role/context packages.

## What is canonical here

### A1 startup authority

Read these first when entering the repo fresh for current carrier work:

1. `ION/REPO_AUTHORITY.md`
2. `ION/02_architecture/ION_MOUNT_CONTRACT.md`
3. `ION/docs/setup/ION_CURRENT_OPERATING_PACKET_V119.md`
4. the selected carrier profile under `ION/03_registry/`
5. the selected carrier execution packet template under `ION/07_templates/carriers/`
6. the active packet or spawn-row context package under `ION/05_context/current/`
7. `ION/01_doctrine/CANONICAL_WORKFLOW.md` when broad workflow doctrine is needed
8. `ION/AGENT_CONTRACT.md` when legacy agent-contract context is explicitly needed

### A1 executable authority

These are the executable center of gravity in the current repo:

- `ION/04_packages/kernel/`
- shell-root `pyproject.toml`
- `ION/tests/`

Current runnable proof posture already recorded in this branch:

- editable install works from the branch shell root
- after editable install from the branch shell root, `import kernel` works
  without manual `PYTHONPATH`
- after editable install from the branch shell root, `python -m kernel` works
- `env -u PYTHONPATH python3 -m pytest ION/tests -q` passes from the branch
  shell root for the current branch generation

### A1 workflow authority

These documents define the lawful loop rather than merely describing it:

- `ION/01_doctrine/CANONICAL_WORKFLOW.md`
- `ION/AGENT_CONTRACT.md`
- `ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md`
- `ION/02_architecture/HANDOFF_TAKEOVER_NORMALIZATION_PROTOCOL.md`
- `ION/02_architecture/MANUAL_AUTOMATION_EQUIVALENCE_PROTOCOL.md`
- `ION/02_architecture/CONTEXT_PERFECT_CONTINUATION_PROTOCOL.md`
- `ION/02_architecture/LAWFUL_ORCHESTRATION_SCHEDULER_PROTOCOL.md`
- `ION/02_architecture/BOUNDED_PARALLELISM_AND_SETTLEMENT_PROTOCOL.md`

## What is supporting but not primary

These are useful orientation or projection surfaces, but they should not replace the primary law above:

- `ION/README.md`
- `ION/STATUS.md`
- `ION/PLAN.md`
- `ION/MASTER_ORCHESTRATION_INDEX.md`
- `ION/docs/README.md`
- current-branch orchestration maps under `ION/06_intelligence/orchestration/`

## What is witness and recovery context

The corpus recovery program and wider-estate references remain valuable, but they are **witness context**, not startup law for this repo.

Primary recovery surfaces:

- `ION/06_intelligence/orchestration/2026-04-13_corpus_recovery_program_index.md`
- `ION/06_intelligence/orchestration/corpus_recovery/`
- `ION/06_intelligence/research/2026-04-11_codex_m16_witness_authority_crosswalk.md`

Important practical rule:

- if a recovery note references wider-estate paths that are not present in this zip, do **not** treat that as a defect in the runnable kernel root
- treat those references as archaeology, provenance, or future recovery inputs unless a bounded packet explicitly imports them

## Current truthful posture

The current repo already contains the ratified kernelized branch with doctrine, registry, templates, packaging, operator CLI, daemon surfaces, packet law, continuation law, takeover law, scheduler law, allocator law, runtime reports, and proof tests.

The current repo does **not** require a fresh executor to resolve the full wider estate before operating lawfully here.

## Next-work rule

Do not infer an automatic successor phase from the existence of historical packets.

Any further implementation should be chosen as a **new bounded workload** against the current canonical root.


## Codex CLI local worker lane (V125)

Codex CLI is the preferred local bounded worker carrier for current build work.
It is governed by:

- `ION/02_architecture/CODEX_CLI_CARRIER_PROTOCOL.md`
- `ION/03_registry/codex_cli_carrier_profile.yaml`
- `ION/07_templates/carriers/CODEX_CLI_EXECUTION_PACKET.md`
- `ION/docs/setup/CODEX_CLI_ION_DOGFOOD_SETUP_V125.md`
- `ION/04_packages/kernel/ion_codex_cli_carrier_audit.py`

ChatGPT browser remains coordinator/continuity lane through the bounded MCP
connector. Codex CLI is the local filesystem/build/test worker carrier. Neither
carrier is ION identity, STEWARD, RELAY, or PERSONA.

## One-sentence judgment

Treat this repository as the active runnable ION kernel branch, but keep shell
root and content root distinct: package-aware commands start from the shell
root, while ordinary startup law and content navigation remain centered on
`ION/`.
