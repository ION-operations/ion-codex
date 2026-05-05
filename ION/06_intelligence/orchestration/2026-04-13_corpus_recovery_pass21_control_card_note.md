# Corpus recovery Pass 21 — control-card compression note

## What this pass does

Pass 21 compresses the atlas operating layer into a smaller practical control card.

New surfaces added:
- `00_program/atlas_control_card.md`
- `00_program/future_work_control_defaults_matrix.csv`

## Why this matters

The atlas already had:
- question-class control
- center-selection control
- posture control
- answer/output control
- landing-boundary control
- horizon/completion control

But those controls were still spread across too many files for fast practical use.

This pass creates one smaller entry layer that lets future work answer, in one place:
- what kind of question is this
- which center do I consult first
- what posture should I default to
- what output class is lawful
- where may it land
- may it widen at all

## Result

The operating layer is now harder to bypass through convenience and easier to follow without guessing.
