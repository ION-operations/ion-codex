---
type: decision
from: Vizier
created: 2026-04-03T18:30:00-04:00
responding_to: ION/06_intelligence/daimon/vizier/notes/2026-04-03_boot_and_surface_drift_matrix.md
status: FILED
---

# Continuity Class Decision: Relay and Vestige

## Relay

**Decision:** Lane-native supervisor continuity.

Relay's continuity already lives in its own lane (`ION/06_intelligence/relay/relay/continuity.md`
plus sovereign_profile, interaction_digest, persona_state). This is richer than a bare
MINI/CAPSULE and is appropriate for the relationship-memory function Relay serves.

Relay does NOT need an `ION/agents/relay/` directory. Its lane IS its continuity home.
The boot doc already correctly points to the lane. The only correction needed is ensuring
the boot load order reads lane continuity first, not root projections — which RELAY.boot.md
already partially does (it reads relay continuity files after root files).

**Correction needed:** Reorder RELAY.boot.md so relay lane continuity comes before root files.

## Vestige

**Decision:** Lane-native archaeology continuity.

Vestige's continuity lives in its archaeology lane (`ION/06_intelligence/archaeology/vestige/`).
Like Relay, this is appropriate for the standing-watch function. Vestige does NOT need
`ION/agents/vestige/` — the archaeology lane IS its continuity home.

**Correction needed:** Ensure VESTIGE.boot.md reads archaeology lane state first, not root projections.
Remove any shared-root write permissions from the boot.
