# ION V66 Local MCP Client Certification Protocol

## Status

Branch: `V66_LOCAL_MCP_SDK_COMPATIBILITY_AND_CLIENT_CERTIFICATION`

Authority: protocol and contract-certification branch only.

This protocol certifies ION's local MCP bridge as a bounded client-facing socket for local MCP-capable environments. It does not certify hosted MCP, OAuth, ChatGPT app deployment, live execution, browser mutation, provider dispatch, or direct governed-write authority.

## Core law

MCP client certification proves that an external agent host can see the correct ION bridge contract. It does not grant the host authority to execute ION.

Every certified V66 client profile must preserve the V64/V65 resolution set:

- `READ_ONLY`
- `DRY_RUN`
- `APPROVAL_REQUIRED`
- `REFUSED`

No V66 result may resolve as `LIVE_EXECUTED`.

## Certification scope

V66 certifies contract-level compatibility for:

- generic stdio MCP client profile;
- Cursor-style local stdio profile;
- VS Code-style local stdio profile;
- Codex-style local stdio profile.

This is not a claim that those external products were live-launched in this branch. The certification is ION-owned and checks that the generated configuration examples, tool descriptors, dry-run behavior, and refusal behavior form a stable contract for those clients.

## Required client contract

A certified local client must be able to discover or invoke the following baseline tools:

- `ion.mount`
- `ion.status`
- `ion.boot_packet`
- `ion.horizon.current`
- `ion.receipts.list`
- `ion.approvals.list`
- `ion.job.plan`
- `ion.job.submit_dry_run`
- `ion.daemon.dry_run_step`
- `ion.bundle.export_preview`

A certified local client must not see live tools as exposed bridge tools:

- `ion.execute`
- `ion.job.execute_live`
- `ion.daemon.run`
- `ion.daemon.loop`
- `ion.shell.run`
- `ion.browser.mutate`
- `ion.provider.dispatch`
- `ion.secrets.read`
- `ion.secrets.write`
- `ion.governed_write.direct`

If a client invokes a forbidden tool name anyway, ION must return `REFUSED` and emit a refusal receipt.

## Required certification sequence

For each profile, V66 certification performs the following sequence:

1. Validate the bridge tool surface.
2. Validate that the profile's example configuration exists and points at the local bridge.
3. Mount ION through `ion.mount` in dry-run mode.
4. Run `ion.job.plan` and require `DRY_RUN`.
5. Run `ion.job.submit_dry_run` and require `APPROVAL_REQUIRED`.
6. Attempt `ion.job.execute_live` and require `REFUSED`.
7. Fail certification if any result mutates kernel truth or authorizes live execution.

## Relationship to V63-V65

V63 defines the MCP mount/session and account/state-root doctrine.

V64 implements the first local MCP bridge to ION's kernel/session/receipt/approval surfaces.

V65 adds client configuration examples and an external-process stdio smoke harness.

V66 certifies that the local bridge contract is stable enough to be used by local MCP-capable clients as an agent-facing socket.

## Non-goals

V66 does not implement:

- official SDK replacement;
- remote Streamable HTTP server;
- OAuth login;
- hosted account workspace system;
- cloud worker plane;
- Kubernetes deployment;
- live execution;
- browser mutation;
- provider API dispatch;
- credential vault access.

These are future hosted/productization branches.
