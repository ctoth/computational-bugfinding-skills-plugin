# Conditional reducer recipes

Examples below are source-documented recipes, not executed demonstrations. Numbers illustrate finite limits; select them from the actual task. Keep an untouched original and use separate writable reduction artifacts. Build/instrumentation setup belongs to the relevant runtime skill.

## C-Reduce

For a compatible existing installation, inspect `creduce --version` and `creduce --help`. Its test "should be deterministic and should not expect any command line arguments", runs in "a fresh temporary directory containing only the partially reduced file(s)", and accepts exit zero. Resolve fixed tools/fixtures absolutely; inspect reducible files relative to that directory. `--n` controls cores and `--timeout` bounds one test (default 300 seconds). The files to reduce "must be writable": C-Reduce rewrites them in place and keeps a `file.orig` backup unless `--tidy` is given. Before reducing, its sanity check runs the test on the unmodified files in a fresh temporary directory and exits if the test "does not return zero" ([executable contract](https://raw.githubusercontent.com/csmith-project/creduce/31e855e290970cba0286e5032971509c0e7c0a80/creduce/creduce.in)).

```sh
creduce --n 1 --timeout 60 /absolute/interesting.sh case.c
```

The interestingness program must encode the selected validity/witness conditions, not any failure. Test its calling convention before reduction. `--not-c` omits C/C++ passes; it does not supply another language's semantic validity check. Only exit zero is interesting; to keep a variant showing a different genuine violation, `--also-interesting <exitcode>` makes C-Reduce "save a copy of the variant" when the test returns that code ([options](https://raw.githubusercontent.com/csmith-project/creduce/31e855e290970cba0286e5032971509c0e7c0a80/creduce/creduce.in)).

The repository's installation guide names OS packages and historical LLVM/Clang 9.0.0 source prerequisites. Verify the chosen release/package instead of treating that page as a modern support matrix; no Windows compatibility is established here ([install guide](https://raw.githubusercontent.com/csmith-project/creduce/31e855e290970cba0286e5032971509c0e7c0a80/INSTALL.md)). C-Reduce uses the "University of Illinois Open Source License." ([COPYING](https://raw.githubusercontent.com/csmith-project/creduce/31e855e290970cba0286e5032971509c0e7c0a80/COPYING)).

## LLVM IR or MIR

Use matching installed LLVM tools and the actual IR/MIR dialect. llvm-reduce passes the candidate path to its test; its documented example script reads it as `$1`, and `--test-arg` passes extra arguments. Run the selected failure-producing toolchain inside that test ([guide and example](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/CommandGuide/llvm-reduce.md)).

```sh
llvm-reduce --test=/absolute/interesting.sh --max-pass-iterations=5 -j 1 case.ll
```

Choose format/passes from installed help. `--in-place` "will replace your input file with the reduced version"; `--abort-on-invalid-reduction` aborts "if any reduction results in invalid IR". Normal reducer exit is distinct from final target replay; exit 2 means "the interestingness test reported the initial input was not interesting". Keep ordinary interestingness verification: with `--skip-verify-interesting-after-counting-chunks`, "a warning will no longer be printed on flaky reproducers" ([options and exit status](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/CommandGuide/llvm-reduce.md)). LLVM is under the "Apache License v2.0 with LLVM Exceptions" ([license](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/LICENSE.TXT)).

## libFuzzer crash input

Run the same compatible target binary, instrumentation and relevant options used for the original:

```sh
./fuzz_target -minimize_crash=1 -max_total_time=300 -exact_artifact_path=reduced-case original-case
```

`-minimize_crash=1` "minimizes the provided crash input"; `-merge=1` minimizes a corpus "while still preserving the full coverage", and `-reduce_inputs` shrinks inputs "while preserving their full feature sets". These goals differ. "Do not use the same path for several parallel processes" with `-exact_artifact_path`, then replay the reduced file against the selected semantic predicate ([libFuzzer corpus and options](https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/LibFuzzer.md)). A crash-preserving engine does not independently check a world-effect witness. LLVM licensing is noted above.

## Existing Go or Hypothesis shrinker

Keep Go corpus argument types and ordering: corpus values "must match the fuzzing arguments exactly, in that order". Choice bytes and generated source are different inputs; retain both when regeneration matters. Use the emitted focused selector such as `go test -run=FuzzName/CASE_ID` in the authorized runner. Go minimizes toward a value "which will still produce an error", meaning any error, so replay the minimized entry against the selected predicate. `-fuzzminimizetime` limits each minimization attempt, not the whole job ([Go failing input, settings and corpus format](https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/security/fuzz/index.md)).

For Hypothesis, use the maintained generator/shrinker for dependent values. `@example` replays explicit values, but "examples provided using |@example| do not shrink". Changes to a test's source "may also change its database key", and the reproduction blob "is not stable across Hypothesis versions"; preserve readable arguments and compatible version identity, then retain a proper regression ([replay guide](https://raw.githubusercontent.com/HypothesisWorks/hypothesis/9ab0be61aaaa27396fc1bbf4b34e7925cc68d1e2/hypothesis/docs/tutorial/replaying-failures.rst)). State-model design belongs to `stateful-property-testing`; this recipe does not introduce a standalone shrink API or new package dependency.
