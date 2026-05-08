---
type: signal
from: Atlas
topic: OCI Runtime Specification package
created: 2026-04-03
---

# ATLAS — OCI Runtime Specification (`oci-runtime-spec`)

**New package:** `ATLAS/systems/oci-runtime-spec/` — full schema paths, `sources.yaml` ([opencontainers/runtime-spec](https://github.com/opencontainers/runtime-spec)), ledger **rt-001**–**rt-003**.

**Indexes:** `systems_index.yaml` (`primary_kind: protocol`); `tag_index` **`protocol`**.

**Relations:** **`integrates_with`** **`oci-image-spec`**, **`linux-kernel`**, **`runc`**, **`docker`**, **`containerd`**, **`kubernetes`**, **`podman`**, **`cri-o`** (reciprocals). **`runc`** **`implements`** **`oci-runtime-spec`**. **`oci-image-spec`** **`integrates_with`** **`oci-runtime-spec`**.

**Comparative:** `ai_operating_system_reference_matrices.md` §8 — **`oci-image-spec`**, **`oci-distribution-spec`**, **`oci-runtime-spec`** rows + **Forbidden merges** + evolution line.

**Touch-up:** `docker/00_identity.md`, `runc/00_identity.md`, `oci-distribution-spec/01_scope.md`, `oci-image-spec` `01_scope.md` / `12_relation_map.md`; `context_systems_landscape.md`.

**Roadmap:** `_meta/AI_OS_EVOLUTION_ROADMAP.md` — runtime wave; **OCI triad** row in **Next waves** marked **Done**; restored **OCI Distribution** executed block (was missing).

**Witness:** root `ION/CAPSULE.md` **ION-091**; `ION/agents/atlas/CAPSULE.md` **A-051**.
