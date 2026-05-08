# ION V69 Hosted MCP Auth and Account/Workspace Alpha Protocol

## Branch identity

`V69_HOSTED_MCP_AUTH_AND_ACCOUNT_WORKSPACE_ALPHA_PROTOCOL`

V69 converts the V68 hosted HTTP alpha boundary into an explicit account, workspace, state-root, token, and session separation protocol. It remains an alpha/protocol boundary and does not certify OAuth, public hosting, cloud deployment, Kubernetes, provider dispatch, shell execution, browser mutation, credential access, or live execution.

## Governing law

1. A bearer token is not an ION session.
2. An MCP transport session is not ION authority.
3. A ChatGPT/Cursor/Codex/Claude/VS Code client identity is not enough to mutate ION.
4. A workspace mount must resolve through account, workspace, state-root, token audience, token subject, token workspace scope, requested scopes, execution mode, and receipt constraints.
5. Hosted alpha may only resolve to `READ_ONLY`, `DRY_RUN`, `APPROVAL_REQUIRED`, or `REFUSED`.
6. Hosted alpha may not resolve to `LIVE_EXECUTED`.

## Object model

```text
Account
  -> Workspace
    -> State Root
      -> Mounted ION Session
        -> Receipts / approvals / dry-run jobs
```

Token and session are deliberately separate:

```text
Access token:
  proves a subject, audience, expiry, and granted scopes.

MCP transport session:
  belongs to the protocol transport and may carry stream/session continuity.

ION mounted session:
  belongs to the ION kernel/session/receipt layer and binds account, workspace,
  state root, execution mode, and policy.
```

## V69 non-goals

- No OAuth certification.
- No public endpoint certification.
- No hosted cloud certification.
- No Kubernetes certification.
- No live execution.
- No provider dispatch.
- No shell execution.
- No browser mutation.
- No credential access.
- No direct governed-write mutation.
- No daemon loop activation.

## Allowed alpha modes

`read_only` and `dry_run` only.

## Required branch invariant

Every hosted-MCP-facing decision must resolve to one of:

```text
READ_ONLY
DRY_RUN
APPROVAL_REQUIRED
REFUSED
```

No hosted alpha decision may claim:

```text
LIVE_EXECUTED
live_authorized
provider_dispatch_authorized
browser_mutation_authorized
credential_access_authorized
canonical_write_authorized
```

## Promotion gate

V70 or later may only implement real OAuth/hosted transport if V69 remains green and the resulting implementation proves the same invariants with actual HTTP/auth tooling.
