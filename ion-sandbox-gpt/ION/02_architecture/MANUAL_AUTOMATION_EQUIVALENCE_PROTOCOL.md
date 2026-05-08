---
type: architecture_protocol
authority: A3_OPERATIONAL
created: 2026-04-09T19:20:00-04:00
status: ACTIVE
purpose: Prove that manual and automation carriers can carry the same bounded step under the same packet, takeover, and receipt discipline
connections:
  - ION/02_architecture/MANUAL_AUTOMATION_FALLBACK_PROTOCOL.md
  - ION/02_architecture/HANDOFF_TAKEOVER_NORMALIZATION_PROTOCOL.md
  - ION/02_architecture/HORIZON_PACKET_ENACTMENT_PROTOCOL.md
  - ION/04_packages/kernel/equivalence.py
  - ION/04_packages/kernel/horizon_state.py
  - ION/04_packages/kernel/takeover.py
  - ION/04_packages/kernel/operator_cli.py
  - ION/tests/test_kernel_manual_automation_equivalence.py
  - ION/tests/test_kernel_workflow_rehearsal.py
---

# Manual and Automation Equivalence Protocol

## Principle

Manual fallback and automation execution must be able to carry the same lawful step.

L3 does not claim every carrier is identical in embodiment.
It claims that for one bounded packet-ready step, the kernel can prove:
- the same source candidate was used,
- the same continuity boundary was preserved,
- the same required reads were carried,
- and the same packet/takeover witness discipline remained visible.

## Equivalence floor

The current L3 equivalence floor is bounded to one packet-ready horizon candidate.

From that same source candidate, the kernel should be able to emit:
- one automation-targeted canonical packet (`handoff` or `cursor_handoff`),
- one `manual_automation_fallback` packet,
- one takeover receipt for each packet,
- and one durable equivalence receipt linking the two paths.

## Compared invariants

The current bounded equivalence proof compares:
- candidate identity,
- source horizon ids,
- objective,
- scope binding,
- required reads,
- canonical packet validation success,
- and takeover-assessment success.

This is enough to prove a real symmetry floor without overstating total carrier sameness.

## Durable witness

L3 adds a durable kernel record family:
- `manual_automation_equivalence_receipt`

Each receipt should preserve:
- scope type and scope ref,
- source horizon ids and source layer,
- candidate item id and title,
- automation packet type and path,
- manual packet type and path,
- linked horizon enactment receipt ids,
- linked takeover receipt ids,
- shared objective,
- shared scope binding,
- shared required reads,
- the compared fields,
- and any visible warnings.

This receipt proves bounded equivalence witness.
It does not replace packet law, review law, or execution truth.

## Operator surface

The operator CLI should expose:
- `python -m kernel equivalence rehearse-horizon ...`
- `python -m kernel equivalence snapshot ...`
- `python -m kernel status ...` projection of the latest available equivalence receipt

## Boundaries

This protocol does not yet claim:
- context-perfect continuation,
- equivalence across every automation subsystem,
- or full branch/settlement-aware symmetry.

Those remain later work.

## Success condition

L3 succeeds when a packet-ready horizon candidate can be carried into both automation-targeted and manual-fallback continuity artifacts, both artifacts remain takeover-sufficient, both leave durable receipts, and the kernel can prove they preserved the same bounded step without hidden oral tradition.
