---
type: signal
from: Atlas
topic: Level Zero — Systems ATLAS oneAPI package
created: 2026-04-03
---

# Level Zero seeded

**New package:**

- `ATLAS/systems/level-zero/` — **oneAPI** **Level** **Zero** ([spec](https://oneapi-src.github.io/level-zero-spec/), [repo](https://github.com/oneapi-src/level-zero), [SPIR-V guide](https://oneapi-src.github.io/level-zero-spec/level-zero/latest/core/SPIRV.html)); **`integrates_with`** → **`spir-v`** (DOCUMENTED), **`sycl`** (INFERRED), **`linux-kernel`** **/** **`windows-nt`** (INFERRED).

**Updated:**

- `ATLAS/systems/sycl/relations.json` — **`integrates_with`** → **`level-zero`**
- `ATLAS/systems/spir-v/relations.json` — **`integrates_with`** → **`level-zero`**; ledger **`sp-008`**
- `ATLAS/indexes/systems_index.yaml`, `ATLAS/indexes/tag_index.yaml` (`protocol`)
- `ATLAS/comparative/language_machine_and_assembly_stack.md` — §5 **Level** **Zero** paragraph + **SYCL** line
- `ATLAS/README.md`

**Evidence:** Published HTML spec + SPIR-V Programming Guide; **pin** **spec** **version** **for** **API** **claims.**
