# C++ FuzzTest

The inspected Bazel route requires Clang and C++17 on Linux or experimental macOS. Reuse the project's supported dependency/configuration owner; check the selected release's generated fuzz configuration instead of copying a tutorial's historical dependency pins ([FuzzTest Bazel quickstart](https://raw.githubusercontent.com/google/fuzztest/main/doc/quickstart-bazel.md)).

For an already configured target:

```sh
bazel run --config=fuzztest :TARGET -- --fuzz=SUITE.PROPERTY
```

That selected-property mode is indefinite. `--fuzz_for=5m` instead runs all fuzz tests in the binary for its duration; do not claim it selects only the named property. Pick the correct target/mode and an authorized outer bound. `--rss_limit_mb` and `--time_limit_per_input` are separate guards. Ordinary `bazel test` unit mode does not establish an instrumented discovery run ([FuzzTest Bazel quickstart](https://raw.githubusercontent.com/google/fuzztest/main/doc/quickstart-bazel.md), [FuzzTest flags](https://raw.githubusercontent.com/google/fuzztest/main/doc/flags-reference.md)).

Inspect fixture lifetime. `PerIterationFixtureAdapter` and `PerFuzzTestFixtureAdapter` have different setup/reset boundaries. Share expensive immutable setup only while restoring state needed by the tested property; don't assume a unit-test fixture is recreated for every mutation ([FuzzTest fixtures](https://raw.githubusercontent.com/google/fuzztest/main/doc/fixtures.md)).

Use `semantic-program-generation` for dependent domains and world/program construction. This execution skill owns the actual build, discovery mode, lifecycle and retained reproducer. General FuzzTest licensing is Apache-2.0 with enumerated file exceptions; inspect the selected source/dependencies rather than apply that label universally ([FuzzTest license](https://raw.githubusercontent.com/google/fuzztest/main/LICENSE)).
