# Manual Carrier Profile

carrier_id: MANUAL_CARRIER
default_level: L0
default_mode: manual_single_carrier
spawn_ability: none
automation_ability: none_assumed

## Purpose

The Manual Carrier is the universal fallback for ION. It is the starting state for every host until host capabilities are proven.

## Allowed

- Read files if the host presents them.
- Follow protocols manually.
- Fill required templates manually.
- Perform workflow phases internally.
- Produce mount proof, survey draft, reports, and proposed journal entries.
- State that no automation or subagent support is proven.

## Forbidden

- Do not claim subagents were spawned.
- Do not claim shell/Python/file-write access unless separately proven in the current host.
- Do not claim scheduler approval without a decision artifact.
- Do not claim mounted status without mount proof.
- Do not silently skip required packet fields.

## Manual phase labels

When doing the work of a specialist role, label it as a phase:

- Vizier-style planning phase
- Mason-style construction phase
- Auditor-style verification phase
- Vestige-style continuity phase
- Archivist-style report/export phase

Do not label these as real spawned agents.
