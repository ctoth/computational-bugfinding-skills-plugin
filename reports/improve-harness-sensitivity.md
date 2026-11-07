# Improve harness-sensitivity

Skill: `plugins/bugfinding/skills/harness-sensitivity/`. Accessed 2026-11-07.

## Findings

Baseline read: SKILL.md 42 lines, common-mistakes.md 43, control-design.md 45, runtime-integrations.md 41, sources.yaml 81. Governing pattern read in full: skill-draft, skill-audit, skill-improve SKILL.md and skill-improve common-mistakes.md; research-harness-sensitivity.md; Just 2014 paper-reader notes at `C:/Users/Q/code/bugfinding-literature/harness-sensitivity/papers/Just_2014_MutantsRealFaults/notes.md` (page citations only, no section numbers).

Decision on URLs: every docs site cited (pitest.org, stryker-mutator.io, google.github.io/oss-fuzz) is an unversioned page built from its repo's default branch, i.e. a moving alias under skill-draft Step 5. Each is repointed to the SHA-pinned raw GitHub source that I fetched at that SHA (same approach as the sibling failure-reduction improvement). Sources fetched with `gh api repos/<org>/<repo>/contents/<path>?ref=<sha>` (raw media type).

### F1. WARNING: SKILL.md:32 PIT outcome names do not match PIT
- Text: "PIT explicitly distinguishes surviving, uncovered, invalid and runtime-failure outcomes".
- Source (pitest-site `quickstart/basic_concepts.markdown` @614bec6, "Running the tests"): outcomes are "**Killed**", "**Survived**", "**No coverage**", "**Non viable**", "**Timed Out**", "**Memory error**", "**Run error**". "invalid" and "runtime-failure" are not PIT terms; Non viable = "could not be loaded by the JVM".
- Fix: use PIT's own outcome names with quoted fragments.

### F2. WARNING: SKILL.md:34 liveness sentence attributed to Stryker
- Text: "If progress itself is the promised property, use its justified liveness oracle instead ([Stryker states and metrics])".
- Source (mutation-testing-elements `docs/mutant-states-and-metrics.md` @a4f8163, "Mutant states"/"Metrics"): Timeout "is counted as \"detected\"" because "the tests will never complete"; Detected = "`killed + timeout`". The page says nothing about liveness oracles; the liveness sentence is the skill's inference.
- Fix: cite Stryker only for the timeout rationale (quoted) and state the inference as following from it.

### F3. INFO: Stryker and PIT claims elsewhere verified
- common-mistakes.md:13 and control-design.md:29: "Stryker counts timeouts as detected; invalid compile/runtime cases are excluded from its mutation score" matches: Runtime/Compile error "It is not represented in your mutation score"; "Mutation score `detected / valid * 100`".
- common-mistakes.md:25 "PIT reports nonviable and run-error outcomes separately from killed" matches. runtime-integrations.md:13 "Bytecode requires line-number/source-file metadata" matches "Line numbers" / "Source file name".
- Fix: add quote fragments and pin URLs.

### F4. WARNING: SKILL.md:20 OSS-Fuzz cited for the execution/state/observation split
- Text: the five-boundary convention "distinguishes execution, state change and observation ... ([Just et al., §2.5], [OSS-Fuzz integration])".
- Source (oss-fuzz `docs/advanced-topics/ideal_integration.md` @156f862, "Fuzz Target"): only "make sure that the fuzzer can make at least some progress" and "must have good coverage". Nothing on state change or observation.
- Fix: cite OSS-Fuzz only for the Producer step (quoted), Just for the detection split.

### F5. INFO: PIT Maven claims verified; threshold caution added
- runtime-integrations.md:7-13 verified against pitest-site `quickstart/maven.markdown` @614bec6: goal `mvn test-compile org.pitest:pitest-maven:mutationCoverage`; "limit which code is mutated and which tests are run using `targetClasses` and `targetTests`"; dry run "Introduced in 1.17.3" and "without running any tests against the mutants"; cross module "the results are undefined".
- Same page, "mutationThreshold": "your build may contain equivalent mutations. Careful thought must therefore be given when selecting a threshold." This directly supports SKILL.md:42's refusal to prescribe a mutation percentage, which was uncited.
- Fix: cite it at SKILL.md:42.

### F6. WARNING: runtime-integrations.md:17,29 license claims uncited
- Text: "StrykerJS is Apache-2.0 licensed." and "Stryker.NET is Apache-2.0 licensed." had no citation; PIT's cited the moving repo root.
- Source: `LICENSE` at stryker-js @8f24ef0 and stryker-net @2ec2d68, `LICENSE.txt` at pitest @1edd5b4 all open "Apache License / Version 2.0, January 2004".
- Fix: cite each pinned license file.

### F7. WARNING: runtime-integrations.md:23 StrykerJS command runner judges by exit code (gap)
- Text said per-test coverage needs a supporting runner, but not what the default runner can establish.
- Source (stryker-js `docs/configuration.md` @8f24ef0, "testRunner"): default is `command`, which "bases the result on the exit code of that program (0 for success, otherwise failed)"; "coverageAnalysis": coverage lets Stryker "distinguish between \"Survived\" and \"NoCoverage\"" and the `command` runner is excluded "since Stryker will just run your command has no way of knowing more about your tests".
- Fix: one sentence: under the `command` runner a killed mutant is only a nonzero exit, so the rejecting assertion must come from the test output. Directly serves the skill's "do not infer outcome from exit status" rule; no new machinery.

### F8. WARNING: runtime-integrations.md:25 Node requirement claim cited to a page that says nothing about it
- Text: "Verify the chosen package's Node/test-runner requirements rather than assume one runtime floor ([StrykerJS getting started])". The getting-started page says only "Make sure you have npm and nodejs installed."
- Source: `packages/core/package.json` @8f24ef0: `"version": "10.1.1"`, `"engines": { "node": ">=22.0.0" }`.
- Fix: cite the pinned package.json engines field for the checked release, keep the recheck instruction.

### F9. INFO: sources.yaml section names do not match headings
- StrykerJS Getting Started lists "Install", "Run Stryker"; actual headings are "1 Prepare", "2 Install", "3 Let's kill some mutants". Stryker.NET lists "Run Stryker"; actual heading is "Let's kill some mutants". PIT Maven lists "Getting started", "mutationCoverage goal", which exist.
- Fix: correct sections_used.

### F10. INFO: Fuzz Introspector claims verified
- oss-fuzz `docs/advanced-topics/fuzz_introspector.md` @156f862: "For projects written in C/C++, Python and Java"; "static reachability potential and compare it against dynamic coverage"; build tooling LLVM LTO/Gold, modified PyCG, Soot. Matches runtime-integrations.md:41 and the other citing lines.
- Fix: quotes and pinned URL.

Paper section numbers checked against the existing paper-reader page images of Just et al. 2014 (`pngs/page-001`, `-002`, `-004`, `-006`, `-007`, `-009`; image index n = paper p.n+1), viewed as images this session. No extracted text used.

### F11. ERROR: Just et al. §2.1 cited for fault isolation (SKILL.md:14, control-design.md:7, sources.yaml:78)
- Text: "[Just et al., §§2.1 and 3.2]" and "[Just et al., §§2.1–2.2]" for historical isolation.
- Source: p.2 "2.1 Subject Programs" lists project desiderata only. Isolation is "2.2 Locating and Isolating Real Faults" (pp.2-3), with "2.2.2 Discarding Non-reproducible Faults" (dependent / non-deterministic tests) and "2.2.3 Discarding Non-isolated Faults": "Isolation is important because unrelated changes could affect the outcome".
- Fix: cite §2.2 (with quote); SKILL.md:14 split so §2.2 supports the isolation sentence and §3.2 the operator sentence.

### F12. ERROR: Just et al. §2.5 cited for a state-change / propagation step it does not contain (SKILL.md:20, control-design.md:15, control-design.md:35)
- Text: "Its distinctions follow the difference between reaching code, changing its state and detecting the change ([Just et al., §2.5])"; "This experiment applies the state-propagation distinction from [Just et al., §2.5]".
- Source p.5 §2.5 defines only two relations: "A test is said to cover a mutant if it reaches and executes the mutated code. A test detects a mutant if the test outcome indicates a fault — a test assertion fails or the test causes an exception in the mutant." No state-infection or propagation step. The paper-reader notes also mark the decomposition as "a design inference".
- Fix: cite §2.5 for cover-versus-detect (quoted); state the activation/state/observation steps as this skill's audit convention.

### F13. WARNING: SKILL.md:8 range "§§2.5–3.2"
- The range spans §2.6 (experiments), §3.1 (coupling results) that the sentence does not use. The supported claim (coverage and detection are distinct) is §2.5.
- Fix: cite §2.5.

### F14. INFO: §3.2 and §5 claims verified; quotes added
- §3.2 (pp.7-8): "results derived from mutation analysis do not generalize to those real faults"; "Mutation analysis is context insensitive, while bugs can be context sensitive"; categories "Algorithm modification", "Violation of pre/post conditions or invariants", "Numerical analysis errors", "Specific literal replacements".
- §5 (p.10): "reveals some inherent limitations of mutation analysis"; selection/minimization "might lead to a reduced real fault detection rate of the test suite, even if the mutation score does not decrease."
- Fix: quotes at load-bearing places; sources.yaml section titles corrected to the paper's headings.

### F15. ERROR: SKILL.md:34 uncited normative claim
- Text: "A healthy case rejected by the same setup also leaves discrimination unestablished." No citation.
- Source: Just et al. §2.3 (p.3): "The resulting test suite T_fail fails on V1 but passes on the fixed source code version V2"; the paired design requires the fixed version to pass.
- Fix: cited §2.3 with quote; added §2.3 to sources.yaml sections_used.

### F16. ERROR: SKILL.md:14 uncited normative claim
- Text: "a syntax error or broken setup is not a substitute for the intended wrong effect" had no supporting source in its sentence.
- Source: PIT basic concepts: "A **non viable** mutation is one that could not be loaded by the JVM"; listed as an outcome separate from Killed.
- Fix: cited with quote.

### Applied to SKILL.md (F1, F2, F4, F5, F11-F16)
Edits at lines 8, 12, 14, 20, 32, 34, 36, 42; all URLs pinned.

### Applied to control-design.md (F3, F10, F11, F12, F14)
- :7 §§2.1–2.2 → §§2.2.2–2.2.3 with quotes ("dependent tests", "non-deterministic tests", "do not expose a real fault", "unrelated changes could affect the outcome").
- :9 §3.2 context quote added.
- :15 and :35 rewritten so the state/observation steps are labelled as the skill's convention and §2.5 is cited only for cover-versus-detect.
- :29 Stryker quotes added, URL pinned. :45 §5 selection/minimization quote added.

### Applied to runtime-integrations.md (F3, F5, F6, F7, F8, F10)
- :3 states the commits are pinned in each link.
- :7 PIT license → pinned LICENSE.txt; quote "By default pitest will mutate all code in your project".
- :13 quotes "Introduced in 1.17.3", "without running any tests against the mutants", "the results are undefined".
- :17 StrykerJS license cited; :23 command-runner exit-code sentence and coverage/CLI quotes; :25 install quote and pinned engines `"node": ">=22.0.0"` for core 10.1.1.
- :29-31 Stryker.NET license cited; quotes "Stryker requires the dotnet 10 runtime or newer", "Your application does not need to target dotnet 10 or newer", "*unit test* project dir".
- :41 Fuzz Introspector language quote.

### F17. WARNING: common-mistakes.md entries lacked a one-line why
- skill-draft Step 3: "Each pair: the wrong code, the right code, and a one-line *why*." All seven entries were Wrong / Use instead with the reason folded in.
- Fix: each entry now has **Wrong:**, **Use instead:**, **Why:** (cited, with quotes); URLs pinned. Order WRONG-first kept.

### F18. INFO: Stryker's own docs state the mistake common-mistakes.md:15-19 warns against
- Source (mutant-states-and-metrics.md @a4f8163): Survived "You're missing a test for it."
- Fix: one sentence in that entry's Why marking it as the tool's default reading, not a diagnosis.

### Audit checks 1-6 (no further changes)
- Frontmatter: name matches directory, description is third person with a when-clause (quick_validate passes). Description matches body.
- Lengths after edits: SKILL.md 42, common-mistakes.md 57, control-design.md 45, runtime-integrations.md 41, sources.yaml 102 lines. No reference over 100 lines of prose needing a TOC.
- No filler phrases found; local links all resolve.

### Counts
ERROR 5 (F11, F12, F15, F16, F19), WARNING 8 (F1, F2, F4, F6, F7, F8, F13, F17), INFO 6 (F3, F5, F9, F10, F14, F18). Claims cut: 0 (the misattributed state-propagation claims were relabelled as the skill's convention rather than deleted).

### F19. ERROR: moving URLs (all files)
- Every docs link (pitest.org, stryker-mutator.io, google.github.io/oss-fuzz) is an unversioned page rebuilt from a default branch; `github.com/hcoles/pitest` was the repo root. skill-draft Step 5: "never `/latest`, `/stable`, or other moving aliases".
- Fix: all repointed to SHA-pinned raw GitHub sources read at that SHA (below). DOI link kept: it is a persistent identifier (resolves 302 to dl.acm.org/doi/10.1145/2635868.2635929).

## Pinned URLs

| Old | New (pinned, fetched at this SHA 2026-11-07) |
|---|---|
| https://google.github.io/oss-fuzz/advanced-topics/ideal-integration/ | https://raw.githubusercontent.com/google/oss-fuzz/156f862e5976b3d23828230a0a5b4fef54074d32/docs/advanced-topics/ideal_integration.md |
| https://google.github.io/oss-fuzz/advanced-topics/fuzz-introspector/ | https://raw.githubusercontent.com/google/oss-fuzz/156f862e5976b3d23828230a0a5b4fef54074d32/docs/advanced-topics/fuzz_introspector.md |
| https://pitest.org/quickstart/basic_concepts/ | https://raw.githubusercontent.com/hcoles/pitest-site/614bec6fd16670852e94c8cc03a002f6bf05db09/quickstart/basic_concepts.markdown |
| https://pitest.org/quickstart/maven/ (and #dry-run-mode) | https://raw.githubusercontent.com/hcoles/pitest-site/614bec6fd16670852e94c8cc03a002f6bf05db09/quickstart/maven.markdown (anchor kept) |
| https://github.com/hcoles/pitest | https://raw.githubusercontent.com/hcoles/pitest/1edd5b4e14fbe3a7169d79bc179ac2f4cc5e417c/LICENSE.txt |
| https://stryker-mutator.io/docs/mutation-testing-elements/mutant-states-and-metrics/ | https://raw.githubusercontent.com/stryker-mutator/mutation-testing-elements/a4f816358a06701b7680d54bbb56180c19781c25/docs/mutant-states-and-metrics.md |
| https://stryker-mutator.io/docs/stryker-js/getting-started/ | https://raw.githubusercontent.com/stryker-mutator/stryker-js/8f24ef0be3a2119fc44ac48bfce58930ab2c9032/docs/getting-started.md |
| https://stryker-mutator.io/docs/stryker-js/configuration/ | https://raw.githubusercontent.com/stryker-mutator/stryker-js/8f24ef0be3a2119fc44ac48bfce58930ab2c9032/docs/configuration.md |
| https://stryker-mutator.io/docs/stryker-net/getting-started/ | https://raw.githubusercontent.com/stryker-mutator/stryker-net/2ec2d68614600d191de828675a10f1d91048a7be/docs/getting-started.md |
| (new) | https://raw.githubusercontent.com/stryker-mutator/stryker-js/8f24ef0be3a2119fc44ac48bfce58930ab2c9032/packages/core/package.json |
| (new) | https://raw.githubusercontent.com/stryker-mutator/stryker-js/8f24ef0be3a2119fc44ac48bfce58930ab2c9032/LICENSE |
| (new) | https://raw.githubusercontent.com/stryker-mutator/stryker-net/2ec2d68614600d191de828675a10f1d91048a7be/LICENSE |

SHAs resolved with `gh api repos/<org>/<repo>/commits/<default-branch> --jq .sha` (oss-fuzz master, pitest master, pitest-site gh-pages, stryker-js master, stryker-net master, mutation-testing-elements master). 9 URLs pinned, 3 new pinned sources added.

## Validation

```
$ python C:/Users/Q/.codex/skills/.system/skill-creator/scripts/quick_validate.py plugins/bugfinding/skills/harness-sensitivity
Skill is valid!

$ git diff --check -- plugins/bugfinding/skills/harness-sensitivity
diffcheck exit 0

cited-vs-sources.yaml check (fragments ignored):
== cited not in yaml
== yaml not cited
== moving            (grep /(main|master|HEAD|latest|stable)/ : no hits)
== local links
](references/runtime-integrations.md)
](references/control-design.md)
](references/common-mistakes.md)
](control-design.md)      (from references/, resolves)

sources.yaml: yaml.safe_load OK, 13 entries, every entry has exactly name/url/type/accessed/sections_used.

HTTP check (curl -L): all 12 raw.githubusercontent.com URLs 200. DOI: local curl exit 43; WebFetch shows 302 to https://dl.acm.org/doi/10.1145/2635868.2635929.

Trailing bytes: every file ends with a single "\n".
```

## Unverified

- Paper section numbers and quotes were checked by viewing the existing paper-reader page images (`C:/Users/Q/code/bugfinding-literature/harness-sensitivity/papers/Just_2014_MutantsRealFaults/pngs/`) directly this session, not by a fresh paper-reader skill run. Pages viewed: p.2, p.3, p.5, p.7, p.8, p.10. §2.3's quote renders V₁ as "V1".
- ACM landing page content behind the DOI was not fetched (redirect only); title/authors rest on the paper-reader's p.1 check.
- The rendered docs pages were not compared byte-for-byte with the raw sources; the skill now cites the raw sources only.
- No tool command in runtime-integrations.md was executed (unchanged from the draft).
