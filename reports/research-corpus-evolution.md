# Research: corpus-evolution

Date: 2026-11-07

## State

Per-skill research complete for drafting. This report is the only owned repository output; completed paper-reader artifacts remain outside the plugin repository. Literature uses paper-reader and page images only. No drafting, target execution/mutation, installation, commit or publication.

## Evidence ledger

Reading approved scope, primary corpus tooling, representation/replay contracts and relevant literature. Provenance, regression evidence and current search material will remain distinct.

### Primary documentation read so far

- Go fuzz corpus arguments must preserve type and order; `[]byte` construction choices and rendered source strings are different inputs. Source: https://go.dev/doc/security/fuzz/ (Requirements; Corpus file format), accessed 2026-11-07. Decision: corpus exchange needs a verified representation/producer conversion, not matching filename or language alone.
- OSS-Fuzz corpus access is project-authorized and backup-based; a maintained corpus can be reused before rebuilding seeds, but no GCS dependency or access authority follows. Source: https://google.github.io/oss-fuzz/advanced-topics/corpora/ (Obtain access; Downloads; Backups), accessed 2026-11-07.
- Read existing fetched Barn `origin/master:scripts/fuzz_differential.py` directly. `decode_corpus_file` accepts exactly one `string(...)` record; `load_programs` ignores unsupported decoding and deduplicates rendered sources. The strongest baseline already has native corpus persistence and differential replay. No target mutation, fetch or execution.
- Installed `golang/go-testing-advanced` read: native seed corpus, generated-cache persistence and regression retention are already covered. New value is corpus purpose/compatibility/semantic diversity decisions rather than repeating basic Go corpus tutorial.

### Literature selected

Rebert et al., *Optimizing Seed Selection for Fuzzing* (USENIX Security 2014), primary PDF https://www.usenix.org/system/files/conference/usenixsecurity14/sec14-paper-rebert.pdf . Selected for direct paper-reader page-image reading; search snippets and PDF auto-extracted web text will not supply findings.

All sixteen local images (cover plus paper pp. 1-15 / proceedings pp. 861-875) have now been directly read. Identity verified on cover/title page; no extracted text used. Paper-reader artifacts are being written at `C:/Users/Q/code/bugfinding-literature/corpus-evolution/papers/Rebert_2014_OptimizingSeedSelection/`.

- Paper pp. 3-4 (863-864): seed minimization is set cover relative to measured code blocks; weighted variants can encode size/time. A minimum coverage subset is not a proof that omitted files contain no distinct bugs.
- Paper pp. 5-7 (865-867): evaluating seed selection is coupled to scheduler and budget. The paper's ex-post ILP uses already-observed per-seed bug arrival traces to compute an upper bound; it is not an online omniscient scheduler to copy into this plugin.
- Paper pp. 8-10 (868-870): stack-based uniqueness produced 2,702 apparent mp3gain bugs from one manually identified vulnerability. Decision: preserve raw cases and classify causes before treating corpus/crash counts as unique product defects.
- Paper pp. 11-12 (871-872): reduced coverage seed sets helped the studied round-robin scheduler, while the full set cannot lose against a subset under the paper's optimal scheduler. Preprocessing coverage can cost more than a short campaign. Decision: account acquisition/minimization cost and use measured target/scheduler results, not a universal smaller-is-better rule.
- Paper pp. 12-14 (872-874): studied transfer between same-format targets is coverage evidence, not proof of future bug-yield transfer. Study uses historical file-based black-box mutation; data did not establish statistically significant strict superiority of the preferred selection strategy over random. Decision: replay incoming seeds on the receiving harness/build/oracle and avoid modern runtime/yield guarantees from the historical result.

### Current AFL++ licensing/source distinction

Unexpected root-license result was checked against actual primary README and LICENSING.md rather than explained from memory. `git ls-remote https://github.com/AFLplusplus/AFLplusplus.git refs/heads/stable` returned `d0070729206a80a9af297b2341edd63f68fdac35`; pinned raw README, LICENSING.md and src/afl-cmin.c were then read. README states the project/combined afl-fuzz is AGPL-3.0-or-later with per-file Apache-2.0 components; src/afl-cmin.c's header specifically says Apache-2.0. Do not generalize either root or individual-file label to all selected binaries/components. Primary URLs: https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/README.md (License), https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/LICENSING.md and https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/src/afl-cmin.c (header). This is source provenance, not legal advice or a request to change the target's licensing. No install/recovery action was needed.

## Primary tool contracts and conditional recipes

All sources accessed 2026-11-07. Commands below were read from actual documentation/source, not executed. Use the existing compatible target/instrumentation/environment; this corpus skill does not install a fuzz engine or own its instrumented build.

### S1: AFL++ collecting, reducing and exchanging inputs

- URL: https://aflplus.plus/docs/fuzzing_in_depth/ ; sections 2a-2c, 3c-3h, 5. Small quoted fragment: “corpus count”.
- Verified command shapes: `afl-cmin -i INPUTS -o INPUTS_UNIQUE -- ./target @@` selects coverage-relevant files; omit `@@` for a stdin consumer. `afl-tmin -i case -o smaller -- ./target @@` simplifies one input. Those goals differ from preserving a particular semantic violation.
- The guide supports importing complementary fuzzer queues via AFL++ main-instance `-F`; shared names must be unique. Newly useful inputs can be injected via a temporary compatible secondary. It also distinguishes seed count from actual covered code and notes exclusive target options may need separate lanes.
- Decision: confirm receiving input format, harness/config and actual behavior before exchange. Preserve intentional diversity and original evidence separately from the selected active search set. Do not copy the guide's system-protection changes, arbitrary sync intervals or fixed plateau thresholds into this skill.

### S2: Current afl-cmin / afl-merge executable source

- Exact source: https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/d0070729206a80a9af297b2341edd63f68fdac35/src/afl-cmin.c ; inspected header, usage and option/output paths around lines 2608-2699 and 3009-3340, not every algorithm line. GNUmakefile entrypoints also read: https://raw.githubusercontent.com/AFLplusplus/AFLplusplus/stable/GNUmakefile (PROGS/SH_PROGS).
- Source supports a distinct incremental `afl-merge` mode; its help says existing output files remain unchanged and only coverage-adding inputs are added. Conditional shape: `afl-merge -o CURRENT -i INCOMING -- ./target @@`. This is selected-version-specific; verify executable availability/help rather than assume every installed AFL++ has it.
- Ordinary cmin requires an empty output directory in the inspected source. `-t` is a per-input millisecond timeout; `-m` limits a child; `-T` selects execution/update workers. These do not define a whole-job budget. `-e` changes selection to edges only, ignoring hit counts. Default crash/timeout acceptance differs from `-A`/`-C`; excluded inputs are not thereby resolved defects. `--crash-dir` can move crash files; do not suggest it against the only original evidence.
- Decision: keep command mode, limits and selection predicate in the record. An exit of zero describes that operation's success, not preservation of every semantic class or regression. The old root `afl-cmin` script URL returned 404; current source is under src/. No fallback guessed script is shipped.

### S3: libFuzzer corpus and merge/replay semantics

- URL: https://llvm.org/docs/LibFuzzer.html ; sections Corpus, Running, Options, Resuming merge, Output. Small quote fragment: “full feature sets”.
- Conditional shapes: `./fuzzer -merge=1 SELECTED FULL` selects coverage into a distinct first directory; `./fuzzer -merge=1 CURRENT INCOMING` adds coverage-contributing inputs. A list of file paths replays without mutation. New discoveries go to the first corpus directory; parallel instances can reload compatible additions.
- `-reduce_inputs` preserves fuzzer features, while `-minimize_crash` has a failure predicate. `cov`, `ft`, `corp`, speed and RSS are different measurements. A resumable merge uses `-merge_control_file=PATH`; its state belongs to that operation/configuration. Do not copy the docs' process-name-wide kill command. Exact build/instrumentation/runtime support belongs to coverage-guided-fuzzing.
- License source: https://raw.githubusercontent.com/llvm/llvm-project/main/LICENSE.TXT ; Apache-2.0 with LLVM exceptions. No compiler/fuzzer setup was executed.

### S4: Go typed corpus, seeds, cache and regression

- URL: https://go.dev/doc/security/fuzz/ ; Requirements, Failing input, Corpus file format, Glossary. Small quoted fragment: “identical”.
- Seed types/order must match the target. Saved failures become finite seed regressions; generated search material in `$GOCACHE/fuzz` is used during fuzzing. Preserve the actual typed file and emitted replay selector, e.g. `go test -run=FuzzName/CASE_ID`, within the project's permitted runner. Generated cache retention alone is not committed regression retention.
- Decision: validate a target's decoder/arguments before migration. Rendering a choice stream to source must call its actual producer and retain both representations plus generator revision, rather than relabel bytes as strings. No native Go corpus tutorial or unverified standalone minimization command is needed here.

### S5: OSS-Fuzz access, acquisition and backups

- URL: https://google.github.io/oss-fuzz/advanced-topics/corpora/ ; Obtain access, Downloading the corpus, Corpus backups. Small quoted fragment: “daily zipped backups”.
- Corpus access depends on project contact authorization; documented acquisition uses `gcloud storage cp -r gs://BUCKET_PATH LOCAL_DIRECTORY`, or the existing daily zip backups. This is an optional route for an actual authorized OSS-Fuzz integration, not a required account/tool for the plugin. Check project/target identity and authorized retention before import; no corpus was downloaded here.

### S6: Seed-selection literature

- Rebert et al. primary PDF and full sixteen-image paper-reader evidence described above. Dense notes contain equations, experiment controls, numeric results and limitations; no historical reported gain is a prediction for this plugin.
- Important source-bounded result: seed selection depends on scheduling, preprocessing cost and measurement purpose. Same-format coverage transfer is worth testing on the receiver; it is not a license to assume semantic/replay equivalence across applications or versions.

## Corpus decisions that change discovery

The following is plugin design inferred from S1-S6 and actual Barn source. It is not a new mandatory directory schema, service, format or scoring formula.

### Identify each artifact's purpose

Keep the original acquired/generated material and provenance when selecting an active search subset. Separately preserve confirmed regressions and unresolved candidates with their witnesses. These can use existing project conventions rather than three new required directories. Coverage deduplication may remove a file from a current active set without establishing it is redundant as a regression or semantic example.

For a target's actual contract, record enough to distinguish representation, producer/generator version, target entrypoint/build/configuration and relevant initial state. If a source changes meaning across generator revisions, retain the produced program/world as well as its choices. Where object IDs, sessions or schemas require context, the corpus unit includes that replay material. General bundle reduction belongs to failure-reduction.

Logical duplicate categories differ: exact bytes, same decoded input, same measured features, same semantic state/effect, and same established bug cause. Do not implement them as one universal hash. Use exact identity when it solves the actual import/replay problem; use native coverage selection for the active target; leave causal duplicate adjudication to evidence-based-triage.

### Validate imports on the receiving lane

First read its actual producer/decoder, expected types/arity/encoding, build/config, argument transport, resource limits, state-reset contract and oracle. Trace one representative seed into the intended target operation before bulk exchange. Classify malformed, excluded, unsupported, valid-but-unreached, completed and failing entries according to actual evidence; do not silently count every copied file as useful search input.

If conversion is required, call the existing producer/serializer. Preserve provenance from original representation to generated artifact and actual receiving result. A conversion that compiles but normalizes away the selected feature has not retained it. Recompute coverage/semantic reach under the receiving build rather than transfer numeric feature IDs between instrumentations. Same source file format or matching test-name suffix does not establish compatibility.

Measure additions against the actual property: successful operations, effect/transition classes, supported error boundaries, recovery points or other justified observations. These are target-dependent dimensions, not an invitation to add a generic semantic taxonomy or model framework. A coverage-selected core can be supplemented by deliberately retained contract cases when they test a distinct promised behavior. State the added cost and purpose instead of claiming the coverage minimizer proved them unnecessary.

### Select with total cost and limits visible

Measure acquisition, decoding/rendering, baseline execution, coverage collection, minimization and replay cost alongside discovery. Keep counters for candidate files, valid/admitted cases, actual property evaluations, coverage/semantic novelty, failed/slow cases and retained findings. A reduced corpus that consumes the entire authorized discovery allocation is not automatically an improvement. Compare matched bounded pilots before asserting benefit; a historical study or increased executions/second does not establish new bugs.

Investigate repeatedly expensive cases against the target's resource/progress contract. Preserve them as evidence; an expected costly valid path may merit a separate bounded resource lane, while an unrelated harness bottleneck belongs in the existing owner. Do not silently delete slow/OOM/timeout inputs to make throughput look better, nor force every long-running case into every low-latency replay. Original evidence and the reason for active-set selection remain available.

After a harness, compiler, instrumentation, feature configuration, schema or generator change, replay/reselect where those changes affect meaning or measurements. Unsupported stale inputs need a recorded migration or an explicit scoped retirement from that lane, not erasure of original regression evidence. No periodic service, cache invalidator or universal expiration policy is justified by this research.

### Evolve with complementary lanes

Source-native exchange can share compatible inputs while keeping differing search strategies. Distinguish a shared byte encoding from matching semantics and target APIs. Retain lane provenance and validate new samples on the receiver; do not concatenate incompatible structured-choice streams, network conversations and raw file inputs into one directory merely because an engine takes bytes.

Mutation dictionaries are hints to a selected engine/encoding, not complete testcases. Inspect the selected parser/mutator's documented token syntax and domain, then measure whether added tokens unlock useful target paths. Exact dictionary construction/runtime flags belong to the coverage-guided runner; this corpus skill owns provenance and compatibility of exchanged material.

## Advanced worked applications

Illustrative designs, not target findings or executed campaigns.

1. **Structured choices to engine comparison.** Barn's fetched structured producer `fuzzseed.Source(choices)` emits source via production IR/formatter, while the inspected differential decoder accepts a single Go `string(...)` record. An authorized target-owned export can call that producer, retain choices/rendered source/generator identity, and encode the receiving lane's actual string format. Validate exclusions and successful comparisons before importing the full set. Renaming a `[]byte(...)` corpus file does not perform this conversion. This advances the actual demonstrated integration gap without inventing an alternate formatter or assuming every generated form lies in the engine contract intersection.
2. **Same edges, different state effects.** Two API sequences exercise the same instrumented branches but different ownership/lifetime or recovery states. If the target promises a behavior difference relevant to its oracle, retain representative replayable cases even when the active coverage selector chooses only one. Demonstrate those states/observations from the real producer; do not assert semantic distinction from filenames alone. This is a reasoned supplemental selection, not proof that every discarded coverage-equivalent file hides a bug.
3. **A large cache overwhelms finite regression.** The generated exploration cache contains many valid expensive cases, while a small set protects known product failures. Preserve confirmed regressions under the target's normal finite-test convention, budget active discovery separately and investigate expensive evidence. Do not copy the whole search cache into an always-run suite merely to preserve files, or prune the original regression set with a coverage-only merge.
4. **Incoming seeds from another build.** A previous sanitizer/configuration or generator version produced useful material. Re-execute it under the new decoder/config/oracle; record broken format, changed semantics, new failure and actual novelty separately. Transfer source inputs where compatible, not stale coverage bitmap IDs or opaque replay blobs presumed stable.

## Boundaries and overlap

The source-read Barn baseline already acquires real verb sources, deduplicates exact bytes, uses optional `.moo` sources, retains native fuzz failures and replays string corpora against Toast. Directly read `origin/master:internal/fuzzseed/seeds.go` and the first 108 lines of structured.go plus the complete differential script; no fetch/worktree change or target execution. This is a bounded source inventory, not absence proof over every branch or a claim of current remote CI.

Existing installed Go testing guidance already owns native corpus basics. This skill adds purpose-specific retention/selection, semantics-aware supplemental cases, representation conversion, receiver validation and total-cost reasoning. It links campaign allocation, coverage runner, semantic generation, stateful testing, reduction and triage rather than copy their mechanics. No generic corpus store, content-addressed service, installer or universal adapter is justified. External marketplace novelty was not exhaustively audited; no novelty claim is needed.

## Drafter handoff

Suggested substantive references: corpus-selection-and-retention.md (purpose and selection interpretation), exchange-and-replay.md (typed/producer compatibility plus worked cases), conditional-tool-recipes.md (AFL++/libFuzzer/Go/authorized OSS-Fuzz commands), required common-mistakes.md and sources.yaml. Preserve current AFL++ project/component license distinction with selected-revision caveat; avoid broad legal advice. Corpus commands assume an existing fitting instrumented target and authorization for their outputs; runner owner handles installations/platform setup.

A blind evaluation can supply source producers/decoders, a structured-choice corpus, a string-only receiving lane, redundant coverage inputs and a unique regression. Ask the evaluator to produce a useful receiving active set and retained evidence under a finite budget. Observe actual conversion/replay provenance, preserved regression, scoped cost and classifications, not copied-file count. A second scenario can supply a changed generator/schema and a slow family; observe meaning-preserving migration and resource evidence retention. No such experiment or discovery-yield comparison ran in this research.

## Paper artifacts and verification limits

Canonical PDF length 377,516 bytes; render helper reported sixteen pages and sixteen named images exist. All images directly inspected. External paper-reader outputs: dense notes with page-numbered equations/parameters/results, metadata, description, short-excerpt/paraphrased abstract, all 29 bibliography entries, index, reader ledger and helper-generated keymap. The parent/Q reader-only rule excluded nested reconcile, tagging, process and propstore orchestration; none was invoked and no completion of those workflows is claimed. No paper binary/image enters plugin staging.

Failed root afl-cmin source URL returned 404; actual src/afl-cmin.c supplied operational evidence. The referenced developer researcher role file does not exist. Source-doc commands, target inputs and mutation/minimization operations were not executed. External mutable URLs are dated observations; exact AFL++ ref is preserved above to resolve its checked licensing/source mechanics. No target tools installed, no git mutation/commit, no host registration or publication.

## Completion

Research ready for independent drafting: S1-S6 primary evidence, full seed-selection paper-image pass, current corpus-tool recipes and selected-ref licensing scope, concrete semantic/replay/provenance decisions and advanced examples. Only this plugin report and isolated external paper-reader artifacts were authored.
