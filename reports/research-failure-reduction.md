# Research: failure-reduction

Date: 2026-11-07

## State

Per-skill research in progress. This report is the only owned repository output. Literature uses paper-reader only and direct page images; no paper-process workflow, target mutation, installation, commit or publication.

## Evidence ledger

Primary reduction tools, interestingness semantics, relevant paper images and replay limitations are being checked. No draft or empirical discovery claim.

## Literature evidence: C-Reduce (paper-reader)

Regehr, Chen, Cuoq, Eide, Ellison and Yang (PLDI 2012), *Test-Case Reduction for C Compiler Bugs*. Author-hosted PDF: https://www.cs.utah.edu/~regehr/papers/pldi12-preprint.pdf . Retrieved exact PDF (288,825 bytes, checked from filesystem), rendered with installed paper-reader render_pages.py, verified title/authors from page 1, and directly read all eleven images page-000 through page-010 on 2026-11-07. No extracted paper text or paper-process used. Local artifact owner: C:/Users/Q/code/bugfinding-literature/failure-reduction/papers/Regehr_2012_TestCaseReduction/.

- **Validity is independent of the failure predicate** (pp. 2-5,10). A reduced program can retain a compiler disagreement solely because a removed initialization introduced undefined behavior. The acceptable valid-input contract depends on the actual defect: compiler-crash cases can admit inputs a wrong-code equality experiment must reject. Do not demand invalid behavior avoidance when invalid-input robustness is itself the target; state the domain explicitly.
- **Reduction is not absolute minimization** (p. 3). The paper distinguishes a heuristic smaller failure-inducing input from the globally smallest one. A local stopping point or finite budget cannot support a claim of absolute minimum.
- **Transformation choice changes achievable reductions** (pp. 3-6). Contiguous deletion can get stuck; tree operations and coordinated noncontiguous changes (e.g. remove a parameter and all arguments) preserve useful structure. Intermediate size-increasing changes can enable later simplification. Reuse the producer's representation/formatter rather than invent a second parser.
- **A useful objective can include human comprehension** (p. 4). Whitespace deletion makes bytes smaller without helping diagnosis. The paper's framework separates search, transformations, validity and fitness. Plugin design can preserve world/program/schedule structure and choose a useful size/readability metric instead of assuming bytes are universally correct.
- **Generated choices are reducible material** (p. 5). Seq-Reduce modifies Csmith's decision sequence; regeneration preserves Csmith's valid-program constraints but early choices can perturb later generation. This motivates replaying the produced artifact and its witness after every accepted choice reduction, not trusting smaller seeds alone.
- **The original bug can be lost during reduction** (p. 10). The paper uses a specific compiler-crash string where practical, but notes wrong-code bugs have no universally obvious fingerprint. A symptom/witness guard supports continuity without proving identical cause. Preserve the original and treat changed/uncertain cause as unresolved or another candidate.
- **Nondeterminism and resource failures complicate interestingness** (p. 10). The historical evaluation assumes deterministic detection; memory-layout variation and time/memory exhaustion can break that assumption. The paper's historical decision to disable ASLR is NOT a recommended setup action for this skill. Improve controlled replay using existing seams, retain trials/limits and keep uncertain observations.
- Historical corpus: 98 Csmith inputs (57 compiler crashes, 41 wrong-code cases), x86-64 Linux; historical mean wrong-code C-Reduce+Frama-C result 258 bytes/12 minutes and median 192 bytes/7 minutes (pp. 7-9). These are study facts, not a forecast or tool-selection guarantee for Barn. No yield comparison is made here.

Decision consequence: the reduction target is a bundle and a precise interestingness predicate with validity/replay/witness preconditions; shrinking only source bytes can delete the world, schedule or recovery event that establishes the real violation.

## Primary tool evidence and conditional operations

All accessed 2026-11-07. These are source-read examples, not commands executed against a target.

### S1 — C-Reduce current repository and executable contract

- Sources: https://github.com/csmith-project/creduce ; https://raw.githubusercontent.com/csmith-project/creduce/master/creduce/creduce.in (options/help lines 72-179; delta_test lines 274-298); https://raw.githubusercontent.com/csmith-project/creduce/master/INSTALL.md ; https://raw.githubusercontent.com/csmith-project/creduce/master/COPYING .
- Quote fragment from help: “returns 0”. The test accepts a candidate on zero; nonzero is not interesting. It receives no arguments and runs in a fresh temporary directory with reducible file basenames. Refer to non-reduced fixtures/tools by resolved paths. `--timeout` limits an individual test; `--n` controls cores; `--not-c` omits C/C++-specific passes. The tool supports multiple reducible files. A generic text mode is not proof that a particular protocol/world/schedule encoding will remain valid.
- Conditional invocation after a compatible existing installation and a tested interestingness program: `creduce --n 1 --timeout 60 /absolute/interesting.sh case.c`. Values are illustrative resource choices, not universal thresholds. Preserve original evidence before invoking a reducer that rewrites working files. Per-test timeout is not a whole-campaign budget. On a changed property, reject/retain separately rather than return zero because something failed.
- The install document names package-manager paths for Linux/FreeBSD/macOS and LLVM 9-era source prerequisites; it is not current evidence of a modern compatibility matrix. Use actual selected package/release requirements and `creduce --help`/`--version` before execution. No Windows support claim from a few MSWin32 branches. License: University of Illinois Open Source License in COPYING. No install was performed.
- Decision relevance: adapt the actual reducer/test calling convention instead of assuming every tool takes the input path as an argument. Reuse a chosen compatible tool; do not ship a new general reducer framework merely to wrap it.

### S2 — llvm-reduce for IR/MIR, not arbitrary source

- Source: https://llvm.org/docs/CommandGuide/llvm-reduce.html ; read Description, Generic Options, Exit Status and Example. License source: https://raw.githubusercontent.com/llvm/llvm-project/main/LICENSE.TXT (Apache-2.0 with LLVM exceptions).
- Quote fragment: “invalid IR”. The format is IR or MIR. The documentation shows `llvm-reduce --test=script.sh test.ll`, whose test receives the candidate path as `$1`. Options include `--abort-on-invalid-reduction`, ordered pass selection, `-j`, and `--max-pass-iterations`. `--in-place` overwrites the input; do not select it for the only retained evidence. A flag that skips repeated interestingness verification also removes a flaky-reproducer warning.
- Conditional example: `llvm-reduce --test=/absolute/interesting.sh --max-pass-iterations=5 -j 1 case.ll`, with limits chosen from actual budget and installed help. This is an LLVM artifact recipe, not a Go source reducer. Source-build/installed LLVM version must match relevant IR/MIR syntax and target assumptions; host package installation was not investigated or performed.
- Decision relevance: use a producer's native representation and its maintained reducer where available; validate the candidate with the actual failure-producing toolchain. Reducer normal exit alone is not final replay evidence.

### S3 — libFuzzer distinguishes three reduction goals

- Source: https://llvm.org/docs/LibFuzzer.html ; read Running and Options (`-merge`, `-minimize_crash`, `-reduce_inputs`, `-runs`, `-max_total_time`, artifact paths).
- Quote fragment: “minimizes the provided crash input”. `-merge=1` minimizes retained coverage corpus material; `-reduce_inputs` preserves observed feature sets; `-minimize_crash=1` shrinks a supplied failing file. These predicates are not interchangeable.
- Existing compatible target example: `./fuzz_target -minimize_crash=1 -max_total_time=300 -exact_artifact_path=reduced-case original-case`. Keep paths distinct, source/instrumentation/options/architecture unchanged, and replay the final artifact with the original semantic predicate. Multiple processes must not share one exact artifact path. Limits are illustrative. Native crash reduction is not proof of unchanged cause or of preservation of a richer world/history oracle.
- Toolchain/platform/instrumentation setup belongs to coverage-guided-fuzzing/native instrumentation; this report does not turn this command into a generic managed-language backend. LLVM license as S2.

### S4 — Hypothesis replay, explicit examples and flakiness

- Sources: https://hypothesis.readthedocs.io/en/latest/tutorial/replaying-failures.html (database, explicit examples, reproduce_failure); https://hypothesis.readthedocs.io/en/latest/tutorial/flaky.html (requirements, sources, FlakyFailure); https://hypothesis.readthedocs.io/en/latest/reference/api.html (FlakyFailure/FlakyStrategyDefinition); license https://raw.githubusercontent.com/HypothesisWorks/hypothesis/master/LICENSE.txt (MPL-2.0 except noted contributions).
- Quote fragment: “do not shrink”. An `@example` is a stable explicit replay, not a request to minimize it. Saved database keys and opaque reproduction blobs can become invalid after test/version changes; preserve actual readable values and compatible version information, then retain a proper regression rather than only an opaque blob.
- Hypothesis requires deterministic generated draws and visible pass/fail outcome, not necessarily every hidden implementation event. Uncontrolled randomness, external/global state, filesystem/database residue and scheduling can change those outcomes. A failed or distinct replay yields flaky evidence, not a successful reduced reproducer.
- Decision relevance: use the existing generator/shrinker while it preserves legal dependent structure, and make missing state/choices visible to it. Do not invent an unsupported standalone `find` shrink recipe from older memory; the current API page did not expose that name in this read. Exact supported Python/package versions must be checked at execution; no install/runtime promise or new dependency here.

### S5 — Go's saved corpus and minimization limits

- Source: https://go.dev/doc/security/fuzz/ ; read Failing input, Custom settings, Corpus file format. Quote fragment: “each minimization attempt”. `-fuzzminimizetime` is an attempt limit, not a whole-campaign budget. A saved failure has typed ordered arguments; a `[]byte` choice stream and rendered source `string` are different replay inputs. Use the emitted `go test -run=FuzzName/CASE_ID` within the authorized runner; no campaign was executed.
- Decision relevance: native minimization and saved regressions already exist in Barn and installed Go guidance. The new skill adds semantic/witness continuity and multi-artifact reduction, not another basic Go fuzz tutorial. Preserve initial worlds/schedules/outputs missing from a single encoded input if they matter to the selected property.

### S6 — Delta debugging's minimality and unresolved outcomes

- Source: https://www.debuggingbook.org/html/DeltaDebugger.html ; read ddmin, generic_test, minimality discussion and code-reduction failure example. Quote fragment: “1-minimal”. Its `test` interface distinguishes PASS, FAIL, UNRESOLVED; an unexpected exception is not automatically the selected failure. A deletion-fixed-point guarantee is relative to moves and predicate, not a global smallest input. Its code-reduction example can delete meaningful functionality while still triggering an overly broad assertion.
- Decision relevance: state the actual granularity/transforms and completion/budget status. Keep invalid/setup/unknown results distinct even if a two-valued reducer maps all of them to not-interesting. No copying this implementation into the plugin or claiming exception type equality proves common cause. This is author-maintained executable documentation, not an independently read paper.

## Concrete reduction workflow for the drafter

The following is proposed plugin behavior inferred from the primary evidence. It is not a new mandatory schema, a universal mathematical guarantee, or a measured optimal schedule.

### Select the retained violation before the reducer

Identify the real producer, exact original artifacts, enabled configuration, legal input/state domain, required observation and failure relation. Capture original witness, invocation/build/runtime/instrumentation, raw outputs and actual replay attempts. Decide what identity can be observed: violation class plus semantic witness/objects/dependency edges or expected/actual effect, not merely any nonzero exit. Exact object names may legitimately change during shrinking; compare witness meaning with a recorded identity mapping. If cause is unknown, claim witness continuity only, not proved root-cause equality. Sources: paper pp. 2-6,10; S1/S4/S6.

Exercise the selected interestingness program on the original, a healthy/irrelevant candidate, and an invalid/setup candidate using the reducer's actual invocation/current-directory convention. Reuse existing controls; route substantive sensitivity design to harness-sensitivity. A predicate that accepts the empty input because its own setup throws is broken. Reject new faults separately without erasing their evidence. Sources: S1 source sanity_check and test contract; S6 wrong exception semantics.

### Choose the correct representation and moves

Prefer the current generator's shrinker, representation or native reducer when applicable. Delete coarse units before fine simplification if that reduces useful cost; revisit passes because one simplification can expose another. Preserve the domain's dependencies or regenerate them through the existing producer, rather than add another parser/model. A local minimum can justify another meaningful transformation, not a claim that further compute guarantees a smaller case. Sources: paper pp. 3-6; S2/S4/S6.

| Reduction unit | Validity and witness to retain | Meaningful move examples |
|---|---|---|
| Raw bytes/typed primitive corpus | Actual decoder/types and selected violation, not a different parser/setup error | Chunk deletion, value/boundary simplification through native shrinker |
| Program plus generated world | Variables/object identities/types/permissions required to reach selected operation; same forbidden effect | Remove unused declarations/entities and matching uses, simplify values, regenerate valid state |
| API operation sequence | Lifetime/identity and prerequisites; actual result/effect relation | Delete operation blocks with dependent uses, simplify arguments using existing model |
| Concurrent workload plus schedule | Executable decisions on remaining operations; same safety/progress witness and model | Remove irrelevant operations and matching decisions, then replay the controller's real trace format |
| Recovery workload plus faults | Acknowledged operation, actual failure-model boundary and recovered-state violation | Remove irrelevant operations/faults, preserve event identity rather than assume syscall ordinal remains stable |
| Numerical/resource input family | Original domain and tolerance/growth/progress contract, matched observations | Simplify parameters while preserving conditioning/regime or repeated size-family evidence |

Rows beyond the C/LLVM/native shrinker examples are **design adaptations**, not claims that a verified generic tool currently reduces arbitrary worlds, schedules or fault traces. The selected runtime's maintained replay/shrink APIs must establish those moves. Detailed generation, schedule/fault encoding and specialized oracle validity stay with their owning skills.

### Handle nondeterministic and costly interestingness honestly

First look for missing controlled state, prior sequence, scheduler/fault trace, randomness, version, timing/resource limit or observer change. A random seed alone does not recreate uncontrolled scheduling. Use an existing replay seam where available. Retain trial results, not just a final success flag; a one-time smaller symptom is not a reliable substitute for the original. Sources: paper p. 10; S4.

Deterministic caching and greedy acceptance cannot automatically be trusted for flaky outcomes. Repeated/matched observations can inform a qualified candidate decision but need a target-specific acceptance rule and budget; no universal retry count or confidence threshold is supported here. If the missing behavior cannot be controlled or resolved, preserve the original and smallest actually reproduced artifacts plus uncertainty instead of forcing a completed-looking reduction. No proposal to disable ASLR, relax a check, mask exceptions or install a global scheduler follows from the historical paper.

Account reduction cost separately from discovery: attempts, total elapsed/CPU, property evaluations, invalid/unresolved/timeouts and useful improvements. Per-test guards protect an attempt; an outer authorized resource envelope bounds the job. Stop when required handoff usefulness is reached, transformations stop improving under their actual scope, or budget/observability is exhausted. Preserve any partial best case and why it stopped. Sources: S1-S3 operational limits; paper pp. 3,7,10. Allocation policy is plugin design rather than a proven optimum.

### Final replay and handoff

Re-run original and reduced artifacts with the same selected contract/configuration and actual toolchain. Record exactly what reproduced and what changed. Preserve original even if minimized case is sufficient for a finite regression. A smaller output with another witness remains separate evidence until its connection is established. Route attribution/deduplication/LLM explanation to evidence-based-triage, not this reducer. Sources: paper p. 10; S4/S5/S6.

Report reduction goal, original/reduced paths and sizes under the chosen metric, transformation domain, actual invocation/resource limits, witness/replay results, invalid/unresolved attempts and scope of minimality. Do not state global minimum, fixed cause, completed exhaustive search or fixed product behavior from reducer success alone.

## Advanced worked examples

All are proposed evaluation scenarios, not executed target findings.

1. **Wrong world effect hidden by return equality.** A program returns the same value on two engines but one permitted mutation differs. Reducing only the source removes the world setup and causes both sides to reject an object reference. The correct predicate requires the selected operation to execute under equivalent worlds and preserve the forbidden effect difference; shrink unused entities/operations together. If witness IDs change, retain semantic identity mapping rather than requiring irrelevant raw names. This advances beyond existing value-only or byte-only reduction without asserting Barn has this defect.
2. **Schedule reduction switches to a setup panic.** Removing object creation and a scheduling decision produces a smaller null/reference error. A broad any-failure predicate accepts it; the retained-history/effect predicate must not. Revalidate schedule feasibility through the real controller, keep invalid and alternate-failure evidence separate. No generic Go schedule reducer is promised.
3. **Fault ordinal changes after workload shrink.** A disk-failure test injects at the nth write. Removing earlier work shifts that ordinal before the acknowledged operation under investigation. The smaller case no longer checks the same durable promise. Use actual recorded failure-event identity/acknowledgment and recovery oracle if the target seam supports it, or mark reduction unresolved; do not fabricate equivalence from the ordinal.
4. **Resource failure vanishes when only one point is shrunk.** A scaling anomaly is evidenced by matched input sizes and repeated resource observations. The reduction must preserve the declared growth/resource predicate, not just a single timeout. Lowering host memory or timeout to preserve failure changes the experiment rather than reduces the original evidence.

## Existing overlap and boundaries

Read installed golang/go-testing-advanced SKILL.md's native minimization/corpus section (around line 57). It already explains minimized failure persistence and finite replay. The Barn source inventory in domain research already includes valid-IR choices, string-source Toast replay, snapshot mutation and rich histories. This report did not freshly re-audit Barn or claim missing reducers across all worktrees. New value is selecting a precise continuity/validity predicate and reducing the dependent bundle, with runtime-specific calling conventions and explicit unknowns.

No external marketplace novelty claim, new generic reduction library, code duplication, mandatory storage service or tool installer is justified. Source-native commands remain conditional and authorized target edits/runs stay under their actual task scope. No target program, reducer, test or campaign was executed here.

## Drafter handoff

Suggested substantive references: interestingness-and-replay.md (outcome/continuity/flakiness and unit table), tool-recipes.md (selected C-Reduce/LLVM/libFuzzer/Go/Hypothesis conventions), worked-bundle-reduction.md (advanced examples). Required common-mistakes.md and sources.yaml should link actual primary URLs, not this report as technical authority. Avoid exhaustive manuals and repeated generic triage rules. Keep method selection in the entrypoint; runtime details load conditionally.

Blind evaluation: provide original/reduced raw artifacts, the actual target contract and a reducer predicate containing an unrelated-setup pass path; include one valid same-witness reduction, one changed-witness reduction, one missing state/schedule case and a budget-limited partial reduction. Ask the evaluator to use the skill to preserve evidence and obtain a trustworthy smaller counterexample. Do not reveal expected labels/cause. Evaluate actual replay artifacts and qualified claims, not whether headings match. This research ran no such evaluation and establishes no empirical bug yield.

## Paper artifacts and scope limits

Paper-reader local artifact set: paper.pdf, all eleven pngs, notes.md, metadata.json, description.md, short-excerpt/paraphrased abstract.md, 18-entry citations.md, task-local index, reader ledger and helper-generated keymap. Full authored abstract transcription omitted for quotation limits. Parent explicitly excluded nested reconciliation workflows; therefore the reader's nested reconcile step was not invoked and no full reconciliation-completion claim is made. No other paper exists in this new task collection. No paper-process, tagging, propstore or additional agents.

Initial web requests for Utah paper/website timed out; direct PDF download succeeded after a first curl output attempt found the destination directory absent. No partial PDF from that failed write was treated as valid; successful canonical PDF length and all helper-rendered pages were checked. C-Reduce source/install docs are dated mutable snapshots and include historical assumptions. A guessed Hypothesis find API was not used. Referenced developer researcher role file did not exist; explicit parent constraints governed the work.

## Completion

Per-skill research is ready for drafting with the reader nested-workflow limit above explicit. Only this report changed in the plugin repository; local paper-reader artifacts are outside it. No SKILL.md, target action, installation, commit, host registration, remote mutation or publication.
