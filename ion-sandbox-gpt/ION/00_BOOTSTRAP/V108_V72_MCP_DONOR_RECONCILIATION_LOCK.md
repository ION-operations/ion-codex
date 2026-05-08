# V108 V72 MCP Donor Reconciliation Lock

```yaml
lock_id: V108_V72_MCP_DONOR_RECONCILIATION_LOCK
version_line: V108_V72_MCP_DONOR_RECONCILIATION
created_at: 2026-05-02
authority_class: bounded_donor_reconciliation
production_authority: false
live_execution_authority: false
previous_trunk: V107_NO_SILENT_DELETION_AND_TRUNK_PRESERVATION_GATE
donor_branch: ION_MASTER_CURRENT_3_V72_HOSTED_MCP_BUNDLE_IMPORT_EXPORT_AND_REPLAY_ALPHA_20260426
```

## Lock

V108 restores the V72 MCP substrate as a bounded donor import. It does not revert the trunk to V72, does not crown V72 as current authority, and does not import old V72 runtime-session receipts into hot state.

The current trunk remains the V107 safe-preservation line plus the Codex V106 lifecycle/telemetry work. V72 is used only as a donor for MCP protocol, registry, kernel, tests, documentation, and example client configuration surfaces.

## Preserved current authority

The following current-trunk MCP control bridge remains authoritative for the Cursor-facing control path:

```text
.cursor/mcp.json
ION/09_integrations/mcp/ion_mcp_server.py
ION/04_packages/kernel/ion_mcp_bridge_audit.py
ION/tests/test_kernel_ion_mcp_bridge_audit.py
```

## Restored donor capability families

```text
local MCP bridge
MCP mount/front-door session protocol
MCP client configuration generation
MCP client certification
MCP transport preview
optional SDK wrapper boundary
hosted auth/account/workspace alpha boundary
hosted OAuth/streamable HTTP preview lineage
hosted storage receipt ledger alpha lineage
hosted bundle import/export/replay alpha lineage
```

## Excluded from hot trunk

```text
ION/05_context/runtime_state/v64_local_mcp_bridge/
```

Those old runtime-session receipts are forensic history, not current hot state.

## Required proof

```text
1. V72 donor surfaces present.
2. V105/V107 Cursor MCP bridge preserved.
3. Old V72 runtime-state receipts absent from hot trunk.
4. Focused MCP tests pass.
5. Trunk preservation gate reports no unexpected/protected removals.
```
