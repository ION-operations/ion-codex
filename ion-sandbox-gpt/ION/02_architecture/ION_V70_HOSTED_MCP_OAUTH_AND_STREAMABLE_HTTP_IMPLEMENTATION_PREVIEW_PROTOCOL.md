# ION V70 — Hosted MCP OAuth and Streamable HTTP Implementation Preview Protocol

## Branch

`V70_HOSTED_MCP_OAUTH_AND_STREAMABLE_HTTP_IMPLEMENTATION_PREVIEW`

## Purpose

V70 converts the V69 hosted-auth alpha boundary into a local implementation preview of the mechanics that a future hosted ION MCP endpoint will require:

1. OAuth authorization-code + PKCE-shaped preview.
2. Bearer-header validation for hosted `/mcp` requests.
3. Streamable-HTTP-style POST dispatch.
4. Delegation into ION's existing local MCP bridge and V69 hosted mount evaluator.
5. Preservation of account/workspace/state-root/token/session separation.

## Non-goals

V70 does not certify production OAuth, public endpoint operation, cloud tenancy, Kubernetes, provider dispatch, shell execution, browser mutation, secret-vault access, live daemon activation, or direct governed-write mutation.

## Law

A successful OAuth preview authenticates an actor; it does not authorize execution.

A token is not an ION session.

An MCP transport session is not ION authority.

A hosted `/mcp` request must bind token audience, subject, workspace, state root, requested scopes, execution mode, and receipts before any tool request may be accepted.

Every MCP-facing result must resolve to one of: `READ_ONLY`, `DRY_RUN`, `APPROVAL_REQUIRED`, or `REFUSED`.

`LIVE_EXECUTED` is forbidden in V70.

## Implementation surface

`ION/04_packages/kernel/ion_mcp_hosted_oauth_http_preview.py`

The module exposes:

- `issue_authorization_code_preview`
- `exchange_authorization_code_preview`
- `validate_bearer_preview`
- `handle_hosted_streamable_http_oauth_preview_request`
- `build_v70_oauth_http_preview_report`

## Required invariant

The preview may prove HTTP/auth mechanics, but any state-changing or live-capability request must remain blocked, dry-run-only, or approval-required.
