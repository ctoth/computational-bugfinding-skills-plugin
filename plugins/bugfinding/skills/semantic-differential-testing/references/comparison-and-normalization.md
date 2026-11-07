# Comparison and normalization

Choose equality from the target contract, then inspect whether the implemented observer retains that information. Preserve raw observations alongside normalized ones. PostgreSQL's contracts distinguish duplicate elimination from row ordering ([SELECT, Description steps 6–8](https://www.postgresql.org/docs/current/sql-select.html), [ORDER BY](https://www.postgresql.org/docs/current/queries-order.html)).

| Promised result | Comparison design | Information to preserve |
|---|---|---|
| Ordered typed rows | Sequence equality under the promised tie/NULL/collation rules | Every required column, type, duplicate and promised order |
| Unordered rows retaining duplicates | Bag equality | Full rows and each row's multiplicity |
| Distinct unordered values | Set equality | Every distinct value in the contracted projection |
| Scalar/error plus effects | Result/error relation and the promised state/output observation | Error policy and permitted effects, not only printed text |

The table is a design aid, not a claim that one generic comparator implements these relations. When order has ties or nondeterministic permitted outcomes, derive the allowed relation explicitly rather than demand one byte-for-byte result. Numerical tolerances need `numerical-oracles`; do not select a global epsilon to make disagreement disappear ([PostgreSQL ordering](https://www.postgresql.org/docs/current/queries-order.html), [SQLancer's concrete numerical/string canonicalization](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/ComparatorHelper.java)).

## Inspect the real observer and caller

The inspected SQLancer helper reads first-column strings, normalizes selected spelling, and checks size plus distinct values; a real MySQL DQP caller uses it for baseline versus hinted/optimizer-setting runs. This is an actual partial observation, not proof of a DBMS or SQLancer defect ([comparator](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/ComparatorHelper.java), [DQP caller](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/mysql/oracle/MySQLDQPOracle.java)).

Illustrative comparator counterexample: `[a, a, b]` and `[a, b, b]` have equal length and equal distinct sets but different multiplicities. A contract requiring bags needs more information. Conversely, sorting all results can hide a promised-order violation. Validate the observer against the selected guarantee rather than copying a familiar helper ([PostgreSQL duplicate/order contracts](https://www.postgresql.org/docs/current/sql-select.html)).

Normalize only documented irrelevant differences. Match implementation-defined semantics or restrict the comparison to an appropriate class; do not normalize away a meaningful sign, encoding, identity or effect. Csmith explicitly restricts comparisons across implementation-defined target classes ([Csmith, §2.6](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf)).

## Preserve distinct outcomes

Record completed comparisons separately from skipped/unsupported cases and missing observations. SQLancer's helper maps selected expected errors or absent results to a skipped check; that does not establish equality ([comparator](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/ComparatorHelper.java)). A mismatch remains a candidate until the contract and input validity support attribution. A timeout cannot select the wrong-value implementation, and agreement cannot exclude shared faults ([Csmith, §2.6](https://users.cs.utah.edu/~regehr/papers/pldi11-preprint.pdf), [LLVM miscompilations](https://llvm.org/docs/HowToSubmitABug.html#miscompilations)).
