---
type: signal
from: Atlas
topic: Service mesh alternatives, eBPF dataplane, UEFI boot / UKI
created: 2026-04-05
---

# ATLAS mesh / boot / UKI wave (seed packages)

**New packages** (`ATLAS/systems/`):

| Slug | Focus |
|------|--------|
| `linkerd` | Kubernetes-native service mesh (Linkerd2 architecture) |
| `cilium` | eBPF-based networking / CNI / Gateway / mesh on Linux |
| `systemd-boot` | Minimal UEFI boot loader (systemd family) |
| `unified-kernel-image` | UKI — PE bundle of kernel + initrd + cmdline (UAPI.5, `systemd.ukify`) |

**Comparative:** `ATLAS/comparative/ai_operating_system_reference_matrices.md` (§1 loaders row, §8 mesh/boot rows, §9 gaps)

**Script:** `ATLAS/scripts/scaffold_mesh_boot_wave.py`

**Indexes:** `ATLAS/indexes/systems_index.yaml`, `tag_index.yaml`

**Roadmap:** `ATLAS/_meta/AI_OS_EVOLUTION_ROADMAP.md` (executed 2026-04-05 section)

**Locator fix:** UAPI UKI canonical path is `specs/unified_kernel_image/` (not `spec/unified_kernel_image/`).

**Evidence:** Survey-grade 00–14 scaffolds — deepen per slug before audit-grade claims.
