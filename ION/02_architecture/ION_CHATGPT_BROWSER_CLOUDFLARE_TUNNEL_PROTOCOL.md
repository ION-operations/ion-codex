# ION ChatGPT Browser Cloudflare Tunnel Protocol

## Status

```yaml
version_line: V122_CHATGPT_BROWSER_CLOUDFLARE_TUNNEL
production_authority: false
live_execution_authority: false
deployment_authority: false
```

## Purpose

V122 connects the V121 local HTTP MCP preview to the ChatGPT browser connector
path through Cloudflare Tunnel.

The tunnel is not ION identity and does not grant machine control. It only
publishes the already bounded ION `/mcp` connector surface over HTTPS so
ChatGPT browser developer-mode connectors can reach it.

## Current Path

```text
ChatGPT browser
-> HTTPS Cloudflare Tunnel URL
-> local V121 HTTP MCP preview /mcp
-> V120 bounded ChatGPT browser connector contract
-> ION kernel read/status or bounded queue/receipt operations
```

## Corrected Tunnel Target

The older AIMOS tunnel script used an SSE endpoint. V122 does not preserve that
as current ION connector authority.

Current target:

```text
https://<cloudflare-host>/mcp
```

Local service target:

```text
http://127.0.0.1:8765
```

## Required Boundaries

The tunnel must not expose:

```text
arbitrary shell
arbitrary file write
direct delete
git push
credential access
browser/computer control
provider API calls
unbounded local filesystem access
direct acceptance of unproofed worker output
production deployment authority
```

The V121 write confirmation gate remains active:

```text
ION_BOUNDED_WRITE_CONFIRMED
```

## Status Evidence

Tunnel runtime state is written to:

```text
ION/05_context/current/ACTIVE_CHATGPT_BROWSER_CLOUDFLARE_TUNNEL.json
```

V122 audit state is written to:

```text
ION/05_context/current/CHATGPT_BROWSER_CLOUDFLARE_TUNNEL_V122.json
```

These are evidence surfaces. They do not create production or live execution
authority.
