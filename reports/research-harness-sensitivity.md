# Research: harness-sensitivity

Date: 2026-11-07

## State

Per-skill research complete for drafting. This report is the only repository artifact owned here; literature artifacts are in a separate task-local collection. No skills drafted, targets changed/executed, tools installed, commits or publication.

Latest Q instructions relayed by parent after this research completed: use ONLY the research-papers plugin's paper-reader, NEVER paper-process. No further paper-process, tagging or reconciliation orchestration will run. The historical completed operations below are recorded accurately and are not instructions for future work. Existing page-image reads remain the literature evidence. Any additional paper work must use paper-reader only.

## Evidence ledger

### S1: OSS-Fuzz ideal integration

- URL: https://google.github.io/oss-fuzz/advanced-topics/ideal-integration/ ; accessed 2026-11-07; sections Fuzz Target, Coverage, Regression Testing.
- Quote fragment: “make at least some progress”.
- Finding: short initial execution should establish progress rather than immediate failure; corpus regression replay is distinct from discovery fuzzing. Coverage diagnosis can point to missing seeds, dictionaries and harness time/resource bottlenecks.
- Decision relevance: require evidence that a proposed oracle actually executes and that a healthy baseline completes; do not count construction or compilation of a harness as sensitivity.

### S2: Fuzz Introspector

- URL: https://google.github.io/oss-fuzz/advanced-topics/fuzz-introspector/ ; accessed 2026-11-07; overview, local running, build tooling.
- Quote fragment: “static reachability potential”.
- Finding: the documented integration distinguishes static reachable code from observed execution. This page supports C/C++, Python and Java, with LLVM LTO/Gold, PyCG and Soot build restrictions respectively.
- Decision relevance: diagnose an unreachable public operation separately from reached code whose results are unchecked. Do not prescribe this tool for Go from its general name. Documented example `python3 infra/helper.py introspector libdwarf --seconds=30` requires a compatible OSS-Fuzz checkout/build; it is not a universal command. No invocation was executed.

### S3: PIT basic concepts

- URL: https://pitest.org/quickstart/basic_concepts/ ; accessed 2026-11-07; Mutation Operators, Equivalent Mutations, Running the tests.
- Quote fragment: “No coverage”.
- Finding: bytecode mutation requires line/source debug metadata. Outcomes distinguish killed, survived, uncovered, nonviable, timed-out, memory-error and run-error cases. Equivalent mutations can preserve behavior or differ outside the asserted scope.
- Decision relevance: a surviving mutation is a prompt to diagnose reach, state change and observation; it is not automatically a missing product test. A broken mutant build is not a successful semantic check.

### S4: Stryker states and metrics

- URL: https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/ ; accessed 2026-11-07; Mutant states, Metrics.
- Quote fragment: “killed + timeout”.
- Finding: Stryker counts killed tests and timeouts together as detected; invalid runtime/compile mutants are excluded from mutation score. Raw outcomes therefore carry more information than the score.
- Decision relevance: retain whether the intended oracle rejected the representative fault, whether only a watchdog fired, or whether the harness broke. A timeout may detect a real liveness violation, but cannot establish sensitivity of a separate value/effect oracle. Apache-2.0 shown in footer; concrete runtime setup remains to verify.

### S5: Mutation sensitivity versus real faults, literature image evidence

- Primary paper: René Just, Darioush Jalali, Laura Inozemtseva, Michael D. Ernst, Reid Holmes, Gordon Fraser (FSE 2014), *Are Mutants a Valid Substitute for Real Faults in Software Testing?*, DOI https://doi.org/10.1145/2635868.2635929 ; author PDF https://homes.cs.washington.edu/~rjust/publ/mutants_real_faults_fse_2014.pdf . Accessed 2026-11-07.
- Historical workflow completed before Q's revised literature instruction: paper-process fallback, retriever, reader, tag and reconcile steps. `fetch_paper.py` DOI metadata lookup returned HTTP 429 from Semantic Scholar and `Could not resolve metadata`; retriever's documented author/open-repository fallback retrieved the exact PDF. Title/authors independently checked on rendered p.1. All twelve local page images read directly, no extracted paper text. Notes, metadata, description, abstract paraphrase, all 42 bibliography entries, index, processed ledger and generated keymap exist at `C:/Users/Q/code/bugfinding-literature/harness-sensitivity/papers/Just_2014_MutantsRealFaults/`. Tagging verified three existing description/index tags; reconciliation found no other processed papers, zero forward/reverse/conceptual links and four new leads. No propstore work. Full-abstract transcription adapted to paraphrase; metadata abstract remains null because metadata lookup failed. No further process/tag/reconcile orchestration is requested or needed.
- Pages 3-4: faulty/fixed revisions and paired tests isolate the actual fault from unrelated changes, build failures and nondeterminism. Use historical controls only after confirming their failure really comes from that defect.
- Pages 5-6: mutant execution, changed state and an observed assertion/exception are different; coverage influences mutation-score changes. Evaluate what a control actually demonstrates.
- Pages 7-10: common operators miss algorithm changes, contexts, invariants and selected numerical/literal faults. Results from five Java projects cannot establish completeness for a new storage/Go/distributed contract. Representative controls support bounded sensitivity claims, not an invented expected product-bug yield.
- Decision relevance: historical faults or carefully justified contract-specific controls may reveal missing semantic observations that generic mutation scores miss. Keep the oracle's outcome and witness, not merely tool-level “killed”.

### S6: PIT Maven integration

- URL: https://pitest.org/quickstart/maven/ ; accessed 2026-11-07; Installation, mutationCoverage, Dry Run Mode, targetClasses/targetTests, crossModule.
- Quote fragment: “without running any tests against the mutants”.
- Documented integration: configure `org.pitest:pitest-maven` in the existing Maven project with a project-selected compatible version; execute `mvn test-compile org.pitest:pitest-maven:mutationCoverage`. Narrow source/test globs rather than mutate everything. Dry-run introduced in 1.17.3 gathers coverage and mutants without executing mutant tests; it cannot establish assertion sensitivity. Cross-module reporting needs deliberate ownership to avoid duplicate/undefined aggregation. This is JVM/Maven guidance, not a Go recipe. No command executed.
- License verification: https://github.com/hcoles/pitest shows Apache-2.0. The guessed `LICENSE` blob URL returned 404; that URL supplies no evidence. Current Java/test-runner plugin compatibility must be checked against the selected release before execution; no minimum is claimed here.

### S7: StrykerJS integration and coverage

- URLs: https://stryker-mutator.io/docs/stryker-js/getting-started/ ; https://stryker-mutator.io/docs/stryker-js/usage/ ; https://stryker-mutator.io/docs/stryker-js/configuration/ ; accessed 2026-11-07.
- Sections: installation/run; configuration selection; mutate/buildCommand/checkers/coverageAnalysis.
- Documented setup: `npm init stryker@latest` installs and initializes project configuration; `npx stryker run` performs mutation testing. Installation is a target change, not an action implied by this research. Existing configured integration should be preferred. Scope `mutate` to the relevant source and choose the actual runner/checker; command-line options replace corresponding config values. Per-test coverage can optimize execution, but requires independent tests and runner support. The generic command runner cannot supply the same per-test coverage evidence as supported adapters. Use actual installed package/runtime requirements, not an assumed universal Node version. Apache-2.0 shown by docs; no exact Node support claim.

### S8: Stryker.NET integration

- URL: https://stryker-mutator.io/docs/stryker-net/getting-started/ ; accessed 2026-11-07; prerequisites, project install, Prepare, run.
- Documented setup: current page requires .NET 10+ **for the tool runtime**, even when the application targets older .NET. Existing local tool integration uses `dotnet tool restore`; new local setup uses a tool manifest and `dotnet tool install dotnet-stryker`. Run `dotnet stryker` from the test-project directory. Framework-specific applications also require NuGet tooling. Version-sensitive prerequisite must be rechecked for selected release. Do not change target runtime merely to match the mutation tool's runtime. Apache-2.0 per docs. Commands were not executed.

## Actual Barn baseline read

Read existing fetched `origin/master:scripts/check_elle.py` directly on 2026-11-07 without fetch or target mutation. `FAULTS` at lines 11-18 lists twenty removed protections. Lines 22-30 demand one exact true/false/unknown verdict for the requested history; exit status alone is insufficient. Lines 56-69 generate healthy and faulty cases from matched seeds/workloads, with controlled waves to avoid relying on lucky scheduling. Lines 74-103 require nonempty histories, expected verdict/exit and anomaly witness text. This is source evidence, not a new run or live remote claim.

The new skill must exceed repeating those controls. A useful next application inspects a newly proposed world-effect, recovery or numerical oracle and discovers whether a representative violation reaches it and changes its result. No absence claim about other Barn tests is made.

## Proposed decision workflow for the drafter

This is plugin design inferred from the source evidence, not a normative outside standard or a required new framework.

1. **Select the exact claim.** State the producer, enabled path/config, guarantee, expected healthy result and intended checker outcome. Example: an acknowledged operation must survive a specified failure model only if actual storage documentation promises that guarantee. Do not invent it from the example.
2. **Use the smallest relevant real control.** Prefer an isolated historical regression or existing defect switch. If none fits, justify a narrowly introduced control from actual source, such as suppressing a required state update. Don't inject arbitrary syntax errors and call them semantic controls. Keep controls out of production execution; existing task authorization governs edits and runs.
3. **Observe what happens at each necessary boundary.** Did the same actual producer run? Did the mutation/fault become active? Did it alter relevant state? Was the changed effect observable? Did the intended oracle reject it with a witness? Logs/counters/snapshots should identify the first unanswered boundary. Merely reaching the source line establishes less than all five observations.
4. **Run the healthy and faulty cases with matched inputs/configuration.** Preserve raw logs and producer/control provenance. An always-failing harness cannot demonstrate useful discrimination; an unrelated build error, killed process, malformed history or assertion in setup is not rejection by the claimed semantic oracle.
5. **Classify each control explicitly.** Healthy pass and fault rejected by intended oracle supports the selected sensitivity claim. Fault never reached, equivalent/irrelevant change, changed-but-unobserved effect, timeout, invalid build, checker unknown and infrastructure failure require different next actions. Do not silently add them to a “passed” denominator.
6. **Report scope and use evidence to improve the existing owner.** Repair a verified reach/observation/check defect in the current harness/check when authorized; retain the control as a meaningful regression if it protects the contract. Then resume the relevant discovery method. No universal mutation percentage, additional recurring gate or new control framework follows from this skill.

### Outcomes that change the next action

| Observed control behavior | What it establishes | Next investigation |
|---|---|---|
| Relevant method absent from call graph | Harness can't reach claimed behavior in this lane | Existing public producer/configuration seam |
| Method executed but no changed relevant state | Control may be inactive, equivalent or irrelevant | Control activation and contract-specific inputs |
| State changed but observed output unchanged | Propagation/observation may hide defect, or effect outside scope | World/recovery/history evidence and oracle contract |
| Intended oracle returns explicit violation and witness | Sensitivity to this representative fault under these conditions | Retain replay; expand only within evidence |
| Generic timeout rejects wrong-value control | Process failed to finish; intended value oracle sensitivity unestablished | Root cause and progress contract |
| Mutant won't compile/load or test runner crashes | Invalid experiment, not product violation | Build/tool compatibility and ownership |
| Checker returns unknown or missing witness | Inconclusive for promised anomaly claim | Observation loss/checker limits |
| Healthy control also rejected | Discrimination or baseline problem | Actual guarantee, baseline health and harness isolation |

## Advanced worked applications

### World effects beyond returned values

An existing differential lane compares only printed results while a program mutates a permissioned object. First establish that both engines receive equivalent worlds and execute a successful operation. A justified control suppresses one committed effect while preserving the printed result. If the comparator accepts it, longer input search cannot reveal that effect discrepancy. Extend the existing comparison owner to observe the promised effect; then repeat the same control. This is an illustrative experiment design, not a Barn defect finding. Basis: S1/S2 reach and coverage; S5 missing semantic operators; correctness of the particular effect belongs to the target contract.

### Recovery acknowledgment

For a target with an explicit durable-acknowledgment guarantee and controllable persistence boundary, choose a known historical lost-acknowledgment case or an equivalent narrow control. Record acknowledged operation, fault point, recovery and recovered-state assertion. A process dying as expected is not the oracle; losing the acknowledged operation must produce the intended recovery witness. Completed round-trip equality does not test the interrupted boundary. This is a proposed acceptance scenario, pending target storage-source research and authorized disposable execution.

### Context and history

A control removing a validation check can still appear harmless when no competing update occurs, or when the recorder collapses retry attempts. Establish the conflicting state and recorder observation before interpreting checker success. Barn's current checker already demonstrates matched seed/workload, explicit outcomes and witnesses; use that standard for a new dependency dimension rather than claim reimplementation as a new contribution.

## What belongs in the skill and references

- Compact audit entrypoint: claim, representative control, healthy/faulty execution evidence, explicit classification, bounded conclusion and correction in existing owner.
- `references/common-mistakes.md`: wrong/right interpretation examples for dry-run, coverage-only, timeout-only, invalid mutants, always-failing setup, equivalent controls, historical fault contaminated by unrelated changes, generic mutation scores and ignored unknowns. Cite S1-S8 at each factual claim.
- A substantive control-design/interpretation reference: the outcome table and world-effect/recovery examples, with target guarantees explicitly unresolved until source inspection.
- Optional runtime reference for actual existing PIT/Stryker integrations. Keep general audit usable without installing a tool. Do not add Go mutation tooling from an unverified name; no Go mutation backend was investigated deeply here. Existing targeted controls and historical regressions are valid routes.
- `sources.yaml` should inventory S1-S8 with exact page/section use and dates. Paper provenance can point to DOI/author PDF and page range; no local machine path should be required by distributed instructions.

## Existing skills, quality and limits

Read installed `golang/go-testing-advanced` SKILL.md: it covers native fuzzing seeds, assertion properties, basic coverage and concurrency testing. It does not supply this report's representative-control discrimination procedure. This is a bounded overlap observation, not a complete marketplace novelty claim. No empirical model-competence test or broad external-marketplace audit was performed; keep generic definitions and language testing tutorials out of the new skill.

All tool commands above were read in primary documentation, not executed. No mutation tool installed. Exact release compatibility must be rechecked at target execution; no unverified commands are offered for Go, Rust or Python mutation systems. Failed PIT license URL and Semantic Scholar lookup supplied no technical facts. No cloud/process cleanup, CI rule bypass or repeated approval process is needed to implement this audit skill.

## Behavioral evaluation suggestion

Give an independent evaluator raw harness/control artifacts containing a healthy case, a reached-but-unobserved state change, an inactive control, a genuine intended-oracle rejection, and an unrelated runner timeout. Ask it to determine which claimed guarantees are actually sensitive and improve a verified existing observation defect within allowed scope. Do not reveal expected diagnoses. Success is correct artifact-backed distinctions and a replayable control demonstrating the repaired oracle, not a guessed mutation-score target or promised real-bug count. This evaluation has not been executed here.
