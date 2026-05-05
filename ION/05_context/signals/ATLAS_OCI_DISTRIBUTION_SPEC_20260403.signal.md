---
type: signal
from: Atlas
topic: OCI Distribution Specification package
created: 2026-04-03
---

# ATLAS — OCI Distribution Specification (`oci-distribution-spec`)

**New package:** `ATLAS/systems/oci-distribution-spec/` — full schema paths, `sources.yaml` ([opencontainers/distribution-spec](https://github.com/opencontainers/distribution-spec)), ledger **dist-001**–**dist-003**.

**Indexes:** `systems_index.yaml` (`primary_kind: protocol`); `tag_index` **`protocol`**.

**Relations:** **`integrates_with`** **`oci-image-spec`**, **`docker`**, **`containerd`**, **`kubernetes`**, **`podman`**, **`cri-o`** (reciprocals). **`oci-image-spec`** **`integrates_with`** **`oci-distribution-spec`** (reciprocal).

**Comparative:** `ai_operating_system_reference_matrices.md` §8 row + **Forbidden merges** + evolution line; `context_systems_landscape.md` companion.

**Touch-up:** `oci-image-spec/01_scope.md`, `05_storage_network_ipc.md`, `12_relation_map.md`; `docker/00_identity.md` — registry API boundary.

**Roadmap:** `_meta/AI_OS_EVOLUTION_ROADMAP.md` — distribution wave; **Next waves** OCI/registry row marked **Done**.

**Witness:** root `ION/CAPSULE.md` **ION-090**; `ION/agents/atlas/CAPSULE.md` **A-050**.
