# Conditional runtime recipes

Use existing fitting harnesses and the project's permitted runner. Commands below are source-read shapes, not executed examples or authority to change dependencies. Choose actual target names and budgets; preserve output using the environment's approved artifact mechanism.

## Go workload families

In an existing faithful benchmark, select the discovered cases and repeat observations:

```text
go test ./path/to/pkg -run='^$' -bench='^BenchmarkCase$' -benchmem -count=10
benchstat reference.txt candidate.txt
```

The count is the upstream example, not a required threshold. Keep benchmark identities matched; benchstat compares corresponding records. Allocation figures do not establish retained bytes ([benchstat, Example](https://raw.githubusercontent.com/golang/perf/be2c69fb417e05de5fec05c732911f4c5f172606/cmd/benchstat/main.go), [Go benchmark, timer/allocation counters](https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/testing/benchmark.go)). Preserve the lifecycle prefix that the benchmark actually runs. Use existing profiling only to diagnose the confirmed workload, not as a replacement for discovery.

## Python measurement

For an existing pyperf Runner harness, choose its processes/values/warmups/loops and `--timeout`, writing a fresh named result with `-o RUN.json`. A benchmark execution timeout exits124; no timeout is configured by default ([Runner, Loop iterations/JSON/Misc](https://raw.githubusercontent.com/psf/pyperf/2ed9b9ed4d56448b6a19b6236c7a519a62f6dfe5/doc/runner.rst)). Inspect and compare retained results:

```text
python -m pyperf check RUN.json
python -m pyperf stats RUN.json
python -m pyperf dump RUN.json
python -m pyperf compare_to reference.json candidate.json --table
```

These commands operate on recorded suites; comparison does not reset or rerun the subject ([pyperf CLI, check/stats/dump/compare_to](https://raw.githubusercontent.com/psf/pyperf/2ed9b9ed4d56448b6a19b6236c7a519a62f6dfe5/doc/cli.rst)). Choose memory mode using [metrics and lifecycle](metrics-and-lifecycle.md). Selected package metadata requires Python>=3.11 and psutil outside Emscripten, and declares MIT; verify the selected installed release rather than rely on older optional-dependency prose ([pyproject, project](https://raw.githubusercontent.com/psf/pyperf/2ed9b9ed4d56448b6a19b6236c7a519a62f6dfe5/pyproject.toml)).

## Historical native PerfFuzz

Only use this implementation when its toolchain actually fits. The pinned README documents Linux Clang3.8/Mac Clang8 context, instrumented C/C++ compiler wrappers and no Windows build. It is not an established modern Go/Windows backend ([README, Building/Compile](https://raw.githubusercontent.com/carolemieux/perffuzz/f937f370555d0c54f2109e3b1aa5763f8defe337/README.md)).

```text
./afl-fuzz -p -i SEEDS -o OWNED_OUT -N 64 ./target @@
```

Here, `64` is an illustrative maximum file size and seeds must be smaller; these are fork-specific flags. Its `total paths` means saved inputs and `+max` marks performance-key improvements, not verified defects ([README, Run/Interpret](https://raw.githubusercontent.com/carolemieux/perffuzz/f937f370555d0c54f2109e3b1aa5763f8defe337/README.md)). Inspect selected executable help before applying old options to another AFL build. The actual afl-showmax source sets leak detection off in its default ASan environment, so that route cannot silently supply a leak oracle ([afl-showmax, ASAN_OPTIONS setup](https://raw.githubusercontent.com/carolemieux/perffuzz/f937f370555d0c54f2109e3b1aa5763f8defe337/afl-showmax.c)). That file's Apache2.0 header does not establish whole-project terms ([same source, license header](https://raw.githubusercontent.com/carolemieux/perffuzz/f937f370555d0c54f2109e3b1aa5763f8defe337/afl-showmax.c)).
