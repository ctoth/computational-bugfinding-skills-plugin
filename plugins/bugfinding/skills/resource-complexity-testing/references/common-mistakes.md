# Common mistakes

| WRONG | RIGHT |
|---|---|
| Keep only increasing total work; discard a case whose distinct hotspot improves. | Retain useful independent maxima; the paper shows scalar local maxima can impede search ([PerfFuzz, §3](https://www.carolemieux.com/perffuzz-issta2018.pdf)). |
| Report high B/op as a retained-memory leak. | Measure the promised live resource at its lifecycle boundary; benchmark allocation deltas include churn ([Go benchmark, timer counters](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/testing/benchmark.go)). |
| ResetTimer restores the warm subject. | Reset actual subject state separately when the experiment requires it; ResetTimer clears counters ([Go benchmark, ResetTimer](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/testing/benchmark.go)). |
| Treat Windows pyperf peak as current RSS. | Label lifetime peak commit charge and keep the platform/phase ([Runner, Misc](https://raw.githubusercontent.com/psf/pyperf/2ed9b9ed4d56448b6a19b6236c7a519a62f6dfe5/doc/runner.rst)). |
| Flat tracemalloc data clears every native leak. | Preserve its tracing domain and missing pre-start allocations ([tracemalloc, take_snapshot/Filter](https://raw.githubusercontent.com/python/cpython/0e98aea32593e39c647c2b3d7054ec4e36bf643a/Doc/library/tracemalloc.rst)). |
| A significant benchmark difference is automatically a product bug. | Establish the resource promise independently; benchstat reports statistical comparisons, not a product budget ([benchstat, Usage](https://raw.githubusercontent.com/golang/perf/be2c69fb417e05de5fec05c732911f4c5f172606/cmd/benchstat/main.go)). |
| Apply PerfFuzz `-p/-N` flags to any current AFL executable. | Use the selected fork's documented interface and verified fit ([PerfFuzz README, Run](https://raw.githubusercontent.com/carolemieux/perffuzz/f937f370555d0c54f2109e3b1aa5763f8defe337/README.md)). |
| A smaller candidate that fails only after lowering the host limit reproduces the original. | Keep metric, subject quota, setup and matched controls fixed; otherwise preserve it as a different experiment (this pack's reduction rule). |
