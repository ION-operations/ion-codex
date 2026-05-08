# V58 Budget and API Rate Governors Lock

**Version:** V58_BUDGET_AND_API_RATE_GOVERNORS  
**Authority:** A3 Steward model-economics candidate surface  
**Production authority:** false  
**Live provider API calls authorized:** false  
**Provider credentials authorized:** false  
**Scheduler direct provider calls authorized:** false

V58 installs deterministic budget-governor and API-rate-governor surfaces for the API Provider Orchestration / Model Economics lane.

The scheduler still does not call providers directly. The router still only selects a dry-run candidate. V58 answers two separate questions:

1. **Budget Governor:** should this candidate run economically under the workflow budget posture?
2. **API Rate Governor:** may this candidate dispatch now under the known/placeholder provider capacity state?

These governors are deterministic policy surfaces only. They do not execute provider calls, load credentials, enforce production quotas, or grant production model-routing authority.

