# Security Policy

This public repository must not contain secrets or production-only operational
state.

## Public / Private Boundary

This repository is intended to be public collaboration infrastructure for ION.
Future private production infrastructure may live elsewhere. Do not treat the
presence of public code, docs, issues, or pull requests as production authority
or live external execution authority.

## Do Not Commit

- API keys, access tokens, OAuth client secrets, session cookies, or refresh
  tokens
- `.env` files or private config with credentials
- browser profiles, credential helper dumps, cloudflared credentials, or tunnel
  tokens
- private logs, incident material, customer/user data, or production
  infrastructure state

If a file is useful only because it contains a secret, credential, or private
session artifact, it does not belong in this public repository.

## Report A Concern

Open a GitHub security advisory or contact the repository owner out of band if
the issue includes a secret, credential, or exploit detail that should not be
public.

For non-sensitive hardening work, open a normal issue or pull request and label
it clearly.

## Authority Boundary

Security reports, issues, and pull requests are evidence and proposals. They do
not directly mutate ION runtime state and do not grant production authority.

Security fixes should still preserve ION's state boundary where practical:
describe the affected paths, the risk, the validation run, and any receipt,
gate, issue, or pull request that proves the handling path.
