# Pass 41 — Activation/lifecycle interface review packet

## Purpose

Review the **interface seam** between `ACTIVATION_AUTHORITY_PROTOCOL` and `EXECUTOR_LIFECYCLE_PROTOCOL` before either surface is considered for thaw or installation.

Passes 39 and 40 produced a matched pair of quarantined review drafts.
That solved the absence of explicit activation and lifecycle centers.
It did **not** yet prove that their boundary is clean.

This packet exists to test that boundary directly.

## Control declaration

- Source draft A: `corpus_recovery/15_quarantined_active_law_review/drafts/ACTIVATION_AUTHORITY_PROTOCOL.review_draft.md`
- Source draft B: `corpus_recovery/15_quarantined_active_law_review/drafts/EXECUTOR_LIFECYCLE_PROTOCOL.review_draft.md`
- Question class: quarantined interface review
- Default posture: seam clarification
- Output class: interface packet + review matrix + interface note
- Landing boundary: review layer only
- Active installation into `02_architecture/`: forbidden in this pass

## Why the seam needs its own packet

A common historical failure mode is to write two reasonable protocol surfaces and still leave their handoff undefined.
When that happens, the organism quietly regresses into implication:
- scheduler law starts impersonating activation,
- activation starts smuggling lifecycle claims,
- lifecycle starts re-deciding activation,
- or runtime/service shells start filling the seam with convenience behavior.

That is exactly the class of drift this packet is meant to prevent.

## Interface thesis

The clean boundary is:

- **Activation authority** governs whether a bounded enactment candidate may cross from candidate status into lawful enactment.
- **Executor lifecycle** begins only after that crossing is lawfully authorized or when preserved authority justifies lawful re-entry.
- The seam between them is the explicit handoff from `ActivationDecision(ALLOW)` to the first lifecycle transition set that binds an executor to the work.

## What this packet contains

1. a review packet describing the activation/lifecycle seam,
2. a matrix of boundary tests and failure modes,
3. a short review note that states the interface in minimal terms.

## Review questions that must now become explicit

1. **Crossing moment** — what exact event or object marks the boundary between activation judgment and lifecycle start?
2. **Authority reuse** — under what conditions may resume/re-entry rely on preserved authority rather than a fresh activation?
3. **Denial discipline** — can lifecycle ever deny what activation already allowed, or must it instead block entry due to failed prerequisites?
4. **Executor nomination** — is executor choice part of activation, lifecycle claim, or a bounded shared seam?
5. **Carrier neutrality** — can the seam remain one-workflow across manual, IDE, daemon, API, and bounded multi-carrier paths?

## Current best judgment

The seam should be governed by a narrow shared contract:

- activation emits an explicit enactment permission with scope, boundary, carrier/executor posture, prerequisites, and receipt identity,
- lifecycle consumes that permission to perform claim/readiness/entry transitions,
- and lifecycle may block or fail entry if prerequisites collapse, but it must not silently re-adjudicate activation authority.

That is the smallest clean split presently visible.

## Follow-up expectation

If this interface review survives scrutiny, the next lawful move is not installation.
It is a **promotion-candidate packet** that lists what would need to be true for the activation/lifecycle pair to enter thaw review together.

## Artifacts

- `activation_lifecycle_interface_review_matrix.csv`
- `drafts/ACTIVATION_LIFECYCLE_INTERFACE.review_note.md`

## Pass result

The repo now has an explicit review object for the seam between activation authority and executor lifecycle, reducing the risk that the pair remains only locally coherent while globally ambiguous.
