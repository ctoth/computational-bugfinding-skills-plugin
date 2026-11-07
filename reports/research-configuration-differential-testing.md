# Research: configuration-differential-testing

Date: 2026-11-07

## State

Primary-source research complete for the bounded handoff below. This is the only owned repository output. Other agents' skills, improvement/formalism reports and task-note text are preserved. Literature uses paper-reader and direct page images only. No target action, dependency installation, staging, commit or publication.

## Evidence ledger

Inspecting constrained valid configuration products, interaction coverage, actual PICT/ACTS contracts and semantic comparison/reduction. No exhaustive coverage or bug-yield claim.

## Verified discovery state

- PICT actual main ref observed with git ls-remote: `ab76c2548f551fcb46314e58653a1bd1172f3a72`. Pinned primary docs/source will ground commands and constraints.
- Supplied `usnistgov/acts` repository does not exist at the queried public URL (web404 and git repository-not-found). This supplies no implementation evidence. NIST's actual project/tool-distribution pages are the appropriate discovery owner.
- Selected paper from NIST's official publication record: Kuhn, Kacker and Lei, *Measuring and Specifying Combinatorial Coverage of Test Input Configurations*, publication DOI10.1007/s11334-015-0266-2. NIST-hosted preprint will be read as page images through paper-reader; automatic search/PDF text is not paper-reading evidence.
- Developer-referenced researcher role file is absent at its exact path. Assigned research scope and parent/common instructions govern this work.

## Primary findings saved progressively

- PICT's pinned guide documents constrained generation, mixed strengths/submodels, negative values, seed/replay and machine-readable rows. Its new best-of-N/parallel options optimize suite packing; they do not establish bug detection or execute the subject. Source: https://raw.githubusercontent.com/microsoft/pict/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md (Usage, Output, Constraints). Do not delete invalid rows after generation and still claim the valid pairs they uniquely covered were exercised.
- Actual NIST distribution page distinguishes freely downloaded Basic ACTS from the advanced constraint-capable tool obtained by request. Supplied GitHub ACTS URL was404. Source: https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software/downloadable-tools (Downloadable Tools, accessed2026-11-07). No email/contact request or installation was performed; PICT supplies a directly researched open-source constrained route without inventing ACTS commands.
- Fifteen-page NIST-hosted paper rendered successfully; all images000–014 directly read. Paper pp.2–5 distinguish simple t-way coverage from total variable-value coverage, and a covered factor-value tuple from a triggered/detected fault. The fault-coverage estimate depends on an assumed fault profile and deterministic behavior; its historical small-interaction observations cannot promise that pairwise testing finds every bug in a new target. No extracted PDF text is evidence.

## Completed literature reading

All fifteen images `page-000.png` through `page-014.png` were directly inspected through the paper-reader page-image lane. Local collection: `C:/Users/Q/code/bugfinding-literature/configuration-differential-testing/papers/Kuhn_2016_MeasuringCombinatorialCoverage/`. Canonical PDF and rendered images are retained outside the plugin and are not package dependencies. The paper-reader's reconciliation/propstore workflow is excluded by the assigned reader-only scope. The publication is a measurement/theory paper with historical examples, not a controlled comparison on Barn or a present-day fault-yield estimate. [Official publication record](https://csrc.nist.gov/pubs/journal/2016/12/measuring-specifying-combinatorial-coverage-test-i/final), [NIST preprint](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=917142), DOI `10.1007/s11334-015-0266-2`.

Decision-changing findings: the paper distinguishes the proportion of fully covered factor subsets, total tuple coverage, and the minimum coverage of any subset (pp.2–3). A fault-coverage calculation additionally requires a fault interaction profile (pp.3–5). Its branch result requires the modeled values to reach the relevant branch variables; transformed internal values can invalidate that premise (pp.6–7). Appendix III changes hypothetical fault profiles while keeping the test arrays fixed, producing substantially different predicted fault coverage; Appendix IV makes the same point for an existing spacecraft suite (pp.14–15). These are reasons to report actual supported-domain tuple coverage and oracle execution separately. They do not justify a universal strength or reliability percentage. Exact short fragment for citation: “fault coverage” (p.15); use paraphrase for the remainder.

## Scope and capability added

The capability is to search **valid configuration interactions that can change an otherwise shared semantic result**, while carrying the same input and explicit preconditions across comparable executions. This is an execution method built on a configuration model, not a matrix service or a replacement build system. Reuse the subject's real build/test owners. Existing semantic-differential-testing owns general oracle comparison; correctness-oracles owns contract selection; failure-reduction owns input reduction. This skill should own factor modeling, constraints, configuration-sensitive test selection, evidence of the configuration actually exercised, and reduction of responsible configuration changes.

Existing-skill overlap checked: the installed `golang:go-testing-advanced` entrypoint and fuzzing/benchmark sections cover Go fuzz inputs, seed regression, benchmarks, virtual time and code coverage. That is useful target-runner guidance but does not supply this report's constrained configuration model or paired configuration-reduction method. Do not duplicate its Go fuzzing tutorial or make this package depend on its installed path. The approved plan's acceptance example requires a justified capability combination reaching a path outside a core-only lane and a reduced configuration retaining the violated guarantee; the scenarios below are proposed evaluations of that capability, not claims of a completed target experiment.

Research synthesis, not a claim from the paper: testing every runtime separately at its default settings can miss a runtime × optional capability × optimization interaction. A covering array can expose such a combination efficiently, but only if its factor values are real, its constraints preserve supported configurations, the selected test reaches the relevant behavior, and an oracle observes a violated guarantee. A large generated table alone adds no bugfinding capability.

## Model before search

Recommended method, derived from the literature's modeled-domain limitations and PICT's constrained generation contract:

1. Read the supported build/platform/runtime/capability contracts and actual test/build commands. Record a finite set of factors with their concrete producer: a build flag, selected binary, environment variable, runtime switch, detected platform capability, or existing test fixture. Record values, default, and what proves the requested value took effect. A configuration label is insufficient evidence.
2. For each constraint, cite the owner of the restriction. Distinguish a product exclusion, a semantic precondition, and an unavailable local execution lane. Unavailable infrastructure is an unexecuted supported configuration, not an invalid product. A build that fails for a documented supported tuple is a candidate finding; never make it disappear by adding a constraint inferred from that failure.
3. Give each comparable group a shared contract and admitted input domain. Selecting a different numeric model, locale, consistency mode, feature semantics, or wire format can intentionally change results. Compare the guarantees that both modes promise; do not force complete equality. A feature's disabled state may require absence/rejection while its enabled state requires a result. Those require separate conditional assertions.
4. Partition values by behavior with evidence, retaining boundary values and capability states. Do not merge values solely because they produce identical results in a small probe. An alias is unsuitable for two spellings/platform values whose different behavior is part of the experiment.
5. Identify the complete constrained domain when tractable. Start with full enumeration when cheap enough; otherwise use a requested interaction strength, plus explicit regression rows and high-risk higher-order groups. State which universe was modeled and the residual untested combinations. Never describe pairwise coverage as exhaustive testing.

The necessary constrained tuple universe is the projection of **full valid configurations**, not every locally noncontradictory partial assignment. For factor subset J, let V_J be all value tuples that extend to at least one supported full configuration. An executed suite covers E_J contained in V_J. Report `|E_J|/|V_J|`, with zero-denominator subsets treated explicitly, and aggregate/minimum measures as appropriate. This definition is the proposed constrained adaptation of the paper's coverage distinctions, not a theorem copied from it. It prevents impossible pairs inflating the denominator and silently skipped valid pairs disappearing from it.

## Verified PICT route

Source identity observed with `git ls-remote`: `ab76c2548f551fcb46314e58653a1bd1172f3a72`. Do not substitute a moving branch link in the draft. These are source-verified conditional recipes; no executable was installed, built or run in this research.

- [README, build sections](https://github.com/microsoft/pict/blob/ab76c2548f551fcb46314e58653a1bd1172f3a72/README.md): Windows route uses Visual Studio2022/VC++ tools and `_build.cmd`; non-Windows route requires CMake and a C++ toolchain. Build commands are `cmake -DCMAKE_BUILD_TYPE=Release -S . -B build` then `cmake --build build`. This is optional tool preparation, not a request to replace target build ownership. The README's container recipe uses a floating image tag and should not be copied as a reproducible recipe.
- [LICENSE.TXT](https://github.com/microsoft/pict/blob/ab76c2548f551fcb46314e58653a1bd1172f3a72/LICENSE.TXT): MIT license; retain required notice when redistributing. Short exact fragment: “MIT License”. No claim about unrelated dependencies follows.
- [Guide, Constraints/Sub-models/Seeding sections](https://github.com/microsoft/pict/blob/ab76c2548f551fcb46314e58653a1bd1172f3a72/doc/pict.md): generate with constraints rather than deleting invalid rows afterward. Submodels support chosen interaction groups; a seed row that violates constraints can be omitted. Negative values separate invalid-value cases. These behaviors require validating the model and preserving mandatory regressions outside the packing step. Short fragment: “will be skipped entirely”.
- [CLI option parser, parseArg/showUsage](https://github.com/microsoft/pict/blob/ab76c2548f551fcb46314e58653a1bd1172f3a72/cli/cmdline.cpp): `/o:N|max` selects order, `/r:N` sets a seed, `/e:file` loads seed rows, `/c` makes model comparison case-sensitive, `/t:N` selects worker count, `/f:json` selects JSON output, `/s` switches to statistics. Do not use `/s` when expecting the normal table. Hidden approximate/preview modes are unsuitable for claiming complete requested interaction coverage. Pinning matters: an older release may not accept the current source's options.
- [Generation/seed search, execute/findBestSeed](https://github.com/microsoft/pict/blob/ab76c2548f551fcb46314e58653a1bd1172f3a72/cli/pict.cpp): `/b:N` tries consecutive seed values and selects the smallest successful generated suite, with deterministic earliest-seed tie breaking. `/t:N` controls generator workers, not target execution concurrency. Preserve stdout rows and stderr diagnostics, effective seed, tool identity, model and constraints. Packing fewer rows is distinct from finding more defects.
- [Model value handling, GetNamesForComparisons/GetNextName](https://github.com/microsoft/pict/blob/ab76c2548f551fcb46314e58653a1bd1172f3a72/cli/model.cpp): aliases cycle output spellings while comparisons use the primary name. Use independent values for behaviorally distinct cases. Case sensitivity and alias treatment belong in the saved model.

Conditional command for the verified source version, with an already prepared subject-derived model:

```text
pict configurations.txt /o:3 /r:12345 /t:1 /e:regressions.tsv
```

The numeral3 illustrates an explicitly chosen order; it is not a universal minimum. Save exact generated rows as the replay artifact rather than relying solely on regenerating them with a seed. The tool generates configurations; the subject's existing runner must apply each row and produce observations. Do not claim these commands were execution-validated here.

Illustrative PICT syntax (invented factor names; **not a supported target model**):

```text
Runtime: base, candidate
Backend: portable, accelerated
Capability: absent, present
Optimize: off, on
IF [Backend] = "accelerated" THEN [Capability] = "present";
```

That implication is permissible only when the actual target contract requires the capability. If the target promises accelerated mode will fall back when capability is absent, the implication would exclude exactly the behavior to test and must not be used. A failed row cannot supply its own exclusion rule.

## ACTS route and availability limits

[NIST Downloadable Tools](https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software/downloadable-tools), observed2026-11-07, page updated2026-06-08, sections Downloadable Tools and Software: Java ACTS has Basic download; Advanced supports constraints and is distributed by request. The page describes GUI/CLI and variable strength but does not establish an acquired runnable artifact or current exact command here. Short fragment: “supports constraints”. NIST describes its tools as public domain; scope that statement to the distributed NIST software, not an entire Java/dependency ecosystem. No request email was sent. **Do not publish a guessed `java -jar` constrained-generation command or equate Basic and Advanced.** PICT is the concrete open-source route verified above. The supplied `usnistgov/acts` GitHub URL is404; actual additional-tool repository is `usnistgov/combinatorial-testing-tools`, which is not evidence that ACTS source is there.

## Execution and differential oracle

The following is a proposed campaign method, not an empirical claim about a target:

- Use a stable input corpus or a saved generated input set across rows. Hold the oracle, fixtures and initial state fixed within each comparable group. For stateful subjects restore the same baseline; record service/environment state relevant to behavior. Preserve input seeds separately from the PICT generator seed.
- Capture requested and effective configuration, binary/build identities, command, working directory, dependencies/capability observations, input bytes/history, stdout/stderr, structured result and exit status. Reject a row that accidentally reuses the baseline binary or ignores its switch as harness evidence failure; no bug conclusion follows from the row label alone.
- Apply the paired semantic contract: ordered equality only when order is promised, multiset comparison when order is unspecified, representation-independent comparison where promised, and documented numeric/error rules. Save raw observations before normalization. An optimizer is generally expected to preserve the language's defined results, but undefined/unspecified behavior or a deliberately relaxed mode cannot be silently treated as the same contract.
- Classify build failure, unsupported capability, harness failure, timeout, crash, contract mismatch and pass separately. Preserve supported failing builds. A timeout is evidence of exceeding the recorded bound, not a proof of semantic inequality; repeating with a justified bound or specialist liveness work may be necessary.
- Count coverage only after the configuration is applied and the intended test and oracle run. Publish generated, buildable, applied, observed and compared counts separately. A generated-but-unexecuted row supplies no exercised semantic coverage. If target-input effects matter, configuration coverage of one inert input is inadequate: measure which relevant inputs/preconditions actually ran under the tuple.

Compute can be spent on greater interaction strength, several independent arrays to diversify full-row contexts, more inputs per row, targeted boundary inputs for uncovered behavior, or costly real-platform lanes. Compare marginal evidence/unique reproducible findings against the measured cost. PICT's best-of-N reduces packing cost; it does not choose the target configurations most likely to reveal bugs.

## Joint reduction and interpretation

Recommended reduction predicate: the same contract violation remains between two recorded executions, with both configurations supported, their input in the shared admitted domain, and the effective tested values confirmed. Save the original pair first. Reduce changed factors toward a supported baseline while keeping prerequisite closure; reject invalid simplifications rather than treating their build failures as reproductions. Where one-factor removal is impossible because features are coupled, test valid groups of changes and state that coupling. Then reduce the input/history under that same pair, alternating when simplification reveals that another factor is unnecessary. Preserve fixture and numeric/environment preconditions.

The result is a locally reduced witness relative to the attempted moves. A factor that disappears in one reduction is unnecessary for that witness; this is not proof that all other factors or interactions are globally irrelevant. Discovery at strength2 does not prove the bug has order2: that full row contains many higher-order tuples (paper pp.4–5,8). One differing platform pair is not a root-cause diagnosis. A product contract violation should retain the supported-build documentation alongside the concrete failing invocation.

## Advanced worked scenarios for the drafter

1. **Compiler/runtime optimizer with optional backend.** Use the same defined-semantics input under reference/candidate runtime, optimization and backend/capability factors. First establish the real capability/fallback contract. Select configurations with a covering array and a higher-order optimizer/backend/runtime group when warranted; run input families reaching the affected lowering paths. Preserve semantic output, errors and effective backend evidence. If optimized candidate+accelerated differs, first remove unrelated flags along valid configurations, then reduce the program while retaining defined behavior. This goes beyond collecting more core-language random programs: configuration changes are controlled experimental factors. No present target bug is asserted.
2. **Serialization/storage build variants.** Compare a documented portable logical roundtrip across architecture width/endianness/build codec/runtime only where the format and value-domain contract promises compatibility. Share exact input bytes, retain decoding errors and logical records, and avoid byte-equality if the format permits ordering/compression differences. If a feature-disabled build promises rejection, assert that rejection separately rather than comparing it to successful enabled output. A legitimate format-version difference is not a defect. Reduce a mismatching logical record jointly with enabled flags and platform pair.
3. **Capability fallback negative case.** A documented fallback path supports an absent capability. Include absence in the valid domain and compare its logical result to the accelerated path. Do not encode absence as an invalid negative value merely because an implementation crashes. If invalid combinations instead must be rejected cleanly, use a separate rejection-contract lane; PICT's one-negative-at-a-time convention does not establish that multi-invalid interactions are safe or uninteresting.

## Drafter handoff and limits

Build a method skill with a compact PICT reference and primary-source map. Require a concrete factor/constraint/contract/replay artifact and a reduced configuration witness when a violation is found; do not add a generic scheduler, matrix registry or helper framework. Source citations should accompany the particular mechanics they support, with the pinned paths above and small exact fragments; do not cite the coverage paper for the proposed target runner or configuration-reduction algorithm. Their status here is research synthesis.

No target campaign, build, installation, paper-process, staging or publication was performed. No bug-yield number, universal pairwise assurance, newest ACTS version, acquired Advanced ACTS command, or empirical cross-platform reproduction is claimed. All tool availability/source observations are dated2026-11-07. The separate local reader collection is evidence for this report, not something the packaged skill may require users to have.
