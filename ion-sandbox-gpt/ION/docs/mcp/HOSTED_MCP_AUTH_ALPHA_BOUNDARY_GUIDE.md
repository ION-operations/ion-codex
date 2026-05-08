# Hosted MCP Auth Alpha Boundary Guide

V69 is the first hosted-account boundary for ION MCP. It does not run OAuth, cloud hosting, or live execution. It models the minimum objects that must exist before those systems are safe to implement.

Run the local boundary report from an extracted project root:

```bash
PYTHONPATH=ION/04_packages python -m kernel.ion_mcp_hosted_auth_alpha --ion-root ION --json
```

Expected high-level result:

```json
{
  "passed": true,
  "oauth_certified": false,
  "hosted_cloud_certified": false,
  "public_endpoint_certified": false,
  "live_execution_authorized_seen": false,
  "token_session_separation_verified": true,
  "transport_session_authority_separation_verified": true
}
```

The critical rule is that "connected to ION" is not enough. A hosted mount must bind account, workspace, state root, subject, token audience, token workspace scope, requested scopes, execution mode, and receipts.

V69 is the gate before V70. V70 may implement an actual Streamable HTTP/OAuth preview only if it preserves V69's no-live-execution invariant.
