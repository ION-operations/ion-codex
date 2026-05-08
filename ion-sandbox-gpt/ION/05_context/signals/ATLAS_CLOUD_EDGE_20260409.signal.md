---
type: signal
from: Atlas
topic: Managed cloud load balancing and API gateway (AWS, Azure, GCP)
created: 2026-04-09
---

# ATLAS cloud edge wave (seed packages)

**New packages** (`ATLAS/systems/`):

| Slug | Focus |
|------|--------|
| `aws-elastic-load-balancing` | AWS ELB (ALB / NLB / GWLB / Classic per AWS docs) |
| `amazon-api-gateway` | Amazon API Gateway (HTTP/REST/WebSocket API front door) |
| `azure-application-gateway` | Azure Application Gateway (L7, WAF/AKS ingress patterns) |
| `gcp-load-balancing` | Google Cloud Load Balancing (L4/L7 families) |

**Comparative:** `ATLAS/comparative/ai_operating_system_reference_matrices.md` (§4 managed cloud row, §9 gaps)

**Script:** `ATLAS/scripts/scaffold_cloud_edge_wave.py`

**Indexes:** `ATLAS/indexes/systems_index.yaml`, `tag_index.yaml`

**Roadmap:** `ATLAS/_meta/AI_OS_EVOLUTION_ROADMAP.md` (executed 2026-04-09 section)

**Evidence:** Survey-grade scaffolds — pin **region**, **product version**, and **feature flag** before audit-grade claims (AWS/Azure/GCP surfaces change frequently).
