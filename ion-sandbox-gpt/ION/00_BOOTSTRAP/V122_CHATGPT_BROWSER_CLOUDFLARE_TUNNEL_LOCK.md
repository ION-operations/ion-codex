# V122 ChatGPT Browser Cloudflare Tunnel Lock

## Locked Objective

Add an ION-native Cloudflare Tunnel bridge for the V121 local HTTP MCP preview.

## Authority Boundary

```yaml
production_authority: false
live_execution_authority: false
deployment_authority: false
```

## Current Law

The tunnel may expose only the bounded ION `/mcp` connector surface. It may not
expose arbitrary shell, file writes, credentials, provider calls, browser
control, direct deletes, git push, or unbounded filesystem access.

## Current Connector URL Shape

```text
https://<cloudflare-host>/mcp
```

The older `/sse` tunnel pattern is historical only for this branch.
