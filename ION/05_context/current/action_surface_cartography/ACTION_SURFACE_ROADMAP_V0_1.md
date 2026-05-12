# Action Surface Roadmap v0.1

Status: candidate roadmap (not settled law).

## Packet Queue

### ACTION_SURFACE_CONTEXT_PACKAGE_002_ROUTE_COMPILER_REPAIR
Objective:
Repair assistant-work route compiler prerequisites and normalize missing-registry handling for browser-facing route previews.

Targets:
- Resolve `pyyaml_unavailable` dependency path.
- Ensure route registry and lifecycle registry availability checks are explicit and paginated in status surfaces.
- Add focused tests for degraded-to-ready transition behavior.

### ACTION_SURFACE_CONTEXT_PACKAGE_003_PAGINATED_STATUS_SURFACES
Objective:
Reduce oversized response risk for `ion_context_plan`, `ion_cockpit_view`, and queue/state endpoints by standardizing pagination and bounded summaries.

Targets:
- Add page/limit controls and compact summary modes.
- Document response-size guardrails for browser carrier consumption.
- Add proof surfaces for page completeness and truncation warnings.

### ACTION_SURFACE_CONTEXT_PACKAGE_004_GITHUB_DRAFT_SCHEMA_FIX
Objective:
Resolve schema mismatch between `create_github_issue_draft` payload variants and validator expectations.

Targets:
- Reconcile flat keys (`github_owner`, `github_repo`, `github_title`, `github_body`) with nested `github.{owner,repo,title,body}` contract.
- Add compatibility mapping or explicit policy refusal with clear remediation.
- Add validation matrix tests for both payload shapes.

### ACTION_SURFACE_CONTEXT_PACKAGE_005_SAFE_LOCAL_IDE_LOOP
Objective:
Define a safe local IDE-to-queue loop for candidate draft writes and artifact registration without broadening authority.

Targets:
- Keep bounded write roots and confirmation token gate.
- Preserve no-secrets/no-git-push/no-production constraints.
- Add operator-visible receipts for each state transition.

## Settlement Gate
All packets remain candidate until accepted through context settlement proof intake.
