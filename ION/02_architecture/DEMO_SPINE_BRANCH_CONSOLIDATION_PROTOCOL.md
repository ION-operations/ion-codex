# DEMO SPINE BRANCH CONSOLIDATION PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-25  
**Authority posture:** A3 until reviewed  
**Purpose:** Govern consolidation of a demo-spine donor branch into the current release-readiness branch without downgrading later runtime gates.

---

## 1. Controlling law

```text
A donor branch may add missing capability, but it must not overwrite newer authority,
contract, readiness, or release-gate surfaces without explicit review.
```

V21 uses V20 as the authority base and V17 demo spine as a donor branch.

---

## 2. Merge posture

```text
base: V20 release-readiness branch
donor: V17 demo-spine merged branch
merge class: additive front-door runtime/demo spine consolidation
overwrite policy: no overwrite of V20 contract/readiness surfaces
registry policy: merge front-door rows into current-phase surface registry with corrected indentation
readiness policy: extend release readiness to require front-door demo surfaces
```

---

## 3. Non-loss clauses

This protocol is invalid if interpreted to allow:

1. V17 donor code to downgrade V20 contract-bound eventing;
2. front-door demo surfaces to bypass release readiness;
3. Persona Interface, Relay, and Steward roles to collapse;
4. demo-spine paths to be treated as final constitutional law;
5. donor registry content to replace newer V20 registry content wholesale;
6. packaging without test and receipt evidence.
