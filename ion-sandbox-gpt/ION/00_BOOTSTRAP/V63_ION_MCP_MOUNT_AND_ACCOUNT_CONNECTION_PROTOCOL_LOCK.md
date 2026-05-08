# V63 ION MCP Mount and Account Connection Protocol Lock

**Branch:** `V63_ION_MCP_MOUNT_AND_ACCOUNT_CONNECTION_PROTOCOL`  
**Date:** 2026-04-26  
**Authority posture:** Protocolization and dry-run/read-first MCP front-door planning only. No live provider dispatch, browser mutation, credential access, paid cloud launch, Kubernetes deployment, direct kernel write, or production authority.

## Purpose

V63 locks the next lawful branch horizon: ION should become mountable through MCP while preserving V62's approval queue and dry-run handoff boundary.

## Branch rule

```text
MCP is an ION front door, not an execution bypass.
```

## Required surfaces

```text
ION/02_architecture/ION_FULL_OPERATIONALIZATION_AND_TESTING_PROTOCOL.md
ION/02_architecture/ION_MCP_FRONT_DOOR_AND_MOUNT_SESSION_PROTOCOL.md
ION/02_architecture/ION_ACCOUNT_WORKSPACE_AND_STATE_ROOT_PROTOCOL.md
ION/02_architecture/ION_PRODUCT_PACKAGING_AND_DEPLOYMENT_PROTOCOL.md
ION/02_architecture/ION_V63_BRANCH_DEFINITION_AND_EXECUTION_HORIZON_PROTOCOL.md
ION/03_registry/ion_mcp_mount_session.schema.json
ION/03_registry/ion_mcp_capability_scope_policy.yaml
ION/03_registry/ion_operational_readiness_gate_policy.yaml
ION/05_context/handoff/V63_ION_MCP_MOUNT_AND_FULL_OPERATIONALIZATION_HANDOFF.md
```

## Non-authority boundary

V63 may define and prototype read-only and dry-run MCP mount behavior. V63 may not authorize live execution, external model/provider calls, credential access, browser mutation, paid cloud launch, or production deployment.

## Success condition

The next implementation branch should prove that a client can mount ION, receive a boot packet, inspect horizon/state/receipts/approvals, and request dry-run planning while all privileged actions remain refused or approval-required.
