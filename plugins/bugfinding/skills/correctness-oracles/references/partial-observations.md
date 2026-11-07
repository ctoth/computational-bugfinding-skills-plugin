# Partial observations and independence

## A count-only comparison

The inspected NoREC implementation generates optimized and unoptimized queries, compares counts, and throws `IgnoreMeException` when either result is the sentinel `-1`. Its reproducer also excludes sentinel outcomes ([NoRECOracle.java, check and NoRECReproducer](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/common/oracle/NoRECOracle.java)).

Use that as an exact information boundary:

| Observation | Justified interpretation |
|---|---|
| Unequal valid counts | Candidate contradiction of the relation, requiring its preconditions and raw queries/state for adjudication |
| Equal valid counts | The count relation held; equal row contents were not established |
| Sentinel/error path skipped | This comparison did not decide the relation |

These interpretations follow the actual compared values and skip branches, not an assumed universal SQL oracle. Preserve expected errors separately from completed comparisons. If the required guarantee concerns content or effects, derive another justified observation; do not discard a useful partial check because it is partial ([NoREC implementation](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/common/oracle/NoRECOracle.java)).

The linked source follows a mutable branch. Preserve the exact target/checker revision for an actual experiment; rerun source inspection before relying on a changed implementation.

## Find correlated blind spots

For each expected result, ask where it came from and which suspect path it shares. A checker that calls the same transformation to produce its expectation may reproduce the defect. A smaller model helps only when its assumptions are justified independently; a copied complex implementation has no automatic independence. This is a design test, not a requirement to buy or port a second product. NoREC's same-engine comparison is an example of an alternative relation with a narrower information boundary ([NoREC implementation](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/common/oracle/NoRECOracle.java)).

Inspect the observer as well as the expected value. If both observations normalize away the forbidden effect, agreement is uninformative for that guarantee. Elle illustrates how observability determines the dependencies that can be inferred; record missing information explicitly ([Elle §§3 and 4.3](https://arxiv.org/abs/2003.10554)).

## Keep evidence states distinct

Use only distinctions relevant to the experiment; no new outcome protocol is required. Record whether the property was evaluated, a supported guarantee was contradicted, the input was outside preconditions, the observer could not decide, or the harness failed. NoREC's sentinel path and Elle's incomplete observations are concrete reasons these states must not collapse into one pass count ([NoREC implementation](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/common/oracle/NoRECOracle.java), [Elle §4.3](https://arxiv.org/abs/2003.10554)).

A checker witness still needs inspection against the recorded history and actual contract; Elle explicitly recommends checking reported anomalies. Preserve the witness for `evidence-based-triage` instead of replacing it with a persuasive explanation ([Elle usage](https://github.com/jepsen-io/elle)).
