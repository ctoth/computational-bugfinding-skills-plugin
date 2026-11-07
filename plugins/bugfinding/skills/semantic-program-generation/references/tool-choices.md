# Conditional tool choices

Documentation snapshot checked 2026-11-07. Recheck the selected release and existing project integration before execution; these examples were not run for this skill.

## Csmith: C programs

Use Csmith for a compatible C compiler target, not as a Go/MOO generator. In an existing installation, `csmith -h` and `csmith -hh` expose options; generated source is compiled with the installation's header include path. Preserve emitted source and selected compilers/configurations. The README warns that generated programs may not terminate, and differences can also originate in the generator. Its package/build instructions are platform-specific; no host installation is implied ([Csmith README](https://raw.githubusercontent.com/csmith-project/csmith/master/README.md)). The source uses a two-clause BSD license ([COPYING](https://raw.githubusercontent.com/csmith-project/csmith/master/COPYING)).

## FuzzTest: dependent C++ domains

Use constructive dependent domains for legal ranges/relationships. Check empty-container and overflow boundaries in the domain itself. Restrictive `Filter` predicates waste search; `Map`/`FlatMap` lack ordinary initial-seed support. Reversible variants require their inverse law. Recursive domains carry a documented recursion-limit warning in this snapshot; bound your actual construction ([domain reference, combinators](https://raw.githubusercontent.com/google/fuzztest/main/doc/domains-reference.md)).

The Bazel quickstart requires Clang and Linux or experimental macOS support, with C++17 configuration. For an already configured target, distinguish finite unit-test mode from instrumented fuzz mode ([Bazel quickstart](https://raw.githubusercontent.com/google/fuzztest/main/doc/quickstart-bazel.md)):

```text
bazel test :TARGET
bazel run --config=fuzztest :TARGET -- --fuzz=SUITE.PROPERTY
```

The second command is only a mode-selection example; obtain duration/resource controls from `coverage-guided-fuzzing` and the installed version before launching a budgeted run. Property calls share a process; avoid exiting and reset state needed for deterministic replay ([property contract](https://raw.githubusercontent.com/google/fuzztest/main/doc/fuzz-test-macro.md)). General source is Apache-2.0 with specifically listed exceptions ([LICENSE](https://raw.githubusercontent.com/google/fuzztest/main/LICENSE)).

These tools illustrate generation mechanisms. When a target already owns suitable IR/choice and fixture construction, improve those owners rather than introduce a second parser, formatter or implementation just to use a named tool.
