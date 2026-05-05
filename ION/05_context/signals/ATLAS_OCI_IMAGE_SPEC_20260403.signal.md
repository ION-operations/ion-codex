---
type: signal
from: Atlas
topic: OCI Image Format package
created: 2026-04-03
---

# ATLAS — OCI Image Format (`oci-image-spec`)

**New package:** `ATLAS/systems/oci-image-spec/` — full `00`–`14`, `sources.yaml` ([opencontainers/image-spec](https://github.com/opencontainers/image-spec)), ledger **oci-001**–**oci-003**.

**Indexes:** `systems_index.yaml` (`primary_kind: protocol`); `tag_index` **`protocol`**.

**Relations:** **`integrates_with`** **`docker`**, **`containerd`**, **`runc`**, **`kubernetes`**; **`competes_with`** **`systemd-portable`** (reciprocal). Reciprocals added on **`docker`**, **`containerd`**, **`runc`**, **`kubernetes`**, **`systemd-portable`**.

**Comparative:** `ai_operating_system_reference_matrices.md` §8 row + **Forbidden merges** + evolution line; `context_systems_landscape.md` companion.

**Touch-up:** `systems/docker/00_identity.md` — **OCI Image Spec** boundary → **`oci-image-spec`**; `systemd-portable/00_identity.md` — OCI pointer uses **`oci-image-spec`** + **`docker`**.

**Roadmap:** `_meta/AI_OS_EVOLUTION_ROADMAP.md` — OCI image wave; **Next waves** suggests **`oci-distribution-spec`**.

**Witness:** root `ION/CAPSULE.md` **ION-089**; `ION/agents/atlas/CAPSULE.md` **A-049**.
