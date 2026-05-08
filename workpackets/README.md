# ION Workpackets Lane

Status: operator/source packet intake lane, not accepted state.

This folder stores human-authored or model-authored workpackets that describe
planned ION work, bridge strategies, runbooks, OpenAPI candidates, Codex CLI
packets, product package plans, and research/protocol ideas.

Active implementation remains under:

```text
ION/
```

Workpackets are processed through:

```text
read -> classify -> compare to active build -> plan -> implement selected pieces -> validate -> receipt
```

Do not assume a workpacket is current simply because it exists. Check date,
status, overlap with already-implemented surfaces, and whether a newer receipt
or active file supersedes it.

## Current Inventory

See:

```text
WORKPACKET_INDEX_20260508T190626Z.json
```

The current lane has 20 files.

## Recommended Categories

- Action Gateway and Custom GPT Actions
- Codex CLI / IDE carrier setup
- Helixion bridge and tunnel operations
- Custom GPT browser/product package strategy
- self-knowledge / context export / monolith context protocols
- carrier friction, anti-theater, and action-hang triage

## Non-Claims

- A workpacket is not accepted law.
- A workpacket is not proof that work was completed.
- A workpacket does not override `ION/REPO_AUTHORITY.md`, current code,
  receipts, tests, or explicit operator instruction.
