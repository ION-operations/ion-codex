# Contributing

This repository is public for collaboration, but ION state is still governed by
packets, receipts, proof gates, and bounded carrier authority.

## Start Here

Read the public landing page first:

- `README.md`

Then use the docs layer for the shape of the system:

- `ION/docs/README.md`
- `ION/docs/GITHUB_BRANCHING_AND_LIVE_STATE_POLICY.md`
- `ION/docs/ION_FUNDAMENTALS.md`
- `ION/docs/TEMPLATE_LAW.md`
- `ION/docs/CONTEXT_SYSTEM.md`
- `ION/docs/AGENTS_ROLES_CARRIERS.md`

Use the encyclopedia for broad history and architecture:

- `ION/docs/encyclopedia/ION_Production_Encyclopedia_v4_0_LIVE_V96_V100_CONTEXT_SYSTEM_AND_AUTONOMOUS_LOOP_RECOVERY.md`

The encyclopedia is reference material, not active runtime authority.

## Before You Change Files

1. Read `ION/REPO_AUTHORITY.md`.
2. Use a scoped branch:
   - `docs/<short-topic>`
   - `work/<short-topic>`
   - `agent/<short-topic>`
   - `data-plane/<short-topic>`
   - `volatile/live-YYYYMMDD-<short-topic>` for public live-state snapshots
     that are useful for collaboration but not yet trusted ION state.
3. Keep changes narrow and explain the owner surface you reused.
4. Run the smallest meaningful validation for the change.
5. Open a pull request with evidence.

## Contribution Lanes

Use the smallest lane that matches the work:

| Lane | Good for |
| --- | --- |
| Docs | README, guides, explanation, public navigation. |
| Kernel | Python runtime, tests, audits, gates, queue projections. |
| Integration | MCP, browser extension, daemon, Cursor, Codex carrier surfaces. |
| Context evidence | Receipts, work packets, queue settlement, lifecycle records. |

Keep public docs, runtime implementation, and active-state evidence in separate
pull requests when possible. That makes review and future indexing cleaner.

## Volatile Live Branches

ION can use `volatile/*` branches to show the real local project posture to
other humans and AI carriers. These branches may move quickly and may contain
still-settling code, docs, and non-secret evidence.

They must be labeled as:

```text
VOLATILE / NOT TRUSTED ION STATE
```

Do not treat a volatile branch as Steward acceptance, production authority, or
runtime truth. It is visibility for collaboration. Promotion still requires the
normal packet, proof, gate, review, and receipt path.

Never commit secrets, credentials, private connector auth state, private browser
profiles, or sensitive live tunnel material to a volatile branch. Live connector
URLs and logs should stay local unless they are intentionally public-safe and
useful as redacted evidence.

## Pull Request Evidence

Include:

- objective
- touched paths
- validations run
- known blockers or skipped checks
- relevant ION packet, receipt, issue, branch, or artifact references

## What Not To Submit

- secrets, credentials, tokens, private browser profiles, tunnel credentials, or
  `.env` files
- production deployment changes unless explicitly authorized by ION policy and
  Braden
- broad rewrites that bypass existing architecture, registry, packet, or
  receipt owners
- raw AI output as accepted state without proof-gated integration

## Validation Commands

Useful defaults from the shell root:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages python3 -S -m kernel.ion_status --ion-root . --json
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=ION/04_packages PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python3 -m pytest ION/tests -q
```

## GitHub Is A Data Plane

GitHub issues and pull requests are collaboration surfaces. They do not grant
runtime authority, production authority, secret authority, or Steward
acceptance by themselves. Accepted state still requires the ION proof path:
packet, context, template, proof-bearing return, gate, Steward decision, and
receipt.
