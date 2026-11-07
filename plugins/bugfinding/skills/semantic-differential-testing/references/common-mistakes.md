# Common mistakes

Each entry is **Wrong** first, then **Right**, then why.

## Treating the same input file as comparable semantics

**Wrong:** "Both compilers got the same C file, so any output difference is a compiler bug."

**Right:** Check the effective contract and implementation-defined target class first; Csmith compares "within an equivalence class but not across classes" ([Csmith, §2.6](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).

**Why:** Csmith programs "do not generate the same output across compilers" that differ in integer width or signed behavior, so the difference can be legal.

## Assuming a shared initial fixture keeps every batched case equivalent

**Wrong:** "Both workers started from the same database copy, so case 40's mismatch is about case 40."

**Right:** Inspect the producer and preserve or re-establish the relevant setup or causal prefix; SQLancer logs the failing query "along with the other statements to set up the database state" ([SQLancer README, Logs](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/README.md)).

**Why:** earlier effects can diverge the two worlds, so the query alone does not identify the case.

## Treating equal returned values as equal effects

**Wrong:** "Both calls returned `1`, so the implementations agree."

**Right:** Observe the promised state/output boundary; SQLite runs "exactly the same answer" optimization comparisons separately from journal and anomaly tests ([SQLite testing, §§3, 8.5 and 9](https://www.sqlite.org/testing.html)).

**Why:** a return-only observer accepts any pair whose world effects differ behind the same return.

## Sorting everything or comparing sets universally

**Wrong:** Sort both result lists, deduplicate them and compare.

**Right:** Derive order and multiplicity from the contract and retain complete required rows: `SELECT ALL` keeps rows "including duplicates", and unsorted order "must not be relied on" ([PostgreSQL 18 SELECT, Description step 6](https://www.postgresql.org/docs/18/sql-select.html), [§7.5 Sorting Rows](https://www.postgresql.org/docs/18/queries-order.html)).

**Why:** sorting hides a promised-order violation and deduplication hides lost or extra duplicate rows.

## Trusting a helper named result equality to compare every result dimension

**Wrong:** "The oracle calls `assumeResultSetsAreEqual`, so full rows are compared."

**Right:** Read its actual caller and extraction/comparison path; SQLancer's helper reads `result.getString(1)` and compares size plus `HashSet` contents, and the MySQL DQP caller uses it ([SQLancer comparator](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/ComparatorHelper.java), [real DQP caller](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/mysql/oracle/MySQLDQPOracle.java)).

**Why:** other columns and per-value multiplicities are never observed by that path.

## Counting a missing output or expected-error skip as agreement

**Wrong:** "No assertion fired, so the two runs matched."

**Right:** Keep skipped comparisons separate from successfully evaluated equality; SQLancer's helper throws `IgnoreMeException` for a null result or an expected error ([SQLancer comparator, `getResultSetFirstColumnAsString`](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/ComparatorHelper.java)).

**Why:** a skipped case never reached the comparison, so it is no evidence either way.

## Declaring the majority implementation correct

**Wrong:** "Two of three engines agree, so the third is buggy."

**Right:** Treat disagreement as evidence to adjudicate against the contract; Csmith verifies failure-inducing programs "by hand" and calls an undetected shared wrong answer "an inherent limitation of differential testing without an oracle" ([Csmith, §2.6](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).

**Why:** agreeing implementations can share a wrong answer.

## Accepting any smaller mismatch as the reduced finding

**Wrong:** Keep whatever the reducer emits as long as the outputs still differ.

**Right:** Revalidate input validity and the selected mismatch after shrinking; Csmith found reduced C programs with new undefined behavior "are small but useless", and LLVM's first step is to "make sure it is not using undefined behavior" ([Csmith, §4](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf), [LLVM 23.1.0 Miscompilations](https://releases.llvm.org/23.1.0/docs/HowToSubmitABug.html#miscompilations)).

**Why:** a reducer can swap the original defect for an invalid input that differs for a different reason.
