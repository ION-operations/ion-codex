# `ion_action` YAML Reference

## Required Shape

```yaml
ion_action:
  schema: ion.chatops.action.v1
  action_id: sev-YYYYMMDD-NNNN-short-slug
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
    State the exact bounded work for local Codex/ION to perform.
  target:
    provider: local_ion
    root: ION_CODEX_FULL
  receipts:
    requested:
      - codex_work_packet_receipt
      - action_receipt
```

## Required Fields

- `schema`: must be `ion.chatops.action.v1`.
- `action_id`: concrete ID, never a placeholder.
- `intent`: one supported intent.
- `actor.callsign`: `Sev`.
- `actor.carrier`: `chatgpt_browser`.
- `authority.human_sovereign`: `Braden`.
- `authority.requires_approval`: usually `true`.
- `authority.production_authority`: `false`.
- `authority.live_execution_authority`: `false`.
- `receipts.requested`: list of requested proof outputs.

## Intent Defaults

| Intent | Use |
| --- | --- |
| `create_codex_work_packet` | Local Codex should inspect/build/test under ION gates |
| `write_file_draft` | Write a bounded draft file after approval |
| `register_artifact` | Register a bounded artifact reference |
| `create_github_issue_draft` | Draft issue text, not push or mutate GitHub directly |

## Extension Parser Limits

The MVP parser supports simple YAML mappings, scalar lists, booleans, numbers,
`null`, `[]`, and block text with `|`.

It does not support arbitrary YAML anchors, aliases, flow maps, or complex
list-of-object structures. Larger payloads should be moved through artifact refs
or daemon artifact transfer.

## Non-Claims

An emitted YAML block is not execution. Execution requires extension detection,
user approval, daemon/gateway acceptance, and a receipt.
