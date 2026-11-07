# Relation design

This pack uses a compact relation description: original domain, transformation, admissible execution conditions, observation/composition and undecidable outcomes. Reuse the project's existing test representation; this is a design aid, not a required schema.

## Preconditions that change the verdict

| Boundary | Inspect before accepting the relation | Concrete source |
|---|---|---|
| Evaluation count and effects | Does a rewrite repeat, omit or reorder an observable computation? | SQLite BETWEEN/CASE variants can evaluate their controlling expression different numbers of times ([expressions, §§6–7](https://www.sqlite.org/lang_expr.html)). |
| State and determinism | Do related runs observe compatible session/data state and deterministic behavior? | SQLite functions can depend on prior statements or version; a function's determinism claim needs actual implementation support ([determinism](https://www.sqlite.org/deterministic.html)). |
| Composition | Is the relation about bags, distinct sets or function-specific aggregate values? | TLP changes composition with the tested SQL feature ([Query Partitioning, pp.7–11](https://www.manuelrigger.at/preprints/TLP.pdf)). |
| Ordering and duplicates | Which information may normalization remove? | UNION removes duplicates; UNION ALL retains them, and unordered SELECT supplies no row-order promise ([SELECT, §§3–4](https://www.sqlite.org/lang_select.html)). |
| Numeric and empty cases | Are intermediate values, NULL/empty results and rounding still in the admissible domain? | SQLite sum can overflow during computation; empty sum and total differ ([aggregates](https://www.sqlite.org/lang_aggfunc.html)). Binary64 arithmetic is approximate ([floating point](https://www.sqlite.org/floatingpoint.html)). |

Choose a transformation that changes a relevant implementation path while preserving its stated relation. Adding clauses indiscriminately can suppress the optimization being investigated; the TLP study found complementary clause-specific behavior rather than coverage alone explaining detection ([Query Partitioning, §§5–6](https://www.manuelrigger.at/preprints/TLP.pdf)).

Inspect producer and observer separately. TLPWhereOracle builds the variants and preserves reproducer inputs ([producer](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/common/oracle/TLPWhereOracle.java)); ComparatorHelper can skip expected errors and observes only part of each result ([observer](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/ComparatorHelper.java)). A valid transformation does not strengthen that observation automatically.

For a new world/program relation, establish the actual guarantee before proposing renaming, permutation or reordering. This pack's proposed application is to keep mapped identities, visible state and effects together; it does not assert that every language makes such transformations equivalent. Cross-engine semantic matching belongs to `semantic-differential-testing`; precise numerical bounds belong to `numerical-oracles`.
