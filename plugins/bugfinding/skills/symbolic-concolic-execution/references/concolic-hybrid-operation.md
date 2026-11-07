# Concolic and hybrid operation

## Match compiler, runtime and dependencies

The inspected SymCC README describes best-effort maintenance and LLVM8-18/Z3/C++17 requirements. Its CMake contains differing LLVM-range warnings, and older configuration prose uses QSYM_BACKEND while actual compiler/runtime CMake uses SYMCC_RT_BACKEND. Verify one fitting selected tuple rather than merge contradictory instructions ([README](https://raw.githubusercontent.com/eurecom-s3/symcc/522c48070bc312aeb621a631ff130ded71507d6d/README.md), [compiler CMake](https://raw.githubusercontent.com/eurecom-s3/symcc/522c48070bc312aeb621a631ff130ded71507d6d/CMakeLists.txt), [configuration](https://raw.githubusercontent.com/eurecom-s3/symcc/522c48070bc312aeb621a631ff130ded71507d6d/docs/Configuration.txt), [selected runtime](https://raw.githubusercontent.com/eurecom-s3/symcc-rt/892f817f38f5abfa083dd0c1caa7ced821566bf5/CMakeLists.txt)).

Keep the parent-selected runtime submodule with its compiler. Existing builds use `symcc` or `sym++` as compiler wrappers; real target and dependency code must be included. Compiler source headers declare GPL3-or-later, runtime headers LGPL3-or-later; they are separate component declarations ([compiler](https://raw.githubusercontent.com/eurecom-s3/symcc/522c48070bc312aeb621a631ff130ded71507d6d/CMakeLists.txt), [runtime](https://raw.githubusercontent.com/eurecom-s3/symcc-rt/892f817f38f5abfa083dd0c1caa7ced821566bf5/CMakeLists.txt)). These source snapshots are evidence, not authority for dependency changes.

System C++ libraries can concretize tracked data; instrumented libc++ needs a matching dependency build. A process running successfully is not evidence that symbolic influence survived the boundary ([C++ integration](https://raw.githubusercontent.com/eurecom-s3/symcc/522c48070bc312aeb621a631ff130ded71507d6d/docs/C%2B%2B.txt)).

## Run a concrete seed and validate alternatives

In an existing compatible integration, compile the real C target with `symcc`, then use the following file-input shape. The target must actually read that exact seed. Paths are owned examples, and assignments shown are POSIX shell syntax ([README, usage](https://raw.githubusercontent.com/eurecom-s3/symcc/522c48070bc312aeb621a631ff130ded71507d6d/README.md), [runtime configuration](https://raw.githubusercontent.com/eurecom-s3/symcc/522c48070bc312aeb621a631ff130ded71507d6d/docs/Configuration.txt)).

```text
SYMCC_INPUT_FILE=/absolute/seed SYMCC_OUTPUT_DIR=/absolute/results ./sym_target /absolute/seed
```

Stdin is the default symbolic source unless configured otherwise; memory-symbolic input is a different mode. With the documented QSYM backend, stdin must be available at execution start. Preserve original bytes/arguments, generated files and actual target results; one run follows its concrete path and proposes alternatives for later runs ([README](https://raw.githubusercontent.com/eurecom-s3/symcc/522c48070bc312aeb621a631ff130ded71507d6d/README.md), [configuration](https://raw.githubusercontent.com/eurecom-s3/symcc/522c48070bc312aeb621a631ff130ded71507d6d/docs/Configuration.txt)).

The optional helper's documented shape is `symcc_fuzzing_helper -o AFL_OUT -a AFL_INSTANCE -n UNIQUE_LANE -- ./sym_target @@`. Its guide was tested with classic AFL2.56b; selected AFL++ compatibility needs actual verification. Match symbolic and coverage/sanitizer/semantic builds, use distinct output identities and replay alternatives through the real oracle ([hybrid guide](https://raw.githubusercontent.com/eurecom-s3/symcc/522c48070bc312aeb621a631ff130ded71507d6d/docs/Fuzzing.txt)).

Actual helper source uses a90-second attempt timeout, kill-after5s, forced pruning/linearization and its own coverage-map state. Those are selected-version mechanics, not a whole-job budget, completeness guarantee or AFL's live bitmap. Record generated/admitted/oracle-evaluated/replayed cases, killed attempts and total solver/replay cost; queue-file count is not confirmed defect count ([helper producer](https://raw.githubusercontent.com/eurecom-s3/symcc/522c48070bc312aeb621a631ff130ded71507d6d/util/symcc_fuzzing_helper/src/symcc.rs), [map/input configuration](https://raw.githubusercontent.com/eurecom-s3/symcc/522c48070bc312aeb621a631ff130ded71507d6d/docs/Configuration.txt)).

## Worked boundary

For this pack's illustrative hybrid experiment, take a real decoder with a difficult field relationship. Retain its setup, compile matched symbolic and actual-oracle builds, generate alternatives from a valid seed, then check the same promised effect natively. An unsupported library, pruned branch or timed-out attempt remains an explicit limitation. The guide separates generated testcase management from vulnerability checking; it does not make each new input a defect ([hybrid guide](https://raw.githubusercontent.com/eurecom-s3/symcc/522c48070bc312aeb621a631ff130ded71507d6d/docs/Fuzzing.txt)). Use `corpus-evolution` for compatible exchange and `evidence-based-triage` for attribution.
