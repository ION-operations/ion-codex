# SUMMARY REFRESH DEMO RELEASE CANDIDATE VERIFIER PROTOCOL

**Status:** Current-phase operational proposal  
**Date:** 2026-04-25  
**Authority posture:** A3 until reviewed  
**Purpose:** Verify an existing summary-refresh demo release-candidate capsule without rerunning certification or regenerating evidence.

---

## 1. Verification law

```text
A release-candidate capsule is independently verifiable only if its manifest,
commands, README, copied evidence bundle, and checksum ledger are present and
the checksum ledger matches the current capsule contents.
```

V31 creates release-candidate capsules. V32 verifies them.

---

## 2. Required verification checks

The verifier must check:

```text
release candidate directory exists
manifest JSON exists and is readable
manifest verdict is RELEASE_CANDIDATE unless blocked mode is explicitly allowed
certified is true unless blocked mode is explicitly allowed
README.md exists
COMMANDS.sh exists
CHECKSUMS.sha256 exists
copied evidence_bundle/ directory exists
checksums match all files listed in CHECKSUMS.sha256
required commands are present
boundary claims are false for forbidden mutation claims
```

---

## 3. Command

Verify the latest capsule:

```bash
PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_release_candidate_verify --workspace-root .
```

Verify a specific capsule:

```bash
PYTHONPATH=ION/04_packages python -S -m kernel.summary_refresh_demo_release_candidate_verify --workspace-root . --release-candidate-dir ION/05_context/history/demo_release_candidates/<id>
```

---

## 4. Report location

```text
ION/05_context/history/demo_release_candidate_verifications/
```

---

## 5. Verdicts

```text
VERIFIED
FAILED
```

`VERIFIED` means the release-candidate capsule is structurally intact, checksum-consistent, certified, and evidence-backed.

It does not mean full product completion, global graph canon, or constitutional ratification.

---

## 6. Minimal test guards

```text
test_release_candidate_verifier_verifies_valid_capsule
test_release_candidate_verifier_detects_checksum_mismatch
test_release_candidate_verifier_cli_prints_summary
test_release_candidate_verifier_finds_latest_capsule
test_release_readiness_requires_release_candidate_verifier_surface
```
