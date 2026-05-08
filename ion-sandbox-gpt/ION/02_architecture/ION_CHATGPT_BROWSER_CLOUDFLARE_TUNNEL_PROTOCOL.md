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

## Human Landing / App Root

The local HTTP preview now has two separate public surfaces:

```text
GET  /      human-facing ION connector landing page
GET  /app   same bounded landing/app surface
POST /mcp   MCP JSON-RPC tool endpoint for ChatGPT connector configuration
GET  /health JSON status/audit evidence
```

The root/app page is intentionally a safe projection surface. It may show
connector posture, allowed tool names, blocked capability classes, and authority
flags. It must not expose secrets, local credential paths, arbitrary file
contents, shell controls, or direct state mutation controls.

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

## Stable Hostname Target

The `trycloudflare.com` quick tunnel is a development fallback. It is useful for
zero-configuration testing, but it is not the desired steady-state connector
address because the public hostname can change whenever the tunnel restarts.

The correct durable shape is a named Cloudflare tunnel or equivalent stable
hostname:

```text
https://<stable-ion-hostname>/mcp
```

The stable hostname must route to the same local preview root:

```text
http://127.0.0.1:8765
```

If an older Helixion or AIMOS domain is reused, only the transport/DNS ownership
may be reused. The old `/sse` endpoint, old local port `8000`, and AIMOS service
identity do not become current ION connector authority.

Example bounded named-tunnel launch shape:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages \
python3 -S -m kernel.ion_chatgpt_browser_cloudflare_tunnel \
  --ion-root . \
  --start \
  --port 8765 \
  --tunnel-name ion-browser \
  --stable-hostname ion.helixion.net
```

Before that can work, the host must already have Cloudflare named-tunnel
credentials/configuration outside the repo. ION must not store tunnel tokens,
origin certificates, or Cloudflare account secrets in source control.

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
