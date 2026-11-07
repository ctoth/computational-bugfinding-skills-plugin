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

Three is an illustrative selected strength, not a required minimum. `/o` selects order, `/r` seed, `/e` seed rows and `/t` generator workers. `/s` selects statistics instead of rows; `/f:json` selects JSON ([actual parser](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/cli/cmdline.cpp)). Save rows, stderr, model, constraints, effective seed and binary identity; ordinary table output is tab-separated with a header ([PICT, Model File/Seeding](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md)).

`/b:N` tries deterministic consecutive seeds and chooses the smallest successful suite, breaking ties by earliest seed. It improves packing, not oracle strength; `/t` does not run target tests ([actual producer](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/cli/pict.cpp)). Avoid undocumented approximate/preview modes for a complete requested-coverage claim ([parser](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/cli/cmdline.cpp)).

## Interpret omissions before executing

Constrain generation instead of deleting invalid rows. Seed rows violating constraints are omitted, and unknown columns/values can lose seed information; retain mandatory regressions independently. Case comparison defaults to insensitive; aliases use their primary comparison name while output cycles spellings ([PICT guide](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md), [actual value producer](https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/cli/model.cpp)). Use separate values for behaviorally distinct spellings.

The generator does not execute configurations. The target's existing runner must apply saved values, verify effective configuration, execute meaningful inputs and capture the shared oracle. Keep generator failures, build failures, unapplied values and actual semantic mismatches distinct.

## ACTS availability boundary

The observed NIST page (2026-11-07; updated 2026-06-08) offers Basic ACTS directly, but constraint-capable Advanced ACTS requires a request; no request or service action is implied. It describes NIST software as public domain, not every dependency. Do not invent an acquired Advanced jar/CLI or substitute Basic for its constraints ([NIST distribution](https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software/downloadable-tools)). PICT is this skill's source-verified open route.
