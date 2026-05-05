---
type: research
from: Codex
authority: A3_OPERATIONAL
created: 2026-04-03T13:46:40-04:00
status: FILED
subject: Supervisor continuity correction package
responding_to:
  - ION/02_architecture/CONTINUITY_ARCHITECTURE.md
  - ION/03_registry/boots/RELAY.boot.md
  - ION/03_registry/boots/VESTIGE.boot.md
  - ION/02_architecture/ARCHAEOLOGY_DAEMON_PROTOCOL.md
  - ION/06_intelligence/decisions/relay_vestige_continuity_class.md
  - ION/06_intelligence/daimon/vizier/notes/2026-04-03_supervisor_continuity_classification_vice.md
---

# Codex Supervisor Continuity Correction Package

## Claim

The continuity correction has landed for core task roles, but the supervisor layer is
still only partially aligned.

The remaining drift is now specific:

- `CONTINUITY_ARCHITECTURE.md` still overstates `ION/agents/{role}/` as the universal
  physical form of source continuity
- `RELAY.boot.md` still loads root projections before Relay's own lane continuity
- `VESTIGE.boot.md` still loads root projections before Vestige continuity and still
  grants shared-root write behavior
- `ARCHAEOLOGY_DAEMON_PROTOCOL.md` still grants Vestige writes to root `ION/CAPSULE.md`
  and `ION/STATUS.md`

## Governing correction already on disk

The needed correction is already decided in substance:

- `ION/06_intelligence/decisions/relay_vestige_continuity_class.md`
- `ION/06_intelligence/daimon/vizier/notes/2026-04-03_supervisor_continuity_classification_vice.md`

Working sentence:

> Core task roles use `ION/agents/{role}/` as source continuity; supervisor roles may
> use a role-owned lane as source continuity when that lane already contains the stable
> private state family. In all cases, root shared surfaces remain projections, not
> source state.

## Surface-by-surface correction package

### A. `CONTINUITY_ARCHITECTURE.md`

The document should stop saying every role's source continuity is physically shaped as
`ION/agents/{agent_name}/`.

#### Replacement concept

Replace the current universal wording in section `1.1 Private Continuity` with a
role-owned continuity model:

```md
### 1.1 Source Continuity Is Role-Owned

Every role maintains one private source continuity root.

For core task roles, that root is typically:

ION/agents/{agent_name}/
├── MINI.md
├── CAPSULE.md
├── history/
└── context/ (if needed)

For lane-native supervisor roles, that root may be the role's own lane when the lane
already contains the stable private state family.

Current supervisor examples:

- Relay → `ION/06_intelligence/relay/relay/`
- Vestige → `ION/06_intelligence/archaeology/vestige/`

No role writes another role's private continuity. Ever.
```

#### Replacement concept for section 2

Replace `PER-AGENT CONTINUITY SETUP` with a classification table:

```md
| Role Class | Role | Source Continuity Root | Boot Doc |
|------------|------|------------------------|----------|
| Core task role | Vizier | `ION/agents/vizier/` | `ION/03_registry/boots/VIZIER.boot.md` |
| Core task role | Vice | `ION/agents/vice/` | `ION/03_registry/boots/VICE.boot.md` |
| Core task role | Nemesis | `ION/agents/nemesis/` | `ION/03_registry/boots/NEMESIS.boot.md` |
| Core task role | Mason | `ION/agents/mason/` | `ION/03_registry/boots/MASON.boot.md` |
| Core task role | Scribe | `ION/agents/scribe/` | `ION/03_registry/boots/SCRIBE.boot.md` |
| Core task role | Thoth | `ION/agents/thoth/` | `ION/03_registry/boots/THOTH.boot.md` |
| Lane-native supervisor | Relay | `ION/06_intelligence/relay/relay/` | `ION/03_registry/boots/RELAY.boot.md` |
| Lane-native supervisor | Vestige | `ION/06_intelligence/archaeology/vestige/` | `ION/03_registry/boots/VESTIGE.boot.md` |
```

#### Replacement concept for boot sequence

```md
1. Read own boot doc
2. Read own role-owned source continuity first
3. Read assigned tasks, relevant signals, and routed files
4. Optionally read shared projections for orientation only
5. Begin work
6. Update only own source continuity and public artifacts
```

### B. `RELAY.boot.md`

The boot already has the right write boundaries.
The main defect is load order.

#### Replacement ON SESSION START

```md
1. Read this boot document
2. Read `ION/06_intelligence/relay/relay/continuity.md`
3. Read `ION/06_intelligence/relay/relay/sovereign_profile.md`
4. Read `ION/06_intelligence/relay/relay/interaction_digest.md`
5. Read `ION/06_intelligence/relay/relay/persona_state.md`
6. Read recent signals in `ION/05_context/signals/`
7. Read any inbound or outbound relay packets still open in your lane
8. Optionally read `ION/MINI.md`, `ION/STATUS.md`, and `ION/CAPSULE.md` as shared projections only
9. Begin the current relay thread with the Sovereign
```

### C. `VESTIGE.boot.md`

Vestige needs both load-order correction and write-boundary correction.

#### Replacement ON SESSION START

```md
1. Read this boot document
2. Read `ION/06_intelligence/archaeology/vestige/continuity.md`
3. Read `ION/06_intelligence/archaeology/vestige/watchlist.md`
4. Read recent signals in `ION/05_context/signals/`
5. Inspect new audits, decisions, specs, and open threads relevant to the current phase
6. Optionally read `ION/MINI.md`, `ION/STATUS.md`, and `ION/CAPSULE.md` as shared projections only
7. Begin the highest-priority excavation pass from your watchlist or current-phase triggers
```

#### Replacement YOUR LANE

Remove:

- `ION/CAPSULE.md` — append your own entries
- `ION/STATUS.md` — update YOUR section only

Keep Vestige fully inside:

- `ION/06_intelligence/archaeology/vestige/continuity.md`
- `ION/06_intelligence/archaeology/vestige/watchlist.md`
- `ION/06_intelligence/archaeology/vestige/reports/`
- `ION/06_intelligence/archaeology/vestige/alerts/`
- `ION/06_intelligence/archaeology/vestige/open_threads/`
- `ION/05_context/signals/`

### D. `ARCHAEOLOGY_DAEMON_PROTOCOL.md`

This protocol should match the same lane-native supervisor rule.

#### Replacement for section 4 output surfaces

Delete:

- `ION/CAPSULE.md` for its own work-log entries
- `ION/STATUS.md` for its own section only

Replace with a short clarification:

```md
Vestige does not use root `ION/CAPSULE.md` or `ION/STATUS.md` as private continuity.
If shared operator projections are useful, they are read as projections only.
Vestige's source continuity remains inside its archaeology lane.
```

## Why this package is narrow

This does not reopen the continuity law itself.
It simply brings the architecture and supervisor surfaces into line with a decision
that is already effectively made elsewhere on disk.

## Recommended execution order

1. Patch `CONTINUITY_ARCHITECTURE.md`
2. Patch `RELAY.boot.md`
3. Patch `VESTIGE.boot.md`
4. Patch `ARCHAEOLOGY_DAEMON_PROTOCOL.md`
5. Emit one short signal that supervisor continuity classification is now encoded in the active surfaces
