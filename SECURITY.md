# Security Policy

This public repository must not contain secrets or production-only operational
state.

## Public / Private Boundary

This repository is intended to be public collaboration infrastructure for ION.
Future private production infrastructure may live elsewhere. Do not treat the
presence of public code, docs, issues, or pull requests as production authority
or live external execution authority.

GitHub is a durable collaboration and data plane. It is not ION runtime
authority. A GitHub issue, comment, pull request, or branch is evidence until it
passes the normal ION packet, proof, gate, Steward decision, and receipt path.

## Do Not Commit

- API keys, access tokens, OAuth client secrets, session cookies, or refresh
  tokens
- `.env` files or private config with credentials
- browser profiles, credential helper dumps, cloudflared credentials, or tunnel
  tokens
- Cloudflare origin certificates, named tunnel credential JSON files, API
  tokens, OAuth secrets, or private connector callback secrets
- private logs, incident material, customer/user data, or production
  infrastructure state

If a file is useful only because it contains a secret, credential, or private
session artifact, it does not belong in this public repository.

## Local Automation Boundary

ION may include browser extension, local daemon, Codex CLI, MCP, tunnel, and
future desktop-helper surfaces. These are operator-carrier surfaces, not
standing permission for hidden automation.

Security-sensitive automation must be:

- visible to the operator
- bounded to an approved target and artifact
- revocable
- logged
- receipted when ION state is touched

Do not add hidden upload, hidden Send, credential capture, arbitrary folder
read, production deployment, git push, or destructive local mutation paths.
Higher-risk operations belong behind explicit Steward/local gates and should
fail closed when target, authority, or context is unclear.

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

Relevant public orientation:

- `ION/docs/ION_FUNDAMENTALS.md`
- `ION/docs/ION_PROJECT_INGESTION.md`
- `ION/docs/ION_DOMAIN_GRAPH_AND_FISSION.md`
- `ION/docs/GITHUB_BRANCHING_AND_LIVE_STATE_POLICY.md`
