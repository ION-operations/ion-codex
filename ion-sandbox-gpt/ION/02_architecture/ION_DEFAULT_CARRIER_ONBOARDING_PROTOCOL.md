# ION Default Carrier Onboarding Protocol

## Purpose

ION carriers must have one unmistakable entry point. A carrier must not need to search handoffs, signals, templates, or chat history to discover the first actionable workflow packet.

The default front door is:

```text
ION/05_context/current/ACTIVE_WORK_PACKET.json
```

The default CLI/API surface is:

```bash
PYTHONPATH=ION/04_packages python3 -m kernel.ion_carrier_onboard --ion-root ION --carrier <carrier> --objective "<objective>" --json
```

## Law

1. Carrier is not identity. The carrier is the execution substrate.
2. ION role phases are the mounted identities in the packet.
3. The carrier starts from `ACTIVE_WORK_PACKET.json` if it exists.
4. If the active packet is missing, the onboarding tool creates it from the explicit objective and existing sequential route substrate.
5. The carrier must not infer workflow from repository-wide memory when the active packet exists.
6. The packet must declare role phase sequence, template, next lawful action, paths, validation commands, return contract, integration target, and visible report target.
7. Onboarding does not grant production authority or live execution authority.

## Relationship to existing ION route substrate

This protocol does not replace the sequential kernel router. It binds existing routing/load-target substrate into a carrier-visible active packet so every carrier has a canonical first read.
