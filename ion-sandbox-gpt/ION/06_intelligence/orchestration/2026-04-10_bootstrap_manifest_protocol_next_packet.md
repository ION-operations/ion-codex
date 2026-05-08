---
type: orchestration
authority: A2_EXECUTOR
created: 2026-04-10T21:10:00-04:00
status: ACTIVE
---

# Bootstrap manifest protocol — next packet

## Current truth

The current branch now supports all of the following for fresh extracted roots:

1. `bootstrap init` — write one canonical bootstrap packet
2. `bootstrap emit` — emit one canonical daemon signal
3. `daemon run` — consume that signal lawfully
4. `bootstrap activate` — orchestrate the same three-step chain with linked receipts

## What remains missing

The current surfaces are excellent for one bootstrap packet.
They are not yet the cleanest shape for roots that need multiple bootstrap pressures or role-specific bootstrap packets.

## Next bounded objective

Define one **visible bootstrap manifest** that can declaratively mint one or more bootstrap packets while preserving the existing packet/bridge/daemon layering.

## Preferred order

1. **manifest -> packet set**
   - preserve packet law
   - preserve existing bridge and daemon law
   - widen only the earliest declaration surface

2. **manifest -> activation ceremony**
   - useful later
   - wider because it combines declaration and activation

3. **manifest -> direct daemon pressure**
   - should not be the next move
   - skips the now-valuable packet layer

## Recommendation

Choose option 1 first.

The next packet should land:

- one visible bootstrap manifest shape
- one parser that renders one or more canonical bootstrap task packets
- one focused test proving manifest -> packet set, while leaving bridge/daemon behavior unchanged

## Anti-drift rule

Do not collapse the packet lane.
The manifest should widen only declaration.
It should not become a hidden replacement for packet law.
