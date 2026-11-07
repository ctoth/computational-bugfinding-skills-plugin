# Worked paired cases

These are this pack's illustrative experiment designs, not executed findings. Apply only where the actual target contract supports the stated guarantee. SQLancer's database setup plus query logging and SQLite's distinct answer/failure checks motivate retaining the whole experiment ([SQLancer README, Logs](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/README.md), [SQLite testing, §§3, 8.5 and 9](https://www.sqlite.org/testing.html)).

## Equal return, unequal world effect

Suppose a public API promises that a permitted mutation changes a named logical field. Establish equivalent principal/object/definition state on both implementations through existing fixture/API owners. Execute the mutation, record its result and observe the promised field plus relevant identity relationships. A candidate pair with equal returned scalars can still differ in that observation.

Exercise the same comparison with a healthy pair and a justified control that suppresses the promised effect while preserving the return. If the comparison accepts the control, more input generation cannot expose that effect through this observer. Use `harness-sensitivity` to diagnose whether the operation, control and observation actually ran; this is a proposed application of separate result/effect checking, not authorization for a new mutation framework ([SQLite's separate testing observations, §§8.5 and 9](https://www.sqlite.org/testing.html)).

Retain both initial logical worlds, setup operations, exact workload, raw returns/effects and build/configuration identities. Reduce unused objects and operations together; keep the operation successful and preserve the same forbidden effect. `semantic-program-generation`, `stateful-property-testing` and `failure-reduction` own those mechanics ([SQLancer README, Logs and Reducing bugs](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/README.md), [Csmith reduction hazard, §4](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).

## A later mismatch depends on the batch prefix

A paired batch allocates and modifies objects before a failing lookup. Inspect whether the runner creates state once per batch or per case. If an earlier operation changed one world, replay the causal prefix and compare the relevant logical observations before the lookup. Resetting both to empty state can remove the required setup; comparing only the final lookup can hide the first divergence. This is this pack's stateful comparison design, grounded in setup-preserving replay rather than a claim that every batch is defective ([SQLancer README, Logs and Reducing bugs](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/README.md)).

## Legal row reordering versus lost duplicates

A query uses PostgreSQL `SELECT ALL` without `ORDER BY`. Compare its complete rows as a bag: legal reordering should pass, changed multiplicities should fail. Under a selected `DISTINCT` contract, use the corresponding distinct relation; under a promised ordering, preserve that ordering. The same comparator is not valid for all three experiments: `SELECT ALL` returns rows "including duplicates", and unsorted order "must not be relied on" ([PostgreSQL 18 SELECT, Description steps 6 and 8](https://www.postgresql.org/docs/18/sql-select.html), [§7.5 Sorting Rows](https://www.postgresql.org/docs/18/queries-order.html)).

## Disagreement without an established winner

Two compiler runs disagree. Check input validity and effective implementation-defined choices before investigating miscompilation. Preserve both outputs and any generator defect as a competing explanation. Reduce the legal case, then adjudicate the target's guarantee; majority agreement supplies no ground truth. If evidence remains incomplete, retain the disagreement as unresolved ([LLVM 23.1.0 Miscompilations](https://releases.llvm.org/23.1.0/docs/HowToSubmitABug.html#miscompilations), [Csmith, §§2.6 and 4](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).
