# Python and JVM

Use existing fitting integrations; setup changes require the task's actual scope. Examples use POSIX environment syntax; set the equivalent environment in the chosen shell and restore task-specific changes.

## Atheris

The inspected README supports Python 3.11-3.14 on Linux/macOS. Instrument target imports before importing the target, or explicitly instrument existing functions; call `Setup` before `Fuzz`. A configured harness can run:

```sh
python fuzz_target.py corpus -max_total_time=300
```

If the first two callbacks reach no instrumented code, Atheris can report no interesting inputs despite other modules having instrumentation. Inspect early-return guards and real target calls before adding workers. Catch only errors permitted by the actual input contract; a catch-all can erase findings ([Atheris README](https://raw.githubusercontent.com/google/atheris/master/README.md)).

Native extensions require Clang `-fsanitize=fuzzer-no-link` and compatible Atheris/libFuzzer/runtime-symbol linkage; ordinary Python instrumentation does not instrument native code. Verify the selected platform route rather than transplant an old modified-CPython recipe ([Atheris native extensions](https://raw.githubusercontent.com/google/atheris/master/native_extension_fuzzing.md)).

For a separate coverage.py measurement, the documented `-atheris_runs=N` exits gracefully; ordinary libFuzzer `-runs` or native crashes may not flush Python coverage. Include measurement overhead separately. Atheris has Apache-2.0 licensing ([Atheris README](https://raw.githubusercontent.com/google/atheris/master/README.md), [Atheris license](https://raw.githubusercontent.com/google/atheris/master/LICENSE)).

## Jazzer/JUnit

Verify selected jazzer-junit/JUnit/runtime compatibility. Current README lists Linux x86-64/arm64, macOS 12+ x86-64/arm64 and Windows x86-64. Ordinary test execution defaults to regression; enable `JAZZER_FUZZ=1` for discovery. A configured Maven/Surefire class selection is:

```sh
JAZZER_FUZZ=1 mvn -Dtest=ParserTests test
```

Use the project's actual class/runner. Only one fuzz test runs per discovery invocation. Keep crashing inputs, generated corpus and typed Java reproducer artifacts distinct ([Jazzer README](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer/main/README.md), [Maven Surefire single-test selection](https://maven.apache.org/surefire/maven-surefire-plugin/examples/single-test.html)).

Set `@FuzzTest(maxDuration="5m")` or a chosen execution count; corresponding Jazzer options can override annotation limits, which do not apply in regression mode. The default lifecycle is `PER_TEST`; regression always uses the full JUnit lifecycle per input ([Jazzer FuzzTest annotation](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer/main/src/main/java/com/code_intelligence/jazzer/junit/FuzzTest.java)).

In discovery, `PER_TEST` runs `@BeforeEach` once per fuzz test. `PER_EXECUTION` runs supported callbacks and a separate test instance per input, with documented callback/concurrency limits. Choose actual reset ownership; a passing regression can hide discovery residue. If accumulated state is intentional, preserve its sequence instead of depending on invisible residue ([Jazzer Lifecycle implementation](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer/main/src/main/java/com/code_intelligence/jazzer/junit/Lifecycle.java)).

Jazzer's selected source license is Apache-2.0; dependency/runtime compatibility still belongs to the chosen release ([Jazzer license](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer/main/LICENSE)).
