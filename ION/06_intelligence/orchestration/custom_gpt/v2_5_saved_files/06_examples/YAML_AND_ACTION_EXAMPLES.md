# YAML and Action Examples

## Queue Local Codex Work Through Extension YAML

```yaml
ion_action:
  schema: ion.chatops.action.v1
  action_id: sev-20260508-0001-codex-work
  intent: create_codex_work_packet
  actor:
    callsign: Sev
    carrier: chatgpt_browser
  authority:
    human_sovereign: Braden
    requires_approval: true
    production_authority: false
    live_execution_authority: false
  objective: |
    Inspect the active ION root, read the named context files, implement the
    bounded requested change, run focused validation, and return proof sections.
  target:
    provider: local_ion
    root: ION_CODEX_FULL
  receipts:
    requested:
      - codex_work_packet_receipt
      - action_receipt
```

## Write A Draft File Through Extension YAML

```yaml
ion_action:
  schema: ion.chatops.action.v1
  action_id: sev-20260508-0002-draft-file
  intent: write_file_draft
  actor:
    callsign: Sev
    carrier: chatgpt_browser
  authority:
    human_sovereign: Braden
    requires_approval: true
    production_authority: false
    live_execution_authority: false
  target:
    provider: local_ion
    root: ION_CODEX_FULL
    path: ION/05_context/current/chatops_bridge/drafts/example.md
    overwrite: false
  content:
    encoding: utf-8
    text: |
      # Example Draft

      This is a bounded draft produced through the ION ChatOps bridge.
  receipts:
    requested:
      - file_write_receipt
      - sha256_receipt
```

## MCP `tools/list`

```json
{
  "jsonrpc": "2.0",
  "id": "tools-list-1",
  "method": "tools/list",
  "params": {}
}
```

## MCP `ion_status`

```json
{
  "jsonrpc": "2.0",
  "id": "ion-status-1",
  "method": "tools/call",
  "params": {
    "name": "ion_status",
    "arguments": {}
  }
}
```

## Action Gateway Validate

Use validate before submit. Do not submit without approval evidence.

The GPT should not invent a successful validation result. It must call the
Action when available or say validation is unproven.
