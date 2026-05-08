# Production Readiness Gap Register

**Status:** Current-phase gap register  
**Date:** 2026-04-25

## Critical gaps before production

```text
G1: provisional A3 surfaces require ratification
G2: demo-specific workflow code must split from reusable workflow primitives
G3: global graph canon is not ratified
G4: source-summary rewrite authority is not implemented
G5: agent/subagent activation authority is not implemented
G6: daemon runtime loop is not productionized
G7: rollback and migration law are incomplete for production graph state
G8: adversarial production audit is not complete
```

ION has a verified release-demo chain through release-candidate verification. This is strong enough to serve as the production baseline, but not enough to claim production runtime authority.


## V34 consistency note

V34 aligns the executable production-readiness report with this register.
The kernel report must include G7 rollback/migration law as a critical gap and
must forbid production graph migration authorization until explicit rollback,
migration, replay, and reversibility law exists.
