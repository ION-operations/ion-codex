# Pass 39 — Activation authority protocol review packet

## Purpose

Write the first **quarantined active-law draft** for Era 2 without pretending the law has already changed.

This packet takes the Lane B activation delta and the Lane B activation surface-design bundle and converts them into a reviewable candidate future protocol.

It does **not** ratify active law.
It creates a sharper review object so the project can test whether the proposed activation center is coherent enough to survive formal thaw/revision review.

## Control declaration

- Source lane: `corpus_recovery/13_controlled_reintegration/lane_b_activation_authority_delta_packet.md`
- Source design bundle: `corpus_recovery/14_surface_design/lane_b_activation_surface_design_packet.md`
- Question class: quarantined active-law drafting
- Default posture: review draft only
- Output class: candidate protocol + review matrix
- Landing boundary: review layer only
- Active installation into `02_architecture/`: forbidden in this pass

## Why activation is the first active-law candidate

Activation is the cleanest next candidate because the repo already has strong surfaces for:
- one-workflow doctrine,
- scheduler law,
- operator entry,
- capability registry,
- continuation/takeover,
- and packet/handoff law.

What remains missing is the explicit center that decides when candidate work lawfully crosses into executable enactment.

That missing center is too important to leave as implication.
But it is still risky to install directly into active law.
So the correct next step is a quarantined review draft.

## What this packet contains

1. a review-layer draft of `ACTIVATION_AUTHORITY_PROTOCOL`
2. a review matrix listing unresolved choices and pass/fail checks
3. a boundary statement that keeps executor lifecycle law separate

## Review questions that must now become explicit

The draft should survive review on the following questions:

1. **Jurisdiction** — does activation authority actually govern the boundary between candidate work and executable enactment, without swallowing scheduler law?
2. **Carrier neutrality** — can the draft describe manual, IDE, daemon, API, and later bounded multi-carrier execution without creating different workflows?
3. **Anti-theater discipline** — does the draft refuse fake autonomous swarm rhetoric while still leaving room for lawful bounded executor selection?
4. **Relation to continuation** — does it bind cleanly to takeover and handoff law without re-describing continuation ontology?
5. **Separation from lifecycle** — does it leave claim/readiness/release/failure transition detail to the future `EXECUTOR_LIFECYCLE_PROTOCOL`?

## Current best judgment

The activation center is now precise enough for a review draft.
It is **not** yet precise enough for active-law installation.

The most important sign of maturity here is that the draft can now say what activation authority owns **and what it must refuse to own**.

## Follow-up expectation

If this review draft survives scrutiny, the next paired move should be a quarantined draft for `EXECUTOR_LIFECYCLE_PROTOCOL`, not immediate installation into `02_architecture/`.

## Artifacts

- `drafts/ACTIVATION_AUTHORITY_PROTOCOL.review_draft.md`
- `activation_authority_protocol_review_matrix.csv`

## Pass result

The repo now has its first quarantined active-law candidate draft, giving Era 2 a concrete review object without silently mutating canon.
