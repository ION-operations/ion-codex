# Activation/lifecycle joint bounded thaw packet

## Purpose

This packet opens the first lawful thaw-review entry for the coupled activation/lifecycle candidate.

It answers the exact question left open by Pass 47:

**What is the precise active-file touch set, adjacency-edit set, and review-only remainder for the activation/lifecycle pair if bounded thaw review begins now?**

This packet does **not** close thaw review.
It does **not** install active files into `ION/02_architecture/`.
It defines the bounded review perimeter that thaw review will use.

## Candidate set under thaw review entry

Primary candidate surfaces:
- `15_quarantined_active_law_review/drafts/ACTIVATION_AUTHORITY_PROTOCOL.review_draft.md`
- `15_quarantined_active_law_review/drafts/EXECUTOR_LIFECYCLE_PROTOCOL.review_draft.md`

Coupling / review support surfaces:
- `15_quarantined_active_law_review/drafts/ACTIVATION_LIFECYCLE_INTERFACE.review_note.md`
- `17_counterexample_review/activation_lifecycle_overlap_counterexample_findings.md`
- `18_worked_examples/activation_lifecycle_carrier_crossing_worked_examples.md`
- `18_worked_examples/activation_lifecycle_receipt_settlement_worked_examples.md`
- `19_install_path_mapping/activation_lifecycle_install_path_mapping.md`
- `20_thaw_readiness_reassessment/activation_lifecycle_joint_thaw_readiness_reassessment.md`

## Bounded thaw entry judgment

### Judgment
**Open bounded thaw review: yes.**

### Meaning
The repo may now review the coupled pair as a real prospective active insertion with:
- exact destination files
- exact adjacent-file amendment candidates
- exact review-only remainder
- explicit no-direct-install boundary

### Meaning this packet rejects
This packet rejects:
- direct promotion to active law
- unilateral thaw of only one half of the pair
- adjacency edits expanding beyond the named touch set
- silent replacement of scheduler, capability, continuation, or settlement law

## Exact active destination files

If thaw review closes successfully, only these two new active files are eligible to be created:

1. `ION/02_architecture/ACTIVATION_AUTHORITY_PROTOCOL.md`
2. `ION/02_architecture/EXECUTOR_LIFECYCLE_PROTOCOL.md`

No other active architecture file is authorized for creation by this thaw packet.

## Exact adjacent-file amendment set

The bounded thaw review may propose amendments only to the following existing active files:

- `ION/README.md`
- `ION/STATUS.md`
- `ION/SYSTEM_MAP.md`
- `ION/MASTER_ORCHESTRATION_INDEX.md`
- `ION/02_architecture/LAWFUL_ORCHESTRATION_SCHEDULER_PROTOCOL.md`
- `ION/02_architecture/EXECUTOR_CAPABILITY_REGISTRY_PROTOCOL.md`
- `ION/02_architecture/PACKET_AND_HANDOFF_STANDARDIZATION_PROTOCOL.md`
- `ION/02_architecture/HANDOFF_TAKEOVER_NORMALIZATION_PROTOCOL.md`
- `ION/02_architecture/CONTEXT_PERFECT_CONTINUATION_PROTOCOL.md`
- `ION/02_architecture/BOUNDED_PARALLELISM_AND_SETTLEMENT_PROTOCOL.md`

These amendments are review-bounded to:
- cross-reference insertion
- boundary clarification
- read-order / map visibility
- explicit non-replacement statements

This thaw packet does **not** authorize semantic rewrites of those files.

## Review-only remainder

The following surfaces remain non-canonical and review-only even after thaw review entry opens:
- all `15_quarantined_active_law_review/` drafts and matrices
- all `16_promotion_candidate_review/` artifacts
- all `17_counterexample_review/` artifacts
- all `18_worked_examples/` artifacts
- all `19_install_path_mapping/` artifacts
- all `20_thaw_readiness_reassessment/` artifacts
- this `21_bounded_thaw_packet/` layer itself

These surfaces justify, constrain, and explain the thaw.
They do not become active law by citation alone.

## Mandatory thaw-review questions

Before thaw review can close, the repo must answer all of these:

1. Do the candidate active files preserve the activation/lifecycle boundary without reintroducing scheduler creep?
2. Do the proposed adjacent-file amendments remain strictly cross-referential and boundary-preserving?
3. Are continuation, takeover, and settlement surfaces left intact as adjacent law rather than annexed into the new pair?
4. Does the coupled pair remain promotion-coupled all the way to closure?
5. Is the review-only remainder still clearly marked non-canonical after active insertion is proposed?

## Closure conditions

Bounded thaw review may close only if:
- both active destination files are accepted together
- the adjacent-file amendment list stays inside the named touch set
- explicit non-replacement language is retained
- the review-only remainder is preserved as review-only
- the resulting active-law insertion does not require widening into runtime/session or meta-template thaw in the same packet

## Lawful next move

Use this packet as the entry perimeter for the first coupled thaw review on:
- `ION/02_architecture/ACTIVATION_AUTHORITY_PROTOCOL.md`
- `ION/02_architecture/EXECUTOR_LIFECYCLE_PROTOCOL.md`

Any attempt to add more active files, widen adjacency, or decouple the pair should be treated as a new packet, not as part of this thaw.
