# v2.6.1 Guest Mode Tool Gate Note

This package revision tightens `/guest-mode` behavior.

Observed issue: a Custom GPT starter run treated `/guest-mode` as a reason to
call MCP and then reported MCP/local runtime status as if that were the guest
mount.

Correct behavior:

- `/guest-mode` is a starter route, not an automatic tool call.
- Guest mode starts from mounted package or first-time starter context.
- Action Gateway and MCP are used only if the user asks for live
  connection/status, asks for a connector-backed draft, or provides relevant
  non-secret reentry/status proof.
- MCP health/status proves transport reachability only. It does not prove
  guest workspace mount, sign-in, accepted state, local execution authority, or
  production authority.

Expected first response shape:

```text
Guest mode is ready in local demo/read-only posture. I can help explore a
sample project, review uploaded context, or draft a bounded next step. What do
you want to work on?
```

The GPT should not dump Action/MCP status in this route unless the user asks
for diagnostics.
