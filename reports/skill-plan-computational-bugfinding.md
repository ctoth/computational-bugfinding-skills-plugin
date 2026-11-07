# Skill Plan: Computational Bugfinding

**Date:** 2026-11-07
**Research source:** `reports/skill-research-computational-bugfinding.md`
**Existing marketplace:** none selected for extension; new standalone marketplace/plugin proposed.

## State

Q approved this plan with “Make it so!” Phase 3 research and drafting are authorized. Local repository bootstrap, the foundation skill, correctness-oracles and evidence-based-triage are committed. The independent foundation behavior check found no blocking skill defect; it did not execute a campaign or establish bug yield. Harness-sensitivity drafting is in progress. No tooling installation or target changes have been made. The plan uses Barn's stronger already-fetched `origin/master` source inventory as the baseline, not basic fuzzing capability.

## Design basis

The requested outcome is compute spent on reproducible product defects. Input volume, coverage, crashes, disagreements and LLM confidence are intermediate evidence, not that outcome. Plan independent skills around the search dimension and correctness contract that change the agent's work; use tool-specific references within those boundaries.

## Overview

Propose **25 skills in one `bugfinding` plugin**, distributed by a new `computational-bugfinding-marketplace`. The initial build covers a complete discovery loop plus distinct advanced search methods. Four proposed skills require substantial method-level research before their drafting can be justified; they are identified below as research-first, not represented as ready capabilities. Other skills still require Phase 3 primary-source and literature work, as skillbuilder specifies.

The foundation is `bugfinding-campaign`: establish the target's demonstrated baseline, find an unsearched failure space, choose a usable oracle and a bounded pilot, then allocate further compute using observed evidence. Detailed oracle construction, validation, execution and triage remain separate owners. No generic task scheduler, database, adapter framework, container platform or autonomous publication machinery is proposed.

### What must exceed Barn

The research report's **Stronger already-fetched baseline: `origin/master`** section records thirteen native fuzz targets plus a Toast differential lane (`.github/workflows/fuzz.yml:38-54`), bounded valid-IR construction (`internal/fuzzseed/structured.go:11-105`), and compilation-required structured execution (`vm/fuzz_test.go:27-49`). Its baseline also includes production-validated mutated snapshots, database normalization round trips, multi-operation concurrent engine workloads, controlled renewal interleavings and twenty Elle fault controls. Those are accomplishments to retain, not new features of this pack.

The pack earns its value by changing what an agent can test next: generate a valid world plus a successful state-dependent program, compare observable world effects across equivalent engine states, search and replay schedules beyond selected interleavings, interrupt actual persistence boundaries, solve hard path constraints where a supported backend exists, and search for resource/liveness failures under stated contracts. These are proposed capability advances, not claims that the inspected Barn tree is defective or lacks every implementation elsewhere. The report did not inspect every worktree or query the live remote.

## Proposed Skills

All skills retain normal automatic discovery and explicit invocation. `both` below means a precise request can select the skill; it does not confer permission to run campaigns or mutate targets. `fork` is a Claude execution hint, not a requirement for Codex or another host to spawn an agent. Portable frontmatter uses `name` and `description`; host-specific settings stay optional. Size estimates refer to the entrypoint, with detailed platform/tool instructions in references.

### 1. `bugfinding-campaign` — foundation

- **Type / invocation / context / size:** behavioral-guidance / both / inline / medium (100-300 lines).
- **Scope:** Move a target from its demonstrated bugfinding baseline into a specific new failure space; compare short pilots and allocate an authorized compute budget.
- **Excludes:** Method implementations, an optimization service, guaranteed bug yield, automatic cloud spending or publishing.
- **Key content:** Baseline source inventory; target/contract/search/oracle tuple; harness sensitivity evidence; bounded pilot; useful semantic reach; unique reproduced defects, duplicate and infrastructure rates; reduction/triage costs; explicit negative results and stopping reasons. References route to the specialist skills rather than duplicating them.
- **Cross-tool notes:** Self-contained campaign record in ordinary files; no dependency on Ward, this user's paper collection or protocols installation.
- **Why separate:** Deciding which experiment deserves compute is different from executing any one fuzzer or checker.
- **Evidence / research:** Research report, Gap analysis and Barn capability candidates; AFL++ campaign documentation. No empirical yield claim is supported.
- **Acceptance example:** Given Barn's current fuzz/Elle source inventory and a fixed budget, choose and justify a new search dimension rather than merely raise `-fuzztime`; save pilot evidence and a reasoned continuation or stop decision.

### 2. `correctness-oracles`

- **Type / invocation / context / size:** behavioral-guidance / both / inline / medium.
- **Scope:** Turn a documented behavioral guarantee into an executable discriminator with explicit preconditions and outcomes.
- **Excludes:** Detailed metamorphic, differential, linearizability or isolation algorithms; inventing unspecified product guarantees.
- **Key content:** Real producers and externally visible effects; independent expected behavior; partial oracles; unsupported/inconclusive outcomes; observation loss; avoid implementing the same defect in both target and checker.
- **Cross-tool notes:** Language-neutral contract and observation design; references contain examples, not a required assertion library.
- **Why separate:** Stronger input search cannot compensate for an oracle that accepts wrong behavior.
- **Evidence / research:** Elle page-image notes and SQLancer primary docs in the research report; deeper oracle literature required.
- **Acceptance example:** Replace a panic-only property with a justified state invariant that rejects an independently specified wrong effect while accepting legal quota errors.

### 3. `harness-sensitivity`

- **Type / invocation / context / size:** checklist-audit / both / fork / medium.
- **Scope:** Establish that the harness reaches its claimed target and rejects representative violations before expensive search.
- **Excludes:** Product hardening, mandatory mutation infrastructure or a claim that mutation score measures all bugs.
- **Key content:** Known historical regressions; justified negative controls; reachability and instrumentation checks; fault provenance; distinguish unreachable, equivalent and surviving mutants; isolate state leakage and accidental pass paths.
- **Cross-tool notes:** Prefer existing defects/checks and the current test runner; mutation tools only where justified and supported.
- **Why separate:** This tests the experiment's power, not the product's correctness.
- **Evidence / research:** Barn's `scripts/check_elle.py:11-18,58-103` is the baseline example; mutation-tool selection needs further research.
- **Acceptance example:** Demonstrate a new persistence oracle catches a known lost-acknowledgment fault; simply restating Barn's existing twenty Elle controls does not qualify as new capability.

### 4. `stateful-property-testing`

- **Type / invocation / context / size:** behavioral-guidance / both / inline / medium.
- **Scope:** Generate and shrink dependent API-operation sequences and object states against a simpler justified model.
- **Excludes:** Grammar/program generation, thread scheduling and a copied production implementation as the model.
- **Key content:** Preconditions and state-dependent domains; object identity/lifetime; legal and deliberately illegal sequences; model transitions; successful-operation reach; shrink sequence and initial state together. Hypothesis and fast-check belong in conditional runtime references.
- **Cross-tool notes:** Python/JS examples plus language-neutral operation modeling; Go must use a verified fitting harness, not pretend Hypothesis is native Go.
- **Why separate:** Operation validity depends on previous results rather than independent values.
- **Evidence / research:** Hypothesis stateful docs and fast-check introduction; advanced shrink/model details require Phase 3 research.
- **Acceptance example:** Generate object creation, permissions and mutations that reach successful deep paths, preserving a replayable initial world and sequence beyond Barn's empty-store VM input lane.

### 5. `semantic-program-generation`

- **Type / invocation / context / size:** behavioral-guidance / both / inline / medium.
- **Scope:** Generate programs whose semantic preconditions reach intended runtime behavior, not merely syntactically valid source.
- **Excludes:** Reimplementing a parser/formatter, byte-level mutation configuration, treating existing Barn structured generation as novel.
- **Key content:** Existing IR/formatter ownership; variable environments, types and object capabilities; effect-aware generation; defined-behavior restrictions; generation-choice shrinking; successful path measurements and rejection diagnosis.
- **Cross-tool notes:** Target semantics first; Csmith/FuzzTest are examples to research, not universal backends.
- **Why separate:** Valid programs require environment and semantic constraints that general API sequences do not.
- **Evidence / research:** Barn `origin/master:internal/fuzzseed/structured.go` baseline and Csmith/FuzzTest docs; semantic generator literature still required.
- **Acceptance example:** A Barn generated program creates the world its property/verb operation requires and reaches that operation successfully; the world and program shrink without losing the same violation.

### 6. `coverage-guided-fuzzing`

- **Type / invocation / context / size:** tool-runner / both / fork / medium.
- **Scope:** Build and operate an instrumented input-search lane appropriate to the actual runtime and harness.
- **Excludes:** A native Go fuzzing tutorial, corpus lifecycle ownership, oracle invention or one skill per fuzz engine.
- **Key content:** Instrumented code coverage and harness overhead; state reset/reentrancy; reject ratios; dictionaries and custom mutators where needed; source/binary mode; throughput versus semantic reach; per-lane replay and owned process cleanup.
- **Cross-tool notes:** Progressive references for native AFL++/libFuzzer/FuzzTest, Go, Rust cargo-fuzz, Python Atheris, JVM Jazzer. Validate toolchain/platform first; add no universal wrapper.
- **Why separate:** Instrumentation and search mechanics require runtime-specific operations independently of the property.
- **Evidence / research:** Primary docs in research report's tool map; current maintenance, build matrices and licenses need verification for each shipped reference.
- **Acceptance example:** Demonstrate a selected lane instruments target code and reaches an asserted property; a larger corpus of rejected inputs alone fails the evaluation.

### 7. `corpus-evolution`

- **Type / invocation / context / size:** tool-runner / both / fork / medium.
- **Scope:** Preserve and improve search material across campaigns without losing reproductions or provenance.
- **Excludes:** A cache service, content-addressed storage framework or assuming language-identical corpora share an input encoding.
- **Key content:** Real-producer seeds; coverage and semantic diversity; minimization versus regression retention; encoding conversion; generator decision inputs versus source artifacts; corpus exchange compatibility; stale/poisoned seeds; cost of repeatedly slow entries.
- **Cross-tool notes:** Use native corpus tools and existing directories; metadata proportional to provenance/replay needs.
- **Why separate:** A long-lived corpus has different goals from one campaign's runtime tuning or one failure's reduction.
- **Evidence / research:** AFL++ corpus docs, Go fuzz docs and Barn's structured-choice/string-corpus distinction.
- **Acceptance example:** Recognize that Barn's structured-choice bytes cannot be sent unchanged to a string-source Toast lane; use the existing producer to create a valid replay artifact and retain provenance.

### 8. `semantic-differential-testing`

- **Type / invocation / context / size:** behavioral-guidance / both / inline / medium.
- **Scope:** Compare independent implementations, modes or versions under matched semantic conditions, including observable effects.
- **Excludes:** Calling every difference a bug, majority vote as a specification, or defaulting to textual equality.
- **Key content:** Contract intersections; equivalent per-case state; result/error/effect comparison; nondeterminism; expected divergence ledger; undefined/implementation-defined behavior; minimize disagreements; adjudicate with primary contract evidence.
- **Cross-tool notes:** Language-neutral comparison; tool adapters only where target needs demonstrate them.
- **Why separate:** Establishing valid cross-implementation comparison is independent of generation.
- **Evidence / research:** Barn `origin/master:scripts/fuzz_differential.py:52-82,199-220`; Csmith and SQLancer docs.
- **Acceptance example:** Extend a finite return-value comparison to a justified world-effect contract with equivalent starting worlds; preserve both raw outcomes and distinguish timeout from semantic inequality.

### 9. `metamorphic-testing`

- **Type / invocation / context / size:** behavioral-guidance / both / inline / medium.
- **Scope:** Derive and search justified relations between executions when direct expected results are unavailable.
- **Excludes:** Assuming all round trips preserve bytes or applying mathematical equalities across effects, overflow and floating-point behavior without preconditions.
- **Key content:** Relation derivation from target guarantees; valid transformations; normalization; effect/order constraints; relation sensitivity controls; reduction of original and transformed cases together.
- **Cross-tool notes:** Reuse target transformations rather than create parallel implementations.
- **Why separate:** A relation between runs has its own validity proof and failure modes, unlike a reference comparison.
- **Evidence / research:** Barn normalized database round trip and SQLancer map; broader relation literature is a Phase 3 requirement.
- **Acceptance example:** Derive a semantics-preserving program/world transformation beyond Barn's existing format and database idempotence checks; show a control violation is rejected.

### 10. `native-memory-instrumentation`

- **Type / invocation / context / size:** tool-runner / both / fork / medium.
- **Scope:** Search executed native code with appropriate memory/undefined-behavior instrumentation.
- **Excludes:** Input generation, race detection, claiming Valgrind observes all managed-runtime semantic defects.
- **Key content:** ASan/MSan/UBSan/LSan and Memcheck selection, build/runtime compatibility, symbolization, instrumentation boundaries, suppressions requiring evidence, overhead and diagnostic reproduction.
- **Cross-tool notes:** Native code and native extensions/FFI need distinct verified build recipes; check current platform support before selecting a tool.
- **Why separate:** Instrumentation establishes a different runtime property and can require incompatible builds.
- **Evidence / research:** ASan and Valgrind quick-start read; other sanitizer documentation, licensing and support matrices require deep research.
- **Acceptance example:** Attribute a diagnostic to the instrumented target path and reproduce it; avoid recommending Memcheck merely because Barn is written in Go.

### 11. `race-detection-campaigns`

- **Type / invocation / context / size:** tool-runner / both / fork / medium.
- **Scope:** Design workloads that expose conflicting memory accesses under a supported race detector.
- **Excludes:** Locking style advice, schedule-exhaustiveness claims and logical transaction correctness.
- **Key content:** Executed shared-memory paths, instrumentation coverage, cgo/native boundaries, varied concurrency pressure, raw conflicting-access evidence, replay limits and coverage omissions.
- **Cross-tool notes:** Go `-race` and researched native/runtime detectors in separate references; existing Go memory-model skills remain language-authoring owners.
- **Why separate:** A race detector's observed-access oracle differs from controlled schedule enumeration and abstract history checks.
- **Evidence / research:** Go race detector docs; other runtime integrations need deeper research.
- **Acceptance example:** Build a workload reaching the target's actual competing accesses; do not turn a green `-race` run into a claim that Barn transactions are correct.

### 12. `schedule-exploration`

- **Type / invocation / context / size:** tool-runner / both / fork / medium.
- **Scope:** Search controlled scheduling decisions for safety or liveness violations and preserve replay traces.
- **Excludes:** Treating arbitrary goroutine stress or virtual time as systematic exploration, or promising exhaustive search outside a stated model/bound.
- **Key content:** Controllable boundaries; scheduler/model coverage; bounded and randomized strategies; reduction of workload plus schedule; uncontrolled sources; replay outside the controller; tool memory-model limitations.
- **Cross-tool notes:** Loom/Shuttle for suitable Rust targets and Coyote for suitable .NET targets; **no verified drop-in Go controller**. Barn adaptation requires target-source research and existing seams, not a new universal scheduler.
- **Why separate:** Schedule choices form a search space independent of input values.
- **Evidence / research:** Loom, Shuttle and Coyote primary docs; bounded schedule-search literature required.
- **Acceptance example:** Search a stated set of validation/publication/retry decisions beyond Barn's existing held interleavings and save the exact failing choice trace.

### 13. `linearizability-checking`

- **Type / invocation / context / size:** tool-runner / both / fork / medium.
- **Scope:** Check concurrent operation histories against a justified executable sequential specification.
- **Excludes:** Transaction-isolation checking, inventing semantics for incomplete operations, or treating a checker as workload generation.
- **Key content:** Invocation/response intervals, operation identity, pending/uncertain operations, model state, partitioning validity, checker cost, witnesses and unknown outcomes.
- **Cross-tool notes:** Porcupine is the initial researched integration; histories remain inspectable raw artifacts.
- **Why separate:** Linearization requires a different model and history contract from serializable transactions.
- **Evidence / research:** Porcupine docs; deeper history/model literature required.
- **Acceptance example:** Establish an applicable public operation contract and produce a sequential-model witness; do not relabel Barn's Elle serializability verdict as linearizability.

### 14. `transactional-history-testing`

- **Type / invocation / context / size:** tool-runner / both / fork / medium.
- **Scope:** Design informative transaction workloads and check the claimed isolation model with explicit anomaly evidence.
- **Excludes:** Generic concurrency stress, schema correctness, predicate guarantees unsupported by the selected checker.
- **Key content:** Observable dependency/provenance design; transaction and retry boundaries; failed/uncertain attempts; isolation selection; anomaly classes; checker soundness/completeness conditions; witness preservation and fault controls.
- **Cross-tool notes:** Elle is the initial integration; exact history format/checker version is target-specific.
- **Why separate:** Transactional dependency inference and isolation claims differ from sequential object models.
- **Evidence / research:** Elle's fully read page images/notes and Barn workload/recorder/checker baseline.
- **Acceptance example:** Identify a new observable dependency dimension or transaction boundary, explain what existing Barn append/register histories cannot decide, and validate the extension's oracle.

### 15. `distributed-fault-testing`

- **Type / invocation / context / size:** tool-runner / both / fork / medium.
- **Scope:** Generate workloads against disposable real systems while injecting justified network/process/clock failures and checking histories.
- **Excludes:** Unrequested production experiments, generic chaos without a correctness oracle, equating real-cluster replay with deterministic simulation.
- **Key content:** Actual client semantics; fault model and topology; recovery; acknowledged versus uncertain operations; fault/workload evidence; checker selection; resource ownership and cleanup.
- **Cross-tool notes:** Jepsen is an initial researched route; its concrete setup, fault support and licensing remain to verify.
- **Why separate:** Real deployment faults include observations and uncontrolled behavior not captured by in-process schedules.
- **Evidence / research:** Jepsen official analyses and Elle distinctions; detailed framework/client/nemesis source research required.
- **Acceptance example:** On an authorized disposable deployment, save client history, injected fault sequence and violated contract; service disruption alone is not a discovered correctness bug.

### 16. `deterministic-simulation`

- **Type / invocation / context / size:** behavioral-guidance / both / inline / medium.
- **Scope:** Use an existing controllable simulation environment to explore system failures reproducibly; assess what cannot be controlled.
- **Excludes:** Retrofitting every project with a simulation runtime, a second production implementation, attach-any-process promises.
- **Key content:** Controlled time/network/disk/randomness; production-code boundary; replay seed plus environment; simulated fault coverage; divergence from real hardware; validate outside simulation.
- **Cross-tool notes:** FoundationDB/Flow is a source-backed example of architecture dependence, not a Go integration plan.
- **Why separate:** Replayable whole-environment control has distinct prerequisites from thread-schedule control and real-cluster faulting.
- **Evidence / research:** FoundationDB testing source docs; further simulation architecture/literature before drafting.
- **Acceptance example:** First establish a real existing simulation seam and one faithfully replayed failure; when absent, explain the constraint and choose a suitable existing technique rather than build infrastructure speculatively.

### 17. `crash-consistency-testing` — research-first

- **Type / invocation / context / size:** tool-runner / both / fork / medium.
- **Scope:** Explore interruption and storage-failure boundaries against a documented recovery/durability contract.
- **Excludes:** Treating database round trips or serializability as durability, assuming process kill models all power failures.
- **Key content:** Acknowledgment/flush/rename ordering; partial writes, ENOSPC and I/O errors; filesystem model; replayable fault points; recovered-state oracle; sequence reduction.
- **Cross-tool notes:** Select tools only after persistence and filesystem-source research; no selected ready backend in Phase 1.
- **Why separate:** Recovered state and acknowledgment promises need a failure model beyond completed executions.
- **Evidence / research:** Research report explicitly identifies this as unresolved; primary crash-consistency papers and concrete tools are mandatory before drafting.
- **Acceptance example:** Against a disposable Barn persistence path, demonstrate an acknowledged-operation recovery property at a real failure boundary beyond normalized completed round trips. This is a proposed evaluation, not authorization to change Barn.

### 18. `symbolic-concolic-execution`

- **Type / invocation / context / size:** tool-runner / both / fork / medium.
- **Scope:** Reach difficult program paths with symbolic constraints or concrete-plus-symbolic exploration where the target/tool supports it.
- **Excludes:** Drop-in KLEE for Go, solver success as evidence of executable reachability, a duplicate target written just for tooling.
- **Key content:** Supported code/build; symbolic input boundaries; environment stubs and their fidelity; path explosion; constraint budgets; solver-model artifacts; concrete replay of counterexamples.
- **Cross-tool notes:** KLEE is a researched LLVM route; concolic/hybrid backends need additional primary-source selection research.
- **Why separate:** Path-constraint search differs operationally from bounded invariant checking.
- **Evidence / research:** KLEE site; method and hybrid literature required before advertised recipes.
- **Acceptance example:** Solve a branch random search misses, then replay the generated input through the real target and the same oracle; unsupported Go applicability is stated plainly.

### 19. `bounded-model-checking`

- **Type / invocation / context / size:** tool-runner / both / fork / medium.
- **Scope:** Check assertions/invariants within an explicit executable model and bounds using a supported checker.
- **Excludes:** Unbounded correctness claims, copying production behavior into an unchecked model, symbolic path exploration recipes owned above.
- **Key content:** Real target linkage; unwinding/completeness assertions; environment and memory models; bounds and solver outcomes; counterexample replay; when abstraction has lost the producer.
- **Cross-tool notes:** CBMC plus separately verified JBMC/Kani references; no implied native Go support.
- **Why separate:** Bounds, model fidelity and solver counterexamples create different interpretation obligations from fuzzing.
- **Evidence / research:** CBMC primary docs; linked tools, specification-checking alternatives and relevant papers need deeper reading.
- **Acceptance example:** State the checked bound and reproduce a counterexample on the real supported target; a bounded pass is reported with its exact limits.

### 20. `resource-complexity-testing`

- **Type / invocation / context / size:** tool-runner / both / fork / medium.
- **Scope:** Search inputs and operation sequences for violations of CPU, allocation, memory/handle retention and scaling contracts.
- **Excludes:** General profiling tutorials, performance tuning, a single slow run treated as a bug.
- **Key content:** Input-size families; cold/warm state; baseline matching; resource reset; growth/retention thresholds; repeated measurements; quota versus host exhaustion; robust minimization of resource violations.
- **Cross-tool notes:** Reuse current profilers/measurement owners; target-specific workload search is the new capability.
- **Why separate:** The interestingness predicate is a resource behavior over measurements or input sizes, not a simple crash.
- **Evidence / research:** Barn watchdog/tick baseline and installed performant-golang overlap; complexity-search literature/tools still required.
- **Acceptance example:** Preserve a repeatable family demonstrating excessive growth or retained resources outside documented quotas, beyond Barn's existing fixed tick and stuck-call guards.

### 21. `liveness-testing` — research-first

- **Type / invocation / context / size:** behavioral-guidance / both / inline / medium.
- **Scope:** Search for lost progress, starvation, deadlock and unbounded retries under stated fairness and environment assumptions.
- **Excludes:** Calling every timeout a product hang, or translating temporal requirements into arbitrary short deadlines.
- **Key content:** Progress witnesses; obligations and fairness; quiescence versus deadlock; virtual versus real clocks; blocked dependency diagnosis; reduced schedule/workload and observer effects.
- **Cross-tool notes:** Runtime/tool selection follows specific progress contract research; schedule skill supplies controlled search where possible.
- **Why separate:** Eventual progress is a distinct correctness contract from safety and measured complexity.
- **Evidence / research:** Phase 1 identifies this gap and baseline guards; dedicated liveness literature and tools not yet established.
- **Acceptance example:** Reduce a workload where an admitted task cannot make its required progress under admissible schedules, with evidence separating scheduler/harness timeout from the product violation.

### 22. `failure-reduction`

- **Type / invocation / context / size:** tool-runner / both / fork / medium.
- **Scope:** Minimize a candidate while retaining the same executable violation and causal evidence.
- **Excludes:** Deduplicating root causes, changing the oracle to make reduction pass, reducing all cases to bytes regardless of structure.
- **Key content:** Interestingness with validity and witness identity; bytes/programs/worlds/operations/schedules/faults; deterministic and flaky cases; reduction budgets; original and minimized artifacts; failed reductions.
- **Cross-tool notes:** Prefer existing shrinkers; C-Reduce where language appropriate; other reducers require verified applicability.
- **Why separate:** Reduction is a search problem with its own oracle and can silently switch the failure.
- **Evidence / research:** C-Reduce docs, native Go/Hypothesis shrinking; domain-specific reducers need Phase 3 research.
- **Acceptance example:** Minimize world plus program plus schedule while preserving the same anomaly witness; a smaller unrelated panic does not satisfy the task.

### 23. `evidence-based-triage`

- **Type / invocation / context / size:** checklist-audit / both / fork / medium.
- **Scope:** Use LLMs to organize failures and investigate them into evidence-backed product findings, harness defects, expected differences or unresolved cases.
- **Excludes:** LLM/majority confidence as correctness, silent dismissal of unreproduced cases, automatic posts or fixes.
- **Key content:** Real input/producer; raw output and contract citation; source/config identity; reproduction status; symptom grouping versus verified duplicate cause; uncertainty; user-visible effect; maintainer-ready artifact paths. Future harness proposals require executable validation rather than persuasive text.
- **Cross-tool notes:** Plain files/raw artifacts usable without the original LLM; no model-specific service dependency.
- **Why separate:** A generated failure is not yet a product bug, and triage can lose real evidence through premature certainty.
- **Evidence / research:** Research report's verified failure classifications and Barn checker outcomes. OSS-Fuzz-Gen effectiveness has not been read; no efficacy claim is proposed.
- **Acceptance example:** A blind evaluation supplies a true defect, harness fault, intended engine difference and inconclusive trace; preserve all four with justified classifications and no invented certainty.

### 24. `configuration-differential-testing` — research-first

- **Type / invocation / context / size:** tool-runner / both / fork / medium.
- **Scope:** Search configuration/build/platform interactions under an explicitly shared behavioral contract.
- **Excludes:** Treating different documented capabilities as bugs, a generic compatibility matrix service, expanding runtime support by implication.
- **Key content:** Valid configurations and dependency constraints; interaction coverage versus full products; cross-architecture/build-mode comparisons; exact enabled config; effect oracle; reduction to responsible factors.
- **Cross-tool notes:** Concrete covering-array/configuration tools and methods remain to research; tool-independent design does not imply integration readiness.
- **Why separate:** The variables are interacting environment/build choices and constrained products, rather than independent implementations alone.
- **Evidence / research:** Report flags combinatorial configuration/cross-architecture testing as unverified; primary tool/literature pass required.
- **Acceptance example:** A justified capability combination reaches a real target path omitted by a core-only lane; minimize the responsible configuration while preserving the same violated guarantee.

### 25. `numerical-oracles` — research-first

- **Type / invocation / context / size:** behavioral-guidance / both / inline / medium.
- **Scope:** Design correctness comparisons and adversarial input search for floating-point/numerical behavior.
- **Excludes:** Global epsilon guesses, exact-real identities assumed under floating point, using the target as its own reference.
- **Key content:** Specified rounding and error bounds; high-precision references; ULP/relative/absolute criteria; conditioning; NaN/infinities/signed zero; architecture variation; reduction that retains numerical meaning.
- **Cross-tool notes:** Numerical libraries and search tools are unselected; domain-specific primary research must precede recipes.
- **Why separate:** Numerical equivalence and valid metamorphic relations require different contracts from exact-value comparison.
- **Evidence / research:** Report identifies numerical oracles as an open area and notes Barn's deliberate float exclusion; no algorithm/tool readiness claim.
- **Acceptance example:** Resolve a selected float contract and build a sensitive oracle before broadening a lane that deliberately excludes floats; do not remove the exclusion simply to increase counts.

## Skill Relationships

`bugfinding-campaign` routes to an appropriate generator/search skill and an oracle skill. `correctness-oracles` owns the general contract-to-observation reasoning; specialist differential/metamorphic/history/numerical skills own their distinct rules. `harness-sensitivity` measures whether the proposed lane can reject representative violations. It is useful evidence for a new expensive experiment, not an extra recurring approval gate.

Stateful/API and semantic-program generators can feed coverage-guided fuzzing, differential checks or schedule search. Corpus evolution preserves search material across those lanes. Race detection, linearizability and transactional isolation are complementary observations, never interchangeable verdicts. Real-system fault injection, deterministic simulation and crash consistency use different failure models. Symbolic execution and bounded checking are selected only for compatible targets. Resource and liveness oracles can guide more than one search engine.

Reduction and triage consume original raw artifacts; the campaign uses their measured cost and confirmed outcomes to choose the next allocation. Shared concepts are linked rather than copied across entrypoints. Skills should read only the relevant runtime references, not load the entire pack.

## Runtime Coverage and Existing Ownership

| Runtime / environment | Initial concrete sources | Boundary or missing research |
|---|---|---|
| Go | Native fuzzing, race detector, Porcupine; Barn valid-IR/Toast/Elle source baseline | Advance search/oracles; no claimed general schedule controller or KLEE/CBMC integration. Existing golang skills retain syntax/testing/memory-model guidance. |
| C/C++ and native extensions | AFL++, libFuzzer, FuzzTest, Valgrind/ASan, KLEE/CBMC, Csmith/C-Reduce | Verify supported builds/platforms and selected tool status; native memory instrumentation does not establish application semantics. |
| Rust | cargo-fuzz, Loom/Shuttle; CBMC-linked Kani discovery | Verify memory-model restrictions, toolchain and Kani details; use actual instrumentable code. |
| Python | Hypothesis, Atheris | Stateful model quality and native-extension build boundaries; exact current runtime/tool support at selection time. |
| JS/TS | fast-check | Deeper API and async sequence guidance required; no verified coverage-guided JS runtime chosen in Phase 1. |
| JVM | Jazzer; CBMC-linked JBMC discovery | Verify current build/runtime support and JBMC limits before recipes. |
| .NET | Coyote | Research supported operations/rewriting and replay limits; no general fuzz backend claimed. |
| Distributed/storage/database | Jepsen, Elle, Porcupine, SQLancer, FoundationDB testing docs | Each needs a target-specific contract and environment; simulation and database tools are not drop-in generic app integrations. |

No existing installed skill must be changed to deliver the new pack. The inspected `go-testing-advanced`, `go-race-and-memory-model`, `go-perf-methodology` and protocols `campaign` overlap is documented in the research report. References may acknowledge those owners, but the plugin must function without this user's other plugins. External marketplace discovery was incomplete in Phase 1; per-skill research must inspect relevant existing work before claiming novelty or recreating a mature integration.

## Proposed Marketplace and Plugin Layout

Approved root: `C:/Users/Q/code/computational-bugfinding-skills-plugin` (bootstrap underway).

```text
computational-bugfinding-skills-plugin/
  .claude-plugin/marketplace.json
  .agents/plugins/marketplace.json
  plugins/bugfinding/
    .claude-plugin/plugin.json
    .codex-plugin/plugin.json
    skills/<skill-name>/SKILL.md
    skills/<skill-name>/references/...
  reports/...
  agent-notes/computational-bugfinding-marketplace.md
```

One plugin avoids artificial package dependencies between complementary methods. Separate skills supply precise discovery and progressive loading. Use marketplace name `computational-bugfinding-marketplace`, plugin name `bugfinding`, initial version `0.1.0`; confirm actual manifest validation requirements during drafting. Do not invent a remote repository URL, license, install claim or publication state. Repository creation/publication remains separate from this written plan.

Packaging evidence inspected read-only: local `golang-skills-plugin/.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`, and the `plugins/golang/.claude-plugin/plugin.json` and `.codex-plugin/plugin.json`. They demonstrate the local two-host manifest layout and a `skills` directory owner. This is compatibility precedent, not verification of a future package. No hook, background runner, cloud account or dependency installer is proposed.

Per-skill research reports hold source URL/section/short quote/decision relevance. Drafted references contain `common-mistakes.md`, `sources.yaml` and the actual method/runtime guidance required by the skillbuilder pipeline; keep substantive material in one owner. Add executable helpers only after a concrete repeated operation justifies one. Do not copy external code/manuals or create empty reference scaffolds.

## What Was Excluded

- A single mega-skill, one skill per product, and a basic Go fuzzing course: they do not meet the user's requested capability gain.
- General secure coding, linting, profile-driven optimization, test-style advice and release/PR machinery: existing owners and outside this discovery domain.
- Dedicated kernel/syscall, GUI/browser, protocol, side-channel/constant-time and grammar-inference skill claims in the first draft set: Phase 1 identified these but did not establish the primary method/tool evidence needed to choose credible boundaries. Protocol sequences can initially use the stateful skill where its model applies. Preserve these as explicit next research candidates rather than pretend coverage.
- A standalone mutation-testing score skill: sensitivity to known defects belongs in harness validation; it is not a direct product-bug count.
- An LLM bug-verdict authority or unattended issue poster: evidence triage is included; publishing is not authorized by discovery.
- A universal scheduler, simulation layer or second implementation for solver access: no demonstrated target problem warrants that infrastructure.

## Recommended Build Order

The whole set is the proposed scope; ordering reduces research/draft failure risk, not the ambition.

1. **Foundation first:** research and draft `bugfinding-campaign`; verify its target/contract/search/oracle/budget decisions on a realistic advanced baseline. It becomes the drafting quality reference.
2. **Trustworthy results:** `correctness-oracles`, `harness-sensitivity`, `evidence-based-triage`, `failure-reduction`. These prevent expensive but uninformative runs and preserve discoveries.
3. **Immediate Barn delta:** `stateful-property-testing`, `semantic-program-generation`, `semantic-differential-testing`, `metamorphic-testing`, `corpus-evolution`, `coverage-guided-fuzzing`. Evaluate effect-aware/stateful progress beyond valid-IR source and Toast return-value replay.
4. **Concurrency and systems:** `schedule-exploration`, `linearizability-checking`, `transactional-history-testing`, `distributed-fault-testing`, `deterministic-simulation`, `race-detection-campaigns`, `native-memory-instrumentation`. Never substitute one correctness claim for another.
5. **Hard paths and failure contracts:** `symbolic-concolic-execution`, `bounded-model-checking`, `resource-complexity-testing`, plus research-first `crash-consistency-testing`, `liveness-testing`, `configuration-differential-testing`, `numerical-oracles`. Resolve the named method/tool evidence gaps before their draft agents start. A failed applicability investigation is recorded, not disguised as a tool recipe.
6. **Audit and behavioral evaluation:** audit all expected files and citations; evaluate the four coverage dimensions and skill selection on realistic artifacts. Repair supported findings within the approved scope. Additional scope uses the skillbuilder research→plan→draft→audit path.

Per skill: dedicated primary-source researcher writes a persistent report; drafter consumes that report and the foundation; use batches of two or three as requested by skillbuilder. Commit sequentially to preserve ownership. Use explicit expected files and inspect each report before its dependent phase. Every tool-bearing reference must verify current setup, invocation, applicable build/runtime/platform, limitations and license. Under Q's replacing AGENTS.md instruction of 2026-11-07, every paper claim requires the research-papers plugin's paper-reader and direct page-image reading only; never use paper-process. Preserve historical evidence of previous workflows without repeating them. Elle alone does not satisfy the other methods' literature needs.

## Behavioral Acceptance and Audit

The pack's effect is assessed from generated artifacts and decisions, not a heading or wording test. Use isolated evaluation targets and finite budgets approved for that evaluation. Do not mutate Barn merely to validate a skill. Suggested scenarios:

| Scenario | Required observable result |
|---|---|
| Advanced Barn-like baseline containing native fuzzing, structured programs, differential replay and Elle controls | Inventory existing capability accurately; choose a demonstrably new failure space and avoid presenting a baseline feature as a discovery. |
| A semantically deep object/permission API path | Generate successful dependent state/operations; save replay and shrink the world together with the workload. |
| An observed cross-engine difference with an intentional semantic exception | Preserve raw outcomes, cite the governing contract and leave unsupported conclusions unresolved. |
| A concurrent counterexample where a seed cannot reproduce scheduling | Preserve a sufficient controlled schedule/decision trace where available; explain uncontrolled sources rather than claim seed replay. |
| A checker with an injected known violation and a healthy case | Reject the representative violation through the intended oracle and accept the healthy case; reveal a harness that always passes. |
| A resource anomaly and an infrastructure timeout | Distinguish the falsifiable resource/progress contract from host/test exhaustion using observed evidence. |
| An incompatible solver or simulation request on a Go target | State the incompatibility and select a supported alternative; do not invent a compatible backend or copy code into a new language. |
| A finite campaign finding zero product defects | Report the actual budget, tested property, search reach and limits; preserve a truthful negative result. |

No promised count of new bugs is an acceptance criterion: a bounded run can legitimately find none. To demonstrate discovery power, use selected historical defects or independently injected, realistic defects without revealing their locations or expected diagnosis to the evaluating agent. Preserve what the skill actually changed relative to a comparable baseline; do not claim an empirical gain without that experiment.

## Coverage Dimensions Assessment

| Dimension | Planned coverage | Remaining evidence/gap |
|---|---|---|
| Technical correctness | Distinct generators, instrumentation, semantic/history oracles, schedule/failure models, solver bounds and replay | Phase 3 primary-source/tool/literature depth required for every skill; four research-first methods and deferred domains remain explicit. |
| Human experience | Triage centers silent corruption, lost acknowledged work, incorrect answers, hangs and service degradation; reports serve affected users and maintainers | Need realistic evaluation of maintainer handoff and duplicate/noise burden; no user-study evidence claimed. |
| Testing reality | Sensitivity controls, real producer paths, configuration identity, original/minimized artifacts, unknown outcomes and replay limits | Requires actual isolated behavioral tests; written coverage is not evidence the skill changes decisions. |
| Process integration | Baseline inventory, bounded pilots, long campaign allocation, finite regressions and maintainable findings | Tool deployment, host validation and real-project adoption remain unperformed; no background campaign platform or auto-publication. |

## Open Questions and Approval Boundary

No additional design preference is required to make this plan reviewable. Routine choices above are proposed explicitly. There are no user-facing questions about tool details that primary-source research should settle.

Q confirmed this 25-skill scope and build order with “Make it so!” The invoked skillbuilder's confirmation gate and the user's code-authorization requirement are satisfied. Build locally through research, drafting, audit and isolated behavioral evaluation. No target-tool installation, Barn mutation, publication, remote repository creation or push is implied.

Per-skill research may determine that a candidate is inapplicable or overlaps an existing owner. Record the evidence and propose a bounded change to the approved plan instead of silently substituting architecture. Repository license and any remote publication/install details are unresolved packaging facts, not permission questions needed for the present planning phase.
