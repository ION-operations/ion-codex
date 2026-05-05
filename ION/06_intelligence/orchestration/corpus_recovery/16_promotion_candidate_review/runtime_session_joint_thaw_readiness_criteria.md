# Runtime/session joint thaw-readiness criteria

This note compresses the minimum criteria that must be satisfied before the
runtime/session trio can enter thaw review.

## Required truths

### 1. Semantic independence with lawful coupling
Runtime session authority, session queue/dispatch, and API runtime entry must
be separable in meaning while still composing lawfully as one center stack.

### 2. Adjacent-layer discipline
The trio must state clearly that:
- scheduler law does not become queue law
- runtime-state witness/reporting does not become session authority
- supervised daemon or API shells do not become the center
- continuation and settlement do not replace runtime identity
- activation law is not silently re-imported through queue or entry language

### 3. Carrier-invariant runtime center
The meaning of the runtime/session center must remain invariant across
internal/manual, supervised daemon, and external/API attachment modes.

### 4. Continuity-safe pause and re-entry
The trio must explain how pause, resume, and lawful re-entry behave without
inventing a second identity center or collapsing into continuation-only logic.

### 5. Receipt and denial legibility
The trio must state:
- what witness proves session creation or re-entry
- what witness proves queue mutation or dispatch
- what witness proves API entry, refusal, or failure
- how closure posture is witnessed without settlement becoming the center

### 6. Promotion path
The repo must be able to answer:
- where the promoted surfaces would live
- which active-law files they complement
- which current files they constrain
- which current files they explicitly do **not** replace

## Current outcome
The promotion path is now strong enough to remove install-path ambiguity as a
primary blocker.
Receipt linkage is now strong enough in first bounded form.
Negative-case coverage is now strong enough in first bounded refusal form.
Pause/re-entry/closure handling is now strong enough in first bounded form.
These criteria are now strong enough for bounded thaw-readiness reassessment,
but not for direct active installation.
