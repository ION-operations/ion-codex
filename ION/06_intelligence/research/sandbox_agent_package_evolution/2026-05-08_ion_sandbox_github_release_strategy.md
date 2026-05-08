# ION Sandbox GitHub Release Strategy

Status: release strategy and readiness audit, not a publication commit.

Created: 2026-05-08T19:16:12Z

Active root:

```text
/home/sev/ION - Production/ION_CODEX FULL
```

Sandbox snapshot:

```text
ION_sandbox/ION_FULL_GPT_SANDBOX_AGENT_PACKAGE_v1_4_AI_ASSISTANT_WORK_TEMPLATE_INSTANCE_EXERCISES_CANDIDATE_20260508T154333Z/
```

## Recommendation

The sandbox GPT package is a real candidate for ION's first public GitHub
project. It should move toward publication on a dedicated release branch, but
not by blindly unignoring and committing the raw local snapshot.

Recommended publication shape:

```text
branch: release/ion-sandbox-gpt-v1
product root: ion-sandbox-gpt/
source: curated copy of ION_sandbox snapshot
status: public candidate release, non-production, non-live
```

The active full development build should remain in `ION/`. The sandbox release
branch should present the Custom GPT/product package clearly as the thing being
published, not as the full local development system.

## Why This Is Worth Doing

Observed evidence supports treating the sandbox package as a product candidate:

- The user reported successful Custom GPT browser operation from this package
  family.
- The package includes a single-carrier sequential role-phase runtime concept.
- The package includes Custom GPT adapter instructions and starter data.
- The package already contains `README.md`, `SECURITY.md`, `CONTRIBUTING.md`,
  manifests, starter data, and tests.
- The newer v1.4 snapshot includes AI Assistant Work candidate domains, agents,
  templates, instances, and exercises that now feed the active candidate
  lifecycle system.

The correct posture is:

```text
publishable candidate, not production-ready runtime
```

## Audit Findings

Local inventory:

- size: about 26M
- file count: 3,756
- largest file: about 719K
- no files larger than 5M found
- no obvious credential filenames found
- tighter secret-pattern scan found no high-confidence API keys, private keys,
  OAuth client secrets, or bearer tokens

Package hygiene issues:

- generated `__pycache__/*.pyc` files are present;
- `.pytest_cache/` is present;
- package manifest metadata still says v1.1 while outer package label says
  v1.4 assistant-work evolution;
- the package contains runtime/current-state surfaces that should be reviewed
  for whether they are starter/demo state or development residue;
- one stale-surface test expects a Cursor rule file that is absent from the
  portable GPT sandbox package.

## Validation

Focused sandbox product tests:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q \
  ION/tests/test_kernel_ion_sandbox_preflight.py \
  ION/tests/test_kernel_single_carrier_sequence_runner.py

10 passed
```

Expanded run including stale-surface audit:

```text
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q \
  ION/tests/test_kernel_ion_sandbox_preflight.py \
  ION/tests/test_kernel_single_carrier_sequence_runner.py \
  ION/tests/test_kernel_ion_stale_surface_audit.py

10 passed, 3 failed
```

Failure class:

```text
portable_sandbox_package_missing_cursor_rule_expected_by_stale_surface_test
```

The failed test reads:

```text
.cursor/rules/ion-carrier-relay-mediation.mdc
```

That path does not exist in the sandbox snapshot. This is not necessarily a
product failure for Custom GPT use. It is a release test-boundary failure:
either the release should include the Cursor rule, or the test should become
conditional/IDE-lane-specific for the sandbox package.

## Branch Strategy

Use a dedicated branch before unignoring raw package contents:

```text
release/ion-sandbox-gpt-v1
```

On that branch:

1. Copy the curated sandbox package to a clean product root, for example
   `ion-sandbox-gpt/`.
2. Exclude generated/runtime residue:
   - `__pycache__/`
   - `*.pyc`
   - `.pytest_cache/`
   - logs/pids
   - local-only runtime caches
3. Fix manifest/package naming drift:
   - package name should identify v1.4 or the chosen release name;
   - README should match the release name;
   - validation report should state what test subset is product-authoritative.
4. Decide Cursor/IDE boundary:
   - include the missing Cursor rule if this release claims IDE/Cursor support;
   - or mark that test as excluded from the Custom GPT product release.
5. Add a release README that says plainly:
   - what the package is;
   - how to use it with Custom GPT knowledge/data package mode;
   - what it cannot do;
   - no production/live/secrets authority;
   - how receipts and exported continuity packages work.
6. Run release test suite and receipt results.
7. Only then make a public branch or repository.

## Repo Shape Options

### Option A - Branch In Current Repo

Pros:

- keeps full build and product release lineage together;
- easiest to diff against active development;
- good for early project history.

Cons:

- branch can confuse active-runtime vs product-package boundaries;
- needs careful `.gitignore`/release root handling.

### Option B - Separate Public Repo

Pros:

- clean product-facing surface;
- easier public onboarding;
- avoids exposing full development tree by accident.

Cons:

- extra synchronization work;
- harder to keep candidate lifecycle evidence linked.

### Option C - Current Repo With `ion-sandbox-gpt/` Subtree

Pros:

- keeps source together;
- public package can live as a product subproject.

Cons:

- more clutter in the full build;
- root-level build/test expectations must be carefully scoped.

Recommended near-term choice:

```text
Option A now: release branch in current repo.
Option B later: separate public repo once product identity stabilizes.
```

## Release Gates

Before publication:

1. Sanitize generated/cache files.
2. Fix package name/version metadata.
3. Decide Cursor/IDE test boundary.
4. Run focused release tests.
5. Run high-confidence secret scan.
6. Write release receipt.
7. Create branch.
8. Stage only curated release files.
9. Review staged file list.
10. Push only after explicit operator approval.

## Non-Claims

- This strategy does not publish the package.
- This strategy does not unignore or stage raw sandbox contents.
- This strategy does not claim production readiness.
- This strategy does not grant live execution, secrets, deployment, git push, or
  arbitrary shell authority.
