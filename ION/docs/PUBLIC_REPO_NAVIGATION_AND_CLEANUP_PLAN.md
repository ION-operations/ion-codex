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

## Implemented Third Slice

- Move root-level witness files into:
  `ION/05_context/archive/root_witness_manifests/`.
- Add a directory README explaining the lifecycle relocation.
- Add a relocation receipt under `ION/05_context/current/github_data_plane/`.
- Keep historical manifests unchanged where they reference old root paths,
  because those references describe prior repository state.

## Implemented Fourth Slice

- Replace the short root README with a full public landing-page README.
- Keep `ION/README.md` as the content-root navigation index.
- Point `pyproject.toml` package metadata at the root `README.md` so the public
  landing page is the package readme.

## Implemented Fifth Slice

- Replace the long catalog-style public README with a sharper landing page
  centered on ION as a continuity substrate.
- Keep detailed navigation in `ION/README.md` and directory-local README files.
- Remove fixed landing-page test-count claims. Public prose should point readers
  to live validation commands instead of freezing a number that can go stale.

## Implemented Sixth Slice

- Revise the landing README language for tighter public positioning.
- Add a full-encyclopedia link with an authority caution so the encyclopedia is
  discoverable without becoming the active mount source.

## Implemented Seventh Slice

- Split public landing prose from deeper doctrine references:
  - `README.md` stays concise.
  - `ION/docs/ION_FUNDAMENTALS.md` carries fundamentals.
  - `ION/docs/TEMPLATE_LAW.md` carries template law.
  - `ION/docs/CONTEXT_SYSTEM.md` carries context inheritance.
  - `ION/docs/AGENTS_ROLES_CARRIERS.md` carries role/carrier boundaries.
- Record the dirty-branch landing split plan at
  `ION/05_context/current/BRANCH_LANDING_PLAN_20260505_CHATOPS_PUBLIC_GITHUB.md`.
- Preserve generated runtime receipts and queue hygiene evidence as a separate
  evidence slice rather than mixing them into the public docs slice.

## Implemented Eighth Slice

- Align the GitHub community-health tab surfaces:
  - `README.md` stays the short public landing page.
  - `CONTRIBUTING.md` carries lawful public collaboration and PR evidence
    expectations.
  - `SECURITY.md` carries the public/private boundary and sensitive report
    path.
  - `ION/docs/README.md` indexes the deeper orientation docs and encyclopedia.
- Keep GitHub framed as collaboration/data plane, not runtime authority.

## Proposed Next Slices

1. Add directory-local README files for:
   - `ION/00_BOOTSTRAP/`
   - `ION/04_agents/`
   - `ION/07_templates/actions/`
   - `ION/07_templates/carriers/`
2. Add a generated or checked navigation index for high-value kernel modules.
3. Add a public-safe issue template for proof returns or task returns if GitHub
   issues become a durable return surface.
4. Decide where future witness manifests should land by default:
   `ION/docs/consolidation/` for public report indexes, or
   `ION/05_context/archive/` for lifecycle evidence.
5. Add a public/private split plan for future production infrastructure repos.
6. Refine `kernel.ion_github_commit_proposal_receipt` so small follow-up
   proposals can emit a changed-path manifest instead of the whole repository
   path set when that is the safer review surface.

## Non-Goals

- No broad file reorganization in this slice.
- No deletion of historical receipts, reports, or witness files.
- No production deployment setup.
- No credential storage guidance beyond refusing to store credentials here.
