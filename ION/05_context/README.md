# ION Context

This directory contains active context, queues, receipts, runtime evidence,
handoffs, archives, and history.

## High-Traffic Areas

```text
current/       active packets, queues, receipts, connector state, work requests
archive/       contained or retired context evidence
comms/         communication and migration ledgers
graph/         context graph state
handoff/       handoff and succession packets
history/       historical receipts and runtime traces
inbox/         inbound work and staging lanes
signals/       signals and signal archives
```

## Current-State Rule

Files under `current/` are often operational evidence. Do not clean them by
moving or deleting without a lifecycle policy, receipt, and owner audit.

## Public Repo Rule

Because this repository is public, do not place secrets, tokens, private logs,
production infrastructure state, browser profiles, or sensitive user data in
context files.

## Useful Current Paths

- `current/ACTIVE_WORK_PACKET.json`
- `current/ACTIVE_CHATGPT_CONNECTOR_CODEX_WORK_QUEUE.json`
- `current/ACTIVE_CARRIER_MESSAGE_QUEUE.json`
- `current/github_data_plane/`
- `current/chatops_bridge/`
- `current/chatgpt_connector/`

