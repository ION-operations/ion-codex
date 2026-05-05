# Public Repo Navigation And Cleanup Plan

Status: draft implementation plan  
Production authority: false  
Live execution authority: false

## Objective

Make the public repository easier for humans and AI carriers to navigate
without deleting evidence, losing receipts, or inventing a second authority
system.

## Current Problems

- There was no root `README.md` for public GitHub entry.
- `pyproject.toml` points at `ION/README.md`, but that file was missing.
- `ION/docs/README.md` was referenced as a supporting surface but was missing.
- Root-level version witness files are useful evidence, but noisy for first
  navigation.
- Integration surfaces exist across MCP, browser extension, local daemon, and
  Cursor lanes, but public entry points were scattered.

## Cleanup Principles

- No deletion as cleanup. If files need to move, use a lifecycle transition
  with receipt evidence.
- Do not move runtime/current context until owner references and tests are
  audited.
- Keep public collaboration docs separate from future private production
  infrastructure docs.
- Prefer indexes and explicit path maps before reorganization.
- Treat generated reports, receipts, and witness manifests as evidence unless a
  policy says otherwise.

## Implemented First Slice

- Add root `README.md` for public entry, commands, and boundaries.
- Add `CONTRIBUTING.md` for scoped branch and PR evidence expectations.
- Add `SECURITY.md` for public repo secret-handling boundaries.
- Add `ION/README.md` for content-root navigation.
- Add `ION/docs/README.md` for docs navigation.
- Add `ION/04_packages/README.md` and `ION/09_integrations/README.md` for
  package and integration orientation.

## Implemented Second Slice

- Add public-safe GitHub issue templates for:
  - bounded ION work packets;
  - non-sensitive bug reports.
- Add a pull request template that requires touched paths, validation, receipts,
  and authority boundaries.
- Add directory-local README indexes for:
  - `ION/02_architecture/`;
  - `ION/03_registry/`;
  - `ION/05_context/`;
  - `ION/06_intelligence/`.

## Proposed Next Slices

1. Add directory-local README files for:
   - `ION/00_BOOTSTRAP/`
   - `ION/04_agents/`
   - `ION/07_templates/actions/`
   - `ION/07_templates/carriers/`
2. Add a generated or checked navigation index for high-value kernel modules.
3. Add a public-safe issue template for proof returns or task returns if GitHub
   issues become a durable return surface.
4. Add a lifecycle proposal for root-level `FILES_ADDED_V*.txt` witness files:
   keep them tracked, but consider moving future witness manifests under
   `ION/docs/consolidation/` or `ION/05_context/archive/` with receipts.
5. Add a public/private split plan for future production infrastructure repos.
6. Refine `kernel.ion_github_commit_proposal_receipt` so small follow-up
   proposals can emit a changed-path manifest instead of the whole repository
   path set when that is the safer review surface.

## Non-Goals

- No broad file reorganization in this slice.
- No deletion of historical receipts, reports, or witness files.
- No production deployment setup.
- No credential storage guidance beyond refusing to store credentials here.
