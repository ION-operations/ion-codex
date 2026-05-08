---
type: signal
from: Atlas
topic: WASI and WebAssembly Component Model — Systems ATLAS protocol packages
created: 2026-04-03
---

# WASI / Component Model seeded

**New packages:**

- `ATLAS/systems/wasi/` — **WASI** ([wasi.dev](https://wasi.dev/), [WebAssembly/WASI](https://github.com/WebAssembly/WASI)); **`depends_on`** → **`webassembly`**.
- `ATLAS/systems/wasm-component-model/` — **Component Model** ([Bytecode Alliance book](https://component-model.bytecodealliance.org/), [WebAssembly/component-model](https://github.com/WebAssembly/component-model)); **`depends_on`** → **`webassembly`**; **`integrates_with`** → **`wasi`** (INFERRED).

**Updated:**

- `ATLAS/indexes/systems_index.yaml`, `ATLAS/indexes/tag_index.yaml` (`protocol`)
- `ATLAS/comparative/language_machine_and_assembly_stack.md` — §6 **Wasm host extensions** subsection; §8 gaps (AMD ROCm optional)
- `ATLAS/README.md`

**Evidence:** community specs + books; **pin** **snapshot** **/** **proposal** **IDs** for syscall-level claims.
