---
type: spec
authority: A2_CONSTITUTIONAL
template: SPEC
created: 2026-04-03T00:10:00-04:00
status: DRAFT
task: T03
depends_on: [T01, T02]
goal: Define the ContextPackageSchema — the bounded cognitive bundle compiled by the daemon for one work unit
connections:
  - ION/06_intelligence/specs/T01_TransitionSchema.yaml
  - ION/06_intelligence/specs/T02_WorkUnitSchema.yaml
  - SOS-OPUS/01_doctrine/SOVEREIGN_KERNEL.md (K3 Context Compilation)
  - SOS-OPUS/01_doctrine/SOVEREIGN_CONSTITUTION.md (Art. 10-12)
  - SOS/04_packages/cognitive/src/context_compiler.py
  - ION/06_intelligence/specs/T04_ReasoningWindowSchema.spec.md
---

# ContextPackageSchema — Bounded Cognitive Bundle

## 1. PURPOSE

A ContextPackage is the ONLY thing an agent receives. It is a self-contained,
versioned, pre-compiled brief that contains everything the agent needs to execute
one transition. Agents do not read the filesystem directly — they consume their
ContextPackage and produce output.

Per the Sovereign Kernel K3:
> "An agent with ONLY its Context Package can execute perfectly."

Per Constitution Art. 11:
> "Agents are ephemeral consumers."

Per Constitution Art. 12, the package is compiled from 5 tiers, dropping from
bottom up when token budget is exceeded. Doctrine and target are NEVER dropped.

## 2. SCHEMA DEFINITION

```yaml
ContextPackageSchema:
  schema_version: "1.0"

  ContextPackage:
    # --- Identity ---
    context_package_id: string   # REQUIRED — unique ID (uuid4)
    context_version: string      # REQUIRED — content hash for stale detection
    compiled_at: string          # REQUIRED — ISO 8601 timestamp
    
    # --- Binding ---
    work_unit_id: string         # REQUIRED — the WorkUnit this package was compiled for
    protocol_id: string          # REQUIRED — from TransitionSchema
    transition_id: string        # REQUIRED — from TransitionSchema
    
    # --- Agent identity (injected into system prompt) ---
    agent_identity:
      personal_name: string      # REQUIRED
      role: string               # REQUIRED
      structural_identity: string # REQUIRED
      tier: integer              # REQUIRED
      domain: string             # REQUIRED
      specialty: string          # REQUIRED
    
    # --- Compilation tiers (per K3 and Art. 12, priority order) ---
    tiers:
      tier_1_doctrine:           # NEVER dropped
        constitution_excerpt: string  # REQUIRED — articles relevant to this agent's domain
        kernel_excerpt: string        # OPTIONAL — K-sections relevant to this transition
        template_spec: string         # REQUIRED — the bound template's full spec
        
      tier_2_target:             # NEVER dropped
        target_files: list[TargetFile]  # REQUIRED — 100% visibility source files
        
      tier_3_mission:            # Dropped third (under budget pressure)
        task_payload: string     # REQUIRED — the mission text from the task/work unit
        objective: string        # REQUIRED — one-sentence goal
        output_schema: string    # OPTIONAL — expected output format reference
        
      tier_4_semantic:           # Dropped second
        semantic_overlays: list[SemanticOverlay]  # OPTIONAL — .semantic.md True Name dictionaries
        prior_findings: list[PriorFinding]        # OPTIONAL — relevant evidence/research from 06_intelligence/
        open_questions: list[string]              # OPTIONAL — questions this work unit should address
        
      tier_5_dependencies:       # Dropped first (under budget pressure)
        dependency_interfaces: list[DependencyInterface]  # OPTIONAL — 0% implementation, signatures only
    
    # --- Budget ---
    token_budget: integer        # REQUIRED — max tokens for this package
    actual_tokens: integer       # REQUIRED — actual token count after compilation
    tiers_dropped: list[string]  # REQUIRED — which tiers (or tier items) were dropped due to budget
    
    # --- Constraints passed to agent ---
    allowed_writes: list[string] # REQUIRED — from WorkUnit
    allowed_next_actions: list[string]  # REQUIRED — from WorkUnit
    must_not: list[string]       # OPTIONAL — from WorkUnit
    
  # --- Supporting types ---
  
  TargetFile:
    path: string                 # REQUIRED — filesystem path
    content: string              # REQUIRED — full file content (100% visibility)
    line_count: integer          # REQUIRED
    language: string             # OPTIONAL — file type hint
    
  SemanticOverlay:
    path: string                 # REQUIRED — .semantic.md file path
    content: string              # REQUIRED — True Name boundary definitions
    
  PriorFinding:
    source: string               # REQUIRED — evidence/research file path
    summary: string              # REQUIRED — compressed finding
    confidence: float            # REQUIRED — [0.0, 1.0]
    
  DependencyInterface:
    path: string                 # REQUIRED — dependency file path
    signatures_only: string      # REQUIRED — public API surface only (0% implementation per Art. 10)
```

## 3. COMPILATION ALGORITHM

The daemon (or Vizier in IDE/manual mode) compiles a ContextPackage:

```
1. Load agent identity from registry
2. Select doctrine excerpts relevant to agent's domain and transition
3. Load target files at 100% visibility
4. Load mission payload from task/work unit
5. Load semantic overlays if they exist for target files
6. Load prior findings relevant to this scope
7. Load dependency interfaces at 0% implementation (signatures only)
8. Measure total tokens
9. If over budget:
   a. Drop tier_5 items one by one (largest first)
   b. If still over: drop tier_4 items one by one
   c. If still over: drop tier_3 items (except objective)
   d. NEVER drop tier_1 or tier_2
10. Hash the final package → context_version
11. Record what was dropped in tiers_dropped
```

## 4. ASYMMETRIC VISIBILITY (Art. 10)

This is the most important architectural constraint in the compilation:

| Layer | Visibility | Rationale |
|-------|-----------|-----------|
| Target files | 100% | Agent needs full implementation to do its work |
| Dependency files | 0% implementation (signatures only) | Prevents token dilution, forces bounded scope |
| Doctrine | Full text of relevant articles | Agent must know the law |
| Prior findings | Summary only | Agent gets conclusions, not raw evidence |

An agent that receives a ContextPackage with proper asymmetric visibility
cannot drift into cross-file synthesis it wasn't authorized for, because it
literally cannot see the implementation of files outside its scope.

## 5. IDE/MANUAL MODE ADAPTATION

In IDE/manual mode (current operating mode), the ContextPackage is not a
compiled artifact — it is the set of files the IDE agent reads on session start.

The MINI.md ROUTE section IS the tier_2/tier_5 reference list.
The task description IS tier_3_mission.
The doctrine files in the ROUTE IS tier_1_doctrine.
The boot document IS the agent_identity injection.

When the daemon is built, this implicit compilation becomes explicit and programmatic.
The governed reasoning chamber layered on top of this package is defined separately in `T04_ReasoningWindowSchema.spec.md`.

## 6. VALIDATION CRITERIA

- [ ] Tier priority order matches K3 and Art. 12 (doctrine never dropped)
- [ ] Asymmetric visibility is enforced (target=100%, deps=signatures only)
- [ ] context_version hash enables stale detection per T02
- [ ] Package is self-contained — agent needs nothing else
- [ ] Budget management algorithm is deterministic and reversible
- [ ] IDE/manual mode mapping is documented (MINI → tiers, boot doc → identity)
