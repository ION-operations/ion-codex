# Canonical future-work answer and output classes

## Purpose

This file defines the smallest stable set of answer/output classes that future work should use after the question has been classified and the starting center has been chosen.

The goal is to reduce another recurring failure mode:
future work begins from a reasonable question class, but still produces the wrong kind of answer or artifact, causing silent widening, false landing, or accidental reinvention.

These classes are not ontology-final.
They are a working control layer for atlas-guided output discipline.

## Canonical classes

### 1. Consultation answer
Use when the work should answer from existing preserved centers without changing project truth.

Default artifact:
- advisory note in chat or a non-landing consultation note

Default landing boundary:
- no mutation to code or law
- optional advisory update only if explicitly useful

### 2. Comparison judgment
Use when the work must compare two or more preserved centers and record a difference, tension, or provisional conclusion.

Default artifact:
- comparison note
- lineage/supersession update
- conflict entry if unresolved

Default landing boundary:
- atlas/conflict layer only

### 3. Recovery note
Use when the work must recover missing historical evidence, restore context, or pull a buried center back into legible view.

Default artifact:
- recovery note
- profile update
- evidence receipt
- missing-evidence update

Default landing boundary:
- atlas/evidence layer only

### 4. Bridge-repair note
Use when the work is a narrow repair to the current branch that the atlas already recognizes as local bridge work.

Default artifact:
- branch-local clarification note
- narrow repair record
- template/protocol bridge update

Default landing boundary:
- current branch repair surfaces only
- no silent widening into new systems

### 5. Conflict entry
Use when the work discovers or sharpens a contradiction that should remain preserved instead of flattened.

Default artifact:
- conflict register entry
- contradiction ledger update

Default landing boundary:
- conflict layer only

### 6. Missing-evidence escalation
Use when the work cannot responsibly continue because evidence is absent or too weak.

Default artifact:
- missing-evidence register entry
- recover-first recommendation

Default landing boundary:
- missing-evidence layer only

### 7. Executable receipt
Use when the work has actually run or verified a historical or current implementation surface.

Default artifact:
- runnable verification receipt
- capability receipt

Default landing boundary:
- runnable proofs / recovery evidence layer

### 8. Lineage update
Use when the work clarifies predecessor, sibling, continuation, wrapper, or supersession status.

Default artifact:
- system profile update
- supersession graph update
- center-status adjustment

Default landing boundary:
- lineage / profile / center-status layer only

### 9. Atlas update
Use when the work improves the atlas operating layer itself without widening implementation.

Default artifact:
- atlas index/read-order/control update
- usage contract refinement
- control-layer refinement

Default landing boundary:
- atlas operating layer only

### 10. Bounded implementation packet
Use only when the atlas gate says the work is genuinely not satisfied by consultation, comparison, recovery, or bridge repair.

Default artifact:
- bounded implementation packet
- bounded implementation receipt

Default landing boundary:
- tightly scoped branch/code surface only
- must carry explicit non-reinvention proof

## Rule

If a work item can be satisfied by a narrower output class, it should not escalate to a wider one.

Default output priority should generally be:
consultation -> comparison -> recovery -> conflict/missing-evidence -> executable receipt -> bridge repair -> bounded implementation packet


## Landing-boundary pairing rule

Each answer/output class should also be paired with a landing-boundary class using:
- `canonical_landing_boundary_classes.md`
- `canonical_landing_boundary_defaults.csv`

Future work should always choose the narrowest lawful landing boundary that fits the chosen answer/output class.
