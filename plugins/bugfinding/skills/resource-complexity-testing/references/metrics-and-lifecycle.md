# Metrics and lifecycle

Choose the quantity and phase that can refute the actual promise. Source pins below are evidence snapshots, not a universal installed-runtime support matrix.

| Observation | Information retained / lost | Consequence |
|---|---|---|
| Go B/op and allocs/op | Deltas of TotalAlloc/Mallocs, including churn | Do not label allocation throughput as retained live memory ([benchmark source, StartTimer/StopTimer](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/testing/benchmark.go)). |
| Go heap versus allocs profile | Heap uses the latest completed GC boundary; allocs defaults to cumulative allocated bytes, including reclaimed bytes | Record GC/profile phase and selected sample index ([pprof, Heap/Allocs](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/runtime/pprof/pprof.go)). |
| Go CPU-class estimates | Runtime estimates are not directly comparable to system CPU | Use a matching actual observer for system CPU accounting ([metrics descriptions, /cpu/classes](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/runtime/metrics/description.go)). |
| pyperf track-memory | Linux private mappings; Windows lifetime peak commit charge | Preserve platform and metric identity; this is not portable RSS or retained-object count ([Runner, Misc](https://raw.githubusercontent.com/psf/pyperf/2ed9b9ed4d56448b6a19b6236c7a519a62f6dfe5/doc/runner.rst)). |
| Python tracemalloc | Traced Python allocations; extensions may register other domains | Early untraced/native resources can remain outside the observation ([tracemalloc, startup/Filter](https://raw.githubusercontent.com/python/cpython/0e98aea32593e39c647c2b3d7054ec4e36bf643a/Doc/library/tracemalloc.rst)). |

Go custom resource profiles retain tracking keys until removed; the observer itself can cause retention. Reuse a correct existing owner rather than add a universal resource registry ([pprof, Profile.Add](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/runtime/pprof/pprof.go)). Python tracing also consumes CPU/memory; frame depth and tracing overhead must remain visible ([tracemalloc, start/get_tracemalloc_memory](https://raw.githubusercontent.com/python/cpython/0e98aea32593e39c647c2b3d7054ec4e36bf643a/Doc/library/tracemalloc.rst)).

## Preserve lifecycle meaning

Distinguish fresh subject, warmed subject, intended bounded cache and repeated long-lived lifecycle. These are experiment choices, not interchangeable cleanup strategies. ResetTimer changes counters; it does not restore application state ([Go benchmark, ResetTimer](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/testing/benchmark.go)). A pyperf in-process run explicitly affects subsequent runs ([Runner, --in-process](https://raw.githubusercontent.com/psf/pyperf/2ed9b9ed4d56448b6a19b6236c7a519a62f6dfe5/doc/runner.rst)).

Record creation, use, cancellation/close and required drain/quiescence from the real ownership contract. Observe before reset. Conversely, do not charge deliberate growing state as a leak without a bound. Keep profiler-instrumented and production-cost observations distinct.

For a growth claim, preserve the measured size/history family and ordinary controls. Report the finite range and uncertainty; a fitted curve is not an asymptotic proof. For retention, reduce the repeated lifecycle and failure placement together, not just the final payload. These are this pack's evidence-preservation rules; `failure-reduction` owns the general reducer.
