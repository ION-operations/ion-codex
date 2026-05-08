# ION Carrier Mount Index

ION orchestrates. Carriers carry.

This file is a root-level mount index for a new carrier or agent. It is not ION identity, not STEWARD, not RELAY, not PERSONA, and not the source of protocol authority.

Authoritative state comes from the confirmed shell root, active runtime packets, current branch locks/reports, and ION kernel audits.

## 0. Current Operating Packet

Current carrier operating guidance is summarized in:

```text
ION/docs/setup/ION_CURRENT_OPERATING_PACKET_V119.md
```

This root file is a compatibility index only. It is not core ION onboarding
authority.

## 1. Confirm Shell Root

Work only from the directory containing both files:

```text
pyproject.toml
ION/REPO_AUTHORITY.md
```

If this invariant fails, stop with:

```text
ROOT_NOT_CONFIRMED
```

## 2. Read Current Runtime Truth

From shell root:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_status --ion-root . --json
```

Then inspect active state as needed:

```text
ION/05_context/current/ACTIVE_WORK_PACKET.json
ION/05_context/current/ACTIVE_CARRIER_TURN_PACKET.json
ION/05_context/current/ACTIVE_ROLE_SPAWN_PLAN.json
ION/05_context/current/ACTIVE_CARRIER_TASK_RETURN_LEDGER.json
ION/05_context/current/ACTIVE_STEWARD_INTEGRATION_QUEUE.json
```

Do not infer current truth from chat memory, stale boot files, old branch numbers, archived zips, or host-specific onboarding text.

## 3. Mount As A Carrier, Not An ION Role

Carrier is not identity. The carrier is the host/tool substrate that helps ION execute bounded work.

Use the actual current carrier id:

```text
codex_extension  # Codex extension / Codex CLI carrier
cursor           # Cursor parent-chat adapter only
mcp              # MCP host adapter only when mounted and audited
manual           # human/manual carrier
```

Refresh carrier state with the carrier-neutral entrypoint:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_carrier_continue --ion-root . --carrier <carrier_id> --operator-message "<message>" --json
```

For a direct bounded patch where no worker rows should be launched, use plan-only zero-spawn mode:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_carrier_continue --ion-root . --carrier <carrier_id> --operator-message "<message>" --max-spawn-rows 0 --mode plan-only --json
```

Cursor `/ion` commands are Cursor host adapter shortcuts. They are not universal ION law and do not apply to Codex or other carriers except through their own mounted adapter.

## 4. Follow Generated Packets

The active spawn plan decides what executes. A carrier must not choose routine roles from memory.

For each `spawn=true` row, use the generated context package or compiled context bundle named in the row. Boot files, MINI, CAPSULE, saved host agent definitions, and path-list acknowledgments are not enough.

Every worker return must be recorded through ION return intake before it becomes accepted state.

## 5. Preserve The Project

No project file may be silently lost. This is not a freeze on project
evolution: stale or harmful files should move to containment/quarantine/archive
with hash proof so they stop affecting hot runtime while remaining auditable.

Any full-project artifact must be built through the safe preservation gate:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_safe_full_project_packager --ion-root . --previous-full-zip <previous_zip> --zip-output <new_zip> --json
```

The package is invalid if protected or unexpected uncontained removals are
nonzero. Containment moves must appear as `contained_removed_files` and
`containment_moves` with matching SHA-256 proof.

## 6. Current Protocol Anchors

Read these when carrier authority is unclear:

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
```
