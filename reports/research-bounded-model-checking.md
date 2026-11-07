# Research: bounded-model-checking

Date: 2026-11-07

## State

Per-skill research complete for drafting. This report is the only owned repository output; paper-reader artifacts are external. Literature uses paper-reader and page images only. No target execution, installation, target changes, commits or publication.

## Evidence ledger

Inspecting actual CBMC, JBMC and Kani target/build/model/bound contracts and relevant primary paper images. No copied target implementation or unverified Go backend is proposed.

## Literature image evidence

Clarke, Kroening and Lerda (TACAS2004), *A Tool for Checking ANSI-C Programs*, primary author PDF https://www.kroening.com/papers/tacas2004.pdf . Canonical PDF rendered through installed paper-reader into nine pages; title/authors verified visually and ALL images000-008 read directly (printed pp.168-176). No extracted paper text used. External collection: C:/Users/Q/code/bugfinding-literature/bounded-model-checking/papers/Clarke_2004_ToolCheckingANSI/.

- pp.168-170: the actual program and assertion are jointly unwound; solver query is constraints AND negated property. An unsatisfiable query establishes the modeled property only with adequate unwinding/model assumptions. Unwinding assertions check whether a loop/recursion can exceed the supplied bound. A failed bound assertion is not the same as a witnessed product assertion failure.
- pp.169-171: preprocessing, side-effect removal, loop/backward-goto unwinding, call/recursion expansion and SSA/bit-vector encoding preserve a particular executable language model; dynamic arrays need symbolic treatment rather than allocating every possible array element.
- pp.171-172: counterexample traces permit state inspection but the reported failure line need not contain the root cause. Concrete input/native replay and actual producer mapping remain necessary for an implementation claim.
- pp.173,176: historical tables specify a then-current subset and memory model, including fixed-point treatment of floats and unsupported fall-through switch. Do not carry those 2004 limits into current CBMC recipes or infer current IEEE/UB support from this paper alone.
- pp.174-175: figures show distinguishing insufficient unwinding from violated safety assertions and using project-specific entrypoints/options. Historical GUI/platform and performance claims are not current installation or yield evidence.

## Early current-source decisions

- Pinned CBMC source ref826c1c739051aa1c2dd8846282e12691db1cee35 (git ls-remote develop), man page doc/man/cbmc.1: current standard checks include unwinding and undefined-behavior checks, despite a stale5.59 header. --partial-loops explicitly admits paths continuing beyond a still-enabled loop and may yield spurious alarms; do not use it as a silent completeness repair.
- Pinned Kani ref94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca (git ls-remote main): verification-results.md distinguishes unreachable/vacuous success and undetermined checks. Its experimental JSON export warns a killed run can leave an earlier file apparently complete; run identity/time matters.
- Kani concrete playback generates panic/assertion tests, not all non-panic UB checks; same tool version/compile options are required. A missing native crash is not refutation of a verifier-only UB witness.

## Primary-source handoff

All sources accessed2026-11-07. Refs below were obtained by read-only git ls-remote and files fetched at the exact immutable ref. They identify research evidence, not a tested installed binary or a recommendation to use development builds in production. Commands are conditional source-read shapes, not executed tools. Failed guessed paths supply no facts.

### S1 — CBMC executable input, properties and bounds

Pinned base: https://raw.githubusercontent.com/diffblue/cbmc/826c1c739051aa1c2dd8846282e12691db1cee35/ . Sources: doc/man/cbmc.1 (standard checks, frontends, platform, BMC/backend/UI options); doc/cprover-manual/cbmc-unwinding.md (iteration/backjump counts, per-loop bounds, partial loops). Public overview https://www.cprover.org/cbmc/ was also read for supported product/download scope.

CBMC consumes supported C/C++ source or a linked GOTO binary from goto-cc, retaining the actual program rather than a copied implementation. Include paths/macros, entrypoint, language mode, architecture/OS and integer/pointer widths affect the model. Native host defaults are not automatically the embedded/cross-compiled target's semantics. Current source has C89/C99/C11/C17/C23 selections and limited listed C++ modes; do not infer every modern C++ feature from the product label.

Conditional existing fitting integration: `cbmc harness.c target.c --function harness --unwind 12 --unwinding-assertions --trace --json-ui`. Choose bounds from the real domain and budget, not this illustrative12; preserve full output and source/config. `--show-loops`/`--unwindset` select actual loop IDs. Backjump accounting can need an extra unwind beyond intuitive body count. A failed unwind assertion says the chosen bound is insufficient; it does not establish the target violates the separate safety property. Adequate unwind proves only the specified finite/model/input assumptions.

The manual header still says5.59 while its standard-check section describes6.0+ defaults. Actual src/cbmc/cbmc_parse_options.cpp was inspected for standard-analysis defaults and cover-mode override. Unwinding is enabled by standard checks, but coverage mode explicitly disables it and cannot be combined with explicit --unwinding-assertions. Run coverage as a distinct observation, not substitute its success for a safety proof. `--partial-loops` may introduce nonexistent paths; depth/complexity cutoffs change assurance. Do not remove checks or introduce unsound pruning merely to obtain green output. Quote fragment: “such paths may be spurious”.

### S2 — assumptions, harness state and vacuity

Pinned sources: doc/cprover-manual/modeling-assumptions.md and doc/cprover-manual/goto-harness.md under S1's base. Quote fragment: “pass vacuously”. An impossible assume empties later search; assumptions are not retroactive and one nondeterministic index does not universally constrain every array element. Diagnose admissibility/reach through the real contract and separate `--cover assume` observation; don't weaken the asserted guarantee to create a pass.

goto-harness can set up a call-function environment or load memory-snapshot state and havoc selected variables. Its actual quickstart compiles the real program with goto-cc, generates a harness, then analyzes harness+original source. Generated pointers/tree sizes and alias/state choices still require target invariants; generation does not prove every state is reachable through a public producer. Use existing setup/API or captured state where needed. No generic harness framework, copied target or mandatory automatic generator is warranted.

### S3 — JBMC bytecode, library model and actual frontend

Pinned sources: jbmc/README.md; doc/cprover-manual/jbmc-user-manual.md; jbmc/src/jbmc/jbmc_parse_options.cpp (defaults85-114, bounds/complexity173-225, threading330-336, result551-553, generate_function_body918-958). Quote fragment: “simple stub implementation”.

JBMC takes real compiled Java classes/JARs; debug `javac -g` preserves parameter names for counterexample inspection. A configured existing integration can run `jbmc package.Class.method --unwind 12 --unwinding-assertions --trace` with selected target entrypoint/classpath and model library. The source-supported core-models.jar models common Java library classes; it is not the actual JVM library implementation. Preserve exact application bytecode, compiler/Java version, classpath, model set and options. A colon-separated classpath in Unix examples needs the actual platform's convention; don't blindly copy it on Windows.

Actual generate_function_body substitutes simple stubs for unavailable/excluded Java method bodies, so inspect loaded methods/context and stubbing before calling a result end-to-end. The frontend warns depth/complexity-limited analysis can be unsound. `--java-threading` actually enables allow-pointer-unsoundness for shared pointers; do not advertise general sound concurrent-Java checking from a sequential recipe. Runtime exceptions and uncaught-exception checking are separate features: disabling the latter removes a property, not a defect fix. Current README explicitly distinguishes tested releases from develop builds. No Java/checker invocation occurred.

### S4 — actual result/exit distinction

Pinned source: src/util/exit_codes.h under S1 base. The selected definitions distinguish successful analysis0, verification-unsafe10, inconclusive5, usage1, parse2 and internal/task/OOM6. Code10 is also used for conversion failure in another operation. Program-only/formula-output modes can finish successfully without proving properties. Retain operation mode, actual per-property result and diagnostics; do not classify by a generic zero/nonzero or one global label. Unwinding failure, violated user property, unsupported analysis and exhausted host resource need different evidence dispositions. No actual output was fabricated as a fixture.

### S5 — Kani real Rust harness, types and domain

Pinned base: https://raw.githubusercontent.com/model-checking/kani/94253e32fe7ead82c9f1ef842bd9ddc6fae7e8ca/ . Sources: README.md; docs/src/tutorial-real-code.md; docs/src/tutorial-nondeterministic-variables.md; docs/src/tutorial-loop-unwinding.md. Quote fragment: “upper bound on the size”.

Proof harness calls the actual Rust function with valid nondeterministic values (`kani::any`, justified `Arbitrary`/constructive domains) and a real assertion, rather than copying implementation branches as a model. Bounded input/container size and loop/recursion unwind count are distinct. The selected tutorial shows `cargo kani --harness check_initialize_prefix --unwind 11`; values are example-specific. A global default only affects harnesses without an explicit unwind; override semantics differ when selecting a specific harness. A too-small unwind yields failed completeness checks and undetermined properties, not the same as the intended last-iteration bounds defect.

Valid type generation is not proof of every application invariant. Use actual constructor/setup dependencies for objects/lifetimes and leave deliberate invalid-input contracts separate. Large operation sequences/heap containers can explode solver cost; start with an actual bounded hard path/invariant that existing fuzzing misses rather than directly port a huge random workload. Kani's real-code guide says I/O is not modeled and suggests selecting a suitable actual pure component. That narrows the guarantee; it does not authorize a replacement implementation or prove the enclosing persistence/network contract.

### S6 — Kani outcomes, model omissions and artifact identity

Pinned sources: docs/src/verification-results.md; docs/src/rust-feature-support.md; docs/src/soundness.md; docs/src/undefined-behaviour.md. Quote fragments: “vacuously”; “started_at”. Success can be unreachable/over-constrained; explicit UNREACHABLE and UNDETERMINED are not newly exercised correctness. `kani::cover` can establish reachability of a chosen condition, separate from safety. Inspect every relevant property and unsupported-feature diagnostics, not only the summary.

Current support docs warn concurrency is outside scope and may be compiled sequentially; no race/linearizability assurance follows. Aliasing/immutable mutation and other UB dimensions are not comprehensively modeled. Soundness and feature-support pages differ in some detailed enabled/partial UB claims; do not merge them into a universal complete-memory-safety claim. Selected compiler/backend/version/configuration and concrete controls determine the actual lane.

The experimental export-json docs say an interrupted run can leave an earlier result file without an INCOMPLETE marker. Preserve actual fresh invocation, run start/identity, process status and export timestamps; stale files cannot establish completion. JSON schema/flags are selected-version unstable. This is a documented interpretation boundary, not a newly reproduced bug.

### S7 — concrete counterexample playback

Pinned source: docs/src/reference/experimental/concrete-playback.md under S5 base. Quote fragment: “same Kani version”. `cargo kani --harness H -Z concrete-playback --concrete-playback=print` emits a test for supported failed panic/assertion or reached cover cases. Prefer print when authored-file changes must use the editor; inplace modifies target source. Source docs' blanket git-revert suggestion is not task authorization.

The test can run through `cargo kani playback -Z concrete-playback -- TEST_NAME` after placing the emitted test in the actual harness module through the editing tool. Preserve generated values, compatible Kani/compiler options and real target call. Non-panic UB checks may have no failing native unit test because they do not necessarily trap; multiple-assertion support is limited. Do not claim every solver witness must crash natively, nor count a changed setup panic as replay of the original property. Keep model-only or unsupported replay explicitly qualified and investigate with an appropriate independent observer.

### S8 — setup, version and licenses

CBMC public download page lists Linux, Windows and macOS routes; Windows binary uses the Visual Studio command prompt, and packaged older Linux distributions can ship very old CBMC. Prefer an existing fitting selected release; check actual --version/--help/frontend configuration before a target task. Pinned CBMC LICENSE is four-clause BSD; optional external solvers have separate terms. JBMC build shares CBMC requirements and needs its model submodule/library. No tool/dependency was installed or built.

Kani docs/src/install-guide.md lists ready binaries for Linuxx86-64, macOSx86-64 and macOSarm64, with source-build route for others; no ready native Windows claim. Documented install when separately in target scope: `cargo install --locked kani-verifier --version SELECTED_VERSION`, then `cargo kani setup`. This downloads its matching compiler/support tools; merely having a new stable rustc is not the same environment. The pinned rust-toolchain.toml uses nightly-2026-10-23 and listed compiler components. README and actual LICENSE-MIT/LICENSE-APACHE confirm Kani dual MIT/Apache2.0 with separate Rust/dependency terms. No installed support/whole-project legal interpretation is claimed.

## Skill decisions for useful bugfinding

The following are plugin design adaptations supported by S1-S8 and the paper, not an externally mandated framework or guaranteed bug yield.

### Select a real target and falsifiable bounded guarantee

Read the actual public producer, enabled runtime/configuration and property. Choose a supported source/bytecode component with an independently justified invariant: e.g. index/length arithmetic, state-transition conservation, authorization effects or memory ownership. Find the actual call path/state preparation; an unconstrained internal struct may represent impossible states and manufacture bugs, while a copied “simplified” implementation proves the copy. A small abstract specification can be legitimate, but its correspondence must be checked against actual executions and counterexamples. No verified native Go BMC route was investigated here; do not claim absence of all such tools, or invent support through CBMC/Kani names. Suitable supported dependencies may be targets only when their real producer is relevant.

### Bound separate dimensions and test non-vacuity

Record input ranges, operation counts, container sizes, loop/recursion bounds, heap/object/pointer parameters, language/ABI/memory model and environment summaries separately. More unwind cannot compensate for excluding the decisive input or API. A small domain and exact completion may supply stronger evidence than a huge domain pruned by unsound heuristics. Check healthy/known wrong controls through the same harness and actual assertion; use coverage/reach observations to detect impossible assumptions or unused properties. Existing sensitivity and oracle owners supply details, not a new score/gate.

### Spend compute without weakening the experiment

Increase the dimension justified by observed missing reach: a boundary size, additional state operation, deeper loop or a different relevant implementation path. Retain per-property outcomes and explicit resource/bound exhaustion. Solver time, preprocessing, symbolic execution, formula size and replay have separate costs; apply a target/task-approved outer resource envelope without pretending a semantic cutoff preserves completeness. Do not disable unwinding/UB/assertion checks, force assumptions equal to desired results, stub the suspected behavior, or silently drop difficult paths to turn red green. If bounds cannot fit the authorized budget, report tested domain and unresolved space.

### Turn witnesses into maintained counterexamples

Retain exact source/build/bytecode/checker/solver versions, harness/preconditions/stubs, model/library, architecture/options/bounds, raw property results and trace, concrete inputs/state/operation sequence and actual replay attempts. Reproduce the same promised violation on the real supported producer using an appropriate native observer. Undefined behavior can lack a visible crash; model mismatch can create a spurious trace. Preserve both and qualify which claim is established. Reduce real input/state/sequence while keeping validity and property meaning, not just any solver failure. Failure-reduction and evidence-based-triage own detailed minimization/attribution.

## Worked advanced scenarios

These are illustrative experiment designs, not executed product findings.

1. **Last-iteration defect hidden by a small bound.** A supported parser helper promises every accepted length indexes within its buffer. Input-size bound10 and unwind1 cannot decide the full chosen domain. Inspect completeness result, raise the correct loop bound while retaining input constraints, and separate the actual index counterexample from bound failure. Replay concrete size/index through the real helper rather than a copied loop. This adds an exhaustive finite hard-path lane beyond random bytes, not an unbounded parser proof.
2. **Impossible state makes green.** A proof assumes an object simultaneously satisfies contradictory lifecycle conditions. Coverage after the assume is empty and all later assertions succeed vacuously. Restore the actual producer/state invariant, demonstrate admitted reach, then search; do not count vacuous success as tested semantics. Conversely, an impossible arbitrary internal pointer can produce a model-only failure; distinguish legal state construction from robustness tests.
3. **Java dependency silently stubbed.** Actual method bytecode is missing or excluded by context and JBMC creates a simple stub. A result concerns that abstraction, not the external library. Preserve loaded/classpath/model evidence, bring in the existing actual supported dependency or explicitly narrow the contract; no replacement implementation. A concurrent-Java option enabling an unsound pointer mode cannot establish a blanket thread-safe result.
4. **Verifier-only UB and stale output.** Kani reports a non-panic UB check that experimental playback cannot turn into a failing unit test; retain its model/trace and use a fitting independent observer rather than dismiss it. Separately an interrupted subsequent run leaves an earlier JSON success file: run identity/process evidence must prevent treating it as fresh completion. Neither case justifies invented native replay or green verification.

## Boundaries, overlap and drafter handoff

Installed golang/go-testing-advanced was read: it covers native random fuzzing/assertion/corpus/synctest basics, not bounded source-linked solver guarantees. The approved domain report establishes Barn's advanced fuzz/Toast/Elle baseline; this research did not re-audit Barn, run it or prove absence of a solver lane across branches. The capability advance is a supported real component with informative finite constraints, complete bounds and a replayable violated guarantee. Do not relabel more native fuzz iterations or a hand-copied specification as that advance.

Symbolic-concolic-execution owns path-generation/hybrid search mechanics; this skill owns explicit domain/completeness/model and property interpretation. Schedule/history/simulation specialists own their respective concurrency/environment claims. General oracle sensitivity, campaign allocation, reduction and triage remain linked owners. No universal solver adapter, harness framework, copied implementation or mandatory install is justified.

Suggested references: bounds-and-models.md (domain, ABI, assumptions and adequacy), tool-recipes.md (conditional actual CBMC/JBMC/Kani integration and result modes), counterexamples-and-replay.md (validity, UB and artifact freshness), plus common-mistakes.md/sources.yaml. Cite actual immutable URLs above with short fragments, sections and access date; local paper paths are evidence only, never distributed dependencies. Discovery pins do not freeze runtime dependencies indefinitely.

Blind evaluation can supply a real supported target/harness, a too-small unwind, contradictory assumption, missing Java method, unsupported Kani concurrency path and stale JSON from an interrupted run. Ask the evaluator to produce justified checks and retained counterexamples without giving expected diagnoses. Observe actual reach, bounds/results and same-contract replay, not named-tool or heading matches. No such target/checker/behavior/yield experiment ran here.

## Reader artifacts and verification limits

Canonical PDF675779bytes; all9 images read. External paper-reader notes preserve algorithm, constraints/property equation, parameters, all six bibliography identities, figures and historical limits; metadata, description, abstract paraphrase, citations, index, reader ledger and helper-generated keymap exist. Nested reconciliation/tagging/process/propstore excluded under Q's reader-only rule. No PDF/image enters git staging. Source abstract is retained in canonical PDF, not fully transcribed again.

Incorrect guessed kani-docs paths returned404; actual pinned repository tree located docs/src. Guessed jbmc man path returned404; actual user manual and parser supplied evidence. Some web outputs truncate long files, so executable source claims are scoped to named directly read regions; no exhaustive audit of backend/solver correctness is claimed. Missing developer researcher role file was checked at its exact path. No CBMC/JBMC/Kani/solver install, build, target/checker invocation, campaign, target mutation, git operation, host registration or publication. Report ready for independent drafting.
