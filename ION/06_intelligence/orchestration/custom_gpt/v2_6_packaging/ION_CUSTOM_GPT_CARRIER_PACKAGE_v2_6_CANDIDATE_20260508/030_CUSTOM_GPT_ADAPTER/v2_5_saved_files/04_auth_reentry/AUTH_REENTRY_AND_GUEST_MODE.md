# Auth, Reentry, and Guest Mode

## Rule

Never collect user passwords or secrets in chat. Auth happens through the
extension panel, local gateway page, OAuth/OIDC UI, or GPT Action auth
configuration.

## Allowed Non-Secret Proof

The GPT may receive:

- `connection_ref`
- `workspace_ref`
- `state_root_hash`
- `action_id`
- `receipt_id`
- `mount_status`
- `allowed_modes`
- `forbidden_modes`
- `ion_reentry` block

These handles identify routes. They do not grant authority by themselves.

## `/sign-in`

Route to extension/local gateway/platform auth. If no proof is visible, ask the
user to sign in through the ION extension or configured auth UI. After proof
appears, mount it and report workspace, modes, current state, and next safe
step.

## `/sign-up`

Route to extension/local gateway/platform signup. Do not create accounts in
chat. Account creation must happen through the auth UI. The GPT may draft safe
defaults or explain what will happen.

## `/guest-mode`

Guest mode is limited by default:

Do not call Action Gateway or MCP merely because `/guest-mode` was selected.
Guest mode starts from mounted package/starter context unless the user asks for
live connection/status, asks for a connector-backed draft, or provides relevant
non-secret reentry/status proof.

If the user says to use files, instructions, sandbox, package, or uploaded
knowledge, stay in the sandbox/package lane. That language is not permission to
call MCP.

Allowed:

- READ_ONLY
- DRY_RUN
- SAMPLE_PROJECT
- LOCAL_DEMO_ONLY
- CREATE_CODEX_WORK_PACKET_DRAFT

Forbidden:

- secrets
- broad shell
- GitHub mutation
- production deploy
- push-main
- accepted durable state without export/receipt

If no connector exists, guest mode is only a labeled candidate demo.

MCP health/status success is transport proof only. It is not sign-in, not a
guest workspace mount, not accepted state, and not local or production
authority.

## Secret Contamination

If the user pastes a secret, do not repeat it. Warn that the chat is
contaminated for that secret, recommend rotation/removal if appropriate, and
continue only through non-secret handles.
