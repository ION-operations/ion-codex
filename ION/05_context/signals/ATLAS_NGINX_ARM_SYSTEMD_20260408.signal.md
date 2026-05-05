---
type: signal
from: Atlas
topic: NGINX, ingress-nginx, ARM CCA, systemd UKI/portable edges
created: 2026-04-08
---

# ATLAS NGINX / ARM CCA / systemd deepen wave

**New packages** (`ATLAS/systems/`):

| Slug | Focus |
|------|--------|
| `nginx` | Open-source NGINX HTTP server / reverse proxy |
| `ingress-nginx` | Kubernetes Ingress controller (NGINX datapath); `depends_on` `nginx` |
| `arm-cca` | Arm Confidential Compute Architecture overview grain |

**systemd deepen** (existing package):

- `relations.json`: `integrates_with` `systemd-boot`, `unified-kernel-image`
- `sources.yaml`: `src-systemd-ukify`, `src-systemd-portablectl`
- `13_evidence_ledger.md`: **sd-005** (ukify), **sd-006** (portablectl)

**Comparative:** `ATLAS/comparative/ai_operating_system_reference_matrices.md` (§1, §4, §8, §9)

**Script:** `ATLAS/scripts/scaffold_nginx_arm_wave.py`

**Indexes:** `ATLAS/indexes/systems_index.yaml`, `tag_index.yaml`

**Roadmap:** `ATLAS/_meta/AI_OS_EVOLUTION_ROADMAP.md` (executed 2026-04-08 section)

**Evidence:** New scaffolds are survey-grade; systemd remains **A** with added ledger rows only.
