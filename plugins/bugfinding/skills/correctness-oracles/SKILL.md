---
name: correctness-oracles
description: Guides executable correctness-oracle design from actual guarantees and observations. Use when a bugfinding harness checks only crashes, overlooks state effects, relies on an uncertain reference, or conflates skipped comparisons with successful checks, including JavaScript/TypeScript, Node and React harnesses that rely on process exit, unhandled rejections, uncaughtException, test-runner status, error boundaries, onRecoverableError, StrictMode, console errors or Playwright pageerror.
---

# Correctness oracles

Choose an observation that can refute the promised behavior. Specify what a successful check leaves untested: a count comparison, structural check and dependency witness observe different properties ([NoREC implementation](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/common/oracle/NoRECOracle.java), [SQLite integrity checks](https://www.sqlite.org/pragma.html#pragma_integrity_check), [Elle §4.3](https://arxiv.org/abs/2003.10554v1)).

## Derive the check from the actual boundary

Read the target's enabled configuration, public producer and governing contract. Identify legal starting states, operation preconditions, permitted errors and the promised boundary: one operation, statement, transaction, recovery or observed history. In SQLite, ABORT undoes one statement, while a deferred foreign key is "not checked until the transaction tries to COMMIT" ([SQLite ABORT](https://www.sqlite.org/lang_conflict.html), [deferred foreign keys](https://www.sqlite.org/foreignkeys.html#fk_deferred)). Query effective settings when possible; SQLite's foreign-key setting, for example, "is a no-op within a transaction" ([SQLite foreign_keys](https://www.sqlite.org/pragma.html#pragma_foreign_keys)).

Write a concrete candidate observation before scaling search:

- **Promise:** the exact prohibited result or effect, with its contract citation.
- **Observation:** actual returned content, state or witness that distinguishes that violation from allowed behavior.
- **Preconditions and blind spots:** supported configuration, valid state, omitted information and indistinguishable executions.
- **Replay evidence:** input and initial state, operation sequence, effective configuration and raw observations.

This is a compact design convention, not a required schema. Its purpose is to expose information lost by the proposed check; Elle's observation model shows why hidden dependencies cannot be recovered merely by generating more histories: blind register writes "destroy history" ([Elle §§3–4.3](https://arxiv.org/abs/2003.10554v1)). Read [contract examples](references/contract-examples.md) for worked boundaries.

In JavaScript, a process exit code, test-runner status or clean console is such an observation: its meaning depends on the effective mode, installed listeners, runner configuration and build. With an `uncaughtException` handler installed, Node's process "will exit with 0" unless the handler sets `process.exitCode` ([Node process, uncaughtException](https://raw.githubusercontent.com/nodejs/node/18b32a3b1552e199a01f1a8d9fd64aa756d3b75b/doc/api/process.md)). Read [JavaScript observation channels](references/javascript-observation-channels.md) for Node, test-runner, React and Playwright channels.

## Keep the observation independent of the suspect behavior

Trace how the expected value or invariant is obtained. Identify shared code and assumptions that could let target and checker agree on the same wrong answer. Prefer a justified abstract model, independently specified invariant or valid relation over a copied production algorithm. A second implementation is one option: SQLite's SQL Logic Test runs statements against several engines and checks "that they all get the same answers". A same-engine relation is another: SQLite reruns suites with optimizations disabled, and SQLancer's NoREC compares an optimized query with an unoptimized one ([SQLite testing §2](https://www.sqlite.org/testing.html#test_harnesses), [§9](https://www.sqlite.org/testing.html#disabled_optimization_tests), [NoREC implementation](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/common/oracle/NoRECOracle.java)).

Measure the information actually compared. Equal row counts do not establish row identity; a healthy `integrity_check` does not establish referential integrity, because it "does not find FOREIGN KEY errors". Preserve valid partial checks and add a complementary observation only when the target guarantee requires it ([NoREC implementation](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/common/oracle/NoRECOracle.java), [SQLite integrity checks](https://www.sqlite.org/pragma.html#pragma_integrity_check)). Read [partial observations](references/partial-observations.md) when choosing a reference, normalization or witness.

## Check allowed errors and their effects

Derive the permitted post-state separately from the returned status. SQLite's ABORT and FAIL both return a constraint error, but ABORT backs out the failing statement while FAIL "does not back out prior changes of the SQL statement that failed". An error-only assertion can miss a wrong effect; a blanket rollback assertion can reject legal behavior ([SQLite conflict policies](https://www.sqlite.org/lang_conflict.html)).

Select an observer for the actual promise, with valid preconditions. For SQLite referential checks, use the applicable foreign-key observation, effective enforcement setting and legal NULL semantics; do not substitute a generic integrity result ([SQLite foreign keys](https://www.sqlite.org/foreignkeys.html), [foreign_key_check](https://www.sqlite.org/pragma.html#pragma_foreign_key_check)). These are worked contracts, not defaults for arbitrary APIs.

## Preserve the check's outcome and limits

Distinguish evaluated properties from rejected inputs, expected errors, skipped checks and insufficient observations whenever that difference affects the conclusion. NoREC skips a comparison when either count is its `-1` sentinel (for example, after an expected query error) rather than counting it as equality, and reports an unexpected error as a failure. Elle's completeness depends on recorded information, and "observations are rarely complete" ([NoREC implementation](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/common/oracle/NoRECOracle.java), [Elle §4.3](https://arxiv.org/abs/2003.10554v1)).

Use `harness-sensitivity` to establish that the observation reaches and rejects a representative independently justified violation. Keep the raw witness for `evidence-based-triage`: Elle's own documentation recommends "checking reported anomalies by hand" rather than treating the label as final authority ([Elle README](https://raw.githubusercontent.com/jepsen-io/elle/4e359e597c52938b0afebb8bc42273914d68a424/README.markdown)). General search allocation belongs in `bugfinding-campaign`.

Route the chosen specialist reasoning to `semantic-differential-testing`, `metamorphic-testing`, `linearizability-checking`, `transactional-history-testing`, `numerical-oracles`, `resource-complexity-testing` or `liveness-testing`; this skill owns the contract-to-observation decision. Read [common mistakes](references/common-mistakes.md) for misleading shortcuts.

## Return the usable oracle

Return the producer, cited guarantee, effective preconditions, executable observation and outcome interpretation, with a worked allowed/forbidden distinction. State what remains unobservable and what evidence must survive replay. A witnessed contradiction supports only the guarantee and assumptions actually checked ([Elle §§4.3 and 9](https://arxiv.org/abs/2003.10554v1)).
