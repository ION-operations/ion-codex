# Codex CLI ION Dogfood Setup V125

## Status

```yaml
version_line: V125_CODEX_CLI_CARRIER_AND_CHATGPT_CONNECTOR_DOGFOOD_SETUP
carrier_id: CODEX_CLI_CARRIER
host_family: codex_cli
production_authority: false
live_execution_authority: false
```

## Goal

This setup makes Codex CLI the preferred local worker carrier while ChatGPT
browser remains the coordinator and long-horizon reasoning lane. ION remains the
governing runtime: packets, templates, proof gates, receipts, lifecycle law,
and cockpit state.

## Install / Auth

Install or update Codex CLI on the local machine using the current OpenAI Codex
CLI distribution method selected by the operator. ION records the carrier lane;
it does not store credentials.

```bash
npm install -g @openai/codex
codex login
codex --version
```

For API-key operation, keep secrets in the shell environment or OS secret store,
not in the ION repo.

```bash
export OPENAI_API_KEY="..."
```

## Shell Root

Always start from the ION shell root:

```bash
cd "<path-to>/ION - CODEX"
test -f pyproject.toml
test -f ION/REPO_AUTHORITY.md
```

## ION Preflight

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_status --ion-root . --json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_carrier_onboarding_packet --ion-root . --carrier codex_cli --json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_codex_cli_carrier_audit --ion-root . --json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest ION/tests/test_kernel_ion_codex_cli_carrier_audit.py -q
```

Expected:

```text
ION_STATUS_READY
ION_CARRIER_ONBOARDING_PACKET_READY
ION_CODEX_CLI_CARRIER_READY
```

## Prompt/Return Capture Directory

```bash
mkdir -p ION/05_context/current/codex_cli
```

The standard paths are:

```text
ION/05_context/current/codex_cli/latest_prompt.md
ION/05_context/current/codex_cli/latest_return.md
ION/05_context/current/codex_cli/latest_events.jsonl
```

## Minimal Dogfood Invocation

Create a bounded prompt from the current ION packet and template requirements,
then run Codex CLI in a captured mode:

```bash
codex exec --sandbox workspace-write \
  --output-last-message ION/05_context/current/codex_cli/latest_return.md \
  < ION/05_context/current/codex_cli/latest_prompt.md
```

Optional JSONL event capture:

```bash
codex exec --json --sandbox workspace-write \
  --output-last-message ION/05_context/current/codex_cli/latest_return.md \
  < ION/05_context/current/codex_cli/latest_prompt.md \
  > ION/05_context/current/codex_cli/latest_events.jsonl
```

## Return Intake

The Codex CLI final answer must include:

```text
### CONTEXT PROOF
### TEMPLATE ACTION PROOF
### RESULT
```

Then ingest through the local proof-gated return path or the ChatGPT connector
`ion_submit_task_return` path when the connector is live.

## Operating Boundary

Allowed by default:

```text
read files
edit bounded project files
run local tests
write captured return/event evidence under ION/05_context/current/codex_cli/
```

Still forbidden without explicit human gate:

```text
git push
deployment
credential access
direct deletion without lifecycle receipt
unbounded filesystem access
provider API orchestration outside Codex itself
production authority
```
