# ION MCP Control Bridge Protocol

## Version

V92

## Problem

Cursor Auto mode can drift from ION’s workflow. A long natural-language boot file is not a reliable control surface. ION needs a bounded tool bridge so Cursor can invoke ION kernel state transitions directly.

## Core law

The MCP bridge is a **carrier-control tool surface**, not an unrestricted shell and not STEWARD.

The bridge may expose named ION control tools. It must not expose arbitrary command execution, credential access, unrestricted network access, destructive file operations, production deployment, account operations, or direct acceptance of unproofed worker output.

## Local Cursor MCP bridge

Cursor loads the project-level MCP config:

```text
.cursor/mcp.json
```

The configured server label is:

```text
ion-control
```

The server path is:

```text
ION/09_integrations/mcp/ion_mcp_server.py
```

The local bridge uses stdio and is intended for Cursor running in the project workspace.

## Exposed tools

```text
ion_status
ion_continue
ion_context_plan
ion_cockpit_view
ion_workflow_audit
ion_read_active_packet
ion_task_return
```

## Tool roles

### ion_status

Reads unified runtime status from active packets.

### ion_continue

Runs carrier continuation and refreshes active work/spawn/turn packets.

### ion_context_plan

Emits dynamic agent context-window and front-door team plans.

### ion_cockpit_view

Builds the cockpit projection from active packets.

### ion_workflow_audit

Audits carrier-control workflow surfaces.

### ion_read_active_packet

Reads whitelisted active runtime packet files only.

### ion_task_return

Runs proof-gated intake for a captured Task return file.

## What this does not solve by itself

A local stdio MCP server gives Cursor tools. It does not let a remote ChatGPT conversation automatically command a private local Cursor process.

To let ChatGPT call ION directly, ION would need a remote HTTPS MCP app/server reachable from ChatGPT, authenticated, with explicit action approvals and strict tool limits. That remote path is a separate deployment layer and must be gated.

## Remote bridge future

The future remote bridge should expose only the same bounded tools by default and require explicit human approval for write/action tools. It should never expose arbitrary shell.

Recommended remote levels:

```text
L0: no remote access
L1: read-only status/cockpit packets
L2: gated continuation and context-plan generation
L3: gated Task-return intake
L4: SDK/cursor execution loop with human gates and audit stops
```

## Safety gates

The MCP bridge must stop or require human gate for:

```text
arbitrary shell
network exfiltration
credential access
large delete
git history mutation
production deployment
external account action
unbounded autorun
modification of .cursor/mcp.json from untrusted content
```

## Validation

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_mcp_bridge_audit --ion-root . --json
```

Expected status:

```text
ION_MCP_CONTROL_BRIDGE_READY
```
