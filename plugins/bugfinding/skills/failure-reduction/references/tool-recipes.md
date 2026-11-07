# Conditional reducer recipes

Examples below are source-documented recipes, not executed demonstrations. Numbers illustrate finite limits; select them from the actual task. Keep an untouched original and use separate writable reduction artifacts. Build/instrumentation setup belongs to the relevant runtime skill.

## C-Reduce

For a compatible existing installation, inspect `creduce --version` and `creduce --help`. Its test accepts no arguments, runs in a fresh temporary directory containing candidate basenames, and accepts exit zero. Resolve fixed tools/fixtures absolutely; inspect reducible files relative to that directory. `--n` controls cores and `--timeout` bounds one test ([executable contract](https://raw.githubusercontent.com/csmith-project/creduce/master/creduce/creduce.in)).

```sh
creduce --n 1 --timeout 60 /absolute/interesting.sh case.c
```

The interestingness program must encode the selected validity/witness conditions, not any failure. Test its calling convention before reduction. `--not-c` omits C/C++ passes; it does not supply another language's semantic validity check ([options](https://raw.githubusercontent.com/csmith-project/creduce/master/creduce/creduce.in)).

The repository's installation guide names OS packages and historical LLVM 9 source prerequisites. Verify the chosen release/package instead of treating that page as a modern support matrix; no Windows compatibility is established here ([install guide](https://raw.githubusercontent.com/csmith-project/creduce/master/INSTALL.md)). C-Reduce uses the University of Illinois Open Source License ([COPYING](https://raw.githubusercontent.com/csmith-project/creduce/master/COPYING)).

## LLVM IR or MIR

Use matching installed LLVM tools and the actual IR/MIR dialect. llvm-reduce passes the candidate path to its test; its documented example uses the first argument. Run the selected failure-producing toolchain inside that test ([guide and example](https://llvm.org/docs/CommandGuide/llvm-reduce.html)).

```sh
llvm-reduce --test=/absolute/interesting.sh --max-pass-iterations=5 -j 1 case.ll
```

Choose format/passes from installed help. `--in-place` overwrites input; `--abort-on-invalid-reduction` stops on invalid IR. Normal reducer exit is distinct from final target replay. Keep ordinary interestingness verification: `--skip-verify-interesting-after-counting-chunks` suppresses a flaky-reproducer warning ([options and exit status](https://llvm.org/docs/CommandGuide/llvm-reduce.html)). LLVM is Apache-2.0 with LLVM exceptions ([license](https://raw.githubusercontent.com/llvm/llvm-project/main/LICENSE.TXT)).

## libFuzzer crash input

Run the same compatible target binary, instrumentation and relevant options used for the original:

```sh
./fuzz_target -minimize_crash=1 -max_total_time=300 -exact_artifact_path=reduced-case original-case
```

`-minimize_crash` reduces the supplied crash; `-merge=1` minimizes retained coverage-corpus material, and `-reduce_inputs` preserves observed feature sets. These goals differ. Use a distinct exact artifact path for each parallel process, then replay the reduced file against the selected semantic predicate ([libFuzzer options](https://llvm.org/docs/LibFuzzer.html#options)). A crash-preserving engine does not independently check a world-effect witness. LLVM licensing is noted above.

## Existing Go or Hypothesis shrinker

Keep Go corpus argument types and ordering. Choice bytes and generated source are different inputs; retain both when regeneration matters. Use the emitted focused selector such as `go test -run=FuzzName/CASE_ID` in the authorized runner. `-fuzzminimizetime` limits each minimization attempt, not the whole job ([Go failing input and settings](https://go.dev/doc/security/fuzz/)).

For Hypothesis, use the maintained generator/shrinker for dependent values. `@example` replays explicit values but does not shrink them. Database keys can change with tests, and reproduction blobs are version-sensitive; preserve readable arguments and compatible version identity, then retain a proper regression ([replay guide](https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html)). State-model design belongs to `stateful-property-testing`; this recipe does not introduce a standalone shrink API or new package dependency.
