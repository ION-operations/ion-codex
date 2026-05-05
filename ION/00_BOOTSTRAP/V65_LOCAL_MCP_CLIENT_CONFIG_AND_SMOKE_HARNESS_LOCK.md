# V65 Local MCP Client Config and Smoke Harness Lock

## Branch

`V65_LOCAL_MCP_CLIENT_CONFIG_AND_SMOKE_HARNESS`

## Locked posture

V65 extends V64 by adding usability and verification surfaces for local MCP clients. It does not extend execution authority.

## Authority

This lock permits:

- local stdio bridge smoke testing;
- client configuration profile generation;
- dry-run bridge validation;
- refusal testing for live tool names.

This lock forbids:

- live execution;
- daemon loop activation;
- shell execution;
- browser mutation;
- external provider dispatch;
- credential access;
- direct canonical writes through MCP;
- hosted multi-tenant runtime assumptions.

## First operational command

```bash
PYTHONPATH=ION/04_packages python -m kernel.ion_mcp_local_bridge_smoke --ion-root ION --json
```

## Success condition

A valid V65 smoke report must show:

```text
passed: true
forbidden_resolution_seen: false
live_execution_authorized_seen: false
kernel_truth_mutation_seen: false
```

