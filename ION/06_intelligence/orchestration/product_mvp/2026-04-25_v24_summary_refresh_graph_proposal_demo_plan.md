# V24 Summary Refresh Graph Proposal Demo Plan

**Date:** 2026-04-25  
**Purpose:** Extend the summary-refresh demo into Phase 4 proposal-only graph writeback.

## Path

```text
front-door turn
→ summary-refresh request template
→ contract-bound completion witness
→ contract-bound reaction selection
→ projection-only index surface
→ proposal-only graph writeback surface
→ controlled Relay/Persona return
```

## Boundary

Phase 4 creates proposal evidence only. It does not commit graph state, rewrite source summaries, or mutate graph truth.


## Verification

```text
Ran 91 tests in 3.722s
OK
```

## Current demo depth

```text
front-door ingress
→ template request
→ completion witness
→ reaction selection
→ projection-only index surface
→ proposal-only graph writeback surface
→ persona return
```
