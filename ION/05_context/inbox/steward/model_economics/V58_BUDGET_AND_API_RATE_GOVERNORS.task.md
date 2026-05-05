# V58 Budget and API Rate Governors Task

**Task:** Install deterministic budget-governor and API-rate-governor surfaces for the model-economics lane.  
**Authority:** A3 Steward candidate  
**Production authority:** false  
**Live provider calls:** false  
**Credentials:** false

Acceptance:

- `budget_governor.py` classifies allow / approval / downgrade / batch / block.
- `api_rate_governor.py` classifies allow / queue / reroute / batch / throttle / block.
- Both surfaces preserve separation from router, scheduler, provider adapters, and model-call receipts.
- Tests pass without credentials or provider access.

