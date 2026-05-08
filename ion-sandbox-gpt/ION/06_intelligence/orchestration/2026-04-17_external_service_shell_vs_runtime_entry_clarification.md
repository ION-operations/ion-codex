---
type: clarification
authority: A3_OPERATIONAL
created: 2026-04-17T00:00:00-04:00
status: ACTIVE
purpose: Clarify the relationship between top-level production external service shells and extracted-branch runtime-entry law
connections:
  - ION/02_architecture/API_RUNTIME_ENTRY_PROTOCOL.md
  - ION/02_architecture/EXTERNAL_EXECUTION_MCP_BRIDGE_PROTOCOL.md
  - ION/04_packages/kernel/api_runtime_entry.py
  - /home/sev/ION - Production/ION/04_packages/ion_api/main.py
  - /home/sev/ION - Production/ION/04_packages/ion_state_mcp/logic.py
  - /home/sev/ION - Production/ION/04_packages/ion_recon_mcp/logic.py
  - /home/sev/ION - Production/ION/04_packages/ion_evidence_mcp/logic.py
  - /home/sev/ION - Production/ION/04_packages/ion_state_mcp/server.py
  - /home/sev/ION - Production/ION/tests/test_ion_api.py
  - /home/sev/ION - Production/ION/tests/test_ion_api_integration.py
  - ION/tests/test_kernel_api_runtime_entry.py
  - ION/06_intelligence/decisions/2026-04-17_top_level_production_surface_promotion_map_canonicalization_decision.md
---

# External Service Shell vs Runtime Entry Clarification

## Purpose

This note closes one more scoping ambiguity inside q003:

- top-level production `ion_api` and `ion_*_mcp` are external transport shells
- extracted-branch `kernel.api_runtime_entry` is internal runtime/session-entry law

They are adjacent surfaces. They are not the same object and should not be
promoted or compared as if one replaces the other.

## What exists in top-level production

The top-level production root carries:

- `ion_api` as a FastAPI read-only HTTP control plane
- `ion_state_mcp`, `ion_recon_mcp`, `ion_evidence_mcp`, and `ion_policy_mcp`
  as FastMCP server shells
- helper modules such as `kernel.genome_manager`,
  `kernel.host_substrate`, and `kernel.template_catalog`

The tests show the intended posture clearly:

- `test_ion_api.py` and `test_ion_api_integration.py` exercise HTTP routes over
  kernel store / recon / host / genome / template helpers
- the MCP smoke tests only assert server construction, not broader authority
  collapse

The service shell is therefore:

- read-only in posture
- transport-bearing
- operator/support-facing
- built on top of already-existing kernel truth and helper logic

It is not the scheduler, not runtime/session authority itself, and not direct
activation law.

## What exists in the extracted branch

The extracted branch carries:

- `kernel.api_runtime_entry`
- `API_RUNTIME_ENTRY_PROTOCOL.md`
- tests in `ION/tests/test_kernel_api_runtime_entry.py`

That surface governs:

- how an external/API carrier may attach to an existing runtime/session center
- when a session may be created explicitly
- how entry receipts and carrier-boundary witnesses are emitted

It explicitly does **not** import a server stack.

So the extracted branch already has the lawful internal boundary for API
carriers, but it does not yet ship the top-level production transport shells.

## The correct relationship

The right mental model is:

1. runtime entry law decides how an external/API carrier may attach
2. external service shells are optional transport adapters that can sit on top
   of that lawful center or adjacent helper logic
3. neither HTTP nor MCP transport becomes kernel truth merely by existing

This matches the generic external bridge law already present in
`EXTERNAL_EXECUTION_MCP_BRIDGE_PROTOCOL.md`:

- external surfaces are subordinate to kernel truth
- service artifacts are not doctrine
- no authority collapse is allowed

## Consequence for q003

q003 should not describe the top-level production API/MCP surfaces as if they
were the branch's missing runtime-entry core.

The actual promotion candidate, if chosen later, is:

- an **external read-only service shell / transport adjunct packet**

That packet would include:

- top-level production `ion_api`
- the `ion_*_mcp` packages
- the helper modules they depend on
- any coupled packaging / preflight / dependency declarations needed to run
  them honestly

It would not be described as:

- the first missing packaging floor
- the runtime/session center itself
- or the branch's missing API-entry law

## What should happen next

If this surface is promoted later, it should be framed as an optional external
service/transport packet over already-existing kernel truth.

If it is not promoted yet, that does not mean the extracted branch lacks API
boundary law. It only means it lacks the top-level production HTTP/MCP shell.

## Final judgment

The extracted branch already owns the internal runtime-entry center.

Top-level production owns a separate read-only transport shell family.

The next execution phase must keep those two truths distinct.
