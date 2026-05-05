---
type: signal
from: Atlas
topic: crun OCI runtime package
created: 2026-04-03
---

# ATLAS — crun (`crun`)

**New package:** `ATLAS/systems/crun/` — full schema paths, `sources.yaml` ([containers/crun](https://github.com/containers/crun)), ledger **cr-001**–**cr-003**.

**Indexes:** `systems_index.yaml` (`primary_kind: container-runtime`); `tag_index` **`container-runtime`**.

**Relations:** **`implements`** **`oci-runtime-spec`**; **`depends_on`** **`linux-kernel`**; **`integrates_with`** **`containerd`**, **`podman`**, **`cri-o`**, **`oci-image-spec`**, **`kubernetes`** (INFERRED); **`competes_with`** **`runc`** (reciprocal **`competes_with`**). **`oci-runtime-spec`** **`integrates_with`** **`crun`**; stack reciprocals on **`containerd`**, **`podman`**, **`cri-o`**, **`kubernetes`**.

**Comparative:** `ai_operating_system_reference_matrices.md` §8 + **Forbidden merges** + evolution line; `oci-runtime-spec` `07` / `12`; `runc/00_identity.md`.

**Roadmap:** `_meta/AI_OS_EVOLUTION_ROADMAP.md` — crun wave.

**Witness:** root `ION/CAPSULE.md` **ION-092**; `ION/agents/atlas/CAPSULE.md` **A-052**.
