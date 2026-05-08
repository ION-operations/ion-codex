# V69 Branch Lock

Branch: `V69_HOSTED_MCP_AUTH_AND_ACCOUNT_WORKSPACE_ALPHA_PROTOCOL`

This lock promotes the V69 hosted MCP account/workspace/state-root/auth boundary as the active continuation horizon.

## Locked constraints

- Hosted alpha is not hosted production.
- Token is not session.
- MCP transport session is not authority.
- Workspace mount must bind account, workspace, state root, subject, scopes, mode, and receipt.
- V69 cannot execute live work.
- V69 cannot certify OAuth, public endpoint, Kubernetes, provider dispatch, browser mutation, shell execution, or credentials.

## Allowed resolutions

- `READ_ONLY`
- `DRY_RUN`
- `APPROVAL_REQUIRED`
- `REFUSED`

## Forbidden resolution

- `LIVE_EXECUTED`
