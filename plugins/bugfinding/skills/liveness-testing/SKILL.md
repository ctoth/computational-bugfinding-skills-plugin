---
name: liveness-testing
description: Guides computational searches for starvation, deadlock, livelock and unbounded retries. Use when admitted work fails to progress, recovery appears stuck, or a watchdog timeout needs an obligation-specific oracle and reproducible evidence.
---

# Liveness testing

Find a real pending obligation and an admissible execution that prevents its required progress. Fairness and environmental enabledness determine whether apparent nontermination is meaningful; a long run alone is weaker evidence ([CHESS, §§4.2–4.3 and 5](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osdi2008-CHESS.pdf)).

## Define the progress claim

Read the actual producer, enabled configuration and completion/cancellation semantics. Name the admitted request or recovery phase, its start, and every permitted discharge event. Choose the monitor from that contract: Coyote's task helper requires successful completion, so it does not implement a contract allowing cancellation merely because both are terminal task states ([task helper, IsSatisfied](https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/Source/Core/Specifications/Monitors/TaskLivenessMonitor.cs)). Read [progress contracts](references/progress-contracts.md) for concrete cases.

State the scheduler, delivery, availability and retry assumptions the target actually promises. Preserve a recoverable regime where progress is required: FoundationDB restores modeled hardware to a state permitting recovery before checking it, and TigerBeetle's healthy-core regime can expose failures that repeated healing/restarts erase ([FDB, p.9](https://www.foundationdb.org/files/fdb-paper.pdf), [TigerBeetle, Teaching the VOPR](https://tigerbeetle.com/blog/2023-07-06-simulation-testing-for-liveness/)). Do not invent eventual delivery or a deadline to make the claim decidable.

## Choose a fitting search and observer

Use existing runtime/control seams for actual work; use an existing temporal model only with an explicit mapping to implementation state/actions. TLC distinguishes a fairness-bearing behavior specification from the property being checked; its clock example states the fairness condition separately ([LiveHourClock, LSpec](https://raw.githubusercontent.com/tlaplus/tlaplus/d8fb231de4e4b5d02c1b2ed1ac759c086f694021/tlatools/org.lamport.tlatools/test-model/examples/SpecifyingSystems/Liveness/LiveHourClock.tla)). Detailed scheduling and environmental control belong to `schedule-exploration` and `deterministic-simulation`; read [runtime and model routes](references/runtime-and-model-routes.md) for supported operation.

Spend compute on obligation-relevant sequences, interleavings, retry state and admissible persistent faults. Preserve the state that causes nonprogress instead of resetting it out of the experiment; TigerBeetle's historical repair resonance disappeared when restart reset the retry counter ([TigerBeetle, Resonance](https://tigerbeetle.com/blog/2023-07-06-simulation-testing-for-liveness/)). Use `stateful-property-testing` for dependent workload construction and `bugfinding-campaign` for allocation.

## Interpret the witness before attributing a bug

Separate healthy idle quiescence, exhausted search, heuristic temperature, promised deadline violation, supported deadlock evidence and a fair temporal-model counterexample. Coyote checks temperature on fair iterations and only increments a hot monitor's counter; Go synctest observes durable blocking rather than enumerating schedules ([Coyote runtime](https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/Source/Core/Runtime/CoyoteRuntime.cs), [Monitor, IsLivenessThresholdExceeded](https://raw.githubusercontent.com/microsoft/coyote/2202e75a861f4e8a63149366c2e41ea21d73ae54/Source/Core/Specifications/Monitors/Monitor.cs), [synctest, Time and Blocking](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/testing/synctest/synctest.go)). Read [witnesses and replay](references/witnesses-and-replay.md).

Keep obligation identity, admissible environment, actual producer/wait dependencies, observer state, choices, tool/build/configuration and bounds with the original trace. Reduce the workload and choices while retaining those premises; CHESS documents environmental interference and imperfect replay as limits on observed enabledness and search ([CHESS, §4.2](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/osdi2008-CHESS.pdf)). Use `failure-reduction` and `evidence-based-triage` for their separate mechanics.

Return the promised progress, reached pending work, admitted assumptions, observed failure and replay evidence, tested scope and unresolved alternatives. A TLC exploration result is incomplete until the required final liveness check completes ([ModelChecker, modelCheck](https://raw.githubusercontent.com/tlaplus/tlaplus/d8fb231de4e4b5d02c1b2ed1ac759c086f694021/tlatools/org.lamport.tlatools/src/tlc2/tool/ModelChecker.java)); a model witness still needs implementation correspondence. For source-backed corrections to misleading shortcuts, read [common mistakes](references/common-mistakes.md).

Invocation preserves existing execution authority; it does not grant target edits, installations, external fault injection or publication.
