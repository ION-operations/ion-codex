# Hosted MCP Bundle Import/Export Replay Alpha Guide

V72 provides the first bundle round-trip contract for hosted ION-over-MCP.

Run:

```bash
PYTHONPATH=ION/04_packages python -m kernel.ion_mcp_hosted_bundle_replay_alpha --json
```

The report must pass only when export preview, import validation, replay preview, and tamper refusal all succeed. V72 is not a live execution branch.
