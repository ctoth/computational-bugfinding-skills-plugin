# Worked relations

These are illustrative test designs, not executed findings.

## Duplicate- and NULL-bearing partition

For a stable table and a deterministic predicate p, compare the unfiltered projection with the bag concatenation of results filtered by p, NOT p and p IS NULL. Do not silently add DISTINCT or replace concatenation with a set. TLP's WHERE relation uses all three partitions and bag addition; other clauses require different composition ([Query Partitioning, pp.7–11](https://www.manuelrigger.at/preprints/TLP.pdf)).

Include duplicate rows and NULL-valued predicates in the example state. A control omitting the NULL partition or deleting one repeated row should violate this chosen relation. Compare complete required rows and multiplicities under the selected SQL contract; raw row order is not promised without ORDER BY ([SQLite SELECT](https://www.sqlite.org/lang_select.html)). This is a proposed sensitivity control, not a demand for a new mutation framework.

Inspect the implemented observer before accepting the control result: equal total count plus equal distinct-value sets can still hide changed multiplicities. The inspected SQLancer helper has this count/set boundary ([ComparatorHelper](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/ComparatorHelper.java)). This is an information limit, not a claim that an actual DBMS failure escaped it.

## Algebraic-looking rewrite with an effect

Before expanding BETWEEN into two comparisons, determine whether its left expression can change state or observe changing values. SQLite specifies one evaluation for BETWEEN; expansion can repeat it ([expressions, §6](https://www.sqlite.org/lang_expr.html)). Restrict to a fitting pure deterministic domain or use a justified target-owned construction retaining evaluation semantics. Keep an invalid-relation mismatch as a harness hypothesis.

## Aggregate decomposition

Do not compare average-of-partition-averages to a full average without deriving weighting, empty/NULL and numeric behavior. TLP uses aggregate-specific composition rather than a uniform operator ([Query Partitioning, p.11](https://www.manuelrigger.at/preprints/TLP.pdf)). SQLite counts non-NULL values differently from rows, returns NULL for an empty sum, and can fail on intermediate integer overflow ([aggregates](https://www.sqlite.org/lang_aggfunc.html)). Preserve these conditions or record the relation as unsupported; do not import a global epsilon.

## Stateful structural transformation

For a target whose documented contract permits a specific identity-preserving transformation, construct original world/program through existing owners, derive the transformed case, and compare the promised mapped effects. Preserve relevant principals, definitions, aliases and external conditions. This is the pack's proposed adaptation; no universal MOO transformation is asserted.

Shrink the original world/program and regenerate its dependent variant. Require the same selected violation under valid preconditions, preserving the original evidence. SQLancer similarly documents retaining setup and both related executions through reduction ([logs/reduction](https://raw.githubusercontent.com/sqlancer/sqlancer/main/README.md)); domain-specific shrinking mechanics belong to `failure-reduction`.
