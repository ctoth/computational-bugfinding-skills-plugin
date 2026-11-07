# Selected tool operation

Source snapshot: PICT ab76c2548f551fcb46314e58653a1bd1172f3a72, read 2026-11-07. Verify the installed artifact's supported options before use. These are source-checked shapes, not commands executed on a target.

## Setup and bounded generation

Use an existing fitting installation. The selected README documents Visual Studio 2022/VC++ and `_build.cmd` on Windows, or CMake with a C++ toolchain elsewhere; the actual license is MIT ([README](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/README.md), [license](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/LICENSE.TXT)). Optional documented source build:

```text
cmake -DCMAKE_BUILD_TYPE=Release -S . -B build
cmake --build build
```

For a subject-derived model and compatible saved regression rows:

```text
pict configurations.txt /o:3 /r:12345 /t:1 /e:regressions.tsv
```

Three is an illustrative selected strength, not a required minimum. `/o` selects order, `/r` seed, `/e` seed rows and `/t` generator workers. `/s` selects statistics instead of rows; `/f:json` selects JSON ([actual parser](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/cli/cmdline.cpp)). Save rows, stderr, model, constraints, effective seed and binary identity; in ordinary table output "The first line of the output contains names of the parameters" and values are tab-separated; a randomized run prints its seed "to the error output stream" ([PICT, Output Format](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md)).

`/b:N` tries deterministic consecutive seeds and chooses the smallest successful suite: "smallest suite wins, ties broken by earliest seed" ([actual producer, `findBestSeed`](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/cli/pict.cpp)). It improves packing, not oracle strength; the guide says the seed "does not relax the requested coverage target" and that parallelism "never changes the produced test suite", so `/t` does not run target tests ([PICT, Output Format and Parallelism](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md)). Avoid the undocumented `/x` and `/p` modes for a complete requested-coverage claim; their usage lines are commented out, and `/x` is "best effort, might not cover all combinations" ([parser, `showUsage`](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/cli/cmdline.cpp)).

## Interpret omissions before executing

Constrain generation instead of deleting invalid rows. A seed row that violates constraints "will be skipped entirely", and unknown columns/values are ignored, so a complete row can become partial; retain mandatory regressions independently. By default PICT "does all its comparisons and checks case-insensitively" (`/c` makes them case-sensitive); for aliases "only the first name counts" in constraints while output rotates names ([PICT, Seeding, Case Sensitiveness and Aliasing](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md), [actual value producer](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/cli/model.cpp)). Use separate values for behaviorally distinct spellings.

The generator does not execute configurations; PICT "accepts a plain-text model file as an input and produces a set of test cases" ([PICT, Usage](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md)). The target's existing runner must apply saved values, verify effective configuration, execute meaningful inputs and capture the shared oracle. Keep generator failures, build failures, unapplied values and actual semantic mismatches distinct.

## ACTS availability boundary

The observed NIST page (2026-11-07; updated 2026-06-08) offers the ACTS Basic version as a direct ".jar file" download, but for "the advanced ACTS tool, which supports constraints" it says "please send a request"; no request or service action is implied. It says "this software is public domain" about NIST's own software and says nothing about third-party dependencies. The page names constraint support only for the advanced tool, so do not invent an acquired Advanced jar/CLI or assume Basic provides its constraints ([NIST distribution, Downloadable Tools](https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software/downloadable-tools)). PICT is this skill's source-verified open route.
