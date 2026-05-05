# ION/JOC Release Candidate Preview and Preflight Verifier View Model Protocol

V70 defines the non-materializing release-candidate preview layer for the ION/JOC cockpit.

## Upstream

V69 must provide `PACKAGE_ASSEMBLY_PLAN_PREVIEW_READY` with execution mode `PACKAGE_ASSEMBLY_PLAN_PREVIEW_ONLY`.

## Required visible surfaces

- release candidate preview panel
- preflight verifier checklist rail
- checksum preview ledger table
- package plan reference strip
- evidence bundle index preview
- operator acceptance criteria rail
- blocked capability ledger
- future release authority rail

## Non-authority boundary

V70 must never claim release archive creation, file-system write, zip creation, real checksum generation, artifact export, memory write, canonical graph write, source-summary rewrite, live dispatch, or production readiness.

## Next lawful branch

A future branch may define operator release approval and materialization authority. V70 only proves the cockpit can preview the release-candidate anatomy and preflight checklist.
