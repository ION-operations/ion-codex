# Corpus recovery pass 28 — kernel thaw/revision protocol note

## What this pass adds
- project control kernel revision and thaw protocol
- kernel change-class matrix
- kernel revision record template
- frozen-kernel change path

## Why this matters
The frozen default project control kernel is now strong enough to govern work-start discipline.
That creates a new risk: informal bypass or ad hoc change whenever the kernel becomes inconvenient.

This pass closes that gap by requiring any revision to move through:
- explicit trigger
- explicit insufficiency evidence
- smallest change class
- declared thaw record
- explicit re-freeze outcome

## Current judgment
The project now has not only a frozen default control baseline, but also a lawful path for changing that baseline without collapsing back into unmanaged drift.
