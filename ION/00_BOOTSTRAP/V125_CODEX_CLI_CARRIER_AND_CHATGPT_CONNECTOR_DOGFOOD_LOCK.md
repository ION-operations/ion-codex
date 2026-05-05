# V125 — Codex CLI Carrier and ChatGPT Connector Dogfood Lock

## Status

```yaml
version_line: V125_CODEX_CLI_CARRIER_AND_CHATGPT_CONNECTOR_DOGFOOD_SETUP
status: ACTIVE_WORK_SURFACE_LOCK
production_authority: false
live_execution_authority: false
```

## Locked Truth

Codex CLI is now represented as its own local worker carrier lane rather than
being collapsed into the older Codex extension/IDE carrier surface.

The intended dogfood topology is:

```text
ChatGPT browser / GPT-5.5 Pro = coordinator + continuity + decision lane
ChatGPT browser MCP connector = bounded read/queue/receipt bridge
Codex CLI = local bounded filesystem/build/test worker carrier
ION = runtime law, packet compiler, template gates, receipts, lifecycle, cockpit
```

## Added Surfaces

- `ION/02_architecture/CODEX_CLI_CARRIER_PROTOCOL.md`
- `ION/03_registry/codex_cli_carrier_profile.yaml`
- `ION/07_templates/carriers/CODEX_CLI_EXECUTION_PACKET.md`
- `ION/docs/setup/CODEX_CLI_ION_DOGFOOD_SETUP_V125.md`
- `ION/04_packages/kernel/ion_codex_cli_carrier_audit.py`
- `ION/tests/test_kernel_ion_codex_cli_carrier_audit.py`

## Preserved Boundary

This lock does not grant production authority, live execution authority, git
push authority, arbitrary shell/file authority, credential access, or deployment
authority.

Codex CLI must return `### CONTEXT PROOF`, `### TEMPLATE ACTION PROOF`, and
`### RESULT` before ION treats its output as intake material.
