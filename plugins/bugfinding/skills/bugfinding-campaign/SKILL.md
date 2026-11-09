---
name: bugfinding-campaign
description: Guides compute-budgeted bugfinding campaigns by finding gaps in existing generators, execution models and correctness oracles. Use when choosing what to test next, extending an established fuzzing setup, or deciding whether more compute will produce useful evidence.
---

# Bugfinding campaign

Choose an experiment that can expose a new violated guarantee, then spend compute according to what the experiment actually observes. Keep discovery, reproduction and triage costs visible. Speed is one listed performance factor beside "Code coverage should grow over time" and resolving blocking issues, and a useful target "must have good coverage in the code that it is testing"; execution counts alone do not establish useful reach ([OSS-Fuzz integration, Coverage](https://raw.githubusercontent.com/google/oss-fuzz/156f862e5976b3d23828230a0a5b4fef54074d32/docs/advanced-topics/ideal_integration.md), [ClusterFuzz performance, Performance factors](https://raw.githubusercontent.com/google/clusterfuzz/77bbad2432fb931906c523786defac928d12afdb/docs/using-clusterfuzz/workflows/analyzing-fuzzer-performance.md)).

## Establish the present capability

Read the actual target revision, enabled build, harness producers and assertion bodies. Record which inputs, initial states, operations, effects, schedules, failures and configurations each existing lane can exercise and observe. Inspect exclusions and rejected cases. Use coverage or reachability tooling only where its documented build/runtime applies; Fuzz Introspector documents reports "For projects written in C/C++, Python and Java", each with its own build tooling, so it is not a universal backend ([Fuzz Introspector, overview and Differences in build tooling](https://raw.githubusercontent.com/google/oss-fuzz/156f862e5976b3d23828230a0a5b4fef54074d32/docs/advanced-topics/fuzz_introspector.md)). For a JavaScript or TypeScript project, read the [JS lane inventory](references/campaign-example.md#inventorying-a-javascript-or-typescript-project).

Count a capability as existing when the inspected implementation provides it. For a target already using valid-program generation, cross-engine result comparison and transaction histories, adding the same mechanisms under new names is not the proposed advance. Choose an uncovered interaction or observation instead: SQLite's dbsqlfuzz "mutates both the SQL input and the database file at the same time" and found faults "missed by prior fuzzers", a concrete precedent for searching dimensions together. It is "a proprietary fuzz tester": borrow the mechanism, not an assumed public tool ([SQLite testing, §2 and §4.1.3](https://www.sqlite.org/testing.html)).

## Make one candidate executable

Describe the candidate in the project's existing experiment note; do not introduce a service or mandatory schema. Keep these decisions together, with evidence paths. OSS-Fuzz asks that a target "make at least some progress" in a short local run, and reproduction needs the build that matches the report ([OSS-Fuzz integration, Fuzz Target](https://raw.githubusercontent.com/google/oss-fuzz/156f862e5976b3d23828230a0a5b4fef54074d32/docs/advanced-topics/ideal_integration.md), [reproduction, Build the image and the fuzzers](https://raw.githubusercontent.com/google/oss-fuzz/156f862e5976b3d23828230a0a5b4fef54074d32/docs/advanced-topics/reproducing.md)):

- **Producer and gap:** actual entrypoint plus the failure space omitted by the baseline.
- **Guarantee and oracle:** governing contract, executable observation and legal/unsupported/inconclusive outcomes.
- **Search:** generated values/state/operations and any controlled schedule, fault or configuration choices.
- **Pilot:** authorized elapsed/worker/resource envelope, replay material and the evidence that will justify the next allocation.

Design observations before multiplying workloads. Elle's traceable objects reveal dependencies that ordinary overwrites hide, because blind writes to a register "destroy history". Its inference also has explicit limits: the checker is sound and "comes close to guaranteeing completeness", and "Our approach ignores predicates and deals only in individual objects". A generator that produces more uninformative histories does not repair those limits ([Elle, §§3, 4.3 and 9](https://arxiv.org/abs/2003.10554)). Use `correctness-oracles` for the general contract and a specialist below for its particular model.

| Missing dimension or observation | Relevant specialist |
|---|---|
| Dependent API objects and legal operation sequences | `stateful-property-testing` |
| Reachable browser or React UI states without an operation model, with per-state oracles and path replay | `ui-state-exploration` |
| Runtime-valid programs with required state/effects | `semantic-program-generation` |
| Independent execution comparison or justified run-to-run relation | `semantic-differential-testing`, `metamorphic-testing` |
| Instrumentation/search mechanics or retained search material | `coverage-guided-fuzzing`, `corpus-evolution` |
| Memory-access diagnostics or controlled scheduling choices | `native-memory-instrumentation`, `race-detection-campaigns`, `schedule-exploration` |
| Concurrent object or transaction guarantees | `linearizability-checking`, `transactional-history-testing` |
| Deployment faults, controlled environment or recovery boundaries | `distributed-fault-testing`, `deterministic-simulation`, `crash-consistency-testing` |
| Hard path constraints or bounded invariants | `symbolic-concolic-execution`, `bounded-model-checking` |
| Resource growth, progress, build interactions or numerical accuracy | `resource-complexity-testing`, `liveness-testing`, `configuration-differential-testing`, `numerical-oracles` |

The table routes this pack's responsibilities; it does not establish that a named tool supports the target. Read only the selected specialist and its applicable references. Use `harness-sensitivity` to obtain evidence that a new oracle reaches and rejects representative violations, preferably through existing regressions or controls; SQLite's mutation testing "verifies that the test suite catches the mutation" ([SQLite testing, §7.6](https://www.sqlite.org/testing.html)). Keep this proportional to the experiment, not a recurring approval round.

## Allocate from pilot evidence

Run within the authorized envelope. Check whether target code and the intended property are exercised; distinguish unavailable paths from reachable paths that mutation has not solved. Fuzz Introspector compares each fuzzer's "static reachability potential" against dynamic coverage for this distinction. Change the experiment when a missing producer, semantic prerequisite or observation is the limiting factor ([Fuzz Introspector, overview](https://raw.githubusercontent.com/google/oss-fuzz/156f862e5976b3d23828230a0a5b4fef54074d32/docs/advanced-topics/fuzz_introspector.md)). For diagnoses, read [pilot diagnosis](references/pilot-diagnosis.md).

Extend an informative lane when its evidence justifies more search. Compare complementary lanes where their search mechanisms differ; AFL++ says "For every secondary fuzzer there should be a variation" ([AFL++ depth, §3.c Using multiple cores](https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/docs/fuzzing_in_depth.md)). Use actual time, workers and resource limits, not a universal duration or core count. Keep runtime flags in the specialist; per-input timeout, campaign duration and memory limits are different controls ([libFuzzer 23.1.0 options](https://releases.llvm.org/23.1.0/docs/LibFuzzer.html#options)).

Keep raw counters for property evaluations and semantic/code reach, raw candidates and reproduced findings, duplicates and unknowns, and setup/execution/reduction/triage cost. Do not collapse them into an invented productivity score. Where comparative claims matter, use matched conditions and repeated trials with variability; FuzzBench reports "the number of trials, mean, median, standard" deviation and the "distribution of the reached coverages" rather than a single lucky run ([FuzzBench report, Per-benchmark summary](https://raw.githubusercontent.com/google/fuzzbench/3234e151d70f6093272a9b4155e68ee57faf986c/docs/reference/report.md)).

Preserve original inputs, starting state, source/build/configuration, instrumentation, raw outputs and replay choices before summarizing. An OSS-Fuzz testcase "contains the bytes that were fed to the" target, and some bugs "are reproducible only in 32 bit mode or only in 64 bit mode" under the reported sanitizer; a seed alone is not that complete artifact ([OSS-Fuzz reproduction, Fuzz target bugs and Build the image and the fuzzers](https://raw.githubusercontent.com/google/oss-fuzz/156f862e5976b3d23828230a0a5b4fef54074d32/docs/advanced-topics/reproducing.md)). Route candidates to `failure-reduction` and `evidence-based-triage`; leave unreliable or unresolved findings visible rather than quietly counting or discarding them. ClusterFuzz filters on reliability of reproduction and keeps statistics "on how often issues occur, and under what conditions" ([ClusterFuzz triage, Filtering testcases and Crash statistics](https://raw.githubusercontent.com/google/clusterfuzz/77bbad2432fb931906c523786defac928d12afdb/docs/using-clusterfuzz/workflows/triaging-new-crashes.md)).

## Finish the allocation decision

Record continue, change dimension, reproduce/reduce/triage, or stop, with the observed reason and remaining space. A plateau motivates diagnosis; it proves neither correctness nor that another tool will help. Preserve zero findings as a bounded result. A queue of unprocessed candidates can justify spending the next tranche on evidence rather than generation. For coverage-guided libFuzzer or AFL targets, ClusterFuzz advises that when a target finds many new crashes, "fixing them is probably more important than analyzing performance" ([ClusterFuzz performance, When to analyze fuzz target performance](https://raw.githubusercontent.com/google/clusterfuzz/77bbad2432fb931906c523786defac928d12afdb/docs/using-clusterfuzz/workflows/analyzing-fuzzer-performance.md)).

Return the tested guarantee, actual budget, reached behavior, evidence paths, classified findings and next decision. Describe user-visible effects where established; keep a possible cause separate from a demonstrated violation. For a worked allocation and record, read [campaign example](references/campaign-example.md); for misleading shortcuts, read [common mistakes](references/common-mistakes.md).

Invocation preserves the user's existing scope and execution rules. It does not itself authorize target changes, installations, cloud spending, production fault injection or external publication.
