---
type: router_trace
authority: A3_OPERATIONAL
created: 2026-04-08T23:25:00-04:00
status: COMPLETE
workstream: implementation
objective: Land the K1 operator entry surface over the live supervised runtime stack
---

# Trace — K1 Operator Entry Surface

## Intent

Expose the active supervised runtime stack through one discoverable operator-facing CLI without creating a second workflow.

## Planned passes

1. Codex — inspect live service carriers and identify the smallest lawful operator surface.
2. Codex — implement CLI delegation over existing service modules.
3. Codex — write protocol/spec/examples and focused CLI proofs.
4. Codex — update root read surfaces so operators can find the entrypoint immediately.

## Expected output

- `ION/04_packages/kernel/operator_cli.py`
- `ION/02_architecture/OPERATOR_ENTRY_SURFACE_PROTOCOL.md`
- `ION/06_intelligence/specs/T49_OperatorEntrySurface.spec.md`
- `ION/tests/test_kernel_operator_cli.py`
