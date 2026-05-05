# V31 Summary Refresh Demo Release Candidate Capsule Plan

**Date:** 2026-04-25  
**Purpose:** Add a release-candidate capsule command over the certified demo evidence bundle.

## Command

```bash
PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_release_candidate --workspace-root .
```

## Capsule contents

```text
summary_refresh_demo_release_candidate_manifest.json
README.md
COMMANDS.sh
CHECKSUMS.sha256
evidence_bundle/
```

## Boundary

This command packages a certified demo release candidate. It does not widen mutation, rewrite summaries, mutate registries, mutate schedules, activate agents, claim global graph canon, or ratify provisional A3 surfaces.


## Verification

```text
Focused release-candidate suite:
Ran 6 tests in 0.115s
OK
```

## Live project-root release-candidate smoke

```bash
PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_release_candidate --workspace-root .
```

The smoke run produced a release-candidate capsule under:

```text
ION/05_context/history/demo_release_candidates/
```
