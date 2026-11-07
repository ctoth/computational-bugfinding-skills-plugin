---
name: bugfinding-campaign
description: Guides compute-budgeted bugfinding campaigns by finding gaps in existing generators, execution models and correctness oracles. Use when choosing what to test next, extending an established fuzzing setup, or deciding whether more compute will produce useful evidence.
---

# Bugfinding campaign

Choose an experiment that can expose a new violated guarantee, then spend compute according to what the experiment actually observes. Keep discovery, reproduction and triage costs visible; high execution counts alone do not establish useful reach ([OSS-Fuzz integration](https://google.github.io/oss-fuzz/advanced-topics/ideal-integration/), [ClusterFuzz performance](https://google.github.io/clusterfuzz/using-clusterfuzz/workflows/analyzing-fuzzing-performance/)).

## Establish the present capability

Read the actual target revision, enabled build, harness producers and assertion bodies. Record which inputs, initial states, operations, effects, schedules, failures and configurations each existing lane can exercise and observe. Inspect exclusions and rejected cases. Use coverage or reachability tooling only where its documented build/runtime applies; Fuzz Introspector's documented language integrations are not a universal backend ([Fuzz Introspector](https://google.github.io/oss-fuzz/advanced-topics/fuzz-introspector/)).

Count a capability as existing when the inspected implementation provides it. For a target already using valid-program generation, cross-engine result comparison and transaction histories, adding the same mechanisms under new names is not the proposed advance. Choose an uncovered interaction or observation instead: SQLite's joint database-and-SQL mutation is a concrete precedent for searching dimensions together ([SQLite testing, §2 and §4.1.3](https://www.sqlite.org/testing.html)).

## Make one candidate executable

Describe the candidate in the project's existing experiment note; do not introduce a service or mandatory schema. Keep these decisions together, with evidence paths ([OSS-Fuzz integration](https://google.github.io/oss-fuzz/advanced-topics/ideal-integration/), [reproduction](https://google.github.io/oss-fuzz/advanced-topics/reproducing/)):

- **Producer and gap:** actual entrypoint plus the failure space omitted by the baseline.
- **Guarantee and oracle:** governing contract, executable observation and legal/unsupported/inconclusive outcomes.
- **Search:** generated values/state/operations and any controlled schedule, fault or configuration choices.
- **Pilot:** authorized elapsed/worker/resource envelope, replay material and the evidence that will justify the next allocation.

Design observations before multiplying workloads. Elle's traceable objects reveal dependencies that ordinary overwrites can hide; its inference also has explicit limits. A generator that produces more uninformative histories does not repair those limits ([Elle, §§3, 4.3 and 9](https://arxiv.org/abs/2003.10554)). Use `correctness-oracles` for the general contract and a specialist below for its particular model.

| Missing dimension or observation | Relevant specialist |
|---|---|
| Dependent API objects and legal operation sequences | `stateful-property-testing` |
| Runtime-valid programs with required state/effects | `semantic-program-generation` |
| Independent execution comparison or justified run-to-run relation | `semantic-differential-testing`, `metamorphic-testing` |
| Instrumentation/search mechanics or retained search material | `coverage-guided-fuzzing`, `corpus-evolution` |
| Memory-access diagnostics or controlled scheduling choices | `native-memory-instrumentation`, `race-detection-campaigns`, `schedule-exploration` |
| Concurrent object or transaction guarantees | `linearizability-checking`, `transactional-history-testing` |
| Deployment faults, controlled environment or recovery boundaries | `distributed-fault-testing`, `deterministic-simulation`, `crash-consistency-testing` |
| Hard path constraints or bounded invariants | `symbolic-concolic-execution`, `bounded-model-checking` |
| Resource growth, progress, build interactions or numerical accuracy | `resource-complexity-testing`, `liveness-testing`, `configuration-differential-testing`, `numerical-oracles` |

The table routes this pack's responsibilities; it does not establish that a named tool supports the target. Read only the selected specialist and its applicable references. Use `harness-sensitivity` to obtain evidence that a new oracle reaches and rejects representative violations, preferably through existing regressions or controls. Keep this proportional to the experiment, not a recurring approval round ([SQLite testing, §7.6](https://www.sqlite.org/testing.html)).

## Allocate from pilot evidence

Run within the authorized envelope. Check whether target code and the intended property are exercised; distinguish unavailable paths from reachable paths that mutation has not solved. Change the experiment when a missing producer, semantic prerequisite or observation is the limiting factor ([Fuzz Introspector](https://google.github.io/oss-fuzz/advanced-topics/fuzz-introspector/)). For diagnoses, read [pilot diagnosis](references/pilot-diagnosis.md).

Extend an informative lane when its evidence justifies more search. Compare complementary lanes where their search mechanisms differ; AFL++ documents varied cooperating configurations rather than only identical workers ([AFL++ depth, Using multiple cores](https://aflplus.plus/docs/fuzzing_in_depth/)). Use actual time, workers and resource limits, not a universal duration or core count. Keep runtime flags in the specialist; per-input timeout, campaign duration and memory limits are different controls ([libFuzzer options](https://llvm.org/docs/LibFuzzer.html#options)).

Keep raw counters for property evaluations and semantic/code reach, raw candidates and reproduced findings, duplicates and unknowns, and setup/execution/reduction/triage cost. Do not collapse them into an invented productivity score. Where comparative claims matter, use matched conditions and repeated trials with variability; FuzzBench reports distributions rather than a single lucky run ([FuzzBench report](https://google.github.io/fuzzbench/reference/report/)).

Preserve original inputs, starting state, source/build/configuration, instrumentation, raw outputs and replay choices before summarizing. A testcase can depend on sanitizer and architecture; a seed alone is not that complete artifact ([OSS-Fuzz reproduction](https://google.github.io/oss-fuzz/advanced-topics/reproducing/)). Route candidates to `failure-reduction` and `evidence-based-triage`; leave unreliable or unresolved findings visible rather than quietly counting or discarding them ([ClusterFuzz triage](https://google.github.io/clusterfuzz/using-clusterfuzz/workflows/triaging-new-crashes/)).

## Finish the allocation decision

Record continue, change dimension, reproduce/reduce/triage, or stop, with the observed reason and remaining space. A plateau motivates diagnosis; it proves neither correctness nor that another tool will help. Preserve zero findings as a bounded result. A queue of unprocessed candidates can justify spending the next tranche on evidence rather than generation ([ClusterFuzz performance](https://google.github.io/clusterfuzz/using-clusterfuzz/workflows/analyzing-fuzzing-performance/)).

Return the tested guarantee, actual budget, reached behavior, evidence paths, classified findings and next decision. Describe user-visible effects where established; keep a possible cause separate from a demonstrated violation. For a worked allocation and record, read [campaign example](references/campaign-example.md); for misleading shortcuts, read [common mistakes](references/common-mistakes.md).

Invocation preserves the user's existing scope and execution rules. It does not itself authorize target changes, installations, cloud spending, production fault injection or external publication.
