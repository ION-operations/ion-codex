# ION Cursor Work Cycle Packet

```yaml
schema_id: ion.cursor_work_cycle_packet.v1
status: active_template
production_authority: false
carrier_authority: bounded
```

## Purpose

This packet is the default carrier work-cycle template for a Cursor-hosted ION pass. It is not a role prompt and it is not authority by itself. It is the work contract that prevents the carrier from improvising the workflow.

## Required carrier posture

The carrier must:

1. mount the repository from the shell root where `pyproject.toml` and `ION/REPO_AUTHORITY.md` coexist;
2. inspect the active work packet, cockpit view model, human gate queue, role spawn plan, and relevant context-system surfaces;
3. perform only work inside the allowed paths or explicitly report why a path expansion is required;
4. produce context proof and template/action proof for any return that claims integration;
5. run the focused tests relevant to the changed surfaces;
6. return one consolidated project zip when packaging is requested.

## Required work-cycle sections

Every substantial carrier work cycle should resolve the following fields:

```yaml
cycle_id:
objective:
true_north:
current_gate:
allowed_paths:
context_loaded:
changes_made:
tests_run:
receipts_written:
open_blockers:
next_lawful_move:
production_authority: false
```

## Stop conditions

The carrier must stop or downgrade to report-only when:

- a human gate blocks continuation;
- a required authority surface is missing;
- an action would delete, archive, compress, or move evidence without explicit lifecycle authority;
- external worker/MCP/API execution would bypass context proof, template/action proof, or Steward integration;
- the repository root invariant is not satisfied.

## Evidence contract

A completed work cycle must leave enough residue for the next carrier to resume without reconstructing the work from chat. The minimum residue is:

```text
- active state update or explicit no-state-change receipt
- audit/report document when the work changes doctrine or planning
- focused test result or explicit untested boundary
- updated FILES_ADDED marker when files are added
- full consolidated zip when requested by the operator
```
