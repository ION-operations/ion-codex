---
type: protocol
authority: A2_EXECUTOR
created: 2026-04-08T20:20:00-04:00
status: ACTIVE
connections:
  - ION/02_architecture/MANUAL_AUTOMATION_EQUIVALENCE_PROTOCOL.md
  - ION/02_architecture/HANDOFF_TAKEOVER_NORMALIZATION_PROTOCOL.md
---

# Manual Automation Fallback Protocol

## Supreme statement

When automation is unavailable, disabled, blocked, or intentionally held, the current executor must be able to perform the same next lawful automation step manually.

Manual fallback is **not** a different workflow. It is the same workflow with the executor carrying the automation transition directly.

## Trigger conditions

Manual fallback may be invoked when:
- automation mode is disabled,
- the runtime is held / drained / stopped,
- the daemon carrier is unavailable,
- an external execution bridge is unavailable,
- or doctrine explicitly requires manual handling.

## Required behavior

The current executor must:
1. identify the blocked automation service or carrier,
2. read the same bounded context the automation carrier would have used,
3. perform one bounded step only,
4. emit the same class of lawful outputs the carrier would have produced where possible,
5. preserve receipts / handoff / unresolved risk.

## Examples

- child-work issuance performed manually from the same manifest/pressure state
- external execution packet prepared manually for a local IDE worker
- daemon-carried next-step packet compiled manually under runtime hold
- recovery replay handled manually using the same resumable service receipt

## What manual fallback may not do

- silently widen the step boundary
- bypass governed write / validation / review
- hide that fallback occurred
- invent a different packet family than the carrier would have used

## L3 equivalence link

Manual fallback is now also part of the bounded L3 equivalence proof floor.

That means one packet-ready horizon candidate may be rendered into:
- one automation-targeted canonical packet,
- one `manual_automation_fallback` packet,
- linked takeover receipts for both,
- and one explicit equivalence receipt proving the same bounded step survived both paths.
