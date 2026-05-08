# V32 Summary Refresh Demo Release Candidate Verifier Plan

**Date:** 2026-04-25  
**Purpose:** Add an independent verifier for existing summary-refresh demo release-candidate capsules.

## Command

```bash
PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_release_candidate_verify --workspace-root .
```

## Specific capsule

```bash
PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_release_candidate_verify --workspace-root . --release-candidate-dir ION/05_context/history/demo_release_candidates/<id>
```

## Checks

```text
manifest exists/readable
verdict/certified status valid
README exists
COMMANDS exists
CHECKSUMS exists
evidence_bundle exists
checksums match
required commands present
forbidden boundary claims remain false
```

## Boundary

Verification reads and reports. It does not rerun certification, mutate graph state, rewrite summaries, mutate registries, mutate schedules, activate agents, or claim global graph canon.


## Verification

```text
Focused release-candidate verifier suite:
Ran 5 tests in 0.305s
OK
```

## Live verifier smoke

```bash
PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_release_candidate_verify --workspace-root .
```

The smoke verified the real V31 release-candidate capsule with zero checksum mismatches.
