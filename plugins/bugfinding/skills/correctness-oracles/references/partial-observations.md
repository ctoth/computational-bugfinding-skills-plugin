# Partial observations and independence

## A count-only comparison

The inspected NoREC implementation generates optimized and unoptimized queries, compares counts, and throws `IgnoreMeException` when either result is the sentinel `-1`. Its reproducer also excludes sentinel outcomes, and a mismatch fails with "the counts mismatch" plus both queries and counts ([NoRECOracle.java, check and NoRECReproducer](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/common/oracle/NoRECOracle.java)).

The sentinel comes from `countRows`/`extractCounts` when the result set is `null` or iteration throws. The query adapter returns `null` after `checkException` accepts an error as expected (or when the driver returns no result set); any other error is thrown as `AssertionError`, and `check` attaches an error reproducer and rethrows it. Expected errors are skipped; unexpected errors are reported failures ([NoRECOracle.java, check, countRows and extractCounts](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/common/oracle/NoRECOracle.java), [SQLQueryAdapter.java, checkException and internalExecuteAndGet](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/common/query/SQLQueryAdapter.java)).

Use that as an exact information boundary:

| Observation | Justified interpretation |
|---|---|
| Unequal valid counts | Candidate contradiction of the relation, requiring its preconditions and raw queries/state for adjudication |
| Equal valid counts | The count relation held; equal row contents were not established |
| Sentinel `-1` skipped (expected error, no result set or failed result read) | This comparison did not decide the relation |
| Unexpected DBMS error | Reported failure with its own reproducer; not a count comparison |

These interpretations follow the actual compared values and skip branches, not an assumed universal SQL oracle. Preserve expected errors separately from completed comparisons. If the required guarantee concerns content or effects, derive another justified observation; do not discard a useful partial check because it is partial ([NoREC implementation](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/common/oracle/NoRECOracle.java)).

The linked source is pinned to the commit read on 2026-11-07. Preserve the exact target/checker revision for an actual experiment; rerun source inspection before relying on a later implementation.

## Find correlated blind spots

For each expected result, ask where it came from and which suspect path it shares. A checker that calls the same transformation to produce its expectation may reproduce the defect. A smaller model helps only when its assumptions are justified independently; a copied complex implementation has no automatic independence. This is a design test, not a requirement to buy or port a second product. SQLite shows both sources of independence: its SQL Logic Test compares separately developed engines, and its optimization-disabled reruns rely on the rule that SQLite "should always generate exactly the same answer" either way. NoREC's same-engine comparison is an example of an alternative relation with a narrower information boundary ([SQLite testing §2](https://www.sqlite.org/testing.html#test_harnesses), [§9](https://www.sqlite.org/testing.html#disabled_optimization_tests), [NoREC implementation](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/common/oracle/NoRECOracle.java)).

Inspect the observer as well as the expected value. If both observations normalize away the forbidden effect, agreement is uninformative for that guarantee. Elle illustrates how observability determines the dependencies that can be inferred: "The more recoverable a history is", the more non-cycle anomalies it can catch. Record missing information explicitly ([Elle §§3 and 4.3](https://arxiv.org/abs/2003.10554v1)).

## Keep evidence states distinct

Use only distinctions relevant to the experiment; no new outcome protocol is required. Record whether the property was evaluated, a supported guarantee was contradicted, the input was outside preconditions, the observer could not decide, or the harness failed. NoREC's sentinel path and Elle's incomplete observations ("observations are rarely complete") are concrete reasons these states must not collapse into one pass count ([NoREC implementation](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/common/oracle/NoRECOracle.java), [Elle §4.3](https://arxiv.org/abs/2003.10554v1)).

A checker witness still needs inspection against the recorded history and actual contract; Elle's maintainers are "not 100% confident in its inference rules yet" and recommend "checking reported anomalies by hand". Preserve the witness for `evidence-based-triage` instead of replacing it with a persuasive explanation ([Elle README](https://raw.githubusercontent.com/jepsen-io/elle/4e359e597c52938b0afebb8bc42273914d68a424/README.markdown)).
