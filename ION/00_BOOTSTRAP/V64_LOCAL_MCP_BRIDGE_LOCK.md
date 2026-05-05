# V64 Local MCP Bridge Lock

**Branch:** V64_LOCAL_MCP_BRIDGE_TO_ION_KERNEL_AND_SUPERVISED_DAEMON  
**Date:** 2026-04-26  
**Authority:** branch lock / execution-boundary checkpoint

## Locked purpose

V64 implements the first local MCP-facing bridge into ION's kernel/session/receipt/approval surfaces.

## Locked invariant

The local bridge may mount, inspect, plan, queue dry-run work, and preview daemon steps. It may not execute live work.

Every exposed tool must resolve to:

```text
READ_ONLY
DRY_RUN
APPROVAL_REQUIRED
REFUSED
```

Never:

```text
LIVE_EXECUTED
```

## Required implementation surfaces

```text
ION/04_packages/kernel/ion_mcp_local_bridge.py
ION/tests/test_kernel_ion_mcp_local_bridge.py
ION/02_architecture/ION_LOCAL_MCP_BRIDGE_TO_KERNEL_AND_DAEMON_PROTOCOL.md
ION/02_architecture/ION_V64_LOCAL_MCP_BRIDGE_EXECUTION_HORIZON_PROTOCOL.md
ION/03_registry/ion_mcp_local_bridge_tool_policy.yaml
```

## Handoff rule

A future branch may wrap this bridge in a production MCP SDK or hosted transport only after the V64 invariant tests pass.
