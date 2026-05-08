---
type: action_template
authority: A2_EXECUTOR
created: 2026-04-08T20:30:00-04:00
revised: 2026-04-09T00:03:00-04:00
status: ACTIVE
---

# MANUAL_AUTOMATION_FALLBACK

## Required frontmatter

```yaml
---
type: manual_automation_fallback
template: MANUAL_AUTOMATION_FALLBACK
created: <ISO timestamp>
status: <ACTIVE|COMPLETE>
automation_surface: <blocked or paused carrier>
reason: <why the carrier cannot carry the step>
---
```

## Required sections

```markdown
# Manual Automation Fallback: <title>

## Carrier blocked or disabled
- Automation carrier / service:
- Why unavailable:
- Current automation mode / operator-control posture:

## Lawful bounded inputs
- Governing task / manifest / packet refs:
- Current scope / work id:
- Allowed writes:
- Blocking review / policy state:

## Manual fallback step
- Exact single step being carried manually:
- Expected output family:
- Proposed follow-up / handoff target:

## Outputs emitted
- Receipts / signals / handoff generated:
- Proposal surfaces generated:
- Unresolved risk preserved:
```
