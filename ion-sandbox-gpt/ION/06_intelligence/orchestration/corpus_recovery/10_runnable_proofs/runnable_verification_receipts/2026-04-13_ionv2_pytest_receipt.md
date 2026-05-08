# IONv2 pytest receipt

## Scope
Executable recovery receipt for the `IONv2` line.

## Recovery workspace
- Extracted from `ION - Production(2).zip`
- Workspace root: `IONv2/`

## Command
- `pytest -q`

## Result
- `366 passed, 3 failed`

## Failure class
All three failures came from `tests/test_live_gemini.py` and were caused by missing async pytest plugin support in the current recovery environment, not by broad line collapse.

Observed error pattern:
- `async def functions are not natively supported`
- suggested missing plugin types included `pytest-asyncio`, `anyio`, `pytest-trio`, etc.

## Interpretation
This is strong executable evidence that:
- `IONv2` is a large runnable/tested compact line
- most of the suite executes cleanly in the current recovery environment
- the remaining failures appear environment/plugin-bound rather than evidence of total implementation failure

## Recovery value
`IONv2` should be treated as a serious compact implementation witness and not merely a minor sibling. It appears particularly relevant to governed-write/context-compiler/continuity-adjacent compact implementation memory.
