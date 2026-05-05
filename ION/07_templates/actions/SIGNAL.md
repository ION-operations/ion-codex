---
type: template
template_name: SIGNAL
created: 2026-04-03T15:51:02-04:00
status: ACTIVE
---

# TEMPLATE — SIGNAL

Use this for short filesystem-visible event emission.

## Required frontmatter

```yaml
---
type: signal
from: <role>
to: <role or list of roles>
signal: <signal vocabulary name>
status: <ACTIVE|COMPLETE|BLOCKED|WITNESS>
created: <ISO timestamp>
payload:
  artifact: <path or primary pointer>
  summary: <one short summary>
---
```

## Body

One short paragraph or one short note that points the reader to the real artifact.

## Invariants

1. Signals announce; they do not replace the real artifact.
2. Signals should be short enough to scan quickly.
3. If the signal is about a delta or correction, say that plainly in `payload.summary`.

## Do not

- paste full reports into the signal
- use signals as hidden governance
- leave the primary artifact unspecified
