# Python and JVM

Use existing fitting integrations; setup changes require the task's actual scope. Examples use POSIX environment syntax; set the equivalent environment in the chosen shell and restore task-specific changes.

## Atheris

The inspected README says "Atheris supports Linux (32- and 64-bit) and Mac OS X, Python versions 3.11-3.14." Instrument target imports inside `atheris.instrument_imports()` before importing the target, or explicitly instrument existing functions; "You must call `atheris.Setup()` before `atheris.Fuzz()`." Atheris "is based off of libFuzzer", whose flags it accepts. A configured harness can run ([Atheris README, Installation Instructions and Using Atheris](https://raw.githubusercontent.com/google/atheris/e36da74cf42b5834c4e31d7cabb58d796695d29f/README.md)):

```sh
python fuzz_target.py corpus -max_total_time=300
```

Atheris reports "no interesting inputs were found" "if the first 2 calls to `TestOneInput` didn't produce any coverage events", even when other modules have instrumentation. Inspect early-return guards and real target calls before adding workers. Atheris "will report a failure if the Python code under test throws an uncaught exception", so catch only errors permitted by the actual input contract; a catch-all can erase findings ([Atheris README, Python coverage and Why am I getting "No interesting inputs were found"?](https://raw.githubusercontent.com/google/atheris/e36da74cf42b5834c4e31d7cabb58d796695d29f/README.md)).

Native extensions "must be built with Clang, using the argument `-fsanitize=fuzzer-no-link`" and need compatible Atheris/libFuzzer/runtime-symbol linkage; ordinary Python instrumentation does not instrument native code. Verify the selected platform route: the recommended sanitizer+libFuzzer preload "is not yet supported on Mac", and the modified-CPython alternative targets "Python 3.8.6", outside current support ([Atheris native extensions](https://raw.githubusercontent.com/google/atheris/e36da74cf42b5834c4e31d7cabb58d796695d29f/native_extension_fuzzing.md)).

For a separate coverage.py measurement, "Coverage reports are only generated when your fuzzer exits gracefully": the documented `-atheris_runs=N` does; a native crash or "libFuzzer's `-runs` flag" does not. Include measurement overhead separately; coverage.py "will significantly slow down your fuzzer". Atheris has Apache-2.0 licensing ([Atheris README, Visualizing Python code coverage](https://raw.githubusercontent.com/google/atheris/e36da74cf42b5834c4e31d7cabb58d796695d29f/README.md), [Atheris license](https://raw.githubusercontent.com/google/atheris/e36da74cf42b5834c4e31d7cabb58d796695d29f/LICENSE)).

## Jazzer/JUnit

Verify selected jazzer-junit/JUnit/runtime compatibility; the README requires "JUnit (version 5.9.0 or newer)" and lists Linux x86-64/arm64, macOS 12+ x86-64/arm64 and Windows x86-64. "By default, Jazzer operates in regression mode unless fuzzing mode is explicitly enabled"; enable `JAZZER_FUZZ=1` for discovery ([Jazzer README, platform list, Setup and Running Jazzer](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer/a4e09fbbc775d129ce61d5802e893160e31a6d40/README.md)). A configured Maven/Surefire class selection is:

```sh
JAZZER_FUZZ=1 mvn -Dtest=ParserTests test
```

Use the project's actual class/runner; Surefire's documented route is to "set the test property to a specific test case" ([Maven Surefire 3.5.4 single-test selection](https://maven.apache.org/surefire-archives/surefire-3.5.4/maven-surefire-plugin/examples/single-test.html)). "In fuzzing mode, only a single fuzz test per test run will be executed." ([Jazzer FuzzTest annotation](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer/a4e09fbbc775d129ce61d5802e893160e31a6d40/src/main/java/com/code_intelligence/jazzer/junit/FuzzTest.java)). Keep crashing inputs (the inputs directory under test resources), the generated corpus (`.cifuzz-corpus/...`) and stand-alone Java reproducers (`reproducer_path`) distinct ([Jazzer README, Directories and files](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer/a4e09fbbc775d129ce61d5802e893160e31a6d40/README.md), [Jazzer configuration options](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer/a4e09fbbc775d129ce61d5802e893160e31a6d40/docs/arguments-and-configuration-options.md)).

Set `@FuzzTest(maxDuration=...)` (default `"5m"`) or `maxExecutions`; `jazzer.max_duration`/`jazzer.max_executions` can override them, and each "has no effect during regression testing". The default lifecycle is `PER_TEST`; during regression "fuzz tests always go through the full JUnit lifecycle for every execution" ([Jazzer FuzzTest annotation](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer/a4e09fbbc775d129ce61d5802e893160e31a6d40/src/main/java/com/code_intelligence/jazzer/junit/FuzzTest.java)).

In discovery, `PER_TEST` runs `@BeforeEach` "once for each fuzz test" and is "more likely to unintentionally preserve state between fuzz test executions, which can result in non-reproducible findings". `PER_EXECUTION` runs supported callbacks and "every execution uses its own test class instance"; its lifecycle methods "may be invoked concurrently". Choose actual reset ownership; a passing regression can hide discovery residue. If accumulated state is intentional, preserve its sequence instead of depending on invisible residue ([Jazzer Lifecycle implementation](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer/a4e09fbbc775d129ce61d5802e893160e31a6d40/src/main/java/com/code_intelligence/jazzer/junit/Lifecycle.java)).

Jazzer's selected source license is Apache-2.0; dependency/runtime compatibility still belongs to the chosen release ([Jazzer license](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer/a4e09fbbc775d129ce61d5802e893160e31a6d40/LICENSE)).
