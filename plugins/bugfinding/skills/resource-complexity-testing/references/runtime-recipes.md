# Conditional runtime recipes

Use existing fitting harnesses and the project's permitted runner. Commands below are source-read shapes, not executed examples or authority to change dependencies. Choose actual target names and budgets; preserve output using the environment's approved artifact mechanism.

## Go workload families

In an existing faithful benchmark, select the discovered cases and repeat observations:

```text
go test ./path/to/pkg -run='^$' -bench='^BenchmarkCase$' -benchmem -count=10
benchstat reference.txt candidate.txt
```

The count matches benchstat's stated floor: "Each benchmark should be run at least 10 times" for a statistically significant sample; it is a sampling minimum, not a product threshold. Keep benchmark identities matched; benchstat compares corresponding records ([benchstat, Usage and Example](https://raw.githubusercontent.com/golang/perf/be2c69fb417e05de5fec05c732911f4c5f172606/cmd/benchstat/main.go)). Allocation figures do not establish retained bytes ([Go benchmark, timer/allocation counters](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/testing/benchmark.go)). Preserve the lifecycle prefix that the benchmark actually runs. Use existing profiling only to diagnose the confirmed workload, not as a replacement for discovery.

## Python measurement

For an existing pyperf Runner harness, choose its processes/values/warmups/loops and `--timeout`, writing a fresh named result with `-o RUN.json`. On a benchmark execution timeout "pyperf exits with error code 124", and "There is no time out by default" ([Runner, Loop iterations/JSON/Misc](https://raw.githubusercontent.com/psf/pyperf/2ed9b9ed4d56448b6a19b6236c7a519a62f6dfe5/doc/runner.rst)). Inspect and compare retained results:

```text
python -m pyperf check RUN.json
python -m pyperf stats RUN.json
python -m pyperf dump RUN.json
python -m pyperf compare_to reference.json candidate.json --table
```

These commands operate on recorded suites; comparison does not reset or rerun the subject. `check` warns, among other checks, "if the standard deviation is greater than 10% of the mean"; `compare_to` will "use the first file as the reference" and decides significance with "a Student's two-sample, two-tailed t-test" ([pyperf CLI, check/stats/dump/compare_to](https://raw.githubusercontent.com/psf/pyperf/2ed9b9ed4d56448b6a19b6236c7a519a62f6dfe5/doc/cli.rst)). Choose memory mode using [metrics and lifecycle](metrics-and-lifecycle.md). Selected package metadata requires Python >= 3.11 and psutil outside Emscripten, and declares MIT; verify the selected installed release rather than rely on older optional-dependency prose ([pyproject, project](https://raw.githubusercontent.com/psf/pyperf/2ed9b9ed4d56448b6a19b6236c7a519a62f6dfe5/pyproject.toml)).

## Historical native PerfFuzz

Only use this implementation when its toolchain actually fits. The pinned README says PerfFuzz "was evaluated with clang-3.8.0 on Linux" and works with version 8 on Mac, builds through instrumented C/C++ compiler wrappers, and "will not build on Windows machines". It is not an established modern Go/Windows backend ([README, Building/Compile](https://raw.githubusercontent.com/carolemieux/perffuzz/f937f370555d0c54f2109e3b1aa5763f8defe337/README.md)).

```text
./afl-fuzz -p -i SEEDS -o OWNED_OUT -N 64 ./target @@
```

Here, `64` is an illustrative maximum file size, and the README requires seed inputs "of smaller size than" that limit; these are fork-specific flags. Its `total paths` is "just the number of saved inputs" and `+max` marks inputs saved because they maximized a performance key, not verified defects ([README, Run/Interpret](https://raw.githubusercontent.com/carolemieux/perffuzz/f937f370555d0c54f2109e3b1aa5763f8defe337/README.md)). Inspect selected executable help before applying old options to another AFL build. The actual afl-showmax source sets `"detect_leaks=0:"` in `ASAN_OPTIONS` when that variable is unset, so that route cannot silently supply a leak oracle ([afl-showmax, ASAN_OPTIONS setup](https://raw.githubusercontent.com/carolemieux/perffuzz/f937f370555d0c54f2109e3b1aa5763f8defe337/afl-showmax.c)). That file's Apache 2.0 header does not establish whole-project terms ([same source, license header](https://raw.githubusercontent.com/carolemieux/perffuzz/f937f370555d0c54f2109e3b1aa5763f8defe337/afl-showmax.c)).
