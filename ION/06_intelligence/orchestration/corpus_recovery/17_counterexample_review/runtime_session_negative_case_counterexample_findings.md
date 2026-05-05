# Runtime/session negative-case counterexample findings

## Purpose
Compress the main findings from the first adversarial negative-case review pass
against the Lane C runtime/session promotion candidate.

## Main findings

### 1. The current kernel already carries a real refusal spine
This branch is no longer guessing about negative cases.

The bounded current slice already refuses:
- invalid session identifiers,
- non-dispatch-ready queue items,
- dispatch-ready queue items missing `work_unit_id`,
- API entry without a lawful target session,
- API entry without `root_authority_ref` when creation is requested,
- malformed context attachment,
- carrier/context conflict,
- and invalid carrier-ref syntax.

That means the remaining blocker is no longer "do refusals exist at all?"
It is whether the unresolved edge cases are the right ones and remain
semantically bounded.

### 2. Queue-local truth is stronger than dispatch convenience
The healthiest current behavior is that queue state remains authoritative.

If a queue item is cancelled or otherwise not `DISPATCH_READY`, runtime/session
dispatch binding refuses the move instead of silently coercing it into kernel
dispatch. That is a real protection against scheduler-style annexation.

### 3. API refusal is legible, but still entry-centered
The API runtime entry slice now names several refusal dispositions explicitly.
That is good, but it is still fundamentally entry-centered refusal logic.

The unresolved question is not whether refusal exists.
It is how pause, re-entry, and closure behave after a lawful runtime history
already exists.

### 4. Pause and re-entry remain the real semantic edge
The active-law and current kernel slices can now show:
- creation,
- attachment,
- queue mutation,
- dispatch,
- refusal,
- and conflict.

What they do not yet show cleanly is:
- runtime pause as a first-class bounded posture,
- lawful re-entry under prior carrier/context state,
- or closure posture that stays subordinate to runtime/session authority while
  citing continuation/settlement law.

That is the real remaining edge set before thaw discussion can be honest.

## Resulting judgment
The runtime/session promotion candidate is stronger after this pass.

The blocker should now be named more narrowly:
- pause / re-entry / closure negative-case handling

It should not still be described as generic negative-case uncertainty.
