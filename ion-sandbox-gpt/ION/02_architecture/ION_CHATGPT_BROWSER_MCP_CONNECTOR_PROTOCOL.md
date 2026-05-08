# ION ChatGPT Browser MCP Connector Protocol

## Version

V120_CHATGPT_BROWSER_MCP_CONNECTOR_AND_CORRECT_CARRIER_ONBOARDING

## Purpose

V120 defines the ChatGPT-browser-facing connector lane for ION. The connector
is a bounded coordinator and continuity surface for ChatGPT browser sessions. It
does not replace the local Cursor/Codex build lane and does not grant arbitrary
machine control.

The local Cursor/Codex lane remains responsible for heavy filesystem edits,
tests, packaging, and direct shell work. The ChatGPT browser connector is for
current-state visibility, bounded queueing, decision receipts, and proof-gated
task-return packets.

## Current Build Target

The fact that ChatGPT browser does not yet have live access to the local ION
MCP server is not the conclusion. It is the V120 build target.

The intended architecture is dual-lane:

```text
1. Cursor/Codex local MCP lane
   Purpose: local IDE/build carrier lane.
   Uses local ion-control MCP and direct repo access.

2. ChatGPT browser MCP/custom connector lane
   Purpose: coordinator/continuity/management lane.
   Must be built as a bounded ChatGPT-facing connector to ION.
```

## Connector Law

```text
ION orchestrates.
Cursor carries.
Codex carries.
ChatGPT browser carries.
MCP carries.
No carrier is ION identity.
```

The ChatGPT browser connector must never claim STEWARD, RELAY, PERSONA,
live execution authority, live_execution_authority, or production authority.

## Transport Direction

The connector should be compatible with current ChatGPT Apps/MCP expectations:

```text
ChatGPT browser -> HTTPS /mcp endpoint -> bounded ION connector adapter -> ION kernel packets
```

OpenAI's Apps SDK documentation describes MCP servers as tool surfaces with
tool listing, tool calling, and optional component/resource returns. For
ChatGPT connection, the server must be reachable over HTTPS and registered as a
connector in ChatGPT developer mode.

V120 does not deploy that hosted endpoint. V120 creates the contract, policy,
schema, and local audit surface that any hosted endpoint must satisfy before it
is allowed to become an active connector.

## Allowed MVP Tool Families

### status/read

```text
ion_status
ion_current_operating_packet
ion_carrier_onboarding_packet
ion_read_active_packet
ion_context_plan
ion_cockpit_view
ion_artifact_manifest
ion_receipt_search
ion_git_status_summary
```

These tools may read bounded ION state and emit structured summaries. They must
not execute arbitrary shell commands or read unbounded filesystem paths.

`ion_carrier_onboarding_packet` is the canonical ChatGPT-browser onboarding
entry point. It returns the ION-native onboarding path:

```text
shell root proof
current operating packet
carrier profile
mount contract
active packets
role/context surfaces
compiled context bundles
execution packet templates
context proof / template-action proof / task return / receipt flow
```

It must not use root-level `START_HERE_FOR_ANY_AGENT.md` or `AGENTS.md` as
carrier onboarding authority.

### bounded queue/receipt

```text
ion_queue_operator_message
ion_request_codex_work_packet
ion_submit_task_return
ion_record_chatgpt_decision
ion_create_containment_receipt
```

These tools may write only bounded packet/receipt records under active ION
state. They must not directly edit arbitrary project files or move/delete
project surfaces.

## Forbidden MVP Capabilities

```text
arbitrary shell
arbitrary file write
direct delete
git push
credential access
browser/computer control
provider API calls
unbounded local filesystem access
production deployment
direct acceptance of unproofed worker output
```

## Task Return Gate

`ion_submit_task_return` must validate both:

```text
### CONTEXT PROOF
### TEMPLATE ACTION PROOF
```

before recording a ChatGPT-origin task-return packet for carrier intake. A
validated packet still does not become accepted project truth by itself. It must
pass ION carrier task-return intake and Steward integration before it can affect
current authority.

## Containment Receipt Gate

`ion_create_containment_receipt` may record a proposed containment/quarantine/
archive/supersession transition with hash evidence. It must not physically move
or delete the target path. Actual movement remains a separate bounded mutation
with preservation proof.

## Current Authority

This connector obeys:

```text
NO SILENT LOSS + CONTAINMENT PRESERVATION
```

Meaning no authority-bearing state may disappear from hot state without
classification, proof, and custody. Stale or harmful surfaces should be moved
through containment/quarantine/archive/supersession custody rather than kept hot
or silently removed.

## Validation

Run:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_chatgpt_browser_mcp_connector_contract --ion-root . --write --json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest ION/tests/test_kernel_ion_chatgpt_browser_mcp_connector_contract.py -q
```

Expected verdict:

```text
ION_CHATGPT_BROWSER_MCP_CONNECTOR_CONTRACT_READY
```
