# Research: native-memory-instrumentation

Date: 2026-11-07

## State

Per-skill primary-source research complete for drafting. This report is the only owned repository output; paper-reader artifacts are external. Other agents' files, peer citation improvements and State bullet are preserved. Literature uses paper-reader and direct page images only; no target action, dependency installation, staging, commit or publication.

## Evidence ledger

Checking actual sanitizer and Memcheck build/runtime contracts, observation boundaries, diagnostics and replay. No clean-run correctness or universal Go applicability claim.

### Initial verified source identities and limits

- LLVM main observed by git ls-remote: `635f30899dd0914fa89f0b3dc9a9e548e6d0ceec`. Actual GitHub contents response and rendered docs edit link show sanitizer documents now use `.md`, not guessed `.rst`. Failed `.rst` URLs supply no evidence. Pinned Markdown source is being read.
- Valgrind official manual index identifies Release 3.28.0, 23 Oct 2026; actual official platform page lists current platform/ISA restrictions and historical Windows ports. Exact docs/version/sections will scope recipes. Sourceware HEAD was observed as `cd7f7c7c9f1ee996686e4fd7fa2c8c337b8789ea`, but a raw-source HTTP200 response was an anti-bot HTML page, not XML. No pinned source/code finding is inferred from it.
- Primary paper selected from USENIX author/title landing page: AddressSanitizer ATC2012. Only page images through paper-reader will establish paper findings; search/PDF-extraction summaries are not reading evidence.

### Paper-image pass complete

Serebryany, Bruening, Potapenko and Vyukov, AddressSanitizer: A Fast Address Sanity Checker (USENIX ATC2012), https://www.usenix.org/system/files/conference/atc12/atc12-final39.pdf. Canonical PDF directly downloaded to task-local paper directory, reader helper counted/rendered ten pages, title/four authors verified visually on page1, ALL ten images page-000 through page-009 read directly. No extracted paper text used. Reader artifacts are complete externally within the stated reader-only scope; no process/tag/reconcile workflow.

- pp.3-5: shadow addressability, poisoned redzones and delayed allocator reuse determine detection. An invalid access can evade the model by landing in another valid allocation; a use-after-free may evade detection after enough allocation churn drains quarantine. More CPU alone does not fix an absent memory observation.
- pp.4,6: instrumentation occurs after optimization in the historical design; optimized-away accesses and uninstrumented behavior delimit what is seen. ASan may expose a race manifestation as use-after-free but does not guarantee detecting the race. Keep race-detection separate.
- pp.6-8: memory/quarantine/redzone/unwind choices change cost and diagnostic/detection behavior; historical evaluation used particular small redzones and zero quarantine. Do not adopt its historical slowdown as a target forecast or its tuning as current defaults.
- p.9: compiler instrumentation does not automatically cover arbitrary closed libraries. Current interceptors and actual dependency builds must establish native/FFI coverage; a driver instrumented alone is not full-process semantic assurance.

### Current operational boundaries established

- Pinned MSan document requires instrumented dependency closure with compatible interceptors; ignorelisted loads are treated initialized and full instrumentation disabling can introduce false positives. It is not ASan's addressability check.
- Pinned UBSan document says many checks report and continue; unsigned overflow, implicit conversions, local-bounds and vptr are not all included by the undefined group. A zero program exit is not proof no finding occurred, and suspicious-but-defined arithmetic needs the actual target contract.
- Valgrind3.28 manual distinguishes leak kinds shown from kinds counted as errors, and default error-exitcode0 preserves the application's status. Its pool interface is needed for accurate custom-allocation boundaries. Tool report/exit/finished leak scan must be recorded separately.

## Primary source inventory and supported operational handoff

All source reads accessed2026-11-07. Commands are conditional shapes read from actual sources, not executed targets or installers. Repository pins were observed/fetched; a chosen future compiler/runtime must be checked independently.

### S1 — ASan addressability/lifetime lane

Pinned source: https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/AddressSanitizer.md (Usage; Additional Checks; Issue Suppression; Limitations; Supported Platforms). Exact fragment: “exits on the first detected error”.

Use an existing compatible compiler-rt installation and instrument the target code as well as its driver. Source-read C++ build shape: `clang++ -O1 -g -fsanitize=address -fno-omit-frame-pointer harness.cc target.cc -o memory_target`; compile and final-link flags matter, and final linking must use the compiler driver rather than ld. Symbolization uses matching binaries/debug information plus llvm-symbolizer on PATH or ASAN_SYMBOLIZER_PATH. Retain the first report, faulting access and allocation/free stacks before reduction; later corrupted-state outcomes may be misleading. No build was run.

Runtime knobs cover different observations: stack-use-after-return requires the relevant compiled mode and runtime option; use-after-scope has its own instrumentation. Container logical-size checks rely on library annotations; partial instrumentation/partial stack poisoning can produce false reports or omissions despite the page's general no-false-positive wording. Inspect annotation/lifetime/setup before declaring target or tool blame. External-library interception observes selected library calls, not every direct load/store in an uninstrumented dependency.

ASan uses substantial virtual address space and additional real memory/stack; a virtual-address ulimit is not equivalent to an RSS budget. Current LLVM doc prohibits fully static executables; MSVC static CRT support below is a different implementation/configuration. Native platform list includes Windows8.1+, but Windows port support is weaker; do not combine it with MSVC's separate Windows10+/x86/x64 promise or infer all options work everywhere. A clean run is only evidence about reached instrumented behavior.

### S2 — MSan definedness lane and dependency closure

Pinned source: https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/MemorySanitizer.md (Usage; Origin Tracking; Handling external code; Ignorelist; Supported Platforms; Limitations). Exact fragment: “requires that all program code is instrumented”.

Source-read build shape: `clang++ -O1 -g -fsanitize=memory -fsanitize-memory-track-origins=2 -fno-omit-frame-pointer harness.cc target.cc -o definedness_target`. Link the fitting runtime via compiler driver; supply the selected compatible instrumented dependencies/C++ library and verified interceptors. Uninstrumented dependency output, inline assembly writes and custom syscall paths can corrupt shadow-definedness propagation and create false reports. Existing libc interceptors help, but their existence does not establish arbitrary closure. Do not add blanket unpoisoning to make a report disappear.

Origins2 tracks allocation plus intermediate stores; origins1 retains allocation origins only. This adds cost beyond ordinary MSan, so a long discovery lane and a diagnostic replay can select different recorded configurations. Use MSAN_SYMBOLIZER_PATH or PATH llvm-symbolizer. The current doc lists Linux/NetBSD/FreeBSD, not a Windows-native MSan route. Full static linking is unsupported. Ignorelisting can suppress reports and treat loaded values as initialized; disable_sanitizer_instrumentation can lose propagation and create false positives, unlike no_sanitize(memory)'s retained supporting instrumentation. Preserve these omissions with results rather than calling the lane complete.

### S3 — UBSan, explicit checks and report/exit semantics

Pinned source: https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/UndefinedBehaviorSanitizer.md (Usage; Available checks; Minimal Runtime; Stack traces; Issue Suppression). Exact fragment: “continues execution”.

Source-read selected-check build shape: `clang++ -O1 -g -fno-omit-frame-pointer -fno-sanitize-merge -fsanitize=undefined -fno-sanitize-recover=undefined harness.cc target.cc -o ub_target`. On compatible target this makes the chosen group's findings terminate rather than merely report. A report-observing campaign may intentionally retain recovery; it must parse/preserve diagnostics instead of equating zero exit with no finding. Trap mode has different evidence (signal without full runtime report), and -fsanitize-trap/recover without an enabled sanitizer may be no-ops. Do not change recover/trap behavior silently during replay.

The undefined group excludes unsigned overflow, implicit conversions, local-bounds, vptr and several other checks; those selected checks test different contracts. Some suspicious arithmetic is defined language behavior. A valid wraparound policy is not a demonstrated UB defect, while narrowing before arithmetic is not covered merely by signed-overflow checking. vptr needs RTTI, C++ linking and no vptr trap mode. Bounds can depend on compiler knowledge/optimization; volatile-qualified pointers exclude several checks. General numerical correctness remains numerical-oracles, and source-level invariants remain correctness-oracles.

Symbolized UBSan reports require selected build's debug/frame information, llvm-symbolizer, and `UBSAN_OPTIONS=print_stacktrace=1`. Check-specific runtime suppressions require recoverable checks and enough symbols; group-wide suppression isn't supported. Do not propose suppressions/overflow semantics changes to evade a target failure. The minimal runtime has different logging/features and is not a substitute for evidence-rich discovery just because it exists.

### S4 — LSan, retained roots and explicit lifecycle checks

Pinned sources: https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/LeakSanitizer.md (Usage; Programmatic Disabling; Flags); https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/compiler-rt/lib/lsan/lsan_common.h (CAN_SANITIZE_LEAKS, lines38-59). Exact short fragment from docs: “reachable from it”.

Standalone documented link shape: `clang -g -fsanitize=leak target.c -o leak_target`; fitting ASan integrations can provide leak checks too. ASan/MSan/LSan flags have separate environment-variable parsers; LSan-specific controls belong in LSAN_OPTIONS even when integrated with ASan. An exit-based leak phase must actually execute: timeout, crash or abrupt process exit cannot be reported as a completed clean scan. The explicit recoverable leak-check API prints a report and returns0/1 without disabling the final scan; the nonrecoverable check's invocation affects subsequent automatic checking. Use an existing supported lifecycle seam rather than create a global instrumentation wrapper.

Root-region registration, ignored objects (including reachable descendants) and thread-local disable scopes alter what is counted. Reachable retained memory can violate an application retention budget without becoming an unreachable-allocation leak report; that inference is why resource-complexity-testing is complementary. Source's supported macro branches include Linux/Apple/NetBSD/Fuchsia and architecture/API exclusions; ASan's broad integration paragraph describes a narrower list. Preserve selected runtime/platform evidence instead of asserting one merged universal matrix.

### S5 — Clang lane compatibility and implementation license

Actual driver source: https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/lib/Driver/SanitizerArgs.cpp (IncompatibleGroups, lines727-751; diagnostic handling862-872). Exact fragment: `IncompatibleGroups`.

The inspected driver rejects address with thread/memory, thread with memory, and leak with thread/memory. Design distinct compatible builds; do not instruct a single all-sanitizer binary. It also notes standalone leak flag handling in the presence of address, so integrated runtime behavior must be checked rather than assume flags stack independently. Supported ASan+UBSan can be a fitting lane, but exact target/version/runtime still governs. Race tool integration belongs to race-detection-campaigns.

Pinned LICENSE.TXT at the same LLVM ref was read: Apache-2.0 with LLVM exceptions, with separately identified third-party components. This is scoped source metadata, not legal advice or proof of every bundled dependency's terms. No compiler/toolchain was installed.

### S6 — Memcheck observation, custom allocators and origins

Official versioned-by-manual source: https://valgrind.org/docs/manual/mc-manual.html, release3.28.0 identified by https://valgrind.org/docs/manual/index.html. Read sections4.2,4.3,4.4,4.5,4.7-4.8. Exact fragments: `--errors-for-leak-kinds` and `VALGRIND_DO_ADDED_LEAK_CHECK` (seven words total counting flags as tokens).

Memcheck distinguishes addressability and value-definedness. A copied uninitialized byte need not report until it affects a checked decision/address/syscall. Origins identify earlier allocation/stack context at added cost. Custom allocators need faithful client-request/pool descriptions; merely naming a block does not change addressability. Completed leak scans distinguish definitely/indirectly/possibly lost and reachable memory. Selection of displayed leak kinds differs from kinds counted as errors; full leak checking is required for leaks to contribute to error-exitcode. Keep report categories, suppressed counts and lifecycle phase separately.

Conditional existing-binary example: `valgrind --tool=memcheck --leak-check=full --show-leak-kinds=all --errors-for-leak-kinds=definite,possible --track-origins=yes --error-exitcode=99 --log-file=memcheck.%p.log ./target CASE`. Error code99 is illustrative and must not collide ambiguously with target status. Origins and full scans can cost substantially more than basic address checks; choose representative bounded workloads and diagnostic replays. No Valgrind run occurred.

### S7 — Valgrind core/process/platform and installation boundaries

Official docs: https://valgrind.org/docs/manual/manual-core.html (2.1-2.5; error-related options; child tracing; thread support); https://valgrind.org/docs/manual/dist.readme.html (build/install); https://valgrind.org/info/platforms.html ; https://valgrind.org/info/about.html. Manual index gives release3.28.0/23Oct2026. Exact core fragment: `--error-exitcode`.

Default error-exitcode0 preserves target status; explicit report parsing or a chosen nonzero code is needed for automation. Start the real native executable, not just its shell launcher. Exec-child tracing is separate from fork inheritance; use per-process log identities where children matter. Valgrind serializes thread execution and changes scheduling, so a clean memory run is not an exhaustive concurrency result. Current platform page lists supported ISA/OS pairs and historical Windows ports; it supplies no native current Windows route. Existing compatible environment and selected-release installation should be checked; documented source setup is configure/make/make-install, not an action authorized here. Official about page identifies GPL terms; full selected source license text wasn't fetched because Sourceware raw-source access returned an anti-bot HTML response. Do not invent a more specific license expression from that response.

### S8 — Real Go/cgo interoperation, not general managed-memory assurance

Pinned primary Go source: https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/cmd/go/alldocs.go (build -asan/-msan); https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/cmd/go/internal/work/exec.go (cgo flags3553-3560). Exact fragment: “enable interoperation with address sanitizer”. This pin resolves actual fetched source; the parent race researcher independently recorded its identity, and these specific files were read here.

The build docs describe OS/architecture/compiler-specific -asan/-msan interoperation; actual cgo builder prepends matching sanitizer C/link flags. That does not rebuild arbitrary precompiled dependencies or prove all native writes/allocator boundaries are observed. Conditional fitting focused-test shape: `go test -asan ./path/to/pkg -run '^TestNativeBoundary$' -count=1`, or a separate -msan build only where the selected toolchain and native dependency closure support it. Reuse the target's permitted runner; no test was executed. Source declares -asan Linuxamd64/arm64/loong64 with differing host-compiler floors and -msan Linuxamd64/arm64/loong64 plus FreeBSDamd64/Clang requirements. These master-source facts are not a promise about an installed release. Don't recommend Memcheck merely because a project is Go or infer pure-Go logic/race safety from these native interop flags.

### S9 — Microsoft native Windows route and managed boundary

Pinned actual public doc sources independently fetched after resolving MicrosoftDocs/cpp-docs main: https://raw.githubusercontent.com/MicrosoftDocs/cpp-docs/f29e25fb8f05bb38cf0246476b5c1fc92bf33876/docs/sanitizers/asan.md and https://raw.githubusercontent.com/MicrosoftDocs/cpp-docs/f29e25fb8f05bb38cf0246476b5c1fc92bf33876/docs/sanitizers/asan-known-issues.md . Rendered docs use view=msvc-170 and identify updates28May/20Aug2026. Exact fragments: “resumable functions are exempt from instrumentation” and “native translation units”. Public source documentation license is CC-BY4.0; that is not the MSVC toolchain's license.

A compatible installed developer-command-prompt recipe is `cl /fsanitize=address /Zi target.cpp`, followed by the resulting executable with its actual workload. Docs scope support to x86/x64 Windows10+ and identify incompatible /RTC, edit-and-continue, incremental linking, unsupported coroutine/OpenMP/etc paths and uninstrumented precompiled headers. Use a separate supported diagnostic configuration rather than remove checks from an unrelated existing build. Preserve actual compiler/runtime DLL/debug identity; ASAN_SAVE_DUMPS can retain a diagnostic dump when supported.

Known-issues source shows allocator overrides can hide/misclassify errors; partially instrumented DLL loading/unloading can create coverage gaps/runtime artifacts. It describes C++/CLI instrumentation as experimental: isolate relevant unsafe code in existing native translation units/DLLs where appropriate, and do not treat managed methods/arrays/threads as guaranteed ASan-instrumented accesses. The MSVC implementation must not inherit arbitrary Clang-only suppression/stack-return options from a generic recipe. No installation, project property change, build or target execution occurred.

## Method decisions that buy useful evidence

The following are proposed plugin decisions derived from the sources, not a mandatory framework or a guaranteed detection rate.

### Select a missing executable property

Read the real producer, input/setup, enabled build and lifetime contract. Choose addressability/lifetime, value-definedness, specific UB, or allocation leak/retention according to the claimed failure. A native access report may refute memory safety on that path, but cannot establish arbitrary wrong-result semantics, exploitable severity, correct data-race behavior or absence of all memory faults. Barn's existing structured execution and histories are baseline; this research did not freshly audit all Barn code or prove a native-memory blind spot there. A new fitting lane needs an actual native dependency/FFI/unsafe producer and a testable guarantee, not a tool selected from language branding.

Inventory all relevant driver, library, allocator, module/FFI, assembly/syscall and lifecycle boundaries. Verify the selected objects really carry the intended instrumentation and load a compatible runtime. A source-level build flag on one target is insufficient evidence about another prebuilt library. Model a custom pool only where the actual allocator contract supports the descriptions; no copied allocator or plugin-wide wrapper follows. Use representative supported controls to check sensitivity, then explore actual allocation/lifecycle/input sequences rather than just replay trivial crashes.

### Preserve the observation when scaling compute

Choose distinct compatible builds and measure startup/reset/instrumentation/allocator costs separately. Redzone/quarantine/origin/stack settings change either detection windows, diagnostic information or costs; retain exact values and do not silently trade away the selected property to improve throughput. For persistent workers, reset state or encode meaningful sequence state as the case. A memory fault may require allocation churn or a prior sequence; one saved final input may not replay it.

Leak observations need a meaningful phase: normal exit or an actual supported explicit scan after the operation/quiescence. A worker repeatedly killed by timeout may never perform its final leak scan. Repeated recoverable scans and current pool/root APIs can help a long-running test only through a real existing lifecycle seam. An object still reachable from a root may satisfy leak detector reachability yet violate a documented application resource budget; route that contract to resource-complexity-testing.

Read actual diagnostics, not only program status. ASan/MSan commonly terminate on first error; UBSan often recovers; Memcheck preserves application status unless configured otherwise. Keep reporting mode, instrumentation omissions, suppressed errors and scan completion alongside outcomes. Distinguish unsupported instruction/runtime initialization failures from reached target diagnostics. Existing suppressions/ignorelists must have narrow provenance; do not introduce one to make an unexplained finding green or claim suppressed paths were tested cleanly.

### Reproduce a native finding without switching its contract

Retain original bytes/typed values, setup and prior allocation sequence, target and loaded native-module build identities, source/symbols, architecture/compiler/runtime version, build flags, runtime options, allocator/quarantine/root settings, raw report/status, faulting and allocation/free/origin stacks, and exact replay attempts. Symbolized logs should resolve against the same binary/debug files; rebuilding from a different revision to obtain symbols can change the execution. An instrumented host crash after unloading its runtime has a different producer from an actual target invalid write. State the demonstrated behavior before proposing cause or severity.

Reduce while preserving the same diagnostic and real valid-call/lifetime preconditions. A smaller harness that violates the API, suppresses uninitialized propagation, changes allocator reuse or switches from native to managed execution does not prove the original defect. Keep original artifacts and qualified intermittent evidence. Generic reduction, LLM triage and causal grouping remain their specialist owners.

## Advanced worked scenarios

These are illustrative experiment designs, not executed product findings.

1. **FFI input decoder calls a prebuilt unsafe library.** The wrapper is ASan-instrumented but the library's direct writes are not. Trace an actual documented call through the native boundary; use its existing compatible instrumented build or another fitting binary-instrumentation lane. A malloc interceptor's existence does not establish every library access is checked. Match valid-call/lifetime requirements so an invalid generated wrapper isn't blamed on the product.
2. **Uninitialized payload crosses an uninstrumented dependency.** An MSan report appears after a native callback, but the dependency never updated shadow definedness. Check instrumentation/interceptor/assembly boundary and actual initialization before target attribution. Blanket unpoisoning can erase a real defect, while pretending closure exists can manufacture a false one. Preserve the same raw payload and native chain.
3. **Long-running pool test never finishes a leak phase.** A timeout ends the worker, with no leak report. That is not a completed clean scan. Use an existing supported explicit scan/quiescence boundary where the guarantee requires one, preserve pool/root semantics, and inspect actual retained growth separately from unreachable leaks. More repeated killed workers cannot repair the missing observation.
4. **Undefined behavior reports with exit0.** UBSan emits a selected-check finding and recovery continues; the harness only checks status. Observe and preserve the diagnostic or choose a supported fail-fast build for that contract, then verify healthy/faulty sensitivity. Do not globally change target semantics or assume every unsigned-overflow report means UB.
5. **Windows mixed-mode unload artifact.** An ASan-enabled DLL unloads while intercepted references remain, or managed code never received access instrumentation. Inspect the actual native/CLR module and lifetime source before calling it an application buffer overflow. Retain loader/runtime evidence and use an actual fitting native test seam; neither disabling the check nor claiming all managed code is covered is justified.

## Existing ownership, reference depth and evaluation

Read installed golang/go-testing-advanced entrypoint and fuzzing guidance: ordinary input generation/assertions/corpus are already owned there. This skill adds specific native-memory observation and build/runtime/dependency closure, not another fuzzing tutorial. Race detection owns conflicting-access workload/TSan; coverage-guided-fuzzing owns input search and instrumented feedback; generators own dependent valid inputs; resource complexity owns growth contracts; triage/reduction own their existing mechanics. No exhaustive ecosystem novelty claim or new instrumentation framework is needed.

Suggested references: lane-selection-and-coverage.md (property/build/FFI/allocator boundary), sanitizer-recipes.md (compatible source-native ASan/MSan/UBSan/LSan routes), memcheck-and-platforms.md (status/scan/custom-pool/process restrictions), replay-and-diagnostics.md (native evidence/phase examples), required common-mistakes.md and sources.yaml. Windows/Go details can be conditional subsections or separate progressive files if material warrants it. Public source URLs and page citations replace local paper paths in distributed instructions. Every factual/operational claim needs a source, not a citation only at a large table's end where scope is ambiguous.

Blind evaluation can supply real raw native boundary/build/module artifacts, a UBSan report with exit0, an unfinished leak scan, a managed access outside instrumentation and a custom allocator whose pool metadata is absent. Ask the evaluator to establish a fitting new diagnostic lane or investigate the candidate without expected diagnoses. Evaluate actual instrumentation/phase evidence, retained artifacts and qualified conclusion. No such behavior experiment or empirical yield comparison was performed here.

## Reader artifact status and limits

All ten ASan paper images were read. External notes preserve equations/algorithms/parameters, all printed memory/stack table values with discrepancies left explicit, historical evaluation context, figures, limitations and all31 bibliography identities. Metadata, description, abstract paraphrase, citations, index, reader ledger and helper-generated keymap exist. No full abstract was transcribed. Reader-only instructions excluded nested reconciliation/tagging/process; those were not invoked or claimed complete. No raw PDF/page image belongs in plugin staging.

Current technical sources were actually read at the named paths; no sanitizer, compiler build, target test, fuzzer, Valgrind run, dependency installer, git mutation, host registration or publication occurred. Initial guessed LLVM .rst URLs returned404; actual repository listing and rendered-page edit link resolved .md. Sourceware raw-source endpoint returned anti-bot HTML despite HTTP200; no code/license finding relies on it. An initial PowerShell Select method mistake on an object was corrected to Select-Object for a read-only directory listing; no file state was affected. One generalized-shadow equation typo in the external note was corrected against the already-read page3 before completion. No missing researcher-role file was invented; the developer-referenced path does not exist.

## Completion

Research complete for independent drafting with primary source pins/sections/exact fragments, real supported conditional recipes, ten-page paper-reader evidence, concrete native/FFI/phase decisions and explicit limitations. Only this repository report and isolated external paper-reader artifacts were authored. No product defect, empirical effectiveness or clean-run correctness claim.
