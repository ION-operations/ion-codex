---
type: research
from: Codex
created: 2026-04-03T19:11:00-04:00
status: COMPLETE
topic: Whether ION templates should be shared, agent-specific, or layered
connections:
  - ION/01_doctrine/SOVEREIGN_CONSTITUTION.md
  - ION/01_doctrine/SOVEREIGN_KERNEL.md
  - ION/07_templates/README.md
  - ION/07_templates/_MASTER.md
  - ION/03_registry/boots/CODEX.boot.md
  - ION/03_registry/boots/VIZIER.boot.md
  - ION/03_registry/boots/MASON.boot.md
  - ION/03_registry/boots/THOTH.boot.md
  - ION/02_architecture/CODEX_LEAD_ORCHESTRATION_PROTOCOL.md
  - ION/PLAN.md
---

# Codex Template Architecture: Shared vs Agent-Specific

## Why this exists

The active build now has a real minimum template floor and a real role field.
That makes the template question load-bearing.

The user’s intuition is strong: agents already differ in authority, regulations, lane
law, and function. It is natural to ask whether each agent should therefore have its own
templates.

The answer matters because templates in ION are doing more than formatting.
They are part of the machine language of the protocol field.

## Sources or surfaces considered

- `ION/01_doctrine/SOVEREIGN_CONSTITUTION.md`
- `ION/01_doctrine/SOVEREIGN_KERNEL.md`
- `ION/07_templates/README.md`
- `ION/07_templates/_MASTER.md`
- `ION/03_registry/boots/CODEX.boot.md`
- `ION/03_registry/boots/VIZIER.boot.md`
- `ION/03_registry/boots/MASON.boot.md`
- `ION/03_registry/boots/THOTH.boot.md`
- `ION/02_architecture/CODEX_LEAD_ORCHESTRATION_PROTOCOL.md`
- `ION/PLAN.md`

## Findings

### 1. Templates are currently carrying two different kinds of burden

There are at least two distinct layers hiding inside the word `template`:

1. **artifact contract**
   the shared machine-legible shape of a thing:
   `TASK`, `SIGNAL`, `HANDOFF`, `AUDIT`, `RESEARCH`, `CODE`, `EVIDENCE`

2. **role-specific execution discipline**
   how a given role is expected to use that artifact:
   what it must read first, what claims it may make, what lane it may write to,
   what kind of judgment it owns, and what it must not silently claim

The first layer belongs to template law.
The second layer mostly belongs to boots, role law, and packet constraints.

If those layers are not separated, the system starts asking templates to do too much.

### 2. Fully separate per-agent template trees would weaken the system if made the default

If every role had its own full private version of `RESEARCH`, `AUDIT`, `CODE`, `TASK`,
and so on, several failures would appear:

- the machine language would fragment,
- cross-role comparability would decline,
- audits would get harder because outputs would no longer line up structurally,
- support routing would become more brittle,
- extracted runtime portability would get worse,
- and the team would start confusing stylistic differences with truly distinct artifact types.

In short:

> if everything becomes agent-specific, nothing remains system-legible enough to act as
> common protocol law.

### 3. Purely shared templates are also insufficient

The opposite extreme is also weak.

If `RESEARCH` means exactly the same thing for Codex, Thoth, Vizier, Atlas, and Relay,
the template becomes too generic to shape role-specific excellence.

The result is a thin universal form that says:

- write some findings,
- mention some sources,
- maybe add implications

That may be legal, but it does not encode the deeper role-specific discipline the system
actually wants.

Example:

- Thoth research should likely be evidence-denser and line-cited.
- Codex research may lawfully include design synthesis and build recommendations.
- Vizier research may sit closer to architecture and plan implications.
- Atlas research should keep evidence-tier discipline tied to external systems packages.

These are not merely stylistic differences.
They are real role-specific obligations.

### 4. The right answer is a layered template architecture

The strongest structure is:

#### Layer A — Core shared templates

These remain universal and system-visible.

They define:

- minimum structure
- required fields
- invariant distinctions
- lifecycle semantics
- machine-legible expectations

Examples:

- `TASK`
- `SIGNAL`
- `HANDOFF`
- `ROLE_SESSION`
- `AUDIT`
- `RESEARCH`
- `CODE`
- `EVIDENCE`

#### Layer B — Role bindings or template profiles

These are not wholly separate templates.
They are role-specific bindings that sit on top of the core templates.

They define:

- how a role should use a shared template,
- what additional sections or rigor that role owes,
- what authority ceiling applies,
- and what common mistakes that role must avoid.

Examples:

- `Thoth + RESEARCH`
  requires exact citations, stronger source accounting, weaker free synthesis
- `Codex + CODE`
  requires bounded implementation plus continuity/update obligations
- `Nemesis + AUDIT`
  requires explicit findings ordering and verdict discipline
- `Relay + HANDOFF`
  requires packet clarity, courier framing, and no silent architecture claims

#### Layer C — Truly role-native templates

These should exist only when the artifact itself is genuinely role-unique.

Not because the role is special.
Because the artifact type is actually different.

Examples likely justified:

- `DAIMON_DISSENT`
- `RELAY_PACKET`
- `ARCHAEOLOGY_FINDING`
- `KERNEL_ROUTER_RUN`

Those are not just flavored versions of `RESEARCH` or `AUDIT`.
They are distinct operational objects.

### 5. Boots and templates should not collapse into one another

Boots should continue to hold:

- identity
- role law
- continuity load order
- lane law
- authority ceilings
- anti-drift obligations

Templates should hold:

- artifact structure
- output contract
- invariants
- lifecycle semantics

If boots absorb templates, machine legibility weakens.
If templates absorb boots, roles become flattened.

The system should keep both layers visible and distinct.

### 6. The active root is not ready for a full role-profile tree yet, but it is ready for the idea

The active root only recently restored a minimum template floor.
That means it is too early to explode into a large per-agent template catalog.

But it is not too early to define the rule:

> core templates stay shared by default; role-specific bindings are added where needed;
> wholly unique templates are reserved for genuinely role-native artifacts.

That is mature enough to guide future restoration without prematurely multiplying files.

## Implications

1. The future template system should not be “one template set per agent.”
2. It should become a **three-layer field**:
   shared core templates, role bindings, and rare truly role-native templates.
3. This structure matches the deeper ION idea better:
   universal machine law plus role-shaped cognition inside that law.
4. It also preserves portability.
   A future API-native runtime can still understand a shared `TASK` or `AUDIT` contract
   even if different roles bind to it differently.

## Recommended next moves

1. Do **not** duplicate the current template tree per agent.
2. When the next template-restoration pass happens, add a new explicit concept such as:
   `ION/07_templates/profiles/` or `ION/07_templates/bindings/`
   rather than creating fully separate per-agent template forests.
3. Only introduce a truly role-native template when all three conditions are met:
   - the artifact type is not just a flavored shared template,
   - the role’s output has distinct lifecycle semantics,
   - and independent review still benefits from the split more than it suffers from it.
4. Treat the current question as an architectural guideline now, not ratified doctrine yet.
