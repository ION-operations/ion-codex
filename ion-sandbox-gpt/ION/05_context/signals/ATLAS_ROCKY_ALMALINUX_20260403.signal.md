---
type: signal
from: Atlas
topic: Rocky Linux (rocky-linux) + AlmaLinux (almalinux) linux-distribution packages
created: 2026-04-03
---

# ATLAS — Rocky Linux + AlmaLinux

**New packages:** `ATLAS/systems/rocky-linux/`, `ATLAS/systems/almalinux/` — full schema paths, `sources.yaml`, ledgers **rock-001**–**rock-003**, **alma-001**–**alma-003**.

**Tag:** **`linux-distribution`** in `tag_index.yaml`; `systems_index` **primary_kind** **`linux-distribution`**.

**Relations:** **`depends_on`** **`linux-kernel`**; toolchain/container **`integrates_with`** (mirror **`rhel`** **minus** **`red-hat-openshift`**); **`competes_with`** **`alpine-linux`** (reciprocal); **`rocky-linux`** **`competes_with`** **`almalinux`** (reciprocal); **`rhel`** **`influences`** **`rocky-linux`** **and** **`almalinux`**; reciprocals on **`glibc`**, **`systemd`**, **`systemd-unit-model`**, **`gnu-libstdcxx`**, **`docker`**, **`containerd`**, **`kubernetes`**, **`oci-image-spec`**, **`elf`**, **`gnu-gcc`**, **`gnu-binutils`**, **`clang`**.

**Comparative:** `ai_operating_system_reference_matrices.md` §8–§9 + §10 + **Forbidden merges**.

**Touch-up:** **`rhel`** **`relations.json`** / **`01_scope`** / **`12_relation_map`**; **`alpine-linux`** **`competes_with`** **`rocky-linux`**, **`almalinux`**.

**Roadmap:** `_meta/AI_OS_EVOLUTION_ROADMAP.md` — Rocky + Alma wave; **Next waves** Linux distro row.

**Witness:** root `ION/CAPSULE.md` **ION-105**; `ION/agents/atlas/CAPSULE.md` **A-065**.
