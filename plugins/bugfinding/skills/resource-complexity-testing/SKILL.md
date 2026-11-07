---
name: resource-complexity-testing
description: Searches inputs and operation histories for CPU, allocation, memory-retention or handle-growth violations. Use when an established test needs resource-sensitive discovery, a repeatable expensive input family, or lifecycle-aware confirmation and reduction.
---

# Resource complexity testing

Find costly valid structures and histories, then confirm the actual resource promise on the real producer. Treat search feedback and the confirming observation separately: PerfFuzz maximizes per-location execution counts, which are its search objective rather than a wall-time or retention guarantee: its authors note the identified bottlenecks "may not be the points in which the program spends the most time" ([PerfFuzz, §§3, 6](https://www.carolemieux.com/perffuzz-issta2018.pdf)).

## Select the experiment

Read the public entrypoint, enabled build, accepted input/state, quotas and required cleanup. Name the resource, observation phase and evidence that would violate the target's actual contract. This pack's procedure is engineering synthesis; it does not invent a latency threshold or declare every expensive operation a bug. Use `correctness-oracles` for the governing guarantee.

Choose the missing dimension: equal-size collision structure, decoded expansion, populated state, or create/use/cancel/close history. PerfFuzz preserves improvements at separate hot spots "even if the mutation reduces the total execution path length", allowing search past scalar local maxima ([PerfFuzz, §§2–3](https://www.carolemieux.com/perffuzz-issta2018.pdf)). Preserve useful intermediates; do not rank only by file size or one aggregate cost. Read [search and confirmation](references/search-and-confirmation.md).

## Execute search and confirmation

Use a compatible existing search/measurement owner. Conditional commands, setup limits and output interpretation are in [runtime recipes](references/runtime-recipes.md); the historical PerfFuzz implementation instruments C/C++ builds and "will not build on Windows machines", so it is not a generic modern Windows/Go backend ([PerfFuzz README, Building; Running PerfFuzz on a program of your choice](https://raw.githubusercontent.com/carolemieux/perffuzz/f937f370555d0c54f2109e3b1aa5763f8defe337/README.md)). Invocation preserves the user's current execution/dependency scope.

Separate generated candidates, admitted operations, useful fitness improvements, measured confirmations and reproduced violations. Promote promising candidates to repeated matched observations; benchstat compares "each benchmark in the first file to the same benchmark" in later files and supplies medians, confidence intervals and significance, not a product budget ([benchstat, Usage and Example](https://raw.githubusercontent.com/golang/perf/be2c69fb417e05de5fec05c732911f4c5f172606/cmd/benchstat/main.go)). Its usage says each benchmark "should be run at least 10 times" for a statistically significant sample ([benchstat, Usage](https://raw.githubusercontent.com/golang/perf/be2c69fb417e05de5fec05c732911f4c5f172606/cmd/benchstat/main.go)); treat that as a sampling floor for benchstat, raise it from observed uncertainty and decision cost, and never read it as a product acceptance rule.

Match input/decoded size, state, lifecycle phase, build and observer. Go's ResetTimer "zeroes the elapsed benchmark time and memory allocation counters", not subject state ([Go benchmark, ResetTimer](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/testing/benchmark.go)). pyperf's `--in-process` mode "makes each run affect the next run" ([pyperf Runner, Misc](https://raw.githubusercontent.com/psf/pyperf/2ed9b9ed4d56448b6a19b6236c7a519a62f6dfe5/doc/runner.rst)). Read [metrics and lifecycle](references/metrics-and-lifecycle.md) before interpreting growth.

## Preserve the resource counterexample

Keep the original input family or operation prefix, actual contract, raw candidate/control samples, observer/configuration, reset/quiescence evidence, source/build/runtime and subject versus harness limits. These are this pack's handoff conventions. Do not call finite measurements an asymptotic proof or replace the selected contract with a shorter timeout.

Reduce structure and required history while retaining the same metric, size regime and matched violation. A useful reduction can be a family of cases rather than one file; PerfFuzz defines pathological inputs as those that, "given a fixed input length, maximize" a component's execution count, and its evaluation varies that maximum length as a separate axis, which motivates keeping size and structure separate ([PerfFuzz, §§1, 5](https://www.carolemieux.com/perffuzz-issta2018.pdf)). Use `failure-reduction` for generic mechanics and `evidence-based-triage` for attribution.

Return the tested promise, family and controls, observed range/variability, lifecycle and metric scope, resource use, reproduced evidence and remaining uncertainty. Use [common mistakes](references/common-mistakes.md) to check that allocation churn, peaks, live resources and proxy counts have not been collapsed into one finding.
