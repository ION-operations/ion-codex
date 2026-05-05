# Current parallelization strategy

## Why parallelization is allowed now

The activation/lifecycle reintegration cycle is complete and active-law emission for that pair has already occurred. The project is no longer deciding whether a first activation center exists; it is deciding how to advance the next bounded lanes without re-entering drift.

That makes this a good moment to parallelize the **review pipeline**, not the canon itself.

## Serial authority

The following remain serial and conductor-only:

- orchestration-board state
- selected-lane changes
- root orientation surfaces
- promotion judgments
- thaw judgments
- active-law emission
- any direct mutation under `ION/02_architecture/` unless explicitly authorized by the conductor

## Parallel authority

The following may run in branch chats:

- lane-specific delta analysis
- proposal-space surface design
- quarantined review drafts
- counterexample review
- worked examples
- install-path mapping
- promotion-candidate preparation

## Active topology

### Conductor
Maintains the single authoritative program state.

### Lane C runtime/session branch
Current selected work lane.
Horizon: review-entry through first promotion-candidate readiness.

### Lane A meta-template branch
Secondary background lane.
Horizon: design-space and quarantined-review preparation only.

### Adversarial audit branch
Cross-lane pressure test surface.
Horizon: detect overlap, carrier drift, adjacency sprawl, and false readiness.

## Explicit non-goals

This topology does not authorize:

- parallel active-law emission
- parallel root README / STATUS / SYSTEM_MAP updates
- broad code mutation
- freeform branch cleanup
- branch-local claims of canonical truth
