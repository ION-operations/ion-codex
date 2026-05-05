# ChatGPT Browser Cloudflare Tunnel Setup V122

## Current Verdict

V121 created the local HTTP MCP preview. V122 adds the Cloudflare Tunnel layer
needed for ChatGPT browser to reach that local `/mcp` endpoint through HTTPS.

This is still a development connector path:

```yaml
production_authority: false
live_execution_authority: false
deployment_authority: false
```

## Prerequisite

Install `cloudflared` and make sure it is on `PATH`.

ION does not auto-install it because package installation is host-level setup,
not an ION runtime mutation.

## Terminal 1: Start Local ION MCP Preview

From the ION shell root:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_chatgpt_browser_mcp_http_preview --ion-root . --host 127.0.0.1 --port 8765 --serve
```

Local MCP endpoint:

```text
http://127.0.0.1:8765/mcp
```

## Terminal 2: Start Cloudflare Tunnel

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_chatgpt_browser_cloudflare_tunnel --ion-root . --start --port 8765
```

When Cloudflare emits a `trycloudflare.com` URL, ION writes:

```text
ION/05_context/current/ACTIVE_CHATGPT_BROWSER_CLOUDFLARE_TUNNEL.json
```

Use the `connector_url` field in ChatGPT connector setup. It should end in:

```text
/mcp
```

## ChatGPT Connector Setup

In ChatGPT developer mode, create a connector using the public URL:

```text
https://<cloudflare-host>/mcp
```

Do not use the older AIMOS `/sse` endpoint pattern for this V122 connector.

## Audit

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_chatgpt_browser_cloudflare_tunnel --ion-root . --write --json
```

Possible states:

```text
ION_CHATGPT_BROWSER_CLOUDFLARE_TUNNEL_READY
ION_CHATGPT_BROWSER_CLOUDFLARE_TUNNEL_SETUP_REQUIRED
ION_CHATGPT_BROWSER_CLOUDFLARE_TUNNEL_BLOCKED
```

`SETUP_REQUIRED` is expected when `cloudflared` is not installed or no tunnel is
currently running.
