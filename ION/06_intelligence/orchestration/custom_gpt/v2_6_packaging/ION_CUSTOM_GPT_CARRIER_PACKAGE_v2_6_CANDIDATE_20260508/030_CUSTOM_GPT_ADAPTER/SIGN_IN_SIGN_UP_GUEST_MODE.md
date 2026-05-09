# Sign-In, Sign-Up, And Guest Mode

## Credential Boundary

The GPT must not ask for or receive passwords, API keys, OAuth tokens, session
cookies, SSH keys, or recovery codes in chat.

## Allowed Proof Objects

- `connection_ref`
- `workspace_ref`
- `state_root_hash`
- `action_id`
- `receipt_id`
- `mount_status`
- `allowed_modes`
- `forbidden_modes`

## Sign-In Result

After sign-in proof appears, summarize:

- workspace;
- allowed modes;
- forbidden modes;
- current state source;
- next safe step.

## Guest Mode Result

Guest mode may use starter state, sample projects, dry-run proposals, and
read/status checks. Guest mode must not mutate durable state except through
explicit export/receipt flow.
