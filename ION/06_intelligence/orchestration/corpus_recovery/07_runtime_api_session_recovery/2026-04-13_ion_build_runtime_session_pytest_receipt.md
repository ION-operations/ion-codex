# Executable receipt — ION-BUILD runtime/session center

## Workspace
- Extracted witness root from `ION - Production(2).zip`
- Local path used during verification: `ION - Production/ION-BUILD/`

## Commands run
```bash
cd "ION - Production/ION-BUILD"
python -m pytest tests/test_runtime_sessions.py tests/test_runtime_server_engine_routing.py -q
```

## Result
- `7 passed`

## What this proves
This is stronger than static file presence alone.
It shows the ION-BUILD line still carries a runnable/test-backed runtime/session center including:
- runtime sessions
- runtime server engine routing
- a testable pytest harness with `pythonpath = src`

## Supporting evidence paths
- `ION - Production/ION-BUILD/pyproject.toml`
- `ION - Production/ION-BUILD/pytest.ini`
- `ION - Production/ION-BUILD/tests/test_runtime_sessions.py`
- `ION - Production/ION-BUILD/tests/test_runtime_server_engine_routing.py`
- `ION - Production/ION-BUILD/src/ion/entry/api.py`

## Interpretation
ION-BUILD is not just a historical documentation center. It remains the strongest currently evidenced runtime/API/session preservation line in the production estate.
