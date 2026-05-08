# Specialist Domain Routing Protocol v0.1

## Status

Candidate current-context protocol. Not accepted canon.

## Purpose

Prevent generic-agent overreach by routing repeated AI-assistant work into specialist domains and agents.

## Rule

When a task names or implies a stable work family, route to the specialist domain before execution.

Examples:

- UI → `ui_ux_domain` before implementation.
- Docs → `documentation_writing_domain` before writing.
- Tests → `testing_quality_domain` before validation claims.
- Security → `review_security_domain` before risk closure.
- IDE workspace work → `ide_work_domain` before code changes.
- Feature delivery → product + planning + UI/docs/tests/release + settlement.

## Template/agent relationship

```text
template = action grammar
domain = governed work field
agent = domain-local interface
protocol = movement rule
receipt = inheritance unit
```

A template without an agent can format output but cannot maintain domain-local context over time.

An agent without a domain is roleplay.

A domain without templates is informed improvisation.

A result without receipt is weak inheritance.
