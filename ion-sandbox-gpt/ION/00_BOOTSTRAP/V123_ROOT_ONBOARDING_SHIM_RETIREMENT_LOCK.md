# V123 Root Onboarding Shim Retirement Lock

## Authority

V123 retires `AGENTS.md` and `START_HERE_FOR_ANY_AGENT.md` from hot shell-root
carrier onboarding authority.

## Problem

The files were repeatedly described as compatibility or convenience surfaces,
but their root location and procedural content made them act as onboarding law.
That contradicted ION-native carrier onboarding through `ION/REPO_AUTHORITY.md`,
`ION/02_architecture/ION_MOUNT_CONTRACT.md`, carrier registry profiles,
runtime identity registries, execution packet templates, active packets, and
proof gates.

## Law

Root-visible markdown must not carry procedural carrier onboarding, command
spines, mandatory reads, protocol anchors, or universal carrier identity claims.

Former root onboarding shims may be retained only as containment or forensic
evidence with hash proof.

## Active Custody

```text
AGENTS.md
-> ION/05_context/archive/containment/V123_ROOT_ONBOARDING_SHIMS/AGENTS.md

START_HERE_FOR_ANY_AGENT.md
-> ION/05_context/archive/containment/V123_ROOT_ONBOARDING_SHIMS/START_HERE_FOR_ANY_AGENT.md
```

Containment receipt:

```text
ION/05_context/current/CONTAINMENT_RECEIPT_V123_ROOT_ONBOARDING_SHIMS.json
```

The April 17 exported root-authority bundle is also retired from hot startup
authority because it centered `START_HERE.md` as the first read:

```text
ION/05_context/exports/2026-04-17_root_authority_bundle/
-> ION/05_context/archive/containment/V123_ROOT_ONBOARDING_SHIMS/root_authority_bundle_2026-04-17/
```

Containment receipt:

```text
ION/05_context/current/CONTAINMENT_RECEIPT_V123_ROOT_AUTHORITY_BUNDLE_START_HERE.json
```

The stale April 27 operator-visible last-run witness was also retired from
current context because it still listed retired `START_HERE` surfaces as
required reads. The related generated `_tmp_onboard.json` was contained for the
same reason:

```text
ION/05_context/current/OPERATOR_VISIBLE_LAST_RUN.md
-> ION/05_context/archive/containment/V123_ROOT_ONBOARDING_SHIMS/OPERATOR_VISIBLE_LAST_RUN_20260427_STALE_START_HERE.md

ION/05_context/current/_tmp_onboard.json
-> ION/05_context/archive/containment/V123_ROOT_ONBOARDING_SHIMS/_tmp_onboard_20260427_STALE_START_HERE.json
```

Containment receipt:

```text
ION/05_context/current/CONTAINMENT_RECEIPT_V123_STALE_OPERATOR_VISIBLE_LAST_RUN.json
```

## Required Enforcement

V123 requires:

- carrier onboarding audit blocks procedural root markdown
- active Cursor hook no longer requires retired root files
- repo authority no longer points to the April 17 `START_HERE.md` bundle as first-read startup law
- mount contract states that former root shims are retired from hot authority
- compact runtime packaging does not include root onboarding shims
- full-project safe packager reports the containment transition instead of a silent removal

## Authority Ceiling

Production authority remains `false`.

Live execution authority remains `false`.
