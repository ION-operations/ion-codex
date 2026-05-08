# Current branch vs precursor compaction register

## Compared lines
- current extracted branch: `ION/04_packages/kernel`
- production precursor pair:
  - `ION - Production/ION/04_packages/kernel`
  - `ION - Production/ION (codex branch)/04_packages/kernel`

## Static comparison
Current branch vs production precursor:
- current Python kernel modules: **89**
- production precursor Python kernel modules: **22**
- common same-path modules: **22**
- exact same content among those: **9**
- changed same-path modules: **13**
- current-only modules: **67**

Production `ION` vs `ION (codex branch)`:
- same-path modules: **22**
- exact same content: **22**
- interpretation: implementation-identical precursor pair with doc/state variation

## Executable posture
- production `ION`: `113 passed, 3 subtests passed`
- production `ION (codex branch)`: `113 passed, 3 subtests passed`
- current branch: `359 passed, 3 subtests passed`

## Judgment
The current branch is a **major expansion** of the compact precursor pair.

What it gains:
- more explicit law and governance surfaces
- many additional runtime/reporting/schedule/repair families
- more tests and more branch self-description

What it risks losing:
- compactness
- obvious center visibility
- atlas/kernel compression

## Conflict to preserve
The current branch is **broader and more explicit**, but the precursor pair remains a **stronger compact witness** of what an executable extracted core can look like.
