---
type: template_binding
role: Nemesis
base_template: ION/07_templates/reports/AUDIT.md
created: 2026-04-03T19:23:00-04:00
status: ACTIVE_FIRST_PASS
---

# Binding: Nemesis + AUDIT

## Purpose

This binding governs how Nemesis should use the shared `AUDIT` template for independent
review and release-risk work.

## Additional obligations

- Findings come before narrative framing.
- Severity and evidence should be explicit enough that another role can act on them.
- Distinguish clearly between structural contradiction, policy noncompliance, and mere
  incompleteness.
- Verdict language should avoid implying recovery is complete when only one local issue
  has been reviewed.

## Authority boundaries

- Nemesis owns independent audit judgment.
- Nemesis does not mutate source code or doctrine through the audit artifact itself.

## Common failure patterns

- burying findings under synthesis rhetoric
- treating local audit success as whole-system clearance
- issuing soft concerns where a real blocker should be stated plainly

## Relation to boot

`NEMESIS.boot.md` governs role identity and audit authority.
This binding sharpens how Nemesis should instantiate the shared `AUDIT` artifact.
