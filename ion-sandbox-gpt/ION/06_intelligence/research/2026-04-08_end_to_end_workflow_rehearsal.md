---
type: research
template: RESEARCH
created: 2026-04-08T19:20:00-04:00
status: ACTIVE
connections:
  - ION/tests/test_kernel_workflow_rehearsal.py
  - ION/01_doctrine/CANONICAL_WORKFLOW.md
  - ION/AGENT_CONTRACT.md
---

# End-to-end workflow rehearsal

This artifact names the repository's first explicit workflow proof center.

## Rehearsal claim

A lawful executor should be able to:
1. read state,
2. compile bounded context,
3. emit a manual/sequential packet bundle,
4. hand a bounded step to a supervised automated carrier,
5. accept the result back as proposal,
6. keep kernel truth gated,
7. generate the next operational witness surfaces.

## Current proof entrypoint

`ION/tests/test_kernel_workflow_rehearsal.py`

## What the test proves now

- bounded context compilation from kernel truth,
- sequential/manual carrier packet generation through `sequential_kernel.py`,
- explicit role-session update recording,
- supervised runtime start / status packaging,
- supervised external execution export,
- bounded external return acceptance back into the normal validating path,
- horizon state persistence and lawful tightening,
- direct-render vs CLI-write carrier symmetry for the enacted packet,
- enactment receipt persistence and packet validation,
- latest horizon/receipt projection through operator status,
- runbook and acceptance packaging over the live service stack.

## What it does not yet prove

- full multi-generation child-work family issuance and replay in one single scenario,
- second-executor blind continuation / takeover from K6 outputs alone,
- full review interruption inside the same rehearsal,
- parallel swarm execution.

Those should be follow-on rehearsal expansions, not reasons to keep the current loop implicit.
