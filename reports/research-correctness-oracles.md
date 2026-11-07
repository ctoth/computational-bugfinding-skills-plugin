# Research: correctness-oracles

Date: 2026-11-07

## State

Per-skill primary-source research complete for drafting. This report is the only owned deliverable; no drafting, target changes, installation, commits or publication.

## Evidence ledger

Primary oracle documentation, selected literature page images and the approved skill scope are being checked. Findings distinguish documented guarantees, partial observations and design inferences.

## Literature reused through direct page images

Existing completed paper-process --light collection: `C:/Users/Q/code/papers/Kingsbury_2020_ElleInferringIsolationAnomalies/`. Directly read page images 002, 006, 007 and 011 (printed pp. 3, 7, 8, 12) on 2026-11-07; no extracted text read and no collection files modified. Source: Kingsbury and Alvaro (2020), https://arxiv.org/abs/2003.10554.

- **Observation design is part of the oracle.** Unique write identities can expose read provenance; ordered append traces reveal more dependencies than ordinary overwriting registers (p. 3). Quote fragment: “recoverability”. **Decision:** design data/observations to distinguish forbidden behavior rather than presume longer random execution supplies missing information.
- **Soundness and completeness differ.** The paper's results depend on trace-recoverable observations and compatible histories; indeterminate or unobserved operations limit completeness (pp. 7-8). **Decision:** an oracle should state what a violation establishes and which legal/illegal executions can remain indistinguishable. Preserve insufficient observation as inconclusive, not healthy.
- **A useful checker can still omit a contract dimension.** Predicate dependencies are excluded from this paper's model (p. 12). **Decision:** define the guarantee first, then check the observer's scope. Do not infer a broader isolation promise from the absence of a reported non-predicate anomaly.

## Primary documentation and executable source

### S1 — SQLancer README

- URL: https://github.com/sqlancer/sqlancer ; read Test input generation and Test oracles, accessed 2026-11-07.
- Quote fragment: “multiple complementary test oracles”.
- Findings: SQLancer separates generator and validator; result correctness, expected errors and crashes are different checks. Its target is DBMS implementation correctness, not whether an application's query expresses its business intention. MIT license shown by repository.
- Decision: choose a discriminator for the actual guarantee and producer. Do not mistake a generic DBMS fuzzer for an application's state invariant checker or one successful oracle for complete correctness coverage.

### S2 — SQLancer NoRECOracle implementation

- URL: https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/common/oracle/NoRECOracle.java ; accessed 2026-11-07; inspected full 206-line source snapshot.
- Sections: check lines 96-147; NoRECReproducer lines 29-57; countRows/extractCounts lines 159-204.
- Quote fragment: “the counts mismatch”.
- Actual behavior: query pairs compare counts; sentinel -1 triggers IgnoreMeException. Reproducer excludes sentinel results; mismatch records queries/counts.
- Decision: count equality does not establish row identity. Preserve skipped checks separately and retain database setup for replay.
- Limit: main is a mutable source reference, not a reproducibility pin. Record exact implementation revision in an actual campaign; this research did not execute SQLancer. Initial NoRECBase.java guess returned 404 and supplies no evidence.

### S3 — Elle README and core implementation

- URLs: https://github.com/jepsen-io/elle ; https://raw.githubusercontent.com/jepsen-io/elle/main/src/elle/core.clj ; accessed 2026-11-07.
- Sections: README introduction/usage; core.clj dependency analyzers and explainers, lines 49-86 and 119-134.
- Quote fragment (README): “checking reported anomalies by hand”.
- Findings: histories are analyzed through dependency graphs with explanations; repository explicitly warns inference rules remain under development and recommends inspecting anomalies. Current usage supports a JVM dependency or a file/stream bridge from another language. EPL-2.0 license shown.
- Decision: a checker witness is inspectable evidence. Preserve the inference chain and verify it against actual observations/contract rather than treat a tool label as final authority. The general skill should route algorithm details to transactional-history-testing.

### S4 — SQLite testing account

- URL: https://www.sqlite.org/testing.html ; accessed 2026-11-07; read Test Harnesses, Anomaly Testing and dbsqlfuzz descriptions.
- Quote fragment: “both the SQL and the database file”.
- Findings: SQLite describes separately developed harnesses and anomaly tests for allocation, I/O and crashes. Joint SQL/database mutation reaches states SQL-only or file-only mutation can miss. dbsqlfuzz is proprietary.
- Decision: generator dimensionality and oracle dimensionality are different levers. Reuse documented public contracts and existing failure seams; do not invent a public dbsqlfuzz installation or imply one oracle covers integrity, returned answers and recovery alike.

### S5 — SQLite PRAGMA observer and configuration contracts

- URL: https://www.sqlite.org/pragma.html#pragma_integrity_check ; https://www.sqlite.org/pragma.html#pragma_foreign_key_check ; https://www.sqlite.org/pragma.html#pragma_foreign_keys ; accessed 2026-11-07; same documentation source, sections read in full around lines 366-390 and 487-513.
- Quote fragment: “does not find FOREIGN KEY errors”.
- Findings: integrity_check omits foreign-key violations; foreign_key_check returns violating references. Setting foreign_keys inside an active transaction is a no-op. Unknown pragmas may be silently ignored. Enforcement defaults can be compile-time-dependent.
- Decision: record and query the effective configuration, then select the observer for the actual guarantee. Successful configuration syntax, a generic integrity verdict and absence of a crash are inadequate substitutes. Any example using these pragmas must explicitly verify supported behavior and effective setting, not assume it.

### S6 — SQLite ON CONFLICT behavior

- URL: https://www.sqlite.org/lang_conflict.html ; accessed 2026-11-07; ABORT, FAIL, IGNORE and REPLACE sections.
- Quote fragment: “changes caused by prior SQL statements”.
- Findings: ABORT backs out the current statement while retaining earlier transaction effects. FAIL can retain earlier row changes within the failed statement. The error code alone therefore does not determine the permitted final state.
- Decision: an expected error is not a blanket exemption from effect checking. Derive the allowed effect boundary from the selected conflict policy. Conversely, asserting total transaction rollback on every constraint error creates a false finding.

### S7 — SQLite foreign-key prerequisites and semantic edge cases

- URL: https://www.sqlite.org/foreignkeys.html ; accessed 2026-11-07; Introduction and Enabling Foreign Key Support.
- Quote fragment: “enabled separately for each”.
- Findings: enforcement depends on compile support and the connection setting; querying the pragma verifies availability/enforcement. NULL child references can be legal. Enabling inside a transaction silently has no effect.
- Decision: include configuration and legal-null preconditions in any invariant. An anti-join that treats NULL children as invalid does not implement this contract. These are SQLite-specific semantics; do not transplant them into an arbitrary relation API.

## Guidance for the general oracle skill

The following is proposed plugin behavior derived from the evidence above, not an externally proven taxonomy or a mandatory new schema.

### Derive an executable discriminator before search

Use the target's actual guarantee, enabled configuration and public producer. Write enough to answer:

- What behavior is promised, for which legal inputs and states, and at which boundary (operation, statement, transaction, recovery, externally observed history)?
- Which observation would refute that promise? Include externally visible effects where the promise concerns them.
- Which observations are unavailable, ambiguous, normalized away or outside the checker model? Which inputs do not reach the property?
- How will the same evidence be replayed and adjudicated? Preserve input, initial state, operations, build/configuration, raw outcomes and any witness.

Sources supporting the decisions: Elle pp. 3,7-8,12; S2's actual comparison and IgnoreMeException paths; S5-S7's explicit observation/configuration/error-effect contracts. The detailed history/differential/metamorphic algorithms belong to their specialist skills.

### Inspect independence at the right boundary

Independence is a design question, not an all-or-nothing requirement that every oracle use a second product. Ask whether the expected behavior is derived independently of the suspect implementation path, whether the observation can hide the same defect, and what shared assumptions can make both sides agree incorrectly. Same-engine relational checking (S2) and independently maintained harnesses (S4) provide different evidence, neither blanket correctness.

Use a smaller abstract model when its contract is defensible, but do not port the target's complex implementation and call the copy independent. For a returned-result guarantee, observe returned content; for a permission/effect guarantee, inspect protected state; for acknowledged recovery, inspect recovered state under the right failure model. These are proposed selection rules, not claims about uninspected Barn behavior.

### Preserve what was and was not checked

Treat a witnessed contradiction, a successfully evaluated property, a rejected input, an expected target error, an unsupported check, an incomplete observation and a harness/infrastructure failure as different evidence. A concrete record need not introduce every category; it must avoid collapsing materially different outcomes into one success count. S2 supplies skip evidence; S3/Elle establish observation limits. A witness still needs contract/source adjudication.

An expected error may satisfy the result part of a guarantee while violating its effect part. Conversely, a timeout or a missing field can make the oracle unable to decide rather than demonstrate a product violation. Determine which case the actual contract and evidence support. Resource/liveness thresholds and scheduler details remain specialist owners.

### Assess sensitivity without reproducing the target

Use a known historical or independently justified wrong effect to see whether the new observation can distinguish it from the healthy case. Link to harness-sensitivity for execution details rather than prescribe a mutation framework. Elle p. 3 motivates checking whether the recorded data contains the required information.

## Worked source-backed examples for the drafter

These examples propose experiments; none was executed and none asserts a SQLite or Barn defect.

### 1. A constraint error with forbidden side effects

Select a disposable SQLite build and documented ABORT conflict mode. Establish pre-statement state, execute an operation that may encounter a constraint violation, then inspect both the error and post-state. The allowed comparison excludes earlier transaction effects from rollback expectations (S6). The oracle should reject changes made by the failed statement that remain despite ABORT, while accepting legal retained work from earlier statements. Run the same oracle against FAIL only after changing its effect contract; identical error outcomes do not justify identical state expectations.

Why it changes capability: a panic-only or error-code-only harness observes neither forbidden effects nor false rollback expectations. This is a contract-derived discriminator, not more random inputs. Detailed generation and fault reduction are other skills' jobs.

### 2. A healthy storage check that says nothing about an application invariant

For a documented referential-integrity guarantee, query effective per-connection foreign-key support before operations; do not set it after BEGIN and assume it took effect (S5,S7). Observe the relevant relationship, allowing legal NULL semantics, and use foreign_key_check where appropriate. An integrity_check result alone does not decide this guarantee (S5). Keep compile/configuration unsupported outcomes distinct from a violated supported guarantee.

Why it changes capability: this selects the missing observable guarantee rather than funding a longer structurally healthy search. The invariant derives from real SQLite docs; the sketch is not an application policy invented for Barn.

### 3. A count-only oracle's exact information limit

Use S2 to state the existing check's exact information boundary. If the guarantee requires content/effects, select a complementary observation with justified preconditions. Do not rewrite a valid partial oracle solely to enlarge a metric.

## Barn calibration, overlap and delivery boundaries

The source-inspected domain report already documents semantic round trips, Toast outcome replay, arbitrary verifier-accepted bytecode execution and sophisticated Elle checks. This report does not re-audit Barn or claim missing features. The desired advance is a previously unobserved contract dimension, e.g. real state effects under an explicit permitted-error boundary, demonstrated with an independently justified discriminator. Existing witnesses/controls should be reused, not sold as new work introduced by this plugin.

The general correctness-oracles skill owns contract-to-observation reasoning only. Detailed metamorphic transformations, cross-engine comparison, transaction dependency inference, linearizability models, numerical tolerances, resource/progress checks, and sensitivity execution remain the corresponding planned skills' owners. No tool installer, shared framework, assertion library or mandatory outcome schema is justified here. No first-party package changes are needed.

The approved domain report records installed Go guidance's overlap with ordinary fuzz assertions; this researcher did not independently re-audit those installed files. No exhaustive external marketplace novelty claim was researched or is needed. The new material is boundary/precondition/partial-observation discipline and concrete source-backed discriminators, not a glossary of oracle types.

## Drafter handoff and acceptance evidence

Recommended depth references: contract-to-observation worked examples and partial-oracle/independence failure cases, plus required common-mistakes.md and sources.yaml. Keep the entrypoint short and route algorithm specifics outward. Use public primary URLs and page citations, never this local paper path as a distributed dependency. Citation inventory should include the actual S2 implementation, not just product landing pages.

A blind behavioral evaluation can provide a raw API guarantee, execution/configuration evidence and a harness whose error-only check misses a state effect. Observe whether the agent identifies the promised boundary, derives a usable observation, preserves valid error cases and distinguishes insufficient evidence. Supply the underlying producer/artifacts without telling the evaluator the suspected fault. A second scenario can provide equal result counts with differing content and expected-error skips; the acceptable artifact states exactly what the existing oracle checks and proposes additional observations only where the contract requires them.

No model competence/yield experiment was performed. Paper reuse is complete for the selected Elle evidence; no new ingestion was started. No tested command recipe or runtime installation is needed for this language-neutral guidance. SQL/Java/Clojure snippets from sources are evidence, not code executed here. Sources are mutable documentation snapshots dated above; actual campaigns must preserve their selected target/checker revisions and enabled config.

## Completion

Per-skill research complete for drafting. All primary-source findings above came from actual fetched docs/source or direct reused paper page images. Report contains explicit source sections, small quote fragments, decision relevance, examples and limitations. No SKILL.md, target execution, target mutation, installation, commit or publication was performed. The referenced developer researcher role file was absent; parent and skill task constraints governed this work. The developer checkpoint required the single minimal task-note state update communicated to parent.
