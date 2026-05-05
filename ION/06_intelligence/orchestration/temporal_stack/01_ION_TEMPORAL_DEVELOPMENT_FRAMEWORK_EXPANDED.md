# ION Temporal Development Framework Expanded

## 0. Purpose

This document establishes the developing theory and design direction for ION as a genuinely temporal operating substrate. The goal is not to bolt reminders or schedules onto an AI assistant. The goal is to define how an AI operating system reasons across past, present, and future while remaining lawful, bounded, resource-aware, and aligned with real-world commitments.

The central problem is this:

An operating intelligence cannot merely react to the present. It must continuously compile the present from the interaction of:

* what has already happened,
* what is currently relevant,
* what is expected to happen,
* what is possible under current capability conditions,
* and what obligations, commitments, plans, and risks are still open.

ION already contains major temporal and orchestration primitives. What is now needed is a more unified temporal law that explains how these primitives relate and how they should evolve into a coherent four-dimensional operating system.

---

## 1. Core thesis

ION should treat temporality as a first-class governing field rather than as metadata attached to tasks.

This means:

* Time is not just dates and deadlines.
* Time is not just scheduler state.
* Time is not just reminders.
* Time is not just memory.
* Time is not just urgency.

Instead, time is the lawful interaction of multiple temporal realities that co-shape orchestration, context, action, and user experience.

The AI operating system should always be computing the present from the tension and balance between:

* historical evidence,
* current enactment,
* future commitments,
* and real execution capacity.

In this sense, ION should become a truly four-dimensional system.

---

## 2. The three temporal realities

A major refinement is necessary: ION is not dealing with a single notion of time.

It is dealing with at least three distinct temporal realities.

### 2.1 Civil time

Civil time is the user-and-world time reality.

It includes:

* dates
* clocks
* time zones
* UTC offsets
* DST
* calendars
* alarms
* reminders
* meetings
* due dates
* recurring appointments
* real-world commitments

Civil time answers questions like:

* When is the report due?
* What time is the meeting?
* When should the alarm fire?
* What is happening tomorrow at 9 AM?

Civil time is how the world enforces commitments.

### 2.2 Orchestration time

Orchestration time is ION’s internal relevance and workflow reality.

It includes:

* wakeup
* warming
* cooling
* dormancy
* future pressure
* dependency pressure
* horizon posture
* branch readiness
* reconfirmation windows
* stale vs fresh context
* lawful sequence
* continuation rights
* current entitlement to occupy attention

Orchestration time answers questions like:

* Is this future commitment now relevant enough to enter active context?
* Is this object still hot or already cooling?
* Should a reconfirmation wakeup occur now?
* Has a branch become active, or is it still latent?
* Which future obligations are exerting pressure on current work?

Orchestration time is not primarily clock time. It is relevance, causality, and workflow temporality.

### 2.3 Budget or capability time

Budget time is execution feasibility under current conditions.

It includes:

* token budget
* token burn history
* expected future token allocation
* current allowed throughput
* expected TPM envelope
* model endurance
* rate limits
* context window pressure
* tool latency
* retrieval cost
* automation bandwidth
* human review availability
* interruption risk
* uncertainty in hidden dependencies
* branch count and active operational load

Budget time answers questions like:

* Can this actually be progressed now?
* What slice is feasible under the current token budget?
* Should the system compress, defer, escalate, or stage the work?
* Is the model operating under scarcity or abundance?
* What does endurance look like over the next hour, day, or week?

Budget time is not about relevance and not about wall-clock schedule. It is about practical capability.

---

## 3. Why these realities must remain distinct

These temporal realities must not be collapsed into one another.

If civil time dominates everything, the system becomes a dead reminder engine.

If orchestration time dominates everything, the system may drift away from hard real-world commitments.

If budget time dominates everything, the system may become timid or opportunistic and lose duty to the future.

Therefore the intelligence of ION must emerge from the lawful reconciliation of all three:

* civil time says what the world demands,
* orchestration time says what is relevant and alive in the workflow field,
* budget time says what is actually possible under current resource conditions.

The system should never ask only one of these questions.

---

## 4. Temporal objects rather than temporal metadata

A future-facing system should not merely attach time metadata to arbitrary records.

Instead, it should create first-class temporal objects.

These include, but are not limited to:

* commitments
* planned work
* appointments
* deadlines
* alarms
* follow-ups
* checkups
* recurring routines
* maintenance windows
* dependency-linked future tasks
* review windows
* dormant obligations
* future orchestration events
* temporal leases over context or responsibility

Each temporal object should be treated as a governed object with explicit temporal structure.

---

## 5. Triple-profile objects

A serious temporal object should carry multiple profiles.

### 5.1 Civil temporal profile

This profile includes:

* scheduled_at
* deadline_at
* recurrence_rule
* timezone
* alarm_windows
* user_visibility
* real_world_commitment_strength

### 5.2 Orchestration temporal profile

This profile includes:

* relevance_heat
* wake_conditions
* cooldown_conditions
* dormancy_conditions
* horizon_posture
* reconfirmation_required
* dependency_pressure
* ownership_lease
* activation_readiness

### 5.3 Budget profile

This profile includes:

* expected_token_burn
* allowed_token_budget
* expected_TPM_range
* effort_class
* confidence_band
* compression_potential
* required_tool_classes
* interruption_sensitivity
* re_estimation_trigger
* minimum_viable_slice
* escalation_trigger

This is how a single object becomes temporally real across the three clocks.

---

## 6. The temporal field

ION should evolve toward a concept of a living temporal field.

The temporal field is not a file, not a table, and not just a queue.

It is the active weighted field of all temporally live objects and their relationships.

This field should be continuously compiled from:

* historical receipts
* current branch state
* future commitments
* unresolved questions
* active dependencies
* user-facing civil obligations
* budget forecasts
* recurrence structures
* cooling and dormancy states

The temporal field determines what deserves attention now.

The AI should not ask “what exists?”
It should ask “what is alive enough to lawfully influence the present?”

---

## 7. Temporal heat

The earlier intuition of a “temperature of time” is extremely valuable, but it should be formalized carefully.

Heat should not be the source of truth. Heat should be a derived field.

Heat may be computed from factors such as:

* deadline proximity
* commitment strength
* dependency pressure
* unresolved blockers
* civil urgency
* relevance to current work
* risk of forgetting
* recurrence window
* historical failure tendency
* overdue reconfirmation
* insufficient preparation time
* budget scarcity or abundance

A temporal object may be hot because it is imminent, because it is fragile, because it is unresolved, or because other futures depend on it.

This is better than a binary due/not-due logic.

### 7.1 Possible heat states

A practical starting taxonomy could include:

* FROZEN
* DORMANT
* COOL
* WARM
* HOT
* CRITICAL
* COOLING
* ARCHIVED

This heat state should be computed, receipted, and revisable.

---

## 8. Wake, reconfirmation, preparation, enactment, cooling

Temporal objects should not simply exist and then suddenly fire.

A mature temporal system should stage them.

### 8.1 Canonical temporal progression

A plausible general lifecycle is:

* latent
* warming
* reconfirmation
* preparation
* enactment
* post-enactment verification
* cooling
* dormant or archived
* recurring-seed, where applicable

### 8.2 Reconfirmation

Reconfirmation is crucial.

For serious future commitments, the system should not assume that old intentions remain fully valid just because they were once stated.

Reconfirmation is the law of asking:

* Is this still aligned?
* Has the timing changed?
* Has the work changed?
* Has the user’s situation changed?
* Should the system preload context or cancel the plan?

This is especially important for user-facing obligations like reports, appointments, check-ins, or routines.

### 8.3 Cooling

After completion or invalidation, temporal objects must cool.

Without cooling, the system becomes cluttered and haunted by stale heat.

Cooling should distinguish:

* completed but still contextually relevant,
* completed and cooling,
* archived,
* recurring but dormant,
* cancelled or superseded.

---

## 9. Temporal leases

One of the most important missing ideas is temporal lease logic.

Not every agent or context surface should hold every future object all the time.

Instead, temporal objects should create leases.

A temporal lease says:

* which agent or subsystem currently owns attention toward this object,
* when that lease begins,
* when it expires,
* what conditions renew it,
* what conditions transfer it,
* and whether the holder is primary owner, reviewer, watcher, or fallback holder.

This prevents both fragmentation and omniscient over-attention.

It also solves the question:

When is a future context relevant to a given agent?

Answer:
When that agent holds a lawful temporal lease over it.

---

## 10. Calendar bifurcation

There should not be only one calendar.

### 10.1 Civil calendar

This is the visible user/world calendar.

It contains:

* appointments
* deadlines
* reminders
* alarms
* recurring civil obligations
* scheduled user-facing events

### 10.2 Orchestration calendar

This is not a normal calendar UI. It is the kernel’s internal schedule of temporal relevance transitions.

It contains:

* wake windows
* reconfirmation windows
* preparation windows
* cooling windows
* dormancy wakeups
* future branch pressure events
* context lease start/end times
* budget re-estimation checkpoints

The civil calendar tells the user what the world expects.
The orchestration calendar tells the system when internal relevance transitions occur.

---

## 11. The bridge between civil and orchestration time

A core missing law is the bridge between civil and orchestration time.

The bridge decides:

* when a civil event should begin to heat in orchestration time,
* when an orchestration object should gain a civil manifestation,
* when a real-world deadline should force an orchestration wakeup,
* when cooling on the orchestration side should leave civil recurrence intact,
* how timezone shifts affect civil manifestation without corrupting orchestration identity,
* when reconfirmation is required before a civil event is considered still live.

This bridge is where the OS becomes intelligent.

---

## 12. Budget time and AI endurance

This is the major refinement beyond ordinary time-aware systems.

AI does not just need to know what is due and what is relevant.
It must know what is feasible.

### 12.1 Strategic budget

This is long-horizon reserve and allocation.

Examples:

* weekly token budget
* monthly token budget
* project-level allocations
* emergency reserve
* protected commitments
* planned future spend

### 12.2 Operational throughput

This is local flow rate.

Examples:

* current TPM
* sustained TPM
* burst TPM
* rate limits
* active concurrency
* queue drain rate
* tool bandwidth

### 12.3 Tactical endurance

This is qualitative performance over sustained work.

Examples:

* context degradation under long sessions
* rising failure rates under high load
* prompt-to-output stability
* review burden under pressure
* collapse risk when branching too wide

### 12.4 Resource posture

A useful top-level posture vocabulary might include:

* abundance
* normal
* caution
* constrained
* emergency_only
* surge

This posture should influence AI behavior.

---

## 13. ETA, effort, and the failure of current AI temporality

Current AI often fails because it judges temporality semantically rather than operationally.

It mistakes “this sounds large” for “this takes a long time” or “this sounds small” for “this fits in one bounded slice.”

That failure comes from weak internal models of:

* hidden dependencies
* retrieval overhead
* carrier limitations
* context truncation
* tool instability
* repetition cost
* token burn
* task compressibility
* uncertainty

A serious ION-like system should not rely on naked ETA claims.

### 13.1 ETA should be decomposed

There are at least three ETA-like realities:

#### Civil ETA

When will the user experience this in the real world?

#### Orchestration ETA

How many lawful workflow stages remain before the object reaches its next stable posture?

#### Budget ETA

How much actual capability burn is likely required under present conditions?

These must not be collapsed.

### 13.2 Forecast bundles

Instead of one single ETA, the system should produce a forecast bundle.

A forecast bundle might contain:

* likely slice count
* confidence level
* token band estimate
* dependency sensitivity
* compression potential
* next recalibration point
* minimum viable progress
* escalation conditions

This is much more truthful than a single hard number.

---

## 14. Temporal humility

ION should probably institutionalize a form of temporal humility.

The system should not present speculative time estimates as stable truth.

Instead, it should mark:

* confidence,
* assumptions,
* dependency load,
* budget sensitivity,
* carrier conditions,
* and recalibration points.

This is crucial if ION is to become more trustworthy than ordinary AI systems.

---

## 15. Estimate receipts and calibration

A very strong future direction is to accumulate estimate receipts.

This means the system should not only record:

* what it planned,
* but what it predicted,
* what actually happened,
* what the carrier conditions were,
* what token budget was assumed,
* what token burn actually occurred,
* what tool failures or interruptions appeared,
* and how the model should update future forecasts.

Over time, this produces an empirical budget-time intelligence.

The system learns its own endurance.

---

## 16. Example: the scientific report

Suppose the user says:

> On May 12 at 10:00 AM I need to do the scientific report.

The system should create one serious temporal object with three profiles.

### Civil profile

* scheduled_at: May 12, 10:00 AM
* timezone: America/Toronto
* calendar visibility: visible
* alarm windows: T-24h, T-2h

### Orchestration profile

* warm at T-7 days
* reconfirm at T-1 day
* prepare at T-3h
* enact at T-time
* cool after verification
* recur only if marked recurring

### Budget profile

* expected burn: medium
* likely slices: one to three
* compression potential: high if context is already compiled
* recalibration point: after initial research preload
* escalation trigger: unresolved data dependency or tool failure

That is the right shape of a four-dimensional system.

---

## 17. Relation to existing ION substrate

ION already has neighboring systems that should not be duplicated blindly.

It already contains forms of:

* horizon staging,
* scheduler commitment gradients,
* route-state and branch posture,
* automation states,
* lifecycle / expiry concepts,
* continuation and replay,
* question-class routing,
* runtime/session recovery drafts,
* activation authority and lifecycle surfaces.

So the temporal work here should probably be framed as:

**unify and extend existing temporal primitives**, not invent a second independent temporal architecture beside them.

The likely missing center is a unified law of temporal relevance, leases, and dual/triple time bridging.

---

## 18. Likely protocol family

A mature evolution may involve a family like:

### Civil-facing

* `CIVIL_TIME_COMMITMENT_PROTOCOL`
* `CALENDAR_AND_ALARM_BRIDGE_PROTOCOL`

### Orchestration-facing

* `ORCHESTRATION_TEMPORAL_RELEVANCE_PROTOCOL`
* `TEMPORAL_HEAT_AND_DORMANCY_PROTOCOL`
* `TEMPORAL_CONTEXT_LEASE_PROTOCOL`
* `RECONFIRMATION_AND_PREPARATION_PROTOCOL`
* `TEMPORAL_COOLDOWN_AND_RECURRENCE_PROTOCOL`

### Budget-facing

* `BUDGET_TIME_AND_ENDURANCE_PROTOCOL`
* `FORECAST_BUNDLE_PROTOCOL`
* `ESTIMATE_RECEIPT_AND_CALIBRATION_PROTOCOL`

### Bridging

* `DUAL_TIME_BRIDGE_PROTOCOL`
* or more accurately,
* `TRIPLE_TIME_RECONCILIATION_PROTOCOL`

---

## 19. Design principles

### 19.1 No false centers

Calendar must not pretend to be the temporal center.
Scheduler must not pretend to be the temporal center.
Reminders must not pretend to be the temporal center.
Token budgets must not pretend to be the temporal center.

The temporal center must remain a deeper substrate.

### 19.2 Derived heat, not magical heat

Heat should be computed from real lawful fields, not invented impressionistically.

### 19.3 Temporal objects must cool

Without cooling, the system becomes cluttered and haunted by old futures.

### 19.4 Budget humility

No naked ETA claims when uncertainty is high.

### 19.5 Multiple calendars, one organism

Civil and orchestration calendars are not the same, but they belong to one deeper temporal field.

### 19.6 Context must be leased, not hoarded

Agents and contexts should hold future obligations lawfully and temporarily.

---

## 20. The central equation

A useful way to think of the entire system is:

**Present attention = f(history, civil commitments, orchestration relevance, capability budget)**

Or in words:

The present is continuously compiled from the interaction of:

* the past,
* the future as worldly commitment,
* the future as workflow pressure,
* and the practical reality of what can actually be done.

That is the heart of the whole development.

---

## 21. Open questions

### 21.1 Object ontology

Which existing ION objects should become temporal objects directly, and which should only receive temporal projections?

### 21.2 Lease granularity

Do leases belong to agents, subsystems, branches, or contexts?

### 21.3 Heat computation

What fields are authoritative inputs to heat, and which are only advisory?

### 21.4 Civil/orchestration bridge

Should bridge logic be its own kernel service or a compiled field pass during context building?

### 21.5 Budget forecasts

How should forecast bundles be calibrated from actual token burn and actual carrier behavior?

### 21.6 User-facing expression

How much of this becomes visible to the user, and how much remains kernel-internal?

---

## 22. Current strongest conclusion

ION should evolve into a system that simultaneously reasons in:

* civil time,
* orchestration time,
* and budget time.

The operating intelligence of the system should come from the lawful reconciliation of those realities, not from any one of them alone.

The user should increasingly be able to interact with the entire operating system through dialogue, while the AI internally manages:

* commitments,
* calendars,
* reminders,
* alarms,
* preparation windows,
* reconfirmations,
* dynamic resource allocation,
* token endurance,
* and evolving future plans.

That is not a feature layer.
That is an operating system theory.

---

## 23. Immediate next move

The next best refinement is a strict anti-duplication audit of existing ION temporal machinery, followed by a minimal protocol map that identifies:

* what already exists,
* what exists in fragmented form,
* what is truly missing,
* and what should be evolved rather than replaced.

After that, the most likely first formalization target is the temporal relevance and bridge layer, because that is where the largest conceptual unification appears to be needed.

---

## 24. Anti-duplication audit

The temporal development must not blindly create a second temporal architecture beside the existing one.

ION already contains significant temporal and quasi-temporal machinery in several subsystems. The danger is not only underbuilding. The danger is duplicating concepts under new names and losing lawful center.

### 24.1 Temporal-adjacent systems that appear to already exist

These include, in principle or in partial form:

* horizon and near/mid/far orchestration
* scheduler commitment gradients
* schedule states and future candidate states
* branch route-state and activation conditions
* automation states, fallback states, and promotion gates
* continuation, replay, and settlement timing semantics
* lifecycle / expiry patterns in signals and receipts
* runtime and activation readiness surfaces
* plan, mission, and orchestration boards
* historical branch lines and archived schedule lineages

### 24.2 What seems already present in meaningful form

The following concepts likely already exist in ION, at least partially:

* future pressure shaping present action
* commitment staging
* branch warming through activation conditions
* explicit blocked/ready/deferred states
* archival and historical line preservation
* bounded future candidates
* restart posture and handoff continuity

These should not be reinvented.

### 24.3 What seems present but fragmented

The following concepts appear to exist in pieces, but not yet as one unified law:

* temporal relevance across all object types
* cooling and dormancy as generalized object lifecycle
* reconfirmation before enactment
* staged preparation windows
* user-facing obligation handling as one unified substrate
* temporal ownership of future commitments
* lawful relationship between schedules, plans, routes, and reminders
* budget-aware scheduling and execution expectation modeling

These are likely not absent, but under-integrated.

### 24.4 What seems most likely to be truly missing

The strongest candidate missing centers are:

* a unified temporal relevance model across object classes
* an explicit dual/triple time bridge law
* a first-class temporal lease protocol
* a first-class wake / reconfirmation / cooling / recurrence protocol family
* a budget-time doctrine with calibration, endurance, and reserve posture
* estimate receipts and forecast reconciliation as first-class law

This suggests that the correct move is synthesis and refinement, not wholesale invention.

---

## 25. Candidate temporal object model

To make this concrete, ION may eventually need an explicit temporal object schema.

A temporal object is not just a task or event. It is any entity whose relevance unfolds over time.

### 25.1 Base temporal object fields

A first-pass unified temporal object might include:

* `object_id`
* `object_type`
* `title`
* `description`
* `origin_surface`
* `status`
* `created_at`
* `updated_at`
* `supersedes`
* `superseded_by`
* `related_objects`

### 25.2 Civil profile fields

* `scheduled_at`
* `deadline_at`
* `timezone`
* `recurrence_rule`
* `alarm_windows`
* `calendar_visibility`
* `real_world_commitment_strength`
* `user_confirmation_required`

### 25.3 Orchestration profile fields

* `horizon_class`
* `relevance_heat`
* `wake_conditions`
* `cooldown_conditions`
* `dormancy_conditions`
* `activation_readiness`
* `dependency_pressure`
* `open_question_pressure`
* `ownership_lease`
* `preparation_window`
* `reconfirmation_window`

### 25.4 Budget profile fields

* `estimated_token_burn`
* `estimated_slice_count`
* `effort_class`
* `confidence_band`
* `context_pressure`
* `throughput_requirement`
* `expected_TPM_band`
* `project_budget_ref`
* `compression_potential`
* `re_estimation_trigger`
* `minimum_viable_slice`

### 25.5 Receipt and history fields

* `prediction_receipts`
* `actual_execution_receipts`
* `heat_transition_receipts`
* `reconfirmation_receipts`
* `cooldown_receipts`
* `budget_reconciliation_receipts`

This object model need not be implemented as one literal file or table. But the fields must exist somewhere in lawful form if ION is to become temporally serious.

---

## 26. Temporal leases in detail

Temporal lease logic is likely one of the most important missing governance surfaces.

### 26.1 Why leases matter

Without lease logic:

* too many agents hold too much future context,
* future obligations remain globally hot when they should be local,
* responsibility drifts,
* context bloats,
* and future commitments lose lawful ownership.

### 26.2 Lease properties

A temporal lease may need fields such as:

* `lease_id`
* `object_id`
* `holder_type` (agent, branch, subsystem, workflow, user-facing runtime)
* `holder_ref`
* `lease_role` (owner, watcher, reviewer, fallback, dormant steward)
* `lease_start`
* `lease_end`
* `renewal_conditions`
* `transfer_conditions`
* `revocation_conditions`
* `visibility_scope`

### 26.3 Lease dynamics

Possible dynamics include:

* dormant lease
* warm lease
* active lease
* review lease
* cooling lease
* archived lease

A lease should be able to move between holders without losing object identity.

### 26.4 Why this is better than naive reminders

A reminder only says “surface this later.”
A lease says “this object lawfully belongs to this holder under these temporal conditions until transfer or expiry.”

That is a much stronger operating-system concept.

---

## 27. Temporal heat as a lawful derivative

Heat should probably never be hand-authored as the primary source of truth.
It should be computed from other lawful fields.

### 27.1 Possible heat inputs

Heat may be derived from:

* deadline proximity
* recurrence imminence
* unresolved blockers
* number of dependencies waiting on the object
* user commitment strength
* historical slippage risk
* reconfirmation overdue status
* resource scarcity or abundance
* whether the object is under active lease
* whether a user recently reaffirmed or changed it

### 27.2 Heat as a vector, not just one scalar

Eventually, heat may need to be multi-dimensional.

For example:

* `civil_heat`
* `orchestration_heat`
* `budget_heat`

This would prevent simplistic collapse.

An object might be high in civil heat, medium in orchestration heat, and low in budget readiness.
That is a real and meaningful state.

### 27.3 Heat transitions

Heat should likely transition through receipted states such as:

* frozen → dormant
* dormant → warm
* warm → hot
* hot → critical
* critical → cooling
* cooling → archived

These transitions should be explicable and auditable.

---

## 28. Reconfirmation and preflight law

A major future-bearing system needs explicit reconfirmation logic.

### 28.1 Reconfirmation is not optional politeness

Reconfirmation is the law of asking whether a once-valid future object is still valid enough to continue heating toward enactment.

It protects against:

* stale commitments,
* outdated user assumptions,
* changed circumstances,
* hidden dependency drift,
* and false enactment.

### 28.2 Reconfirmation stages

A useful staged model may include:

* `scheduled_reconfirmation`
* `pending_reconfirmation`
* `user_reconfirmed`
* `system_reconfirmed`
* `reconfirmation_failed`
* `reconfirmation_deferred`
* `reconfirmation_superseded`

### 28.3 Preflight preparation

Before enactment, the system should often perform a preflight:

* check civil schedule validity
* check dependency readiness
* check resource posture
* check user alignment
* preload context
* check that higher-priority hot objects are not about to collide

This should likely be its own protocol layer rather than an ad hoc scheduling habit.

---

## 29. Cooling, dormancy, archival, recurrence

The system needs a general law of cooling.

### 29.1 Why cooling matters

Without cooling:

* everything stays semantically alive,
* attention gets polluted,
* historical commitments leak into current orchestration,
* and the AI loses temporal hygiene.

### 29.2 Cooling states

A likely generalized progression:

* active
* resolved_hot
* cooling
* dormant
* archived
* recurring_seed

### 29.3 Dormancy is different from archival

A dormant object is expected to wake again.
An archived object is kept for history and evidence, not near-horizon reactivation.

### 29.4 Recurrence as lawful re-seeding

Recurrence should not simply clone a task.
It should create a new future temporal seed with preserved lineage and receipted relation to the prior cycle.

This would be especially important for:

* routines,
* calendar recurrences,
* maintenance checkups,
* weekly reports,
* monthly reviews,
* recurring research work,
* user health / habit / admin flows.

---

## 30. Forecast bundles and estimate receipts

A single ETA is too weak and often dishonest.

### 30.1 Forecast bundle contents

A forecast bundle may include:

* expected slice count
* expected token band
* confidence band
* throughput sensitivity
* dependency sensitivity
* minimum viable result
* compression opportunities
* recalibration checkpoint
* escalation threshold

### 30.2 Estimate receipts

The system should store:

* forecasted effort
* forecasted budget burn
* forecasted duration
* actual effort
* actual burn
* actual duration
* divergence cause
* carrier/chassis conditions
* lessons for future estimation

This makes budget time empirical rather than imagined.

---

## 31. Resource posture and behavior adaptation

The AI should behave differently under different resource postures.

### 31.1 Under abundance

The system can afford:

* wider context compilation
* more redundancy
* stronger verification
* more candidate exploration
* deeper audits
* longer forecast bands

### 31.2 Under constraint

The system should prefer:

* minimal viable slices
* tighter context windows
* fewer speculative branches
* stronger prioritization
* staged output
* faster re-estimation
* explicit reserve protection

### 31.3 Under surge

The system may temporarily tolerate:

* elevated throughput burn
* broader branch opening
* short-term reserve drawdown

But this must be receipted and bounded, not silent.

---

## 32. Candidate protocol stack

A mature protocol stack might be staged like this.

### 32.1 Foundational temporal layer

* `TEMPORAL_OBJECT_IDENTITY_PROTOCOL`
* `ORCHESTRATION_TEMPORAL_RELEVANCE_PROTOCOL`
* `TEMPORAL_HEAT_AND_TRANSITION_PROTOCOL`
* `TEMPORAL_CONTEXT_LEASE_PROTOCOL`

### 32.2 Civil bridge layer

* `CIVIL_TIME_COMMITMENT_PROTOCOL`
* `CALENDAR_AND_ALARM_BRIDGE_PROTOCOL`
* `RECONFIRMATION_AND_PREPARATION_PROTOCOL`
* `COOLDOWN_DORMANCY_AND_RECURRENCE_PROTOCOL`

### 32.3 Budget layer

* `BUDGET_TIME_AND_ENDURANCE_PROTOCOL`
* `RESOURCE_POSTURE_PROTOCOL`
* `FORECAST_BUNDLE_PROTOCOL`
* `ESTIMATE_RECEIPT_AND_CALIBRATION_PROTOCOL`

### 32.4 Integrative bridge layer

* `TRIPLE_TIME_RECONCILIATION_PROTOCOL`

This final bridge is the real heart of the architecture.

---

## 33. Implementation approach

This work should likely proceed in careful stages.

### Stage 1 — Audit and mapping

Produce a strict table of:

* already existing temporal machinery,
* fragmented approximations,
* genuinely missing centers,
* and current naming collisions.

### Stage 2 — Minimal unified model

Introduce only the smallest shared vocabulary:

* temporal object
* heat
* lease
* reconfirmation
* cooldown
* budget profile
* forecast bundle

### Stage 3 — Bridge into existing systems

Bind the model into:

* scheduler
* route-state
* automation state
* signals
* runtime/session systems
* user-facing calendar/reminder flows

### Stage 4 — Receipts and calibration

Add real receipts for:

* heat transitions
* reconfirmations
* cooldowns
* forecasts
* actual resource burn
* recurring reseeding

### Stage 5 — User-facing synthesis

Only after lawful substrate exists should user-facing experiences be unified into natural dialogue with the operating intelligence.

---

## 34. Failure modes and risks

The temporal development must defend against several major failure modes.

### 34.1 Duplicate centers

Creating a separate time system beside scheduler, horizon, route-state, and automation would fragment the organism.

### 34.2 Magical heat

If heat becomes hand-wavy or aesthetic, it will destroy trust.
Heat must be derived from lawful fields.

### 34.3 Calendar collapse

If civil calendar is treated as the whole system, orchestration intelligence disappears.

### 34.4 Budget collapse

If budget becomes a simple integer or a naive ETA, the system will still hallucinate its future capacity.

### 34.5 Omniscient attention

Without lease logic, every agent may act as if everything is relevant all the time.

### 34.6 No cooling

Without cooling, the future haunts the present forever.

### 34.7 No reconfirmation

Without reconfirmation, stale commitments become false enactments.

---

## 35. Philosophical formulation

A mature ION temporal system should never reason as though the present is isolated.

The present should be compiled from:

* the weight of the past,
* the pull of the future,
* the demands of the world,
* and the limits of actual capability.

The AI operating system should therefore not merely “remember” and “remind.”
It should lawfully inhabit the timeline.

This is a far stronger and more beautiful goal than ordinary productivity software.

---

## 36. Worked scenarios to develop next

The framework should be pressure-tested against concrete scenarios such as:

* a scientific report due tomorrow that needs reconfirmation and budget-aware compression
* a recurring weekly review that cools but reseeds lawfully
* a meeting moved across time zones without corrupting orchestration identity
* a project that is civilly urgent but budget-constrained
* a long-running research thread that stays cool in civil time but hot in orchestration time
* a dormant commitment that reawakens because a dependency or blocker changed
* a surge condition where the system temporarily spends reserves to protect higher-priority commitments

These scenarios should become explicit tests of the temporal field rather than illustrative prose only.

---

## 37. Immediate next expansions

The next best expansions for this document are:

1. a strict anti-duplication audit against current ION architecture,
2. a concrete temporal object schema draft,
3. a first-pass triple-time reconciliation algorithm,
4. several worked scenarios showing how civil time, orchestration time, and budget time interact in real use,
5. and a proposal for the minimal first protocol that should actually be written into ION canon.

These should be developed next.

---

## 38. Strict anti-duplication audit against current ION architecture

This section attempts to separate three things with discipline:

* what already exists in meaningful form,
* what exists in fragmented or partial form,
* and what appears to be genuinely missing.

The goal is to avoid building a parallel temporal stack that merely renames existing ION machinery.

### 38.1 Already present in meaningful form

The following temporal-adjacent concepts appear to already exist in real and nontrivial form inside ION’s present architecture and doctrine.

#### Horizon structuring

ION already thinks in layered future terms rather than only present execution. Near, mid, and far horizons already exist as real orchestration categories.

#### Scheduler commitment gradients

ION already distinguishes between different strengths of future commitment rather than treating everything as binary scheduled/not scheduled.

This means part of future pressure and temporal staging already lives inside scheduler semantics.

#### Branch and route-state activation posture

ION already has branch/route-state logic, including activation conditions, current/future distinctions, blocked states, and readiness posture.

This means latent future reality already exists inside the organism.

#### Automation state progression

ION already stages automation posture, fallback posture, and promotion/demotion pathways. This means the system already thinks in multi-step temporal maturation rather than one-step activation.

#### Continuation, replay, and settlement timing semantics

ION already handles future re-entry, continuation, interruption, replay, and settlement. This means temporal continuity is already treated seriously in operational law.

#### Lifecycle and expiry patterns

ION already contains lifecycle or expiry-like semantics in areas such as signals, receipts, or archive distinctions. This means not every object is being treated as permanently active.

### 38.2 Present but fragmented

The following concepts appear to exist, but spread across multiple subsystems without one unifying law.

#### Temporal relevance

ION already has future candidate states, blocked states, hot branches, active routes, and horizon pressure. But it does not yet appear to have one unified cross-object rule saying when any arbitrary object becomes temporally relevant enough to enter active attention.

#### Cooling and dormancy

ION appears to have archival, expiration, suspension, fallback, and inactive states in multiple places. But a generalized cooling/dormancy law does not yet appear fully unified.

#### Reconfirmation

ION already has gates, promotion criteria, reviews, and readiness checks. But an explicit generalized reconfirmation law for user commitments and future objects seems only partially present.

#### Preparation windows

ION often prepares and stages work through horizons, context compilation, readiness checks, and transition gates. But a generalized preparation-window layer for all future-bearing commitments still seems fragmented.

#### Budget-aware future behavior

ION already tracks and reasons about budgets, bounded work, context pressure, and execution slices in multiple places. But explicit budget-time doctrine with calibrated future allocation, reserves, and resource posture appears incomplete.

#### Temporal ownership

ION already has executors, roles, route-state, and holder-like responsibility concepts. But explicit temporal lease law over future commitments appears under-specified.

### 38.3 Likely missing centers

These are the areas that most likely require genuine new formalization rather than mere rewording.

#### Unified temporal relevance model

A general law for when an object becomes warm, hot, cooling, dormant, or archival across object classes does not yet appear to exist as one coherent center.

#### Triple-time bridge

ION seems to need an explicit law reconciling:

* civil time,
* orchestration time,
* and budget time.

This bridge appears to be the real missing unifier.

#### Temporal lease protocol

A first-class law for who holds future obligations, when that lease starts, how it renews, and when it transfers still appears missing.

#### Reconfirmation / wake / cooldown / recurrence family

The ingredients exist in fragments, but a unified protocol family governing those transitions appears not yet consolidated.

#### Estimate receipt and calibration doctrine

ION appears to need a stronger explicit doctrine for forecast bundles, actual burn receipts, recalibration, and endurance learning.

---

## 39. Audit table

A concise formulation of the anti-duplication audit is below.

### 39.1 Already exists

* horizon layering
* scheduler commitment staging
* branch/route-state activation conditions
* blocked/ready/deferred posture
* automation progression and fallback posture
* continuation, replay, settlement timing
* archive and historical line preservation
* future candidate logic

### 39.2 Exists in fragmented form

* temporal relevance across object classes
* cooling/dormancy as generalized lifecycle
* reconfirmation before enactment
* preparation windows
* user-facing future obligation handling
* budget-aware execution expectation
* temporal ownership of future commitments

### 39.3 Likely missing

* unified temporal relevance law
* temporal lease law
* triple-time bridge law
* generalized wake/reconfirmation/cooling/recurrence family
* budget-time endurance/calibration doctrine
* estimate receipts and forecast reconciliation as first-class law

---

## 40. Minimal first protocol recommendation

The first protocol should not attempt to define everything.

The best first candidate appears to be a protocol that unifies temporal relevance across existing systems without erasing their local structure.

### 40.1 Recommended first formalization

A likely first protocol would be:

`ORCHESTRATION_TEMPORAL_RELEVANCE_PROTOCOL`

Its purpose would be to define:

* what it means for any object to be temporally alive,
* how heat is derived,
* how warm/hot/cooling/dormant states are determined,
* how current relevance is compiled from existing horizon, scheduler, route-state, and automation inputs,
* and how this law remains distinct from civil schedule and budget posture.

This first protocol is attractive because it does not replace the scheduler, the calendar, or the budgeting system. It simply gives them a common temporal language.

### 40.2 Why not start with the full triple-time bridge

Starting with the full bridge may be premature because it risks building a unifying abstraction before the system has a disciplined common relevance model.

First establish what temporal relevance means.
Then build the bridge across civil time and budget time.

### 40.3 Why not start with calendar integration

Calendar integration is too downstream. It risks falsely turning civil time into the whole center.

### 40.4 Why not start with budget doctrine first

Budget doctrine is critically important, but without a unified relevance model it may become a parallel planning system rather than part of one temporal field.

---

## 41. Candidate first-pass algorithm for temporal relevance

A first-pass computation model might look like this.

### 41.1 Inputs

* horizon position
* scheduler commitment state
* route-state activation conditions
* dependency pressure
* unresolved blocker count
* civil deadline proximity
* reconfirmation overdue state
* current resource posture
* recurrence imminence
* recent user reaffirmation or change
* current lease ownership

### 41.2 Outputs

* civil_heat
* orchestration_heat
* budget_heat
* composite_relevance
* wake_required
* reconfirm_required
* preparation_required
* cooling_permitted
* dormant_eligible

### 41.3 Constraints

* civil heat must not overwrite orchestration truth
* orchestration heat must not erase real-world commitments
* budget heat must not silently cancel commitments
* explicit receipts should exist when state transitions occur

This algorithm should likely begin as a conservative, auditable pass rather than an aggressive autonomous planner.

---

## 42. First worked scenario template

A reusable scenario template should be added so future design work stays concrete.

### Scenario skeleton

1. Object introduced
2. Civil profile assigned
3. Orchestration profile assigned
4. Budget profile assigned
5. Initial heat computation
6. Lease assignment
7. Wake/reconfirmation behavior
8. Enactment decision
9. Cooling outcome
10. Receipt and calibration result

Every future scenario should be written through that skeleton.

---

## 43. Next concrete authoring targets

The strongest next authoring targets are now:

1. a dedicated draft of `ORCHESTRATION_TEMPORAL_RELEVANCE_PROTOCOL`
2. a draft of `TEMPORAL_CONTEXT_LEASE_PROTOCOL`
3. a strict schema proposal for temporal objects
4. a first-pass `TRIPLE_TIME_RECONCILIATION_PROTOCOL` note
5. several worked scenarios using the scenario skeleton

These should be authored in that order unless further audit shows duplication risk is higher than currently believed.
