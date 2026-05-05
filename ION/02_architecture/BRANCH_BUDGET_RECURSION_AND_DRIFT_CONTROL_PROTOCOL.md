---
type: architecture_protocol
authority: A3_OPERATIONAL
created: 2026-04-10T03:00:00-04:00
status: ACTIVE
purpose: Define explicit branch-budget posture, recursion ceilings, stale-claim decay, and stale-return drift handling on top of the bounded fan-out / fan-in loop
connections:
  - ION/02_architecture/BOUNDED_PARALLELISM_AND_SETTLEMENT_PROTOCOL.md
  - ION/02_architecture/BOUNDED_MULTI_AGENT_ALLOCATOR_PROTOCOL.md
  - ION/02_architecture/FAN_IN_MERGE_REVIEW_SETTLEMENT_PROTOCOL.md
  - ION/06_intelligence/orchestration/2026-04-10_post_m3_state_forward_path_and_codex_handoff.md
---

# Branch Budget / Recursion / Drift Control Protocol

## Principle

Once bounded fan-out and bounded fan-in exist, branch growth itself becomes a governed surface.
M3 exists so the branch loop cannot silently widen into uncontrolled recursion, dead active claims, or orphaned child returns.

## Law

The parent scope now carries explicit branch-control posture.
At minimum that posture must answer:
- how many active branches are lawful now,
- whether the current parent may re-fan-out,
- which active claims have decayed into stale budget pressure,
- and whether any child returns now exist outside the active claim set.

## Budget law

The default budget surface is the parent work unit's spawn policy.
When a bounded override is passed, the lower ceiling governs.
Active non-stale claims consume budget.
Stale claims may be decay candidates; they must not remain invisible permanent consumers.

## Recursion law

Recursive re-fan-out is refused once the configured branch depth ceiling is reached.
M3 does not widen recursion law.
It makes the current bounded refusal explicit.

## Stale-claim law

An active claim that ages beyond the stale window without a child return becomes a stale-claim candidate.
The system may surface it, decay it, and exclude it from effective budget posture.
Decay must remain explicit; it must not happen as a hidden side effect.

## Stale-return law

A child return that no longer belongs to the active claim set is a stale return.
It must not be ignored silently.
M3 treats stale returns as drift pressure that later settlement or review must see.

## Receipt law

M3 adds the canonical witness family:
- `branch_control_receipt`

That receipt preserves:
- parent scope,
- branch depth,
- effective budget posture,
- stale-claim set,
- decayed claim set when decay occurs,
- stale-return set,
- recursion refusal posture,
- and the next recommended control action.

## Relation to allocator and settlement

Allocator law now reads branch-control posture before selecting children.
Settlement law now sees stale-return pressure explicitly rather than silently ignoring off-claim returns.
M3 does not replace allocator or settlement law.
It constrains their legitimacy.

## Boundaries

M3 does not yet land:
- branch-aware horizon synchronization,
- branch-aware schedule projection updates,
- or wide swarm posture.

Those remain later work.

## Success condition

M3 succeeds when the kernel can:
- project explicit branch-control posture,
- refuse recursive fan-out beyond the current depth ceiling,
- decay stale claims,
- surface stale returns as review pressure,
- and expose all of that through canonical receipts, CLI, status, and focused rehearsal.
