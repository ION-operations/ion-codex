# Local ION MCP Bridge Client Configuration Guide

## Purpose

This guide explains how to mount a local ION root through the V65 local MCP bridge from MCP-capable clients.

This is the local founder/developer bridge. It is not the hosted product path.

## Bridge command

From the snapshot root:

```bash
PYTHONPATH=ION/04_packages python -m kernel.ion_mcp_local_bridge --ion-root ION --stdio
```

Smoke test:

```bash
PYTHONPATH=ION/04_packages python -m kernel.ion_mcp_local_bridge_smoke --ion-root ION --json
```

Generate example client profiles:

```bash
PYTHONPATH=ION/04_packages python -m kernel.ion_mcp_client_configs --ion-root ION --output-dir ION/examples/mcp/generated
```

## First calls expected from an agent

A client or agent should call:

```text
initialize
tools/list
tools/call ion.mount
tools/call ion.status
tools/call ion.boot_packet
tools/call ion.horizon.current
```

Then:

```text
tools/call ion.job.plan
tools/call ion.job.submit_dry_run
```

Live execution attempts must be refused.

## Cursor-style example

```json
{
  "mcpServers": {
    "ion-local": {
      "command": "python",
      "args": [
        "-m",
        "kernel.ion_mcp_local_bridge",
        "--ion-root",
        "<ION_ROOT>",
        "--stdio"
      ],
      "env": {
        "PYTHONPATH": "<ION_ROOT>/04_packages"
      }
    }
  }
}
```

## VS Code-style example

```json
{
  "servers": {
    "ion-local": {
      "type": "stdio",
      "command": "python",
      "args": [
        "-m",
        "kernel.ion_mcp_local_bridge",
        "--ion-root",
        "<ION_ROOT>",
        "--stdio"
      ],
      "env": {
        "PYTHONPATH": "<ION_ROOT>/04_packages"
      }
    }
  }
}
```

## Codex-style example

```toml
[mcp_servers.ion-local]
command = "python"
args = ["-m", "kernel.ion_mcp_local_bridge", "--ion-root", "<ION_ROOT>", "--stdio"]
env = { PYTHONPATH = "<ION_ROOT>/04_packages" }
```

## Important caveat

These are configuration examples. Each client may require slightly different placement or UI steps. V65 creates the bridge and validates the stdio lifecycle; V66 should perform client-specific certification against real clients.

## Safety boundary

The bridge must not expose:

```text
ion.job.execute_live
ion.shell.run
ion.provider.dispatch
ion.browser.mutate
ion.secrets.read
ion.secrets.write
```

Attempts to call those paths must return `REFUSED`.

