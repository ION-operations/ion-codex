---
type: signal
from: Atlas
topic: Ingress breadth (Emissary, HAProxy) and x86 TEE vendor grains
created: 2026-04-07
---

# ATLAS ingress + TEE vendor wave (seed packages)

**New packages** (`ATLAS/systems/`):

| Slug | Focus |
|------|--------|
| `emissary-ingress` | CNCF Envoy-based Kubernetes ingress / API gateway |
| `haproxy` | TCP/HTTP load balancer and reverse proxy |
| `intel-tdx` | Intel Trust Domain Extensions (confidential VM class) |
| `amd-sev` | AMD SEV / SEV-SNP (memory encryption / guest isolation) |

**Comparative:** `ATLAS/comparative/ai_operating_system_reference_matrices.md` (§1 TEE row, §4 ingress row, §9 gaps)

**Script:** `ATLAS/scripts/scaffold_ingress_tee_wave.py`

**Indexes:** `ATLAS/indexes/systems_index.yaml`, `tag_index.yaml`

**Roadmap:** `ATLAS/_meta/AI_OS_EVOLUTION_ROADMAP.md` (executed 2026-04-07 section)

**Locator note:** Emissary primary locators use **CNCF project page** + **GitHub** (`emissary.io/docs/...` returned 404 at capture time).

**Evidence:** Survey-grade 00–14 scaffolds — pin CPU generation / kernel version for TEE claims before audit-grade use.
