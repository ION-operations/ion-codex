# ION V124 Legacy Cloudflare Tunnel Reuse Report

## Verdict

```yaml
line: V124_LEGACY_CLOUDFLARE_TUNNEL_REUSE
verdict: ION_CHATGPT_BROWSER_LEGACY_TUNNEL_REUSE_SETUP_REQUIRED
accepted: true
cloudflared_found: false
production_authority: false
live_execution_authority: false
deployment_authority: false
```

`SETUP_REQUIRED` means the host does not currently expose `cloudflared` on
`PATH`. It does not mean the connector design is blocked.

## Finding

The old AIMOS tunnel system should be reused only as Cloudflare quick-tunnel
donor evidence.

Reusable donor pattern:

```text
cloudflared tunnel --url http://localhost:<port>
trycloudflare.com public URL extraction
status JSON recording
```

Forbidden current carry-forward:

```text
AIMOS identity
legacy /sse endpoint
legacy data/mcp status path
legacy port 8000 assumption
host-level auto-install behavior
```

## Donor Evidence

V124 found both legacy tunnel donor scripts:

```text
/home/sev/AIM-OS/scripts/cloudflare_tunnel.py
/home/sev/ION - Production/AIM-ION/scripts/cloudflare_tunnel.py
```

Both scripts have the same SHA-256:

```text
aa441fb95a2ef0fa749e3b5dfd25f33ddd5088ddd308c96b51a9b22ddefeb0d3
```

The donor scripts contain reusable Cloudflare quick-tunnel patterns and legacy
patterns now classified as donor-only.

## Current ION Connector Shape

Current ION connector URL shape:

```text
https://<cloudflare-host>/mcp
```

Current local preview:

```text
http://127.0.0.1:8765/mcp
```

Cloudflare target:

```text
http://127.0.0.1:8765
```

The old `/sse` endpoint is forbidden for the current ChatGPT browser connector.

## Added Enforcement

V124 adds:

```text
ION/00_BOOTSTRAP/V124_LEGACY_CLOUDFLARE_TUNNEL_REUSE_LOCK.md
ION/02_architecture/ION_LEGACY_CLOUDFLARE_TUNNEL_REUSE_PROTOCOL.md
ION/04_packages/kernel/ion_chatgpt_browser_legacy_tunnel_reuse_audit.py
ION/docs/setup/CHATGPT_BROWSER_LEGACY_CLOUDFLARE_TUNNEL_REUSE_V124.md
ION/tests/test_kernel_ion_chatgpt_browser_legacy_tunnel_reuse_audit.py
ION/05_context/current/CHATGPT_BROWSER_LEGACY_TUNNEL_REUSE_AUDIT_V124.json
```

## Validation

Focused V120-V124 connector validation:

```text
25 passed
```

Full kernel validation:

```text
168 passed
```

The audit blocks any current tunnel module that carries `/sse` forward and
keeps the current tunnel surface on `/mcp`.

## Next Lawful Move

Install or expose `cloudflared`, then run the V122 tunnel command while the
V121 local HTTP MCP preview is serving.

Do not restore the old AIMOS MCP server or `/sse` endpoint as current ION
authority.
