# Research: liveness-testing

Date: 2026-11-07

## State

Research complete for drafter handoff. This is the only owned repository output. Literature uses paper-reader and direct page images only. No target execution, installation, target mutation, staging, commit or publication. Tool commands below are conditional examples, not executed validation of a target.

## Evidence ledger

Inspecting actual progress/fairness/environment contracts and supported temporal/progress observers. Existing paper-reader artifacts and primary tool source will ground bounded examples; no deadline-as-proof or copied-production-model claim.

## Reused paper-reader image evidence

Directly reread existing CHESS (Musuvathi et al., OSDI2008) printed pp.8-10 as local images page-007 through page-009, and FoundationDB (Zhou et al., SIGMOD2021) p.9 as image page-008 on 2026-11-07. Existing task collections already contain full page-image reads and reader artifacts from their owning researchers; no new ingestion or collection mutation. No extracted paper text read, no process/tag/reconcile workflow.

- CHESS pp.8-9: fairness assumptions determine which nonterminating schedules are meaningful. Environment interference can produce apparent deadlock; the observer must establish actual enabledness/blocking. Yield/sleep-based test perturbations can conflict with the scheduler's fairness assumptions. The historical tool's particular fair strategy is not a universal present-runtime guarantee.
- CHESS p.10: empty enabled-task sets support its deadlock monitor; liveness requires fair termination reasoning and a real progress condition. A high execution bound is a bounded observation, not an unqualified mathematical proof of starvation.
- FDB p.9: recoverability checks first restore modeled hardware to an environment permitting recovery, then observe eventual recovery. Excessive faults can trap execution in a shallow state-space. Useful compute can explore the fault distribution/healthy regime, not simply add more failures or more time.

Primary paper URLs: https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osdi2008-CHESS.pdf and https://www.foundationdb.org/files/fdb-paper.pdf . Existing local artifacts are provenance only, not future distributed dependencies.

## Verified source identities

Read-only git ls-remote established Coyote main2202e75a861f4e8a63149366c2e41ea21d73ae54, TLC masterd8fb231de4e4b5d02c1b2ed1ac759c086f694021 and Go masterdcc06a82727b447270b1a58cc5f86b49736e317c. Actual GitHub tree responses located the liveness documentation/source paths before fetching them. Pins identify evidence snapshots, not installed/released support claims. Referenced developer researcher role file was absent at its exact path.

## Primary findings saved progressively

### Coyote real obligation and observer boundaries

Pinned base https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/ . Read docs/how-to/liveness-checking.md, docs/concepts/specifications.md; actual Source/Core/Specifications/Specification.cs, Monitors/TaskLivenessMonitor.cs and selected Monitor.cs regions; Source/Core/Runtime/CoyoteRuntime.cs liveness callers; Source/Core/Configuration.cs thresholds; actual TaskLivenessMonitorTests.cs and UnfairExecutionTests.cs. Accessed2026-11-07.

- The hot/cold monitor represents a real pending obligation and its discharge, distinct from the scheduler. Termination with a hot monitor is checked separately from a long hot prefix. Task helper requires TaskStatus.RanToCompletion; valid cancellation/fault under another API contract needs a fitting obligation monitor rather than assuming any terminal task satisfies this helper. Exact source fragment: `TaskStatus.RanToCompletion` (TaskLivenessMonitor.cs).
- Actual runtime checks temperature only when liveness checking is enabled and Scheduler.IsIterationFair (CoyoteRuntime.cs around870-873). The monitor increments only while ActiveState.IsHot and threshold>0 (Monitor.cs616-628), resets on entering cold (around583-585); warm states do not increase this counter. Do not turn broad documentation prose into a complete hot/warm cycle-checking claim.
- Threshold exhaustion is a potential-liveness heuristic, not a wall-time bound or proof of an infinite execution. Configuration source says threshold0 disables the check; max-fair scheduling steps and threshold are separate quantities. Actual closed finite obligations can supply stronger bounded evidence when the contract requires completion before the test ends. Preserve exact search strategy/fairness, step bounds, temperature, observer state and trace.
- Pin/version matters: how-to prose contains example-derived10N/5N heuristics and calls portfolio schedulers fair while also naming an unfair prioritization strategy. Use selected source/actual reported fair-versus-unfair iteration evidence instead of a universal scheduler taxonomy. No runtime test was executed here.

### TigerBeetle real liveness-search change

Primary dated account https://tigerbeetle.com/blog/2023-07-06-simulation-testing-for-liveness/ (matklad,2023-07-06), read actual page. Exact fragment: “making those failures permanent”. Uniform faults/restarts can repair a livelock before a progress oracle notices it. Its actual target guarantee requires a chosen healthy quorum to progress despite non-core failures; their liveness mode heals that core and freezes non-core failures, then observes core transactions. An alternating repair request pattern is a concrete historical nonprogress example. This is a target-specific failure model, not a universal quorum size, deadline or a promise of current bugs.

Decision: derive the recoverable/healthy regime from the actual contract, then hold it stable long enough to observe required progress. More retries, healing or restarts can erase the failure state. A real retry-counter/durable-state/protocol witness is stronger than an arbitrary timeout alone. Detailed simulator/runtime controls belong to deterministic-simulation.

### TLC temporal checking and correspondence

Read pinned [README](https://raw.githubusercontent.com/tlaplus/tlaplus/d8fb231de4e4b5d02c1b2ed1ac759c086f694021/README.md), [USE](https://raw.githubusercontent.com/tlaplus/tlaplus/d8fb231de4e4b5d02c1b2ed1ac759c086f694021/USE.md), selected TLC.java, TLCGlobals.java, ModelChecker.java and LiveWorker.java regions under tlatools/org.lamport.tlatools/src/tlc2/, and official model documentation below. These are code/model-checking sources, not unread-paper claims.

- The actual [LiveHourClock.tla example](https://raw.githubusercontent.com/tlaplus/tlaplus/d8fb231de4e4b5d02c1b2ed1ac759c086f694021/tlatools/org.lamport.tlatools/test-model/examples/SpecifyingSystems/Liveness/LiveHourClock.tla) attaches weak fairness to its clock action and states temporal progress properties separately. Its matching configuration intentionally checks a false settling property too; copying the whole example as a passing target test would be wrong. Exact fragment: `WF_hr(HCnxt)`.
- [Model overview](https://raw.githubusercontent.com/tlaplus/tlaplus/d8fb231de4e4b5d02c1b2ed1ac759c086f694021/toolbox/org.lamport.tla.toolbox.doc/html/model/overview-page.html) distinguishes behavior specification, fairness, invariant and temporal property. A normal allowed terminal state differs from an unintended no-successor state. A model must represent actual admission, completion/cancellation and environment actions; an independent model counterexample initially establishes a model defect or candidate implementation defect.
- [ModelChecker.java](https://raw.githubusercontent.com/tlaplus/tlaplus/d8fb231de4e4b5d02c1b2ed1ac759c086f694021/tlatools/org.lamport.tlatools/src/tlc2/tool/ModelChecker.java), selected final-check path and no-successor branch: successful state exploration is followed by final temporal checking. Do not call a timed-out temporal check a completed proof. [LiveWorker.java](https://raw.githubusercontent.com/tlaplus/tlaplus/d8fb231de4e4b5d02c1b2ed1ac759c086f694021/tlatools/org.lamport.tlatools/src/tlc2/tool/liveness/LiveWorker.java), class comment/behavior-graph processing, checks accepting cycles with temporal obligations; a repeated application log line is insufficient evidence of such a cycle.
- [State constraints](https://raw.githubusercontent.com/tlaplus/tlaplus/d8fb231de4e4b5d02c1b2ed1ac759c086f694021/toolbox/org.lamport.tla.toolbox.doc/html/model/spec-options-page.html) prune exploration, so record their effect on possible progress. [Symmetry documentation](https://raw.githubusercontent.com/tlaplus/tlaplus/d8fb231de4e4b5d02c1b2ed1ac759c086f694021/toolbox/org.lamport.tla.toolbox.doc/html/model/model-values.html), final warning, says symmetry sets must not be used for liveness: they can miss errors or produce nonexistent errors. Exact fragment: “Symmetry sets should not be used”.
- [Distributed mode](https://raw.githubusercontent.com/tlaplus/tlaplus/d8fb231de4e4b5d02c1b2ed1ac759c086f694021/toolbox/org.lamport.tla.toolbox.doc/html/model/distributed-mode.html), limitations, excludes liveness checking. Increasing distributed TLC workers is therefore not the supported way to buy this skill's temporal search. Actual [TLC.java](https://raw.githubusercontent.com/tlaplus/tlaplus/d8fb231de4e4b5d02c1b2ed1ac759c086f694021/tlatools/org.lamport.tlatools/src/tlc2/TLC.java) parser makes `-deadlock` disable deadlock checking; do not suggest it as enabling detection.
- USE documents JSON trace dumping/loading for model-based testing and trace validation. These can help test correspondence; they do not establish that an authored abstraction contains every real implementation behavior. Reuse an existing relevant model and mapping where available. Do not create a second production state machine just to make a temporal property pass.

### Go quiescence support has a narrower contract

Read [selected go1.27.3 package documentation](https://pkg.go.dev/testing/synctest) and [pinned package source](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/testing/synctest/synctest.go), package comment and Test/Wait behavior. The selected documentation release and development source snapshot are distinct evidence identities; inspect the target's go.mod/toolchain before choosing an API.

The bubble waits for its goroutines to exit; fake time advances when all are durably blocked. Wait observes other bubble goroutines becoming durably blocked. Bubble-owned channels/select, supported condition/wait-group operations and sleeps can participate; mutex locking, I/O and system calls do not generally establish durable blocking. Exact source fragment: “durably blocked”. A healthy service waiting for future input may be quiescent; an admitted request waiting forever for an impossible response may be defective. The obligation and environment decide which. A CPU loop may prevent quiescence/fake-clock advancement and needs bounded external execution protection, not another fake timer inside the same bubble. Nothing in this API is a schedule-enumeration guarantee or a starvation proof.

## Source inventory for drafting and sources.yaml

Access date for all entries: 2026-11-07. Preserve immutable URLs above and the pinned base below; resolve named paths into full URLs when authoring the skill. Keep source fragments short and tied to a decision, rather than appending a bibliography to unsupported instructions.

| Source family | Actual inspected sections and relevance | Prerequisites and attribution |
| --- | --- | --- |
| CHESS OSDI2008, primary PDF above | Direct page images pp.8-10: fairness, blocking/environment interference, practical termination bound | Historical research, not current runtime compatibility; no source-code copying |
| FDB SIGMOD2021, primary PDF above | Direct p.9 image: restored recoverable regime and simulation boundary | Historical research, not a portable simulator or measured yield claim |
| Coyote liveness how-to | Hot/cold, fair strategies, temperature, sample commands | https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/docs/how-to/liveness-checking.md ; actual runtime source resolves prose limits |
| Coyote specification implementation | Specification.cs; Monitors/TaskLivenessMonitor.cs and Monitor.cs; CoyoteRuntime.cs selected callers | Pinned base above; success-specific helper and fair-iteration temperature checking |
| Coyote configuration and actual tests | Configuration.cs selected defaults/setters; Tests/Tests.BugFinding/Specifications/TaskLivenessMonitorTests.cs; Tests/Tests.Actors.BugFinding/Specifications/Liveness/UnfairExecutionTests.cs | Replay-capable examples and fairness-sensitive tests; not a universal step threshold |
| Coyote setup/CLI | docs/get-started/install.md and docs/get-started/using-coyote.md | At snapshot docs support .NET10/.NET8/.NETStandard2 and Windows .NETFramework4.6.2; actual existing target integration controls. Coyote LICENSE says MIT |
| TLC temporal engine/docs/examples | Linked exact paths above, not entire source audit | README/USE require Java11+; existing tla2tools.jar and relevant spec/config. LICENSE says MIT; README marks Toolbox unmaintained |
| Go synctest | Selected release docs and pinned source above | Existing fitting Go toolchain and testing package; Go LICENSE preserves copyright/conditions, source headers say BSD-style |
| TigerBeetle dated primary account | Healthy-core mode and historical repair livelock | Blog evidence, not a current bug claim or exported universal fault policy |

License files were fetched at the same pins and their initial grant/conditions read. No upstream implementation was copied into this report. No installation was attempted. Development snapshots do not establish that a released binary implements the exact inspected source.

## Recommended behavioral guidance

The following is proposed skill guidance derived from the evidence above; these are engineering decisions, not quotations or assertions that all tools implement them.

1. Start with a real admitted unit of work: request ID, queued item, transaction, lock acquisition or recovery phase. Identify the actual producer and completion/abort/cancellation event. Write what must eventually happen, when the obligation starts, and which outcomes legitimately discharge it. Aggregate throughput can hide one starved request; attempts and heartbeats can conceal no semantic progress.
2. Record admissible conditions: scheduler fairness actually promised, eventual message delivery if promised, availability, retry policy, time semantics, capacity and external service responses. Unconditional delivery or fair lock acquisition must not be invented. If the environment can reject or postpone forever, a failing progress run needs a stronger admitted contract or is inconclusive.
3. Choose the existing fitting route. Observe actual runtime operations using an existing scheduler/monitor; use Go synctest for fitting fake-time/quiescence assertions; use TLC for an existing temporal model with an explicit implementation mapping. Hand implementation of scheduling to schedule-exploration and simulator infrastructure to deterministic-simulation.
4. Spend compute on admissible schedules, admission/retry/backoff inputs, timing relationships and persistent fault regimes. Preserve a healthy/recoverable regime where the contract promises progress. Do not let cleanup/restarts silently repair the state before the observer samples it. Increase independent search diversity and meaningful depth based on observed runs; do not substitute an invented deadline for an eventuality.
5. Classify evidence precisely. An empty enabled set with pending required work and complete environmental accounting can witness deadlock. A model accepting lasso satisfying the recorded fairness constraints can witness model liveness failure. A bounded real deadline violation is a target defect only when that deadline is actually promised. A hot threshold, exhausted steps or harness wall timeout is a candidate needing triage, not an infinite-execution proof. Expected quiescence with no pending obligation is healthy.
6. Save work identity and obligation state, thread/task stacks and wait dependencies, enabled operations, virtual and wall clocks, scheduler/fault choices, relevant durable state, strategy/fairness/bounds, build/tool versions and replay artifacts. Reduce while preserving the same obligation and admissible environment. Removing the only fair scheduling opportunity or recovery condition changes the claim. LLM triage may connect traces to source and group candidates; replay and raw witnesses remain the evidence.

### Concrete decisions the skill should enable

- **Retry livelock:** a durable request remains pending while repair attempts alternate among replicas. The environment guarantees an available healthy core. Keep that core available and preserve failed outsiders rather than restarting everyone. Record request/repair-target evolution. Distinguish the TigerBeetle historical mechanism from a newly reproduced target finding.
- **Task completion:** a valid cancellation is incorrectly checked by a helper requiring successful completion. Inspect the real target contract and use the correct discharge event. A Coyote hot-state failure can be an observer defect; changing the observer is justified by actual cancellation semantics, not by wanting green output.
- **Go worker:** after admitted work, workers block waiting for an event the producer can no longer send. Trace actual producers and bubble blocking before classifying. A bubble with no admitted work may be intentionally idle. A spinning worker can prevent fake-time advance; a fake timeout inside that bubble supplies no independent bound.
- **TLC result:** exploration finishes but temporal processing is interrupted, or symmetry/state pruning changes the admissible behaviors. Report incomplete checking or configuration limits. A temporal counterexample in a simplified model becomes an implementation finding only after mapping its actions/state and replaying or otherwise witnessing the real path.

## Scope, baseline and evaluation handoff

Barn context from the parent-provided research baseline already includes structured Go fuzzing, differential checks, scheduler controls, snapshots and rich histories. This report does not claim a new Barn audit or empirical bug yield. The additional capability is obligation-specific progress search with explicit fairness/environment accounting and appropriate runtime/model witnesses. This is distinct from simply extending a watchdog timeout, adding ticks or counting retries.

Keep detailed schedule enumeration, simulator implementation, resource limits, oracle construction and failure reduction in their owning skills. This skill chooses and interprets progress witnesses and hands off the necessary controls. Useful optional references: progress-contracts.md (actual producer/discharge and fairness examples), runtime-and-model-routes.md (conditional integration/limits), witnesses-and-replay.md (deadlock/livelock/starvation/quiescence evidence). Avoid a mandatory universal monitor framework or production-model copy.

For a blind evaluation, provide realistic source plus traces with undisclosed outcomes: one admitted request starved despite the promised healthy regime, one healthy idle service, one run denied progress by an inadmissible environment, one canceled task that legitimately discharges its obligation, and one incomplete temporal-model check. Require the agent to locate producers/contracts, select a fitting observer/search, distinguish verified defect from candidate/inconclusive/healthy results and retain raw evidence. Do not tell it which trace contains the bug or grade it on repeating these labels. Compare observable artifacts and source-correct contract decisions; no bug-yield numbers are claimed here.

### Conditional native command examples

Only after inspecting the existing target/tool integration, and within authorized execution scope:

```text
coyote rewrite EXISTING_REWRITE_CONFIG.json
coyote test EXISTING_TEST.dll --iterations N --max-steps S
coyote replay EXISTING_TEST.dll FAILURE.trace
java -cp EXISTING_tla2tools.jar tlc2.TLC -config EXISTING.cfg EXISTING.tla
go test ./ACTUAL_PACKAGE -run '^TestActualProgress$' -count=1 -timeout=ACTUAL_EXECUTION_BUDGET
```

Coyote rewrite/test/replay forms and flags above come from the pinned using-coyote document; inspect current help for a matching installed artifact. Its test entry method must carry the actual systematic-testing attribute, and iteration-shared static state must be reset. The liveness-temperature option is documented in the liveness/specification pages; select it from the measured workload/actual obligation, not a universal constant. TLC command form comes from USE/TLC parser; do not add `-deadlock` or symmetry sets to enable detection. The Go command is an illustrative focused existing test with an external execution budget, not a contract deadline or an authorization to run it now. No command was executed against a target.

## Completion and unresolved evidence

Complete research handoff; report only. No claim of current target compatibility, bug discovery, exhaustive runtime exploration or implementation liveness proof. No new dedicated liveness paper was represented as read: CHESS/FDB image evidence covers the paper-derived decisions, supplemented by inspected source-native tools and the dated primary implementation account. Future claims about a specific target need its actual contracts and fitting build. One read-only remote probe returned exit1 with no output; it supplied no evidence and no cause is inferred. Relevant source was obtained through successful primary fetches instead.
