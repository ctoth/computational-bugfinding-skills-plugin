# Diagnose the pilot before buying more search

Use this table on observed pilot artifacts. These are campaign design choices grounded in the cited mechanisms, not a proven optimal allocation policy.

| Observed evidence | Next useful action | Evidence needed to continue |
|---|---|---|
| Desired API has no call path from this harness | Find an existing producer or suitable harness entrypoint | Source/configuration path showing the desired code can execute; static potential and dynamic execution are different ([Fuzz Introspector](https://google.github.io/oss-fuzz/advanced-topics/fuzz-introspector/)). |
| Input accepts/compiles, but dependent operations mostly reject | Inspect missing state, identities, types and permissions; generate prerequisites with operations | Successful visits to the intended behavior, not merely parsing; joint state/input search has a real precedent ([SQLite §2 and §4.1.3](https://www.sqlite.org/testing.html)). |
| Interesting operations execute, but only crash/no-crash is checked | Derive a contract-backed result/effect/recovery oracle | An observable contradiction or a representative violation the oracle rejects; wrong results need their own checks ([SQLite §4.1.4](https://www.sqlite.org/testing.html)). |
| Histories omit information needed by the checker | Change workload values/observations or use a fitting oracle | Identify which dependencies can actually be inferred and preserve the witness ([Elle §§3 and 4.3](https://arxiv.org/abs/2003.10554)). |
| Reached paths stall behind comparisons | Investigate a supported dictionary, comparison-feedback or solver lane | A target-compatible mechanism and a concrete pilot; AFL++ offers instrumentation choices, not universal success ([AFL++ §1](https://aflplus.plus/docs/fuzzing_in_depth/)). |
| Same slow/OOM/failure case repeatedly consumes the run | Reproduce and classify it; preserve evidence before excluding or repairing anything | Separate product resource/progress contracts from runner limits; recurrent blocking failures affect search ([ClusterFuzz performance](https://google.github.io/clusterfuzz/using-clusterfuzz/workflows/analyzing-fuzzing-performance/)). |
| Many candidates, little completed reproduction | Allocate to replay, reduction and triage | Reproduction reliability and affected build/platform information ([ClusterFuzz triage](https://google.github.io/clusterfuzz/using-clusterfuzz/workflows/triaging-new-crashes/)). |
| Useful property-relevant reach continues | Extend within budget or compare a complementary lane | Preserve counters over comparable intervals; diverse AFL++ configurations are an available tactic ([AFL++ §3.c](https://aflplus.plus/docs/fuzzing_in_depth/)). |
| Reach plateaus and no new findings appear | Diagnose blind spots, change dimension or stop with a bounded negative result | Record remaining uncertainty; performance analysis is useful for quiet targets ([ClusterFuzz performance](https://google.github.io/clusterfuzz/using-clusterfuzz/workflows/analyzing-fuzzing-performance/)). |

## Keep the denominators

Record counts rather than only percentages. If one campaign evaluates a property for every input and another skips most inputs, equal execution counts are not equal observations. Seed quality and target progress are explicit integration concerns ([OSS-Fuzz integration](https://google.github.io/oss-fuzz/advanced-topics/ideal-integration/)).

Keep separate columns in the existing experiment record:

- **Search:** submitted and accepted cases, property evaluations, reached operations/effects, instrumented code coverage where applicable.
- **Findings:** raw candidates, reproduced violations, verified cause groups, harness/infrastructure cases and unresolved observations.
- **Cost:** elapsed time, workers/CPU, peak resources, setup, replay, reduction and triage effort.

This metric selection is the pack's decision aid. Do not claim the columns are interchangeable or empirically calibrated. FuzzBench's coverage distributions support reporting variation, while ClusterFuzz's triage fields support retaining reproduction conditions ([FuzzBench report](https://google.github.io/fuzzbench/reference/report/), [ClusterFuzz triage](https://google.github.io/clusterfuzz/using-clusterfuzz/workflows/triaging-new-crashes/)).

## Interpret controls, not just totals

When a new expensive lane claims a property, reuse a known regression or independently justified fault to see whether it reaches and rejects the violation. SQLite documents mutation testing as one way to evaluate tests; that does not make mutation score a product-bug count ([SQLite §7.6](https://www.sqlite.org/testing.html)). Use `harness-sensitivity` for the detailed choice. If the control survives, investigate the oracle or reach before spending the full allocation.

Preserve campaign-level versus per-case limits distinctly. For example, libFuzzer documents separate `-max_total_time`, `-timeout` and `-rss_limit_mb` options; choose their target-specific values in the execution skill, and record which limit ended an observation ([libFuzzer options](https://llvm.org/docs/LibFuzzer.html#options)).
