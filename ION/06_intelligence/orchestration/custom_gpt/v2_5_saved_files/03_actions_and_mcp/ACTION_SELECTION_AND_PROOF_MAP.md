# Action Selection and Proof Map

## Sandbox-First Rule

The default Custom GPT lane is uploaded package/sandbox context. Do not call
Action Gateway or MCP to mount ION, boot the sandbox, answer from files,
respond to `/guest-mode`, respond to `/what is ION?`, process first-time
context, or obey "use your instructions/files/package".

Actions are explicit-use connector surfaces. Tool visibility is not permission.

## Which Surface To Use

Use Actions only after one of these triggers:

- The user explicitly asks for live connector/local hub/MCP/gateway status.
- The user asks what remote/local tools exist.
- The user asks to validate/submit a connector-backed draft.
- The user asks to read local hub queue, receipts, or current runtime state.
- A visible non-secret reentry/status proof says connector lane is already the
  active target.

Conversation starters are not automatic tool-call instructions. `/guest-mode`
should mount package/starter context and declare guest limits without calling
Action Gateway or MCP unless the user asks for live connection/status, asks for
a connector-backed draft, or provides relevant non-secret reentry/status proof.

| Need | Prefer | Why |
| --- | --- | --- |
| Check if ION is reachable | Gateway `/health` or MCP `ping` | Fast transport proof |
| Inspect policy/context | Gateway `/policy`, `/context-pack` | Purpose-built action surface |
| Inspect MCP tools | MCP `tools/list` | Current tool visibility |
| Read ION status | MCP `ion_status` or Gateway context | Runtime-oriented proof |
| Queue Codex work | Gateway validate/submit or extension `ion_action` | Approval-gated work packet route |
| Emit local browser proposal | Extension `ion_action` YAML | User-visible approval path |
| Read receipts | Gateway `/receipts/recent` or MCP receipt tools | Proof surface |
| Sign in or auth | Extension/gateway/OAuth UI | No chat secrets |
| Attach/export packages | Extension artifacts/packages tabs | User-visible browser/local handoff |

## Proof Ladder

Use the highest available proof:

1. Live Action/MCP/daemon return with timestamp and receipt.
2. Extension `ion_reentry` or approved local receipt.
3. Uploaded continuity bundle or memory pack with manifest.
4. Saved GPT files and current instructions.
5. User statement only.

User statements can start a route, but they do not prove runtime access, current
state, successful execution, or accepted continuity.

MCP health/status proves transport reachability only. It does not prove a guest
workspace mount, sign-in, accepted state, local execution authority, or
production authority.

## Connection Claims

Before saying "ION is connected" or "I can access local ION", require one of:

- Action Gateway health/policy/context return;
- MCP health/status/tool-list return;
- extension `ion_reentry`;
- daemon/gateway receipt;
- uploaded status block or log.

If none is present, say the route is unproven and ask for sign-in/connector
proof.
