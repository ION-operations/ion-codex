# Project control kernel revision and thaw protocol

## Purpose

The default project control kernel is now frozen as the long-lived work-control baseline.
That freeze must not be mistaken for immobility.

This protocol defines the only lawful path for revising or thawing the frozen kernel without falling back into ad hoc control drift.

## Core rule

The frozen kernel may be revised only through a **declared thaw path**.
A thaw path is lawful only when all of the following are true:
- the motivating pressure is explicit
- the kernel insufficiency is evidenced
- preserved conflicts have been checked
- the smallest possible change class is selected
- the revised kernel can be re-frozen with a new judgment

## Allowed thaw triggers

A thaw proposal is allowed only when at least one of the following holds:
- a control-surface contradiction prevents lawful work-start
- a question class cannot be routed honestly through the frozen kernel
- a landing/output rule creates repeated lawful dead-ends
- a preserved center shows that the frozen kernel omits a control necessity already known elsewhere in the estate
- a repeated reassessment trigger shows the kernel is too small or misordered for real work

## Forbidden thaw motives

A thaw proposal is not lawful when the real motive is:
- convenience
- impatience
- a desire to skip conflict preservation
- a desire to treat the newest line as the default truth without atlas comparison
- an attempt to widen work before proving that the kernel is actually insufficient

## Change classes

Use the smallest change class that fits the evidence:
- clarification only
- ordering correction
- defaults correction
- new control primitive
- freeze rollback

Each change class has different evidence and re-freeze requirements.
Consult `project_control_kernel_change_classes.csv`.

## Required thaw record

Any thaw/revision proposal must create a record using:
- `project_control_kernel_revision_record_template.md`

At minimum it must state:
- trigger
- insufficiency evidence
- affected kernel surfaces
- change class
- preserved conflicts consulted
- widening needed or not
- re-freeze condition

## Re-freeze rule

Any accepted thaw must end in one of these states:
- re-frozen with clarified kernel
- re-frozen with expanded kernel
- rolled back and original freeze retained

The kernel may not remain indefinitely in a vague thawed state.

## Why this exists

The project repeatedly drifted because frozen or stable centers were later bypassed informally.
This protocol exists so the frozen kernel can evolve only through an auditable, bounded, and re-freezable path.

## Approval and lifecycle companions

Use the following companion surfaces when a thaw path is opened:
- `project_control_kernel_revision_approval_matrix.csv`
- `project_control_kernel_revision_lifecycle.md`
- `project_control_kernel_revision_examples/README.md`

These help distinguish simple clarifications from higher-risk kernel changes.
