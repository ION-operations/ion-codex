# AGENTS.md — ION Carrier Onboarding And Return Contract

## One-Sentence Law

ION orchestrates. Carriers carry. A host assistant, IDE chat, Codex session, MCP host, or browser session is not ION identity and is not automatically STEWARD, RELAY, PERSONA, MASON, or any other ION role.

## Shell Root

Work from the directory containing both:

```text
pyproject.toml
ION/REPO_AUTHORITY.md
```

No absolute path is canonical. If this two-file root cannot be confirmed, stop with `ROOT_NOT_CONFIRMED`.

## Current Carrier

Use the carrier id that matches the actual host:

```text
codex_extension  # Codex extension / Codex CLI
cursor           # Cursor parent-chat adapter
mcp              # mounted MCP adapter
manual           # human/manual carrier
```

For this Codex environment, the default carrier id is:

```text
codex_extension
```

Cursor-specific `/ion` commands are host adapter commands under `.cursor/`. They remain useful for Cursor, but they are not the universal ION workflow and must not be pasted into every carrier onboarding surface as root law.

## First Runtime Check

From shell root:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_status --ion-root . --json
```

Status is current runtime evidence. Do not infer active objective, gates, worker state, MCP readiness, or production authority from chat memory.

## Carrier Continue

Carrier-neutral continuation:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_carrier_continue --ion-root . --carrier <carrier_id> --operator-message "<message>" --json
```

Plan-only continuation for direct lead-dev edits where no worker rows should launch:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_carrier_continue --ion-root . --carrier <carrier_id> --operator-message "<message>" --max-spawn-rows 0 --mode plan-only --json
```

Read the generated state:

```text
ION/05_context/current/ACTIVE_WORK_PACKET.json
ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json
ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json
ION/05_context/current/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json
ION/05_context/current/ACTIVE_STEWARD_INTEGRATION_QUEUE.json
```

## Role And Spawn Law

The carrier does not decide from memory which ION roles should run. It follows `ACTIVE_ROLE_SPAWN_PLAN.json`.

A lawful worker spawn uses the row's generated context surfaces:

```text
context_package_path
compiled_context_bundle_path
context_load_receipt_path
```

Boot files, MINI, CAPSULE, session packets, saved Cursor agent definitions, or path lists are witness inputs only. They are never sufficient as the primary task prompt when a generated role context package exists.

## Return Contract

Every worker return intended for ION intake must begin:

```text
### CONTEXT PROOF
```

For Codex carrier work, use:

```text
### CONTEXT PROOF
### TEMPLATE ACTION PROOF
### RESULT
```

Record worker output through:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_carrier_task_return --ion-root . --role "<ROLE>" --index "<INDEX>" --task-output "<PATH>" --json
```

Accepted returns enter `ACTIVE_STEWARD_INTEGRATION_QUEUE.json`. Rejected returns are not accepted state.

## Current Operating Packet

Current carrier operating guidance is summarized in:

```text
ION/docs/setup/ION_CURRENT_OPERATING_PACKET_V119.md
```

This root file remains a compatibility index and return contract. It is not
core ION onboarding authority.

## No-Silent-Loss Law

No project file may be silently lost. This is not a no-deletion-ever rule.
Files may leave hot/runtime paths through hash-proven containment, quarantine,
or archive movement.

Full-project artifacts must be produced through:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_safe_full_project_packager --ion-root . --previous-full-zip <previous_zip> --zip-output <new_zip> --json
```

Do not treat a package as trunk when:

```text
unexpected_removed_files > 0
protected_removed_files > 0
zip_root_audit != ZIP_ROOT_CONFIRMED
```

If a protected file moved to containment, the report must show
`contained_removed_files` and `containment_moves` with matching SHA-256 proof.

## Stop Conditions

Stop and report instead of patching blindly when:

```text
ROOT_NOT_CONFIRMED
active state is missing or contradictory
human gates are open
worker returns lack context proof
package preservation fails
carrier capability is unproven
production/live authority would be implied without a ratified gate
```

## Authority Anchors

```text
ION/REPO_AUTHORITY.md
ION/docs/setup/ION_CURRENT_OPERATING_PACKET_V119.md
ION/docs/setup/CHATGPT_BROWSER_MCP_CONNECTOR_SETUP_V120.md
ION/docs/setup/CHATGPT_BROWSER_HTTP_MCP_PREVIEW_SETUP_V121.md
ION/docs/setup/CHATGPT_BROWSER_CLOUDFLARE_TUNNEL_SETUP_V122.md
ION/02_architecture/ION_CARRIER_ONBOARDING_AUTHORITY_PROTOCOL.md
ION/02_architecture/ION_CARRIER_RUNTIME_FOUNDATION_PROTOCOL.md
ION/02_architecture/ION_DEFAULT_CARRIER_ONBOARDING_PROTOCOL.md
ION/02_architecture/CODEX_EXTENSION_CARRIER_PROTOCOL.md
ION/02_architecture/ION_CHATGPT_BROWSER_MCP_CONNECTOR_PROTOCOL.md
ION/02_architecture/ION_CHATGPT_BROWSER_HTTP_MCP_PREVIEW_PROTOCOL.md
ION/02_architecture/ION_CHATGPT_BROWSER_CLOUDFLARE_TUNNEL_PROTOCOL.md
ION/02_architecture/ION_NO_SILENT_LOSS_AND_CONTAINMENT_PRESERVATION_PROTOCOL.md
ION/03_registry/codex_extension_carrier_profile.yaml
ION/03_registry/ion_chatgpt_browser_mcp_tool_policy.yaml
```
