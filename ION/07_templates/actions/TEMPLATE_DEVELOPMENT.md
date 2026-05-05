---
type: template
template_name: TEMPLATE_DEVELOPMENT
created: 2026-03-28T00:00:00-04:00
status: ACTIVE
authority: A3_OPERATIONAL
provenance: >-
  Primary body text carried forward from
  /home/sev/ION - Production/ION-BUILD/context/templates/actions/TEMPLATE_DEVELOPMENT.md
  (historical ION-BUILD context layout). Active-root frontmatter and the
  "Current-line routing addendum" were added 2026-04-18 as part of Tier 0/1
  forensic restoration (see FORENSIC_RESTORATION_PACKAGE_2026-04-18/PATCH_NOTES.md).
connections:
  - ION/02_architecture/META_TEMPLATE_CONSTITUTION_PROTOCOL.md
  - ION/02_architecture/TEMPLATE_SURFACE_EVOLUTION_PROTOCOL.md
  - ION/07_templates/_MASTER.md
---

# TEMPLATE: TEMPLATE_DEVELOPMENT (Meta-Template Creation Protocol)

> **Authority:** A1_KERNEL — meta-governance (template creation governs all other templates)  
> **Governing Protocol:** D31 (Dynamic Protocol Authority), D27 (Template-First)  
> **Created:** 2026-03-28 | **Status:** ACTIVE

---

## PURPOSE

Governs the creation of NEW templates. This is the comprehension protocol that guides
the AI through the process of recognizing a gap, designing a template, and integrating
it into the system. _MASTER.md defines WHAT a template must contain structurally.
THIS template defines HOW to think through creating one and how it fits into ION.

Template creation is a PERMANENT part of ION — new project types, new workflows,
and system evolution will always require new templates. This process never ends.

---

## PREREQUISITES

- The AI has identified an action type with no governing template
- _MASTER.md has been read (structural requirements)
- All existing templates in templates/ reviewed to confirm no overlap
- CSR Direction: CLEAR on why this template is needed
- §14 boundaries checked: is template creation in scope?

---

## SPEC — TEMPLATE DEVELOPMENT PROCESS

### Phase 1: IDENTIFY THE GAP

```markdown
# Template Proposal: {ACTION_TYPE}

**Date:** {timestamp} | **Agent:** {callsign} | **Type:** Template Development
**Template:** TEMPLATE_DEVELOPMENT (D31)
**Gap Source:** {where was the missing template discovered?}

## Gap Analysis
**Action being performed:** {what the AI needs to do}
**Current state:** {raw/ungoverned — what happens without a template}
**Frequency:** {how often this action occurs: every output / every session / rare}
**Trigger:** {what causes this action: user request / system event / AI autonomously}
**Impact if ungoverned:** {what goes wrong when template is missing}
```

### Phase 2: MAP RELATIONSHIPS

```markdown
## Relationship Map
**Produces:** {what this action outputs — files, state changes, evidence}
**Requires:** {what must exist before this action: specs, context, other templates}
**Affects:** {what systems change: CAPSULE, branches, evidence, questions, automation}
**Connected templates:** {which existing templates relate to this one}
**ION equivalent:** {what ION v3 runtime component this maps to — if applicable}
```

### Phase 3: IDENTIFY FAILURE MODES

```markdown
## Failure Modes
| # | Failure | Cause | Impact | Prevention |
|---|---------|-------|--------|-----------|
| F1 | {what goes wrong} | {why} | {consequence} | {what template should enforce} |

**Historical evidence:** {has this type of failure caused drift before?}
**Worst case:** {what happens if AI does this without governance permanently?}
```

### Phase 4: DESIGN AUTOMATION HOOKS

```markdown
## Automation Integration
**Machine-readable output?** {YES/NO — can this template's output be parsed by extension?}
**FileWatcher trigger?** {what file change would signal this action completed?}
**Gate integration?** {does this action produce/consume gates?}
**Cross-validation?** {can extension verify compliance?}
**SENTINEL monitoring?** {should SENTINEL audit this action type?}
**Proposed format:** {JSON/YAML/Markdown with frontmatter — what enables automation?}
```

### Phase 5: WRITE THE TEMPLATE

Follow _MASTER.md structure exactly:
1. HEADER (Authority, Governing Protocol, Created, Status)
2. PREREQUISITES (Context files, conditions, CSR fields)
3. SPEC (Required metadata, content sections, relationships, tags)
4. ROUTING (where filed, what updated)
5. INVARIANTS (W1-W10 manual checks)
6. DYNAMIC EXPANSION (rules for going beyond minimum)

### Phase 6: REGISTER AND CONNECT

```markdown
## Registration
- [ ] Template filed at: templates/{category}/{NAME}.md
- [ ] _MASTER.md registry updated (add row to Template Registry Index)
- [ ] CAPSULE §4 updated (new decision recorded)
- [ ] Connected templates updated (if they reference this action type)
- [ ] MINI ROUTE updated (include template path when relevant to next task)
- [ ] automation_unified_spec checked (does this template create new automation needs?)
```

---

## ROUTING

- Template proposal filed at: `context/08_comms/replies/{timestamp}_template_proposal.md`
- Template itself filed at: `context/templates/{category}/{NAME}.md`
- _MASTER.md: add to Template Registry Index
- CAPSULE §4: add decision entry for template creation
- 12_evidence: add evidence of template creation

---

## INVARIANTS

- W1 Intake: All 6 phases documented (gap, relationships, failures, automation, write, register)
- W3 Classify: Template follows _MASTER format, all 6 sections present
- W6 Zone: Filed in templates/ under correct subdirectory
- W7 Contradict: New template doesn't duplicate existing template's scope
- W7 Contradict: New template doesn't contradict A0-A2 governance
- W8 Verify: Template actually prevents the failure modes identified in Phase 3
- W9 Provenance: Date, author, D31 reference, gap source documented
- W10 Propagate: _MASTER registry updated, CAPSULE updated, connected templates updated

---

## DYNAMIC EXPANSION

- If template creation reveals ADDITIONAL missing templates → file separate proposals
- If template requires new automation hooks → update automation_unified_spec
- If template modifies existing protocols → requires A1_PRIME (Braden) approval
- Template refinement: templates can be updated via copy-on-update after usage experience

---

## THE TEMPLATE LIFECYCLE (Permanent ION Evolution)

```
DISCOVER → AI encounters ungoverned action, flags it
PROPOSE → AI follows THIS template to design a new template
REVIEW → A1_PRIME approves (if A0-A2 affected) or AI self-approves (A3+)
CREATE → Template written to _MASTER format
REGISTER → Added to _MASTER registry, connected to system
USE → Template governs future instances of this action
REFINE → Template updated via copy-on-update after usage experience
AUTOMATE → Extension backend wired to validate compliance

This cycle never ends. ION's governance evolves by growing its template library.
```

---

## Current-line routing addendum (packaged `ION/` root)

When executing inside the packaged current-generation root, map historical ION-BUILD paths like:

- `context/templates/{category}/{NAME}.md` → prefer `ION/07_templates/{category}/{NAME}.md` (actions/reports/bindings as appropriate)
- `context/08_comms/replies/...` → prefer `ION/05_context/comms/...` or the governing inbox path named by the active orchestration memo for the lane
- `_MASTER.md` → `ION/07_templates/_MASTER.md`

Meta-template constitutional framing for this root lives at:

- `ION/02_architecture/META_TEMPLATE_CONSTITUTION_PROTOCOL.md`

Mutation provenance remains governed by:

- `ION/02_architecture/TEMPLATE_SURFACE_EVOLUTION_PROTOCOL.md`
- `ION/07_templates/actions/TEMPLATE_SURFACE_CHANGE.md`
