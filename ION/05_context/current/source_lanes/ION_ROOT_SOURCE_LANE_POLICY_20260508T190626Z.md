# ION Root Source Lane Policy

Status: active source-lane operating policy for local consolidation.

Created: 2026-05-08T19:06:26Z

Active root:

```text
/home/sev/ION - Production/ION_CODEX FULL
```

## Purpose

The root now has three intentional source lanes beside the active `ION/` tree:

- `workpackets/`
- `diffs/`
- `ION_sandbox/`

These lanes are useful because they keep operator packets, patches, and sandbox
GPT/product package snapshots together with the full development build. They
also create a wrong-root risk unless their authority is explicit.

## Authority Split

```text
ION/
  active full build, current runtime, accepted/candidate implementation

workpackets/
  operator/source packet intake; plan and instruction evidence

diffs/
  patch evidence and candidate patch intake

ION_sandbox/
  sandbox GPT/product package snapshots and source evidence
```

Only `ION/` is the active runtime tree. The other lanes may be read, indexed,
diffed, imported as candidate evidence, or used to draft promotion proposals.
They do not automatically mutate active state.

## Processing Rule

```text
source lane material
-> read and classify
-> compare to current active build
-> decide apply/import/supersede/archive
-> validate
-> receipt
-> capsule update when material
```

## Integration With Candidate Domains

The source lanes should feed the candidate lifecycle system:

- workpacket ideas can become candidate packets, protocols, or routes;
- diffs can become bounded patch packets or archived witness evidence;
- sandbox package surfaces can become candidate domains, templates, agents,
  scorecards, or promotion proposals.

Candidate material remains candidate until accepted through explicit review,
tests, receipts, and human/Steward acceptance.

## Commit Hygiene

`workpackets/` and `diffs/` are small source/evidence lanes and may be tracked
when useful.

Raw package snapshots under `ION_sandbox/` are ignored by default. Track
`ION_sandbox/README.md` and `ION_sandbox/ION_SANDBOX_INDEX_*.json`; promote
specific sandbox files intentionally rather than committing the entire package
tree by accident.

## Non-Claims

This policy does not promote any source-lane file into accepted ION canon. It
does not mutate `ION/03_registry/`, product front-door law, MCP tools, Action
schemas, production state, live execution state, secrets, deployment surfaces,
or git remotes.
