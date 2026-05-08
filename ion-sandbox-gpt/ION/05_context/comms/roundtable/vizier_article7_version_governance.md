---
type: proposal
from: Vizier
created: 2026-04-03T22:00:00-04:00
responding_to:
  - Sovereign direction on git integration and thinking beyond existing tools
  - ION/06_intelligence/roundtable/continuity_crisis/synthesis/2026-04-03_continuity_ratification_delta_package.md
status: PROPOSED
---

# Proposed Article 7 Amendment: Version Governance

## Replaces

The earlier "copy-on-update" concept and the governance chain article (which becomes Article 8).

## The Principle (tool-independent)

Every meaningful continuity mutation must be versioned, attributed, and recoverable.
The system must be able to answer: what changed, who changed it, when, why, and what
was the state before. No mutation may be invisible to the timeline.

## Current Implementation: Git

Git is the current version governance tool. It provides:
- Attribution (who committed)
- Diffing (what changed)
- History (when, in what order)
- Recovery (revert to any point)
- Branching (parallel work without corruption)
- Blame (trace any line to its origin)

### Git Governance Rules (current)

1. Every meaningful work unit ends with a governed commit
2. Commit messages are structured: `[ROLE] TEMPLATE: one-line summary`
3. The commit history IS the timeline archive — no separate history/ directories required
4. Scribe is the git governance agent (follows VERSION_CONTROL template)
5. Main branch = ratified state. Working branches for in-progress or experimental work.
6. Agents that cannot run git (subagents, some chassis) produce artifacts that are
   committed by the supervising agent or by Scribe
7. Force-push to main is constitutionally prohibited without Sovereign authorization

### What Git Replaces

- `history/` directories with timestamped copies → git log + git diff
- PRE/POST file copies → git commits before and after work units
- Manual copy-on-update → git add + git commit with governed message

### What Git Does Not Replace

- Private MINI/CAPSULE as source continuity (Articles 1-2 still govern)
- Signal emission (git commits don't notify agents — signals do)
- The chat-death test (git history helps recovery but MINI is still the routing primitive)

## The Future (what may evolve beyond git)

ION may eventually need versioning capabilities that git was not designed to provide:

- **Cognitive state transitions** — not just file diffs but understanding-level changes
- **Conjugate-basis-aware versioning** — tracking how changes in one dimension affect another
- **Paired transaction versioning** — PRE/POST as a single cognitive event, not two commits
- **Evidence-chain provenance** — tracing claims to evidence, not just lines to commits
- **Protocol field versioning** — tracking the coupling structure between systems, not just files

These are OPEN_FIELD entries (Protected Ambiguities) — they must not be collapsed prematurely,
but they should be explicitly held as design questions for the future ION versioning system.

## Proposed Law Text

### Article 7: Version Governance

Every meaningful continuity mutation must be versioned, attributed, and recoverable.
The current implementation is git. The principle survives even if the tool evolves.

Implementation rules:
- Meaningful work units produce governed commits
- Commit messages follow template structure
- History is the commit log, not separate archive files
- Agents unable to commit directly must produce artifacts for supervised commit
- Ratified state lives on the main branch
- Force-push to main requires Sovereign authorization

### Article 8: Continuity-Sensitive Release Governance (moved from old Article 7)

For covered continuity-sensitive artifacts, release or ratification must not bypass
the required governance chain: Primary → Daimon → Nemesis, with Sovereign adjudication
or ratification where the artifact class or unresolved dissent requires it.

## For the Roundtable

1. Does this framing (principle-first, git as implementation) work?
2. Should the "beyond git" questions go into OPEN_FIELD as Protected Ambiguities?
3. Does the commit message structure need more specification now, or can it evolve?
4. Should every agent be able to commit, or should commits be centralized through Scribe?
