# Research: evidence-based-triage

Date: 2026-11-07

## State

Per-skill research complete for drafting. This report is the only owned output. No skill draft, target execution, installation, commit or publication was performed. The developer-referenced researcher role file was absent at its specified path; explicit task constraints govern this bounded research.

## Evidence ledger

Primary triage/reproduction documentation, actual analyzer code and relevant literature have been inspected in the bounded scope below. Candidate failures, confirmed product defects, harness faults, intended differences and unresolved evidence remain distinct.

### Literature reused through direct page images

Kingsbury and Alvaro (2020), *Elle: Inferring Isolation Anomalies from Experimental Observations*, https://arxiv.org/abs/2003.10554. Existing completed paper-process --light collection: `C:/Users/Q/code/papers/Kingsbury_2020_ElleInferringIsolationAnomalies/`. This researcher directly viewed images for printed pp. 7, 8, 9 and 12 on 2026-11-07; no paper text extraction or new ingestion was used and no collection artifact changed.

- **Sections 4.3 and 4.3.2, pp. 7-8:** sound inference depends on recoverability/traceability and the set of compatible interpretations. Observations often leave transaction outcomes indeterminate. **Decision changed:** preserve uncertainty as an evidence state; absence of an inferred violation does not justify a stronger guarantee than the checker model.
- **Section 6, p. 9:** a dependency-cycle witness can be translated into a readable contradiction. Quote fragment: “human-readable explanation”. **Decision changed:** keep the machine witness and build the prose finding from it; an LLM story without the witness is not equivalent evidence.
- **Section 9, p. 12:** predicates and distinctions among isolation levels remain limited in this paper. **Decision changed:** a negative checker result cannot dispose of a report outside that checker’s observation/model coverage. No historical performance or detection-rate claim is transferred to this skill.

### S1: ClusterFuzz triaging new crashes

- URL: https://google.github.io/clusterfuzz/using-clusterfuzz/workflows/triaging-new-crashes/
- Accessed: 2026-11-07. Sections read: Filtering testcases; Regression revision range; Crash stacktrace; Crash statistics.
- Quote fragment: “Reliability of reproducing the crash”.
- Supported guidance: triage records include crash type/state, fuzzer/job, reproduction reliability and platform; a useful regression range requires reproducible cases. Sanitizer stacks help investigate but do not dictate one exact cause-finding process.
- Decision relevance: preserve these facts before LLM compression, qualify intermittent findings, and use build/revision evidence where available. Do not treat a failed replay or stack-only guess as a root-cause verdict. Access-limited reports need their existing authorization, not public redistribution.

### S2: OSS-Fuzz reproducing

- URL: https://google.github.io/oss-fuzz/advanced-topics/reproducing/
- Accessed: 2026-11-07. Sections read: Fuzz target bugs; Building using Docker; Reproducing bugs; local source checkout; build failures.
- Quote fragment: “appropriate sanitizer”.
- Supported guidance: retain actual testcase bytes and match build/instrumentation/architecture; resource-failure reproduction can require matching limits. An existing OSS-Fuzz checkout/integration documents `python3 infra/helper.py reproduce PROJECT FUZZ_TARGET TESTCASE`; a compatible target binary can replay its testcase directly.
- Decision relevance: preserve both original input and execution identity. These are conditional examples, not generic commands for arbitrary Go or managed targets. This skill should route setup to the selected runtime owner, not install Docker or OSS-Fuzz. The page’s post-fix submission steps are not publication authority.

### S3: ClusterFuzz glossary

- URL: https://google.github.io/clusterfuzz/reference/glossary/
- Accessed: 2026-11-07. Sections read: Crash state, Minimization, Reliability of reproduction, Testcase.
- Quote fragment: “signature”.
- Supported guidance: crash state is generated from the stack for deduplication; minimization aims to preserve the underlying bug, and reliable reproduction means consistent crash state for the input.
- Decision relevance: separate a useful symptom bucket from a verified common cause. Keep per-case evidence when grouping, and do not count all members as independently confirmed defects or erase a member because another symptom matches.

### S4: OSS-Fuzz-Gen README and license

- URL: https://github.com/google/oss-fuzz-gen
- Accessed: 2026-11-07. Sections read: framework overview, metrics, independent agent execution. License shown: Apache-2.0.
- Quote fragment: “Runtime coverage”.
- Supported guidance: the project generates/evaluates fuzz targets for C/C++/Java/Python and separately evaluates compilation, runtime failures, coverage and coverage delta. Its historical success counts are not used here.
- Decision relevance: executable validation and harness quality are separate from LLM text. This is primary evidence of an existing implementation worth learning from, not a mandatory service dependency or a demonstrated triage accuracy guarantee.

### S5: OSS-Fuzz-Gen crash analyzer implementation

- URL: https://raw.githubusercontent.com/google/oss-fuzz-gen/main/agent/crash_analyzer.py
- Accessed: 2026-11-07. Actual source read: `_initial_prompt`, `_container_handle_conclusion`, `_container_tool_reaction` and tool-result formatting (visible lines 47-144).
- Quote fragment: `true_bug`.
- Observed producer: `_initial_prompt` supplies generated fuzz source, runtime error and crash function. `_container_handle_conclusion` maps the model’s conclusion tag to a boolean. Tool-reaction code insists on debugger use and rejects apparent fabricated tool output before accepting a conclusion.
- Decision relevance: preserve actual tool results/provenance with the conclusion; debugger use alone is not evidence the conclusion follows. A boolean produced by parsing an LLM response is a candidate classifier result, not independent product-bug confirmation. This is source behavior, not an accusation that every stored verdict is wrong. Main-branch source is version-sensitive.

### S6: OSS-Fuzz-Gen semantic analyzer implementation

- URL: https://raw.githubusercontent.com/google/oss-fuzz-gen/main/agent/semantic_analyzer.py
- Accessed: 2026-11-07. Actual source read: parser constants and `_parse_libfuzzer_logs` through early-crash classification (visible lines 24-146).
- Quote fragment: `EARLY_FUZZING_ROUND_THRESHOLD`.
- Observed behavior: heuristic classifications cover null dereference, signals, controlled exit, constant-input overwrite, resource symptoms and near-initialization failure; artifact-name matching excludes certain slow/timeout/leak/OOM cases from the ordinary crash route.
- Decision relevance: understand a classifier’s scope before using its output. These are implementation heuristics for generated harness evaluation; they do not establish that every early crash, null dereference or resource failure is a harness defect. Preserve raw input/output and investigate real API preconditions and resource contracts instead of inheriting blanket dismissal rules.

### S7: OSS-Fuzz-Gen execution stage implementation

- URL: https://raw.githubusercontent.com/google/oss-fuzz-gen/main/stage/execution_stage.py
- Accessed: 2026-11-07. Actual source read: execute (visible lines 53-146).
- Quote fragment: `build_and_run`.
- Observed behavior: a generated driver/build-script pair is materialized and evaluated; result handling requires runtime coverage data and compares with existing coverage.
- Decision relevance: compiling a proposed harness, observing its executed paths and judging its failures are separate evidence. The skill may request LLM suggestions, but never upgrade a generated snippet to a working reproducer without actual execution evidence. No setup command is proposed for this project because the skill does not need to install it.

### S8: Go fuzzing failure/replay contract

- URL: https://go.dev/doc/security/fuzz/
- Accessed: 2026-11-07. Sections read: Suggestions; Failing input; Corpus file format.
- Quote fragment: “intended behavior”.
- Supported guidance: failures can arise in the target or its test, from nonrecoverable exits, or from long execution that may be legal. Saved corpus arguments have exact types/ordering; Go emits a focused replay selector such as `go test -run=FuzzFoo/CASE_ID`.
- Decision relevance: an engine failure classification is evidence to investigate, not automatic product fault attribution. Retain the actual corpus encoding and emitted replay command; a mismatched decoder or unsupported conversion is a harness issue until shown otherwise. Use the target’s permitted runner/environment; no local campaign was executed here.

### S9: libFuzzer execution and artifact boundaries

- URL: https://llvm.org/docs/LibFuzzer.html
- Accessed: 2026-11-07. Sections read: Fuzz target; Running; Options; FAQ on in-process limitations.
- Quote fragment: “global state”.
- Supported guidance: file arguments replay without mutation search, resource limits produce failure cases, and in-process state not reset between inputs can contaminate later executions. Persistent threads and delayed corruption can make the last saved input insufficient by itself.
- Decision relevance: record whether replay was in a fresh process, with the same initialization and required prior sequence. Failure to replay one saved file is a clue to missing state or another difference, not evidence that the original event was imaginary. Native binary/Clang requirements remain the runner skill’s concern. No libFuzzer installation or target execution occurred here.

### S10: LLVM maintainer report requirements

- URL: https://llvm.org/docs/HowToSubmitABug.html
- Accessed: 2026-11-07. Sections read: Introduction, AI policy, front-end bugs and miscompilations.
- Quote fragment: “All information necessary to reproduce”.
- Supported guidance: maintainers need a reduced reproducer, exact invocation and compiler provenance; miscompilation candidates require checking whether the input program itself violates its language contract. Current LLVM-specific policy also asks authors to understand AI-assisted reports and identify generated-testcase frameworks.
- Decision relevance: draft an understandable artifact-backed finding, rather than forwarding an LLM theory. Cite the actual violated target contract and distinguish target behavior from invalid harness/input behavior. Publication policy is target-specific and must be checked only when publishing is separately authorized; this skill does not post reports. LLVM’s specific reporting rules should not become a universal workflow for unrelated projects.

## Existing ownership and non-novel content

Installed protocols/investigation SKILL.md was read directly. It already distinguishes facts from theories, competing hypotheses, and discriminating tests. Do not copy that general debugging protocol into this skill or make it a dependency. The new owner is the transition from computational candidates to maintained evidence: exact producer/configuration/witness, classifier provenance, replay status, duplicate grouping without evidence loss, explicit disposition, and user-visible impact. Barn’s already existing explicit true/false/unknown history checks remain baseline according to the source inventory; this research did not freshly audit Barn or claim an absence there.

## Decision guidance for the drafter

The following are proposed skill decisions derived from the sources, not measured optimal triage policy. They do not impose a new database, mandatory review, fixed replay count or report schema.

### Keep disposition, reproduction and cause separate

A case can be a demonstrated product-contract violation whose exact cause is still unknown. It can also be a plausible candidate with one authentic trace but no successful replay. Avoid one confidence score that hides these differences. A useful compact ordinary-file record contains:

| Fact | What to preserve |
|---|---|
| Producer and observation | Exact original input, encoded arguments, generated source/world/operation/fault or schedule artifacts as applicable; raw output and observer/checker witness. |
| Execution identity | Source/build/configuration/runtime/instrumentation/architecture and invocation, environment and relevant limits; what was measured rather than presumed. |
| Claimed violation | Governing contract and preconditions, expected versus actual externally visible behavior; supported scope and checker/model limits. |
| Reproduction | Actual attempts and results, original versus reduced input, fresh-process versus prior-sequence execution, missing evidence or uncontrolled choices. No arbitrary success percentage threshold. |
| Disposition | Demonstrated product violation; harness/oracle/input defect; documented expected behavior; infrastructure cause supported by evidence; or unresolved. |
| Cause and grouping | Observed failure site; candidate mechanism; verified cause if established; provisional symptom bucket distinct from proven duplicates. |
| Next useful work | Small discriminating replay/source check, reduction preserving the witness, or a justified stop with retained evidence. |

S1-S3 and S8-S10 support the retained execution/reproduction details; Elle supports model/witness limits. The choice of separate fields is the plugin’s design. Reuse existing project artifacts rather than force this exact table.

### Use LLM effort on falsifiable work

Give the LLM the actual target producer, raw evidence and relevant contract/source sections. Ask it to state the narrowest supported observation, plausible competing explanations and the cheapest permitted next test that separates them. Verify its cited locations and tool results. Use it to draft readable witness explanations, prioritize missing evidence and organize provisional buckets; treat generated harnesses and classifier conclusions as proposals until their execution/contract evidence exists (S5-S7).

An explanation must remain weaker than its evidence. A sanitizer diagnosis can demonstrate an invalid access on a real path without establishing an exploit or complete root cause. A history witness can demonstrate one supported anomaly without proving every stronger consistency claim. A differential result can establish disagreement without selecting the incorrect implementation. A timeout can establish a configured deadline was exceeded without proving a deadlock. Route the deeper oracle interpretation to the relevant specialist (Elle, S8-S10).

### Preserve cases through grouping and reduction

Keep each candidate’s original artifacts when placing it in a stack/symptom group; use the group to amortize investigation, not to erase evidence. Mark duplicate causes only after evidence connects them. When reduction changes the symptom/witness, retain the original and treat the new smaller failure as another candidate until the causal connection is established. Detailed shrinking belongs to failure-reduction (S3).

If one-file replay fails, inspect mismatched build/configuration/instrumentation and missing initialization, prior inputs, state or concurrent events before deciding what the event means. Do not silently turn intermittent reproduction into a harness defect; do not silently count it as a unique confirmed product bug either. The real retained event remains open evidence (S1-S2, S9).

### Preserve a maintainer-usable finding

Use the project’s existing report format. Supply a short observable trigger, violated guarantee with source, expected/actual behavior, exact original/minimized reproducer paths and execution results, environment identity, scope and unknowns. Explain the user-visible effect supported by evidence, such as lost acknowledged work or a wrong result. Keep proposed mechanism and fix separate from demonstrated behavior. A maintainer should be able to reproduce or identify the exact missing material without rerunning the full campaign (S1-S2, S10; Elle pp. 9,12).

Do not require a fix before preserving a real finding. Do not invent source blame, severity, exploitability, user impact or a successful replay to make a report appear finished. Leave it unresolved when the required evidence is unavailable. Posting, fixing and retesting a target follow the current task’s authority; this research and triage skill do not authorize external communication.

## Worked evidence examples for references

These are explicitly illustrative inputs and decisions, not observed product findings or executed experiments.

1. **Generated native harness crashes immediately.** Input and sanitizer report are authentic, but the generated call uses a freed object contrary to the actual API lifetime requirement. The smallest discriminating check follows the documented valid lifetime through the real producer. If evidence establishes the invalid call came only from the harness, classify the demonstrated case as a harness defect and retain it. Do not infer that every immediate or null crash is invalid merely because S6 has that heuristic.
2. **Paired engines print different output.** The two configurations expose documented different semantics for the selected feature. Save both outputs and the contract difference; classify this comparison as expected/unsupported for an equality oracle. If configurations supposedly match but evidence is incomplete, leave the disagreement unresolved rather than choose a winner. The semantic-differential owner establishes the valid comparison contract.
3. **History checker emits a contradiction.** Save the exact history, outcomes, dependency witness and selected model. Explain the contradiction from the witness, with its assumptions. If one operation outcome is unknown and that interpretation determines the conclusion, retain that uncertainty rather than fabricating a committed/aborted outcome (Elle pp.7-9).
4. **Saved input fails only in the long-running worker.** Preserve original worker log, prior sequence if available, build/options and actual replay attempts. A fresh-process miss cannot distinguish state contamination in the harness from an accumulated product bug by itself. Investigate the missing sequence or controlled event; keep disposition unresolved until evidence separates them (S1, S9).
5. **Many identical top frames.** Keep provisional buckets and all member inputs. One minimized representative showing a cause does not establish that every member shares it; compare the remaining evidence before collapsing the confirmed defect count (S3). Do not send fifty unverified near-duplicate reports merely because fifty files exist.

## Suggested artifact-based behavior evaluation

Use an isolated evaluation with raw candidate inputs, exact build/configuration and contracts; the evaluator must not receive the intended diagnosis. Include a real historical product failure, invalid generated harness call, intentional cross-engine difference, intermittent trace and two similar stack signatures with distinct causes. Observe whether it retains the raw evidence, separates reproduction from disposition, verifies its claims and identifies missing material. Accept alternate evidence-backed investigation paths; do not score by matching invented labels or fixed wording. Measure lost/misclassified evidence and maintainer handoff usability before claiming LLM triage effectiveness. No such evaluation was executed in this research.

## Proposed reference depth and boundaries

- `triage-decisions.md`: state separation, conditional next investigations and when evidence is insufficient; examples above.
- `maintainer-handoff.md`: compact artifact-backed finding, raw versus reduced evidence, actual reproduction history and user-visible effect; project format wins over a fixed template.
- Required `common-mistakes.md`: boolean/stack/LLM confidence substituted for evidence; blanket early/resource-failure dismissal; reduction switching witness; dropping intermittent or grouped evidence; blaming one side of a disagreement without a contract.
- Required `sources.yaml`: S1-S10 plus Elle, with URLs, sections and access date. Do not cite this report or another skill as technical authority.

Keep the entrypoint short and decision-oriented. It can link correctness-oracles, semantic-differential-testing, transactional-history-testing, failure-reduction and the campaign owner for their independent concerns. Avoid cloning those algorithms or installed investigation guidance. No mandatory model vendor, hosted service, installation, executable helper or schema is needed for this skill.

## Verification limits and failed discovery URLs

- The referenced researcher role file is absent; no replacement role policy was invented.
- The guessed OSS-Fuzz bug-fixing guidance URL was inaccessible; a guessed raw documentation path returned 404. Neither supplies facts.
- An external syzkaller skill-directory fetch was restricted. No ecosystem novelty or exhaustive overlap claim is made.
- Main-branch analyzer source is a dated source snapshot, not a stable API or an endorsed ready integration. No model accuracy evaluation, target campaign, reproduced product defect or statistical triage-yield measurement was performed.
