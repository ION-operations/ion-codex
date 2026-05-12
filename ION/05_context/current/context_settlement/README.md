# ION Context Settlement Lane

Status: active provisional settlement lane
Created: 2026-05-11

This folder serializes shared context updates when multiple agents are active.

Workers may write candidate packets here. Workers must not directly assign checkpoint numbers or mutate settled shared context.

Settled shared context includes:

```text
ION/05_context/current/codex_solo/CAPSULE.md
ION/05_context/current/codex_solo/MINI.md
ION/05_context/current/codex_solo/HOT_CONTEXT.md
ION/05_context/current/codex_solo/STATUS.json
ION/05_context/current/codex_solo/ROUTE.json
```

Folders:

```text
claims/    active write-scope claims
inbox/     candidate packets awaiting settlement
accepted/  settler-approved packets and generated context updates
conflicts/ conflict receipts and collision records
```

Current source protocol:

```text
ION/02_architecture/ION_MULTI_AGENT_CONTEXT_AND_WORKPACKET_SETTLEMENT_PROTOCOL_V0_1.md
```

Current imported workpacket/diff control artifact:

```text
ION_CODEX FULL/workpackets/ion_workpackets_diffs_ingestion_002_20260510T234208.zip
```

Core law:

```text
parallel agents produce candidate receipts
settlement lane serializes accepted context
only the context settler assigns C-numbers
```
