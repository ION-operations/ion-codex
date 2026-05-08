---
type: clarification
authority: A3_OPERATIONAL
created: 2026-04-17T00:00:00-04:00
status: ACTIVE
purpose: Clarify extracted-branch shell root versus inner packaged content root before further reintegration execution
connections:
  - ION/REPO_AUTHORITY.md
  - ION/06_intelligence/orchestration/2026-04-17_post_q005_execution_phase_readiness_assessment.md
  - ION/06_intelligence/decisions/2026-04-17_top_level_production_surface_promotion_map_canonicalization_decision.md
  - ION/tests/test_packaging_entry_posture.py
  - /home/sev/ION - Production/ION most recent/ion_current_canonical_runtime_fleet_temporal_2026-04-16/pyproject.toml
  - /home/sev/ION - Production/ION/pyproject.toml
---

# Branch-Root Shell vs Content-Root Clarification

## Purpose

This note closes one specific confusion that distorted the first post-q005
readiness read:

- the extracted current-generation branch has a real packaging surface
- that packaging surface lives at the extracted branch shell root
- the inner `ION/` directory remains the canonical content root

Those are not competing truths. They are two different layers of the same
extracted branch.

## Root distinction

Inside this extracted branch, the two important paths are:

- **shell root**:
  `/home/sev/ION - Production/ION most recent/ion_current_canonical_runtime_fleet_temporal_2026-04-16`
- **content root**:
  `/home/sev/ION - Production/ION most recent/ion_current_canonical_runtime_fleet_temporal_2026-04-16/ION`

The shell root is where `pyproject.toml` lives and where editable-install /
pytest configuration is anchored.

The content root is where doctrine, architecture, registry, templates, code,
and tests live under the `ION/` subtree.

## What was wrong in the earlier read

The earlier readiness read treated the inner `ION/` directory as if it were
also the packaging root. That was incorrect.

The extracted branch already has:

- `pyproject.toml` at the shell root
- `ION/tests/test_packaging_entry_posture.py` proving that shell-root
  packaging surface exists and points at `ION/04_packages`

So the true issue is not "missing packaging."

The true issue is that commands run from the inner `ION/` directory without an
editable install can bypass the shell-root packaging configuration and fall
through to an already-installed top-level production `ion-kernel`.

## Proof gathered

### Positive proof: shell-root editable install works

From the extracted branch shell root, in a clean temporary virtual
environment:

1. `python -m pip install -e .` succeeded
2. `import kernel` resolved to:
   `/home/sev/ION - Production/ION most recent/ion_current_canonical_runtime_fleet_temporal_2026-04-16/ION/04_packages/kernel/__init__.py`
3. `python -m kernel --help` exited successfully
4. `python -m pytest ION/tests/test_packaging_entry_posture.py -q` passed

That means the extracted branch packaging floor is real.

### Negative proof: inner content-root commands can mislead

From the inner `ION/` directory, without editable install:

`env -u PYTHONPATH python3 - <<'PY'`
`import kernel`
`print(kernel.__file__)`
`PY`

resolved to the top-level production installation at:

`/home/sev/ION - Production/ION/04_packages/kernel/__init__.py`

That is a startup / working-directory ambiguity, not evidence that the
extracted branch lacks packaging.

## Consequence for q003

The top-level production `ION/pyproject.toml` is not a missing first-wave
packaging floor that the extracted branch lacks.

Instead:

- the extracted branch already owns a minimal packaging floor at its shell root
- the top-level production `ION/pyproject.toml` and
  `ION/04_packages/kernel/preflight_cli.py` are both coupled to the later
  API/MCP service layer

So they should not be treated as standalone Class-A promotion surfaces.

## Practical rule going forward

When the task is package-aware, distinguish the two roots explicitly:

- use the **shell root** for editable install, pytest commands that rely on
  `pyproject.toml`, and other package-aware shell operations
- use the **content root** for code reading, doctrine reading, registry
  reading, orchestration reading, and ordinary file navigation inside the
  branch

## Final judgment

The extracted current-generation branch is not blocked on absent packaging.

It is blocked only if carriers keep collapsing shell root and content root into
one ambiguous startup location.

That is a carrier/startup clarity problem, not a packaging-floor absence
problem.
