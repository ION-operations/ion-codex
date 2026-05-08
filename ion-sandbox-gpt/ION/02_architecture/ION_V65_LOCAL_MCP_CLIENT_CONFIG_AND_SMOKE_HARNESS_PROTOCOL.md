# ION V65 Local MCP Client Configuration and Smoke Harness Protocol

## Branch

`V65_LOCAL_MCP_CLIENT_CONFIG_AND_SMOKE_HARNESS`

## Status

Protocol + kernel utility branch. V65 does not grant live execution authority.

## Purpose

V64 proved that ION can expose a local MCP-facing bridge over the governed kernel/session/receipt/operator-approval surfaces. V65 makes that bridge usable by agents and IDE clients by adding:

1. a local stdio smoke harness that mounts ION as an external process;
2. client configuration profile generators for Cursor-style, VS Code-style, Codex-style, and generic stdio clients;
3. explicit installation/use guidance for the local founder bridge;
4. test invariants proving live execution remains refused.

## Governing principle

The local MCP bridge is an agent socket, not an authority center.

An external AI client may connect, initialize, list tools, mount ION, read the boot packet/status/horizon, plan dry-run work, submit dry-run queue items, preview daemon dry-run steps, and receive refusal receipts for live paths.

An external AI client may not gain direct execution authority merely by connecting through MCP.

## V65 allowed result classes

Every MCP-facing bridge result must resolve to one of:

- `READ_ONLY`
- `DRY_RUN`
- `APPROVAL_REQUIRED`
- `REFUSED`

No V65 path may resolve to:

- `LIVE_EXECUTED`

## Required first-call lifecycle

A local client should perform this sequence:

```text
initialize
tools/list
tools/call ion.mount
tools/call ion.status
tools/call ion.boot_packet
tools/call ion.horizon.current
tools/call ion.approvals.list
```

Only after this sequence may the client request:

```text
tools/call ion.job.plan
tools/call ion.job.submit_dry_run
tools/call ion.daemon.dry_run_step
tools/call ion.bundle.export_preview
```

## Refused tool classes

The V65 bridge must refuse:

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

## External-process proof

The smoke harness must prove that an external process can:

1. start the local bridge through stdio;
2. receive `initialize`;
3. list bounded bridge tools;
4. call `ion.mount`;
5. call `ion.status`;
6. call `ion.job.plan`;
7. call `ion.job.submit_dry_run`;
8. call `ion.job.execute_live` and receive `REFUSED`;
9. complete without seeing `LIVE_EXECUTED`, live authorization, or kernel-truth mutation.

## Client profile law

Generated client profiles are examples only until client-specific certification is performed. The profile generator may output configuration templates for local stdio use, but must not install them into user applications automatically.

The profiles must point at:

```text
python -m kernel.ion_mcp_local_bridge --ion-root <ION_ROOT> --stdio
```

with:

```text
PYTHONPATH=<ION_ROOT>/04_packages
```

## Non-goals

V65 does not implement:

- hosted remote MCP;
- OAuth;
- account/workspace cloud tenancy;
- Kubernetes;
- live execution;
- shell execution;
- browser mutation;
- provider/model dispatch;
- credential access;
- direct governed-write authority.

## Promotion gate

V65 may promote only if:

1. local bridge tests pass;
2. smoke harness reports `passed: true`;
3. client profiles generate successfully;
4. live execution remains refused;
5. kernel truth mutation remains false for all smoke calls.

