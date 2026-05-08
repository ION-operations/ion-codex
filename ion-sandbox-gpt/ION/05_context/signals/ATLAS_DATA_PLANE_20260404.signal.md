---
type: signal
from: Atlas
topic: Data plane — databases, streaming, service mesh, boot loader
created: 2026-04-04
---

# ATLAS data-plane / mesh / boot wave (seed packages)

**New packages** (`ATLAS/systems/`):

| Slug | Focus |
|------|--------|
| `postgresql` | Relational server (wire protocol, SQL) |
| `sqlite` | Embedded SQL library / file format |
| `redis` | In-memory store (RESP) |
| `apache-kafka` | Partitioned event log / streaming |
| `envoy` | L7 proxy / mesh data plane (xDS) |
| `istio` | Service mesh (control plane + Envoy data plane) |
| `grub` | Boot loader (UEFI/BIOS adjacency to `uefi`) |

**Comparative:** `ATLAS/comparative/ai_operating_system_reference_matrices.md` (§8)

**Script:** `ATLAS/scripts/scaffold_data_plane_wave.py`

**Indexes:** `ATLAS/indexes/systems_index.yaml`, `tag_index.yaml`

**Roadmap:** `ATLAS/_meta/AI_OS_EVOLUTION_ROADMAP.md` (executed 2026-04-04 section)

**Evidence:** Survey-grade 00–14 scaffolds — deepen per slug before audit-grade claims.
