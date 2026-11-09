# Conditional tool choices

Documentation snapshot checked 2026-11-07. Recheck the selected release and existing project integration before execution; these examples were not run for this skill.

## Csmith: C programs

Csmith "is a random generator of C programs"; use it for a compatible C compiler target, not as a Go/MOO generator. In an existing installation, `csmith -h` and `csmith -hh` expose options; generated source is compiled with the installation's header include path (`-I$HOME/csmith/include` in the README example). Preserve emitted source and selected compilers/configurations. The README warns that "generated programs might contain infinite loops" and advises "to apply timeout to their executions"; an output difference can also be "a bug in Csmith itself". Its build instructions are platform-specific (Ubuntu commands plus a separate Windows guide); no host installation is implied ([Csmith README, Install and Use](https://raw.githubusercontent.com/csmith-project/csmith/0cdc710315cfee9035e22ef4363ca479270d1934/README.md)). The source uses a two-clause BSD license ([COPYING](https://raw.githubusercontent.com/csmith-project/csmith/0cdc710315cfee9035e22ef4363ca479270d1934/COPYING)).

## FuzzTest: dependent C++ domains

Use constructive dependent domains for legal ranges/relationships; `FlatMap` exists for "parameters that are dependent on each other", such as a string and a valid index into it. Check empty-container and overflow boundaries in the domain itself: the reference's string/index example derives `InRange(0, s.size() - 1)`, which has no valid index for an empty string, and its recommended `Map` example bounds inputs to "Ensure we don't try to produce a value that causes integer overflow". Prefer constructive `Map` to restrictive `Filter`: low-yield filters cause "ineffective fuzzing" and "too restrictive filter functions will trigger an abort in the framework". `Map`/`FlatMap` "don't support initial seeds"; their reversible variants do, and require the inverse law `f(g(y)) == y` (for `ReversibleFlatMap`, `y` must be in `f(g(y))`). For recursive domains the reference warns "Recursion limit for recursive domains is not implemented yet" and initial generation can cause "resource exhaustion"; bound your actual construction ([domain reference, Map/ReversibleMap/FlatMap/ReversibleFlatMap/Filter/Recursive Domains](https://raw.githubusercontent.com/google/fuzztest/1b4e4f0e4c446aca4660c43a28ec1b8d893b6510/doc/domains-reference.md)).

The Bazel quickstart requires Clang and Linux or experimental macOS support, with C++17 configuration. For an already configured target, distinguish unit-test mode, which runs tests "for a short time without sanitizer and coverage instrumentation", from fuzzing mode, which runs one test with instrumentation "until it finds a crash or it is explicitly terminated by the user" ([Bazel quickstart, Prerequisites and Create and run a fuzz test](https://raw.githubusercontent.com/google/fuzztest/1b4e4f0e4c446aca4660c43a28ec1b8d893b6510/doc/quickstart-bazel.md)):

```text
bazel test :TARGET
bazel run --config=fuzztest :TARGET -- --fuzz=SUITE.PROPERTY
```

The second command is only a mode-selection example; obtain duration/resource controls from `coverage-guided-fuzzing` and the installed version before launching a budgeted run. The property function "will be run with many different inputs in the same process"; it "should not `exit()` on any input", should ideally be deterministic because "Non-determinism can make fuzzing inefficient", and should ideally "not use any global state" ([property contract, The property function](https://raw.githubusercontent.com/google/fuzztest/1b4e4f0e4c446aca4660c43a28ec1b8d893b6510/doc/fuzz-test-macro.md)). General source is Apache-2.0 with specifically listed exceptions ([LICENSE](https://raw.githubusercontent.com/google/fuzztest/1b4e4f0e4c446aca4660c43a28ec1b8d893b6510/LICENSE)).

JavaScript: Fuzzilli generates JavaScript for engine shells that have been patched for its REPRL mode (its targets include V8, SpiderMonkey and JavaScriptCore) ([Fuzzilli README](https://raw.githubusercontent.com/googleprojectzero/fuzzilli/bee2fabef881f9360a4994ecce552c687633a8b1/README.md), [Fuzzilli targets](https://api.github.com/repos/googleprojectzero/fuzzilli/contents/Targets?ref=bee2fabef881f9360a4994ecce552c687633a8b1)); no generator was verified for Node-level program consumers such as bundlers, transpilers or template engines.

These tools illustrate generation mechanisms. When a target already owns suitable IR/choice and fixture construction, improve those owners rather than introduce a second parser, formatter or implementation just to use a named tool.
