# Action Selection Matrix

## Use Uploaded Package

Use the mounted ZIP/package when:

- Actions are unavailable;
- the user asks conceptual/project-memory questions;
- no live local-hub proof exists;
- the work is draft/proposal/export-oriented.

## Use ION Action Gateway

Use Action Gateway when:

- checking public gateway health;
- reading policy/context pack;
- validating an `ion_action` packet;
- queueing a Codex work packet after approval;
- reading gateway receipts/status.

## Use ION MCP JSON-RPC

Use MCP JSON-RPC when:

- checking local ION status;
- listing tools;
- reading current operating packet;
- invoking bounded read/status tools;
- diagnosing local hub/service readiness.

## Use Extension YAML Bridge

Use fenced YAML when:

- the user is in browser chat and needs a human-approved local action proposal;
- the action is one of the supported MVP intents;
- the extension can receive/approve the proposal.

## Never

Never use chat text to collect passwords/tokens. Never claim a tool ran if only
a proposal was drafted.
