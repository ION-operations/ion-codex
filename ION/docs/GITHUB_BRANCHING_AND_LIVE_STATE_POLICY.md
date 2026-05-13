# GitHub Branching And Live State Policy

Status: public collaboration policy  
Production authority: false  
Live execution authority: false

## Purpose

GitHub is ION's public collaboration and data plane. It should let humans and AI
carriers inspect real project movement without mistaking every pushed snapshot
for trusted ION state.

## Branch Classes

| Class | Pattern | Meaning |
| --- | --- | --- |
| Stable | `main` | Public stable line. No direct push by default. |
| Review | `docs/*`, `work/*`, `agent/*`, `data-plane/*` | Scoped review lanes for bounded changes. |
| Volatile live | `volatile/*` | Current working-state mirror for collaboration. Useful, not trusted. |

## Volatile Live Branch Rules

`volatile/*` branches are allowed to move quickly. They exist so other AI
workers and reviewers can see the live local project posture without waiting for
a polished release branch.

They are not production authority, Steward acceptance, or final truth.

Use a volatile branch when:

- the work is useful for other carriers to inspect now;
- the branch contains mixed or still-settling runtime/docs/code evidence;
- the change is not yet ready to be described as accepted ION state;
- fast visibility is more valuable than a perfectly separated PR.

Mark volatile pull requests or branch descriptions with:

```text
VOLATILE / NOT TRUSTED ION STATE
```

## What May Be Committed To Volatile Branches

- source code, tests, docs, schemas, registries, and templates;
- non-secret receipts, work packets, queue hygiene records, and validation
  evidence;
- generated artifacts only when they are intentionally public-safe and useful
  for review.

## What Must Not Be Committed

- secrets, credentials, tokens, cookies, private browser profiles, or `.env`
  files;
- live tunnel credentials or private connector auth state;
- private production infrastructure configuration;
- raw AI output presented as accepted ION state without proof gates;
- files that would expose a local machine beyond intended public collaboration.

Live connector URLs and tunnel logs are ephemeral runtime evidence. Commit them
only when intentionally public-safe, expired or non-sensitive, and useful as a
receipt. Otherwise keep them local or record a redacted receipt.

## Promotion Path

A volatile branch can become trusted only by moving through the normal ION path:

```text
bounded change -> validation -> PR evidence -> review -> Steward/gate receipt -> merge or supersession
```

If a volatile branch contains multiple products, split it before promotion when
practical:

```text
public docs
sandbox/runtime implementation
queue hygiene evidence
extension stability repair
JOC restoration
```

The goal is visibility first, acceptance later.

## Current Practical Convention

For fast public collaboration during active development:

```text
volatile/live-YYYYMMDD-<topic>
```

For bounded review after the branch stabilizes:

```text
docs/<topic>
work/<topic>
agent/<topic>
data-plane/<topic>
```

`main` remains the stable public landing branch.
