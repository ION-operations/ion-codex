---
type: protocol
authority: A3_OPERATIONAL
template: SPEC
created: 2026-04-03T19:23:00-04:00
status: ACTIVE
connections:
  - ION/02_architecture/META_TEMPLATE_CONSTITUTION_PROTOCOL.md
  - ION/07_templates/actions/TEMPLATE_DEVELOPMENT.md
  - ION/07_templates/README.md
  - ION/07_templates/_MASTER.md
  - ION/07_templates/bindings/README.md
  - ION/06_intelligence/research/2026-04-03_codex_template_architecture_shared_vs_agent_specific.md
  - ION/03_registry/boots/STEWARD.boot.md
  - ION/03_registry/boots/NEMESIS.boot.md
  - ION/03_registry/boots/MASON.boot.md
  - ION/03_registry/boots/THOTH.boot.md
  - ION/03_registry/boots/RELAY.boot.md
---

# TEMPLATE BINDING PROTOCOL

> Shared templates define common artifact law.
> Template bindings define how a particular role must use that shared template.
> Boots still define role identity, continuity, lane law, and authority ceilings.

## 1. Why this layer exists

The active `ION/` root now has a shared minimum template floor.
That is necessary, but not sufficient.

Different roles use the same artifact types with different rigor, risk, and authority.
If those differences live only in memory or scattered boot prose, the system loses both:

- machine-legible artifact stability, and
- explicit role-shaped execution discipline.

Bindings exist to solve that without fragmenting the template tree.

## 2. Three-layer rule

ION template architecture should be read as three layers:

### Layer A — Core templates

These are shared across the system.

They define:

- artifact shape,
- minimum required sections,
- invariant distinctions,
- lifecycle semantics,
- and machine-legible expectations.

Examples:

- `TASK`
- `SIGNAL`
- `RESEARCH`
- `AUDIT`
- `CODE`
- `HANDOFF`

### Layer B — Template bindings

These are role-template pairings.

They define:

- how a specific role should use a shared template,
- what extra rigor that role owes,
- what it must not silently claim,
- and what common failure patterns matter for that pairing.

Bindings do **not** replace the shared template.
They refine it.

### Layer C — Role-native templates

These are reserved for artifact types that are genuinely distinct, not merely flavored.

Examples that may justify true uniqueness:

- Daimon dissent objects
- relay packets
- archaeology findings
- kernel-router run bundles

## 3. What belongs in a binding

A binding should describe:

- the base shared template it binds to,
- the role it applies to,
- extra required emphases or sections,
- authority ceiling reminders,
- evidence rigor specific to the pairing,
- anti-drift notes,
- and escalation boundaries,
- and any required reasoning-journal triggers for risky execution.

## 4. What does not belong in a binding

A binding should **not** redefine:

- the role’s core identity,
- continuity load order,
- lane permissions,
- constitutional authority,
- or the full shared artifact schema.

Those belong in boots, doctrine, or the base template.

## 5. Binding file pattern

For the active root, binding files should live under:

- `ION/07_templates/bindings/`

Naming rule:

- `<ROLE>__<TEMPLATE>.md`

Examples:

- `STEWARD__TASK.md`
- `NEMESIS__AUDIT.md`
- `THOTH__RESEARCH.md`

## 6. Minimum binding structure

A binding should contain:

1. role
2. base template
3. purpose
4. additional obligations
5. authority boundaries
6. common failure patterns
7. relation to the role boot

## 7. Current status

This bindings layer is a **current-phase operational layer**.
It is not yet final constitutional template law.

The active rule today is:

- shared core templates remain primary,
- bindings may be added when a role-template pair has clearly distinct discipline,
- and full per-agent template duplication remains disallowed.

## 8. Rollout rule

Only add a binding when all three are true:

1. the role repeatedly uses the base template,
2. the role’s extra discipline is real rather than cosmetic,
3. and the extra layer improves clarity more than it increases complexity.

## 9. Immediate first-pass scope

The current first-pass bindings are intentionally narrow:

- Steward + TASK
- Mason + CODE
- Thoth + RESEARCH
- Nemesis + AUDIT
- Relay + HANDOFF
- Steward + PROPOSAL

This is enough to prove the layer without turning the template tree into a second boot tree.
