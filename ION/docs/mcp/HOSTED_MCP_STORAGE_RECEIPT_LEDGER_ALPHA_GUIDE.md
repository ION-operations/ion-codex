# Hosted MCP Storage and Receipt Ledger Alpha Guide

V71 defines how ION can persist hosted account/workspace state-root metadata, receipt events, object references, and bundle export previews without turning storage into execution authority.

Run the alpha report from an extracted project root:

```bash
PYTHONPATH=ION/04_packages python -m kernel.ion_mcp_hosted_storage_receipt_ledger_alpha --json
```

The report must show:

- event chain verified;
- state-root snapshots content-addressed;
- append-only ledger verified;
- bundle export preview verified;
- hosted cloud not certified;
- Kubernetes not certified;
- production object storage not certified;
- live execution not authorized;
- kernel truth not mutated.

V71 is a substrate branch. It prepares the account/workspace/state-root storage plane for later productization, but it does not deploy any public endpoint or execution plane.
