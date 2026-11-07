# Common mistakes

Each entry is wrong first, then right, then why.

## Expanding an expression by algebra

**Wrong:** Rewrite `f(x) BETWEEN 1 AND 9` as `f(x) >= 1 AND f(x) <= 9` and call every mismatch a product defect.

**Right:** Restrict `f(x)` to a pure deterministic domain, or keep a construction that evaluates it once, before using the rewrite as a relation.

**Why:** SQLite defines BETWEEN as the pair of comparisons "except that with BETWEEN, the x expression is only evaluated once" ([expressions, §6](https://www.sqlite.org/lang_expr.html)).

## Partitioning only TRUE and FALSE

**Wrong:** Compare `SELECT * FROM t` with `SELECT * FROM t WHERE p UNION ALL SELECT * FROM t WHERE NOT p`.

**Right:** Add the third partition `UNION ALL SELECT * FROM t WHERE p IS NULL` wherever p can be NULL.

**Why:** TLP partitions on "one predicate p, one predicate NOT p, and one predicate p IS NULL" because SQL predicates are ternary ([Query Partitioning, §3](https://www.manuelrigger.at/preprints/TLP.pdf)).

## Using set equality for every result

**Wrong:** Recompose WHERE partitions with UNION, or compare distinct-value sets.

**Right:** Recompose with UNION ALL and compare multiplicities; use set union only where the feature itself removes duplicates (DISTINCT, GROUP BY).

**Why:** SQLite's UNION is UNION ALL "except that duplicate rows are removed" ([SELECT, §3](https://www.sqlite.org/lang_select.html)), and TLP uses multiset addition for WHERE and HAVING ([Query Partitioning, §3](https://www.manuelrigger.at/preprints/TLP.pdf)).

## Treating count-plus-set equality as complete result equality

**Wrong:** Report that a relation over full rows held because SQLancer's comparator passed.

**Right:** Read the real observer and state what it compared before claiming a full typed row/bag check.

**Why:** The pinned SQLancer helper reads only column 1, removes a trailing decimal point followed only by zeros, then compares size and `HashSet` contents, or size alone under its size-only option ([ComparatorHelper, lines 61–63 and 89–112](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/ComparatorHelper.java)).

## Rearranging an aggregate and choosing epsilon afterward

**Wrong:** Split `sum(x)` across partitions, see a small difference, and pick a tolerance that hides it.

**Right:** Establish intermediate overflow, empty/NULL and rounding behavior first; record the relation as unsupported where no justified bound exists.

**Why:** SQLite's sum() fails if "an integer overflow occurs at any point during the computation" ([aggregates, §3](https://www.sqlite.org/lang_aggfunc.html)), and "Floating point values are approximate." ([floating point, §1](https://www.sqlite.org/floatingpoint.html)).

## Counting expected-error skips as passing relations

**Wrong:** Report the number of generated query families as the number of relations checked.

**Right:** Count only executions where both sides completed and the comparison ran; keep skips separately with their reasons.

**Why:** The pinned helper throws IgnoreMeException for a null result or an expected error, so no comparison happens ([ComparatorHelper, lines 57–58 and 73–77](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/src/sqlancer/ComparatorHelper.java)).

## Shrinking one variant or retaining only the final query

**Wrong:** Minimize the partition query that returned the odd result and discard the setup statements and sibling queries.

**Right:** Keep setup and every dependent related execution, and after each reduction step recheck that the related queries still disagree.

**Why:** SQLancer's documented TLP reduction requires "checking that both queries still produce a different result" on the logged setup statements ([README, Logs and Reducing bugs](https://raw.githubusercontent.com/sqlancer/sqlancer/a7d60ee450e6a22ca38599c14e984a49773f4745/README.md)).

## Interpreting agreement as independent correctness proof

**Wrong:** Conclude that the target is correct because original and partitioned results always matched.

**Right:** Report agreement only as the absence of this inconsistency under this relation and observation.

**Why:** TLP "cannot establish a ground truth" because an operator or function might "consistently behave incorrectly" ([Query Partitioning, §6](https://www.manuelrigger.at/preprints/TLP.pdf)).
