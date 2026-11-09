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

## JavaScript and TypeScript

For fast-check inputs, use its own shrinker and retain `seed`, `path` and `replayPath` as described in [stateful-property-testing runtime recipes](../../stateful-property-testing/references/runtime-recipes.md). The fast-check scheduler does not shrink schedules ([schedule-exploration, JavaScript event loop](../../schedule-exploration/references/javascript-event-loop.md)).

For a Jazzer.js crash file, libFuzzer flags go after `--` (`jazzer <fuzzTarget> <fuzzerFlags> [corpus...] [-- <fuzzingEngineFlags>]`) ([Jazzer.js fuzz targets, CLI](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer.js/f23bc5aeb7a6d50cd6256cfc3be44b868da5e7b1/docs/fuzz-targets.md)). Jazzer.js source lists `minimize_crash` among the flags that "cause libFuzzer to spawn subprocesses" and wraps the command for it ([Jazzer.js core options](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer.js/f23bc5aeb7a6d50cd6256cfc3be44b868da5e7b1/packages/core/options.ts)), but its documentation never mentions minimization; treat the following composed command as unexercised:

```sh
npx jazzer <fuzzTarget> crash-<hash> -- -minimize_crash=1 -max_total_time=300
```

Replay the result with `npx jazzer <fuzzTarget> <reduced-file>`, which runs listed inputs "once and exit" ([Jazzer.js fuzzing settings](https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer.js/f23bc5aeb7a6d50cd6256cfc3be44b868da5e7b1/docs/fuzz-settings.md)), and check the selected predicate, because the libFuzzer section above minimizes toward any crash. Fuzz setup belongs to [Jazzer.js](../../coverage-guided-fuzzing/references/node-jazzerjs.md); corpus merge belongs to `corpus-evolution`.

For JavaScript source text, three generic reducers apply; none was executed here:

- **Perses** lists "javascript: `*.javascript`, `*.js`" as supported, while the same README later says "Currently, Perses supports C, Rust, Java and Go". Its test script must return 0 when interesting ([Perses README](https://raw.githubusercontent.com/uw-pluverse/perses/52d6b501f257385d5b50dfe68780986c19136abf/README.md)).
- **Lithium** treats lines as atomic units, which "is great if each line is a JavaScript statement"; "don't use --char when trying to reduce a long sequence of JavaScript statements" ([Lithium README](https://raw.githubusercontent.com/MozillaSecurity/lithium/8b567a5f7572240fc15d25ad0df173f2008010a3/README.md)).
- **Shrink Ray** runs `shrinkray is_interesting.sh my-test-case` and has no JavaScript-specific format. Its LLM mode "is enabled by default" and its first use downloads a model of "about 2.7GB"; pass `--no-llm` unless that download is authorized ([Shrink Ray README](https://raw.githubusercontent.com/DRMacIver/shrinkray/5fe6ee135d732e4b7758b3dbe3d91428523018fb/README.md)).

For a Playwright test, measure the replay rate with `--repeat-each <N>` ("Run each test `N` times") and retries off ([Playwright CLI](https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/docs/src/test-cli-js.md)). A retry is not a replay: after a failure Playwright will "discard the entire worker process along with the browser and will start a new one", and a test that fails then passes on retry is labelled "flaky" ([Playwright retries](https://raw.githubusercontent.com/microsoft/playwright/95e5dca31981bcd0970165853fcc713269d2433a/docs/src/test-retries-js.md)).
