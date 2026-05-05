# ION Legacy Cloudflare Tunnel Reuse Protocol

## Status

```yaml
version_line: V124_LEGACY_CLOUDFLARE_TUNNEL_REUSE
production_authority: false
live_execution_authority: false
deployment_authority: false
```

## Purpose

This protocol governs how ION may reuse the older Cloudflare tunnel system that
previously served AIMOS MCP access from ChatGPT browser.

The reuse target is transport only. The old system does not become current ION
authority.

## Donor Classification

Historical donor scripts may prove these reusable patterns:

```text
cloudflared tunnel --url <local-http-service>
trycloudflare.com public URL extraction
status JSON capture for operator visibility
```

Historical donor scripts may also contain stale patterns. These must be
classified as donor-only and blocked from current surfaces:

```text
AIMOS or AIM-OS identity
/sse endpoint
data/mcp status path
legacy port 8000 assumption
host-level install automation
```

## Current ION Connector Path

Current path:

```text
ChatGPT browser connector
-> https://<cloudflare-host>/mcp
-> Cloudflare Tunnel
-> http://127.0.0.1:8765
-> V121 local HTTP MCP preview /mcp
-> V120 bounded ChatGPT browser connector contract
-> ION status/read and bounded queue/receipt tools
```

The public connector URL must end with:

```text
/mcp
```

The older `/sse` endpoint is forbidden for the current ChatGPT browser
connector.

## Host Setup Boundary

ION may audit whether `cloudflared` is present and may run it when explicitly
requested by the operator through the V122 tunnel command.

ION must not auto-install `cloudflared` as a runtime mutation. If `cloudflared`
is missing, the correct state is setup-required, not a failed connector design.

## Required Audit

V124 requires an audit proving:

```text
old donor scripts were found or reported missing
usable cloudflared quick-tunnel pattern was found
legacy /sse and AIMOS patterns are classified as donor-only
current tunnel module uses /mcp
current tunnel module excludes /sse
current tunnel module records non-authority status fields
production/live/deployment authority remain false
```

Audit module:

```text
ION/04_packages/kernel/ion_chatgpt_browser_legacy_tunnel_reuse_audit.py
```

Audit report:

```text
ION/05_context/current/CHATGPT_BROWSER_LEGACY_TUNNEL_REUSE_AUDIT_V124.json
```
