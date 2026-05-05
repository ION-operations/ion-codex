---
type: signal
from: Atlas
topic: Global CDN and edge compute (Azure Front Door, CloudFront, Cloudflare Workers)
created: 2026-04-10
---

# ATLAS CDN / edge-compute wave (seed packages)

**New packages** (`ATLAS/systems/`):

| Slug | Focus |
|------|--------|
| `azure-front-door` | Azure global CDN / WAF / routing (vs regional Application Gateway) |
| `amazon-cloudfront` | AWS CDN; S3 and ALB/API Gateway as common origins |
| `cloudflare-workers` | Serverless JS/Wasm at Cloudflare PoPs |

**Comparative:** `ATLAS/comparative/ai_operating_system_reference_matrices.md` (§4 CDN row, §9 gaps)

**Script:** `ATLAS/scripts/scaffold_cdn_edge_wave.py`

**Indexes:** `ATLAS/indexes/systems_index.yaml`, `tag_index.yaml` (`distributed-system` backfilled with managed-edge slugs from 2026-04-09 wave)

**Roadmap:** `ATLAS/_meta/AI_OS_EVOLUTION_ROADMAP.md` (executed 2026-04-10 section)

**Evidence:** Survey-grade scaffolds — edge SKUs, pricing tiers, and protocol features change often; pin **doc revision** before audit-grade claims.
