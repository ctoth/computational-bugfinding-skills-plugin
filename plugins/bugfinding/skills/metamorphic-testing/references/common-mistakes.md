# Common mistakes

| Misleading shortcut | Correction |
|---|---|
| Expand an expression using algebra and call every mismatch a product defect. | Preserve actual evaluation count/effects; SQLite BETWEEN/CASE examples make this concrete ([expressions](https://www.sqlite.org/lang_expr.html)). |
| Partition only TRUE and FALSE. | Include the unknown/NULL partition where the relation requires it ([Query Partitioning, §3](https://www.manuelrigger.at/preprints/TLP.pdf)). |
| Use set equality for every result. | Derive composition and observation from duplicates/order/type guarantees ([SQLite SELECT](https://www.sqlite.org/lang_select.html)). |
| Treat count equality as complete result equality. | Inspect the real observer; the shown SQLancer helper retains first-column strings and compares count/sets ([ComparatorHelper](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/ComparatorHelper.java)). |
| Rearrange an aggregate and choose epsilon afterward. | Establish intermediate overflow, empty/NULL and rounding rules first ([aggregates](https://www.sqlite.org/lang_aggfunc.html), [floating point](https://www.sqlite.org/floatingpoint.html)). |
| Count expected-error skips as passing relations. | Record actual completed evaluations; SQLancer's helper skips unavailable/expected-error results ([ComparatorHelper](https://raw.githubusercontent.com/sqlancer/sqlancer/main/src/sqlancer/ComparatorHelper.java)). |
| Shrink one variant or retain only the final query. | Keep setup and dependent related executions, then recheck their relation ([SQLancer reduction](https://raw.githubusercontent.com/sqlancer/sqlancer/main/README.md)). |
| Interpret agreement as independent correctness proof. | Keep the relation's observation limits; shared wrong behavior can satisfy both sides ([Query Partitioning, §6](https://www.manuelrigger.at/preprints/TLP.pdf)). |
