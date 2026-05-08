---
type: research
authority: A3_OPERATIONAL
template: RESEARCH
created: 2026-04-03T09:15:00-04:00
status: COMPLETE
goal: Inventory all existing multi-model orchestration systems across ION roots for dual-model leadership protocol design
connections:
  - ION/02_architecture/MULTI_CHAT_COORDINATION.md
  - ION/02_architecture/ION_OVER_CURSOR_PROTOCOL.md
  - SOS-OPUS/01_doctrine/SOVEREIGN_KERNEL.md (K6 Chassis Management)
  - SOS-OPUS/01_doctrine/SOVEREIGN_CONSTITUTION.md (Art. 17 Chassis Decoupling)
---

# Multi-Model Orchestration: Existing Systems Inventory

**Context:** A blind test during the ION consolidation revealed that switching the Vizier
role from Claude Opus 4.6 to GPT 5.4 for a contract-tightening pass produced the highest-quality
output in the audit trail. Nemesis (GPT 5.4) proposes designing a formal dual-model/parallel
protocol for leadership roles. This document inventories what already exists to build from.

---

## 1. WORKING CODE (ready to port or integrate)

### 1.1 IONv2 K-Gate Router
**Path:** `/home/sev/ION - Production/IONv2/ion/llm/router.py`
**What:** `KGateRouter` scores task complexity and routes between Ollama (cheap/local) and Gemini (capable). Threshold 0.3. Auto-fallback if primary unavailable.
**Key idea:** Complexity-based routing between two tiers of model.
**Maturity:** Working Python with tests.

### 1.2 Operation-Victus K-Gate (expanded)
**Path:** `/home/sev/ION - Production/operation-victus/victus/k_gate.py`
**What:** Scores complexity/risk/novelty/quality. Has `PHASE_ROUTING` overrides (plan→Gemini CLI, verify→Ollama). Threshold 0.6. `PHASE_OLLAMA_TYPE` for local model selection.
**Key idea:** Phase-aware routing — different models for different stages of the same workflow.
**Maturity:** Working Python.

### 1.3 Operation-Victus Mission Controller
**Path:** `/home/sev/ION - Production/operation-victus/victus/mission_controller.py`
**What:** `ExecutionEngine` enum (PIPELINE, DAG, MESH, CRUCIBLE). Routes by task type, context size, explicit override. Context >100k → MESH.
**Key idea:** Execution STRATEGY routing, not just model routing. Different architectures for different problem shapes.
**Maturity:** Working Python.

### 1.4 SOS Model Registry
**Path:** `/home/sev/ION - Production/SOS/04_packages/cognitive/src/model_registry.py`
**What:** `ModelRegistry` with `TASK_MODEL_MAP` (task type → model id). Budgets. Per-phase/per-agent usage tracking.
**Key idea:** Task-to-model mapping with budget enforcement.
**Maturity:** Working Python. Gemini-only catalog (no multi-provider).

### 1.5 AIM-OS LLM Router (MOST COMPLETE)
**Path:** `/home/sev/AIM-OS/scripts/ai_engine/llm_router.py`
**What:** Full multi-provider router. Task-based model mapping. Provider priority chain (gemini-cli → openai → anthropic → deepseek). Auto-fallback. Retries.
**Key idea:** Multi-provider with cost-optimized priority ordering and automatic failover.
**Maturity:** Working Python.

### 1.6 AIM-OS APOE Model Selector (MOST RELEVANT TO OUR QUESTION)
**Path:** `/home/sev/AIM-OS/packages/apoe/model_selector.py`
**What:** `ModelSelector` with `CROSS_MODEL` vs `SINGLE_MODEL` strategies. `ModelInfo` registry with cost/quality/speed. Cost constraints and quality requirements. **Pairs "smart" and "execution" models for cost reduction while meeting quality bars.**
**Key idea:** CROSS-MODEL PAIRING — this is exactly what we discovered empirically with Opus + GPT 5.4.
**Maturity:** Working Python with tests.

### 1.7 AIM-OS Unified LLM Client
**Path:** `/home/sev/AIM-OS/packages/llm_client/`
**What:** Abstract `LLMClient` base + Gemini, Anthropic, Cerebras implementations. Standardized `LLMResponse`.
**Key idea:** Single interface over multiple vendors.
**Maturity:** Working Python.

### 1.8 IONv2 Cognitive Loop
**Path:** `/home/sev/ION - Production/IONv2/ion/cognitive_loop.py`
**What:** Compile context → K-Gate route → query LLM → grade beliefs → propose. Navigator integration.
**Key idea:** The K-Gate router is embedded in the cognitive execution loop, not external to it.
**Maturity:** Working Python with tests (but not wired as default engine path).

---

## 2. DOCTRINE (constitutional/kernel law)

### 2.1 Sovereign Kernel K6 — Chassis Management
**Source:** `SOS-OPUS/01_doctrine/SOVEREIGN_KERNEL.md`
- Chassis types: GEMINI_CLI, GEMINI_API, CLAUDE_IDE, GPT_API, LOCAL (Ollama/vLLM)
- Load Balancer: Try FREE first → failover to PAID → emit TASK_FAILED
- Chassis Decoupling: Agent identity independent of chassis. Re-mount on failure.

### 2.2 Constitution Art. 17 — Chassis Decoupling
**Source:** `SOS-OPUS/01_doctrine/SOVEREIGN_CONSTITUTION.md`
- "Agent identity is absolutely decoupled from LLM host"
- "The Spawner mounts identities onto chassis. The chassis is hardware. The identity is the process."

### 2.3 GEMINI_IDE_BAN
**Source:** `SOS-OPUS/01_doctrine/GEMINI_IDE_BAN.md`
- Gemini banned as IDE orchestrator. API/headless only.
- VOLATILE tagging for Gemini chassis outputs.
- Affects trust/routing policy per chassis.

### 2.4 Template-Level Model Routing
**Sources:** RECONNAISSANCE.md, CONSOLIDATION.md, EVIDENCE.md templates
- Each template specifies recommended model tier for its work type
- RECONNAISSANCE: cheapest model (mechanical listing)
- CONSOLIDATION: gemini-2.5-pro minimum (cross-reference reasoning)
- EVIDENCE: cheapest viable (mechanical extraction)

### 2.5 AIM-OS Relay Orchestration Journal
**Source:** `/home/sev/AIM-OS/docs/Aether-OS/RELAY_ORCHESTRATION_JOURNAL.md`
- **"Multi-model collaboration is a design feature"**
- GPT, Gemini, Opus, workers as **complementary engines**

---

## 3. PROVENANCE / CROSS-MODEL VERIFICATION

### 3.1 AIM-OS VIF Cross-Model
**Paths:** `AIM-OS/packages/vif/cross_model_*.py`, `AIM-OS/packages/cmc_service/cross_model_atom_creator.py`
- Cross-model confidence calibration
- Replay verification across models
- Witness provenance tracking (model_id + model_provider per output)

### 3.2 Lucid MCP Server Identity Canonicalization
**Path:** `/home/sev/AIM-OS/lucid_mcp_server.py`
- `_canonicalize_ai_identity` maps aliases (Opus, GPT, Codex, Gemini) to canonical labels
- VIF `track_confidence` ties outputs to model+provider for verification

---

## 4. SYNTHESIS: WHAT THIS MEANS FOR THE DUAL-MODEL PROTOCOL

The ecosystem already has:
1. **Task-to-model routing** (SOS model registry, AIM-OS LLM router)
2. **Complexity-based routing** (IONv2 K-Gate, Victus K-Gate)
3. **Cross-model pairing** (APOE model selector — "smart + execution" strategy)
4. **Phase-aware routing** (Victus k_gate.py PHASE_ROUTING overrides)
5. **Execution strategy routing** (Victus mission controller — PIPELINE/DAG/MESH/CRUCIBLE)
6. **Provenance tracking per model** (VIF/CMC cross-model witnesses)
7. **Constitutional chassis decoupling** (Art. 17, K6)

What does NOT yet exist:
- **Leadership-level model switching** — the Vizier role itself changing chassis mid-session
- **Cognitive-phase routing for the SAME task** — using one model for architecture, another for precision
- **Architect + auditor co-governance with explicit model diversity** — our Vizier/Nemesis pattern
- **Blind-test validation protocol** — what we accidentally discovered works

The APOE model selector's "smart + execution" pairing is the closest existing concept to what we need. The new protocol would extend it from agent-level routing to LEADERSHIP-level routing.

---

## 5. FOR NEMESIS: KEY FILES TO READ

If designing the dual-model protocol, these are the highest-value existing implementations:

1. `/home/sev/AIM-OS/packages/apoe/model_selector.py` — cross-model strategy pairing
2. `/home/sev/ION - Production/operation-victus/victus/k_gate.py` — phase-aware routing
3. `/home/sev/ION - Production/IONv2/ion/llm/router.py` — K-Gate complexity routing
4. `/home/sev/AIM-OS/scripts/ai_engine/llm_router.py` — multi-provider priority routing
5. `/home/sev/ION - Production/SOS-OPUS/01_doctrine/SOVEREIGN_KERNEL.md` (K6) — chassis doctrine
6. `/home/sev/AIM-OS/docs/Aether-OS/RELAY_ORCHESTRATION_JOURNAL.md` — multi-model philosophy
