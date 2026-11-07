---
name: semantic-differential-testing
description: Guides comparisons of implementations, versions or execution modes under matched semantic conditions, including observable state effects. Use when extending differential fuzzing beyond printed results, investigating disagreements, or designing contract-specific equivalence and replay.
---

# Semantic differential testing

Compare executions that are legitimately expected to agree, and observe the guarantee being tested. Identical source is insufficient when semantics differ; agreeing implementations can also share a wrong answer ([Csmith, §2.6](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).

## Establish comparability before equality

Read the actual producers, enabled configuration, input contract and observer on both sides. State the common guarantee and legal input/state domain. Separate implementation-defined choices, unsupported capabilities and invalid-input robustness from ordinary result equivalence. A compiler disagreement first needs input-validity investigation ([Csmith, §2.6](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf), [LLVM miscompilations](https://llvm.org/docs/HowToSubmitABug.html#miscompilations)).

Establish equivalent logical starting states through existing fixture/reset/API owners; identical physical bytes are not the general definition of equivalent state. For independent cases, re-establish the required state per case. For lifecycle-dependent failures, retain the causal setup prefix instead. Preserve setup alongside the compared operation, as SQLancer does for generated database cases ([SQLancer logs and reduction](https://raw.githubusercontent.com/sqlancer/sqlancer/main/README.md)). Read [matched state and effects](references/matched-state-and-effects.md) for batch drift, identities and observation boundaries.

## Observe what the contract promises

Choose typed results, permitted errors and relevant external effects; do not substitute a scalar return or implementation-specific serialization for a world-effect guarantee. Different testing observations cover different properties; SQLite separates same-answer, journal and failure testing ([SQLite testing, §§3, 8.5 and 9](https://www.sqlite.org/testing.html)). Use `correctness-oracles` for general contract derivation and `crash-consistency-testing` for recovery guarantees.

Read the actual comparison path. SQLancer's inspected MySQL DQP caller uses a first-column string observer with cardinality/set checks; that observation is not complete typed-row bag equality ([DQP caller](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/mysql/oracle/MySQLDQPOracle.java), [comparator](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/ComparatorHelper.java)). Select sequence, bag or set equivalence from the guarantee: PostgreSQL distinguishes duplicate retention from ordering, and unspecified order does not erase duplicate counts ([SELECT](https://www.postgresql.org/docs/current/sql-select.html), [ORDER BY](https://www.postgresql.org/docs/current/queries-order.html)). Read [comparison and normalization](references/comparison-and-normalization.md).

Keep input rejection, expected error, unsupported check, missing/malformed output, resource abort and completed comparison distinct where they affect the conclusion. A skipped comparison is not evidence of agreement; SQLancer's observer explicitly has skip paths ([comparator](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/ComparatorHelper.java)). Use `harness-sensitivity` to establish that the same observation rejects a representative wrong effect while accepting a healthy pair.

## Search, replay and adjudicate the paired case

Reuse existing generators/runners. Vary state and operations together when required, and compare effects at the selected boundary rather than merely extending a return-only lane. Use `semantic-program-generation` or `stateful-property-testing` for those inputs; use `configuration-differential-testing` for factor selection and `metamorphic-testing` for transformation-relation design. SQLancer and SQLite demonstrate complementary state/program and execution-mode dimensions ([SQLancer generation](https://raw.githubusercontent.com/sqlancer/sqlancer/main/README.md), [SQLite testing, §§4.1.3 and 9](https://www.sqlite.org/testing.html)).

Preserve original inputs, initial state/prefix, both build/configuration identities, raw observations, normalization and replay outcomes. Reduce the paired case while retaining legal preconditions and the selected mismatch; a smaller compiler disagreement can arise from newly introduced undefined behavior ([Csmith, §4](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)). Use `failure-reduction` for mechanics and `evidence-based-triage` for attribution and grouping.

Report the observed disagreement before assigning fault. Use the governing contract and inspectable evidence to adjudicate; majority output is not ground truth. State what actually completed, what the observer omitted, what reproduced and what remains unresolved ([Csmith, §2.6](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)). For concrete paired experiments, read [worked cases](references/worked-paired-cases.md); for misleading shortcuts, read [common mistakes](references/common-mistakes.md).
