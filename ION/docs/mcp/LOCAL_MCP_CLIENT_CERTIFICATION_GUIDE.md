# Local MCP Client Certification Guide

V66 certifies ION's local bridge contract for MCP-capable local clients.

## Command

From the snapshot root:

```bash
PYTHONPATH=ION/04_packages python -m kernel.ion_mcp_client_certification --ion-root ION --json
```

## What certification proves

Certification proves that the bridge can expose the required local MCP tool surface, mount ION through `ion.mount`, plan work through `ion.job.plan` as `DRY_RUN`, submit dry-run work through `ion.job.submit_dry_run` as `APPROVAL_REQUIRED`, refuse `ion.job.execute_live` as `REFUSED`, and avoid kernel truth mutation and live execution authorization.

## What certification does not prove

V66 does not prove that external products were live connected in this environment. It does not certify hosted ChatGPT MCP apps, OAuth, remote Streamable HTTP, Kubernetes, provider dispatch, browser mutation, or shell execution.

## Certified local profile classes

- generic stdio MCP profile;
- Cursor-style local stdio profile;
- VS Code-style local stdio profile;
- Codex-style local stdio profile.

## Next step

After V66, ION should evaluate an official MCP SDK wrapper and a local Streamable HTTP preview while preserving the exact same refusal boundary.
