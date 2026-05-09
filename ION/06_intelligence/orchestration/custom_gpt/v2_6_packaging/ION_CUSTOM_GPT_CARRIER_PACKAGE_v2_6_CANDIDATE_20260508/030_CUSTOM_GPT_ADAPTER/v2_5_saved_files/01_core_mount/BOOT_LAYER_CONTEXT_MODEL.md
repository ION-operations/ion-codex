# ION Boot Layer Context Model

status: candidate_custom_gpt_saved_file
purpose: Define BOOT-0 through BOOT-6 context layers for ION carriers.

## Core Thesis

ION carriers should not start from a tiny prompt and hope. They should start
inside a governed working world: identity, carrier mount, current state, domain
context, proof gates, and export law.

The boot package should be large enough that ION behavior is natural, not merely
remembered, while still preserving enough context headroom for the task,
corrections, tool returns, code, validation, receipts, and export.

## Boot Layers

```text
BOOT-0: Kernel law
BOOT-1: Carrier mount
BOOT-2: Current state
BOOT-3: Domain context
BOOT-4: Deep doctrine / architecture
BOOT-5: Retrieval reserve
BOOT-6: Export context
```

## BOOT-0: Kernel Law

Always loaded. Tiny.

Contents:

- identity and non-identity;
- output-is-not-state;
- authority ceiling;
- production/live/secrets boundaries;
- source priority;
- proof/receipt requirement;
- anti-secret rule.

Failure if missing:

- The carrier behaves like generic ChatGPT.
- The carrier claims state or execution too easily.
- The carrier treats ION as passive documentation.

## BOOT-1: Carrier Mount

Always loaded for serious ION work.

Contents:

- carrier profile;
- host family;
- available lanes;
- forbidden lanes;
- active package identity;
- connector/action/MCP/extension status;
- sign-in/reentry proof expectations;
- current action surface limits.

Failure if missing:

- The carrier overclaims local access.
- The carrier confuses ChatGPT Browser, GPT sandbox, MCP, Action Gateway, Codex
  CLI, and extension lanes.

## BOOT-2: Current State

Always loaded or explicitly declared missing.

Contents:

- active packet/current objective;
- accepted/candidate state distinction;
- recent receipts;
- open loops;
- current non-claims;
- state root hash or continuity bundle identity when available.

Failure if missing:

- The carrier answers from stale memory.
- The carrier repeats completed work or loses live obligations.

## BOOT-3: Domain Context

Loaded by route.

Contents:

- only the domain needed for the current work;
- domain-specific vocabulary;
- relevant templates/skills;
- proof obligations;
- common failure modes;
- expected return contract.

Examples:

- coding / Codex work;
- docs and public packaging;
- ingestion and continuity;
- UI/app build;
- agent routing;
- Custom GPT / extension / MCP connectivity;
- ION self-knowledge.

Failure if missing:

- The carrier improvises generic process instead of applying local domain law.

## BOOT-4: Deep Doctrine / Architecture

Loaded for serious design, repair, promotion, audit, or recovery work.

Contents:

- dense ION law;
- graph model;
- template and settlement law;
- continuity architecture;
- historical design decisions;
- candidate/accepted promotion gates;
- architecture non-claims.

Failure if missing:

- The carrier makes local fixes that conflict with ION architecture.

## BOOT-5: Retrieval Reserve

Indexed, available, not always stuffed into live context.

Contents:

- large corpus;
- historical branches and donor material;
- old workpackets;
- reports;
- logs and receipts;
- code maps;
- research/reference packs.

Rule:

BOOT-5 is hydrated just-in-time. It is not treated as active authority until
source priority and authority ranking classify it.

Failure if misused:

- The carrier floods context with old material and lets stale sources outrank
  current law.

## BOOT-6: Export Context

Loaded near the end of state-bearing work, or always loaded in high-discipline
sessions.

Contents:

- receipt draft;
- state delta;
- changed files/artifacts;
- validation results;
- non-claims;
- next packet;
- successor bundle instructions;
- export naming and manifest rules.

Failure if missing:

- Work ends as prose instead of durable continuity.

## Boot Sizes

These are product targets, not strict limits.

| Package | Intended Use | Approximate Size |
| --- | --- | --- |
| `ION_BOOT_MINI` | Always-on Custom GPT / quick chat | 5k-20k tokens |
| `ION_BOOT_STANDARD` | Serious connected work | 50k-150k tokens |
| `ION_BOOT_DEEP` | Architecture/recovery/major implementation | 250k-1M tokens |
| `ION_DOMAIN_PACK_*` | Route-specific domain hydration | variable |
| `ION_RECEIPT_PACK` | Recent proof/state inheritance | variable |
| `ION_DOC_PACK` | Human explanation, lower authority | variable |

## Headroom Rule

Do not fill the whole context window with boot. Preserve working headroom for:

- current user task;
- tool/action returns;
- code/diffs;
- validation output;
- receipts;
- correction turns;
- export continuity.

For very large models, reserve roughly 15-30% for live work unless the task is
explicitly archival/retrieval-only.

## Custom GPT Caveat

Custom GPT saved files are retrieval surfaces, not guaranteed full live context.
Therefore the Custom GPT must treat this boot model as a routing contract:

- BOOT-0 and BOOT-1 belong in instructions/saved files;
- BOOT-2 must come from live state, uploaded bundle, or connector return;
- BOOT-3 must be selected by the current route;
- BOOT-4 is loaded for architecture/recovery/promotion work;
- BOOT-5 is retrieved only when needed;
- BOOT-6 is mounted before state-bearing closure.

If a required boot layer is unavailable, declare CONSERVATIVE, DEGRADED, or
BLOCKED posture rather than fabricating context.

## Operating Sentence

A serious ION carrier must begin from a default context package large enough to
make ION behavior natural, then hydrate domain and retrieval context only as the
task requires.
