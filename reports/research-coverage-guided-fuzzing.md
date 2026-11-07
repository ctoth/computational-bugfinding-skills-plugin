# Research: coverage-guided-fuzzing

Date: 2026-11-07

## State

Per-skill primary-source research complete for drafting. This report is the only owned repository output. Literature uses paper-reader and page images only. No target execution, installs, target changes, commits or publication.

## Evidence ledger

Checking actual runtime instrumentation, harness/reset contracts, supported command shapes, current tool restrictions and selected-ref licensing. Tool names and inherited reports are discovery leads, not primary evidence.

## Early verified primary findings

- AFL++ selected stable ref `d0070729206a80a9af297b2341edd63f68fdac35`: independently read pinned README and LICENSING.md. Combined project/afl-fuzz is AGPL-3.0-or-later; components retain their own SPDX licenses and README states harness-compiled material remains Apache-2.0. No generalized legal conclusion. Sources: https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/README.md and https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/LICENSING.md (accessed 2026-11-07, License sections).
- Native operational detail and current maintenance/build conditions are recorded under S3 below.
- Atheris current README documents Python 3.11-3.14 on Linux/macOS; native extension fuzzing needs matching Clang/libFuzzer integration. Its no-interesting-input error can mean the first two calls never reach instrumentation, even when some module is instrumented. Source: https://raw.githubusercontent.com/google/atheris/master/README.md (Installation, Python coverage; accessed 2026-11-07).
- Jazzer defaults to regression mode; JAZZER_FUZZ enables discovery. A passing ordinary JUnit run is not a discovery campaign. Source: https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer/main/README.md (Running Jazzer; accessed 2026-11-07).

## Reused literature image evidence

Rebert et al. (USENIX Security 2014), *Optimizing Seed Selection for Fuzzing*, primary publisher PDF https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-rebert.pdf . Existing complete paper-reader collection at `C:/Users/Q/code/bugfinding-literature/corpus-evolution/papers/Rebert_2014_OptimizingSeedSelection/`; this researcher directly viewed images 000,002,004,007,011,013,014 (cover plus printed pp.862,864,867,871,873,874). Parent's corpus researcher has read all sixteen pages and written reader artifacts. No new ingestion or collection edits, no extracted paper text.

- pp.862,864: seed selection and online scheduling are different decisions; reduction preprocessing consumes part of the budget. Current engines differ from the historical BFF study. Don't transplant its fixed timings or historical bug counts into a generic lane recipe.
- pp.867,873: target invocation and meaningful input processing must be established, and corpus transfer across programs is empirical rather than guaranteed. The relevant fuzz runner needs evidence that intended code actually executes.
- pp.871,874: historical comparisons depend on scheduling and available observations; apparent differences do not universally establish superiority. Keep feature/reach/throughput/candidate metrics separate and make comparative claims proportional to matched repeated evidence. No new effectiveness claim from this reused reading.

## Operational findings being handed to the drafter

### S1 — Native AFL++ instrumentation and runner

Sources (all accessed 2026-11-07): https://aflplus.plus/docs/fuzzing_in_depth/ (instrumentation, dictionaries, status); pinned install https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/docs/INSTALL.md ; pinned CLI source https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/src/afl-fuzz.c (help lines 349-356, parser 1444-1463, timer reset 3432-3433).

- Current pinned install requires LLVM 14 minimum, recommends 18+; the website compiler-selection diagram still mentions older versions. Use selected release/install requirements rather than combine stale support claims. Linux source builds offer make all/source-only/distrib; choose actual needed mode, no mandatory all-mode install. macOS does not support afl-clang-lto, afl-gcc-fast or QEMU mode in this guide; FRIDA is separate. No Windows-native AFL++ setup was verified.
- Conditional chosen-target command shape: `afl-fuzz -i seeds -o out -V 300 -t 1000 -m 1024 -- ./target @@`. Numbers illustrate independently chosen fuzz/per-case/resource limits, not universal defaults. `@@` substitutes filename; omit for stdin harnesses. Pinned help says -V counts fuzzing time only and -E is approximate executions, not total wall/CPU cost. Dictionary -x and comparison instrumentation are useful hypotheses for a measured blocker; don't enable every mechanism by name.
- The website includes root/system-protection-changing setup commands. Reading them is not authorization to execute them or disable protections/checks. A real environment/configuration failure needs source-based diagnosis, not blindly copying tuning commands. No tool was installed or run.

### S2 — AFL++ persistence, binary targets and custom mutation

Pinned sources: instrumentation/README.persistent_mode.md, docs/fuzzing_binary-only_targets.md, docs/custom_mutators.md under the same ref URL above; read introduction/reset/deferred-init constraints and custom API/usage sections.

- Persistent mode requires relevant state reset and cleanup, including resources. Lower stability relative to fresh-process mode can indicate contamination; it is not proof of a product bug. Deferred forkserver initialization after critical threads, timers, shared descriptors or input reads can invalidate execution. Use existing target lifecycle owner; don't add a new simulation layer.
- Binary-only coverage needs a fitting instrumentation mode such as QEMU -Q or FRIDA -O; noninstrumented -n is not equivalent coverage search. Current per-mode platform/build support must match the target. Emulator behavior and loaded libraries delimit observations.
- Custom C/C++/Python mutation can preserve format structure; `AFL_CUSTOM_MUTATOR_LIBRARY`/`AFL_PYTHON_MODULE` select it, `AFL_CUSTOM_MUTATOR_ONLY` excludes default mutations. C buffer growth must use the documented allocator contract or the fuzzer itself can crash. Inspect actual custom-mutator ABI and trimming behavior; retain generation/replay representation. Semantic dependency correctness belongs to semantic-program-generation/stateful-property-testing.

### S3 — LLVM libFuzzer

Source: https://llvm.org/docs/LibFuzzer.html (Fuzz Target, Fuzzer Usage, Running, Options, Output, Value Profile, User-supplied mutators, Rejecting unwanted inputs), license https://raw.githubusercontent.com/llvm/llvm-project/main/LICENSE.TXT .

Use compatible Clang to instrument the real library and driver; -fsanitize=fuzzer links main, while -fsanitize=fuzzer-no-link separates instrumentation from final driver linking. Conditional existing-target build: `clang++ -g -O1 -fsanitize=fuzzer,address harness.cc target.cc -o fuzz_target`; run `./fuzz_target corpus -max_total_time=300 -timeout=5 -rss_limit_mb=1024 -artifact_prefix=artifacts/`, with owned existing paths and selected limits. Replay via file argument. Reentrant same-process target must handle malformed inputs, join relevant threads, avoid exit and reset relevant state. Returning -1 rejects corpus admission irrespective of coverage. `cov`, features, corpus size, throughput and RSS differ. Dictionary/value profile/custom mutation address different bottlenecks. No coverage-guided assertion can observe a semantic property it never checks. License Apache-2.0 with LLVM exceptions. These recipes were read, not executed.

Current Status section says important bug fixes remain supported; active major-feature work moved to Centipede. This is a maintenance constraint, not a universal replacement recommendation.

### S4 — Rust cargo-fuzz

Sources: https://rust-fuzz.github.io/book/cargo-fuzz/setup.html , guide.html, coverage.html, windows/setup.html; manifest https://raw.githubusercontent.com/rust-fuzz/cargo-fuzz/master/Cargo.toml . Setup current page requires nightly and matching C++/sanitizer support. Windows is explicitly documented with MSVC build tools and AddressSanitizer, so do not copy an old blanket Unix-only claim. Existing integration: `cargo +nightly fuzz run target -- -max_total_time=300`; inspect installed help/options. `cargo fuzz coverage target` replays corpus with source coverage rather than conducting search and needs matching LLVM tools. Features on fuzz crate must forward to target crate. `cfg(fuzzing)` may alter production paths; record those differences. Module snapshot is 0.13.2, MIT OR Apache-2.0; recheck chosen release. No installation or execution.

### S5 — Python Atheris

Sources: https://raw.githubusercontent.com/google/atheris/master/README.md and native_extension_fuzzing.md ; license https://raw.githubusercontent.com/google/atheris/master/LICENSE . Python harness instruments imports before importing target, or explicitly instruments selected functions, then Setup/Fuzz. Conditional run: `python fuzz_target.py corpus -max_total_time=300` under fitting installed integration. To produce coverage.py output, documented -atheris_runs permits graceful exit; libFuzzer -runs/native crashes may not flush Python coverage. Treat coverage measurement overhead separately. Native extensions need Clang fuzzer-no-link instrumentation and compatible runtime symbols; documented preload route is not supported on macOS, and modified-CPython alternative describes historical 3.8.6, not a ready recipe for current supported Python. Uncaught expected-input exceptions need the target's actual error contract; don't catch all exceptions and erase findings. Apache-2.0; no Windows support claimed by current README.

### S6 — JVM Jazzer

Sources: https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer/main/README.md ; docs/advanced.md ; src/main/java/com/code_intelligence/jazzer/junit/FuzzTest.java ; LICENSE under same repo. JUnit 5.9+ integration uses jazzer-junit and @FuzzTest; current platform list Linux x86-64/arm64, macOS 12+ x86-64/arm64, Windows x86-64. Existing Maven integration can select its fuzz test with JAZZER_FUZZ=1 and normal runner selection; no generic dependency version inserted. Annotation maxDuration/default 5m and maxExecutions can be overridden by jazzer.max_duration/max_executions; they don't affect regression mode. Only one fuzz test per discovery run executes. Inputs/generated corpus have different retention roles. Reproducer bytes may differ from typed consumed values, so preserve generated Java replay too where emitted. Apache-2.0. Lifecycle/reset semantics are checked separately below; an ordinary passing JUnit run does not establish coverage search.

### S7 — Fixture lifecycle is part of replay identity

Actual Jazzer source https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer/main/src/main/java/com/code_intelligence/jazzer/junit/FuzzTest.java sets default lifecycle PER_TEST. https://raw.githubusercontent.com/CodeIntelligenceTesting/jazzer/main/src/main/java/com/code_intelligence/jazzer/junit/Lifecycle.java documents that @BeforeEach runs once per fuzz test for PER_TEST during discovery; PER_EXECUTION invokes it before each input on its own test instance. Supported callbacks and concurrent lifecycle behavior have limits. Regression always runs full JUnit lifecycle per input. A passing saved-input regression therefore does not prove discovery used equivalent isolation.

FuzzTest https://raw.githubusercontent.com/google/fuzztest/main/doc/fixtures.md likewise distinguishes persistent custom fixtures, PerIterationFixtureAdapter and PerFuzzTestFixtureAdapter. Relevant mutated state must reset even when expensive immutable setup is shared. Ordinary unit-test assumptions about object lifetime must not be silently transferred into an in-process search loop. These are optional existing framework mechanisms, not a reason to add a shared reset abstraction. Accessed 2026-11-07, lifecycle/per-iteration sections.

### S8 — C++ FuzzTest operational route

Sources: https://raw.githubusercontent.com/google/fuzztest/main/doc/quickstart-bazel.md (Prerequisites, unit/fuzzing modes); https://raw.githubusercontent.com/google/fuzztest/main/doc/flags-reference.md ; https://raw.githubusercontent.com/google/fuzztest/main/doc/fuzz-test-macro.md ; https://raw.githubusercontent.com/google/fuzztest/main/doc/domains-reference.md ; https://raw.githubusercontent.com/google/fuzztest/main/LICENSE .

Current quickstart uses Linux or experimental macOS, Clang, Bazel and C++17; named unit mode lacks sanitizer/coverage instrumentation. Configured fuzzing route is `bazel run --config=fuzztest :TARGET -- --fuzz=SUITE.PROPERTY`; this --fuzz mode is indefinite. Flags reference separately documents `--fuzz_for=5m` for all fuzz tests in that binary, plus --rss_limit_mb/--time_limit_per_input. Do not silently claim --fuzz_for runs only one property. Choose actual target/current help and resource envelope. Tool config generation/setup requires real dependency/build ownership; historical pinned tutorial versions are not a policy to freeze dependencies.

Domain/seed mapping and fixture contracts must match the generated input representation; Filter rejection and recursive growth can block reach. Rich domains supply constructive inputs, not automatic semantic correctness. Runtime semantics belong in this skill; deeper domain/environment reasoning stays in semantic-program-generation. General license Apache-2.0 with separately enumerated file exceptions. No native Windows support recipe was established by this quickstart. No build executed.

### S9 — Go native execution, beyond ordinary tutorial content

Source https://go.dev/doc/security/fuzz/ (Suggestions, Running, Custom settings, corpus format), source license https://raw.githubusercontent.com/golang/go/master/LICENSE . Conditional existing-target command: `go test ./path/to/pkg -run='^$' -fuzz='^FuzzName$' -fuzztime=5m -parallel=2 -timeout=8m`. Values are illustrative, not defaults; authorization and project's runner policy govern execution. -fuzztime and -parallel bound different dimensions, minimization has its own per-attempt limit, and wall/CPU resources need accounting separately. Native discovery currently needs AMD64/ARM64 coverage instrumentation. Typed ordered corpus arguments must match; -fuzz regex selects one target. State must not escape an input invocation despite parallel nondeterministic workers. A source-to-byte representation decoder is the existing producer's responsibility; structured generator choices are not rendered source. No fresh Barn source audit or Go test run occurred. Go source license three-clause BSD form.

Actual installed `go help testflag` and primary https://pkg.go.dev/cmd/go#hdr-Testing_flags were read for -run/-fuzz/-parallel/-timeout contracts; this help-only program invocation was the sole local Go action, not a target test. -timeout is a test-binary limit, distinct from one fuzz-input timeout.

### S10 — Structured mutation and guard-solving levers

Primary guide https://raw.githubusercontent.com/google/fuzzing/master/docs/structure-aware-fuzzing.md (compression example, custom mutation, checksum solving, APIs) demonstrates why mutation over compressed bytes can keep rejecting before interesting code. Mutating a decoded representation and rebuilding format constraints can expose deeper behavior. This is not permission to duplicate the production encoder/parser, erase robustness lanes, or bypass the selected property. Use the existing producer and retain original/structured/rendered inputs plus versioned transformation identity. Custom crossover/mutation/trimming must preserve the actual domain and replay; otherwise the engine may search the wrong input space.

Pinned AFL++ CmpLog source https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/instrumentation/README.cmplog.md requires ordinary and CmpLog builds, the latter built with AFL_LLVM_CMPLOG; -c selects the companion binary. Treat it as a targeted experiment when comparisons are a measured bottleneck. Keep semantically matched builds and compatible limits. Dictionary, compare tracing/value profile, custom structural mutation, semantic generation and solvers address different bottlenecks; don't enable a stack of named tools without evidence. Sources accessed 2026-11-07; no recipe executed.

## Proposed execution decisions

These are plugin design recommendations inferred from the sources above, not a mandated framework or an empirical optimum.

### Identify the actual executable lane

Read the current target entrypoint, build graph, selected language/runtime/architecture/configuration and public producer. Determine where bytes or generated values enter and where an observable property is evaluated. The presence of a fuzz executable or fuzzer-generated coverage counters does not establish that the relevant library/module was instrumented. Reuse an existing fitting lane rather than rewrite harnesses merely to use a named engine. Retain source/build/framework and instrumented module identity.

Choose in-process search only where state/reset/lifetime contracts can make saved cases meaningful. When the desired bug requires a sequence, encode that sequence within one replayable input or use existing stateful/controller seams. Do not allow hidden residue to accidentally become the generator. Compare fresh versus repeated execution to diagnose state contamination where authorized; a changed failure can be a harness defect or a real accumulated product defect, requiring adjudication.

### Diagnose reach before multiplying workers

During a finite pilot, distinguish input decoder entered, parse/validation admitted, intended semantic operation reached, useful effect completed and oracle evaluated. Instrumentation feedback is one observation, not all five. Use supported source-coverage tools/logs/counters already present; harness-sensitivity owns representative faulty controls. If the public operation is absent from the call graph, more mutations cannot reach it. If syntax/checksum/dependent-state gates dominate, choose a fitting dictionary/compare/mutator/generator technique and measure the change. If the oracle remains crash-only, no input budget makes it a wrong-result checker.

Record accepted/rejected/unsupported cases by reason without adding an arbitrary required success ratio. Some invalid-input lanes intentionally exercise rejection guarantees. Split success-path and error-path properties where their contracts differ. Preserve corpus labels/representation and actual failure artifacts; corpus-evolution owns retention and compatible exchange.

### Fit costs and limits to the real process

Use a finite initial allocation and target-appropriate per-case/outer resource controls. A configured one-input timeout, fuzz duration, execution count, total wall time and aggregate CPU are different limits. Include startup, instrumentation/build, calibration, replay/reduction and auxiliary companion-process costs where charged to the envelope. Address-space memory limits may not represent resident-memory consumption for sanitizer builds; choose a supported containment/measurement route rather than assume one -m value applies universally. Runtime/sanitizer source applicability must be checked before selecting that policy.

Use separate owned output/artifact identities for concurrent lanes, and stop only owned processes. Do not copy documentation's process-name-wide cleanup or host-protection tuning into a generic skill. Parallelism is a measured budget choice; complementary instrumentation/semantic lanes can matter more than identical workers. Campaign allocation belongs to bugfinding-campaign. OOM, timeout, assertion, parser failure and infrastructure loss remain raw observations for the appropriate oracle/triage owner, not automatic product-bug attribution.

### Preserve and interpret the run

Keep exact input/typed values, generator choices and rendered source where applicable; initial state or required sequence; executable/source/build/configuration/instrumentation/framework identity; command/environment/limits; raw engine output and coverage/semantic counters; per-case artifact and actual replay attempts. A random seed alone does not recreate uncontrolled execution. Replay a found case through the same property, not an easier generic crash predicate. Failure-reduction/evidence-based-triage own shrink continuity and attribution.

When a pilot ends without a confirmed bug, report what executed, what the oracle observed, resource use and omitted dimensions. Do not call coverage growth, execution volume, a clean sanitizer run or a passed regression corpus a proof of semantic correctness. No new storage service, generic runner wrapper, campaign scheduler or mandatory tool installation follows from this operational skill.

## Worked advanced scenarios

Illustrative designs only, not executed product findings:

1. **Instrumented driver, uninstrumented native library.** The process reports coverage growth in argument decoding while an external library is built without feedback instrumentation. Inspect actual build/object/module identity and source coverage before allocating more workers. Correct the existing build owner when authorized and use a known reached behavior to check the lane. No universal symbol-based proof is promised for every toolchain.
2. **Regression lifecycle hides discovery residue.** A Jazzer test's @BeforeEach initializes a world. Regression uses a fresh lifecycle for each saved case, while default discovery initializes once per fuzz test. Make the intended per-input state explicit through supported lifecycle/reset ownership, or represent the accumulated sequence as the input if that is the promised test. Preserve original failure evidence instead of dismissing it after a fresh regression replay passes.
3. **Compressed/structured payload gate.** A byte lane spends almost every call rejecting format checks. Use a justified existing decoder/encoder or custom domain to mutate valid payload structure while retaining an invalid-input lane for relevant rejection guarantees. Measure target semantic reach and verify the same oracle evaluates; merely inflating corpus size does not demonstrate improvement.
4. **Structured Go choices sent to a source decoder.** The lane already has valid-IR generation. Keep choices as native fuzz input, render using its production producer and deliberately choose any effect/differential replay encoding. Don't feed typed []byte corpus files unchanged to a string decoder or copy the formatter into another utility. The source-inspected Barn baseline supplies this representation distinction; no current Barn defect claimed.

## Existing ownership and runtime limits

Read installed golang/go-testing-advanced SKILL.md directly: it already covers ordinary native fuzz signatures, seeds and minimization. This skill should not duplicate that tutorial. The approved Barn/domain baseline already includes thirteen native lanes, structured programs and a Toast comparison lane; no fresh full-repository absence audit here. New value is actual instrumented executable reach, state/lifecycle fidelity, bottleneck-specific mutation, correct discovery mode and practical cross-runtime operation.

Keep native memory sanitizer semantics in native-memory-instrumentation, dependent state/program construction in their generator skills, corpus exchange in corpus-evolution, and schedules/history/failure models in their specialist owners. A current libFuzzer-to-Centipede maintenance note is not evidence of a ready universal replacement; no Centipede operational integration was researched deeply. No verified JS/TS coverage engine is claimed by this set of recipes; fast-check properties belong to stateful-property-testing. No drop-in Go AFL++/KLEE/scheduler promise.

## Drafter handoff

Suggested reference split: native-runners.md (AFL++/LLVM instrumented/source/binary setup and conditional commands); managed-runners.md (Go/Rust/Python/JVM/C++ FuzzTest modes, support and lifecycle); reach-reset-and-feedback.md (pilot diagnosis and worked cases), plus required common-mistakes.md/sources.yaml. Split runtime references further only when meaningful progressive loading improves use; avoid an engine-option encyclopedia. Cite actual primary source URLs inline and inventory exact sections/access date. Selected-ref licenses should preserve file-scope distinctions, not become unsolicited legal interpretation or a mandatory approval workflow.

Behavior evaluation should provide raw harness/build/mode artifacts plus a permitted small target test and a finite resource budget. Observe whether the evaluator verifies actual target instrumentation, correct discovery mode and state reset, reaches the intended semantic oracle and saves a reproducible case. Include a regression-only invocation and a persistent fixture with hidden state without revealing diagnoses. Evaluate produced artifacts and qualified claims, not heading matching or named-tool choices. This research did not run such an evaluation or establish empirical bug yield.

## Verification limits and completion

All source-read commands above are unexecuted conditional examples. No fuzzer, compiler, native build, library test or target campaign was run; no dependencies installed, source modified outside this report, commit, host registration or publication. Existing seed-selection paper-reader artifacts were reused through direct image reads and remain untouched. No new paper ingestion/process/tag/reconcile, no raw paper-text reading. Initial guessed LLVM rst/FuzzTest flags/run/AFL CmpLog docs paths returned 404; canonical current paths supplied the findings, failed responses supply none. Referenced developer researcher role file did not exist; explicit task constraints governed.

Current docs/main branches are dated snapshots; pinned AFL++ evidence is scoped to the exact ref above. A future execution must verify its selected tool release/support/help and preserve that identity. Report ready for drafting with these explicit operational and evidence limits.
