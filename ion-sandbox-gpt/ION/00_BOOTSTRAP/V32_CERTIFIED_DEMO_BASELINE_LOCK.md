# V32 Certified Demo Baseline Lock

**Status:** Baseline lock  
**Date:** 2026-04-25  
**Authority posture:** A2 evidence-preservation / A3 production-readiness planning

V32 is frozen as the certified release-demo baseline for the summary-refresh spine.

The locked proof chain is:

```text
front-door -> template -> event -> reaction -> projection -> proposal -> review -> bounded commit -> replay -> doctor -> certification -> evidence bundle -> release-candidate capsule -> independent verifier
```

## Lock rule

No post-V32 production work may weaken, overwrite, or silently reinterpret the V32 certified demo evidence. New work must build above this baseline, explicitly refactor demo-specific surfaces into production primitives while preserving V32 behavior, or deprecate a V32 surface with a receipt, replacement, and compatibility test.

## Non-production boundary retained by lock

V32 remains a certified bounded demo, not full production authority. It does not authorize source-summary rewrite, global graph canon mutation, registry mutation, schedule mutation, agent activation, or constitutional ratification of provisional A3 surfaces.
