# ION V125 Codex CLI Carrier and ChatGPT Connector Dogfood Report

## Summary

V125 separates Codex CLI from the older Codex extension/IDE carrier surface and
makes it the preferred local worker carrier for bounded filesystem/build/test
work. ChatGPT browser remains the coordinator and continuity lane, mediated by
the bounded MCP connector contract.

## Changed Files

- Added `ION/02_architecture/CODEX_CLI_CARRIER_PROTOCOL.md`
- Added `ION/03_registry/codex_cli_carrier_profile.yaml`
- Added `ION/07_templates/carriers/CODEX_CLI_EXECUTION_PACKET.md`
- Added `ION/docs/setup/CODEX_CLI_ION_DOGFOOD_SETUP_V125.md`
- Added `ION/04_packages/kernel/ion_codex_cli_carrier_audit.py`
- Added `ION/tests/test_kernel_ion_codex_cli_carrier_audit.py`
- Updated `ION/04_packages/kernel/ion_carrier_onboarding_packet.py` so `codex` and `codex_cli` resolve to the Codex CLI carrier profile.
- Updated `ION/REPO_AUTHORITY.md` with the Codex CLI local worker lane.

## Validation

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_codex_cli_carrier_audit --ion-root . --write --json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_carrier_onboarding_packet --ion-root . --carrier codex_cli --json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest ION/tests/test_kernel_ion_codex_cli_carrier_audit.py ION/tests/test_kernel_ion_carrier_onboarding_packet.py -q
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest ION/tests -q
```

Expected results:

```text
ION_CODEX_CLI_CARRIER_READY
ION_CARRIER_ONBOARDING_PACKET_READY
```

## Remaining Gaps

- ChatGPT browser connector remains local/public-connector setup, not production.
- Codex CLI itself must be installed/authenticated on the operator machine.
- A real Codex CLI dogfood run should capture `latest_prompt.md`, `latest_return.md`, and optionally `latest_events.jsonl`, then ingest the result through proof gates.
