# Improve coverage-guided-fuzzing

Target: `plugins/bugfinding/skills/coverage-guided-fuzzing/` (SKILL.md + references/).

## Findings

Method: every cited source was downloaded at a pinned commit (raw GitHub) or fetched at its published URL into the session scratchpad and grepped/read for each claim. Repos resolved with `gh api repos/<org>/<repo>/commits/<branch> --jq .sha` on 2026-11-07.

### F1 WARNING — Rust Fuzz Book links are moving GitHub Pages URLs
- Where: `SKILL.md:12`, `references/go-rust.md:19,26,28`, `references/common-mistakes.md:5,10`, `references/reach-reset-feedback.md:11`.
- Text: `https://rust-fuzz.github.io/book/cargo-fuzz/{setup,guide,coverage,windows/setup}.html` (rebuilt from `rust-fuzz/book` master on every push).
- Source: same content at `https://raw.githubusercontent.com/rust-fuzz/book/18cfe0e68cfee717392552d3511bac08458d2c01/src/cargo-fuzz/{setup,guide,coverage,windows/setup}.md`. Guide: "Note that these options control the `fuzz_targets` crate"; coverage: "runs the program _without fuzzing_ on the provided corpus"; setup: "This project requires the nightly compiler".
- Fix: pinned all four; added those quote fragments where the claim is load-bearing.

### F2 WARNING — FuzzTest flag claims check out; URL moving
- Where: `references/cpp-fuzztest.md:11`, `references/common-mistakes.md:12`.
- Source (`google/fuzztest@1b4e4f0e`, doc/flags-reference.md): `--fuzz=MySuite.MyTest` "Run a fuzz test in fuzzing mode indefinitely"; `--fuzz_for=T` "Run all fuzz tests in fuzzing mode for `T` duration"; `--rss_limit_mb`, `--time_limit_per_input` separate rows. Text is accurate.
- Fix: pinned URL; added quote.

### F3 ERROR — sanitizer memory-cap claim cited to a page that does not say it
- Where: `references/native-runners.md:17`.
- Text: "sanitizer address-space reservations can make a virtual-memory cap inappropriate ... ([AFL++ memory limits](https://aflplus.plus/docs/fuzzing_in_depth/))".
- Source: `docs/fuzzing_in_depth.md@d0070729` §3.b only says "Memory limits are not enforced by afl-fuzz by default" and recommends `-m`; nothing about sanitizer address space. §3.k says only "There are some unfortunate trade-offs with ASAN and 64-bit binaries." The address-space statement is in `utils/asan_cgroups/limit_memory.sh@d0070729`: limits "actual memory allocated ... using cgroups, instead of the traditional setrlimit() API. This helps avoid the address space problems". `src/afl-fuzz.c` help: "`-m megs - memory limit for child process (%u MB, 0 = no limit [default])`".
- Fix: re-cited to depth §3.k (quote) plus the pinned cgroups script (quote); stated the default no-limit fact from the help text.

### F4 WARNING — CmpLog memory caveat missing
- Where: `references/native-runners.md:21`.
- Source: `instrumentation/README.cmplog.md@d0070729`: "Be careful with the usage of `-m` because CmpLog can map a lot of pages." Its own example uses `-m none`.
- Fix: one clause added to the CmpLog sentence with the quote.

### F5 INFO — AFL++ CLI, install, persistent, custom-mutator, licensing claims verified
- `src/afl-fuzz.c@d0070729` help: `-V seconds` "fuzz for a specified time then terminate (fuzz time only!)"; `-E execs` "Note: not precise and can have several more executions"; `-t msec` "timeout for each run"; `-Q` (Linux-only `#if`), `-O` FRIDA; `-n` "fuzz without instrumentation (non-instrumented mode)"; `-c program` "enable CmpLog by specifying a binary compiled for it".
- `docs/INSTALL.md`: "We recommend llvm 18 or newer, minimum is 14."; "`afl-clang-lto`, `afl-gcc-fast` and `qemu_mode` are not working on macOS"; FRIDA `-O` works on macOS. Depth §1.a diagram still says "clang/clang++ 11+" and "anything below 9 is not recommended" (supports the "older compiler diagram" sentence).
- `instrumentation/README.persistent_mode.md`: "earlier runs will have no impact on future runs"; stability drop "then the fuzz target keeps state"; deferred init must not follow "The creation of any vital threads or child processes" nor "Any access to the fuzzed input".
- `docs/custom_mutators.md`: `AFL_CUSTOM_MUTATOR_LIBRARY`/`AFL_PYTHON_MODULE`; "If `AFL_CUSTOM_MUTATOR_ONLY` is set, all mutations will solely be performed with the custom mutator"; `afl_realloc()` "otherwise afl-fuzz will crash when trying to free your buffers"; generic trimming "can easily destroy the structure of complex formats".
- `LICENSING.md`: "AGPL-3.0-or-later"; per-file `SPDX-License-Identifier` governs.
- Fix: added quote fragments at load-bearing points; no content change needed.

### F6 WARNING — AFL++ Fuzzing in Depth cited at moving website URL
- Where: `SKILL.md:8`, `references/native-runners.md:7,15,17`.
- Text: `https://aflplus.plus/docs/fuzzing_in_depth/` (website, tracks a branch).
- Source pinned: `https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/docs/fuzzing_in_depth.md`. SKILL.md:8 claim supported by §3.g: "The `corpus count` value is a bad indicator for checking how good the coverage is."
- Fix: pinned; added §3.g quote to SKILL.md:8; section labels added.

### F7 WARNING — libFuzzer cited at moving llvm.org/docs; claims verified
- Where: `SKILL.md:12`, `references/native-runners.md:29-39`, `references/reach-reset-feedback.md:7`.
- Source: LLVM converted the page to Markdown; read `https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/LibFuzzer.md` (the `.rst` path 404s at that SHA). Verified: "Note that `-fsanitize=fuzzer` links in the libFuzzer's `main()` symbol" plus `fuzzer-no-link`; "LibFuzzer requires a matching version of Clang."; "execute the fuzz target many times with different inputs in the same process"; "It must not `exit()` on any input."; files passed instead of dirs: "will re-run those files as test inputs but will not perform any fuzzing"; -1 return: "will not add that input top the corpus, regardless of what coverage it triggers" (sic); `-exact_artifact_path` "Do not use the same path for several parallel processes."; Status: "please do not expect major new features"; output fields `cov:`/`ft:`/`corp:`/`exec/s:`/`rss:` defined separately.
- Gap found: `-rss_limit_mb` entry says "If running w/o ASAN/MSAN, you may use 'ulimit -v' instead." This is the primary statement behind the sanitizer/virtual-memory caveat (F3).
- Fix: pinned to the raw `.md` at the SHA; added quotes; used the `ulimit -v` sentence as a second citation for the memory caveat.

### F8 ERROR — Go `-timeout` presented as a bound on the fuzzing run; it is stopped before fuzzing starts
- Where: `references/go-rust.md:10,13`.
- Text: command `... -fuzztime=5m -parallel=2 -timeout=8m` and "Fuzz duration, worker processes, each minimization attempt and test-binary timeout are different limits."
- Source: `cmd/go` docs `-timeout d`: "If a test binary runs longer than duration d, panic." But `src/testing/testing.go` at go1.27.3 (`2aae1000ea1d4b28923b96db28acf4e3b99d6aff`) lines 2596-2630: `deadline := m.startAlarm()` ... runs tests and seed corpora ... `m.stopAlarm()`, and only then `fuzzingOk := runFuzzing(m.deps, m.fuzzTargets)`. `src/cmd/go/internal/test/test.go:825` sets the backup kill timer only `if testTimeout > 0 && testFuzz == "" && testBench == ""`. So `-timeout` covers the pre-fuzz test/seed phase only; `-fuzztime` (default "run forever") plus per-attempt `-fuzzminimizetime` (default 60s) bound the search; an outer wall bound must come from outside `go test`.
- Fix: corrected the sentence and kept the command; cited pinned source lines.

### F9 WARNING — Go docs moving URLs
- Where: `SKILL.md:27,35`, `references/go-rust.md:13,15`, `references/reach-reset-feedback.md:21`.
- Text: `https://go.dev/doc/security/fuzz/` and `https://pkg.go.dev/cmd/go#hdr-Testing_flags`.
- Source: pinned `https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/security/fuzz/index.md` and `https://pkg.go.dev/cmd/go@go1.27.3#hdr-Testing_flags`. Verified: "currently AMD64 and ARM64"; "regexp must match exactly one fuzz test within that package"; types "must match the fuzzing arguments exactly, in that order"; "the state of a fuzz target should not persist past the end of each call"; default `go test` runs seed corpus "much like a unit test".
- Fix: pinned; added quotes.

### F10 WARNING — Atheris links on moving `master`; claims verified
- Where: `references/python-jvm.md:7-17`, `references/common-mistakes.md:11`.
- Source pinned at `google/atheris@e36da74cf42b5834c4e31d7cabb58d796695d29f`: README "Atheris supports Linux (32- and 64-bit) and Mac OS X, Python versions 3.11-3.14."; "You must call `atheris.Setup()` before `atheris.Fuzz()`."; no-interesting-inputs error "if the first 2 calls to `TestOneInput` didn't produce any coverage events"; "Atheris will report a failure if the Python code under test throws an uncaught exception."; "Coverage reports are only generated when your fuzzer exits gracefully"; "or due to libFuzzer's `-runs` flag (use `-atheris_runs`)". native_extension_fuzzing.md: "must be built with Clang, using the argument `-fsanitize=fuzzer-no-link`"; preload option "is not yet supported on Mac"; modified-CPython route is "for Python 3.8.6".
- Fix: pinned; added quotes; added the macOS preload limitation (one clause) since the sentence already tells the reader to verify the platform route.

### F11 ERROR — Jazzer claims cited to README that the README does not contain
- Where: `references/python-jvm.md:27`.
- Text: "Only one fuzz test runs per discovery invocation. Keep crashing inputs, generated corpus and typed Java reproducer artifacts distinct ([Jazzer README](...))".
- Source: README@`a4e09fbb` says only "Jazzer will execute a single fuzz test" in the fuzzing-mode section and defines inputs directory vs `.cifuzz-corpus`; it never mentions Java reproducers. The one-test rule is stated in `FuzzTest.java`: "In fuzzing mode, only a single fuzz test per test run will be executed." Java reproducers are in `docs/arguments-and-configuration-options.md`: `reproducer_path` "Directory in which stand-alone Java reproducers are stored for each finding".
- Fix: added FuzzTest.java and the configuration-options doc as citations with quotes; new sources.yaml entry.

### F12 INFO — Jazzer lifecycle/limits verified; strongest quote added
- `FuzzTest.java@a4e09fbb`: `maxDuration() default "5m"`; "This option has no effect during regression testing."; overridable via `jazzer.max_duration`/`jazzer.max_executions`; "fuzz tests always go through the full JUnit lifecycle for every execution"; `lifecycle() default Lifecycle.PER_TEST`. `Lifecycle.java`: PER_TEST is "more likely to unintentionally preserve state between fuzz test executions, which can result in non-reproducible findings"; PER_EXECUTION "every execution uses its own test class instance"; "may be invoked concurrently". README platforms: "Linux x86_64 & arm64", "macOS 12+ x86_64 & arm64", "Windows x86_64"; "By default, Jazzer operates in regression mode".
- Fix: pinned (moving `main`); added quotes; noted 5m is already the annotation default.

### F13 INFO — FuzzTest quickstart/fixtures verified; URLs moving
- Where: `references/cpp-fuzztest.md:3,11,13,15`, `SKILL.md:27`.
- Source `google/fuzztest@1b4e4f0e4c446aca4660c43a28ec1b8d893b6510`: prerequisites "A Linux-based operating system or macOS (experimental)", Clang, Bazel; `.bazelrc` "Use the C++17 standard."; unit mode "without sanitizer and coverage instrumentation"; fuzzing mode "keeps running the test with different input values until it finds a crash or it is explicitly terminated by the user"; quickstart pins `version = "20241028.0"`. Fixtures: "BEST PRACTICE: Make sure that the property function resets the mutated fixture"; per-iteration "should be the more common one"; per-fuzz-test "relies on the fixture being easily resettable". LICENSE begins with per-file sections (`Files: fuzztest/internal/domains/rune.*`) then Apache 2.0.
- Fix: pinned; added quotes.

### F14 WARNING — Surefire page is unversioned; Google structure-aware guide on `master`
- Where: `references/python-jvm.md:27`; `SKILL.md:29`, `references/reach-reset-feedback.md:8`.
- Source: Surefire current site is 3.6.1 (no 3.6.1 archive; 404). Archived `https://maven.apache.org/surefire-archives/surefire-3.5.4/maven-surefire-plugin/examples/single-test.html` contains "set the test property to a specific test case" and `mvn -Dtest=TestCircle test`. Structure-aware guide pinned at `google/fuzzing@734e55f3cfed1adbb51bf6cb5c65b4c1197b7089`: mutations on compressed data cause "virtually all generated inputs to be invalid for `uncompress`".
- Fix: pinned both; added quotes.

### F15 INFO — Rebert et al. claims re-checked against page images
- Where: `SKILL.md:37`, `references/common-mistakes.md:13`.
- Read this session through paper-reader page images `pngs/page-004.png`, `page-011.png`, `page-013.png` in `C:/Users/Q/code/bugfinding-literature/corpus-evolution/papers/Rebert_2014_OptimizingSeedSelection/` (paper-reader collection; PDF at the cited URL is the same 377516-byte file). p.864: "We assume we are given t seconds to perform the data reduction"; p.871: "Hypothesis 4 is therefore false under the optimal scheduling." with Round-Robin used "more realistically"; p.873: Figure 6 "Transferability of UNWEIGHTED MINSET coverage across configurations" and "We have performed initial hypothesis testing". Claims hold.
- Fix: added two quote fragments.

### F16 WARNING — uncited normative sentences in SKILL.md
- `SKILL.md:29` "Observe decoder admission ... separately from engine coverage." — now cited to structure-aware guide (compression example) and AFL++ depth §3.g.
- `SKILL.md:31` "Use separate owned outputs ..." — cited to libFuzzer `-exact_artifact_path` "Do not use the same path for several parallel processes."
- Not cited (deliberately): pack routing/authority sentences (`SKILL.md:14,23` second half, `:37`, `:39`; reference-file routing tails). They state this pack's division of responsibility, not external facts; the foundation skill leaves the same kind of sentence uncited.

### F17 WARNING — common-mistakes rows lacked an explicit one-line why
- Where: `references/common-mistakes.md:3-13`.
- Text: two-column table "Misleading conclusion | Correction"; rows 1 and 6 had no reason, others mixed reason into the action.
- Fix: same rows, header changed to `Wrong | Right | Why`, each row split into action and one-line why with the existing citations plus quotes. No rows added or dropped.

### F18 INFO — remaining moving URLs pinned
- LLVM license `/main/` → `llvm/llvm-project@635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/LICENSE.TXT` ("The LLVM Project is under the Apache License v2.0 with LLVM Exceptions").
- cargo-fuzz manifest `/master/` (default branch is now `main`) → `rust-fuzz/cargo-fuzz@bf2fc668dafda5295aa6fd01825ee67b885f0f2b/Cargo.toml` (`version = "0.13.2"`, `license = "MIT OR Apache-2.0"`).
- Atheris LICENSE, Jazzer LICENSE, FuzzTest LICENSE pinned at the SHAs above (Apache 2.0 text verified).

### F19 INFO — common-mistakes gains the Go `-timeout` row from F8
- Where: `references/common-mistakes.md` (new row after the AFL `-V` row).
- Fix: Wrong "`go test -timeout=8m` caps the fuzzing run." / Right: bound with `-fuzztime`, account for `-fuzzminimizetime`, enforce wall bound outside `go test` / Why: `m.stopAlarm()` before `runFuzzing(...)`, cited to pinned go1.27.3 `testing.go`. Same error class as the existing AFL `-V` row; no new machinery.

### Counts
ERROR 3 (F3, F8, F11); WARNING 10 (F1, F2, F4, F6, F7, F9, F10, F14, F16, F17); INFO 6 (F5, F12, F13, F15, F18, F19). Claims cut: 0 (every challenged claim had a primary source once re-cited or corrected). Command changed: `-timeout=8m` removed from the Go example (F8).

## Pinned URLs

| Before (moving) | After (pinned) |
|---|---|
| `https://aflplus.plus/docs/fuzzing_in_depth/` | `https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/docs/fuzzing_in_depth.md` |
| `https://llvm.org/docs/LibFuzzer.html` | `https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/llvm/docs/LibFuzzer.md` |
| `https://raw.githubusercontent.com/llvm/llvm-project/main/LICENSE.TXT` | `.../llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/LICENSE.TXT` |
| `https://go.dev/doc/security/fuzz/` | `https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/security/fuzz/index.md` |
| `https://pkg.go.dev/cmd/go#hdr-Testing_flags` | `https://pkg.go.dev/cmd/go@go1.27.3#hdr-Testing_flags` |
| `https://rust-fuzz.github.io/book/cargo-fuzz/{setup,guide,coverage,windows/setup}.html` | `https://raw.githubusercontent.com/rust-fuzz/book/18cfe0e68cfee717392552d3511bac08458d2c01/src/cargo-fuzz/{setup,guide,coverage,windows/setup}.md` |
| `.../rust-fuzz/cargo-fuzz/master/Cargo.toml` | `.../rust-fuzz/cargo-fuzz/bf2fc668dafda5295aa6fd01825ee67b885f0f2b/Cargo.toml` |
| `.../google/atheris/master/{README.md,native_extension_fuzzing.md,LICENSE}` | `.../google/atheris/e36da74cf42b5834c4e31d7cabb58d796695d29f/...` |
| `.../CodeIntelligenceTesting/jazzer/main/{README.md,LICENSE,FuzzTest.java,Lifecycle.java}` | `.../jazzer/a4e09fbbc775d129ce61d5802e893160e31a6d40/...` |
| `.../google/fuzztest/main/{doc/quickstart-bazel.md,doc/flags-reference.md,doc/fixtures.md,LICENSE}` | `.../google/fuzztest/1b4e4f0e4c446aca4660c43a28ec1b8d893b6510/...` |
| `.../google/fuzzing/master/docs/structure-aware-fuzzing.md` | `.../google/fuzzing/734e55f3cfed1adbb51bf6cb5c65b4c1197b7089/docs/structure-aware-fuzzing.md` |
| `https://maven.apache.org/surefire/maven-surefire-plugin/examples/single-test.html` | `https://maven.apache.org/surefire-archives/surefire-3.5.4/maven-surefire-plugin/examples/single-test.html` |

23 moving URLs replaced. New pinned sources added: AFL++ `utils/asan_cgroups/limit_memory.sh`, Jazzer `docs/arguments-and-configuration-options.md`, Go `src/testing/testing.go` and `src/cmd/go/internal/test/test.go` at go1.27.3 (`2aae1000ea1d4b28923b96db28acf4e3b99d6aff`). Already pinned and kept: AFL++ INSTALL/afl-fuzz.c/LICENSING/persistent/CmpLog/custom-mutators at `d0070729` (still the `stable` head on 2026-11-07), Rebert PDF.

## Validation

All commands run from the repository root on 2026-11-07.

```text
$ python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/coverage-guided-fuzzing
Skill is valid!

$ python -I -c "<read-only probe: sources.yaml vs inline URLs, fields, local links, EOF>"
sources 34 cited 34
orphan cited (not in yaml): []
unused yaml: []
dup yaml urls: 0
field errors: []
other errors: [9 hits, all '/main/' inside the Jazzer Java path src/main/java/..., not a branch]

$ python -I -c "<refined probe: raw.githubusercontent ref segment must be a 40-hex SHA; other hosts no /main|master|HEAD|latest|stable/>"
moving/unpinned URLs: []

$ git diff --check -- plugins/bugfinding/skills/coverage-guided-fuzzing
(no output; exit 0)

Line counts: SKILL.md 39; common-mistakes.md 16; cpp-fuzztest.md 15; go-rust.md 32; native-runners.md 39; python-jvm.md 33; reach-reset-feedback.md 23; sources.yaml 244.
```

Quote check: a read-only script searched every `"..."` fragment in SKILL.md and references/*.md against the downloaded pinned sources (whitespace-normalized). Every fragment matched except the two Rebert fragments, which come from page images (F15) and were checked by eye; the parse artifacts around code spans containing `"` were then spot-checked with `grep -c` (all 1).

Skill-audit checks 1-6: frontmatter has name/description only, name matches directory; description still matches body (AFL++, libFuzzer, Go, cargo-fuzz, Atheris, Jazzer, FuzzTest, low useful coverage); SKILL.md 39 lines (≤500); local links (four references + reach-reset-feedback + common-mistakes + go-rust from SKILL.md) resolve; no filler found.

## Unverified

- `https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-rebert.pdf`: local curl fails with libcurl error 43 (a client issue); Python `urllib` fetched it (200, `application/pdf`, 377516 bytes, same size as the paper-reader `paper.pdf`). Paper content was checked only on pages 864, 871, 873.
- The AFL++ website page (`aflplus.plus/docs/fuzzing_in_depth/`) returns 200 but was not compared line-by-line with the pinned `stable` markdown; the skill now cites only the pinned markdown.
- `pkg.go.dev/cmd/go@go1.27.3` text was read; the `-timeout` behavior was confirmed in go1.27.3 source by reading, not by running a fuzz test with a short `-timeout`.
- No fuzzer, compiler or build was executed; all commands in the skill remain unexecuted examples.
- Fetches used `curl`/`gh api` (raw files) instead of the WebFetch tool; content was read from the downloaded files in the session scratchpad.
