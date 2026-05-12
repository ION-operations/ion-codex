# ION Extension Queue Protocol Context Package v0.1 (Candidate)

This candidate package defines queue taxonomy, packet lifecycle, selected-request start behavior, editable queue packet controls, visibility/redaction, and settlement semantics for the extension cockpit.

Status: `CANDIDATE_NOT_ACCEPTED`

Scope:
- Codex work queue
- Browser/self-chat queue
- Carrier-message queue
- Action/approval receipt queue projections
- Agent invocation queue
- Branch carrier messages
- Agent class + context binding classification
- Queue result capture and settlement

Core UX correction:
- `Start queue head` and `Start selected request` are distinct actions.
- Safe default for branch work: `Start selected request` only.
