---
type: canonicalization_decision
template: CANONICALIZATION_DECISION
created: 2026-04-17T00:00:00-04:00
status: WORKING
scope: top_level_production_surface_promotion_map
decision_class: promotion
connections:
  - ION/06_intelligence/decisions/2026-04-17_workspace_root_authority_canonicalization_decision.md
  - ION/06_intelligence/decisions/2026-04-17_aim_ion_aim_os_classification_canonicalization_decision.md
  - ION/06_intelligence/decisions/2026-04-17_external_transport_shell_current_phase_disposition_decision.md
  - ION/06_intelligence/orchestration/2026-04-17_branch_root_shell_vs_content_root_clarification.md
  - ION/06_intelligence/orchestration/2026-04-17_external_service_shell_vs_runtime_entry_clarification.md
  - ION/03_registry/reintegration/root_manifest.yaml
  - ION/03_registry/reintegration/authority_registry.yaml
  - ION/03_registry/reintegration/canonicalization_queue.yaml
  - /home/sev/ION - Production/ION most recent/ion_current_canonical_runtime_fleet_temporal_2026-04-16/pyproject.toml
  - /home/sev/ION - Production/ION most recent/ion_current_canonical_runtime_fleet_temporal_2026-04-16/ION/tests/test_packaging_entry_posture.py
  - /home/sev/ION - Production/ION/pyproject.toml
  - /home/sev/ION - Production/ION/04_packages/ion_api/main.py
  - /home/sev/ION - Production/ION/04_packages/kernel/preflight_cli.py
  - /home/sev/ION - Production/ION/04_packages/kernel/genome_manager.py
  - /home/sev/ION - Production/ION/04_packages/kernel/host_substrate.py
  - /home/sev/ION - Production/ION/04_packages/kernel/template_catalog.py
  - /home/sev/ION - Production/ION/docs/README.md
  - /home/sev/ION - Production/ION/docs/PRODUCTION_RUNBOOK.md
  - /home/sev/ION - Production/ION/docs/O1_RATIFICATION_CHECKLIST.md
  - /home/sev/ION - Production/ION/docs/program/README.md
  - /home/sev/ION - Production/ION/docs/program/00_master_index.md
  - /home/sev/ION - Production/ION/docs/program/program_index.json
  - /home/sev/ION - Production/ION/tests/test_ion_api.py
  - /home/sev/ION - Production/ION/tests/test_ion_api_integration.py
  - /home/sev/ION - Production/ION/tests/test_ion_state_mcp_server.py
  - /home/sev/ION - Production/ION/tests/test_ion_policy_mcp_server.py
  - /home/sev/ION - Production/ION/tests/test_ion_recon_mcp_server.py
  - /home/sev/ION - Production/ION/tests/test_ion_evidence_mcp_server.py
  - /home/sev/ION - Production/ION/tests/test_preflight_cli.py
  - /home/sev/ION - Production/ION/tests/test_template_catalog.py
  - /home/sev/ION - Production/ION/tests/test_genome_manager.py
  - /home/sev/ION - Production/ION/tests/test_host_substrate.py
  - /home/sev/ION - Production/ION/tests/test_kernel_buses.py
---

# Canonicalization Decision: Top-Level Production Surface Promotion Map

## Purpose

Close q003 far enough that the project can stop referring vaguely to
"MCP/API/docs/preflight surfaces in top-level `ION/`" and instead operate from
an explicit promotion map.

This packet does not execute the promotions. It classifies the unique
production-side surfaces into:

- promote first,
- promote as a coupled service packet,
- selectively extract,
- or retain as witness / regenerate later.

## Scope and competing candidates

Primary scope: production-only or production-primary surfaces inside
top-level `ION/` that are not present in the packaged current-generation root.

Surface families in scope:

1. packaging and entry floor
2. read-only API and MCP service packages
3. preflight / operator-support kernel helpers
4. docs hub and runbook surfaces
5. docs/program manual stack
6. generated build and egg-info artifacts
7. older kernel support wrappers unique to production

This decision is about promotion mapping, not code movement.

## Evidence considered

Primary production-root evidence:

- `ION/pyproject.toml`
- `ION/04_packages/ion_api/`
- `ION/04_packages/ion_evidence_mcp/`
- `ION/04_packages/ion_policy_mcp/`
- `ION/04_packages/ion_recon_mcp/`
- `ION/04_packages/ion_state_mcp/`
- `ION/04_packages/kernel/preflight_cli.py`
- `ION/04_packages/kernel/genome_manager.py`
- `ION/04_packages/kernel/host_substrate.py`
- `ION/04_packages/kernel/template_catalog.py`
- `ION/docs/README.md`
- `ION/docs/PRODUCTION_RUNBOOK.md`
- `ION/docs/O1_RATIFICATION_CHECKLIST.md`
- `ION/docs/program/README.md`
- `ION/docs/program/00_master_index.md`
- `ION/docs/program/13_implementation_state_and_roadmap.md`
- `ION/docs/program/program_index.json`

Verification / proof surfaces:

- `ION/tests/test_ion_api.py`
- `ION/tests/test_ion_api_integration.py`
- `ION/tests/test_ion_state_mcp_server.py`
- `ION/tests/test_ion_policy_mcp_server.py`
- `ION/tests/test_ion_recon_mcp_server.py`
- `ION/tests/test_ion_evidence_mcp_server.py`
- `ION/tests/test_preflight_cli.py`
- `ION/tests/test_template_catalog.py`
- `ION/tests/test_genome_manager.py`
- `ION/tests/test_host_substrate.py`
- `ION/tests/test_kernel_buses.py`

Context from the current packaged root:

- the extracted branch already carries a minimal shell-root `pyproject.toml`
- the extracted branch already has packaging posture proof in
  `ION/tests/test_packaging_entry_posture.py`
- the extracted branch already carries internal API carrier-entry law in
  `kernel.api_runtime_entry`
- packaged root lacks top-level `docs/`
- packaged root already carries the later reintegration/orchestration spine

## Decision

### 1. Promotion classes

The top-level production surfaces split into four promotion classes.

#### Class A — No standalone first-wave promotion from top-level production packaging

No top-level production artifact is currently authorized as a standalone
first-wave packaging/entry packet.

Surfaces held out of standalone first-wave promotion:

- `pyproject.toml`
- `04_packages/kernel/preflight_cli.py`

Reason:

- the extracted branch already has its own minimal shell-root packaging floor
- top-level production `pyproject.toml` is coupled to the API/MCP transport shell
  through its declared scripts
- `preflight_cli.py` is also service-coupled because it imports `ion_api.main`
  and the `ion_*_mcp.logic` modules

Rule:

Do not copy top-level production packaging/preflight into the extracted branch
as if they were a missing standalone floor.

#### Class B — Promote, if chosen later, as a coupled external service shell packet

Promote together, not piecemeal:

- `pyproject.toml`
- `04_packages/kernel/preflight_cli.py`
- `04_packages/ion_api/`
- `04_packages/ion_evidence_mcp/`
- `04_packages/ion_policy_mcp/`
- `04_packages/ion_recon_mcp/`
- `04_packages/ion_state_mcp/`
- `04_packages/kernel/genome_manager.py`
- `04_packages/kernel/host_substrate.py`
- `04_packages/kernel/template_catalog.py`

Reason:

- these surfaces already behave as one coupled transport / service-support
  layer
- the production `pyproject.toml` scripts and `preflight_cli.py` are not
  separable from the later transport shell they verify or launch
- `ion_api.main` depends directly on host snapshot, genome summary, template
  registry summary, recon, and state logic
- the MCP packages have explicit server smoke tests and the API has both route
  and integration-style tests
- the extracted branch already owns internal API runtime-entry law, so this
  packet is not the missing runtime/session core; it is an optional external
  read-only service shell / transport adjunct

Rule:

Treat this as one optional later promotion packet over existing branch law, not
as the branch's missing API-entry core and not as five unrelated package
copies.

#### Class C — Selective extraction only

Do not wholesale-promote the entire production docs tree. Instead extract only
the highest-signal operator surfaces first:

- `docs/README.md`
- `docs/PRODUCTION_RUNBOOK.md`
- `docs/O1_RATIFICATION_CHECKLIST.md`

Reason:

- these are operational surfaces with current install/verify/deploy value
- they can guide packaged-root operator onboarding
- they do not need the full older docs/program stack to remain useful

Rule:

These should be re-anchored into the packaged current-generation root in a form
that points at current root authority, not copied as a second competing startup
story.

#### Class D — Retain as witness, extract later if justified

Retain as witness-first material for now:

- `docs/program/`
- `docs/program/program_index.json`
- `04_packages/kernel/comms_bus.py`
- `04_packages/kernel/memory_bus.py`
- `04_packages/kernel/persistence.py`
- `build/`
- generated `ion_kernel.egg-info/` artifacts

Reason:

- the docs/program stack is broad, partly historical, and includes at least one
  explicit stub (`13_implementation_state_and_roadmap.md`)
- the older kernel bus/persistence wrappers are not required for the first
  packaging/API/MCP promotion packet
- build output and egg-info are regenerable artifacts, not canonical sources

Rule:

No full docs/program import and no build-artifact copying in the first
promotion sequence.

### 2. Production domains after mapping

The production-only surface map is now:

1. no standalone top-level production packaging/entry promote-first packet
2. top-level production packaging/preflight plus read-only API/MCP transport
   shell = coupled optional later promotion packet
3. docs hub / runbook / ratification checklist = selective extraction
4. docs/program manual stack = witness-first, selective extraction only later
5. older kernel bus/persistence wrappers = witness-first unless a later packet
   proves they are still needed
6. build artifacts = regenerate, do not promote

### 3. Why the docs/program stack is not first-wave promotion

The docs/program surfaces are valuable witness matter, but they are not clean
first-wave promotion material because:

- they are tied to the older production-root narrative,
- they predate the later packaged reintegration/orchestration center,
- and they contain mixed maturity, including at least one explicit stub.

So the right move is selective extraction of stable operator-facing value, not a
whole-tree docs import.

### 4. Why API/MCP promotion is real, not speculative

The read-only API/MCP layer is not just layout evidence.

It has explicit proof surfaces:

- API route tests
- API integration-style workflow test
- MCP server smoke tests
- preflight CLI tests
- template catalog tests
- genome manager tests
- host substrate tests

This makes Class B a real promotion candidate once the shell-root/content-root
startup rule is kept explicit and the later service packet is opened
deliberately.

## Retained witnesses and deferred matter

Retained witness matter:

- the full `docs/program/` stack
- older kernel bus/persistence wrappers
- generated build and egg-info artifacts

Deferred matter:

- actual code promotion into the packaged root
- API/MCP re-verification in the packaged root after promotion
- whether a future packaged `docs/` hub should exist as a first-class tree
- any broader documentation-program merger

## Confidence and unresolved contradictions

Confidence: **high** that the production-only packaging/API/MCP/preflight
surface is real and bounded enough to map.

Confidence: **high** that the retained top-level production transport shell is
real enough to keep as one bounded family rather than smuggling it into branch
startup piecemeal.

Confidence: **medium** on the long-term fate of the docs/program stack, because
some of it may still be useful as extracted operator reference after current
root authority stabilizes further.

Unresolved contradictions that must remain visible:

- top-level `ION/README.md` and `STATUS.md` still tell a materially older story
  than the packaged current-generation root
- the packaged root has later orchestration truth but lacks the production
  packaging/docs surface
- some production docs are operator-useful while still being tied to an older
  root narrative

## Required follow-up

1. Update the reintegration registries to reflect these promotion classes.
2. Keep q006 focused on packaged-root nested-path disambiguation.
3. Do not open q004 until both this map and q006 are explicit enough for a
   carrier-facing export bundle to reference.
4. Land selective Class C extraction before reopening any broader production
   service-surface packet.
5. Treat the top-level production external transport shell as a separate
   current-phase disposition decision rather than as an automatic next packet.
6. Leave Class D surfaces as witness material unless a later bounded packet
   justifies deeper extraction.
