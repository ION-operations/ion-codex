# BOOT-2 Sign-In, Reentry, And Guest Mode

## Public Routes

```text
/sign-in
/sign-up
/guest-mode
/what is ION?
```

These routes are not proof by themselves.

## Sign-In

Use extension/local-gateway/OAuth/platform Action auth. Never ask for passwords
or tokens in chat. After proof appears, mount the proof object:

- `ion_reentry`
- Action return
- MCP status block
- local gateway receipt
- uploaded status log
- pasted non-secret status block

## Sign-Up

Draft onboarding defaults if useful. Account creation happens in the auth UI,
not chat.

## Guest Mode

Guest mode starts from mounted package/starter context. Do not call Action
Gateway or MCP just because `/guest-mode` was selected.

Allowed by default:

- read/status
- dry-run
- sample project
- local demo
- create Codex work-packet draft

Forbidden by default:

- secrets;
- broad shell;
- GitHub mutation;
- production deploy;
- push-main;
- accepted durable state without receipt/export.

MCP or Action health can be checked only when the user asks for live connection
status, asks to create a connector-backed draft, or provides relevant reentry
proof. MCP readiness is transport proof only; it is not a guest workspace mount,
sign-in proof, accepted state, or local authority.

If no connector proof is visible, run guest mode as a labeled local demo/sample
lane and ask what the user wants to work on.

## Reentry Proof

A reentry proof should identify user/workspace/session handles without exposing
secrets.
