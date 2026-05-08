# Local Hosted MCP OAuth/HTTP Preview Guide

V70 gives ION a local hosted-style mechanics preview.

Run:

```bash
PYTHONPATH=ION/04_packages python -m kernel.ion_mcp_hosted_oauth_http_preview --ion-root ION --json
```

This is not a public server. It is a proof that:

- an OAuth authorization-code + PKCE-shaped exchange can produce a preview token;
- raw bearer material is not stored in the token object;
- `/mcp` requests require an Authorization bearer header;
- hosted mount still binds account/workspace/state-root/token/session constraints;
- live execution remains impossible.

The preview delegates actual tool execution to the V64 local bridge and the V69 hosted mount evaluator.
