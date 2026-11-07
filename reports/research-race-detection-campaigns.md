# Research: race-detection-campaigns

Date: 2026-11-07

## State

Per-skill research complete for drafting. This is the only owned repository output. Literature uses paper-reader and page images only; no target execution, installation, target changes, commits or publication.

## Evidence ledger

Inspecting primary Go race detector, native ThreadSanitizer and Helgrind documentation/source, supported build/runtime boundaries, realistic workloads and relevant literature.

## Early primary findings

- Go's official detector guide distinguishes reached-path race detection from code never executed; a race-enabled binary under realistic load can expose paths missed by unit tests. Its race build tag can exclude tests, so actual selected build/test inputs matter. Source: https://go.dev/doc/articles/race_detector (Usage, Excluding tests, How to Use), accessed 2026-11-07.
- Native TSan needs compiler instrumentation and runtime linkage; selected disabled instrumentation/ignorelist choices can erase synchronization and stack evidence. Current official platform list excludes a generic native-Windows claim. Source: https://clang.llvm.org/docs/ThreadSanitizer.html (Usage, attributes, Ignorelist, Limitations), accessed 2026-11-07.
- Helgrind observes pthread synchronization and can report API misuse, potential lock-order cycles and races; custom primitives need accurate existing annotations. An observed lock-order cycle is not itself a reproduced deadlock. Source: https://valgrind.org/docs/manual/hg-manual.html (Overview, lock ordering, race interpretation), accessed 2026-11-07.

The referenced developer role file is absent at C:/Users/Q/.Codex/AGENTS.md.d/researcher.md. Existing installed go-race-and-memory-model skill was read; it already covers basic race syntax and memory-model authoring. This skill must add workload/reach/build-boundary/evidence campaign decisions, not copy that tutorial.

## Literature image evidence

Serebryany and Iskhodzhanov, *ThreadSanitizer – data race detection in practice* (WBIA2009), DOI https://doi.org/10.1145/1791194.1791203 ; primary author PDF https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/35604.pdf . Canonical PDF retrieved directly, rendered through paper-reader helper, title/authors verified visually, and ALL ten images read (printed pp.62-71). No extracted paper text used. External artifacts at C:/Users/Q/code/bugfinding-literature/race-detection-campaigns/papers/Serebryany_2009_ThreadSanitizer include dense page-cited notes, metadata, description, abstract paraphrase, all22 bibliography identities and collection index/ledger; keymap refresh follows. No nested process/tag/reconcile.

- pp.63-66: detector observes memory/synchronization events; custom annotations change its synchronization model. Missing edges can create warnings, invented edges can hide real races. Use maintained selected-runtime semantics rather than copy historical macros or add annotations merely to silence a report.
- pp.66-67,70: instrumentation changes runtime/memory and even which events remain observable; historical buffer flush/fast-mode tradeoffs are not present-Go flags or universal overhead forecasts.
- pp.67-69,71: initialization/publication/use/destruction and paired access context matter; a downstream allocator crash can be far from the original reference-count race. Generate real lifecycle overlap and preserve both accesses, not only the final symptom.
- pp.68-69: observed HB order, hybrid inference and actual logical safety differ. Extra synchronization in a harness can hide the target's race; an annotation is evidence to audit, not independent synchronization.

The historical implementation is Valgrind-based. It must not be described as the algorithm or supported configuration of current Clang/Go TSan. No empirical discovery or accuracy claim is transferred to the new skill.

## Verified primary-source inventory and operational handoff

All sources below accessed 2026-11-07. Git refs were actually obtained with read-only git ls-remote, then pinned files fetched. A pin identifies this evidence snapshot, not the user's installed compiler/runtime. Official versioned docs are preferred for an actual selected release. Commands are source-read conditional examples, not executed target tests.

### S1: Go detector contracts and report preservation

Pinned official article: https://raw.githubusercontent.com/golang/website/a8b66266e226994e2ead51317bace3ee83cedab9/_content/doc/articles/race_detector.html ; Usage, Report Format, Options, Excluding Tests, Requirements, Runtime Overhead. Human URL: https://go.dev/doc/articles/race_detector . Quote fragment: “failed to restore the stack”.

The article documents paired-access/creation stacks, GORACE log_path/exitcode/history_size/halt_on_error, the race build tag and cgo/C compiler requirements. Windows requires a fitting mingw-w64 runtime; its documented compiler probe is `CC --print-file-name libsynchronization.a`. Current article describes extra defer/recover allocations retained until goroutine exit that do not appear in Go heap profiles. Preserve process RSS and instrumented/native identity when investigating growth; this is not by itself a product leak. Report-history capacity affects missing old stacks, distinct from input generation.

Conditional existing-test recipe: `go test ./path/to/pkg -race -run '^TestSharedLifecycle$' -count=1 -cpu=1,2,4 -timeout=2m`. The selected test and values are illustrative; project authorization/runner policy governs. `GORACE='log_path=OWNED_PREFIX halt_on_error=1'` is POSIX syntax for an optional selected-output/first-finding policy; adapt to actual shell and restore environment afterward. Retain full reports before changing history/resource settings. No command was run.

### S2: Selected Go source, tool flags and real instrumentation boundaries

- https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/internal/platform/supported.go , RaceDetectorSupported:16-32 and FuzzInstrumented:80-90. Actual race function includes Linux amd64/arm64/loong64/ppc64le/riscv64/s390x plus Darwin amd64/arm64 and FreeBSD/NetBSD/Windows amd64. FuzzInstrumented at lines82-86 admits amd64, arm64 and loong64 when FuzzSupported also holds. ARM64 compile admission cannot determine whether runtime VMA width fits. The pinned website article's race matrix omits riscv64, while the selected cmd/go go1.27.3 table omits some other entries. These are source/version-scoped discrepancies, not proof that an arbitrary installed release supports the union. Do not merge them into a universal matrix or present development-main fuzz support as released capability.
- https://pkg.go.dev/cmd/go#hdr-Testing_flags , selected page go1.27.3, count/cpu/shuffle/parallel/timeout. `-count=1` avoids cache reuse; cpu varies GOMAXPROCS for ordinary tests, not fuzz-discovery executions. Shuffle randomizes test ordering, not all goroutine schedules. `-parallel` governs parallel tests/fuzz workers, not an arbitrary SUT's goroutine count. Package/test-binary/outer limits differ.
- https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/cmd/go/internal/work/exec.go , cgo flag construction:3325-3332. This region explicitly adds native MSan/ASan flags; it does not automatically add `-fsanitize=thread` for race mode. This is a bounded build-path observation: inspect actual C/C++ compilation and linked modules before claiming native FFI access coverage. Do not invent a universal mixed Go/native TSan linking recipe.
- https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/src/plugin/plugin.go , warnings:26-32. Quote fragment: “poorly supported”. The package explicitly warns that even simple races in dynamically loaded Go plugins may be missed. A clean host run is not coverage of plugin accesses. Preserve exact host/plugin source/toolchain/tags/flags as required by the package, not just host -race.
- License inspected: https://raw.githubusercontent.com/golang/go/dcc06a82727b447270b1a58cc5f86b49736e317c/LICENSE , BSD three-clause form. No Go install or target build was performed.

### S3: Pinned Clang native TSan operation and omissions

https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/clang/docs/ThreadSanitizer.md ; Supported Platforms, Usage, attributes, Ignorelist, Limitations, Runtime Flags. Human URL: https://clang.llvm.org/docs/ThreadSanitizer.html . Quote fragment: “all code to be compiled”.

Compile/link actual native target code with compatible TSan instrumentation, debug information and usable optimization; current platform list is selected 64-bit Unix-like targets, not generic native Windows. Conditional owned-target shape: `clang++ -g -O1 -fsanitize=thread harness.cc target.cc -o race_target`, then execute the same workload/inputs. Prebuilt noninstrumented modules can hide races or synchronization. no_sanitize(thread), disable_sanitizer_instrumentation and ignored functions remove different observations; their disappearance of warnings is not a fix.

Static libc/libstdc++ linkage is unsupported; large shadow mappings make simple virtual-memory caps misleading. Keep symbolization, full conflicting stacks, actual module/build identity and runtime options. Default detector exit behavior and program failure are separate evidence. Source/license: https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/LICENSE.TXT , Apache-2.0 with LLVM exceptions. No native target compiled or executed.

### S4: Runtime resource controls and actual perturbation producer

Pinned sources under LLVM ref above:

- https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/compiler-rt/lib/tsan/rtl/tsan_flags.inc , history/memory/I/O/SC/adaptive flags:33-115. Quote fragment: “aim at”. memory_limit_mb can flush shadow memory; it is not a hard OS limit. force_seq_cst_atomics changes modeled atomic ordering and is not a production semantic-preserving fix. Flags/admission need selected-runtime help/source verification.
- https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/compiler-rt/lib/tsan/rtl/tsan_interceptors_posix.cpp , actual pthread_create:1052 and lock/unlock:1394-1433 call AdaptiveDelay, around the real operation.
- https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/compiler-rt/lib/tsan/rtl/tsan_rtl.cpp , initialization:729-731 guards AdaptiveDelay::Init with !SANITIZER_GO.
- https://raw.githubusercontent.com/llvm/llvm-project/635f30899dd0914fa89f0b3dc9a9e548e6d0ceec/compiler-rt/lib/tsan/rtl/tsan_adaptive_delay.cpp , time-budget estimates:35-39, per-thread seed:243-251, actual delayed operations:277-399. Exact provenance fragment: `SetRandomSeed(NanoTime())`.

Useful new lane: after proving relevant accesses are reached, a compatible native TSan runtime can perturb synchronization/lifecycle timing via `TSAN_OPTIONS=enable_adaptive_delay=1 ./race_target` (POSIX environment syntax). The feature is disabled by default; actual runtime must expose it. The source's estimated overhead budget is not a hard whole-process budget. Its time-derived seeds and ordinary OS scheduling do not provide deterministic trace replay or exhaustive search. This is not a promised Go GORACE option; recorded source explicitly excludes Go initialization. Preserve raw finding/workload/initial state and actual replay attempts. Runtime docs at the pinned ThreadSanitizer.md Adaptive Delay section corroborate the feature; no yield or speed guarantee is adopted.

### S5: Helgrind observer, output cost and supported native route

https://valgrind.org/docs/manual/hg-manual.html ; sections7.1-7.6, accessed2026-11-07. Quote fragment: “two stack traces”. The pthread event model needs accurate knowledge of custom synchronization. Warnings distinguish pthread misuse, potential lock-order deadlock and a pair of conflicting memory accesses. Full history retains more old-access context; bounded conflict-history caches can lose old stacks. Optional free-is-write changes the observed lifetime-race class and has allocator caveats; do not blindly stack every option.

Conditional existing fitting binary: `valgrind --tool=helgrind --history-level=full --error-exitcode=99 --log-file=helgrind.%p.log ./native_target ARGS`. Numeric exit choice is illustrative. The process needs debug information and a compatible platform/ISA; core options are at https://valgrind.org/docs/manual/manual-core.html (tool selection, logging, errors, child tracing). Default error-exitcode0 can return target success despite reported errors. Exec children require the documented tracing choice; arbitrary child subtrees must not be assumed covered. Raw logs and invocation, including suppressions, are evidence.

Current platform/release evidence: https://valgrind.org/info/platforms.html and https://valgrind.org/docs/manual/dist.news.html (3.28.0,23Oct2026). Matrix/ISA details differ between general page and release notes; selected executable/source plus representative control governs. About page https://valgrind.org/info/about.html declares GPL, but full license-version text was not retrieved here; don't infer one from a failed URL. Existing fitting installations only; no installation recipe was validated. Manual also contains older Qt/GCC advice and a spinlock-support inconsistency between overview/tips; do not transplant historical rebuild/suppression instructions into a current target.

## Campaign decisions for the drafter

These are plugin design adaptations grounded in the sources, not a new mandatory framework, scoring formula, blanket tool mandate or a demonstrated optimal search policy.

### Choose a real sharing/lifetime hypothesis

Read actual producers and enabled configuration: who creates the shared state, who publishes it, which goroutines/native threads access it, who closes/replaces/frees it, and which synchronization should order those accesses. Existing unit tests might never overlap initialization, concurrent use, cancellation/reload and destruction. Generate legal public-operation sequences and values that reach those lifecycle transitions; invalid-handle setup crashes do not establish the intended race lane. Use stateful generation for dependency constraints and semantic effects; this skill owns the executed access/synchronization observer.

Measure representative concurrent access paths and workload outcomes. Line coverage alone cannot establish that two access contexts operated on the same live object. Retain actual identity/lifetime/operation evidence where relevant. A harness-level mutex/barrier that encloses the whole SUT operation can erase exactly the race being searched; supported launch coordination may establish a test phase without serializing the internal competing accesses. Do not manufacture overlap with arbitrary sleeps and then call it exhaustive scheduling.

### Establish instrumented boundaries and sensitivity

Check selected toolchain/platform and actual binary/module compilation, build tags, plugin/FFI/native dependencies, excluded code, annotations, suppressions and reset. A fuzz harness can be instrumented while its real shared-memory dependency is not. Source-specific annotations must describe a real established synchronization/lifetime relation; they cannot be the evidence that relation exists. Reuse maintained runtime integrations rather than rewrite target synchronization to please an observer.

Use an existing justified historical/controlled race and healthy case through the same producer path when establishing a new lane. Observe actual paired-access rejection, not a build failure or arbitrary timeout. Keep documented detector false-positive/negative boundaries and unsupported sources explicit. General sensitivity control design remains harness-sensitivity's responsibility; do not add a mutation service.

### Spend compute on a missing access interaction

Use a short finite pilot to establish useful paths and actual overhead, then vary actual actors, shared keys/objects, lifecycle phases, operation sequences and contention. Repeated uncached runs and selected GOMAXPROCS values can change observed interleavings; they do not enumerate them. Native runtime delay injection is an additional selected-version lane when available, not a substitute for input/operation design or a replayable controller.

Track completed operations, relevant sharing/lifecycle contexts, raw detector reports, reproducible candidates, unsupported/model-boundary reports, run failures and resource cost. Avoid a universal thread count or success-ratio threshold. More goroutines can spend the budget on scheduling/diagnostic overhead or timeouts while exercising no new access relationship. Preserve the actual resource envelope independently of runtime heuristics/history knobs.

Instrumentation can invalidate a real-time deadline or introduce memory retention. Distinguish a configured test timeout, detector shadow-memory/resource exhaustion, target progress failure and actual access report. Do not relax the product's timing guarantee or declare a product leak solely from the instrumented process; use matched observations and the resource/liveness owners. A known target defect remains a finding even if its instrumentation makes the workload slower.

### Interpret and preserve the actual evidence

For each candidate retain exact source/build/config/toolchain/runtime, relevant module/annotation/suppression identity, inputs and initial state/sequence, actual workload options, raw paired access stacks and thread creation, object/address/lifetime information, resource limits and replay attempts. An address can change across ASLR runs; keep semantic identity instead of requiring identical numeric addresses. A stack match is a triage bucket, not proof every case shares one cause.

Inspect both accesses and the claimed missing synchronization against the real language/API semantics. A detector report can arise from a real race or an unmodeled primitive; the source/model evidence distinguishes them. A potential lock-order cycle is narrower than a reproduced deadlock. Conversely, a true shared-access violation does not require demonstrating an eventual crash before preserving the finding.

Reduce workload/inputs while retaining the same object lifetime, competing accesses and genuine ordering model. A smaller fresh-process miss is not proof the old long-lived trace was imaginary; state/schedule may be missing. Keep original evidence and uncertain cases. General reduction and cause/deduplication are failure-reduction and evidence-based-triage concerns. No clean finite race run establishes linearizability, serializability, deadlock freedom, weak-memory completeness or unexecuted-path correctness.

## Advanced worked scenarios

Illustrative designs, not executed tests or observed Barn defects:

1. **Publish/use/close path omitted by unit tests.** Real public operations establish a live object, concurrent readers/use, reload or cancellation, then closure/destruction. Preserve legal ownership and returned handles. Measure whether the competing use/close access paths actually execute; a generic high-load loop that never closes state is not a substitute. Keep actual race stacks/lifetime observations and separate any documented legal error from the race evidence.
2. **Race-enabled host with native/plugin blind spot.** The top-level Go test is race-enabled but actual plugin documentation warns about missed races, or the native library's build does not carry fitting instrumentation. Inspect that boundary and select an existing target-owned supported native observer/harness when it exercises the same contract. Do not report blanket end-to-end coverage or invent mixed runtimes merely because the host prints a race banner.
3. **Native contention lane with adaptive delay.** An existing instrumented native test reaches shared ownership transfer but ordinary runs rarely vary the handoff timing. With verified supported runtime help/source, pilot adaptive delay and retain build/options, workload and actual observations. Additional reports are candidates; no same-seed replay or exhaustive schedule claim follows. Timing failures caused by deliberate perturbation need their actual progress contract, not automatic deadlock classification.
4. **Instrumented memory growth with no Go heap growth.** Long-running goroutines repeatedly defer/recover and the race process grows. The official detector document names retained auxiliary allocations absent from Go profiles. Compare exact instrumented/native lifecycles and process memory before attributing the observed growth to target retention. Preserve the expensive input; do not silently drop it just to improve race-run throughput.

## Barn baseline, ownership and handoff

The approved domain report establishes Barn's strong fuzz/program/history controls. This research did not freshly audit Barn's full race setup or infer a defect/absence across worktrees. A meaningful new lane must identify an actual shared-memory/lifetime interaction omitted by existing executed workloads, use a fitting observer and retain its concrete report. Simply repeating go test -race or relabeling Elle serializability is not the new capability.

Installed Go race/memory-model skill already owns language ordering/locking authoring. Schedule exploration owns controlled choices/model bounds; history skills own abstract operation guarantees; native-memory-instrumentation owns access/lifetime/UB sanitizers other than this race observer; resource/liveness owners interpret their contracts. Link those owners rather than clone their mechanics. No universal harness, task scheduler, new annotations layer or runtime installer is justified by this research.

Suggested depth: race-workloads.md (public lifecycle/access hypotheses and measured reach), runtime-recipes.md (conditional Go/TSan/Helgrind builds/reports/boundaries), report-and-model-limits.md (paired-access evidence, annotations, resource/unknown outcomes), plus required common-mistakes.md and sources.yaml. Source inventory should cite exact pinned files above where used, with sections/short fragments and access date. The original 2009 paper is conceptual evidence only; its historical mode flags must not be advertised as current native/Go APIs.

Blind evaluation can supply an actual API lifecycle contract, a race-enabled driver with an excluded real access path, raw paired reports, a custom synchronization boundary and an instrumented-only resource symptom. Ask the evaluator to produce a useful workload/interpretation without revealing expected diagnosis. Observe actual path/evidence retention and whether the selected contract follows; no words/heading score or promised bug count. No such evaluation ran in this research.

## Verification limits and completion

No target/compiler/checker/test/campaign was run or installed. Only read-only remote-ref/source/document probes and paper rendering/keymap helpers ran; no source-control mutation or publication. All ten paper images were read directly; external notes/metadata/bibliography/index/ledger/keymap were written with editing tools/helper programs. Parent/Q rule excludes the reader's nested reconciliation, tagging, process and propstore, so none was invoked or claimed complete. Paper/PNG files remain outside plugin staging.

Guessed LLVM .rst URL returned404; actual pinned .md source supplied evidence. A guessed Go issue17105 was unrelated and supplies no claim. Search results for third-party pure-Go race tools were not source-audited and are not advertised as integrations or measured replacements. The selected Go master/source, website article and versioned command page have different matrices; no unsupported cause for this discrepancy is asserted. Valgrind's full COPYING URL was inaccessible; only its primary declared GPL scope is recorded. No empirical yield/accuracy claim, complete runtime matrix, target absence proof or definitive product defect.

Report ready for independent drafting. Other agents' skills/improvement reports and parent task note were preserved.
