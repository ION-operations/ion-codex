---
type: assessment
authority: A3_OPERATIONAL
created: 2026-04-17T00:00:00-04:00
status: ACTIVE
purpose: Deep readiness assessment before entering the next execution phase after q005 retained dual-center settlement
connections:
  - ION/06_intelligence/decisions/2026-04-17_retained_dual_center_settlement_canonicalization_decision.md
  - ION/06_intelligence/decisions/2026-04-17_top_level_production_surface_promotion_map_canonicalization_decision.md
  - ION/05_context/exports/2026-04-17_root_authority_bundle/START_HERE.md
  - ION/06_intelligence/orchestration/2026-04-17_branch_root_shell_vs_content_root_clarification.md
  - /home/sev/ION - Production/ION most recent/ion_current_canonical_runtime_fleet_temporal_2026-04-16/pyproject.toml
  - /home/sev/ION - Production/ION most recent/ion_current_canonical_runtime_fleet_temporal_2026-04-16/ION/tests/test_packaging_entry_posture.py
  - /home/sev/ION - Production/ION/pyproject.toml
  - /home/sev/ION - Production/ION/04_packages/kernel/preflight_cli.py
  - /home/sev/ION - Production/ION/tests/test_preflight_cli.py
---

# Post-q005 Execution Phase Readiness Assessment

## Purpose

This note answers one narrow question:

Are we actually ready to begin the next execution phase, meaning real q003-class
promotion work, immediately after q005?

The answer is:

**Governance posture: ready.**

**Execution posture: correction required before top-level production promotion,
but not blocked on missing packaging.**

The current branch now has a truthful root-authority settlement, a stable
carrier-facing startup bundle, and a real extracted-branch packaging floor.
What still needs correction is the startup contract between the branch shell
root and the inner `ION/` content root, plus the q003 mapping that treated
top-level production packaging as if it were a missing first-wave floor.

## What is ready

The project is ready in the governance sense.

The following are now explicit and coherent:

- q001 workspace root authority
- q002 AIM classification
- q003 promotion mapping
- q004 carrier-facing onboarding bundle
- q005 retained dual-center settlement

That means the project no longer lacks authority, naming, or startup law for
the split-center period.

The current truthful governance answer is stable:

- packaged current-generation root = primary center
- top-level production root = retained secondary extraction / promotion center
- single-root ratification = not authorized yet

So the next stop is not more adjudication theatre. It is preparation for real
promotion work.

## Why the next execution phase is not yet ready

Two concrete findings emerged in this readiness pass.

### Finding 1: the extracted branch already has a real packaging floor

The extracted branch already carries:

- shell-root `pyproject.toml` at
  `/home/sev/ION - Production/ION most recent/ion_current_canonical_runtime_fleet_temporal_2026-04-16/pyproject.toml`
- packaging posture proof at `ION/tests/test_packaging_entry_posture.py`

In a clean temporary virtual environment, I verified:

1. `python -m pip install -e .` works from the extracted branch shell root
2. `import kernel` resolves to the packaged branch path
3. `python -m kernel --help` succeeds
4. `python -m pytest ION/tests/test_packaging_entry_posture.py -q` passes

So the earlier thought that the packaged branch lacked its own packaging floor
was incorrect.

The correction is:

- the extracted branch already owns a minimal packaging floor
- the real ambiguity is shell root versus inner content root
- q003 should not treat top-level production `ION/pyproject.toml` as a missing
  first-wave floor

### Finding 2: the startup hazard is shell-root versus content-root ambiguity

The misleading result appears when commands are run from the inner
`.../ION/` directory without editable install.

During this readiness pass, I ran:

```bash
cd 'ION most recent/ion_current_canonical_runtime_fleet_temporal_2026-04-16/ION'
env -u PYTHONPATH python3 - <<'PY'
import kernel
print(kernel.__file__)
PY
```

Result:

`/home/sev/ION - Production/ION/04_packages/kernel/__init__.py`

That proves one narrow point only:

- an inner-content-root command without editable install can fall through to
  the top-level production installation
- that is a carrier/startup ambiguity
- it is not evidence that the extracted branch lacks packaging

### Finding 3: top-level production packaging/preflight are still service-coupled

The remaining coupling concern is real, but it now has the correct shape.

Top-level production `ION/pyproject.toml` and
`ION/04_packages/kernel/preflight_cli.py` are both tied to the later service
surface:

- `ION/pyproject.toml` declares `ion-api` and the `ion_*_mcp` scripts
- `preflight_cli.py` imports `ion_api.main` and the `ion_*_mcp.logic` modules

So those two top-level production artifacts should not be treated as a
standalone Class-A promotion packet.

## Readiness judgment

The project is ready for the next execution phase **only if** we define that
phase correctly.

It is **not** ready for blind top-level production promotion using the earlier
Class-A story.

It **is** ready for one bounded correction packet whose purpose is:

1. make the shell-root versus content-root rule explicit for carriers
2. correct q003 so top-level production packaging/preflight are no longer
   narrated as a missing first-wave floor
3. preserve the real coupling warning around the later API/MCP service layer

## Current execution position

The correction packet described above has now landed:

- shell-root versus content-root distinction is explicit
- q003 no longer treats top-level production packaging as a missing first-wave
  floor
- the API/MCP family is scoped as an optional later external transport shell

The smaller operator-doc packet has also now landed:

- `ION/docs/README.md`
- `ION/docs/PRODUCTION_RUNBOOK.md`
- `ION/docs/O1_RATIFICATION_CHECKLIST.md`

And the remaining q003 follow-up has now been answered directly:

- the top-level production external transport shell remains retained
  witness/support-only for the current phase

So the branch is no longer waiting on a mandatory q003 widening move.

## What should not happen next

The following would be mistakes:

- repeating the claim that the extracted branch lacks packaging
- running package-aware commands from the inner `ION/` content root and
  treating those results as shell-root truth
- copying top-level production `pyproject.toml` unchanged and calling that
  packaging-floor completion
- copying `preflight_cli.py` unchanged and calling that a standalone entry
  packet
- widening immediately into API/MCP promotion to paper over the remaining
  service coupling

Those would either rest on a false premise or turn the next execution phase
into hidden scope creep.

## Concrete minimum success criteria before real production-surface promotion

Before I would call the next execution phase truly ready, I want these four
conditions satisfied:

1. carriers distinguish shell root from content root explicitly
2. q003 no longer treats top-level production packaging/preflight as a
   standalone first-wave floor
3. editable-install proof for the extracted branch remains explicit and cited
4. any later service-entry promotion packet is scoped against real API/MCP
   coupling rather than inferred from packaging ambiguity

## Final judgment

We are not blocked at the project-law level anymore.

We are not blocked by missing packaging either.

We are only blocked if carriers keep using the wrong startup layer and then
reasoning from those contaminated results.

The root-entry and packet-scope correction is now complete.

The correct present judgment is:

- the branch is execution-ready without opening the external transport shell
- the external transport shell remains available for a later bounded packet if
  a concrete operator or deployment need justifies it
- no automatic widening packet is currently selected from q003
