# Atlas control lifecycle demonstration

## Purpose
This document demonstrates the full work-start lifecycle through the compressed atlas control layer.

The goal is to prove that future work can move from:
- question classification
- to center selection
- to posture selection
- to answer/output class
- to landing boundary
- to horizon/completion understanding
- to lawful landing

without improvising across the organism.

## Required lifecycle sequence

1. classify the question with `canonical_future_work_question_classes.md`
2. read the row in `future_work_control_defaults_matrix.csv`
3. consult the primary preserved center
4. check `conflict_register.md` and `missing_evidence_register.md`
5. choose the narrowest lawful posture
6. choose the narrowest lawful answer/output class
7. choose the lawful landing boundary
8. record process position and near/mid/far horizon
9. state the pass-level completion condition
10. produce only the allowed artifact
11. land only in the permitted boundary
12. record any new contradiction instead of flattening it

## Demonstration set

This pass includes three full lifecycle demonstrations:
- `control_lifecycle_examples/consult_only_runtime_lifecycle.md`
- `control_lifecycle_examples/recover_first_meta_template_lifecycle.md`
- `control_lifecycle_examples/bridge_repair_current_branch_lifecycle.md`

These are deliberately chosen because together they show:
- non-widening consultation
- recover-first atlas work
- tightly bounded current-branch repair

## Intended lesson

The operating layer is not only a gate on how work starts.
It is also a discipline on how work remains bounded through to its landing.
