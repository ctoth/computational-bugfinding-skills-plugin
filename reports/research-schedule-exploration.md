# Research: schedule-exploration

Date: 2026-11-07

## State

Per-skill research complete for drafting. This report is the only owned repository deliverable; an explicit developer checkpoint required the single minimal task-note State addition reported to parent. Other agents' files are preserved. Literature uses paper-reader/page images only. No target execution, mutation, installation, commit or publication.

## Evidence ledger

Inspecting supported controlled schedulers, replay/bounds and relevant primary paper images. No generic Go scheduler capability or empirical discovery yield is claimed.

### Established current primary-source findings

- Loom README explicitly documents incomplete memory-model support: SeqCst accesses are weakened to AcqRel (possible false alarms), and some load-buffering executions are omitted (possible missed bugs). A nominally exhaustive scheduler is not full language-model verification. Source: https://raw.githubusercontent.com/tokio-rs/loom/master/README.md, Unsupported features; accessed 2026-11-07.
- Loom Builder separately bounds threads, switches per permutation, permutations, time and preemptions, and supports checkpoint state. Preserve all selected limits and remaining unsearched space. Source: https://docs.rs/loom/latest/loom/model/struct.Builder.html, Fields; snapshot 0.7.2, accessed 2026-11-07.
- Shuttle's controlled Rust synchronization/random APIs and emitted schedule string enable replay; replacing only the test wrapper leaves unsupported synchronization outside control. Random, PCT and DFS schedulers have different search policies and limits. Source: https://docs.rs/shuttle/latest/shuttle/, Writing Shuttle tests and Choosing a scheduler; snapshot 0.9.10, accessed 2026-11-07.
- Coyote TestingEngine alone is insufficient: test and production binaries must be rewritten so control hooks run. TryEmitTraces is lazy and must be iterated to materialize traces. Source: https://microsoft.github.io/coyote/how-to/unit-testing/, accessed 2026-11-07.
- Go synctest supplies self-contained bubbles, fake time, durable-block detection and waiting. The actual docs do not specify enumeration of scheduler choices. Mutex/I/O/syscall blocking differs from durable-block operations. Source: https://pkg.go.dev/testing/synctest, Time/Blocking/Isolation; selected page go1.27.3, accessed 2026-11-07.

### Literature image evidence complete

Musuvathi et al., Finding and Reproducing Heisenbugs in Concurrent Programs (OSDI 2008), primary PDF https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osdi2008-CHESS.pdf. Canonical PDF downloaded directly, helper counted/rendered fourteen pages, title/six authors verified from page1 image, ALL images000-013 read directly. No extracted paper text used as evidence. Reader-only artifacts are external to plugin at C:/Users/Q/code/bugfinding-literature/schedule-exploration/papers/Musuvathi_2008_FindingReproducingHeisenbugs/.

- pp.1-4: capture choices for replay and expose alternatives for search are separate requirements. Initial memory/disk/network state remains caller-owned; recorded schedules do not reconstruct arbitrary successful input reads. **Decision:** save initial state/workload/environment and actual scheduler choices together.
- pp.4-7: API wrappers must preserve actual blocking/enabledness and task/resource identities. Synchronization-only schedules can miss racing memory-access outcomes; the historical tool combines reached race detection with added preemption points. **Decision:** establish what the chosen runtime truly controls, and do not claim thread-interleaving search explores all weak-memory behavior.
- pp.7-9: the stateless loop replays a prefix, records a nonpreemptive fair suffix, then chooses alternatives. Imperfect replay may prune search, priming initialization can omit initialization races, and component scoping omits internal interactions. **Decision:** a non-reproduced trace and an unsearched branch remain limits, not silently healthy evidence.
- pp.8-10: preemption bounds reduce state explosion while fairness assumptions determine meaningful progress. Arbitrary stress sleeps/yields can conflict with a fair scheduler's assumption that a yielding task cannot progress. **Decision:** construct a small real scenario and preserve the supported fairness/step model, instead of maximizing thread count or sprinkling sleeps.
- pp.9-12: scheduling is orthogonal to safety/progress monitoring; the studied deadlock/liveness checks need enabledness and fairness assumptions. Historical27 bugs included multiple failure manifestations of the same cause. **Decision:** use an actual semantic oracle and classify unique causes after evidence, not schedule or crash counts.

The external dense reader notes preserve event abstraction, replay/reset, fairness, partial-order/preemption reasoning, equations n^k and k^p with their stated interpretation, wrapper sizes, all eight system parameters, defect classifications, figures and limitations. Historical results do not predict yield on Barn or current tools. All46 bibliography identities, metadata, description, short-excerpt/paraphrased abstract, index, reader ledger and helper-generated keymap exist. No nested reconcile/tag/process/propstore work was invoked under Q's reader-only rule; no claim those excluded workflows completed.

## Operational primary sources and verified conditional recipes

All sources accessed2026-11-07. These commands/APIs were read, not executed; they require a compatible existing target integration. Installation changes, target mutation and campaigns were not performed.

### S1: Loom control boundary and caveats

- URLs: https://docs.rs/loom/latest/loom/ (Writing tests, Yielding, Running, Debugging, Limitations); https://raw.githubusercontent.com/tokio-rs/loom/master/README.md (Unsupported features); https://raw.githubusercontent.com/tokio-rs/loom/master/Cargo.toml (package/features).
- Small quote fragment: “invisible to loom”. Only code using Loom's replacement types participates in its permutation model; nested dependencies can hide synchronization. All other nondeterminism must be controlled through fitting seams. A passing test with an unmodeled std synchronization path is narrower evidence than an all-path claim.
- README's explicit SeqCst/access and load-buffering limitations qualify the docs' broad exhaustive language. Spin loops assume fairness but Loom's scheduler is not fair; documented yield integration changes exploration and must match real algorithm assumptions.
- Existing configured Rust test command shape: `RUSTFLAGS="--cfg loom" cargo test --test loom_my_struct --release`. `LOOM_MAX_PREEMPTIONS=3` is a documented example, not a recommended universal bound. Set environment using the actual shell; keep source/config/bounds with results.
- Inspected package declares0.7.2, Rust1.73, edition2021 and MIT; recheck selected release/toolchain. It has optional checkpoint support, not enabled by the default dependency declaration.

### S2: Loom actual checkpoint and stopping behavior

- URLs: https://docs.rs/loom/latest/loom/model/struct.Builder.html ; https://raw.githubusercontent.com/tokio-rs/loom/master/src/model.rs (Builder/check and checkpoint modules, visible full258-line source).
- Small quote fragment: “not compiled with `checkpoint` feature”. Actual source227-255 implements serialization only under that optional feature and otherwise panics when load/store is attempted. A recipe promising checkpoint replay must enable the selected dependency's checkpoint feature; the default quickstart alone is insufficient.
- Actual `check` loop153-175 checks maximum duration/permutations only at `checkpoint_interval` boundaries, default20000 in this source. Those limits are not immediate hard cutoffs. Per-permutation branch/thread controls and an owned outer resource envelope solve different problems. Do not claim a short max-duration guarantees interruption of a stuck iteration.
- Docs isolate a failing permutation by retaining `LOOM_CHECKPOINT_FILE`, narrowing interval to1 and replaying with identical other settings; only then turn on expensive location/log tracing. Preserve the exact checkpoint and compatible code/configuration, not just the random seed. Source is a mutable snapshot; runtime report must name the selected version and completed scope.

### S3: Shuttle scheduling and replay

- URLs: https://docs.rs/shuttle/0.9.10/shuttle/ ; https://docs.rs/shuttle/0.9.10/shuttle/fn.check_pct.html ; https://docs.rs/shuttle/0.9.10/shuttle/fn.check_dfs.html ; https://raw.githubusercontent.com/awslabs/shuttle/main/README.md .
- Small quote fragment: “schedule string”. Use the replacement synchronization/thread/random APIs throughout the tested path. Existing feature-switched integration documents `cargo test --features shuttle`; it is not an automatic attach-any-Rust-binary tool.
- `check_random(case, ITERATIONS)` selects repeated random schedules. `check_pct(case, ITERATIONS, DEPTH)` selects PCT; its probabilistic assumptions are not an arbitrary confidence promise. `check_dfs(case, Some(MAX_ITERATIONS))` in the inspected0.9.10 API bounds iteration count, despite a general overview also discussing depth. Do not relabel this function argument as schedule depth.
- Preserve emitted choices and replay with `shuttle::replay(case, SCHEDULE)`; file persistence supports replay_from_file. The same code, setup and controlled sources are prerequisites. A passing random campaign does not exhaust schedules or prove correctness.
- Apache-2.0 from official README. Observed docs0.9.10 and main package0.9.9 differ; choose one actual release/source API set rather than silently mix them. No minimum Rust/platform support was established for a selected installation; verify selected package requirements.

### S4: Shuttle limits and artifacts

- URLs: https://docs.rs/shuttle/0.9.10/shuttle/struct.Config.html ; https://docs.rs/shuttle/0.9.10/shuttle/enum.MaxSteps.html ; https://docs.rs/shuttle/0.9.10/shuttle/enum.FailurePersistence.html .
- Small quote fragment: “only checked between iterations”. `max_time` returns between iterations and does not abort an active stuck iteration. `MaxSteps` counts atomic regions between yieldpoints; FailAfter reports a bound crossing while ContinueAfter moves on. A bound crossing is not by itself a proven application liveness violation.
- Failure persistence defaults to printed schedule, optionally files. Preserve original output and compatible scheduler config. Warnings mention atomic-model unsoundness and lazy_static teardown differences; suppressing warnings does not remove their model limits. Keep relevant warnings with campaign results.
- Record test iterations, scheduling steps/bounds and total resource envelope separately. This source does not justify a universal retry count, thread count or execution budget.

### S5: Coyote supported integration and replay

- URLs: https://microsoft.github.io/coyote/get-started/install/ ; https://microsoft.github.io/coyote/get-started/using-coyote/ ; https://microsoft.github.io/coyote/how-to/unit-testing/ ; https://raw.githubusercontent.com/microsoft/coyote/main/LICENSE .
- Small quote fragment: “static state should be appropriately reset”. Current install docs list .NET10/.NET8/.NETStandard2.0 and Windows-specific Framework4.6.2 routes. Match selected package/tool target rather than upgrade an application to a guessed tool floor. MIT verified from actual license.
- Conditional configured integration: `coyote rewrite REWRITING_CONFIG.json`; `coyote test TEST_ASSEMBLY.dll --iterations N --max-steps S --timeout T`; `coyote replay TEST_ASSEMBLY.dll FAILURE.trace`. Values come from actual permitted budget/scenario; selected CLI `-?` determines supported flags. Rewrite config should use existing disposable test-output ownership; default omission of OutputPath overwrites input assemblies.
- Library `TestingEngine` also requires rewritten binaries. Inspect `TestReport`, assert observed failures in the hosting test, and iterate TryEmitTraces results so lazy trace generation actually occurs. CLI defaults can be only one iteration; simply running a command does not establish useful exploration.
- Iterations share process memory, so reset state between them. Recorded trace/replay requires controlled nondeterminism and compatible binaries/configuration. The older general using page mentions a no-repro mode that disables traces; do not bypass an uncontrolled-operation diagnostic and still promise reproducibility.

### S6: Coyote actual modeled boundary

- URL: https://microsoft.github.io/coyote/concepts/binary-rewriting/ (host selection, rewriting scope, timeouts, memory ordering, named handles), actual full page read.
- Small quote fragment: “sequentially consistent”. Rewriter host must match assembly major target. Test and relevant owned production assemblies need control hooks; dependencies treated as pass-through can hide concurrent internals. Current partial-control behavior uses bounded heuristics, so a broad semantics-preservation statement is not a substitute for reading the feature model.
- The current documented systematic mode treats finite nonzero supported waits as infinite, not wall-clock expiry; zero waits and cancellation have specific rules. It explores SC controlled schedules, not JIT/processor weak-memory reorderings. Named cross-process synchronization is outside the modeled process. Its real-thread systematic-fuzzing mode has different time semantics.
- Decision: select Coyote for compatible task/async interactions under its model, not as evidence about arbitrary timeout races, weak memory or cross-process behavior. Report unsupported/uncontrolled events as such rather than mislabeling all as product deadlock. No change to Coyote settings/checks is proposed here.

### S7: Go synctest and existing skill overlap

- URL: https://pkg.go.dev/testing/synctest ; selected page go1.27.3, Time/Blocking/Isolation. BSD-3-Clause is shown on package page. Installed golang/go-testing-advanced SKILL.md read for existing synctest/native fuzz guidance.
- `synctest.Test` creates a bubble and fake clock; Wait waits for other bubble goroutines to become durably blocked. Some channels/condition/waitgroup/sleep operations are durably blocking, but mutex acquisition, I/O and syscalls are not in that category. Outside processes/network remain inappropriate uncontrolled dependencies for this model.
- These primitives help deterministic time/quiescence tests; their documented contract does not enumerate scheduler permutations. An ordinary stress loop, repeated GOMAXPROCS settings or a seed is not a systematic Go schedule controller. No drop-in Go controller was verified by this research. For Barn, inspect existing held-step seams and actual producer boundaries before proposing controlled choice search; do not invent a plugin-wide scheduler.

### S8: CHESS paper and historical applicability

- Primary source/image evidence and artifacts above. A modern skill can reuse the distinction between data inputs, scheduling choices, monitoring and reset. The paper is not a current installation recipe, and its historical Win32/.NET/Singularity wrappers do not imply Go compatibility.
- Scoping/preemption/partial-order methods prioritize an explicitly described model. Their historical success and low-preemption observations do not justify a claim that two or three preemptions always suffice or every race is covered.

## Skill decisions and scope

The following is proposed plugin behavior grounded in the sources, not a mandatory new framework or guaranteed discovery rate.

### Find the actual controllable boundary

Inspect the real producer and guarantee, then map each relevant thread/task/callback, shared resource and state transition to what the chosen controller can expose. Validation/publication, retry after conflict, irreversible side effects and cancellation/completion are candidate boundaries only when the target really has them. Show the relevant operation passes through the control hook; a top-level test wrapper or hidden third-party synchronization may leave the decisive choice uncontrolled (S1,S3,S5-S8).

Pick a small meaningful scenario with an actual safety/effect/progress assertion and supported end-state observation. Vary operation sequences/data and scheduling choices independently where their producers allow it; a fixed held pair samples only its chosen order. Reuse a target's existing test seams and maintained instrumentable types. Adding a universal scheduler, second implementation or generic event protocol is not justified by this skill. Stateful/model/history owners provide their respective generators/oracles.

### Choose the search policy and preserve its meaning

Use bounded systematic search for small controllable scenarios; randomized/PCT search can spend more executions on larger models without exhaustion claims. Record dimensions and limits separately: actors/threads, workload steps, preemptions, permutations/iterations, scheduling steps, model reduction, fairness, wall time and total cost. A coverage plateau can justify a complementary supported scenario, not a universal correctness threshold (S1-S4,S8).

Partial-order reduction depends on actual independence: two operations that touch different objects may still interact through permissions, allocation, validation state or irreversible publication. Rely on the chosen controller's verified dependency model; don't remove schedules based only on different names. A component treated atomically is an explicit omission. A pass is conditional on explored choices and modeled memory/environment, including explicit current-tool limitations.

Limits are evidence too. Truncation, unsupported operations, hidden synchronization, unexplored bounds and incomplete replay are not successful property checks. A step/time limit crossing can be an infrastructure/search boundary or a real progress candidate; the target's fairness/progress contract and actual trace distinguish them. Raising a limit does not fix a product deadlock, and relaxing a diagnostic does not establish replay (S2,S4-S8).

### Preserve a replayable counterexample

Retain original initial-world/setup, workload, exact code/build/config, observer/witness, scheduler strategy/bounds and complete emitted choices/checkpoint/trace. Include any controlled random values and relevant uncontrolled facts. A seed without those choices can reproduce input generation while missing the failing execution. Verify replay under the same controller, then inspect whether the witness follows the real permitted semantics (S1-S6,S8).

Shrink workload and schedule together through the existing representation/controller. After deleting an operation, re-establish valid choices/enabledness and the same violation; ordinal step numbers alone can shift. Preserve original trace if the reduced run changes fault, exhausts a bound or loses setup. General interestingness/reducer mechanics belong to failure-reduction; common-cause classification belongs to triage. No verified generic schedule shrinker for arbitrary runtimes is claimed.

## Concrete advanced applications

Illustrative experiments, not observed product bugs or executed campaigns.

1. **Validation versus publication.** Given a real transactional object guarantee, generate a small valid workload and explore supported pauses around validation, competing mutation and publication/retry. Assert the promised effect/history, not merely absence of a data race. Save exact choices and initial state. Barn already has rich histories and held renewal interleavings; the advance would be exploring additional supported choices and reducing their trace, not relabeling those tests as new. This research uses the source inventory rather than a fresh complete Barn audit.
2. **Cancellation versus completion.** On a compatible .NET task path, explore which controlled operation wins, inspect the documented state/result effect and replay its trace. A Coyote finite-wait model cannot simultaneously establish wall-clock deadline handling; use a separately justified time/fault lane for that guarantee. Don't infer a task-cancellation outcome from an arbitrary short timeout.
3. **Rust lock-free handoff.** Use actual Loom replacement types throughout the data structure and relevant dependencies; state memory-order assumptions and README limitations. A suspected SeqCst-only counterexample requires adjudication against the tool's weakened access modeling, while a green run cannot exclude omitted relaxed-memory behaviors. Keep model and production observations distinct.
4. **A random run with a stuck worker.** Shuttle's total max_time is checked between iterations; a current iteration can remain stuck. A per-iteration step guard and an owned outer envelope protect different resources. Preserve bound crossing and choices, then decide whether a permitted fairness/progress obligation was actually violated. Don't silently call every clipped iteration a healthy test or a proven deadlock.

## Drafter handoff

Suggested references: controlled-boundaries.md (what is observed/controlled and model omissions); runtime-recipes.md (Loom checkpoint feature/bounds, Shuttle APIs/limits, Coyote rewriting/trace/time-memory model, Go synctest distinction); schedule-replay-and-reduction.md (dependent traces and worked scenarios), plus required common-mistakes.md and sources.yaml. Keep entrypoint compact and method-selecting; load runtime detail only for actual selected environment. Public URLs and paper page citations replace local paths in distributed content.

Sources inventory should list S1-S8 actual URLs above, accessed date and used sections. Source snapshots differ across docs/main; don't claim one current release/API matrix without verifying it. No installations, tests or campaigns were run; recipes are source-read conditional shapes. No helper code, framework, universal scheduler, mandatory score or extra approval gate is justified.

Blind evaluation can provide an actual target with existing held interleavings, a contract, a hidden synchronization dependency, a candidate trace needing initial state, and a run terminated at a schedule bound. Ask the evaluator to establish a supported new search dimension and reproduce/reduce a counterexample without revealing the expected mechanism. Evaluate actual artifacts and distinctions; written plans alone do not demonstrate discovery yield. A compatible tiny historical/injected scenario can later test executable scheduling under explicitly authorized resource limits.

## Limits and completion

No Barn mutation/fetch/target run or exhaustive absence audit was performed; its source-inspected baseline comes from the approved domain report. Installed Go skill overlap was directly checked; no broad marketplace novelty claim. The referenced developer researcher role file was absent at its exact path. Guessed Coyote overview/how-to URLs and Shuttle Cargo source page failed; canonical navigation/actual current primary sources supplied the findings, not failures or snippets. Search-result auto-extracted PDF text was not used as paper evidence.

All14 CHESS images were read and canonical reader artifacts inspected/retained externally, with the explicit no-reconcile/process scope above. The repo deliverable is this research report plus the checkpoint-required minimal note addition already reported to parent. No SKILL.md, target action, dependency installation, git operation, host registration, publication, empirical yield or effectiveness claim. Ready for independent drafting.
