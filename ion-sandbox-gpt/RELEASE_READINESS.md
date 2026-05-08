# ION Sandbox GPT Release Readiness

Status: public candidate release root prepared locally, not published.

Prepared: 2026-05-08T19:28:00Z

## Release Identity

```text
name: ION Sandbox GPT
version: v1.4-public-candidate
track: custom_gpt_portable_sandbox
authority: non-production, non-live
```

## What This Package Is

This package is a portable Custom GPT/browser GPT ION runtime. A GPT can mount
the package as knowledge/data, follow `START_HERE.md`, execute the ION role
sequence in a single carrier, and export updated continuity state after
state-bearing work.

## What This Package Is Not

This package is not the full local development runtime. It does not require MCP,
Codex CLI, Cloudflare tunnels, local services, Cursor, GitHub mutation, or
production credentials.

It does not grant:

- production authority
- live execution authority
- secrets authority
- deployment authority
- git push authority
- arbitrary shell authority

## Sanitization Performed

The release root was copied from `ION_sandbox` with the following excluded:

- `__pycache__/`
- `*.pyc`
- `.pytest_cache/`
- `*.log`
- `*.pid`

High-confidence secret-pattern scan found no API keys, private keys, OAuth
client secrets, or bearer tokens.

## Current Test Gate

Run from this directory:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q \
  ION/tests/test_kernel_ion_sandbox_preflight.py \
  ION/tests/test_kernel_single_carrier_sequence_runner.py \
  ION/tests/test_kernel_ion_stale_surface_audit.py
```

Result after release-root repair:

```text
13 passed
```

The test run created `ION/05_context/current/ACTIVE_STALE_SURFACE_AUDIT.json`
as the current stale-surface proof surface. Generated `.pytest_cache` files were
removed after the run.

## Cursor / IDE Boundary

Cursor IDE support is optional for this package. The public candidate release
does not include `.cursor/rules/ion-carrier-relay-mediation.mdc`. The
stale-surface audit test treats that as valid only when the package manifest
declares `custom_gpt_portable_sandbox` and `cursor_ide_lane.included=false`.

## Publication Gate

Before pushing:

1. Run the test gate.
2. Run high-confidence secret scan.
3. Review `git status --short --untracked-files=all ion-sandbox-gpt`.
4. Stage only the curated release root and receipt/planning files.
5. Push only after explicit operator approval.
