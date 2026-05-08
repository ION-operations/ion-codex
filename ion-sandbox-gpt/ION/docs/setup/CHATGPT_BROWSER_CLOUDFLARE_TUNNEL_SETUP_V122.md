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

Local human/app landing:

```text
http://127.0.0.1:8765/
http://127.0.0.1:8765/app
```

The landing page is a safe status/UI projection. ChatGPT connector setup still
uses `/mcp`, not `/` or `/app`.

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

The tunnel root can be opened in a browser to see the ION connector landing page:

```text
https://<cloudflare-host>/
```

## ChatGPT Connector Setup

In ChatGPT developer mode, create a connector using the public URL:

```text
https://<cloudflare-host>/mcp
```

Do not use the older AIMOS `/sse` endpoint pattern for this V122 connector.

## Stable Hostname / Named Tunnel Path

The free `trycloudflare.com` quick tunnel is a development path. For a durable
ChatGPT connector URL, use a Cloudflare named tunnel and stable hostname such as
an ION/Helixion-owned subdomain.

Host setup happens outside ION source control:

```bash
cloudflared tunnel login
cloudflared tunnel create ion-browser
cloudflared tunnel route dns ion-browser ion.helixion.net
```

Do not commit Cloudflare credentials, tunnel tokens, or origin certificates.

Once host credentials exist, start the ION tunnel runner against the stable
hostname:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages \
python3 -S -m kernel.ion_chatgpt_browser_cloudflare_tunnel \
  --ion-root . \
  --start \
  --port 8765 \
  --tunnel-name ion-browser \
  --stable-hostname ion.helixion.net
```

Expected public surfaces:

```text
https://ion.helixion.net/      ION connector landing/app page
https://ion.helixion.net/app   same app surface
https://ion.helixion.net/mcp   ChatGPT connector MCP endpoint
```

If reusing an older AIMOS/Helixion hostname, verify that it routes to the current
ION local preview on port `8765` and endpoint `/mcp`. Do not carry forward old
`/sse` or port `8000` assumptions.

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
