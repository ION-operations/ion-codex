# Activation/lifecycle thaw-readiness criteria

This note compresses the minimum criteria that must be satisfied before the activation/lifecycle set can enter thaw review.

## Required truths

### 1. Semantic independence with lawful coupling
Activation authority and executor lifecycle must be separable in meaning while still composing lawfully through the interface contract.

### 2. Denial and invalidation semantics
The set must state:
- who may deny enactment entry
- what invalidates a previously valid activation
- whether lifecycle may halt entry without re-adjudicating authority
- what must be emitted when entry is denied or invalidated

### 3. Continuation-safe re-entry
The set must explain how re-entry behaves after interruption, takeover, or bounded replay without inventing a second activation center.

### 4. Carrier-invariant enactment crossing
The meaning of “crossing into enactment” must remain invariant across manual, daemonized, bootstrap, and external carriers.

### 5. Settlement linkage
Lifecycle exit and settlement must remain legible to packet, receipt, and handoff law.

### 6. Promotion path
The repo must be able to answer:
- where the promoted surfaces would live
- which existing files they complement
- which existing files they constrain
- which existing files they do **not** replace

## Current outcome
These criteria are partially met in review space, but not yet met strongly enough for thaw review.
