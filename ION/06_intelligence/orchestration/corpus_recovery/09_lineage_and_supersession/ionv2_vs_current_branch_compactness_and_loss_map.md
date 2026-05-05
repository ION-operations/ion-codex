# IONv2 vs current branch compactness and loss map

## Question
How does `IONv2` compare to the current branch around compact executable implementation memory?

## Static comparison
- `IONv2` Python modules: **37**
- current branch Python kernel modules: **89**
- common same-path modules: **9**
- exact same same-path modules: **0**
- common basenames across important core families: **10**
  - `capsule_manager.py`
  - `context_compiler.py`
  - `governed_write.py`
  - `graph.py`
  - `index.py`
  - `model.py`
  - `store.py`
  - `threshold.py`
  - `execution.py`
  - `__init__.py`

Interpretation:
- `IONv2` is not simply the same implementation line as the current branch
- but it clearly preserves a compact family around context-compiler / governed-write / model-store-graph concerns

## Executable posture
- `IONv2` pytest: **366 passed, 3 failed**
- the 3 failures come from `tests/test_live_gemini.py` and reflect missing async/plugin posture rather than broad collapse

## Judgment
`IONv2` is a serious compact executable witness of an adjacent implementation philosophy:
- stronger compression
- broad runnable posture
- important continuity around governed-write/context-compiler concerns

The current branch preserves a broader repaired law/template/runtime line, but it should not erase the compact executable lesson carried by `IONv2`.

## Recovery implication
A future coherent ION center may need to recover not only historical features, but also historical **compression disciplines** from `IONv2` and the precursor pair.
