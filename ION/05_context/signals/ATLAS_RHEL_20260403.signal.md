---
type: signal
from: Atlas
topic: Red Hat Enterprise Linux (rhel) linux-distribution package
created: 2026-04-03
---

# ATLAS — RHEL (`rhel`)

**New package:** `ATLAS/systems/rhel/` — full schema paths, `sources.yaml` (product + errata/life cycle + systemd admin pointer), ledger **rhel-001**–**rhel-003**.

**Tag:** **`linux-distribution`** in `tag_index.yaml`; `systems_index` **primary_kind** **`linux-distribution`**.

**Relations:** **`depends_on`** **`linux-kernel`**; **`integrates_with`** **`glibc`**, **`systemd`**, **`systemd-unit-model`**, **`gnu-libstdcxx`**, **`elf`**, **`gnu-gcc`**, **`gnu-binutils`**, **`clang`** (INFERRED), **`docker`**, **`containerd`** (INFERRED), **`kubernetes`** (INFERRED), **`oci-image-spec`** (INFERRED), **`red-hat-openshift`**; **`competes_with`** **`alpine-linux`** (reciprocal); **`fedora`** **`influences`** **`rhel`**; **`red-hat-openshift`** **`integrates_with`** **`rhel`**; toolchain/container reciprocals mirrored from **Fedora** wave.

**Comparative:** `ai_operating_system_reference_matrices.md` §8–§9 + §10 + **Forbidden merges**.

**Touch-up:** **`alpine-linux`** **`competes_with`** **`rhel`**; **`fedora`** **`relations.json`** / **`01_scope`** / **`12_relation_map`** for **`influences`** **`rhel`**.

**Roadmap:** `_meta/AI_OS_EVOLUTION_ROADMAP.md` — RHEL wave; **Next waves** Linux distro row.

**Witness:** root `ION/CAPSULE.md` **ION-104**; `ION/agents/atlas/CAPSULE.md` **A-064**.
