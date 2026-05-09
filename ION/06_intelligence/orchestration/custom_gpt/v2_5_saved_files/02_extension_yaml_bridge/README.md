# ION Browser Extension YAML Bridge

## Purpose

The browser extension lets the ION Custom GPT present bounded action proposals
as YAML blocks in ChatGPT. The extension detects `ion_action:`, validates the
packet, asks the user for approval, forwards approved actions to the local
daemon, and surfaces receipts.

The GPT must treat YAML as a proposal until extension approval and daemon
receipt prove otherwise.

## Live Implemented Tag

```yaml
ion_action:
```

The first YAML key must be `ion_action:`. Prose describing YAML is not enough.

## Supported MVP Intents

- `register_artifact`
- `write_file_draft`
- `create_codex_work_packet`
- `create_github_issue_draft`

## Hard-Gated Intents

- `delete_file`
- `overwrite_protected_file`
- `push_main`
- `access_credential`
- `production_deploy`
- `broad_shell`

## Candidate Future Tags

These names are useful for planning but are not live unless the extension or
gateway proves support:

- `ion_connect`
- `ion_reentry`
- `ion_receipt`

`ion_reentry` is expected to be inbound proof from the extension/gateway into
the GPT, not a free-form user claim.

## Source Anchors

- `ION/09_integrations/browser_extension/ion_chatops_bridge/README.md`
- `ION/09_integrations/browser_extension/ion_chatops_bridge/src/schema.ts`
- `ION/09_integrations/browser_extension/ion_chatops_bridge/examples/SEV_CHATOPS_SMOKE.yaml`

## GPT Behavior

Use `ion_action` when the user asks for local ION to do bounded work and an
extension/daemon lane is available or plausibly configured. Prefer
`create_codex_work_packet` for implementation work so local Codex can inspect
the repo, run tests, and return proof.
