# ION Current Operating Packet V119

## Authority Status

This packet is the current short operating packet for carriers mounting the
current ION tree. It supersedes older V105-V123 onboarding canvases wherever
there is conflict.

Older canvases remain historical context only. Do not execute older
instructions that conflict with current runtime state, current carrier law, or
V118 containment-preservation law.

## Current Verified State

The current tree has been verified from shell root:

```yaml
root_confirmed: true
ion_status: ION_STATUS_READY
active_objective: V120_CHATGPT_BROWSER_MCP_CONNECTOR_AND_CORRECT_CARRIER_ONBOARDING
mcp_self_test: ION_MCP_CONTROL_BRIDGE_READY
mcp_bridge_audit: PASS
codex_carrier_audit: ION_CODEX_EXTENSION_CARRIER_READY
carrier_onboarding_authority_audit: ION_CARRIER_ONBOARDING_AUTHORITY_READY
carrier_onboarding_packet: ION_CARRIER_ONBOARDING_PACKET_READY
chatgpt_connector_contract: ION_CHATGPT_BROWSER_MCP_CONNECTOR_CONTRACT_READY
production_authority: false
live_execution_authority: false
```

## Root Invariant

The shell root is the directory containing both:

```text
pyproject.toml
ION/REPO_AUTHORITY.md
```

If this invariant fails, stop with:

```text
ROOT_NOT_CONFIRMED
```

## Governing Law

Current preservation law is:

```text
NO SILENT LOSS + CONTAINMENT PRESERVATION.
```

Meaning:

```text
No project file or authority-bearing surface may vanish without classification, proof, and custody.
Stale, harmful, hallucinated, superseded, or conflicting surfaces should not remain hot merely because they existed before.
They should move to containment, quarantine, archive, or supersession custody with hash-proven receipts.
```

The older no-silent-deletion phrase is obsolete if interpreted as "no file may
leave hot state." It survives only as shorthand for:

```text
No unreceipted disappearance of authority-bearing state.
```

## Lawful Lifecycle Transitions

Current lawful transitions include:

```text
KEEP_ACTIVE
MODIFY_ACTIVE
ADD_ACTIVE
MOVE_TO_CONTAINMENT
MOVE_TO_QUARANTINE
MOVE_TO_ARCHIVE
RETIRE_TO_CONTAINMENT
SUPERSEDE_WITH_REPLACEMENT
REMOVE_GENERATED_CACHE
DELETE_WITH_EXPLICIT_AUTHORITY
```

Packaging or trunk promotion must fail when a meaningful surface disappears
from hot state with no lawful transition receipt.

## Carrier-Onboarding Authority

Current carrier onboarding authority is ION-native:

```text
ION/REPO_AUTHORITY.md
ION/02_architecture/ION_MOUNT_CONTRACT.md, if present and current
carrier registry YAML profiles
runtime identity mount registries
role boot/context surfaces
compiled context bundles
execution packet templates
carrier capability survey templates
active packets under ION/05_context/current/
task return / context proof / template-action proof gates
```

Root convenience files are retired from hot onboarding authority:

```text
AGENTS.md
START_HERE_FOR_ANY_AGENT.md
```

As of V123, their prior hot-root copies belong in containment evidence, not the
shell root. Future carriers must mount through registry profiles, context
bundles, execution packets, carrier templates, active packets, and proof gates.
If either file appears at shell root with procedural onboarding, command lists,
mandatory reads, or authority anchors, treat it as drift and move it to
containment with preservation proof.

The April 17 exported root-authority bundle that centered `START_HERE.md` is
also retired from hot startup authority. Its contained copy is historical
evidence only:

```text
ION/05_context/archive/containment/V123_ROOT_ONBOARDING_SHIMS/root_authority_bundle_2026-04-17/
```

## Carrier Law

```text
ION orchestrates.
Cursor carries.
Codex carries.
ChatGPT browser carries.
MCP carries.
No carrier is ION identity.
```

## MCP State And V120 Build Target

Current repo MCP truth:

```text
.cursor/mcp.json exposes ion-control only.
ion-control exists and passes self-test/audit.
```

Do not claim `openaiDeveloperDocs` or any other documentation MCP is present
unless it is present and verified in the current repo.

The current local MCP server exposes bounded ION control tools only:

```text
ion_status
ion_continue
ion_context_plan
ion_cockpit_view
ion_workflow_audit
ion_read_active_packet
ion_task_return
```

It does not expose arbitrary shell, arbitrary writes, credentials, provider
calls, browser mutation, or destructive operations.

Critical clarification:

```text
The fact that ChatGPT browser does not yet have a live ION connector is not the conclusion.
It is the build target.
```

The intended architecture is dual-lane:

```text
1. Cursor/Codex local MCP lane
   Purpose: local IDE/build carrier lane.
   Uses local ion-control MCP and direct repo access.

2. ChatGPT browser MCP/custom connector lane
   Purpose: coordinator/continuity/management lane.
   Must be built as a bounded ChatGPT-facing connector to ION.
```

Current V120 target:

```text
V120_CHATGPT_BROWSER_MCP_CONNECTOR_AND_CORRECT_CARRIER_ONBOARDING
```

V120 creates the contract, policy, schema, setup guide, local audit, and
connector scaffold for a ChatGPT-browser-facing ION connector. It also exposes
the correct ION-native carrier onboarding packet as a connector read tool.

Correct connector onboarding starts with:

```text
ion_carrier_onboarding_packet
```

That tool returns:

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

Root-level `START_HERE_FOR_ANY_AGENT.md` and `AGENTS.md` are not onboarding
authority.

V120 does not claim a deployed HTTPS connector, production authority, or live
execution authority.

V121 adds a local HTTP MCP preview:

```text
endpoint_path: /mcp
default_bind_host: 127.0.0.1
default_port: 8765
connector_state: LOCAL_HTTP_PREVIEW_NOT_PUBLIC_CONNECTOR
```

This preview is not a ChatGPT public connector. It proves the HTTP MCP-shaped
tool boundary locally before any HTTPS deployment is claimed.

V122 adds the local-development HTTPS exposure path:

```text
local preview: http://127.0.0.1:8765/mcp
Cloudflare Tunnel target: http://127.0.0.1:8765
ChatGPT connector URL: https://<cloudflare-host>/mcp
```

The older AIMOS `/sse` tunnel pattern is historical only for this branch. V122
uses `/mcp` because the current ChatGPT connector setup points at the public MCP
endpoint. V124 classified the older Cloudflare tunnel scripts as donor evidence
for this reusable transport pattern:

```text
cloudflared tunnel --url http://127.0.0.1:8765
```

The forbidden carry-forward remains:

```text
AIMOS identity
legacy /sse endpoint
legacy data/mcp status path
host-level auto-install behavior as an ION runtime mutation
```

V124 audit state:

```text
ION/05_context/current/CHATGPT_BROWSER_LEGACY_TUNNEL_REUSE_AUDIT_V124.json
```

Allowed initial V120 tool families:

```text
status/read:
- ion_status
- ion_current_operating_packet
- ion_read_active_packet
- ion_context_plan
- ion_cockpit_view
- ion_artifact_manifest
- ion_receipt_search
- ion_git_status_summary

bounded queue/receipt:
- ion_queue_operator_message
- ion_request_codex_work_packet
- ion_submit_task_return
- ion_record_chatgpt_decision
- ion_create_containment_receipt
```

Forbidden MVP capabilities:

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

Bounded write calls in the V121 HTTP preview require:

```text
ION_BOUNDED_WRITE_CONFIRMED
```

Cloudflare Tunnel state, when running, is recorded at:

```text
ION/05_context/current/ACTIVE_CHATGPT_BROWSER_CLOUDFLARE_TUNNEL.json
```

## Codex Operating Procedure

Minimum preflight from shell root:

```bash
ls pyproject.toml ION/REPO_AUTHORITY.md
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_status --ion-root . --json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S ION/09_integrations/mcp/ion_mcp_server.py --ion-root . --self-test
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_mcp_bridge_audit --ion-root . --json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_codex_extension_carrier_audit --ion-root . --json
```

Codex return format:

```text
### CONTEXT PROOF
- root confirmed
- current branch/objective confirmed
- files read
- active packets/context surfaces used
- assumptions or missing evidence

### TEMPLATE ACTION PROOF
- requested change
- files changed
- lifecycle/custody transitions
- tests run
- receipts/view models emitted
- boundaries not crossed

### RESULT
- implementation result
- validation result
- remaining blockers
- next lawful move
```

## Forbidden Stale Instructions

Do not execute or repeat older instructions that treat these as current:

```text
V105/V106/V107 as current
blunt no-silent-deletion as current law
START_HERE_FOR_ANY_AGENT.md as a required read
AGENTS.md as core ION carrier authority
V117 setup files as present in the current tree
openaiDeveloperDocs as present in .cursor/mcp.json
Cursor /ion as universal carrier law
MINI/CAPSULE as primary context authority
```

## Current Next Work Gate

Next implementation work should continue from the current V120 connector and
carrier-onboarding state and must
preserve:

```text
root mount proof
carrier-native onboarding authority
no-silent-loss containment preservation
MCP bounded control bridge truth
context proof and template-action proof for worker returns
no production/live authority claims
```

The likely next operational gates remain:

```text
Cloudflare Tunnel live connector test once cloudflared is installed and ChatGPT developer-mode connector is created
hosted-connector deployment hardening after local HTTP preview and tunnel proof
lifecycle-aware compact/full/forensic packaging
front-door proof trace integration
receipt hydration and lane telemetry hardening
bounded worker adapter return enforcement
template graph residue/metabolism
release candidate namespace separation
```
