---
name: correctness-oracles
description: Guides executable correctness-oracle design from actual guarantees and observations. Use when a bugfinding harness checks only crashes, overlooks state effects, relies on an uncertain reference, or conflates skipped comparisons with successful checks.
---

# Correctness oracles

Choose an observation that can refute the promised behavior. Specify what a successful check leaves untested: a count comparison, structural check and dependency witness observe different properties ([NoREC implementation](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/common/oracle/NoRECOracle.java), [SQLite integrity checks](https://www.sqlite.org/pragma.html#pragma_integrity_check), [Elle §4.3](https://arxiv.org/abs/2003.10554)).

## Derive the check from the actual boundary

Read the target's enabled configuration, public producer and governing contract. Identify legal starting states, operation preconditions, permitted errors and the promised boundary: one operation, statement, transaction, recovery or observed history. Query effective settings when possible; SQLite, for example, ignores a foreign-key enforcement change inside a transaction ([SQLite foreign_keys](https://www.sqlite.org/pragma.html#pragma_foreign_keys)).

Write a concrete candidate observation before scaling search:

- **Promise:** the exact prohibited result or effect, with its contract citation.
- **Observation:** actual returned content, state or witness that distinguishes that violation from allowed behavior.
- **Preconditions and blind spots:** supported configuration, valid state, omitted information and indistinguishable executions.
- **Replay evidence:** input and initial state, operation sequence, effective configuration and raw observations.

This is a compact design convention, not a required schema. Its purpose is to expose information lost by the proposed check; Elle's observation model shows why hidden dependencies cannot be recovered merely by generating more histories ([Elle §§3–4.3](https://arxiv.org/abs/2003.10554)). Read [contract examples](references/contract-examples.md) for worked boundaries.

## Keep the observation independent of the suspect behavior

Trace how the expected value or invariant is obtained. Identify shared code and assumptions that could let target and checker agree on the same wrong answer. Prefer a justified abstract model, independently specified invariant or valid relation over a copied production algorithm. A second implementation is one option; SQLancer's NoREC instead compares related executions within one engine ([NoREC implementation](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/common/oracle/NoRECOracle.java)).

Measure the information actually compared. Equal row counts do not establish row identity; a structurally valid database does not establish referential integrity. Preserve valid partial checks and add a complementary observation only when the target guarantee requires it ([NoREC implementation](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/common/oracle/NoRECOracle.java), [SQLite integrity checks](https://www.sqlite.org/pragma.html#pragma_integrity_check)). Read [partial observations](references/partial-observations.md) when choosing a reference, normalization or witness.

## Check allowed errors and their effects

Derive the permitted post-state separately from the returned status. SQLite's ABORT and FAIL can return a constraint error with different allowed retained effects. An error-only assertion can miss a wrong effect; a blanket rollback assertion can reject legal behavior ([SQLite conflict policies](https://www.sqlite.org/lang_conflict.html)).

Select an observer for the actual promise, with valid preconditions. For SQLite referential checks, use the applicable foreign-key observation, effective enforcement setting and legal NULL semantics; do not substitute a generic integrity result ([SQLite foreign keys](https://www.sqlite.org/foreignkeys.html), [foreign_key_check](https://www.sqlite.org/pragma.html#pragma_foreign_key_check)). These are worked contracts, not defaults for arbitrary APIs.

## Preserve the check's outcome and limits

Distinguish evaluated properties from rejected inputs, expected errors, skipped checks and insufficient observations whenever that difference affects the conclusion. NoREC skips sentinel results rather than counting them as equality; Elle's soundness/completeness arguments depend on recorded information ([NoREC implementation](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/common/oracle/NoRECOracle.java), [Elle §4.3](https://arxiv.org/abs/2003.10554)).

Use `harness-sensitivity` to establish that the observation reaches and rejects a representative independently justified violation. Keep the raw witness for `evidence-based-triage`: Elle's own documentation recommends checking reported anomalies rather than treating the label as final authority ([Elle usage](https://github.com/jepsen-io/elle)). General search allocation belongs in `bugfinding-campaign`.

Route the chosen specialist reasoning to `semantic-differential-testing`, `metamorphic-testing`, `linearizability-checking`, `transactional-history-testing`, `numerical-oracles`, `resource-complexity-testing` or `liveness-testing`; this skill owns the contract-to-observation decision. Read [common mistakes](references/common-mistakes.md) for misleading shortcuts.

## Return the usable oracle

Return the producer, cited guarantee, effective preconditions, executable observation and outcome interpretation, with a worked allowed/forbidden distinction. State what remains unobservable and what evidence must survive replay. A witnessed contradiction supports only the guarantee and assumptions actually checked ([Elle §§4.3 and 9](https://arxiv.org/abs/2003.10554)).
