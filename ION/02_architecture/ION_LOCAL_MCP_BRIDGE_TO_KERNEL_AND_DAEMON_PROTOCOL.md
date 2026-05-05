# ION Local MCP Bridge to Kernel and Supervised Daemon Protocol

**Branch:** V64_LOCAL_MCP_BRIDGE_TO_ION_KERNEL_AND_SUPERVISED_DAEMON  
**Authority class:** architecture protocol / execution-boundary law  
**Status:** local-founder bridge prototype protocol  
**Supersedes:** none  
**Depends on:** V62 operator approval queue, V63 MCP mount/account protocolization

## 1. Purpose

V64 creates the first practical local bridge by which an MCP-capable agent may mount ION and use ION's existing kernel/session/receipt surfaces. The bridge exists to prove the product path before cloud hosting or live execution.

The bridge is not an execution authority. It is a socket into ION's governed surfaces.

## 2. Binding law

The V64 bridge may expose:

- mount/session creation through ION's runtime session store;
- status, boot, horizon, receipt, approval, and tool-list projections;
- dry-run job planning;
- dry-run queue submission;
- supervised daemon-step preview;
- bundle-export preview.

The V64 bridge must not expose:

- direct shell execution;
- direct governed-write mutation;
- browser/session mutation;
- provider/model dispatch;
- credential access;
- canonical graph writes;
- daemon-loop autonomy;
- live execution.

Every V64 MCP-facing result must resolve to one of:

```text
READ_ONLY
DRY_RUN
APPROVAL_REQUIRED
REFUSED
```

No V64 result may resolve to `LIVE_EXECUTED`.

## 3. Correct local bridge topology

```text
MCP-capable agent / IDE / local test harness
        ↓
ION local MCP bridge
        ↓
RuntimeSessionStore + ApiRuntimeEntryGateway + receipts
        ↓
V62 operator approval queue projection
        ↓
dry-run queue item / daemon-step preview
```

The daemon remains subordinate to ION kernel/session law. A daemon dry-run step is a projected candidate, not a running daemon loop.

## 4. Implemented kernel surface

```text
ION/04_packages/kernel/ion_mcp_local_bridge.py
ION/tests/test_kernel_ion_mcp_local_bridge.py
```

The module supplies:

- `IonMcpLocalBridge`
- `IonMcpMountRequest`
- `IonMcpMountedSession`
- `IonMcpToolResult`
- `handle_jsonrpc_message`
- `run_stdio_server`

The stdio handler implements a minimal JSON-RPC surface for local experimentation:

- `initialize`
- `notifications/initialized`
- `tools/list`
- `tools/call`

This is intentionally no-dependency. It is suitable as a local shim or SDK wrapping target, not as a final hosted MCP service.

## 5. Tool surface

Read-only:

```text
ion.mount
ion.status
ion.boot_packet
ion.horizon.current
ion.receipts.list
ion.approvals.list
ion.tools.list
```

Dry-run / approval-required:

```text
ion.job.plan
ion.job.submit_dry_run
ion.daemon.dry_run_step
ion.bundle.export_preview
```

Forbidden live tools include:

```text
ion.execute
ion.job.execute_live
ion.daemon.run
ion.daemon.loop
ion.shell.run
ion.browser.mutate
ion.provider.dispatch
ion.secrets.read
ion.secrets.write
ion.governed_write.direct
```

## 6. Operator approval invariant

A dry-run queue item may be produced by the MCP bridge, but it must remain in the runtime session queue and must be surfaced to the operator approval queue before any later execution branch.

V64 may project daemon-service intent but must not start the daemon loop.

## 7. Product significance

This branch converts ION from ZIP-only continuity into a local mountable continuity engine. The ZIP remains the carrier/export format. MCP becomes the local access membrane.

This is the first branch where external agents can begin to use ION through a standard-shaped interface without receiving raw execution authority.
