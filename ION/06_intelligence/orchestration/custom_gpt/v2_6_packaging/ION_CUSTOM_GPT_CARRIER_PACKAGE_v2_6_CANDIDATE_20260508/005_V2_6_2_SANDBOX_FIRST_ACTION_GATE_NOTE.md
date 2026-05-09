# v2.6.2 Sandbox-First Action Gate Note

This revision tightens the Custom GPT default route.

Observed issue: even after being told to use instructions and files, the GPT
attempted to use MCP/local ION instead of operating from the uploaded sandbox
package.

Correct behavior:

- The default Custom GPT lane is uploaded package/sandbox context.
- Action Gateway and MCP are explicit-use connector surfaces.
- Tool visibility is not permission to call tools.
- `Inspect available sources` means inspect mounted/visible sources first; it
  does not mean call Action Gateway or MCP.
- Connector returns outrank sandbox files only inside an explicit connector-lane
  request.
- Requests such as `use your files`, `use your instructions`, `use the sandbox`,
  `use the package`, `/guest-mode`, `/what is ION?`, first-time context, and
  ordinary ION work are negative triggers for Action/MCP.

Action/MCP may be used only when the user explicitly asks for live connector,
local hub, MCP, gateway, queue, receipt, tool-list, validation, submit, or other
connector-backed behavior.

Expected first response for ordinary sandbox boot:

```text
ION sandbox context is mounted. What project, idea, codebase, document, or
workflow should we work on?
```

No MCP/local runtime status should be reported unless the user asked for live
diagnostics.
