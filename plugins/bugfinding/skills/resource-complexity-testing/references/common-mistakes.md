# Common mistakes

## Discarding a case because total work fell

**Wrong:** Keep only increasing total work; discard a case whose distinct hotspot improves.

**Right:** Retain useful independent maxima. PerfFuzz saves an input that maximizes some edge count "even if the mutation reduces the total execution path length", and the authors judge that "a greedy approach to maximizing total path length is likely to get stuck in local maxima" ([PerfFuzz, §§2, 5.1.1](https://www.carolemieux.com/perffuzz-issta2018.pdf)).

**Why:** the first hash collisions shorten the path; only later collisions make it quadratically longer.

## Reporting B/op as a leak

**Wrong:** Report high B/op as a retained-memory leak.

**Right:** Measure the promised live resource at its lifecycle boundary. Benchmark allocation figures are deltas of `memStats.TotalAlloc` and `memStats.Mallocs` taken between StartTimer and StopTimer ([Go benchmark, StartTimer/StopTimer](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/testing/benchmark.go)).

**Why:** TotalAlloc "does not decrease when objects are freed", so churn and retention look the same ([Go runtime MemStats, TotalAlloc](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/runtime/mstats.go)).

## Expecting ResetTimer to restore the subject

**Wrong:** ResetTimer restores the warm subject.

**Right:** Reset actual subject state separately when the experiment requires it. ResetTimer "zeroes the elapsed benchmark time and memory allocation counters" ([Go benchmark, ResetTimer](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/testing/benchmark.go)).

**Why:** state carried between iterations changes what each iteration measures.

## Reading pyperf's Windows peak as current RSS

**Wrong:** Treat Windows pyperf `--track-memory` output as current RSS.

**Right:** Label it "the peak value of the Commit Charge during the lifetime of this process" and keep the platform and phase ([pyperf Runner, Misc](https://raw.githubusercontent.com/psf/pyperf/2ed9b9ed4d56448b6a19b6236c7a519a62f6dfe5/doc/runner.rst)).

**Why:** a lifetime peak cannot show memory released or retained at a later boundary.

## Clearing native leaks with tracemalloc

**Wrong:** Flat tracemalloc data clears every native leak.

**Right:** Preserve its tracing domain and the missing pre-start allocations: a snapshot "does not include memory blocks allocated before" tracing started, and "C extensions can use other domains to trace other resources" ([tracemalloc, take_snapshot/Filter](https://raw.githubusercontent.com/python/cpython/0e98aea32593e39c647c2b3d7054ec4e36bf643a/Doc/library/tracemalloc.rst)).

**Why:** native handles and untraced allocators sit outside what the snapshot observed.

## Treating significance as a product bug

**Wrong:** A significant benchmark difference is automatically a product bug.

**Right:** Establish the resource promise independently. benchstat warns that "\"statistically significant\" is not the same as \"large\"" ([benchstat, Example](https://raw.githubusercontent.com/golang/perf/be2c69fb417e05de5fec05c732911f4c5f172606/cmd/benchstat/main.go)).

**Why:** with enough low-noise samples a tiny, contract-compliant change becomes significant.

## Reusing PerfFuzz flags on another AFL

**Wrong:** Apply PerfFuzz `-p/-N` flags to any current AFL executable.

**Right:** Use the selected fork's documented interface and verified fit. The README adds `-p` as the "option to enable PerfFuzz" in its own `afl-fuzz` ([PerfFuzz README, Run PerfFuzz on your program](https://raw.githubusercontent.com/carolemieux/perffuzz/f937f370555d0c54f2109e3b1aa5763f8defe337/README.md)).

**Why:** the flags belong to this fork; another AFL build may reject them or give them another meaning.

## Lowering the host limit during reduction

**Wrong:** A smaller candidate that fails only after lowering the host limit reproduces the original.

**Right:** Keep metric, subject quota, setup and matched controls fixed; otherwise preserve it as a different experiment (this pack's reduction rule).

**Why:** a tighter limit changes the experiment, so the smaller case no longer shows the original violation.
