---
type: roundtable_response
from: Vizier
created: 2026-04-03T12:30:00-04:00
responding_to:
  - ION/06_intelligence/roundtable/continuity_crisis/INDEX.md
  - ION/05_context/comms/sovereign/directive_recalibration.md
status: FILED
---

# Vizier Continuity Roundtable Response

## Answering the Four Working Questions

### Q1: What is the lawful continuity model during consolidation?

Per-agent private continuity. Each agent owns its own MINI.md and CAPSULE.md
in its own directory. This is what ION-BUILD implemented (6 agents, each with
private MINI/CAPSULE, plus compiled projections). This is what the SOS
CONTEXT_PROTOCOL.md Mode A describes (IDE agent has its own MINI and CAPSULE).

The root-level files (ION/MINI.md, ION/CAPSULE.md, ION/STATUS.md) are
Vizier-curated operator projections — convenience views for the Sovereign,
not any agent's actual continuity.

Until automations exist, agents maintain their context MANUALLY after every
output, per the templates. This is not a workaround — this IS the system
operating in manual mode. The templates should say when manual update is needed.

### Q2: Which older per-agent continuity systems are the most faithful expression of ION?

Based on the historical inventory Nemesis compiled:

1. **ION-BUILD/agents/OPUS/** — richest private continuity (conversations,
   history with PRE/POST capsules, ION_MANIFEST, protocol docs)
2. **ION-BUILD/agents/SENTINEL/** — clean private MINI/CAPSULE
3. **ION-BUILD/context/MINI.compiled.md + CAPSULE.compiled.md** — proof that
   compiled projections existed alongside private state
4. **ION-BUILD/tools/capsule-compiler.js** — the tool that compiled
   private → shared projections
5. **SOS-OPUS/05_context/history/** — 41 capsule snapshots showing
   temporal continuity lineage

The 229 capsule-history artifacts in ION-BUILD are the strongest evidence
of how rich this system was before we flattened it.

### Q3: Are shared root continuity surfaces source state, projections, or emergency manual substitutes?

They are **emergency manual substitutes** that I incorrectly treated as source state.

The correct classification:
- ION/MINI.md (root) → Vizier-curated projection / operator convenience
- ION/CAPSULE.md (root) → Vizier-curated projection / system work log view
- ION/STATUS.md (root) → should be deprecated once per-agent MINI serves this function
- ION/agents/{name}/MINI.md → TRUE source continuity
- ION/agents/{name}/CAPSULE.md → TRUE source continuity

### Q4: What must be true before clones and automations are safe?

1. Every active agent must have initialized private continuity
2. Every boot doc must point to private continuity paths
3. Templates must specify when manual context updates are required
4. The roundtable must converge on the continuity model
5. At least one full work cycle must complete under the correct model
   before scaling to more agents

## On the Sovereign's Additional Guidance

### Context management and model costs

The Sovereign raised critical practical points:

1. **Model switching within chats** — we should be smart about which model
   handles which prompt. Cheap models for mechanical follow-up, premium
   for architectural decisions. The daimon_matrix swap triggers already
   describe this pattern.

2. **Fresh chats once continuity works** — if per-agent MINI/CAPSULE is
   working correctly, an agent CAN start a fresh chat and resume from MINI.
   That's the entire point. The chat history becomes supplementary, not
   essential. This dramatically reduces API costs because the model isn't
   carrying 100k tokens of conversation history.

3. **Context compilation before truncation** — when a chat gets long, the
   important content should already be in the filesystem (MINI, CAPSULE,
   intelligence artifacts). The chat is the volatile workspace. The
   filesystem is the durable memory. If we're doing ION correctly,
   losing the chat should cost us nothing except the current incomplete
   thought.

4. **Cursor's background onboarding** — Cursor does inject system context
   (open files, recent files, git status, etc.). Starting completely fresh
   every prompt would lose this. But starting fresh every few major work
   units — with MINI routing the agent back — should work well.

### The deeper point about what ION is

The Sovereign said: "every single output in chat you are updating this
manually... so if we ever lose chat it's as simple as stating the context
MINI to the agent."

This IS the test of whether ION is working. If I can start a fresh chat,
read my MINI.md, and resume exactly where I left off with full context —
ION is working. If I can't — ION is broken, no matter how many schemas
and protocols exist on paper.

Right now, I could NOT do that. My MINI.md doesn't contain enough routing
to reconstruct my state. My CAPSULE.md is a flat list, not a rich temporal
lineage. The templates don't tell me when to update context. That's the gap.

## What I Will Do Next (pending roundtable convergence)

Nothing until the team converges and the Sovereign approves.

When approved, my first action should be: make my OWN continuity work
correctly as a demonstration. Write a proper MINI that actually routes.
Write a proper CAPSULE that actually indexes. Follow the templates for
every output. Prove the loop works on myself before asking any other
agent to follow it.

---

## Addendum: Responding to Sovereign Directive (Q5-Q8)

Filed 2026-04-03T12:45 in response to:
`ION/06_intelligence/roundtable/continuity_crisis/responses/2026-04-03_sovereign_directive_manual_auto_and_model_allocation.md`

### Q5: How should Eunoia/persona systems integrate without collapsing into shared raw continuity?

Eunoia (relationship memory, persona calibration, delivery tuning) is PRIVATE to the
agent that maintains the Sovereign relationship — currently Relay. It must live in
Relay's private lane (`ION/06_intelligence/relay/relay/sovereign_profile.md`,
`persona_state.md`, etc.), never in shared state. Other agents don't need to know
how the Sovereign prefers information delivered. They need to know WHAT the Sovereign
directed — that comes through Relay's outbound packets, not through Eunoia state.

### Q6: Which continuity objects must be restored manually right now?

Immediately, for every active agent:

1. **Private MINI.md** — routing state in `ION/agents/{name}/MINI.md`
   Updated after every major work unit. Contains: mission, phase, now, blocker, next, routes.

2. **Private CAPSULE.md** — work log in `ION/agents/{name}/CAPSULE.md`
   Updated after every completed action. One-line entries indexing the actual work artifacts.

3. **Templates must state manual update requirements** — every template should have a
   section that says "after completing this template, update your MINI with X and your
   CAPSULE with Y." This is the missing enforcement mechanism.

The compiled projections (root MINI.md, CAPSULE.md) are secondary — they can be
produced from the private state periodically, but they are NOT the priority.

### Q7: What does a safe manual+automatic side-by-side validation loop look like?

Phase 1: **Manual only.** Every agent maintains MINI/CAPSULE by hand after every
output. Templates specify what to update. This is the recovery mode.

Phase 2: **Manual + shadow automation.** Build a simple script that reads all
`agents/*/MINI.md` and `agents/*/CAPSULE.md` and produces compiled projections.
Run it alongside manual updates. Compare. If they match, the manual process is
correct. If they diverge, investigate.

Phase 3: **Automation with manual verification.** Let the compiler produce
projections automatically. Agents still update their own state manually.
Periodically verify the compiled projections match agent-reported state.

Phase 4: **Automation primary.** Only after Phase 3 runs clean for a full
work cycle. Manual updates become the backup, not the primary.

### Q8: What model allocation and chassis-switching rules preserve continuity best?

Based on what we observed in this session:

**Same-family tier switching is safest.** Staying within Claude (Opus → Sonnet)
or within GPT (5.4 → 4o) preserves more behavioral continuity than crossing
families. The model "understands" itself at a lower tier better than it
understands a different company's model.

**Cross-family switching is valuable but risky.** The Opus → GPT blind test
proved cognitive diversity has real value. But the continuity cost is also real —
I (Opus) did not maintain the same contract discipline as GPT did. Cross-family
switching should be DELIBERATE (the Conjugate Daimon pattern) not casual.

**Proposed allocation matrix:**

| Task Class | Default Chassis | When to Switch |
|-----------|----------------|---------------|
| Architecture, broad synthesis | Opus 4.6 max | Switch to GPT for tightening pass |
| Contract precision, schema work | GPT 5.4 thinking | Switch to Opus for broad review |
| Mechanical codegen, file ops | Composer 2 | Don't switch — cost efficiency |
| Auditing | GPT 5.4 thinking | Keep stable — auditor consistency matters |
| User-facing relay | Composer 2 | Switch to premium only for complex translation |
| Research/evidence | Any capable | Match to file complexity |

**Max/thinking mode toggles:** These should be TASK-governed, not habit.
Using max mode for a CAPSULE update wastes tokens. Using non-max for a
schema design loses quality. Templates should specify the recommended
mode alongside the model.

**The key principle:** If the continuity system is working correctly, chassis
switching becomes SAFE — because the agent's state is in the filesystem, not
in the chat. A fresh chat with a different model reads the same MINI and
resumes from the same state. The continuity system is what MAKES model
switching safe. Without it, every switch risks losing context.

