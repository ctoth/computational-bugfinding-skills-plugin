# Research: semantic-differential-testing

Date: 2026-11-07

## State

Per-skill primary-source research complete for drafting. This is the only owned repository output. Literature uses paper-reader and direct page images only; no target changes/execution, installation, commits or publication.

## Evidence ledger

Inspecting primary semantic differential sources and existing paper-reader artifacts. Matched input is insufficient without matched semantic state, configuration and observable effects.

## Reused literature image evidence

Yang, Chen, Eide and Regehr (PLDI 2011), *Finding and Understanding Bugs in C Compilers*, author PDF https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf ; DOI https://doi.org/10.1145/1993498.1993532 . Existing paper-reader directory: `C:/Users/Q/code/bugfinding-literature/semantic-program-generation/papers/Yang_2011_FindingCompilerBugs/`. This researcher directly read page images for printed pp. 1, 4, 5, 8 and 10 on 2026-11-07, using the installed reader's existing artifacts. Parent's semantic-generation researcher read all twelve pages and completed reader artifacts. No new ingestion, paper-process, tagging, reconciliation or extracted-text reading.

- p. 5, implementation-defined behavior: Csmith compares compiler targets within equivalent implementation-defined classes. Identical source does not establish semantic comparability across integer-width/representation/conversion differences. **Decision:** derive the contract intersection and effective configuration before comparison; classify intentional/unsupported differences separately.
- p. 5, no ground truth: agreeing implementations can share a wrong answer; the paper explicitly recognizes the limitation. Historical majority agreement is not a correctness proof. **Decision:** use disagreement to prioritize investigation, not vote to select a guilty implementation; seek independent contract/witness evidence.
- pp. 1,4-5: meaningful wrong-code comparison depends on defined, sufficiently determined program behavior and valid effects. **Decision:** invalid-input robustness can have a different oracle, but ordinary semantic equality cannot silently include undefined/unspecified outcomes.
- p. 8: conventional coverage barely changed despite discovered historical faults, and raw failures did not map automatically to distinct bugs. **Decision:** count successful semantic comparisons/effect families and reproduced causes separately from code coverage or disagreement counts.
- p. 10: reducing wrong-code cases can introduce undefined behavior. **Decision:** reduce paired initial state/program/observation together, preserving validity and selected mismatch; route general reduction mechanics to failure-reduction.

## Primary source findings (accessed 2026-11-07)

### S1: Csmith current operational example

URL: https://raw.githubusercontent.com/csmith-project/csmith/master/README.md ; About, Use Csmith, maintenance notes. Quote fragment: “bug in Csmith itself”. It documents the same generated C program compiled by GCC and Clang and compared after execution; generated programs can loop. Difference attribution includes the generator. Conditional recipe: use existing compatible Csmith/compiler installations, retain one source, compile with each selected toolchain and the installed Csmith include directory, execute with owned bounds, retain both raw outputs. The README's shell redirection examples do not override workspace editing rules. This is a C-specific integration, not a ready Go/MOO differential engine. Current README maintenance is discretionary; no unsupported release/platform assumption.

### S2: SQLancer current README

URL: https://raw.githubusercontent.com/sqlancer/sqlancer/main/README.md ; test generation/oracles, logs/reduction, DBMS-version guidance, DQP/DQE descriptions. Quote fragment: “database state”. It generates setup and queries, supports multiple complementary oracles, and logs the necessary setup with failing queries. DQP changes query plans; DQE observes selected/updated/deleted row identities. Detailed transformation relations belong to metamorphic-testing, but these are concrete evidence that compared outcomes can include effects and execution strategies, not only printed scalar returns. SQLancer tests DBMS implementation behavior, not an application's business invariant. README requires Java 11+ and Maven; MIT shown by repository. Expected-error/version support must match the selected backend; logs from a version-incompatible generator can be false alarms. No effectiveness counts are adopted.

### S3: SQLancer's actual comparator and real DQP producer

URLs: https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/ComparatorHelper.java ; https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/mysql/oracle/MySQLDQPOracle.java . Read full 185-line comparator and full 96-line MySQL DQP producer snapshots. Comparator reads first-column strings (:35-81), strips selected trailing zero spelling (:57-62), and maps expected errors to IgnoreMeException (:64-75). Comparison checks total size plus distinct-value sets (:83-120), optionally size only; an overload canonicalizes both sides (:122-131). MySQL DQP actually calls this helper for baseline and hinted/optimizer-setting executions (:62-82).

Decision: inspect the actual observer and caller rather than assume the oracle compares all typed rows/multiplicities/columns. This is a bounded information-loss observation, not a demonstrated SQLancer defect: no violating query was generated or executed. For a new contract requiring full row/bag equality, first-column/size/set comparison is insufficient by construction; choose a representation retaining the needed information. In a contract where order is unspecified, raw sequence equality can instead create false differences. Generic floating tolerances or signed-zero normalization from an existing helper are not universal semantic rules. Reproduce with setup and plan settings, since the same SQL text does not identify the same experiment.

### S4: PostgreSQL ordering contract

URL: https://www.postgresql.org/docs/current/queries-order.html ; §7.5. Quote fragment: “unspecified order”. Without ORDER BY, row order is unspecified; comparison must preserve the guarantee actually promised. An unordered bag still preserves duplicate counts; a set discards them. Derive canonicalization from the target contract, preserving original raw values. A comparator that sorts everything can hide a violation when order *is* promised.

Companion contract: https://www.postgresql.org/docs/current/sql-select.html , Description steps 6-8: SELECT ALL retains duplicates, DISTINCT eliminates them, and absent ORDER BY permits arbitrary production order. These specify different equivalence relations; neither byte equality nor set equality is universal.

## Actual Barn baseline and advance

Read existing fetched `origin/master` versions of `scripts/fuzz_differential.py`, `scripts/bench_differ.py` and `.github/workflows/fuzz.yml` directly, without fetch/checkout/target mutation or execution. The local branch/ref relation is already scoped in the domain report; no live remote claim.

- `fuzz_differential.py:89-102` decodes a single string corpus field. `:105-118` excludes non-ASCII/control transport and selected runtime facts; `:54-76` explains per-process task/scheduler/process differences. `:144-164` deduplicates and excludes before execution. Existing Unicode-versus-byte string behavior is intentional in this lane's stated contract, not permission to remove exclusions.
- `:189-206` runs the full input list through two lanes and requires one parsed record per input. `:208-220` compares completed compilation/value/error outcomes and separately records one/both missing completed outcomes. This is already generated-source corpus comparison, not novelty introduced by the skill.
- `bench_differ.py:134-168` writes the complete input sequence, makes one private database copy per lane, then runs each engine once. It does **not reset a fresh database per case in this shown producer**. Equivalent initial database bytes alone therefore do not prove equivalent logical worlds before every later effectful case. This is an inspected operational boundary, not evidence of an actual divergent state or a product bug.
- `.github/workflows/fuzz.yml:38-54` includes thirteen native targets plus the differential lane; `:112-115` selects string-source VM/compiler corpora/cache. Structured choice generation and basic cross-engine return/error comparisons are baseline.

Meaningful next capability: select a supported state/effect guarantee, ensure equivalent per-case worlds or preserve and compare the relevant sequence prefix, generate operations that actually reach the intended successful effect, and compare logical external state under the target contract. Inspect existing fixture/reset/snapshot/world-query owners before implementing a seam; no new universal adapter or copied runtime follows. Existing lane exclusions and transport limits remain evidence to research, not defects to announce. Structured-choice corpus conversion belongs to corpus-evolution; successful valid world/program generation belongs to semantic-program-generation.

### S5: SQLite optimization and state/failure testing

URL: https://www.sqlite.org/testing.html ; §2, §4.1.3, §8.5-8.6 and §9. Quote fragment: “same answer”. SQLite describes independent harnesses, joint SQL/database mutation, journal-before-data assertions and same-answer testing with optimizations enabled/disabled. These establish separate evidence dimensions: a result comparison does not itself test durable ordering, and same-engine strategy variation can expose semantic errors without an independent full reference implementation. Such comparisons still share implementation assumptions. The SQLite test-control optimization interface is not a portable application API or public universal fuzzer; inspect actual availability before recommending it. No historic counts/yield generalized.

### S6: LLVM miscompilation investigation

URL: https://llvm.org/docs/HowToSubmitABug.html ; Miscompilations and report requirements. Quote fragment: “undefined behavior”. LLVM explicitly requires investigating validity of the input program before blaming compilation, then retaining/reducing a reproducer with tool provenance. Sanitizer evidence helps examine a class of validity defects but a clean instrumented run does not prove all language preconditions. This skill owns comparison validity and qualified disagreement; instrumentation/reduction/triage remain other owners. LLVM's posting policy is target-specific and grants no publication authority.

### Tool setup, licenses and command scope

- Csmith license inspected directly at https://raw.githubusercontent.com/csmith-project/csmith/master/COPYING : two-clause BSD-style terms. Existing installation's include path and compiler target/options matter; source/runtime must be retained together. README documents compilation with two independent compiler executables; no modern common version matrix was verified. No installation performed.
- SQLancer license inspected at https://raw.githubusercontent.com/sqlancer/sqlancer/main/LICENSE.md : MIT. Verified README command shape in an existing compatible build: `java -jar sqlancer-*.jar --num-threads 4 --timeout-seconds 60 sqlite3 --oracle NoREC` (values illustrative). General flags precede backend; backend oracle flags follow it. This command is source-derived, unexecuted, a conditional specific-tool route, and uses a relational NoREC oracle rather than directly implementing cross-product effect comparison. DQP backend invocation should be obtained from the selected version's actual help/options; no guessed DQP flag is proposed here.
- This skill is behavioral guidance, so a generalized command pretending to compare arbitrary engines is inappropriate. Existing target-owned runners should consume paired inputs/state and emit raw observations; create a small adapter only for a shown target need. Runner construction is not a new plugin-wide service.

## Comparison design for the drafter

The following is plugin design derived from the source evidence, not a universal taxonomy or an empirically optimal algorithm.

### Establish what is legitimately comparable

Read both actual producers and enabled contracts. Name the behavioral guarantee, legal input/state domain, capability intersection and observable boundary. Match effective semantics: language mode, integer/float rules, collation/encoding, optional features, transaction policy and environment values where relevant. Initial artifact equality is useful but neither necessary nor sufficient for logical state equality; two engines may use different physical encodings. Preserve the setup operations or supported logical fixture that establishes equivalent state, and enough evidence to check it. Csmith p.5 establishes why target classes matter; S2 and actual Barn producers establish state/setup relevance.

Where behavior is intentionally implementation-defined, compare only inside an appropriate class or compare against permitted outcomes. Do not erase the difference by normalization without stating its contract basis. If behavior is genuinely nondeterministic, exact equality of one sample per engine is usually not the right discriminator; select a justified set/property/history oracle or controlled environment where available. If the needed control/observation is absent, record the limitation rather than install an imagined universal scheduler. Schedule and history specialists own those mechanisms.

### Observe the promised effects

Choose the smallest observation retaining what the guarantee requires: typed returned values, error class plus allowed effects, complete rows with multiplicities/order where promised, reachable object relationships, external output, or recovered state under a specified fault model. Avoid using implementation-specific serialization hashes as semantic equality unless the contract promises identical encoding. Preserve raw values and the normalization function/provenance so a mismatch is reviewable. S3's real first-column/count/set observer and S4's ordering/duplicate contracts make information loss concrete.

For logical identities, an existing mapping between returned handles may be necessary. Preserve aliasing, identity consistency and relationships; mapping every new physical ID to an arbitrary placeholder can hide object reuse/alias defects. This is a design consequence of retaining object relationships, not a claim that a generic verified identity-mapping library exists. Use the target's real observable identities and supported fixture APIs.

Expected errors are observations, not permission to skip all effect checking. Derive the allowed state boundary from the actual operation/transaction contract. Malformed output, unsupported features, input rejection, oracle skips, quota/resource aborts and missing observations are different facts. A completed-result equality claim requires the comparison to have actually executed. A timeout may deserve a resource/liveness investigation but cannot automatically select a wrong-value winner. Actual Barn source already makes several of these distinctions.

### Preserve per-case state or the causal prefix

If cases are independent, use existing reset/snapshot/fixture ownership to re-establish matched state before each case and verify it where the contract needs it. If the target bug depends on lifecycle/history, preserve and replay the full state-establishing prefix instead of forcing isolated execution and losing it. Batched workers can drift after the first mismatch; later differences may be consequences of earlier state divergence. Identify the earliest proven unequal observable state in the supported sequence where possible. Do not claim one printed-return match implies matching worlds. Actual Barn `run_lanes` is a concrete calibration input, not authorization to change Barn.

Observer operations may affect state, caches or timing. Choose supported observations and note what they alter; don't silently compare a post-observation world to an unobserved one. Strong recovery comparisons require the actual acknowledged-operation and failure contract; crash-consistency-testing owns that model. In-memory result equality does not establish durability (S5's distinct journal/failure tests).

### Test the comparator's sensitivity and adjudicate

Use a healthy pair and an independently justified wrong-result/effect control through the same producer/observation path. An effect control preserving return value demonstrates whether the observation can detect the intended effect discrepancy. Existing controls should be reused; no mandatory mutation framework or recurring approval gate is required. Harness-sensitivity owns detailed execution.

A disagreement establishes a candidate, not which implementation is incorrect. Keep both raw outcomes, source/build/configuration identities, exact input plus initial state/prefix, normalization rules, output parsing and actual replay attempts. Use contract reasoning, a simpler justified relation, independent model or appropriately different observer to adjudicate. A majority can prioritize investigation but cannot prove a winner; agreement can conceal correlated faults (Csmith p.5).

Reduce the paired case while preserving legal input, matched preconditions and the same selected result/effect relation. A smaller mismatch caused by lost setup, undefined behavior or a different intended engine policy is a new/unresolved candidate rather than the same reduced finding (Csmith p.10). Keep the original, smallest actually reproduced paired evidence, and any unresolved mismatch. Failure-reduction and evidence-based-triage own their distinct mechanics.

## Worked advanced scenarios

These are illustrative experiment designs, not executed product findings.

1. **Return equality hides a forbidden world effect.** Two engine executions return the same scalar after mutating a permissioned object. Establish equivalent principal/object/definition state via existing supported producers. Compare the promised reachable state/effects, preserving identity/alias relations. A control suppresses one required effect while preserving the return. If the comparator accepts it, the missing observation must be repaired before more input search can discover this class. Successful compile or printed equality alone does not test the guarantee.
2. **Batched state drift.** A sequence allocates/mutates objects in two private engine worlds. Even if both began with the same fixture, a prior effect mismatch can contaminate subsequent IDs/lookups. Preserve the prefix and paired logical observations; reduce to the earliest demonstrated difference where possible. Starting every replay from empty state may erase the bug. This uses the actual batched-producer boundary without asserting it currently causes a Barn defect.
3. **Bag versus set versus sequence.** A query contract retains duplicates but leaves row order unspecified. Raw sequence equality can reject legal reordered output; distinct-set equality can accept changed multiplicities. Observe full typed rows as a bag, while retaining raw results. If an ORDER BY guarantee is in scope, use an appropriate order-sensitive observation. S3/S4 provide actual source/contract evidence; no violating SQLancer query was executed.
4. **Optimization modes with shared bugs.** Same-query strategy variation can expose a wrong answer (S5), but shared evaluation or decoding can make both modes agree incorrectly. Add an independently justified complementary property for the uncovered guarantee rather than call agreement proof. If changing an option intentionally changes semantics, exclude that comparison or change its relation; do not call it an optimizer bug automatically.
5. **Expected error, unexpected effect.** Both engines reject an operation with a permitted error, yet one leaves a state change forbidden by the selected policy. Match policy and initial state; compare allowed effects as well as normalized error classes. Conversely, a documented partial-effect policy must not be compared against a full-rollback policy under an equality oracle.

## Boundaries, overlap and evaluation

Read installed golang/go-testing-advanced SKILL.md's fuzzing/corpus section. It already supplies the generic agrees-with-reference assertion idea; this skill adds semantic comparability, effect observation, per-case state/prefix and contract-backed normalization. No exhaustive marketplace novelty claim. The domain/plan reports establish other installed owners. No copied comparator framework or target implementation is justified.

Stateful-property-testing owns dependent API/model generation; semantic-program-generation owns executable program/world construction; metamorphic-testing owns relation derivation across transformed executions; configuration-differential-testing owns factor-space selection; numerical-oracles owns error/tolerance contracts. This skill owns valid paired comparison and adjudication across independently selected implementations/modes/versions. Common campaign budgeting, corpus conversion and reduction should be linked, not copied.

Suggested references: matched-state-and-effects.md (initial-state/prefix/identity/effects), comparison-and-normalization.md (contract-specific equality/outcomes), and worked-paired-cases.md where useful, plus required common-mistakes.md and sources.yaml. Inventory actual comparator/producer URLs, PostgreSQL contract sections, Csmith paper/pages and docs, SQLite testing, LLVM validity guidance. Tool recipes stay conditional and sparse in this guidance skill.

Blind behavior evaluation: provide a real stateful API contract, raw paired engine traces, matching return values but differing effects, a legal ordering difference, an expected semantic configuration difference, a missing parsed result and a replay needing a prefix. Ask the agent to derive a sensitive comparison/reproducer without the expected diagnosis. Observe actual retained artifacts, legal preconditions and distinctions; do not score exact labels or claim discovery gain from a written plan. A controlled/injected historical target can later test executable effect discovery under explicit scope. No such evaluation was performed here.

## Verification limits and completion

All primary-source claims above come from fetched official docs/source or direct reused paper images. No target tool, compiler, DBMS, differential campaign or test was run. No target changes, installs, commits, host registration, remote mutations, publication or new paper ingestion. Existing fully processed Csmith reader artifacts were reused; no collection files changed, no paper-process/tag/reconcile orchestration or raw paper-text reading.

Failed guessed SQLite3 TLP/MySQL DQE raw paths returned 404; actual MySQL DQP source supplied the real caller. SQLite sqllogictest about page presented browser verification; its detailed format was not read or claimed. SQLite SELECT page timed out; PostgreSQL official SELECT/ORDER BY contracts supplied explicitly scoped ordering/duplicate examples instead. Missing developer researcher role file recorded; explicit task constraints governed. Mutable main/latest source snapshots are dated evidence, not target reproducibility pins.

Report is complete and ready for independent drafting. Only this repository report was authored. No empirical bug-yield, model accuracy or product defect claim.
