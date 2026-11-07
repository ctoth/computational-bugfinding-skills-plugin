# Research: bugfinding-campaign

Date: 2026-11-07

## State

Per-skill foundation research is complete for drafting. No skill text has been drafted. Ownership is this report only; packaging, task notes and skill files belong to other agents. No target program was run, installed or changed; no commit or publication was made.

## Evidence ledger

Primary campaign documentation and existing processed Elle page images are being read. Findings distinguish documented operations, research inference and target-specific applicability.

### Literature reused, not re-ingested

Existing processed Elle collection: `C:/Users/Q/code/papers/Kingsbury_2020_ElleInferringIsolationAnomalies/`. This researcher directly viewed page images for printed pp. 1, 3, 7-9 and 12 on 2026-11-07. The parent/domain research previously completed paper-process --light for all fourteen pages; no collection files were changed here. Source: Kingsbury and Alvaro, *Elle: Inferring Isolation Anomalies from Experimental Observations* (2020), https://arxiv.org/abs/2003.10554.

- **Finding:** Observation design changes the available oracle. Unique append-only values expose both write identity and order; ordinary overwriting registers hide information (p. 3). Quote fragment: “recoverability and traceability”. **Decision changed:** Before funding longer runs, inspect whether the workload records sufficient causal information to distinguish legal from illegal behavior.
- **Finding:** Sound findings and complete detection differ. Recoverability and traceability constrain anomaly inference; absence of an inferred cycle does not independently establish every isolation guarantee (pp. 7-8). **Decision changed:** Save explicit checker limits and unknown outcomes; don't interpret a green search lane as full correctness.
- **Finding:** Elle presents short contradiction witnesses and omits predicate analysis in this paper (pp. 9, 12). **Decision changed:** Preserve witness structure for triage and consider another oracle/search dimension when the contract is outside the checker's model. No historical performance number is generalized to this marketplace.

### S1: AFL++ Fuzzing in Depth

- URL: https://aflplus.plus/docs/fuzzing_in_depth/
- Read: corpus reduction and Fuzzing the target, especially Using multiple cores; accessed 2026-11-07.
- Quote fragment: “For every secondary fuzzer there should be a variation”.
- Documented behavior: campaigns can diversify instrumented builds, mutation/power modes and cooperating engines. Unique instance identities and shared campaign output are operationally relevant. Target memory/time limits and finite-run options need chosen-build verification.
- Decision relevance: allocate a pilot among meaningfully different lanes rather than cloning identical jobs. Measure added reach and reproduced findings against total resources. The docs' specific core-count and mix suggestions are target-dependent guidance, not a universal pack policy.
- Important source conflict: the older https://aflplus.plus/docs/parallel_fuzzing/ explicitly marks itself outdated and points readers to current multiple-core guidance. Do not lift its stopping heuristic or topology rules as current universal requirements.

### S2: OSS-Fuzz Ideal Integration

- URL: https://google.github.io/oss-fuzz/advanced-topics/ideal-integration/
- Read: Fuzz Target, Seed Corpus, Coverage, Regression Testing, Performance; accessed 2026-11-07.
- Quote fragment: “make at least some progress”.
- Documented behavior: a short pilot checks immediate hangs/OOMs and progress; coverage can improve through better seeds/dictionaries and fixing target bottlenecks. Discovery campaigns and finite corpus regression execution are different operations.
- Decision relevance: confirm target-owned maintained harnesses actually exercise intended code before expanding compute; reuse generated failures as finite regressions after adjudication. Source recommendations do not override a target's authorized CI/local execution boundaries.

### S3: Fuzz Introspector

- URL: https://google.github.io/oss-fuzz/advanced-topics/fuzz-introspector/
- Read: overview and build-tooling differences; accessed 2026-11-07.
- Quote fragment: “static reachability potential”.
- Documented behavior: reports compare static reachable functions with dynamic execution coverage and identify blocking harness paths. This page documents C/C++, Python and Java with language-specific build analysis.
- Decision relevance: distinguish an unreachable API from a reached but unsolved guard. Extra run time cannot exercise a function excluded by the harness's call graph. Do not promise this specific tool works on Barn's Go code.

### S4: ClusterFuzz performance analysis

- URL: https://google.github.io/clusterfuzz/using-clusterfuzz/workflows/analyzing-fuzzing-performance/
- Read: When to analyze fuzz target performance; Performance factors; Coverage report; accessed 2026-11-07.
- Quote fragment: “Blocking issues should be resolved”.
- Documented behavior: execution speed, coverage growth, timeouts/OOMs and other recurrent failures affect search. The page scopes itself to coverage-guided libFuzzer/AFL targets. It advises handling newly found crashes rather than focusing exclusively on throughput.
- Decision relevance: a failure-rich lane may need reduction/triage capacity rather than more workers. A quiet lane needs coverage and blocker diagnosis before a longer allocation. These observations don't establish that every reported timeout is a product bug.

### S5: ClusterFuzz triage

- URL: https://google.github.io/clusterfuzz/using-clusterfuzz/workflows/triaging-new-crashes/
- Read: Filtering testcases; Regression revision range; Crash statistics; accessed 2026-11-07.
- Quote fragment: “Reliability of reproducing the crash”.
- Documented behavior: triage uses reproduction reliability, crash type/state, job/fuzzer, platform and revision-range information. The page distinguishes usable regression ranges for reliably reproducible failures.
- Decision relevance: retain build/configuration and reproduction evidence with candidates; a stack-similar group is not automatically a proven single cause. Intermittent findings remain evidence, even when they cannot yet enter the confirmed count.

### S6: OSS-Fuzz reproduction

- URL: https://google.github.io/oss-fuzz/advanced-topics/reproducing/
- Read: Fuzz target bugs; Building; Reproducing bugs; accessed 2026-11-07.
- Quote fragment: “appropriate sanitizer”.
- Documented behavior: a testcase consists of the actual bytes fed to the target; sanitizer and architecture can affect reproduction. Documented helper command after a compatible OSS-Fuzz build: `python3 infra/helper.py reproduce PROJECT FUZZ_TARGET TESTCASE`.
- Decision relevance: retain exact input plus source/build/runtime/architecture/instrumentation/options. Do not substitute a seed for the actual failure. The helper requires an existing OSS-Fuzz integration; it is not a generic command for Barn or every target.

### S7: SQLite's primary testing account

- URL: https://www.sqlite.org/testing.html
- Read: §2 Test Harnesses; §3 Anomaly Testing; §4.1.3 dbsqlfuzz; §4.1.4 third-party fuzzers; §4.1.5 fuzzcheck; accessed 2026-11-07.
- Quote fragment: “both the SQL input and the database file”.
- Documented behavior: dbsqlfuzz jointly mutates database state and SQL. SQLite reports faults missed by prior SQL-only or database-only fuzzers. Its testing account also distinguishes incorrect-result oracles from easy-to-detect crashes and describes simulated allocation, I/O and crash failures. This is historical project experience, not a promised yield on another target. Dbsqlfuzz itself is proprietary; do not recommend installing an assumed public implementation.
- Decision relevance: look for interacting dimensions excluded by an existing lane, such as state+program or recovery+fault, rather than only turning up input volume. Reuse a target's existing seams and stated guarantees; no universal simulation layer follows from this account.

### S8: FuzzBench experiment interpretation

- URLs: https://google.github.io/fuzzbench/ and https://google.github.io/fuzzbench/reference/report/
- Read: overview/sample report; experiment/per-benchmark summaries; accessed 2026-11-07.
- Quote fragment: “distribution of the reached coverages”.
- Documented behavior: reports aggregate repeated trials, show variability and compare benchmarks. Default coverage rankings are coverage measurements, not a direct count of newly confirmed defects.
- Decision relevance: a single lucky pilot doesn't establish that one lane wins. If comparative claims matter, preserve matched trial budgets, inputs/configuration, independent runs and variability. Don't import a universal trial count from FuzzBench's example or claim statistical certainty from a tiny local pilot. A cost-limited pilot can guide a provisional next allocation without being a publishable experiment.

### S9: libFuzzer operational limits

- URL: https://llvm.org/docs/LibFuzzer.html
- Read: Running, Options, Parallel Fuzzing, Output; accessed 2026-11-07.
- Quote fragment: “maximum total time in seconds”.
- Documented behavior: `-runs` and `-max_total_time` bound search; `-timeout` and `-rss_limit_mb` are separate per-case resource controls. File inputs replay rather than launch mutation search. `cov`, `ft`, `corp`, `exec/s`, and `rss` are distinct output metrics. Exact artifact paths must not be shared by parallel processes.
- Decision relevance: record wall time, worker count/CPU, per-case limits and retained artifacts separately. A timed-out harness resource limit must be interpreted through the product's actual resource/progress guarantee. The foundation should link to a runtime execution owner, not carry all engine flags.

### S10: OSS-Fuzz corpus access

- URL: https://google.github.io/oss-fuzz/advanced-topics/corpora/
- Read: Obtain access; Downloading; Backups; accessed 2026-11-07.
- Quote fragment: “daily zipped backups”.
- Documented behavior: corpus access requires project authorization and uses project-specific storage; backups preserve inputs from previous periods.
- Decision relevance: check whether an existing usable corpus already exists before rebuilding search material; don't assume public access or authority to download private corpora. The new plugin needs neither a GCS account nor its own corpus storage service.

## Campaign decision model for the drafter

The following are **design recommendations/inferences** from the cited observations, not claims of a universal optimal strategy or a proven expected bug rate.

### The experiment unit

Represent a candidate lane in a short ordinary-file record with:

- target source/build/runtime/configuration and actual public producer path;
- failure space not already covered by inspected baseline;
- stated guarantee and executable oracle, including unsupported/inconclusive outcomes;
- generated input/initial state plus controlled scheduling/fault/configuration dimensions;
- pilot resource envelope: elapsed time, workers, CPU/memory/disk limits, external service use;
- preserved replay material and measurement of what reached the oracle;
- observed findings, their classification/reproduction state, and next decision.

This is a compact experiment description, not a mandatory new schema, service or scheduler. Reuse the project's notes and existing artifact conventions. Preserve original input and raw output before reduction or LLM summaries. Source basis: S1-S6, S9; Elle pp. 3,7-9.

### Diagnose the bottleneck before spending the next tranche

| Observed pilot evidence | Decision to investigate | Why that differs from longer identical execution |
|---|---|---|
| The target API is outside harness reach | Existing producer/harness entrypoint, enabled configuration and whether another lane reaches it | Mutation cannot enter code not called by the lane (S3). |
| Inputs parse but successful dependent behavior almost never occurs | Missing object/type/permission/sequence state; stateful or semantic generator | Jointly search state and operations, an advance illustrated by SQLite S7; benchmark actual semantic success, not assumptions. |
| Executions reach intended behavior but the oracle is only crash/no-crash | A justified result/effect/recovery relation or independent model | Wrong-result discoveries require an observable discriminator; Elle pp.3,7-9 and SQLite S7 motivate this dimension. |
| Reachable branches stall behind comparisons or rare schedules | A compatible value-profile/dictionary/solver/schedule technique with its own applicability research | These are hypotheses for a different search mechanism, not proof that installing another fuzzer helps. S1/S3 establish the diagnostic distinction; specialists must validate the selected technique. |
| Repeated slow/OOM/timeout cases dominate the run | Reproduce and classify; consider dedicated resource/progress lane or fix a verified harness defect | Continually discarding unexplained failures loses evidence; continually rediscovering one case also consumes search. S4/S9 inform the tradeoff. |
| Many plausible failures and little completed triage | Reduce, reproduce and classify before scaling generation | Raw count can exceed maintained evidence capacity. S5/S6 support retained reliability/build evidence; the allocation choice is a design judgment. |
| Healthy progress and distinct property-relevant states continue | Extend the useful lane within the authorized envelope; compare a complementary pilot if worthwhile | More compute remains useful when the search and oracle are demonstrably informative. S1/S2/S4. |
| Stable plateau and no accepted new evidence | Diagnose omission first; stop, change dimension or record a bounded negative result | A plateau is a reasoned allocation signal, not proof of correctness or proof that no rare bug remains. S3/S4/S8. |

### What to measure

Keep several metrics rather than collapsing everything into a score:

- **Search:** accepted executions, property evaluations, semantic states/transitions and specified effects reached; code coverage where instrumented.
- **Candidate quality:** raw failures, reproduction success, explicit unknown/unsupported cases, confirmed product defects, harness/infrastructure findings and verified duplicate groups. Label symptom-only clustering as provisional.
- **Cost:** wall time, CPU/worker usage, peak resources, setup, reduction/replay and human/LLM triage effort. A ten-worker half-hour run is not equivalent resource use to a one-worker half-hour run.
- **Progress over time:** new property-relevant reach and newly reproduced evidence per comparable interval; keep raw counters to avoid changing denominators silently.

Use confirmed unique product defects as an outcome when evidence supports it; use reach/sensitivity as provisional evidence when no defect has yet appeared. Don't rank a semantic lane below a crash lane solely because its assertion evaluates fewer inputs per second. These are proposed measurement choices derived from S2-S9, not validated productivity metrics.

### Reallocation and stopping

Use the observed bottleneck to choose continuation, redesign, complementary lane, reduction/triage, or stop. Record the selected reason and the untested space. Zero findings within a finite budget is a legitimate result. Budget exhaustion, incompatible tools, observer limits and unprocessed candidates are separate outcomes. Avoid fixed universal time/core/coverage thresholds; neither the source evidence nor Barn establishes them. Do not let this skill imply authority for cloud spending, target edits, production failure injection, installation or external publication.

## Barn calibration and portability

The approved plan/domain report is the complete inspected baseline record. This researcher additionally read existing `origin/master` source for `internal/fuzzseed/structured.go`, `vm/fuzz_test.go`, and `scripts/check_elle.py`; output of the combined source read was truncated, so no claim of an exhaustive fresh reread is made.

Visible source establishes initialized-variable/IR-based program construction and explicit normalized value exclusions, and the Elle checker lists twenty negative-control fault modes and distinguishes true/false/unknown verdicts. These are already available without the new plugin. The foundation should use Barn as an evaluation input, not hardcode Barn paths, MOO semantics or this user's paper collection into distributed instructions.

The concrete capability test is whether the campaign identifies a supported missing dimension and an executable way to observe a violation beyond that baseline. State+program, world effects, scheduling, persistence interruption and resource growth are candidates to evaluate, not findings that Barn is broken or proof that no other branch covers them. Use source/configuration inventory for the actual target before deciding.

## Suggested behavioral evaluations

Give the evaluator raw project artifacts and an explicit finite resource budget, with the skill; do not reveal the intended method or defect. Preserve both decisions and produced artifacts.

1. **Advanced baseline:** an inventory containing structured source generation, differential return values and history negative controls. Observe whether the agent accurately identifies existing capability, inspects a real uncovered producer/contract and proposes a justified pilot instead of only longer native fuzzing.
2. **Uninformative high-throughput lane:** a corpus/log showing huge counts but no execution of a public state-dependent operation. Observe whether the agent diagnoses reach and state prerequisites before scaling compute. Accept alternate evidence-backed methods, not a predetermined tool name.
3. **Noisy discoveries:** raw candidates with repeatable and intermittent failures, build identities, duplicates and infrastructure loss. Observe preservation, qualified counts and allocation to replay/reduction versus further generation.
4. **Matched pilots:** two observed result histories, one faster and one with different property reach. Observe whether the decision distinguishes oracle coverage from throughput and states uncertainty rather than inventing a statistical winner.
5. **Zero-finding budget:** a finite run with valid search and no product defect. Observe truthful negative results, tested-contract limits and a reasoned next decision, without invented discoveries or unsolicited spending.

These are evaluation designs, not executed tests and not evidence that the foundation already changes behavior. Historical or injected realistic defects can assess discovery power in isolated evaluations, with their locations hidden from the agent; report the comparable baseline and actual observed result before claiming improvement.

## Tooling and unsupported assumptions

This foundation is a decision skill, not an installer/runner. Commands quoted above were read from current primary docs, not executed here. No new project dependency is required. Runtime-specific references belong to the relevant specialist skills. Precise setup/license/platform/tool-version details must be verified before a target-specific execution; no generic Valgrind/AFL/KLEE applicability to Go is implied. Existing source docs contain commands that change host security settings or signal processes by name; they must not be copied as authorized campaign setup/cleanup. Preserve scope and use only owned resources.

The developer-referenced `C:/Users/Q/.Codex/AGENTS.md.d/researcher.md` was absent on a direct existence check. The explicit parent task and installed skill instructions govern this report. Initial guessed ClusterFuzz/FuzzBench URLs failed; the current ClusterFuzz performance page was reached from its triage navigation, and FuzzBench report from its homepage. Failed URLs supply no facts.

## Drafter handoff

Draft the foundation as a compact capability-selection workflow with a worked campaign decision and conditional links to specialist skills. Put substantial pilot diagnosis, measurement interpretation and examples in relevant references. Ship `common-mistakes.md`, `sources.yaml` and meaningful campaign-specific depth. Attribute factual tool/paper claims inline to S1-S10 or the original Elle paper; cite source sections/page numbers where useful. Treat proposed recording/decision conventions as the plugin's design, not externally proven laws. No new helper code, automatic executor or universal scoring formula is justified by this research.
