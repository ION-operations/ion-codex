# SUMMARY REFRESH DEMO RELEASE CANDIDATE CAPSULE PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-25  
**Authority posture:** A3 until reviewed  
**Purpose:** Promote the certified summary-refresh demo evidence bundle into a release-candidate capsule for operator handoff and review.

---

## 1. Release-candidate law

```text
A release-candidate capsule may be assembled only from a certified evidence bundle,
unless explicitly emitted as BLOCKED evidence for failure analysis.
```

V29 certifies the demo. V30 packages evidence. V31 packages that evidence as a release-candidate capsule.

---

## 2. Required capsule contents

A V31 release-candidate capsule must include:

```text
release candidate manifest JSON
README.md
COMMANDS.sh
CHECKSUMS.sha256
copied evidence bundle directory
boundary statement
```

---

## 3. Command

```bash
PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_release_candidate --workspace-root .
```

---

## 4. Capsule location

```text
ION/05_context/history/demo_release_candidates/<release_candidate_id>/
```

---

## 5. Verdicts

```text
RELEASE_CANDIDATE
BLOCKED
```

`RELEASE_CANDIDATE` means the demo is certified and packaged for review/demo handoff.

It does **not** mean:

```text
full product completion
global graph canon
source-summary rewrite authority
agent activation authority
constitutional ratification of provisional A3 surfaces
```

---

## 6. Minimal test guards

```text
test_release_candidate_capsule_from_certified_evidence
test_release_candidate_capsule_copies_evidence_bundle
test_release_candidate_capsule_writes_checksums_and_commands
test_release_candidate_blocks_uncertified_by_default
test_release_readiness_requires_release_candidate_surface
```
