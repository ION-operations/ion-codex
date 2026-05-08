---
type: architecture_protocol
authority: A3_OPERATIONAL
created: 2026-04-09T18:10:00-04:00
status: ACTIVE
purpose: Normalize bounded packet takeover assessment, derived continuation scaffolds, and durable takeover receipts in the canonical kernel
connections:
  - ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md
  - ION/02_architecture/MANUAL_AUTOMATION_FALLBACK_PROTOCOL.md
  - ION/04_packages/kernel/packet_validation.py
  - ION/04_packages/kernel/takeover.py
  - ION/04_packages/kernel/operator_cli.py
  - ION/tests/test_kernel_packet_validation.py
  - ION/tests/test_kernel_takeover.py
  - ION/tests/test_kernel_workflow_rehearsal.py
---

# Handoff and Takeover Normalization Protocol

## Principle

Takeover sufficiency must be explicit, assessable, and durable.

It is not enough for a packet to "feel understandable" to the current operator.
The system should be able to:
- assess whether a packet is sufficient for one bounded takeover step,
- render a lawful second-executor role session from that packet when it is sufficient,
- and persist a durable witness that the takeover boundary was explicit at that moment.

## Continuation-normalized packet families

The current continuation-normalized packet families are:
- `handoff`
- `cursor_handoff`
- `role_session`
- `manual_automation_fallback`

These families now have explicit takeover assessment support.

`task` remains a canonical packet family, but it is not yet guaranteed takeover-sufficient by law.
It may be assessed, but insufficient context should remain visible rather than being silently guessed.

## Required takeover assessment fields

A packet is takeover-sufficient only when it can yield, at minimum:
- objective,
- explicit scope binding,
- explicit required reads,
- explicit next action,
- target executor or target surface when applicable,
- and expected output family when present.

Warnings must remain visible when any of those fields are missing or degraded.

## Derived role-session law

When a packet is takeover-sufficient, the kernel may render one derived `role_session` packet for the next executor.

That derived role session must preserve:
- source packet type,
- source packet path when available,
- source packet timestamp and status when available,
- the same scope binding,
- the same required reads,
- and the bounded next action only.

It must not silently reconstruct missing context or widen the assignment.

## Durable takeover witness

L2 adds a durable kernel record family:
- `takeover_assessment_receipt`

Each receipt should preserve:
- scope type and scope ref,
- source packet path and relative path when available,
- packet checksum,
- packet family, title, created timestamp, and status when available,
- assessed objective,
- target executor or target surface when available,
- required reads,
- next action,
- expected output,
- and any warnings that remained visible at record time.

This receipt is witness, not authority.
It proves that continuation sufficiency was explicit; it does not itself authorize writes or replace packet law.

## Operator surfaces

The operator CLI should expose:
- `python -m kernel packet assess-takeover ...`
- `python -m kernel packet render-takeover-role-session ...`
- `python -m kernel packet record-takeover ...`
- `python -m kernel status ...` projection of the latest available takeover receipt

These surfaces exist to make continuation proof operational rather than test-only.

## Boundaries

This protocol does not claim:
- context-perfect continuation,
- manual and automation equivalence,
- or total takeover sufficiency for every packet family and every carrier.

Those remain later proof tracks.

## Success condition

L2 succeeds when a fresh capable executor can receive a lawful packet, assess its takeover sufficiency explicitly, derive one bounded continuation packet from it, and leave behind a durable witness of that takeover boundary without hidden oral tradition.

## Activation/lifecycle boundary clarification

Normalized takeover preserves continuity and handoff truth.
It does not create a new enactment authority by itself.
A takeover path may carry preserved activation lineage when the work is still lawfully live, but missing or invalid activation may not be reconstructed by takeover normalization alone.
Executor re-entry after takeover therefore still owes lawful lifecycle transition handling under `ION/02_architecture/EXECUTOR_LIFECYCLE_PROTOCOL.md`.
