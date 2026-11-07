# Research: metamorphic-testing

Date: 2026-11-07

## State

Per-skill research complete for drafting. This report is the only owned repository output. Papers use paper-reader and page images only; no paper-process, target execution/mutation, installation, commit or publication.

## Evidence ledger

Primary relation/oracle documentation and selected page-image literature are being inspected. No method-effectiveness or product-bug claim is made.

### S1: Executable SQLancer relation and observer

- Primary URLs: https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/common/oracle/TLPWhereOracle.java and https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/ComparatorHelper.java ; accessed 2026-11-07. Full visible source read (187 and 185 lines respectively).
- Actual producer: TLPWhereOracle.check builds an unfiltered query, then three predicate variants and a combined result (lines 127-174). Its reproducer retains original and transformed queries, and both sides are evaluated through the same helper.
- Observation limit: ComparatorHelper reads the first column, normalizes selected trailing zeros, compares cardinality and then sets unless size-only mode is selected (lines 35-120). Equal cardinality plus equal distinct values does not prove identical duplicate multiplicities; this is a partial observation, not a verified SQLancer defect. More broadly, define bag/set/sequence and type/value equality from the promised contract, not by copying a convenient comparator.
- Conditional next decision: relation validity, transformed execution success, and observation strength are independent. Preserve expected-error/skip outcomes separately; failed transformed execution is not a successful relation evaluation. Mutable main references need a selected revision in an actual campaign. No code was executed here.

### S2: SQLite evaluation semantics

- URL: https://www.sqlite.org/lang_expr.html ; accessed 2026-11-07; Operators, BETWEEN, CASE, IN/NOT IN, Boolean Expressions.
- Documented difference: BETWEEN's left expression is evaluated once, while its pair-of-comparisons expansion may evaluate it twice (section 6). CASE variants likewise differ in evaluation multiplicity (section 7). Quote fragment: “only evaluated once”.
- Decision relevance: algebraic-looking rewrites require effect, evaluation-count, exception and nondeterminism preconditions. Repeating a stateful/volatile expression can invalidate a claimed relation. SQL arithmetic also promotes overflowing integer arithmetic to floating point; use the actual language's rules rather than mathematical integer identities.
- No transformed query was run; examples are source-backed relation-design constraints, not a current product finding.

### S3: Query Partitioning literature, paper-reader images

Primary author preprint: https://www.manuelrigger.at/preprints/TLP.pdf ; title verified visually on p.1, thirty pages rendered through paper-reader. ALL thirty images page-000 through page-029 read directly. Public DOI from SQLancer's own paper inventory: https://doi.org/10.1145/3428279 ; local preprint title page has placeholder DOI and October 2020 date, so preserve that version distinction.

- pp.2-4: a relation needs a defined composition operator, not just two apparently similar executions. SQL uses bags; UNION ALL and UNION have different duplicate semantics. Metamorphic agreement cannot supply an independent ground truth because both sides may be wrong.
- pp.6-9: ternary partitioning uses p, NOT p and p IS NULL; omitting the unknown partition violates coverage in SQL's three-valued logic. Result composition differs among WHERE/HAVING (bag addition), grouping/DISTINCT (set union), and aggregates (function-specific recombination).
- pp.8-10: the paper's oracles do not validate result order, although ORDER BY can trigger different implementation paths. GROUP BY's selected columns must match grouping columns for that particular relation. These are actual validity/observation limits, not interchangeable templates for arbitrary clauses.
- Decision relevance: derive relation, composition and observation from the exact target semantics, record preconditions, then deliberately vary execution paths while preserving the relation. Reuse existing target representation/formatter/transforms rather than add a second implementation.
- pp.11-12,25: aggregate decomposition changes intermediate overflow/rounding and empty/NULL behavior. The paper uses an epsilon for floating-point differences and excludes noncommutative aggregates, but its heuristic tolerance is not a universal numerical correctness contract. Existing numerical-oracles owns rigorous domain-specific error bounds.
- pp.16-20: repeated bug rediscovery constrained campaigns; reporting required reduction and manual contract adjudication. Some apparently valid mismatches were disputed because of dialect conversion semantics. Five TLP cases required content checks beyond cardinality. The relational observation must match the intended guarantee, and a mismatch is a candidate until its preconditions/contract are established.
- pp.20-25: similar line coverage did not imply identical oracle fault detection; extra clauses can also prevent a relevant optimization. Implementation may start with a simple relation and expand based on a demonstrated blind spot. The paper's limited model excludes transactions, window functions, sequences, nondeterministic functions and ambiguous subquery cases; do not generalize its SQL oracle into a concurrency/durability guarantee.
- Study context: six DBMSs and roughly three months of historical testing; 175 confirmed/fixed bugs, 77 logic bugs and 125 fixes at report time (pp.16-18). These are historical study observations, not predicted yield or current defects. No target campaign was run for this skill.

### S4: Current SQLite SELECT/aggregate contracts

- URLs: https://www.sqlite.org/lang_select.html (sections 2.6, 3, 4); https://www.sqlite.org/lang_aggfunc.html (aggregate input ordering, count/sum/total/avg); accessed 2026-11-07. Quote fragment from SELECT: “the order in which the rows are returned is undefined”.
- SELECT's UNION ALL retains duplicates and UNION removes them. Unordered output and tied ORDER BY terms do not define a unique row sequence. A relation expecting bag equality must retain each row's multiplicity; a sequence comparison needs its specified ordering.
- Aggregate input order can affect results; count(X) excludes NULL while count(*) counts rows. sum on an empty/all-NULL group returns NULL, total returns 0.0. Integer overflow may arise at an intermediate sum even if a real-number rearrangement would cancel later. These are concrete reasons not to transplant algebraic aggregate identities without validating actual empty/NULL/type/overflow conditions.
- Decision relevance: derive composition at the same semantic boundary as the feature. Keep general numerical error-bound derivation with numerical-oracles rather than impose the paper's epsilon globally. No query was executed.

### S5: Determinism and floating-point boundaries

- URLs: https://www.sqlite.org/deterministic.html (overview and application-defined functions); https://www.sqlite.org/floatingpoint.html (accuracy and representation); accessed 2026-11-07.
- SQLite documents non-deterministic functions whose values depend on prior statements/session/version as well as random draws. An application label claiming determinism does not establish that the function's actual implementation meets the requirement.
- Binary64 calculations are approximate and SQLite's documentation does not promise exact real-number arithmetic. Choose a justified target-specific relation/tolerance or deliberately restrict a relation's domain, not a guessed global epsilon. Temporal state and build/configuration can be part of relation preconditions even when source expressions look identical.

### S6: SQLancer setup, selected backend and replay

- URLs: https://raw.githubusercontent.com/sqlancer/sqlancer/main/README.md (Getting Started, Running/terminating, Logs, Reducing bugs); https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/sqlite3/SQLite3OracleFactory.java (lines 50-57,83-93); https://raw.githubusercontent.com/sqlancer/sqlancer/main/LICENSE.md ; accessed 2026-11-07.
- Current README states Java 11+ and Maven; use a selected compatible existing build. Factory source verifies WHERE and QUERY_PARTITIONING names; the latter composes WHERE/DISTINCT/GROUP_BY/HAVING/AGGREGATE. Backend/framework versions and the actual bundled DBMS still need to be recorded for an experiment. MIT license is confirmed from the actual license text.
- Conditional documented command shape for an existing fitting integration: `java -jar SQLANCER_JAR --num-threads 1 --timeout-seconds 120 sqlite3 --oracle QUERY_PARTITIONING`. Substitute the actual jar and choose budget values; the example is not executed or a universal default. General options precede backend name and backend oracle follows it. Verify selected build help/available backends before execution.
- README distinguishes current-statement logs from reproducer logs and requires the database setup plus both related query results when reducing TLP. Preserve actual setup and all transformed executions; the last query alone is not a semantic reproducer. No clone/build/install/target run was performed here.

## Design guidance for the drafter

These are proposed plugin decisions grounded in the sources, not a prescribed framework, new schema or guaranteed detection rate.

### Write the relation before adding compute

Identify actual target producer, promise and enabled semantics. Specify: admissible original input/state; transformation and its parameters; permitted transformed states; relation between observations; and which original/transformed outcomes make the relation undecidable. The relation may be equality, a decomposed composition, an invariant under a bijection, or another justified constraint; do not invent one from an attractive mathematical identity. Source basis: S3's feature-specific constructions and limits; S2/S4's actual evaluation/duplicate/numerical contracts.

For each transformation, show why it preserves the chosen relation, what implementation behavior it changes, and what it cannot test. A transformation producing identical code/path can add little search diversity; one that changes evaluation order/effect count can invalidate the promise. Select interaction dimensions the current lane omits: schema/data state, types, views/indexes, collation, optimizer shape, enabled feature modes, state effects, permitted errors or recovery observations—but only when the real contract supports the relation. General world/effect proposals need target-specific source reading, not a universal object-renaming rule.

### Construct and validate meaningful follow-up cases

Reuse target-owned AST/IR/formatter and existing relation transforms. Generate a valid original state/program, choose a relation applicable to that case, derive related executions constructively, and evaluate from states matched to the guarantee. Avoid restrictive rejection of almost all generated cases without observing why. Deliberately invalid inputs require a different promised error/effect relation; they are not automatically metamorphic successes or product defects.

Separate generated relations, admitted originals, successful transformed executions and actual relation evaluations. Record reasons for unsupported/expected-error/timeout/unknown outcomes. A skip, empty log or both sides failing setup is not evidence that the intended relation holds. S1 provides the real producer/observer paths; S3 establishes meaningful alternatives beyond crash-only testing. Instrumentation and campaign allocation remain other skills' owners.

Use a healthy case and a representative known or justified violation to check the intended relation can discriminate. For partitioning, omitting a required NULL partition or losing a duplicate is an observation/control fault, not a required product mutation. The sensitivity owner handles actual authorized execution; do not require installing a mutation platform.

### Retain the related execution bundle

Store actual original setup/world, input/program, transformation parameters, resulting variants, exact build/configuration, raw observations, relation/admissibility evidence, witness and exclusions. Regenerate transformed cases after shrinking the original and revalidate the relation domain. If world identity, predicate references, session state or execution order changes, all dependent variants must still describe the same admissible experiment. Source basis: S1's reproducer and S6's retained setup/query-pair guidance; world/schedule adaptation is plugin design rather than a claim of a generic reducer.

Reduce a witnessed relation violation, not any mismatch/error. Preserving the textual label while introducing a new overflow, NULL omission, illegal effect or inconsistent starting state switches the experiment. Keep original and altered candidates with qualified status; detailed algorithms belong to failure-reduction and adjudication to evidence-based-triage.

### Interpret the result at its actual strength

A valid violated relation demonstrates an inconsistency under its assumptions; it may not tell which execution is wrong. Agreement covers only the tested relation and observation. Shared implementation errors, normalized output, missing columns, duplicate-insensitive comparison or unobserved effects can conceal wrong behavior. A second independent oracle may add an anchor; running more variants is not independent correctness evidence by itself. S1 and S3 are concrete support.

Do not import paper claims of soundness, historical bug totals or a heuristic epsilon as target guarantees. Read actual dialect/version contracts, especially conversions, undefined/implementation-defined behavior, numerical ranges, nondeterminism and allowed partial effects. Preserve unresolved disputes instead of choosing a winner by majority vote. Differential testing owns cross-implementation matching; metamorphic testing owns the relation between justified related executions.

## Advanced worked scenarios

These are illustrative designs, not executed tests or current product findings.

1. **Partition a duplicate-bearing query.** On stable supported SQL state, derive p/NOT p/p IS NULL variants. Recompose WHERE results with bag addition. A state containing repeated equal rows and NULL predicates makes an incorrect UNION or missing-third-partition control observable; compare the promised row content/multiplicities, not only unique values or counts. This is directly grounded in S3/S4 and advances beyond a format round trip.
2. **Reject an invalid algebraic rewrite.** A candidate expands `x BETWEEN y AND z` to two comparisons. If x can observe changing state or produce effects, evaluation multiplicity differs under SQLite's documented semantics, so this is not an unconditional equivalence relation. Restrict x to a proven fitting pure/deterministic domain or use an existing target-owned construction preserving one evaluation. An unexpected result under an invalid relation is a harness hypothesis, not product attribution. S2/S5.
3. **Check aggregate decomposition with the right domain.** A relation partitions SUM/AVG input. Establish empty/NULL/type/collation, intermediate-overflow and rounding behavior before selecting a comparator. Small integer values alone do not prove arbitrary sums fit; a larger partial sum can overflow although the final exact sum is small. If no justified error bound/domain is available, record unsupported rather than guess epsilon. S3 pp.11-12 and S4/S5.
4. **Transform a stateful program beyond normalization.** A target's documented guarantee may allow a particular identity-preserving structural transformation. Read that guarantee and producer first; generate original world/program together, apply the transformation through the existing IR/world owner, execute under matched external conditions and compare mapped effects. Reflection, allocation identity, permission inheritance, task order and visible names can invalidate otherwise tempting renamings/permutations. This is a proposed target-specific research/evaluation path, not a verified universal MOO transformation or a finding that Barn lacks such checks.

## Existing ownership and Barn calibration

Read installed golang/go-testing-advanced native fuzzing/round-trip sections directly. Ordinary assertion and encode/decode examples are already present there. Source inventory in the approved domain report already records Barn's parser canonicalization and normalized DB idempotence; do not present another generic round trip as the new capability. This researcher did not re-audit Barn or claim an absence across its worktrees. The advance is deriving a new contract-supported relation, preserving its admissible state/effects, searching different execution paths and retaining a trustworthy relational counterexample.

Correctness-oracles owns general observation/independence reasoning; semantic generation owns valid program construction; differential owns contract intersections across engines; numerical owns precise error contracts; sensitivity, reduction and triage have their existing owners. Link those, don't reproduce their manuals. No helper code, universal transformation engine, second implementation, storage service or plugin dependency is justified by this research.

External marketplace novelty was not comprehensively audited; no uniqueness claim is made. SQLancer is a mature existing integration worth using for fitting DBMS targets, not a generic app-invariant fuzzer. General model competence was not empirically measured; generic definitions are low-value compared with these concrete admissibility/composition/replay decisions.

## Handoff and behavioral evaluation

Recommended references: relation-design.md (preconditions, effects and composition), worked-relations.md (partition/unsafe rewrite/aggregate/world examples), conditional SQLancer operation guidance if useful, required common-mistakes.md and sources.yaml. Keep SKILL.md concise and source-backed, with method-selection decisions and links; don't ship this report as technical authority. Inventory actual public URLs used above, sections/access date and paper pages. The local paper path must not be a distributed dependency.

Blind evaluation can provide a duplicate/NULL-bearing raw query family, a comparator losing multiplicity, an effectful expression rewrite and a setup/world change after reduction. Ask the evaluator to construct and investigate a valid relation without telling it the intended fault. Observe actual admissibility reasoning, relation evaluations, raw artifacts and retained witness; wording/heading matches do not establish usefulness. No such evaluation or target campaign ran in this research.

## Paper artifacts and verification limits

Canonical local paper-reader directory: C:/Users/Q/code/bugfinding-literature/metamorphic-testing/papers/Rigger_2020_QueryPartitioning. It contains PDF, all thirty directly read page images, dense page-cited notes, metadata, description, short-excerpt/paraphrased abstract, 59 bibliography identities, index, reader ledger and helper-generated keymap. Full authored abstract transcription omitted for quotation limits; abbreviated bibliography preserves every identity, not every printed author/venue field. Reader's nested reconciliation workflow was excluded by the explicit parent/Q reader-only direction; no process/tag/reconcile or propstore claim. Binary outputs stay outside the repository and staging.

Paper preprint tables/narrative have arithmetic discrepancies noted in the external notes; no detection/yield claim relies on silently reconciling them. Current code/docs are dated mutable snapshots, not fixed public contracts for every future release. Commands are documented conditional shapes, not actual executed tools. Exact target/checker/framework config and version must be preserved in actual experiments.

The supplied SQLite-specific TLPWhere filename returned 404; canonical generic producer was found and read. Initial SELECT page fetch timed out; later official fetch succeeded. Fuzzing Book Assertions URL was inaccessible; no claim comes from it. SQLite testing page was read but contributes no unique metamorphic rule, so no copied testing catalog is needed. The referenced developer researcher role file is absent; explicit assigned role/task constraints governed this work.

## Completion

Per-skill deep research complete: actual primary executable producer/observer, SQLite relation constraints, supported conditional SQLancer setup and all thirty paper-reader image pages. Only this repository report and external paper-reader artifacts authored. No SKILL.md draft, target action, dependency installation, git operation, host registration or publication.
