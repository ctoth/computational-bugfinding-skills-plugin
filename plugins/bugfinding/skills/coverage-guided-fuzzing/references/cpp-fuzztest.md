# C++ FuzzTest

The inspected Bazel route requires "A Linux-based operating system or macOS (experimental)", Clang and Bazel, and its `.bazelrc` selects C++17. Reuse the project's supported dependency/configuration owner; check the selected release's generated fuzz configuration (`bazel run @fuzztest//bazel:setup_configs > fuzztest.bazelrc`) instead of copying the tutorial's historical `version = "20241028.0"` pin ([FuzzTest Bazel quickstart, Prerequisites and Set up a Bazel workspace](https://raw.githubusercontent.com/google/fuzztest/1b4e4f0e4c446aca4660c43a28ec1b8d893b6510/doc/quickstart-bazel.md)).

For an already configured target:

```sh
bazel run --config=fuzztest :TARGET -- --fuzz=SUITE.PROPERTY
```

That selected-property mode is indefinite: it "keeps running the test with different input values until it finds a crash or it is explicitly terminated by the user". `--fuzz_for=5m` instead is documented as "Run all fuzz tests in fuzzing mode for `T` duration"; do not claim it selects only the named property. Pick the correct target/mode and an authorized outer bound. `--rss_limit_mb` and `--time_limit_per_input` are separate guards. Ordinary `bazel test` unit mode runs "without sanitizer and coverage instrumentation", so it does not establish an instrumented discovery run ([FuzzTest Bazel quickstart, Create and run a fuzz test](https://raw.githubusercontent.com/google/fuzztest/1b4e4f0e4c446aca4660c43a28ec1b8d893b6510/doc/quickstart-bazel.md), [FuzzTest flags](https://raw.githubusercontent.com/google/fuzztest/1b4e4f0e4c446aca4660c43a28ec1b8d893b6510/doc/flags-reference.md)).

Inspect fixture lifetime. `PerIterationFixtureAdapter` and `PerFuzzTestFixtureAdapter` have different setup/reset boundaries; the latter "relies on the fixture being easily resettable". Share expensive immutable setup only while restoring state needed by the tested property ("BEST PRACTICE: Make sure that the property function resets the mutated fixture"); don't assume a unit-test fixture is recreated for every mutation ([FuzzTest fixtures, Note on mutable test fixtures and Using existing GoogleTest fixtures](https://raw.githubusercontent.com/google/fuzztest/1b4e4f0e4c446aca4660c43a28ec1b8d893b6510/doc/fixtures.md)).

Use `semantic-program-generation` for dependent domains and world/program construction. This execution skill owns the actual build, discovery mode, lifecycle and retained reproducer. General FuzzTest licensing is Apache-2.0 with enumerated file exceptions; inspect the selected source/dependencies rather than apply that label universally ([FuzzTest license](https://raw.githubusercontent.com/google/fuzztest/1b4e4f0e4c446aca4660c43a28ec1b8d893b6510/LICENSE)).
