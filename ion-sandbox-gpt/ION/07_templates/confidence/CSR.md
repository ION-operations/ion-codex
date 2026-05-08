---
type: template
template_name: CSR
created: 2026-04-07T22:25:00-04:00
status: ACTIVE_FIRST_PASS
lineage:
  - SOS/07_templates/confidence/CSR.md
  - SOS-OPUS/07_templates/confidence/CSR.md
  - ION-BUILD/context/templates/confidence/CSR.md
connections:
  - ION/02_architecture/AGENT_REASONING_PROTOCOL.md
  - ION/07_templates/reports/REASONING_JOURNAL.md
  - ION/07_templates/bindings/CODEX__CSR.md
  - ION/06_intelligence/specs/T08_ConfidenceAndDriftSchema.spec.md
---

# TEMPLATE — COGNITIVE STATE REPORT (CSR)

Use this when an agent needs an explicit confidence, direction, concern, and calibration surface that is more operator-facing than a `REASONING_JOURNAL`.

## Why this exists

A `REASONING_JOURNAL` is the bounded reasoning chamber for one execution window.
A `CSR` is the outward-facing control surface that tells the organism:

- whether the work direction is sound,
- whether execution confidence is real,
- what concerns should pressure routing,
- what context is still missing,
- and how calibration should affect the next step.

The two surfaces are related but not identical.
A journal may justify the work internally.
A CSR makes the confidence and pressure state legible.

## Recommended frontmatter

```yaml
---
type: confidence_report
from: <role>
created: <ISO timestamp>
responding_to: <task, directive, or work packet>
mode: FULL | MINI
---
```

## Required body sections

```markdown
# Cognitive State Report — <role> — <timestamp>

## Direction
Narrative:
Summary: CLEAR | UNCERTAIN | CONFLICTED

## Execution
Narrative:
Summary: CAPABLE | PARTIAL | UNABLE

## Intent
Narrative:
Summary: DEFINED | VAGUE | UNDEFINED

## Concerns
Narrative:
Summary: NONE | MANAGEABLE | BLOCKING

## Context Gaps
Narrative:
Summary: COMPLETE | GAPS_RESEARCHABLE | GAPS_NEED_USER

## Calibration
Narrative:
Summary: CALIBRATED | UNTESTED | HISTORICALLY_OVERCONFIDENT

## Recommendation
CONTINUE | NARROW_AND_CONTINUE | RESEARCH_FIRST | ASK_USER | ESCALATE | STOP
```

## Pressure mapping

| Condition | Pressure |
|---|---|
| Direction = CONFLICTED | stop forward motion and route back to doctrine / mission clarity |
| Execution = UNABLE | stop and escalate or ask for a different path |
| Intent = UNDEFINED | do not continue until intent is rewritten or clarified |
| Concerns = BLOCKING | convert the concern into a visible issue surface |
| Context Gaps = GAPS_RESEARCHABLE | research before wider execution |
| Context Gaps = GAPS_NEED_USER | ask the user rather than invent missing state |
| Calibration = HISTORICALLY_OVERCONFIDENT | reduce scope and increase validation burden |

## When to write a CSR

Write a full CSR when:

- the work spans multiple turns,
- the direction is high-stakes or drift-sensitive,
- the task could widen runtime authority,
- the work depends on uncertain context,
- or the next move would otherwise be inferred from generated continuity alone.

A mini CSR is acceptable for smaller but still non-trivial work.

## Invariants

1. Every field must include both narrative and summary.
2. The report must stay evidence-aware and not fake numerical certainty.
3. The recommendation must match the summaries.
4. A CSR does not self-ratify architecture, release, or doctrine changes.
